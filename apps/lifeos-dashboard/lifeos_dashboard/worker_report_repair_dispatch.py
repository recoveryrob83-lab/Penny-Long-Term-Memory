"""Guarded one-shot browser transport for correction-only Worker report wakes.

A report-repair wake may correct only an immutable report artifact. It reuses the
existing canonical run row, records separate repair-dispatch evidence, consumes the
shared send budget, and never authorizes underlying work re-execution.
"""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from .command_center_safety_pause import safety_pause_reason_for_transport
from .command_center_send_budget import BUDGET_RECOVERY_CONDITION
from .worker_command_center import WorkerCommandJob
from .worker_dispatch_runtime import run_worker_browser_dispatch
from .worker_operations import WorkerOperationsService
from .worker_result_repair import WorkerReportRepairWake
from .worker_runtime import ExecutionEnvelope, WorkerRegistryEntry, WorkerRuntimeError

_REPAIR_PENDING = "REPORT_REPAIR_PENDING"
_REPAIR_DISPATCH_SUBMITTED = "REPAIR_DISPATCH_SUBMITTED"


@dataclass(frozen=True)
class WorkerReportRepairDispatchReceipt:
    """Evidence for one submitted correction-only report wake."""

    status: str
    run_id: str
    worker_id: str
    wrapper_id: str
    rejected_report_path: str
    rejection_path: str
    corrected_report_path: str
    user_turn_id: str
    returned_to_source: bool
    dispatch_state: str = _REPAIR_DISPATCH_SUBMITTED

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerReportRepairDispatchService:
    """Dispatch exactly one already-prepared report repair wake."""

    _COLUMNS = {
        "repair_dispatch_claimed_at": "REAL",
        "repair_dispatch_state": "TEXT",
        "repair_dispatch_wrapper_id": "TEXT",
        "repair_dispatch_user_turn_id": "TEXT",
        "repair_dispatch_receipt_json": "TEXT",
        "repair_dispatch_returned_to_source": "INTEGER",
        "repair_dispatched_at": "REAL",
        "repair_dispatch_error": "TEXT",
    }

    def __init__(
        self,
        operations: WorkerOperationsService,
        database_path: Path,
    ) -> None:
        self.operations = operations
        self.database_path = database_path
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
        if len(rows) != 1:
            raise WorkerRuntimeError(
                "Report repair dispatch requires exactly one authoritative Worker send row."
            )
        return rows[0]

    def _advisory(self, run_id: str):
        matches = [
            advisory
            for advisory in self.operations.pipeline.discover()
            if advisory.run_id == run_id and advisory.result_contract is not None
        ]
        if not matches:
            raise WorkerRuntimeError(
                f"No OPEN execution-ready Worker assignment matches {run_id}."
            )
        if len(matches) > 1:
            raise WorkerRuntimeError(f"Worker assignment {run_id} is ambiguous.")
        return matches[0]

    def _prepared_wake(self, run_id: str) -> WorkerReportRepairWake:
        wake = self.operations.result_repair.repair_wake(run_id)
        if wake is None:
            raise WorkerRuntimeError("No correction-only report repair wake is prepared.")
        if wake.work_reexecution_authorized or wake.scope_expansion_authorized:
            raise WorkerRuntimeError("Prepared report repair wake contains prohibited authority.")
        return wake

    @staticmethod
    def _repair_envelope(advisory, wake: WorkerReportRepairWake) -> ExecutionEnvelope:
        return ExecutionEnvelope(
            wrapper_id=wake.wrapper_id,
            run_id=wake.run_id,
            worker_id=wake.worker_id,
            task_id=wake.task_id,
            task_revision=wake.task_revision,
            procedure_id=advisory.procedure_id,
            procedure_version=advisory.procedure_version,
            authorization_source=advisory.authorization_source,
            verification_mode=advisory.verification_mode,
        )

    def _entry(self, wake: WorkerReportRepairWake) -> WorkerRegistryEntry:
        runtime = self.operations.worker_center.runtime
        entry = runtime.worker(wake.worker_id, require_enabled=True)
        route = runtime.store.route_state(wake.worker_id)
        if route is None or route.availability != "available":
            availability = "unknown" if route is None else route.availability
            raise WorkerRuntimeError(
                f"Worker route is {availability}; report repair dispatch must hold."
            )
        if not entry.conversation_url or entry.route_revision < 1:
            raise WorkerRuntimeError(
                "Report repair dispatch requires one registered exact Worker conversation URL."
            )
        return entry

    def _claim(self, row: sqlite3.Row, wake: WorkerReportRepairWake) -> None:
        with self._connect() as connection:
            updated = connection.execute(
                """
                UPDATE execution_history
                SET repair_dispatch_claimed_at = ?, repair_dispatch_wrapper_id = ?,
                    repair_dispatch_error = NULL
                WHERE id = ?
                  AND result_state = 'REPORT_REJECTED'
                  AND repair_state = ?
                  AND COALESCE(repair_dispatch_state, '') = ''
                  AND repair_dispatch_claimed_at IS NULL
                """,
                (
                    time.time(),
                    wake.wrapper_id,
                    int(row["id"]),
                    _REPAIR_PENDING,
                ),
            )
        if updated.rowcount != 1:
            raise WorkerRuntimeError(
                "Report repair wake is already claimed, already submitted, or no longer pending."
            )

    def _clear_claim_before_send(self, row_id: int, error: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE execution_history
                SET repair_dispatch_claimed_at = NULL, repair_dispatch_error = ?
                WHERE id = ? AND COALESCE(repair_dispatch_state, '') = ''
                """,
                (error, row_id),
            )

    def _reserve_budget(self, run_id: str) -> None:
        command_center = self.operations.command_center
        decision = command_center.reserve_send_budget(
            kind="worker_report_repair",
            run_id=run_id,
        )
        if not decision.reserved:
            command_center.trip_safety_pause(
                reason=decision.reason,
                affected_run_id=run_id,
                trigger="send_budget",
                recovery_condition=BUDGET_RECOVERY_CONDITION,
            )
            raise WorkerRuntimeError(
                f"{decision.reason} Reset the budget explicitly while paused before another send."
            )
        try:
            command_center.append_send_budget_evidence(
                run_id=run_id,
                decision=decision,
            )
        except Exception as exc:
            command_center.trip_safety_pause(
                reason=(
                    "A report repair wake reserved a global send attempt, but the reservation "
                    "could not be attached to the authoritative execution row. Nothing was sent."
                ),
                affected_run_id=run_id,
                trigger="send_budget_evidence",
                recovery_condition=BUDGET_RECOVERY_CONDITION,
            )
            raise WorkerRuntimeError(
                "Report repair send-budget evidence could not be persisted before transport."
            ) from exc

    def _record_success(
        self,
        row_id: int,
        wake: WorkerReportRepairWake,
        evidence,
    ) -> WorkerReportRepairDispatchReceipt:
        receipt = WorkerReportRepairDispatchReceipt(
            status="submitted",
            run_id=wake.run_id,
            worker_id=wake.worker_id,
            wrapper_id=wake.wrapper_id,
            rejected_report_path=wake.rejected_report_path,
            rejection_path=wake.rejection_path,
            corrected_report_path=wake.corrected_report_path,
            user_turn_id=evidence.user_turn_id,
            returned_to_source=evidence.returned_to_source,
        )
        with self._connect() as connection:
            updated = connection.execute(
                """
                UPDATE execution_history SET
                    repair_dispatch_state = ?, repair_dispatch_wrapper_id = ?,
                    repair_dispatch_user_turn_id = ?, repair_dispatch_receipt_json = ?,
                    repair_dispatch_returned_to_source = ?, repair_dispatched_at = ?,
                    repair_dispatch_error = NULL
                WHERE id = ?
                  AND repair_dispatch_claimed_at IS NOT NULL
                  AND COALESCE(repair_dispatch_state, '') = ''
                """,
                (
                    receipt.dispatch_state,
                    wake.wrapper_id,
                    evidence.user_turn_id,
                    evidence.dispatch_receipt_json,
                    int(evidence.returned_to_source),
                    time.time(),
                    row_id,
                ),
            )
        if updated.rowcount != 1:
            raise WorkerRuntimeError(
                "Report repair dispatch evidence could not be attached to the existing run row."
            )
        return receipt

    def dispatch(
        self,
        run_id: str,
        *,
        timeout_seconds: int = 600,
    ) -> WorkerReportRepairDispatchReceipt:
        if timeout_seconds < 60 or timeout_seconds > 900:
            raise WorkerRuntimeError("timeout_seconds must be between 60 and 900.")
        command_center = self.operations.command_center
        if command_center.paused:
            raise WorkerRuntimeError("Automation is paused. Resume it before report repair dispatch.")
        run_lock = command_center._run_lock
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError("Another automation job is already running.")
        try:
            row = self._row(run_id)
            if str(row["repair_dispatch_state"] or "") == _REPAIR_DISPATCH_SUBMITTED:
                raise WorkerRuntimeError(
                    "Correction-only report wake was already submitted; do not resend it."
                )
            if str(row["result_state"] or "") != "REPORT_REJECTED":
                raise WorkerRuntimeError(
                    "Correction-only dispatch requires a deterministically rejected report."
                )
            if str(row["repair_state"] or "") != _REPAIR_PENDING:
                raise WorkerRuntimeError("Correction-only report repair is not pending.")

            advisory = self._advisory(run_id)
            wake = self._prepared_wake(run_id)
            entry = self._entry(wake)
            self._claim(row, wake)
            try:
                self._reserve_budget(run_id)
            except WorkerRuntimeError as exc:
                self._clear_claim_before_send(int(row["id"]), str(exc))
                raise

            envelope = self._repair_envelope(advisory, wake)
            job = WorkerCommandJob(
                envelope=envelope,
                instruction=wake.instruction,
                mode="send",
                confirm_send=True,
            )
            result, evidence = run_worker_browser_dispatch(
                job,
                entry,
                command_center.app_root,
                trigger="manual",
                timeout_seconds=timeout_seconds,
            )
            if result.status != "succeeded":
                pause_reason = safety_pause_reason_for_transport(
                    exit_code=result.exit_code,
                    stderr=result.stderr,
                    reason=result.reason,
                )
                if pause_reason is None:
                    self._clear_claim_before_send(int(row["id"]), result.reason)
                else:
                    command_center.trip_safety_pause(
                        reason=pause_reason,
                        affected_run_id=run_id,
                        trigger="worker_report_repair_transport",
                    )
                raise WorkerRuntimeError(result.reason)

            receipt = self._record_success(int(row["id"]), wake, evidence)
            if not evidence.returned_to_source:
                command_center.trip_safety_pause(
                    reason=(
                        "Correction-only Worker wake was submitted, but the courier did not verify "
                        "return to the source chat. Automatic retry is prohibited."
                    ),
                    affected_run_id=run_id,
                    trigger="worker_report_repair_transport",
                )
                raise WorkerRuntimeError(
                    "Correction-only Worker wake submitted without verified return to source."
                )
            return receipt
        finally:
            run_lock.release()

    def status(self, run_id: str) -> dict[str, object]:
        row = self._row(run_id)
        return {
            "run_id": run_id,
            "result_state": row["result_state"],
            "repair_state": row["repair_state"],
            "repair_dispatch_state": row["repair_dispatch_state"],
            "repair_dispatch_wrapper_id": row["repair_dispatch_wrapper_id"],
            "repair_dispatch_user_turn_id": row["repair_dispatch_user_turn_id"],
            "repair_dispatch_returned_to_source": bool(
                row["repair_dispatch_returned_to_source"]
            ),
            "repair_dispatched_at": row["repair_dispatched_at"],
            "repair_dispatch_error": row["repair_dispatch_error"],
        }


__all__ = [
    "WorkerReportRepairDispatchReceipt",
    "WorkerReportRepairDispatchService",
]
