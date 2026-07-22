"""Deterministic Package E report rejection and correction-only repair coordination.

The immutable Worker outbox remains Git evidence and ``execution_history`` remains the one runtime
ledger. This module derives a narrow next-attempt contract only after a report has been rejected. It
never authorizes work re-execution, scope expansion, advisory lifecycle change, or a second ledger.
"""
from __future__ import annotations

import json
import re
import sqlite3
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Iterable

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_result_contract import (
    artifact_checksum,
    artifact_path,
    build_result_submission_contract,
    validate_artifact,
)
from .worker_result_ingester import GitArtifactEvidence, WorkerResultIngester, WorkerResultIngestionReceipt
from .worker_runtime import WorkerRuntimeError

_REPAIR_PENDING = "REPORT_REPAIR_PENDING"
_REPAIR_ACCEPTED = "REPORT_REPAIR_ACCEPTED"
_REPAIR_EXHAUSTED = "REPORT_REPAIR_EXHAUSTED"
_FIELD_ERROR = re.compile(r"^\$\.(?P<field>[^:]+):\s*(?P<message>.*)$")


@dataclass(frozen=True)
class WorkerReportRepairWake:
    """One correction-only wake derived from a deterministic rejection artifact."""

    wrapper_id: str
    run_id: str
    worker_id: str
    task_id: str
    task_revision: int
    rejected_report_attempt: int
    rejection_path: str
    next_report_attempt: int
    corrected_report_path: str
    instruction: str
    work_reexecution_authorized: bool = False
    scope_expansion_authorized: bool = False

    @property
    def idempotency_key(self) -> str:
        return (
            f"report-repair:{self.worker_id}:{self.run_id}:"
            f"{self.next_report_attempt}"
        )

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["idempotency_key"] = self.idempotency_key
        return values


@dataclass(frozen=True)
class WorkerReportRejectionReceipt:
    """Evidence that one malformed report was rejected and a repair was queued."""

    run_id: str
    worker_id: str
    rejected_report_attempt: int
    rejected_report_path: str
    rejected_report_checksum: str
    rejection_path: str
    rejection_checksum: str
    rejection_commit_sha: str
    rejection_blob_sha: str
    next_report_attempt: int
    repair_state: str
    repair_wake: WorkerReportRepairWake | None

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["repair_wake"] = self.repair_wake.to_dict() if self.repair_wake else None
        return values


def _type_name(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _safe_summary(value: object) -> str:
    """Describe an observed value without copying arbitrary report content."""

    if value is None or isinstance(value, (bool, int, float)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, str):
        return f"<string length {len(value)}>"
    if isinstance(value, list):
        return f"<array length {len(value)}>"
    if isinstance(value, dict):
        return f"<object fields {len(value)}>"
    return f"<{type(value).__name__}>"


def _field_value(payload: dict[str, object], field: str) -> object:
    current: object = payload
    for part in field.replace("]", "").replace("[", ".").split("."):
        if not part:
            continue
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None
    return current


def _error_code(message: str) -> str:
    lowered = message.casefold()
    if "required field is missing" in lowered:
        return "MISSING_FIELD"
    if "unknown field" in lowered:
        return "UNKNOWN_FIELD"
    if "expected" in lowered and "observed" in lowered:
        return "WRONG_TYPE"
    if "correlation" in lowered or "does not match" in lowered:
        return "CORRELATION_MISMATCH"
    if "git" in lowered or "blob" in lowered or "commit" in lowered or "evidence" in lowered:
        return "EVIDENCE_INVALID"
    return "REPORT_VALIDATION_ERROR"


def _expected_summary(message: str) -> str:
    lowered = message.casefold()
    if "expected " in lowered:
        return message[lowered.index("expected ") + len("expected ") :].split(",", 1)[0]
    if "required field" in lowered:
        return "required field"
    if "unknown field" in lowered:
        return "field declared by the canonical schema"
    return "schema-valid, assignment-correlated immutable Worker report"


def structured_validation_errors(
    errors: Iterable[str], payload: dict[str, object]
) -> list[dict[str, object]]:
    """Convert deterministic validator messages into the canonical rejection schema."""

    structured: list[dict[str, object]] = []
    for raw in errors:
        message = str(raw).strip() or "Worker report validation failed."
        match = _FIELD_ERROR.match(message)
        field = match.group("field") if match else "report"
        field_message = match.group("message") if match else message
        observed = _field_value(payload, field) if field != "report" else payload
        structured.append(
            {
                "code": _error_code(field_message),
                "field": field,
                "message": field_message,
                "expected": _expected_summary(field_message),
                "observed_type": _type_name(observed),
                "observed_summary": _safe_summary(observed),
            }
        )
    return structured or [
        {
            "code": "REPORT_VALIDATION_ERROR",
            "field": "report",
            "message": "Worker report validation failed without a detailed error.",
            "expected": "schema-valid, assignment-correlated immutable Worker report",
            "observed_type": _type_name(payload),
            "observed_summary": _safe_summary(payload),
        }
    ]


def render_repair_instruction(
    advisory: ExecutionReadyAdvisory,
    *,
    rejected_attempt: int,
    rejection_path: str,
    next_attempt: int,
    corrected_report_path: str,
) -> str:
    """Render a reference-only repair wake with no authority to repeat the work."""

    return (
        f"Report repair for canonical run {advisory.run_id}.\n\n"
        f"Read the deterministic rejection artifact at `{rejection_path}` and the rejected "
        f"report attempt {rejected_attempt}. Do not repeat or broaden the underlying work. "
        f"Correct only the report artifact and create exactly one new immutable attempt at "
        f"`{corrected_report_path}`. Preserve the same run, Worker, task revision, procedure, "
        "authorization source, verification mode, substantive findings, and evidence unless the "
        "rejection artifact identifies a report-correlation defect that must be corrected. "
        "Do not overwrite, delete, edit the source advisory, change lifecycle, re-execute work, "
        "expand scope, or perform any unrelated write or external action. "
        f"The only authorized next report attempt is {next_attempt}."
    )


class WorkerResultRepairCoordinator:
    """Wrap the proven ingester with deterministic rejection and next-attempt handling."""

    _COLUMNS = {
        "rejection_path": "TEXT",
        "rejection_checksum": "TEXT",
        "rejection_commit_sha": "TEXT",
        "rejection_blob_sha": "TEXT",
        "next_report_attempt": "INTEGER",
        "repair_state": "TEXT",
        "repair_wake_json": "TEXT",
        "repair_wake_created_at": "REAL",
    }

    def __init__(self, ingester: WorkerResultIngester, *, max_report_attempts: int = 3) -> None:
        if max_report_attempts < 2:
            raise WorkerRuntimeError("Report repair requires an attempt ceiling of at least two.")
        self.ingester = ingester
        self.database_path = ingester.database_path
        self.max_report_attempts = max_report_attempts
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

    def _row(self, run_id: str) -> sqlite3.Row:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM execution_history
                WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
                ORDER BY id
                """,
                (run_id,),
            ).fetchall()
        if len(rows) != 1:
            raise WorkerRuntimeError(
                "Report repair requires exactly one authoritative Worker send row."
            )
        return rows[0]

    @staticmethod
    def _derived_advisory(
        advisory: ExecutionReadyAdvisory, attempt: int
    ) -> ExecutionReadyAdvisory:
        original = advisory.result_contract
        if original is None:
            raise WorkerRuntimeError("Canonical assignment has no Worker result contract.")
        contract = build_result_submission_contract(
            original.owning_department,
            original.worker_id,
            original.run_id,
            attempt=attempt,
        )
        return replace(
            advisory,
            requested_write_scopes=(contract.result_path,),
            result_contract=contract,
        )

    def expected_attempt(self, advisory: ExecutionReadyAdvisory) -> int:
        row = self._row(advisory.run_id)
        state = str(row["result_state"] or "")
        if state == "REPORT_VALIDATED":
            return int(row["report_attempt"] or 1)
        if state == "REPORT_REJECTED":
            next_attempt = int(row["next_report_attempt"] or 0)
            if next_attempt < 2:
                raise WorkerRuntimeError(
                    "Rejected report has no deterministic next-attempt authority."
                )
            return next_attempt
        contract = advisory.result_contract
        if contract is None:
            raise WorkerRuntimeError("Canonical assignment has no Worker result contract.")
        return contract.attempt

    def _write_create_only_artifact(
        self,
        relative_path: str,
        payload: dict[str, object],
        *,
        commit_message: str,
    ) -> GitArtifactEvidence:
        candidate = self.ingester._safe_path(relative_path)  # noqa: SLF001
        if candidate.exists():
            try:
                existing = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise WorkerRuntimeError(
                    f"Existing rejection artifact is unreadable: {relative_path}"
                ) from exc
            if not isinstance(existing, dict) or artifact_checksum(existing) != artifact_checksum(payload):
                raise WorkerRuntimeError(
                    f"Conflicting create-only rejection artifact already exists: {relative_path}"
                )
            validate_artifact("rejection", existing)
        else:
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_text(
                json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            self.ingester._git("add", "--", relative_path)  # noqa: SLF001
            self.ingester._git(  # noqa: SLF001
                "commit",
                "--only",
                "-m",
                commit_message,
                "--",
                relative_path,
            )
        return self.ingester._git_artifact_evidence(  # noqa: SLF001
            relative_path,
            payload,
            (relative_path,),
        )

    def _repair_wake(
        self,
        advisory: ExecutionReadyAdvisory,
        *,
        rejected_attempt: int,
        rejection_path: str,
        next_attempt: int,
    ) -> WorkerReportRepairWake:
        corrected = self._derived_advisory(advisory, next_attempt)
        corrected_path = corrected.result_contract.result_path  # type: ignore[union-attr]
        return WorkerReportRepairWake(
            wrapper_id=f"REPAIR-{advisory.task_id}-R{advisory.advisory_revision}-A{next_attempt}",
            run_id=advisory.run_id,
            worker_id=advisory.target_worker_id,
            task_id=advisory.advisory_id,
            task_revision=advisory.advisory_revision,
            rejected_report_attempt=rejected_attempt,
            rejection_path=rejection_path,
            next_report_attempt=next_attempt,
            corrected_report_path=corrected_path,
            instruction=render_repair_instruction(
                advisory,
                rejected_attempt=rejected_attempt,
                rejection_path=rejection_path,
                next_attempt=next_attempt,
                corrected_report_path=corrected_path,
            ),
        )

    def prepare_repair(
        self, advisory: ExecutionReadyAdvisory
    ) -> WorkerReportRejectionReceipt:
        row = self._row(advisory.run_id)
        if str(row["result_state"] or "") != "REPORT_REJECTED":
            raise WorkerRuntimeError("Report repair may be prepared only after deterministic rejection.")
        rejected_attempt = int(row["report_attempt"] or 0)
        rejected_path = str(row["report_path"] or "")
        rejected_checksum = str(row["report_checksum"] or "")
        if rejected_attempt < 1 or not rejected_path or not rejected_checksum:
            raise WorkerRuntimeError("Rejected report evidence is incomplete.")
        report_file = self.ingester._safe_path(rejected_path)  # noqa: SLF001
        try:
            report_payload = json.loads(report_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkerRuntimeError("Rejected report is no longer readable JSON.") from exc
        if not isinstance(report_payload, dict):
            raise WorkerRuntimeError("Rejected report is no longer a JSON object.")
        try:
            raw_errors = json.loads(str(row["report_validation_errors_json"] or "[]"))
        except json.JSONDecodeError as exc:
            raise WorkerRuntimeError("Stored report validation errors are invalid JSON.") from exc
        if not isinstance(raw_errors, list):
            raise WorkerRuntimeError("Stored report validation errors have the wrong shape.")

        next_attempt = rejected_attempt + 1
        exhausted = rejected_attempt >= self.max_report_attempts
        rejection_path = artifact_path(
            advisory.result_contract.owning_department,  # type: ignore[union-attr]
            advisory.target_worker_id,
            advisory.run_id,
            "rejection",
            rejected_attempt,
        )
        rejection_payload: dict[str, object] = {
            "schema_id": "lifeos_worker_result_rejection",
            "schema_version": 1,
            "artifact_type": "rejection",
            "attempt": rejected_attempt,
            "run_id": advisory.run_id,
            "worker_id": advisory.target_worker_id,
            "rejected_report_path": rejected_path,
            "rejected_report_checksum": rejected_checksum,
            "validation_errors": structured_validation_errors(
                (str(item) for item in raw_errors), report_payload
            ),
            "next_report_attempt": next_attempt,
            "work_reexecution_authorized": False,
            "scope_expansion_authorized": False,
            "escalation_required": exhausted,
        }
        validate_artifact("rejection", rejection_payload)
        evidence = self._write_create_only_artifact(
            rejection_path,
            rejection_payload,
            commit_message=(
                f"Record Worker report rejection for {advisory.run_id} "
                f"attempt {rejected_attempt}"
            ),
        )
        wake = None if exhausted else self._repair_wake(
            advisory,
            rejected_attempt=rejected_attempt,
            rejection_path=rejection_path,
            next_attempt=next_attempt,
        )
        repair_state = _REPAIR_EXHAUSTED if exhausted else _REPAIR_PENDING
        wake_json = (
            json.dumps(wake.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            if wake
            else None
        )
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE execution_history SET
                    rejection_path = ?, rejection_checksum = ?,
                    rejection_commit_sha = ?, rejection_blob_sha = ?,
                    next_report_attempt = ?, repair_state = ?,
                    repair_wake_json = ?, repair_wake_created_at = ?
                WHERE id = ?
                """,
                (
                    rejection_path,
                    evidence.checksum,
                    evidence.commit_sha,
                    evidence.blob_sha,
                    next_attempt,
                    repair_state,
                    wake_json,
                    time.time(),
                    int(row["id"]),
                ),
            )
        return WorkerReportRejectionReceipt(
            run_id=advisory.run_id,
            worker_id=advisory.target_worker_id,
            rejected_report_attempt=rejected_attempt,
            rejected_report_path=rejected_path,
            rejected_report_checksum=rejected_checksum,
            rejection_path=rejection_path,
            rejection_checksum=evidence.checksum,
            rejection_commit_sha=evidence.commit_sha,
            rejection_blob_sha=evidence.blob_sha,
            next_report_attempt=next_attempt,
            repair_state=repair_state,
            repair_wake=wake,
        )

    def ingest_next(self, advisory: ExecutionReadyAdvisory) -> WorkerResultIngestionReceipt:
        """Ingest the canonical or deterministically authorized next report attempt."""

        attempt = self.expected_attempt(advisory)
        derived = self._derived_advisory(advisory, attempt)
        try:
            receipt = self.ingester.ingest(derived)
        except WorkerRuntimeError as exc:
            row = self._row(advisory.run_id)
            if (
                str(row["result_state"] or "") == "REPORT_REJECTED"
                and int(row["report_attempt"] or 0) == attempt
            ):
                rejection = self.prepare_repair(advisory)
                raise WorkerRuntimeError(
                    "Worker report was rejected and a correction-only repair was prepared: "
                    f"{rejection.rejection_path}; next attempt {rejection.next_report_attempt}. "
                    f"Original error: {exc}"
                ) from exc
            raise
        if attempt > 1 and not receipt.duplicate_suppressed:
            with self._connect() as connection:
                connection.execute(
                    """
                    UPDATE execution_history SET repair_state = ?, next_report_attempt = NULL
                    WHERE run_id = ? AND result_state = 'REPORT_VALIDATED'
                    """,
                    (_REPAIR_ACCEPTED, advisory.run_id),
                )
        return receipt

    def repair_wake(self, run_id: str) -> WorkerReportRepairWake | None:
        row = self._row(run_id)
        raw = str(row["repair_wake_json"] or "").strip()
        if not raw:
            return None
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise WorkerRuntimeError("Persisted repair wake is invalid JSON.") from exc
        if not isinstance(payload, dict):
            raise WorkerRuntimeError("Persisted repair wake has the wrong shape.")
        payload.pop("idempotency_key", None)
        return WorkerReportRepairWake(**payload)

    def records(self, limit: int = 100) -> list[dict[str, object]]:
        if limit < 1:
            raise WorkerRuntimeError("Report repair record limit must be positive.")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, run_id, worker_id, task_id, task_revision,
                       result_state, report_attempt, rejection_path,
                       rejection_checksum, rejection_commit_sha, rejection_blob_sha,
                       next_report_attempt, repair_state, repair_wake_json,
                       repair_wake_created_at
                FROM execution_history
                WHERE repair_state IS NOT NULL
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
                "pending": sum(item.get("repair_state") == _REPAIR_PENDING for item in records),
                "accepted": sum(item.get("repair_state") == _REPAIR_ACCEPTED for item in records),
                "exhausted": sum(item.get("repair_state") == _REPAIR_EXHAUSTED for item in records),
            },
            "records": records,
        }


__all__ = [
    "WorkerReportRejectionReceipt",
    "WorkerReportRepairWake",
    "WorkerResultRepairCoordinator",
    "render_repair_instruction",
    "structured_validation_errors",
]
