"""Derived verification queues and wake decisions for LifeOS Worker runs."""
from __future__ import annotations

import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, Mapping, cast

from .worker_receiver_store import WorkerReceiverStore
from .worker_runtime import WorkerRuntimeError

VerificationQueueState = Literal["pending", "verified", "rejected"]
WakeDisposition = Literal["suppressed", "owning_department_hq", "chief_of_staff_hq"]
ReviewRoute = Literal["none", "routine_batch", "immediate_hq", "automatic"]

_ALLOWED_OUTCOMES = {"IMPLEMENT", "REPORT_AND_HOLD", "ELEVATE_FOR_APPROVAL"}
_ALLOWED_MODES = {"AUTOMATIC", "ROUTINE_BATCH", "IMMEDIATE_HQ"}
_TERMINAL_WAKE_SUPPRESSION_STATES = {"SOURCE_VERIFIED", "CLOSED"}


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise WorkerRuntimeError(f"{field_name} cannot be empty.")
    return text


def verification_state(values: Mapping[str, object]) -> VerificationQueueState:
    """Derive the canonical queue state from persisted receiver evidence."""

    outcome = _required_text(values.get("controlled_outcome"), "controlled_outcome")
    if outcome not in _ALLOWED_OUTCOMES:
        raise WorkerRuntimeError("Worker controlled outcome is invalid.")
    observed = str(values.get("receiver_verification_state") or "").strip().casefold()
    if outcome != "IMPLEMENT":
        return "rejected"
    if observed == "verified":
        return "verified"
    if observed == "rejected":
        return "rejected"
    return "pending"


@dataclass(frozen=True)
class WorkerVerificationRecord:
    """One filtered view over the authoritative execution-history row."""

    history_id: int
    run_id: str
    worker_id: str
    task_id: str
    task_revision: int
    owning_department: str
    controlled_outcome: str
    verification_mode: str
    verification_state: VerificationQueueState
    review_route: ReviewRoute
    queue_eligible: bool
    wake_disposition: WakeDisposition
    wake_target: str | None
    wake_reason: str
    receiver_reason: str
    finished_at: float
    verification_updated_at: float | None = None
    verification_actor: str | None = None
    verification_reason: str | None = None

    @property
    def wake_required(self) -> bool:
        return self.wake_disposition != "suppressed"

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["wake_required"] = self.wake_required
        return values


def _review_route(outcome: str, mode: str, state: VerificationQueueState) -> ReviewRoute:
    if outcome != "IMPLEMENT" or state == "rejected":
        return "none"
    if mode == "ROUTINE_BATCH":
        return "routine_batch"
    if mode == "IMMEDIATE_HQ":
        return "immediate_hq"
    return "automatic"


def _wake_decision(
    *,
    outcome: str,
    mode: str,
    state: VerificationQueueState,
    owning_department: str,
    authoritative_lifecycle_state: str | None = None,
) -> tuple[WakeDisposition, str | None, str]:
    lifecycle = str(authoritative_lifecycle_state or "").strip().upper()
    if lifecycle in _TERMINAL_WAKE_SUPPRESSION_STATES:
        return (
            "suppressed",
            None,
            f"Canonical lifecycle state {lifecycle} suppresses further wakes.",
        )
    if outcome == "ELEVATE_FOR_APPROVAL":
        return (
            "chief_of_staff_hq",
            "Chief of Staff HQ",
            "Rob must decide or authorize the elevated scope.",
        )
    if outcome == "REPORT_AND_HOLD":
        return (
            "owning_department_hq",
            owning_department,
            "The owning Department HQ must resolve the Worker hold.",
        )
    if state == "rejected":
        return (
            "owning_department_hq",
            owning_department,
            "Department review rejected the implementation evidence.",
        )
    if mode == "IMMEDIATE_HQ":
        return (
            "owning_department_hq",
            owning_department,
            "IMMEDIATE_HQ implementation requires prompt Department HQ review.",
        )
    if mode == "AUTOMATIC" and state != "verified":
        return (
            "owning_department_hq",
            owning_department,
            "AUTOMATIC implementation lacks a verified machine postcondition.",
        )
    if mode == "ROUTINE_BATCH" and state == "pending":
        return (
            "suppressed",
            None,
            "Routine implementation is queued for batched Department HQ review.",
        )
    return (
        "suppressed",
        None,
        "Verification is complete or the canonical mode suppresses an immediate wake.",
    )


def record_from_row(
    values: Mapping[str, object],
    *,
    authoritative_lifecycle_state: str | None = None,
) -> WorkerVerificationRecord:
    """Build one queue and wake view from a persisted Worker history row."""

    outcome = _required_text(values.get("controlled_outcome"), "controlled_outcome")
    mode = _required_text(values.get("verification_mode"), "verification_mode")
    if outcome not in _ALLOWED_OUTCOMES:
        raise WorkerRuntimeError("Worker controlled outcome is invalid.")
    if mode not in _ALLOWED_MODES:
        raise WorkerRuntimeError("Worker verification mode is invalid.")
    owning_department = _required_text(values.get("owning_department"), "owning_department")
    state = verification_state(values)
    route = _review_route(outcome, mode, state)
    disposition, wake_target, wake_reason = _wake_decision(
        outcome=outcome,
        mode=mode,
        state=state,
        owning_department=owning_department,
        authoritative_lifecycle_state=authoritative_lifecycle_state,
    )
    return WorkerVerificationRecord(
        history_id=int(values["id"]),
        run_id=_required_text(values.get("run_id"), "run_id"),
        worker_id=_required_text(values.get("worker_id"), "worker_id"),
        task_id=_required_text(values.get("task_id"), "task_id"),
        task_revision=int(values.get("task_revision") or 0),
        owning_department=owning_department,
        controlled_outcome=outcome,
        verification_mode=mode,
        verification_state=state,
        review_route=route,
        queue_eligible=route == "routine_batch" and state == "pending",
        wake_disposition=disposition,
        wake_target=wake_target,
        wake_reason=wake_reason,
        receiver_reason=str(values.get("receiver_reason") or ""),
        finished_at=float(values.get("finished_at") or 0.0),
        verification_updated_at=(
            float(values["receiver_verification_updated_at"])
            if values.get("receiver_verification_updated_at") is not None
            else None
        ),
        verification_actor=(
            str(values["receiver_verification_actor"])
            if values.get("receiver_verification_actor") is not None
            else None
        ),
        verification_reason=(
            str(values["receiver_verification_reason"])
            if values.get("receiver_verification_reason") is not None
            else None
        ),
    )


class WorkerVerificationStore:
    """Expose and review Worker verification without a second queue ledger."""

    _COLUMNS = {
        "receiver_verification_updated_at": "REAL",
        "receiver_verification_actor": "TEXT",
        "receiver_verification_reason": "TEXT",
    }

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        WorkerReceiverStore(database_path)
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

    @staticmethod
    def _select_sql() -> str:
        return """
            SELECT id, run_id, worker_id, task_id, task_revision,
                   owning_department, controlled_outcome, verification_mode,
                   receiver_verification_state, receiver_reason, finished_at,
                   receiver_verification_updated_at, receiver_verification_actor,
                   receiver_verification_reason
            FROM execution_history
            WHERE worker_id IS NOT NULL AND controlled_outcome IS NOT NULL
        """

    def records(self, limit: int = 100) -> list[WorkerVerificationRecord]:
        if limit < 1:
            raise WorkerRuntimeError("Verification record limit must be positive.")
        with self._connect() as connection:
            rows = connection.execute(
                self._select_sql() + " ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [record_from_row(dict(row)) for row in rows]

    def record(self, run_id: str) -> WorkerVerificationRecord | None:
        clean_run_id = _required_text(run_id, "run_id")
        with self._connect() as connection:
            rows = connection.execute(
                self._select_sql() + " AND run_id = ?", (clean_run_id,)
            ).fetchall()
        if not rows:
            return None
        if len(rows) > 1:
            raise WorkerRuntimeError("Verification found ambiguous duplicate run history.")
        return record_from_row(dict(rows[0]))

    def review(
        self,
        run_id: str,
        state: VerificationQueueState,
        *,
        actor: str,
        reason: str,
    ) -> WorkerVerificationRecord:
        """Persist one Department HQ verification decision in the existing run row."""

        if state not in {"verified", "rejected"}:
            raise WorkerRuntimeError("Review state must be verified or rejected.")
        clean_actor = _required_text(actor, "verification actor")
        clean_reason = _required_text(reason, "verification reason")
        clean_run_id = _required_text(run_id, "run_id")
        with self._connect() as connection:
            rows = connection.execute(
                self._select_sql() + " AND run_id = ?", (clean_run_id,)
            ).fetchall()
            if not rows:
                raise WorkerRuntimeError("Worker verification run was not found.")
            if len(rows) > 1:
                raise WorkerRuntimeError("Verification found ambiguous duplicate run history.")
            current = record_from_row(dict(rows[0]))
            if current.controlled_outcome != "IMPLEMENT":
                raise WorkerRuntimeError("Only implemented work may receive a verification review.")
            if current.verification_mode == "AUTOMATIC":
                raise WorkerRuntimeError(
                    "AUTOMATIC verification must come from the machine postcondition evidence."
                )
            if current.verification_state == state:
                return current
            if current.verification_state != "pending":
                raise WorkerRuntimeError("This verification decision is already terminal.")
            updated_at = time.time()
            connection.execute(
                """
                UPDATE execution_history SET
                    receiver_verification_state = ?,
                    receiver_verification_updated_at = ?,
                    receiver_verification_actor = ?,
                    receiver_verification_reason = ?
                WHERE id = ?
                """,
                (state, updated_at, clean_actor, clean_reason, current.history_id),
            )
        updated = self.record(clean_run_id)
        if updated is None:
            raise WorkerRuntimeError("Verification row disappeared after review.")
        return updated


class WorkerVerificationService:
    """Provide filtered verification views and wake-suppression decisions."""

    def __init__(self, database_path: Path) -> None:
        self.store = WorkerVerificationStore(database_path)

    def records(self, limit: int = 100) -> list[WorkerVerificationRecord]:
        return self.store.records(limit)

    def status(self, limit: int = 100) -> dict[str, object]:
        records = self.records(limit)
        summary = {
            "total": len(records),
            "pending": sum(item.verification_state == "pending" for item in records),
            "verified": sum(item.verification_state == "verified" for item in records),
            "rejected": sum(item.verification_state == "rejected" for item in records),
            "routine_queue": sum(item.queue_eligible for item in records),
            "wake_required": sum(item.wake_required for item in records),
            "wake_suppressed": sum(not item.wake_required for item in records),
        }
        return {
            "summary": summary,
            "records": [item.to_dict() for item in records],
        }

    def review(
        self,
        run_id: str,
        state: str,
        *,
        actor: str,
        reason: str,
    ) -> WorkerVerificationRecord:
        if state not in {"verified", "rejected"}:
            raise WorkerRuntimeError("Review state must be verified or rejected.")
        return self.store.review(
            run_id,
            cast(VerificationQueueState, state),
            actor=actor,
            reason=reason,
        )


__all__ = [
    "VerificationQueueState",
    "WakeDisposition",
    "WorkerVerificationRecord",
    "WorkerVerificationService",
    "WorkerVerificationStore",
    "record_from_row",
    "verification_state",
]
