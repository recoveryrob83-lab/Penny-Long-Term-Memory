"""Package E owning-HQ wake state and immutable review-receipt ingestion.

GitHub review artifacts are immutable evidence. SQLite ``execution_history`` remains the single
operational ledger. This module does not close source advisories, wake Chief of Staff, or perform
Rob validation.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from .room_titles import CANONICAL_HQ_TITLES, canonical_room_title
from .worker_result_contract import artifact_checksum, artifact_path, validate_artifact
from .worker_runtime import WorkerRuntimeError
from .worker_verification import WorkerVerificationService

_HQ_WAKE_SUBMITTED = "HQ_WAKE_SUBMITTED"
_ALLOWED_REVIEW_STATES = {
    "VERIFIED",
    "REJECTED",
    "REPAIR_REQUIRED",
    "ROB_VALIDATION_REQUIRED",
}
_HEX40 = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class WorkerHqReviewWake:
    """Pointer-only owning-HQ wake derived from one validated runtime row."""

    run_id: str
    worker_id: str
    owning_department: str
    hq_chat_title: str
    marker: str
    report_path: str
    report_checksum: str
    report_commit_sha: str
    report_blob_sha: str
    verification_mode: str
    review_path: str
    instruction: str

    @property
    def idempotency_key(self) -> str:
        return f"hq-review-wake:{self.owning_department}:{self.run_id}"

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["idempotency_key"] = self.idempotency_key
        return values


@dataclass(frozen=True)
class WorkerHqReviewIngestionReceipt:
    """Deterministic immutable HQ-review ingestion result."""

    status: str
    run_id: str
    worker_id: str
    review_state: str
    review_path: str
    review_checksum: str
    review_commit_sha: str
    review_blob_sha: str
    result_state: str
    ready_for_consumption: bool
    requires_rob_validation: bool
    duplicate_suppressed: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerHqReviewService:
    """Coordinate owning-HQ wakes and ingest one immutable review receipt on the existing row."""

    _COLUMNS = {
        "hq_wake_state": "TEXT",
        "hq_wake_target": "TEXT",
        "hq_wake_marker": "TEXT",
        "hq_wake_user_turn_id": "TEXT",
        "hq_wake_receipt_json": "TEXT",
        "hq_wake_returned_to_source": "INTEGER",
        "hq_wake_sent_at": "REAL",
        "hq_review_path": "TEXT",
        "hq_review_checksum": "TEXT",
        "hq_review_commit_sha": "TEXT",
        "hq_review_blob_sha": "TEXT",
        "hq_review_state": "TEXT",
        "hq_review_reason": "TEXT",
        "hq_review_evidence_json": "TEXT",
        "hq_review_ingested_at": "REAL",
        "ready_for_consumption": "INTEGER",
        "requires_rob_validation": "INTEGER",
    }

    def __init__(self, repository_root: Path, database_path: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.database_path = database_path
        if not (self.repository_root / ".git").exists():
            raise WorkerRuntimeError("HQ review ingestion requires a local Git repository.")
        self.verification = WorkerVerificationService(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            existing = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(execution_history)").fetchall()
            }
            for column_name, column_type in self._COLUMNS.items():
                if column_name not in existing:
                    connection.execute(
                        f"ALTER TABLE execution_history ADD COLUMN {column_name} {column_type}"
                    )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_execution_history_hq_review
                ON execution_history(hq_review_state, run_id)
                """
            )

    def _git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.repository_root), *arguments],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            raise WorkerRuntimeError(f"HQ review Git evidence command failed: {detail or arguments!r}")
        return completed.stdout.strip()

    def _safe_path(self, relative_path: str) -> Path:
        candidate = (self.repository_root / relative_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise WorkerRuntimeError("HQ review path escapes the repository root.") from exc
        return candidate

    def _row(self, run_id: str) -> sqlite3.Row:
        clean_run_id = str(run_id or "").strip()
        if not clean_run_id:
            raise WorkerRuntimeError("run_id cannot be empty.")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM execution_history
                WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
                ORDER BY id
                """,
                (clean_run_id,),
            ).fetchall()
        if not rows:
            raise WorkerRuntimeError("HQ review found no authoritative Worker execution row.")
        if len(rows) > 1:
            raise WorkerRuntimeError("HQ review found ambiguous duplicate Worker execution rows.")
        return rows[0]

    @staticmethod
    def _hq_chat_title(owning_department: str) -> str:
        department = str(owning_department or "").strip().casefold()
        environment_name = f"LIFEOS_{department.upper()}_HQ_CHAT_TITLE"
        configured = str(os.getenv(environment_name) or "").strip()
        if configured:
            canonical = canonical_room_title(configured)
            if canonical not in CANONICAL_HQ_TITLES.values():
                raise WorkerRuntimeError(
                    f"Configured HQ chat title is not a canonical exact title: {configured!r}"
                )
            return canonical
        if department == "engineering":
            return CANONICAL_HQ_TITLES["engineering"]
        raise WorkerRuntimeError(
            "Cross-department HQ routing is not authorized by the Engineering-only Slice 5 pilot."
        )

    @staticmethod
    def _require_validated_report(row: sqlite3.Row) -> None:
        if str(row["result_state"] or "") != "REPORT_VALIDATED":
            raise WorkerRuntimeError("Owning-HQ review requires a REPORT_VALIDATED result.")
        required = (
            "run_id",
            "worker_id",
            "owning_department",
            "report_path",
            "report_checksum",
            "report_commit_sha",
            "report_blob_sha",
            "verification_mode",
        )
        missing = [field for field in required if not str(row[field] or "").strip()]
        if missing:
            raise WorkerRuntimeError(
                "Validated result lacks required HQ-review evidence: " + ", ".join(missing)
            )

    def build_wake(self, run_id: str) -> WorkerHqReviewWake:
        row = self._row(run_id)
        self._require_validated_report(row)
        existing_review = str(row["hq_review_state"] or "").strip()
        if existing_review:
            raise WorkerRuntimeError(f"HQ review is already recorded as {existing_review}.")
        if str(row["hq_wake_state"] or "") == _HQ_WAKE_SUBMITTED:
            raise WorkerRuntimeError("Owning-HQ review wake was already submitted; do not resend it.")
        owning_department = str(row["owning_department"])
        hq_title = self._hq_chat_title(owning_department)
        review_path = artifact_path(
            owning_department,
            str(row["worker_id"]),
            str(row["run_id"]),
            "hq_review",
            1,
        )
        marker = f"HQ-REVIEW-{row['run_id']}"
        instruction = (
            f"{marker}\n\n"
            f"Validated Worker result ready for owning-HQ review. Run: `{row['run_id']}`. "
            f"Worker: `{row['worker_id']}`. Verification mode: `{row['verification_mode']}`. "
            f"Inspect the immutable report at `{row['report_path']}` using checksum "
            f"`{row['report_checksum']}`, creation commit `{row['report_commit_sha']}`, and blob "
            f"`{row['report_blob_sha']}`. Write exactly one immutable schema-valid HQ review receipt "
            f"at `{review_path}` with VERIFIED, REJECTED, REPAIR_REQUIRED, or "
            "ROB_VALIDATION_REQUIRED. Do not copy detailed source truth into this wake, close the "
            "source advisory, wake Chief of Staff, perform Rob validation, or broaden authority."
        )
        return WorkerHqReviewWake(
            run_id=str(row["run_id"]),
            worker_id=str(row["worker_id"]),
            owning_department=owning_department,
            hq_chat_title=hq_title,
            marker=marker,
            report_path=str(row["report_path"]),
            report_checksum=str(row["report_checksum"]),
            report_commit_sha=str(row["report_commit_sha"]),
            report_blob_sha=str(row["report_blob_sha"]),
            verification_mode=str(row["verification_mode"]),
            review_path=review_path,
            instruction=instruction,
        )

    def record_wake(self, run_id: str, browser_receipt: dict[str, object]) -> WorkerHqReviewWake:
        wake = self.build_wake(run_id)
        if browser_receipt.get("status") != "submitted":
            raise WorkerRuntimeError("HQ review courier did not report a submitted user turn.")
        if browser_receipt.get("submission_confirmed") is not True:
            raise WorkerRuntimeError("HQ review courier did not confirm submission.")
        if str(browser_receipt.get("request_marker") or "") != wake.marker:
            raise WorkerRuntimeError("HQ review courier marker does not match the pending wake.")
        if str(browser_receipt.get("run_id") or "") != wake.run_id:
            raise WorkerRuntimeError("HQ review courier run ID does not match the pending wake.")
        user_turn_id = str(browser_receipt.get("user_turn_id") or "").strip()
        if not user_turn_id:
            raise WorkerRuntimeError("HQ review courier receipt has no correlated user turn ID.")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM execution_history WHERE run_id = ?", (wake.run_id,)
            ).fetchone()
            if row is None:
                raise WorkerRuntimeError("HQ review row disappeared before wake persistence.")
            if str(row["hq_wake_state"] or "") == _HQ_WAKE_SUBMITTED:
                if str(row["hq_wake_user_turn_id"] or "") == user_turn_id:
                    return wake
                raise WorkerRuntimeError("Conflicting owning-HQ wake evidence already exists.")
            connection.execute(
                """
                UPDATE execution_history SET
                    hq_wake_state = ?, hq_wake_target = ?, hq_wake_marker = ?,
                    hq_wake_user_turn_id = ?, hq_wake_receipt_json = ?,
                    hq_wake_returned_to_source = ?, hq_wake_sent_at = ?
                WHERE id = ?
                """,
                (
                    _HQ_WAKE_SUBMITTED,
                    wake.hq_chat_title,
                    wake.marker,
                    user_turn_id,
                    json.dumps(browser_receipt, sort_keys=True, ensure_ascii=False),
                    int(bool(browser_receipt.get("returned_to_source"))),
                    time.time(),
                    int(row["id"]),
                ),
            )
        return wake

    def _git_review_evidence(
        self, review_path: str, payload: dict[str, object]
    ) -> tuple[str, str, str]:
        if self._git("status", "--porcelain", "--", review_path):
            raise WorkerRuntimeError("HQ review receipt has uncommitted local changes.")
        commits = [
            line.strip()
            for line in self._git("log", "--format=%H", "--", review_path).splitlines()
            if line.strip()
        ]
        if len(commits) != 1:
            raise WorkerRuntimeError("HQ review receipt must have exactly one creation commit.")
        commit_sha = commits[0]
        if not _HEX40.fullmatch(commit_sha):
            raise WorkerRuntimeError("HQ review receipt creation commit SHA is invalid.")
        blob_sha = self._git("rev-parse", f"{commit_sha}:{review_path}")
        head_blob = self._git("rev-parse", f"HEAD:{review_path}")
        if blob_sha != head_blob:
            raise WorkerRuntimeError("HQ review receipt changed after its creation commit.")
        if not _HEX40.fullmatch(blob_sha):
            raise WorkerRuntimeError("HQ review receipt blob SHA is invalid.")
        commit_paths = {
            path.strip()
            for path in self._git(
                "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit_sha
            ).splitlines()
            if path.strip()
        }
        if commit_paths != {review_path}:
            raise WorkerRuntimeError(
                "HQ review creation commit must contain only the immutable review receipt."
            )
        return commit_sha, blob_sha, artifact_checksum(payload)

    @staticmethod
    def _validate_review_semantics(payload: dict[str, object]) -> None:
        state = str(payload.get("review_state") or "")
        if state not in _ALLOWED_REVIEW_STATES:
            raise WorkerRuntimeError("HQ review state is unsupported.")
        integrity = str(payload.get("report_integrity_state") or "")
        authority = str(payload.get("authority_compliance_state") or "")
        work = str(payload.get("work_verification_state") or "")
        ready = bool(payload.get("ready_for_consumption"))
        needs_rob = bool(payload.get("requires_rob_validation"))
        if state == "VERIFIED" and not (
            integrity == "valid"
            and authority == "compliant"
            and work == "verified"
            and ready
            and not needs_rob
        ):
            raise WorkerRuntimeError("VERIFIED HQ receipt contains inconsistent review states.")
        if state == "ROB_VALIDATION_REQUIRED" and not (
            integrity == "valid"
            and authority == "compliant"
            and work == "unavailable"
            and not ready
            and needs_rob
        ):
            raise WorkerRuntimeError(
                "ROB_VALIDATION_REQUIRED receipt must preserve valid report and authority evidence."
            )
        if state in {"REJECTED", "REPAIR_REQUIRED"} and (ready or needs_rob):
            raise WorkerRuntimeError(
                f"{state} HQ receipt cannot be consumption-ready or require Rob validation."
            )

    @staticmethod
    def _runtime_state(review_state: str) -> str:
        return {
            "VERIFIED": "HQ_VERIFIED",
            "REJECTED": "HQ_REJECTED",
            "REPAIR_REQUIRED": "REPORT_REPAIR_PENDING",
            "ROB_VALIDATION_REQUIRED": "ROB_VALIDATION_REQUIRED",
        }[review_state]

    def ingest_review(self, run_id: str) -> WorkerHqReviewIngestionReceipt:
        row = self._row(run_id)
        self._require_validated_report(row)
        review_path = artifact_path(
            str(row["owning_department"]),
            str(row["worker_id"]),
            str(row["run_id"]),
            "hq_review",
            1,
        )
        review_file = self._safe_path(review_path)
        if not review_file.is_file():
            raise WorkerRuntimeError(f"Immutable HQ review receipt is missing: {review_path}")
        try:
            payload = json.loads(review_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkerRuntimeError("HQ review receipt is not readable valid UTF-8 JSON.") from exc
        if not isinstance(payload, dict):
            raise WorkerRuntimeError("HQ review receipt must be a JSON object.")
        validate_artifact("hq_review", payload)
        self._validate_review_semantics(payload)
        expected = {
            "attempt": 1,
            "run_id": str(row["run_id"]),
            "worker_id": str(row["worker_id"]),
            "reviewing_hq": self._hq_chat_title(str(row["owning_department"])),
            "report_path": str(row["report_path"]),
        }
        mismatches = [field for field, value in expected.items() if payload.get(field) != value]
        if mismatches:
            raise WorkerRuntimeError(
                "HQ review receipt does not match canonical runtime identity: "
                + ", ".join(mismatches)
            )
        commit_sha, blob_sha, checksum = self._git_review_evidence(review_path, payload)
        existing_state = str(row["hq_review_state"] or "").strip()
        if existing_state:
            if (
                existing_state == str(payload["review_state"])
                and str(row["hq_review_path"] or "") == review_path
                and str(row["hq_review_checksum"] or "") == checksum
            ):
                return WorkerHqReviewIngestionReceipt(
                    status="succeeded",
                    run_id=str(row["run_id"]),
                    worker_id=str(row["worker_id"]),
                    review_state=existing_state,
                    review_path=review_path,
                    review_checksum=checksum,
                    review_commit_sha=str(row["hq_review_commit_sha"]),
                    review_blob_sha=str(row["hq_review_blob_sha"]),
                    result_state=str(row["result_state"]),
                    ready_for_consumption=bool(row["ready_for_consumption"]),
                    requires_rob_validation=bool(row["requires_rob_validation"]),
                    duplicate_suppressed=True,
                )
            raise WorkerRuntimeError("A conflicting immutable HQ review is already ingested.")

        review_state = str(payload["review_state"])
        if review_state == "VERIFIED":
            self.verification.review(
                str(row["run_id"]),
                "verified",
                actor=str(payload["reviewing_hq"]),
                reason=str(payload["reason"]),
            )
        elif review_state == "REJECTED":
            self.verification.review(
                str(row["run_id"]),
                "rejected",
                actor=str(payload["reviewing_hq"]),
                reason=str(payload["reason"]),
            )

        runtime_state = self._runtime_state(review_state)
        with self._connect() as connection:
            current = connection.execute(
                "SELECT * FROM execution_history WHERE id = ?", (int(row["id"]),)
            ).fetchone()
            if current is None:
                raise WorkerRuntimeError("HQ review row disappeared before ingestion.")
            if str(current["result_state"] or "") != "REPORT_VALIDATED":
                raise WorkerRuntimeError("Worker result state changed during HQ review ingestion.")
            connection.execute(
                """
                UPDATE execution_history SET
                    result_state = ?, hq_review_path = ?, hq_review_checksum = ?,
                    hq_review_commit_sha = ?, hq_review_blob_sha = ?, hq_review_state = ?,
                    hq_review_reason = ?, hq_review_evidence_json = ?,
                    hq_review_ingested_at = ?, ready_for_consumption = ?,
                    requires_rob_validation = ?
                WHERE id = ?
                """,
                (
                    runtime_state,
                    review_path,
                    checksum,
                    commit_sha,
                    blob_sha,
                    review_state,
                    str(payload["reason"]),
                    json.dumps(payload["evidence_checked"], sort_keys=True, ensure_ascii=False),
                    time.time(),
                    int(bool(payload["ready_for_consumption"])),
                    int(bool(payload["requires_rob_validation"])),
                    int(row["id"]),
                ),
            )
        return WorkerHqReviewIngestionReceipt(
            status="succeeded",
            run_id=str(row["run_id"]),
            worker_id=str(row["worker_id"]),
            review_state=review_state,
            review_path=review_path,
            review_checksum=checksum,
            review_commit_sha=commit_sha,
            review_blob_sha=blob_sha,
            result_state=runtime_state,
            ready_for_consumption=bool(payload["ready_for_consumption"]),
            requires_rob_validation=bool(payload["requires_rob_validation"]),
        )

    def records(self, limit: int = 100) -> list[dict[str, object]]:
        if limit < 1:
            raise WorkerRuntimeError("HQ review record limit must be positive.")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, run_id, worker_id, owning_department, result_state,
                       report_path, report_checksum, hq_wake_state, hq_wake_target,
                       hq_wake_user_turn_id, hq_wake_returned_to_source, hq_wake_sent_at,
                       hq_review_path, hq_review_checksum, hq_review_commit_sha,
                       hq_review_blob_sha, hq_review_state, hq_review_reason,
                       hq_review_ingested_at, ready_for_consumption,
                       requires_rob_validation
                FROM execution_history
                WHERE hq_wake_state IS NOT NULL OR hq_review_state IS NOT NULL
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def status(self, limit: int = 100) -> dict[str, object]:
        records = self.records(limit)
        return {
            "summary": {
                "total": len(records),
                "wake_submitted": sum(
                    item.get("hq_wake_state") == _HQ_WAKE_SUBMITTED for item in records
                ),
                "verified": sum(item.get("hq_review_state") == "VERIFIED" for item in records),
                "rejected": sum(item.get("hq_review_state") == "REJECTED" for item in records),
                "repair_required": sum(
                    item.get("hq_review_state") == "REPAIR_REQUIRED" for item in records
                ),
                "rob_validation_required": sum(
                    item.get("hq_review_state") == "ROB_VALIDATION_REQUIRED" for item in records
                ),
                "ready_for_consumption": sum(
                    bool(item.get("ready_for_consumption")) for item in records
                ),
            },
            "records": records,
        }


__all__ = [
    "WorkerHqReviewIngestionReceipt",
    "WorkerHqReviewService",
    "WorkerHqReviewWake",
]
