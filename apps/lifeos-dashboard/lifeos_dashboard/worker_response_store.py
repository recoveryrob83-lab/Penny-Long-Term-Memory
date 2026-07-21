"""Same-row persistence helpers for captured Worker response reconciliation."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from .worker_receiver_models import ControlledOutcome
from .worker_runtime import WorkerRuntimeError


@dataclass(frozen=True)
class ExistingWorkerOutcome:
    controlled_outcome: ControlledOutcome | None
    reported_outcome: ControlledOutcome | None
    receiver_reason: str | None
    verification_mode: str | None


class WorkerResponseStore:
    """Read and update only the authoritative successful Worker send row."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _successful_rows(
        connection: sqlite3.Connection, run_id: str
    ) -> list[sqlite3.Row]:
        return connection.execute(
            """
            SELECT id, controlled_outcome, worker_reported_outcome, receiver_reason,
                   verification_mode
            FROM execution_history
            WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
              AND status = 'succeeded'
            """,
            (run_id,),
        ).fetchall()

    def existing_outcome(self, run_id: str) -> ExistingWorkerOutcome | None:
        with self._connect() as connection:
            rows = self._successful_rows(connection, run_id)
        if len(rows) > 1:
            raise WorkerRuntimeError(
                "Response reconciliation found duplicate successful Worker send rows."
            )
        if not rows:
            return None
        row = rows[0]
        controlled = row["controlled_outcome"]
        reported = row["worker_reported_outcome"]
        return ExistingWorkerOutcome(
            controlled_outcome=(
                cast(ControlledOutcome, str(controlled)) if controlled else None
            ),
            reported_outcome=(
                cast(ControlledOutcome, str(reported)) if reported else None
            ),
            receiver_reason=(
                str(row["receiver_reason"]) if row["receiver_reason"] else None
            ),
            verification_mode=(
                str(row["verification_mode"]) if row["verification_mode"] else None
            ),
        )

    def record_machine_reported_outcome(
        self, run_id: str, outcome: ControlledOutcome
    ) -> ControlledOutcome | None:
        with self._connect() as connection:
            rows = self._successful_rows(connection, run_id)
            if len(rows) != 1:
                raise WorkerRuntimeError(
                    "Machine report outcome requires exactly one successful Worker send row."
                )
            existing = rows[0]["worker_reported_outcome"]
            if existing is not None and str(existing) != outcome:
                return cast(ControlledOutcome, str(existing))
            connection.execute(
                """
                UPDATE execution_history SET worker_reported_outcome = ?
                WHERE id = ?
                """,
                (outcome, int(rows[0]["id"])),
            )
        return cast(ControlledOutcome, str(existing)) if existing is not None else None

    def record_unresolved_hold(
        self, run_id: str, reason: str
    ) -> tuple[str, ControlledOutcome, ControlledOutcome | None, str]:
        with self._connect() as connection:
            rows = self._successful_rows(connection, run_id)
            if len(rows) != 1:
                raise WorkerRuntimeError(
                    "Response reconciliation requires exactly one successful Worker send row."
                )
            row = rows[0]
            existing = row["controlled_outcome"]
            if existing is None:
                connection.execute(
                    """
                    UPDATE execution_history SET
                        controlled_outcome = 'REPORT_AND_HOLD', receiver_reason = ?,
                        receiver_verification_state = 'unavailable',
                        receiver_completion_state = 'not_attempted'
                    WHERE id = ? AND controlled_outcome IS NULL
                    """,
                    (reason, int(row["id"])),
                )
                controlled = cast(ControlledOutcome, "REPORT_AND_HOLD")
                state = "held"
            else:
                controlled = cast(ControlledOutcome, str(existing))
                reason = str(row["receiver_reason"] or reason)
                state = "already_reconciled"
            reported = row["worker_reported_outcome"]
        return (
            state,
            controlled,
            cast(ControlledOutcome, str(reported)) if reported else None,
            reason,
        )


__all__ = ["ExistingWorkerOutcome", "WorkerResponseStore"]
