"""Package E Rob-validation receipt ingestion on the existing execution row.

GitHub validation artifacts are immutable evidence. SQLite ``execution_history`` remains the sole
operational ledger. This module does not close source advisories, wake Chief of Staff, or perform
unattended validation.
"""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from .worker_result_contract import artifact_checksum, artifact_path, validate_artifact
from .worker_runtime import WorkerRuntimeError
from .worker_verification import WorkerVerificationService, WorkerVerificationStore

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_OBSERVATION_MARKER = re.compile(r"LIFEOS_ROB_OBSERVATION=[A-Z0-9_.:-]+")


@dataclass(frozen=True)
class WorkerRobValidationIngestionReceipt:
    """Deterministic immutable Rob-validation ingestion result."""

    status: str
    run_id: str
    worker_id: str
    validation_state: str
    validation_runtime_state: str
    validation_path: str
    validation_checksum: str
    validation_commit_sha: str
    validation_blob_sha: str
    result_state: str
    ready_for_consumption: bool
    duplicate_suppressed: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerRobValidationService:
    """Ingest one explicit Rob observation without creating another ledger."""

    _COLUMNS = {
        "rob_validation_path": "TEXT",
        "rob_validation_checksum": "TEXT",
        "rob_validation_commit_sha": "TEXT",
        "rob_validation_blob_sha": "TEXT",
        "rob_validation_state": "TEXT",
        "rob_validation_runtime_state": "TEXT",
        "rob_validation_observation": "TEXT",
        "rob_validation_evidence_json": "TEXT",
        "rob_validation_ingested_at": "REAL",
    }

    def __init__(self, repository_root: Path, database_path: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.database_path = database_path
        if not (self.repository_root / ".git").exists():
            raise WorkerRuntimeError("Rob validation ingestion requires a local Git repository.")
        WorkerVerificationStore(database_path)
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
                CREATE INDEX IF NOT EXISTS idx_execution_history_rob_validation
                ON execution_history(rob_validation_state, run_id)
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
            raise WorkerRuntimeError(
                f"Rob validation Git evidence command failed: {detail or arguments!r}"
            )
        return completed.stdout.strip()

    def _safe_path(self, relative_path: str) -> Path:
        candidate = (self.repository_root / relative_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise WorkerRuntimeError("Rob validation path escapes the repository root.") from exc
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
            raise WorkerRuntimeError("Rob validation found no authoritative Worker execution row.")
        if len(rows) > 1:
            raise WorkerRuntimeError(
                "Rob validation found ambiguous duplicate Worker execution rows."
            )
        return rows[0]

    @staticmethod
    def _expected_marker(row: sqlite3.Row) -> str:
        reason = str(row["hq_review_reason"] or "")
        markers = tuple(dict.fromkeys(_OBSERVATION_MARKER.findall(reason)))
        if len(markers) != 1:
            raise WorkerRuntimeError(
                "HQ review must name exactly one deterministic Rob observation marker."
            )
        return markers[0]

    @classmethod
    def _require_pending_validation(cls, row: sqlite3.Row) -> str:
        if str(row["result_state"] or "") != "ROB_VALIDATION_REQUIRED":
            raise WorkerRuntimeError(
                "Rob validation requires a ROB_VALIDATION_REQUIRED runtime state."
            )
        if str(row["hq_review_state"] or "") != "ROB_VALIDATION_REQUIRED":
            raise WorkerRuntimeError(
                "Rob validation requires an immutable HQ ROB_VALIDATION_REQUIRED receipt."
            )
        if not bool(row["requires_rob_validation"]):
            raise WorkerRuntimeError("Runtime state does not require Rob validation.")
        if bool(row["ready_for_consumption"]):
            raise WorkerRuntimeError("Unresolved Rob validation cannot already be consumption-ready.")
        required = (
            "run_id",
            "worker_id",
            "owning_department",
            "report_path",
            "report_checksum",
            "hq_review_path",
            "hq_review_checksum",
            "hq_review_commit_sha",
            "hq_review_blob_sha",
        )
        missing = [field for field in required if not str(row[field] or "").strip()]
        if missing:
            raise WorkerRuntimeError(
                "Rob validation lacks required HQ evidence: " + ", ".join(missing)
            )
        return cls._expected_marker(row)

    def _git_validation_evidence(
        self, validation_path: str, payload: dict[str, object]
    ) -> tuple[str, str, str]:
        if self._git("status", "--porcelain", "--", validation_path):
            raise WorkerRuntimeError("Rob validation receipt has uncommitted local changes.")
        commits = [
            line.strip()
            for line in self._git("log", "--format=%H", "--", validation_path).splitlines()
            if line.strip()
        ]
        if len(commits) != 1:
            raise WorkerRuntimeError(
                "Rob validation receipt must have exactly one creation commit."
            )
        commit_sha = commits[0]
        if not _HEX40.fullmatch(commit_sha):
            raise WorkerRuntimeError("Rob validation creation commit SHA is invalid.")
        blob_sha = self._git("rev-parse", f"{commit_sha}:{validation_path}")
        head_blob = self._git("rev-parse", f"HEAD:{validation_path}")
        if blob_sha != head_blob:
            raise WorkerRuntimeError("Rob validation receipt changed after its creation commit.")
        if not _HEX40.fullmatch(blob_sha):
            raise WorkerRuntimeError("Rob validation receipt blob SHA is invalid.")
        commit_paths = {
            path.strip()
            for path in self._git(
                "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit_sha
            ).splitlines()
            if path.strip()
        }
        if commit_paths != {validation_path}:
            raise WorkerRuntimeError(
                "Rob validation creation commit must contain only the immutable receipt."
            )
        return commit_sha, blob_sha, artifact_checksum(payload)

    @staticmethod
    def _validate_semantics(payload: dict[str, object]) -> None:
        state = str(payload.get("validation_state") or "")
        ready = payload.get("ready_for_consumption") is True
        if state == "VERIFIED" and not ready:
            raise WorkerRuntimeError(
                "VERIFIED Rob validation must be ready for consumption."
            )
        if state == "REJECTED" and ready:
            raise WorkerRuntimeError(
                "REJECTED Rob validation cannot be ready for consumption."
            )

    @staticmethod
    def _runtime_state(validation_state: str) -> tuple[str, str, str]:
        if validation_state == "VERIFIED":
            return "ROB_VERIFIED", "READY_FOR_COS", "verified"
        return "ROB_REJECTED", "ROB_REJECTED", "rejected"

    def ingest_validation(self, run_id: str) -> WorkerRobValidationIngestionReceipt:
        row = self._row(run_id)
        existing_state = str(row["rob_validation_state"] or "").strip()
        validation_path = artifact_path(
            str(row["owning_department"]),
            str(row["worker_id"]),
            str(row["run_id"]),
            "rob_validation",
            1,
        )
        validation_file = self._safe_path(validation_path)
        if not validation_file.is_file():
            raise WorkerRuntimeError(
                f"Immutable Rob validation receipt is missing: {validation_path}"
            )
        try:
            payload = json.loads(validation_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkerRuntimeError(
                "Rob validation receipt is not readable valid UTF-8 JSON."
            ) from exc
        if not isinstance(payload, dict):
            raise WorkerRuntimeError("Rob validation receipt must be a JSON object.")
        validate_artifact("rob_validation", payload)
        self._validate_semantics(payload)

        expected = {
            "attempt": 1,
            "run_id": str(row["run_id"]),
            "worker_id": str(row["worker_id"]),
            "validator": "Rob",
        }
        mismatches = [field for field, value in expected.items() if payload.get(field) != value]
        if mismatches:
            raise WorkerRuntimeError(
                "Rob validation receipt does not match canonical runtime identity: "
                + ", ".join(mismatches)
            )

        if existing_state:
            marker = self._expected_marker(row)
        else:
            marker = self._require_pending_validation(row)
        observation = str(payload["observation"])
        evidence = tuple(str(value) for value in payload["evidence_references"])
        expected_hq_reference = (
            f"hq-review:{row['hq_review_path']}@{row['hq_review_blob_sha']}"
        )
        expected_observation_reference = f"rob-observation:{marker}"
        missing_references = [
            reference
            for reference in (expected_hq_reference, expected_observation_reference)
            if reference not in evidence
        ]
        if marker not in observation:
            raise WorkerRuntimeError(
                "Rob validation observation does not contain the exact HQ-requested marker."
            )
        if missing_references:
            raise WorkerRuntimeError(
                "Rob validation receipt omits required evidence: "
                + ", ".join(missing_references)
            )

        commit_sha, blob_sha, checksum = self._git_validation_evidence(
            validation_path, payload
        )
        if existing_state:
            if (
                existing_state == str(payload["validation_state"])
                and str(row["rob_validation_path"] or "") == validation_path
                and str(row["rob_validation_checksum"] or "") == checksum
                and str(row["rob_validation_commit_sha"] or "") == commit_sha
                and str(row["rob_validation_blob_sha"] or "") == blob_sha
            ):
                return WorkerRobValidationIngestionReceipt(
                    status="succeeded",
                    run_id=str(row["run_id"]),
                    worker_id=str(row["worker_id"]),
                    validation_state=existing_state,
                    validation_runtime_state=str(row["rob_validation_runtime_state"]),
                    validation_path=validation_path,
                    validation_checksum=checksum,
                    validation_commit_sha=commit_sha,
                    validation_blob_sha=blob_sha,
                    result_state=str(row["result_state"]),
                    ready_for_consumption=bool(row["ready_for_consumption"]),
                    duplicate_suppressed=True,
                )
            raise WorkerRuntimeError(
                "A conflicting immutable Rob validation is already ingested."
            )

        validation_state = str(payload["validation_state"])
        validation_runtime_state, result_state, verification_state = self._runtime_state(
            validation_state
        )
        now = time.time()
        with self._connect() as connection:
            current = connection.execute(
                "SELECT * FROM execution_history WHERE id = ?", (int(row["id"]),)
            ).fetchone()
            if current is None:
                raise WorkerRuntimeError("Rob validation row disappeared before ingestion.")
            self._require_pending_validation(current)
            persisted_verification = str(current["worker_verification_state"] or "").strip()
            if persisted_verification not in {"", "pending"}:
                raise WorkerRuntimeError(
                    "Worker verification state changed before Rob validation ingestion."
                )
            connection.execute(
                """
                UPDATE execution_history SET
                    result_state = ?, rob_validation_path = ?,
                    rob_validation_checksum = ?, rob_validation_commit_sha = ?,
                    rob_validation_blob_sha = ?, rob_validation_state = ?,
                    rob_validation_runtime_state = ?, rob_validation_observation = ?,
                    rob_validation_evidence_json = ?, rob_validation_ingested_at = ?,
                    ready_for_consumption = ?, requires_rob_validation = 0,
                    worker_verification_state = ?, worker_verification_updated_at = ?,
                    worker_verification_actor = 'Rob', worker_verification_reason = ?
                WHERE id = ?
                """,
                (
                    result_state,
                    validation_path,
                    checksum,
                    commit_sha,
                    blob_sha,
                    validation_state,
                    validation_runtime_state,
                    observation,
                    json.dumps(evidence, sort_keys=True, ensure_ascii=False),
                    now,
                    int(bool(payload["ready_for_consumption"])),
                    verification_state,
                    now,
                    observation,
                    int(row["id"]),
                ),
            )

        return WorkerRobValidationIngestionReceipt(
            status="succeeded",
            run_id=str(row["run_id"]),
            worker_id=str(row["worker_id"]),
            validation_state=validation_state,
            validation_runtime_state=validation_runtime_state,
            validation_path=validation_path,
            validation_checksum=checksum,
            validation_commit_sha=commit_sha,
            validation_blob_sha=blob_sha,
            result_state=result_state,
            ready_for_consumption=bool(payload["ready_for_consumption"]),
        )

    def records(self, limit: int = 100) -> list[dict[str, object]]:
        if limit < 1:
            raise WorkerRuntimeError("Rob validation record limit must be positive.")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, run_id, worker_id, owning_department, result_state,
                       hq_review_state, hq_review_path, hq_review_blob_sha,
                       rob_validation_path, rob_validation_checksum,
                       rob_validation_commit_sha, rob_validation_blob_sha,
                       rob_validation_state, rob_validation_runtime_state,
                       rob_validation_observation, rob_validation_ingested_at,
                       ready_for_consumption, requires_rob_validation
                FROM execution_history
                WHERE requires_rob_validation = 1 OR rob_validation_state IS NOT NULL
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
                "pending": sum(
                    bool(item.get("requires_rob_validation"))
                    and item.get("rob_validation_state") is None
                    for item in records
                ),
                "verified": sum(
                    item.get("rob_validation_state") == "VERIFIED" for item in records
                ),
                "rejected": sum(
                    item.get("rob_validation_state") == "REJECTED" for item in records
                ),
                "ready_for_cos": sum(
                    item.get("result_state") == "READY_FOR_COS" for item in records
                ),
            },
            "records": records,
        }


__all__ = [
    "WorkerRobValidationIngestionReceipt",
    "WorkerRobValidationService",
]
