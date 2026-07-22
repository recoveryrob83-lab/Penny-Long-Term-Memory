"""Deterministic Package E Worker result ingestion into the existing runtime row.

GitHub result artifacts remain immutable evidence. SQLite ``execution_history`` remains the
single operational ledger. This module discovers and validates one canonical Worker report,
calculates stored-content evidence, and advances the existing run row without creating a second
queue, ledger, or advisory lifecycle.
"""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_result_contract import (
    WorkerResultContractError,
    artifact_checksum,
    validate_artifact,
)
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService
from .worker_verification import WorkerVerificationStore

_REPORT_STATE_DISCOVERED = "REPORT_DISCOVERED"
_REPORT_STATE_REJECTED = "REPORT_REJECTED"
_REPORT_STATE_VALIDATED = "REPORT_VALIDATED"
_HEX40 = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class GitArtifactEvidence:
    """Repository evidence for one committed immutable report artifact."""

    path: str
    commit_sha: str
    blob_sha: str
    checksum: str
    commit_paths: tuple[str, ...]


@dataclass(frozen=True)
class WorkerResultIngestionReceipt:
    """Deterministic same-row ingestion result."""

    status: str
    run_id: str
    worker_id: str
    task_id: str
    task_revision: int
    report_state: str
    report_path: str
    report_attempt: int
    report_checksum: str
    report_commit_sha: str
    report_blob_sha: str
    controlled_outcome: str
    verification_mode: str
    verification_state: str
    completion_state: str
    hq_review_required: bool
    duplicate_suppressed: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerResultIngester:
    """Validate immutable Worker reports and update only the existing execution row."""

    _COLUMNS = {
        "result_state": "TEXT",
        "report_path": "TEXT",
        "report_attempt": "INTEGER",
        "report_checksum": "TEXT",
        "report_commit_sha": "TEXT",
        "report_blob_sha": "TEXT",
        "report_discovered_at": "REAL",
        "report_validated_at": "REAL",
        "report_validation_errors_json": "TEXT",
        "approval_required_discovered": "INTEGER",
        "worker_failure_reason": "TEXT",
    }

    def __init__(
        self,
        repository_root: Path,
        database_path: Path,
        runtime: WorkerRuntimeService | None = None,
    ) -> None:
        self.repository_root = repository_root.resolve()
        self.database_path = database_path
        self.runtime = runtime or WorkerRuntimeService(database_path)
        WorkerVerificationStore(database_path)
        if not (self.repository_root / ".git").exists():
            raise WorkerRuntimeError("Worker result ingestion requires a local Git repository.")
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
                CREATE INDEX IF NOT EXISTS idx_execution_history_result_state
                ON execution_history(result_state, run_id)
                """
            )

    def _safe_path(self, relative_path: str) -> Path:
        candidate = (self.repository_root / relative_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise WorkerRuntimeError("Worker result path escapes the repository root.") from exc
        return candidate

    def _git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.repository_root), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            raise WorkerRuntimeError(f"Git evidence command failed: {detail or arguments!r}")
        return completed.stdout.strip()

    def _git_artifact_evidence(
        self,
        report_path: str,
        payload: dict[str, object],
        requested_write_scopes: tuple[str, ...],
    ) -> GitArtifactEvidence:
        if self._git("status", "--porcelain", "--", report_path):
            raise WorkerRuntimeError("Worker report has uncommitted local changes.")
        commits = [
            line.strip()
            for line in self._git("log", "--format=%H", "--", report_path).splitlines()
            if line.strip()
        ]
        if not commits:
            raise WorkerRuntimeError("Worker report is not present in Git history.")
        if len(commits) != 1:
            raise WorkerRuntimeError("Worker report is not immutable; multiple commits touch it.")
        commit_sha = commits[0]
        if not _HEX40.fullmatch(commit_sha):
            raise WorkerRuntimeError("Worker report creation commit SHA is invalid.")
        blob_sha = self._git("rev-parse", f"{commit_sha}:{report_path}")
        head_blob_sha = self._git("rev-parse", f"HEAD:{report_path}")
        if blob_sha != head_blob_sha:
            raise WorkerRuntimeError("Worker report content changed after its creation commit.")
        if not _HEX40.fullmatch(blob_sha):
            raise WorkerRuntimeError("Worker report blob SHA is invalid.")
        commit_paths = tuple(
            sorted(
                path.strip()
                for path in self._git(
                    "diff-tree",
                    "--root",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    commit_sha,
                ).splitlines()
                if path.strip()
            )
        )
        if report_path not in commit_paths:
            raise WorkerRuntimeError("Worker report creation commit does not contain the report path.")
        unauthorized = sorted(set(commit_paths) - set(requested_write_scopes))
        if unauthorized:
            raise WorkerRuntimeError(
                "Worker report creation commit contains paths outside requested write scopes: "
                + ", ".join(unauthorized)
            )
        return GitArtifactEvidence(
            path=report_path,
            commit_sha=commit_sha,
            blob_sha=blob_sha,
            checksum=artifact_checksum(payload),
            commit_paths=commit_paths,
        )

    @staticmethod
    def _expected_identity(advisory: ExecutionReadyAdvisory) -> dict[str, object]:
        envelope = advisory.envelope()
        return {
            "wrapper_id": envelope.wrapper_id,
            "run_id": envelope.run_id,
            "worker_id": envelope.worker_id,
            "task_id": envelope.task_id,
            "task_revision": envelope.task_revision,
            "procedure_id": envelope.procedure_id,
            "procedure_version": envelope.procedure_version,
            "authorization_source": envelope.authorization_source,
            "verification_mode": envelope.verification_mode,
        }

    def _validate_report_correlation(
        self,
        advisory: ExecutionReadyAdvisory,
        profile: WorkerRegistryEntry,
        payload: dict[str, object],
    ) -> None:
        contract = advisory.result_contract
        if contract is None:
            raise WorkerRuntimeError("Canonical assignment has no Worker result contract.")
        errors: list[str] = []
        for field_name, expected in self._expected_identity(advisory).items():
            if payload.get(field_name) != expected:
                errors.append(f"report {field_name} does not match the canonical assignment")
        expected_profile = {
            "profile_version": profile.profile_version,
            "owning_department": profile.owning_department,
            "attempt": contract.attempt,
        }
        for field_name, expected in expected_profile.items():
            if payload.get(field_name) != expected:
                errors.append(f"report {field_name} does not match canonical Worker state")
        if profile.worker_id != advisory.target_worker_id:
            errors.append("registered Worker does not match the canonical assignment")
        actual_reads = set(payload.get("actual_read_scopes") or [])
        actual_writes = set(payload.get("actual_write_scopes") or [])
        actual_tools = set(payload.get("actual_tools") or [])
        allowed_reads = set(advisory.requested_read_scopes) | set(
            advisory.requested_write_scopes
        )
        unauthorized_reads = sorted(actual_reads - allowed_reads)
        unauthorized_writes = sorted(actual_writes - set(advisory.requested_write_scopes))
        unauthorized_tools = sorted(actual_tools - set(advisory.requested_tools))
        if unauthorized_reads:
            errors.append("actual read scopes exceed assignment: " + ", ".join(unauthorized_reads))
        if unauthorized_writes:
            errors.append("actual write scopes exceed assignment: " + ", ".join(unauthorized_writes))
        if unauthorized_tools:
            errors.append("actual tools exceed assignment: " + ", ".join(unauthorized_tools))
        if contract.result_path not in actual_writes:
            errors.append("actual write scopes do not include the exact report path")
        if payload.get("controlled_outcome") == "IMPLEMENT":
            missing_reads = sorted(set(advisory.requested_read_scopes) - actual_reads)
            if missing_reads:
                errors.append("implemented report omits requested read scopes: " + ", ".join(missing_reads))
            if payload.get("completion_state") != "completed":
                errors.append("IMPLEMENT requires completion_state completed")
            if payload.get("verification_state") != "pending":
                errors.append("IMPLEMENT requires pending Department HQ verification")
            if payload.get("failure_reason") is not None:
                errors.append("IMPLEMENT report cannot contain a failure reason")
        if payload.get("controlled_outcome") == "REPORT_AND_HOLD" and not payload.get(
            "failure_reason"
        ):
            errors.append("REPORT_AND_HOLD requires a failure reason")
        evidence_paths: set[str] = set()
        allowed_evidence_paths = (
            set(advisory.source_references)
            | set(advisory.requested_read_scopes)
            | set(advisory.requested_write_scopes)
        )
        for reference in payload.get("evidence_references") or []:
            text = str(reference)
            if "@" not in text:
                errors.append(f"evidence reference lacks path correlation: {text}")
                continue
            path, witness = text.rsplit("@", 1)
            evidence_paths.add(path)
            if path not in allowed_evidence_paths:
                errors.append(f"evidence reference path is outside assignment: {path}")
                continue
            if witness == "preflight:not-found":
                if path != contract.result_path:
                    errors.append("preflight:not-found is allowed only for the report path")
                continue
            if not _HEX40.fullmatch(witness):
                errors.append(f"evidence reference witness is invalid: {text}")
                continue
            try:
                if self._git("cat-file", "-t", witness) != "blob":
                    errors.append(f"evidence witness is not a Git blob: {text}")
            except WorkerRuntimeError:
                errors.append(f"evidence Git blob is unavailable: {text}")
        if payload.get("controlled_outcome") == "IMPLEMENT":
            missing_evidence = sorted(set(advisory.source_references) - evidence_paths)
            if missing_evidence:
                errors.append(
                    "implemented report omits source evidence: " + ", ".join(missing_evidence)
                )
        if errors:
            raise WorkerRuntimeError("Worker report correlation failed: " + "; ".join(errors) + ".")

    @staticmethod
    def _require_history_row(
        connection: sqlite3.Connection,
        advisory: ExecutionReadyAdvisory,
    ) -> sqlite3.Row:
        rows = connection.execute(
            """
            SELECT * FROM execution_history
            WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
            ORDER BY id
            """,
            (advisory.run_id,),
        ).fetchall()
        successful = [row for row in rows if str(row["status"] or "") == "succeeded"]
        if len(successful) != 1:
            raise WorkerRuntimeError(
                "Result ingestion requires exactly one successful authoritative Worker send row."
            )
        return successful[0]

    @classmethod
    def _validate_history_row(
        cls,
        row: sqlite3.Row,
        advisory: ExecutionReadyAdvisory,
    ) -> None:
        errors: list[str] = []
        for field_name, expected in cls._expected_identity(advisory).items():
            observed = row[field_name]
            if field_name in {"task_revision", "procedure_version"}:
                matches = observed is not None and int(observed) == int(expected)
            else:
                matches = str(observed or "") == str(expected)
            if not matches:
                errors.append(f"runtime {field_name} does not match the assignment")
        if str(row["dispatch_state"] or "") != "DISPATCH_SUBMITTED":
            errors.append("runtime dispatch state is not DISPATCH_SUBMITTED")
        if not str(row["user_turn_id"] or "").strip():
            errors.append("runtime row has no correlated user turn ID")
        if errors:
            raise WorkerRuntimeError("Runtime correlation failed: " + "; ".join(errors) + ".")

    @staticmethod
    def _receipt_from_row(row: sqlite3.Row, *, duplicate: bool) -> WorkerResultIngestionReceipt:
        return WorkerResultIngestionReceipt(
            status="succeeded",
            run_id=str(row["run_id"]),
            worker_id=str(row["worker_id"]),
            task_id=str(row["task_id"]),
            task_revision=int(row["task_revision"]),
            report_state=str(row["result_state"]),
            report_path=str(row["report_path"]),
            report_attempt=int(row["report_attempt"]),
            report_checksum=str(row["report_checksum"]),
            report_commit_sha=str(row["report_commit_sha"]),
            report_blob_sha=str(row["report_blob_sha"]),
            controlled_outcome=str(row["controlled_outcome"]),
            verification_mode=str(row["verification_mode"]),
            verification_state=str(row["receiver_verification_state"]),
            completion_state=str(row["receiver_completion_state"]),
            hq_review_required=(
                str(row["verification_mode"]) == "IMMEDIATE_HQ"
                and str(row["worker_verification_state"] or "") not in {"verified", "rejected"}
            ),
            duplicate_suppressed=duplicate,
        )

    def _record_rejection(
        self,
        history_id: int,
        *,
        report_path: str,
        attempt: int,
        checksum: str,
        errors: Iterable[str],
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE execution_history SET
                    result_state = ?, report_path = ?, report_attempt = ?,
                    report_checksum = ?, report_validation_errors_json = ?
                WHERE id = ?
                """,
                (
                    _REPORT_STATE_REJECTED,
                    report_path,
                    attempt,
                    checksum,
                    json.dumps(
                        list(errors),
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                    ),
                    history_id,
                ),
            )

    def ingest(self, advisory: ExecutionReadyAdvisory) -> WorkerResultIngestionReceipt:
        """Ingest one exact canonical report into its existing successful dispatch row."""

        contract = advisory.result_contract
        if contract is None:
            raise WorkerRuntimeError("Canonical assignment has no Worker result contract.")
        report_file = self._safe_path(contract.result_path)
        if not report_file.is_file():
            raise WorkerRuntimeError(f"Worker result artifact is missing: {contract.result_path}")
        try:
            payload = json.loads(report_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkerRuntimeError("Worker report is not readable valid UTF-8 JSON.") from exc
        if not isinstance(payload, dict):
            raise WorkerRuntimeError("Worker report must be a JSON object.")
        checksum = artifact_checksum(payload)
        attempt_value = payload.get("attempt")
        attempt = (
            attempt_value
            if isinstance(attempt_value, int) and not isinstance(attempt_value, bool)
            else 0
        )
        with self._connect() as connection:
            row = self._require_history_row(connection, advisory)
            self._validate_history_row(row, advisory)
            if str(row["result_state"] or "") == _REPORT_STATE_VALIDATED:
                if (
                    str(row["report_path"] or "") == contract.result_path
                    and int(row["report_attempt"] or 0) == attempt
                    and str(row["report_checksum"] or "") == checksum
                ):
                    return self._receipt_from_row(row, duplicate=True)
                raise WorkerRuntimeError("A conflicting validated report already exists for this run.")
            discovered_at = time.time()
            connection.execute(
                """
                UPDATE execution_history SET
                    result_state = ?, report_path = ?, report_attempt = ?,
                    report_checksum = ?, report_discovered_at = ?,
                    report_validation_errors_json = '[]'
                WHERE id = ?
                """,
                (
                    _REPORT_STATE_DISCOVERED,
                    contract.result_path,
                    attempt,
                    checksum,
                    discovered_at,
                    int(row["id"]),
                ),
            )
            history_id = int(row["id"])
        try:
            validate_artifact("worker_report", payload)
            profile = self.runtime.worker(advisory.target_worker_id, require_enabled=True)
            self._validate_report_correlation(advisory, profile, payload)
            git_evidence = self._git_artifact_evidence(
                contract.result_path,
                payload,
                advisory.requested_write_scopes,
            )
        except (WorkerResultContractError, WorkerRuntimeError) as exc:
            details = list(getattr(exc, "errors", ())) or [str(exc)]
            self._record_rejection(
                history_id,
                report_path=contract.result_path,
                attempt=attempt,
                checksum=checksum,
                errors=details,
            )
            raise WorkerRuntimeError("Worker report was rejected: " + "; ".join(details)) from exc
        validated_at = time.time()
        with self._connect() as connection:
            row = self._require_history_row(connection, advisory)
            self._validate_history_row(row, advisory)
            if str(row["result_state"] or "") not in {
                _REPORT_STATE_DISCOVERED,
                _REPORT_STATE_REJECTED,
                "",
            }:
                raise WorkerRuntimeError("Worker result state changed during ingestion.")
            connection.execute(
                """
                UPDATE execution_history SET
                    result_state = ?, report_path = ?, report_attempt = ?,
                    report_checksum = ?, report_commit_sha = ?, report_blob_sha = ?,
                    report_validated_at = ?, report_validation_errors_json = '[]',
                    profile_version = ?, owning_department = ?, controlled_outcome = ?,
                    receiver_reason = ?, receiver_evidence_json = ?,
                    receiver_verification_state = ?, receiver_completion_state = ?,
                    actual_read_scopes_json = ?, actual_write_scopes_json = ?,
                    actual_tools_json = ?, external_actions_verified = ?,
                    approval_required_discovered = ?, worker_failure_reason = ?
                WHERE id = ?
                """,
                (
                    _REPORT_STATE_VALIDATED,
                    contract.result_path,
                    int(payload["attempt"]),
                    git_evidence.checksum,
                    git_evidence.commit_sha,
                    git_evidence.blob_sha,
                    validated_at,
                    int(payload["profile_version"]),
                    str(payload["owning_department"]),
                    str(payload["controlled_outcome"]),
                    "Deterministic immutable Worker report ingestion passed.",
                    json.dumps(
                        payload["evidence_references"],
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                    ),
                    str(payload["verification_state"]),
                    str(payload["completion_state"]),
                    json.dumps(
                        payload["actual_read_scopes"],
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                    ),
                    json.dumps(
                        payload["actual_write_scopes"],
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                    ),
                    json.dumps(
                        payload["actual_tools"],
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                    ),
                    int(bool(payload["external_actions_verified"])),
                    int(bool(payload["approval_required_discovered"])),
                    payload["failure_reason"],
                    int(row["id"]),
                ),
            )
            updated = connection.execute(
                "SELECT * FROM execution_history WHERE id = ?", (int(row["id"]),)
            ).fetchone()
        if updated is None:
            raise WorkerRuntimeError("Worker result row disappeared after ingestion.")
        return self._receipt_from_row(updated, duplicate=False)

    def records(self, limit: int = 100) -> list[dict[str, object]]:
        if limit < 1:
            raise WorkerRuntimeError("Result ingestion record limit must be positive.")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, run_id, worker_id, task_id, task_revision, result_state,
                       report_path, report_attempt, report_checksum, report_commit_sha,
                       report_blob_sha, report_discovered_at, report_validated_at,
                       report_validation_errors_json, controlled_outcome,
                       verification_mode, receiver_verification_state,
                       receiver_completion_state
                FROM execution_history
                WHERE result_state IS NOT NULL
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
                "discovered": sum(
                    item.get("result_state") == _REPORT_STATE_DISCOVERED for item in records
                ),
                "validated": sum(
                    item.get("result_state") == _REPORT_STATE_VALIDATED for item in records
                ),
                "rejected": sum(
                    item.get("result_state") == _REPORT_STATE_REJECTED for item in records
                ),
            },
            "records": records,
        }


__all__ = [
    "GitArtifactEvidence",
    "WorkerResultIngester",
    "WorkerResultIngestionReceipt",
]
