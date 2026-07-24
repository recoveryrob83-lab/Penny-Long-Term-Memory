"""Persisted shared Command Center pause state and conservative trip classification."""
from __future__ import annotations

import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, cast

PauseKind = Literal["none", "manual", "safety"]
DEFAULT_RECOVERY_CONDITION = (
    "Inspect the affected ChatGPT conversation and browser state, reconcile whether the send "
    "occurred, then resume automation explicitly."
)


@dataclass(frozen=True)
class CommandCenterPauseState:
    """One authoritative shared pause record stored in the Command Center database."""

    paused: bool
    pause_kind: PauseKind
    reason: str
    affected_run_id: str | None
    trigger: str | None
    recovery_condition: str | None
    tripped_at: float | None
    updated_at: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class CommandCenterSafetyPauseStore:
    """Store the one shared pause without creating a second execution ledger."""

    _CONTROL_KEY = "shared_pause"

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        now = time.time()
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS command_center_control (
                    control_key TEXT PRIMARY KEY,
                    paused INTEGER NOT NULL,
                    pause_kind TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    affected_run_id TEXT,
                    trigger TEXT,
                    recovery_condition TEXT,
                    tripped_at REAL,
                    updated_at REAL NOT NULL
                );
                """
            )
            connection.execute(
                """
                INSERT OR IGNORE INTO command_center_control(
                    control_key, paused, pause_kind, reason, affected_run_id,
                    trigger, recovery_condition, tripped_at, updated_at
                ) VALUES (?, 0, 'none', '', NULL, NULL, NULL, NULL, ?)
                """,
                (self._CONTROL_KEY, now),
            )

    @staticmethod
    def _clean_optional(value: str | None) -> str | None:
        clean = str(value or "").strip()
        return clean or None

    @staticmethod
    def _from_row(row: sqlite3.Row) -> CommandCenterPauseState:
        pause_kind = str(row["pause_kind"] or "none")
        if pause_kind not in {"none", "manual", "safety"}:
            pause_kind = "safety"
        return CommandCenterPauseState(
            paused=bool(row["paused"]),
            pause_kind=cast(PauseKind, pause_kind),
            reason=str(row["reason"] or ""),
            affected_run_id=(
                str(row["affected_run_id"])
                if row["affected_run_id"] is not None
                else None
            ),
            trigger=str(row["trigger"]) if row["trigger"] is not None else None,
            recovery_condition=(
                str(row["recovery_condition"])
                if row["recovery_condition"] is not None
                else None
            ),
            tripped_at=(
                float(row["tripped_at"]) if row["tripped_at"] is not None else None
            ),
            updated_at=float(row["updated_at"]),
        )

    def _state_from_connection(
        self,
        connection: sqlite3.Connection,
    ) -> CommandCenterPauseState:
        row = connection.execute(
            "SELECT * FROM command_center_control WHERE control_key = ?",
            (self._CONTROL_KEY,),
        ).fetchone()
        if row is None:
            raise RuntimeError("Shared Command Center pause record is missing.")
        return self._from_row(row)

    def state(self) -> CommandCenterPauseState:
        with self._connect() as connection:
            return self._state_from_connection(connection)

    def pause_manually(self) -> CommandCenterPauseState:
        now = time.time()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            current = self._state_from_connection(connection)
            if current.paused and current.pause_kind == "safety":
                return current
            connection.execute(
                """
                UPDATE command_center_control SET
                    paused = 1,
                    pause_kind = 'manual',
                    reason = 'Automation paused manually.',
                    affected_run_id = NULL,
                    trigger = 'manual',
                    recovery_condition = 'Resume automation explicitly when ready.',
                    tripped_at = COALESCE(tripped_at, ?),
                    updated_at = ?
                WHERE control_key = ?
                """,
                (now, now, self._CONTROL_KEY),
            )
            return self._state_from_connection(connection)

    def trip(
        self,
        *,
        reason: str,
        affected_run_id: str | None,
        trigger: str,
        recovery_condition: str = DEFAULT_RECOVERY_CONDITION,
    ) -> CommandCenterPauseState:
        clean_reason = str(reason or "").strip()
        clean_trigger = str(trigger or "").strip()
        clean_recovery = str(recovery_condition or "").strip()
        if not clean_reason:
            raise ValueError("Safety pause reason cannot be empty.")
        if not clean_trigger:
            raise ValueError("Safety pause trigger cannot be empty.")
        if not clean_recovery:
            raise ValueError("Safety pause recovery condition cannot be empty.")

        now = time.time()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            current = self._state_from_connection(connection)
            if current.paused and current.pause_kind == "safety":
                return current
            connection.execute(
                """
                UPDATE command_center_control SET
                    paused = 1,
                    pause_kind = 'safety',
                    reason = ?,
                    affected_run_id = ?,
                    trigger = ?,
                    recovery_condition = ?,
                    tripped_at = ?,
                    updated_at = ?
                WHERE control_key = ?
                """,
                (
                    clean_reason,
                    self._clean_optional(affected_run_id),
                    clean_trigger,
                    clean_recovery,
                    now,
                    now,
                    self._CONTROL_KEY,
                ),
            )
            return self._state_from_connection(connection)

    def resume(self) -> CommandCenterPauseState:
        now = time.time()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                UPDATE command_center_control SET
                    paused = 0,
                    pause_kind = 'none',
                    reason = '',
                    affected_run_id = NULL,
                    trigger = NULL,
                    recovery_condition = NULL,
                    tripped_at = NULL,
                    updated_at = ?
                WHERE control_key = ?
                """,
                (now, self._CONTROL_KEY),
            )
            return self._state_from_connection(connection)


def safety_pause_reason_for_transport(
    *,
    exit_code: int | None,
    stderr: str,
    reason: str,
    claimed_success_without_valid_receipt: bool = False,
) -> str | None:
    """Return a global-trip reason only for genuine send or browser-state uncertainty."""

    diagnostic = f"{stderr}\n{reason}".casefold()
    if exit_code == 3 or "stopped_after_send:" in diagnostic:
        return (
            "Browser transport stopped after a send attempt with uncertain submission state."
        )
    if claimed_success_without_valid_receipt:
        return (
            "Browser transport claimed success but its dispatch receipt could not be validated."
        )
    if any(
        phrase in diagnostic
        for phrase in (
            "submission state may be uncertain",
            "submission may have occurred",
            "timed out before submission could be proven",
            "do not retry blindly",
        )
    ):
        return "Browser transport ended without proving whether the send occurred."
    if any(
        phrase in diagnostic
        for phrase in (
            "could not verify return to hq",
            "did not verify return to the source chat",
            "could not verify return to the source",
        )
    ):
        return (
            "A send was confirmed, but the browser did not return to a verified source state."
        )
    return None


__all__ = [
    "CommandCenterPauseState",
    "CommandCenterSafetyPauseStore",
    "DEFAULT_RECOVERY_CONDITION",
    "safety_pause_reason_for_transport",
]
