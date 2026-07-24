"""Persistent manually reset send budget for confirmed Worker and HQ wake attempts."""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, cast

SendBudgetKind = Literal["worker_dispatch", "hq_review_wake"]
DEFAULT_SEND_BUDGET_LIMIT = 3
MIN_SEND_BUDGET_LIMIT = 1
MAX_SEND_BUDGET_LIMIT = 20
BUDGET_RECOVERY_CONDITION = (
    "Review the current budget epoch and any affected conversations, reset the send budget "
    "explicitly while automation is paused, then resume automation explicitly."
)


@dataclass(frozen=True)
class SendBudgetState:
    """Current singleton budget state stored beside the shared Command Center pause."""

    limit: int
    used: int
    remaining: int
    exhausted: bool
    epoch: int
    last_reset_at: float | None
    last_reserved_at: float | None
    last_reserved_kind: SendBudgetKind | None
    last_reserved_run_id: str | None
    held_count: int
    last_held_at: float | None
    last_held_kind: SendBudgetKind | None
    last_held_run_id: str | None
    last_hold_reason: str | None
    updated_at: float | None

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["held_operations"] = {
            "count": self.held_count,
            "last": (
                {
                    "at": self.last_held_at,
                    "kind": self.last_held_kind,
                    "run_id": self.last_held_run_id,
                    "reason": self.last_hold_reason,
                }
                if self.last_held_at is not None
                else None
            ),
        }
        return values


@dataclass(frozen=True)
class SendBudgetDecision:
    """Atomic reservation or refusal made before entering browser transport."""

    reserved: bool
    kind: SendBudgetKind
    run_id: str
    epoch: int
    sequence: int | None
    reserved_at: float | None
    reason: str
    state: SendBudgetState

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["state"] = self.state.to_dict()
        return values

    def evidence(self) -> dict[str, object]:
        if not self.reserved or self.sequence is None or self.reserved_at is None:
            raise ValueError("Only a reserved send-budget decision can become execution evidence.")
        return {
            "kind": self.kind,
            "run_id": self.run_id,
            "epoch": self.epoch,
            "sequence": self.sequence,
            "reserved_at": self.reserved_at,
        }


def configured_send_budget_limit(value: str | None) -> int:
    """Parse one explicit bounded limit without silently accepting malformed configuration."""

    clean = str(value or "").strip()
    if not clean:
        return DEFAULT_SEND_BUDGET_LIMIT
    try:
        limit = int(clean)
    except ValueError as exc:
        raise ValueError("LIFEOS_GLOBAL_SEND_BUDGET_LIMIT must be an integer.") from exc
    if limit < MIN_SEND_BUDGET_LIMIT or limit > MAX_SEND_BUDGET_LIMIT:
        raise ValueError(
            "LIFEOS_GLOBAL_SEND_BUDGET_LIMIT must be between "
            f"{MIN_SEND_BUDGET_LIMIT} and {MAX_SEND_BUDGET_LIMIT}."
        )
    return limit


class CommandCenterSendBudgetStore:
    """Reserve confirmed send attempts on the existing singleton control record."""

    _CONTROL_KEY = "shared_pause"
    _CONTROL_COLUMNS = {
        "send_budget_limit": f"INTEGER NOT NULL DEFAULT {DEFAULT_SEND_BUDGET_LIMIT}",
        "send_budget_used": "INTEGER NOT NULL DEFAULT 0",
        "send_budget_epoch": "INTEGER NOT NULL DEFAULT 1",
        "send_budget_last_reset_at": "REAL",
        "send_budget_last_reserved_at": "REAL",
        "send_budget_last_kind": "TEXT",
        "send_budget_last_run_id": "TEXT",
        "send_budget_held_count": "INTEGER NOT NULL DEFAULT 0",
        "send_budget_last_held_at": "REAL",
        "send_budget_last_held_kind": "TEXT",
        "send_budget_last_held_run_id": "TEXT",
        "send_budget_last_hold_reason": "TEXT",
        "send_budget_updated_at": "REAL",
    }
    _EXECUTION_COLUMN = "send_budget_reservations_json"

    def __init__(self, database_path: Path, *, limit: int) -> None:
        if limit < MIN_SEND_BUDGET_LIMIT or limit > MAX_SEND_BUDGET_LIMIT:
            raise ValueError("Send budget limit is outside the supported range.")
        self.database_path = database_path
        self.limit = limit
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        now = time.time()
        with self._connect() as connection:
            control_columns = {
                str(row["name"])
                for row in connection.execute(
                    "PRAGMA table_info(command_center_control)"
                ).fetchall()
            }
            if not control_columns:
                raise RuntimeError(
                    "Send budget requires the existing shared Command Center control record."
                )
            for column_name, column_type in self._CONTROL_COLUMNS.items():
                if column_name not in control_columns:
                    connection.execute(
                        f"ALTER TABLE command_center_control "
                        f"ADD COLUMN {column_name} {column_type}"
                    )

            execution_columns = {
                str(row["name"])
                for row in connection.execute(
                    "PRAGMA table_info(execution_history)"
                ).fetchall()
            }
            if self._EXECUTION_COLUMN not in execution_columns:
                connection.execute(
                    "ALTER TABLE execution_history ADD COLUMN "
                    f"{self._EXECUTION_COLUMN} TEXT NOT NULL DEFAULT '[]'"
                )

            connection.execute(
                """
                UPDATE command_center_control SET
                    send_budget_limit = ?,
                    send_budget_last_reset_at = COALESCE(send_budget_last_reset_at, ?),
                    send_budget_updated_at = COALESCE(send_budget_updated_at, ?)
                WHERE control_key = ?
                """,
                (self.limit, now, now, self._CONTROL_KEY),
            )

    @staticmethod
    def _optional_text(value: object) -> str | None:
        clean = str(value or "").strip()
        return clean or None

    @staticmethod
    def _kind(value: object) -> SendBudgetKind | None:
        clean = str(value or "").strip()
        if clean in {"worker_dispatch", "hq_review_wake"}:
            return cast(SendBudgetKind, clean)
        return None

    def _state_from_row(self, row: sqlite3.Row) -> SendBudgetState:
        limit = int(row["send_budget_limit"])
        used = int(row["send_budget_used"])
        return SendBudgetState(
            limit=limit,
            used=used,
            remaining=max(limit - used, 0),
            exhausted=used >= limit,
            epoch=int(row["send_budget_epoch"]),
            last_reset_at=(
                float(row["send_budget_last_reset_at"])
                if row["send_budget_last_reset_at"] is not None
                else None
            ),
            last_reserved_at=(
                float(row["send_budget_last_reserved_at"])
                if row["send_budget_last_reserved_at"] is not None
                else None
            ),
            last_reserved_kind=self._kind(row["send_budget_last_kind"]),
            last_reserved_run_id=self._optional_text(row["send_budget_last_run_id"]),
            held_count=int(row["send_budget_held_count"]),
            last_held_at=(
                float(row["send_budget_last_held_at"])
                if row["send_budget_last_held_at"] is not None
                else None
            ),
            last_held_kind=self._kind(row["send_budget_last_held_kind"]),
            last_held_run_id=self._optional_text(row["send_budget_last_held_run_id"]),
            last_hold_reason=self._optional_text(row["send_budget_last_hold_reason"]),
            updated_at=(
                float(row["send_budget_updated_at"])
                if row["send_budget_updated_at"] is not None
                else None
            ),
        )

    def _row(self, connection: sqlite3.Connection) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM command_center_control WHERE control_key = ?",
            (self._CONTROL_KEY,),
        ).fetchone()
        if row is None:
            raise RuntimeError("Shared Command Center control record is missing.")
        return row

    def state(self) -> SendBudgetState:
        with self._connect() as connection:
            return self._state_from_row(self._row(connection))

    @staticmethod
    def _validate_kind(kind: str) -> SendBudgetKind:
        clean = str(kind or "").strip()
        if clean not in {"worker_dispatch", "hq_review_wake"}:
            raise ValueError("Send budget kind is unsupported.")
        return cast(SendBudgetKind, clean)

    def reserve(self, *, kind: str, run_id: str) -> SendBudgetDecision:
        clean_kind = self._validate_kind(kind)
        clean_run_id = str(run_id or "").strip()
        if not clean_run_id:
            raise ValueError("Send budget run_id cannot be empty.")

        now = time.time()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = self._row(connection)
            state = self._state_from_row(row)
            if state.exhausted:
                reason = (
                    f"Global send budget exhausted at {state.used}/{state.limit} attempts "
                    f"in epoch {state.epoch}."
                )
                connection.execute(
                    """
                    UPDATE command_center_control SET
                        send_budget_held_count = send_budget_held_count + 1,
                        send_budget_last_held_at = ?,
                        send_budget_last_held_kind = ?,
                        send_budget_last_held_run_id = ?,
                        send_budget_last_hold_reason = ?,
                        send_budget_updated_at = ?
                    WHERE control_key = ?
                    """,
                    (
                        now,
                        clean_kind,
                        clean_run_id,
                        reason,
                        now,
                        self._CONTROL_KEY,
                    ),
                )
                held_state = self._state_from_row(self._row(connection))
                return SendBudgetDecision(
                    reserved=False,
                    kind=clean_kind,
                    run_id=clean_run_id,
                    epoch=held_state.epoch,
                    sequence=None,
                    reserved_at=None,
                    reason=reason,
                    state=held_state,
                )

            sequence = state.used + 1
            connection.execute(
                """
                UPDATE command_center_control SET
                    send_budget_used = ?,
                    send_budget_last_reserved_at = ?,
                    send_budget_last_kind = ?,
                    send_budget_last_run_id = ?,
                    send_budget_updated_at = ?
                WHERE control_key = ?
                """,
                (
                    sequence,
                    now,
                    clean_kind,
                    clean_run_id,
                    now,
                    self._CONTROL_KEY,
                ),
            )
            reserved_state = self._state_from_row(self._row(connection))
            return SendBudgetDecision(
                reserved=True,
                kind=clean_kind,
                run_id=clean_run_id,
                epoch=reserved_state.epoch,
                sequence=sequence,
                reserved_at=now,
                reason=(
                    f"Reserved global send attempt {sequence}/{reserved_state.limit} "
                    f"in epoch {reserved_state.epoch}."
                ),
                state=reserved_state,
            )

    def reset(self) -> SendBudgetState:
        now = time.time()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                UPDATE command_center_control SET
                    send_budget_used = 0,
                    send_budget_epoch = send_budget_epoch + 1,
                    send_budget_last_reset_at = ?,
                    send_budget_last_reserved_at = NULL,
                    send_budget_last_kind = NULL,
                    send_budget_last_run_id = NULL,
                    send_budget_held_count = 0,
                    send_budget_last_held_at = NULL,
                    send_budget_last_held_kind = NULL,
                    send_budget_last_held_run_id = NULL,
                    send_budget_last_hold_reason = NULL,
                    send_budget_updated_at = ?
                WHERE control_key = ?
                """,
                (now, now, self._CONTROL_KEY),
            )
            return self._state_from_row(self._row(connection))

    def append_execution_evidence(
        self,
        *,
        run_id: str,
        decision: SendBudgetDecision,
    ) -> None:
        if not decision.reserved:
            raise ValueError("A held send-budget decision cannot be execution evidence.")
        clean_run_id = str(run_id or "").strip()
        if not clean_run_id or clean_run_id != decision.run_id:
            raise ValueError("Send-budget evidence run_id does not match its reservation.")

        evidence = decision.evidence()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, send_budget_reservations_json FROM execution_history
                WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
                ORDER BY id
                """,
                (clean_run_id,),
            ).fetchall()
            if len(rows) != 1:
                raise RuntimeError(
                    "Send-budget evidence requires exactly one authoritative Worker send row."
                )
            raw = str(rows[0]["send_budget_reservations_json"] or "[]")
            try:
                current = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise RuntimeError("Existing send-budget evidence is not valid JSON.") from exc
            if not isinstance(current, list):
                raise RuntimeError("Existing send-budget evidence has the wrong shape.")
            if any(
                isinstance(item, dict)
                and item.get("epoch") == evidence["epoch"]
                and item.get("sequence") == evidence["sequence"]
                for item in current
            ):
                return
            current.append(evidence)
            connection.execute(
                "UPDATE execution_history SET send_budget_reservations_json = ? WHERE id = ?",
                (
                    json.dumps(current, sort_keys=True, separators=(",", ":")),
                    int(rows[0]["id"]),
                ),
            )


__all__ = [
    "BUDGET_RECOVERY_CONDITION",
    "CommandCenterSendBudgetStore",
    "DEFAULT_SEND_BUDGET_LIMIT",
    "SendBudgetDecision",
    "SendBudgetState",
    "configured_send_budget_limit",
]
