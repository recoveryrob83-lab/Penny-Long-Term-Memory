"""SQLite persistence for LifeOS Worker receiver acceptance and outcomes."""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from .worker_command_center import WorkerExecutionHistoryStore
from .worker_receiver_models import (
    ALLOWED_OUTCOMES,
    ControlledOutcome,
    ExecutionEvidence,
    ReceiverAssignment,
    ReceiverOutcomeRecord,
    WorkerAuthorityProfile,
    canonical_json,
)
from .worker_runtime import WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService


class WorkerReceiverStore:
    """Persist receiver state into the existing authoritative execution-history row."""

    _COLUMNS = {
        "profile_version": "INTEGER",
        "owning_department": "TEXT",
        "task_class": "TEXT",
        "authorization_class": "TEXT",
        "procedure_checksum": "TEXT",
        "parameters_checksum": "TEXT",
        "source_references_json": "TEXT",
        "requested_read_scopes_json": "TEXT",
        "requested_write_scopes_json": "TEXT",
        "receiver_accepted_at": "REAL",
        "receiver_reason": "TEXT",
        "receiver_evidence_json": "TEXT",
        "receiver_verification_state": "TEXT",
        "receiver_completion_state": "TEXT",
        "actual_read_scopes_json": "TEXT",
        "actual_write_scopes_json": "TEXT",
        "actual_tools_json": "TEXT",
        "external_actions_verified": "INTEGER",
    }

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        WorkerExecutionHistoryStore(database_path)
        WorkerRuntimeService(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
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
    def _require_one_history_row(connection: sqlite3.Connection, run_id: str) -> sqlite3.Row:
        rows = connection.execute(
            """
            SELECT id, controlled_outcome, receiver_accepted_at
            FROM execution_history WHERE run_id = ?
            """,
            (run_id,),
        ).fetchall()
        if not rows:
            raise WorkerRuntimeError("Receiver requires one existing transport-history row.")
        if len(rows) > 1:
            raise WorkerRuntimeError("Receiver found ambiguous duplicate transport-history rows.")
        return rows[0]

    @staticmethod
    def _metadata_values(
        assignment: ReceiverAssignment, profile: WorkerAuthorityProfile
    ) -> tuple[object, ...]:
        return (
            profile.profile_version,
            profile.owning_department,
            assignment.task_class,
            assignment.authorization_class,
            assignment.procedure_checksum,
            assignment.parameters_checksum,
            canonical_json(assignment.source_references),
            canonical_json(assignment.requested_read_scopes),
            canonical_json(assignment.requested_write_scopes),
        )

    def record_terminal_preflight(
        self,
        assignment: ReceiverAssignment,
        profile: WorkerAuthorityProfile,
        outcome: ControlledOutcome,
        reason: str,
    ) -> ReceiverOutcomeRecord:
        if outcome not in {"REPORT_AND_HOLD", "ELEVATE_FOR_APPROVAL"}:
            raise WorkerRuntimeError("Preflight may record only a hold or elevation.")
        with self._connect() as connection:
            row = self._require_one_history_row(connection, assignment.envelope.run_id)
            if row["controlled_outcome"] is not None:
                raise WorkerRuntimeError("This run already has a controlled outcome.")
            connection.execute(
                """
                UPDATE execution_history SET
                    profile_version = ?, owning_department = ?, task_class = ?,
                    authorization_class = ?, procedure_checksum = ?,
                    parameters_checksum = ?, source_references_json = ?,
                    requested_read_scopes_json = ?, requested_write_scopes_json = ?,
                    controlled_outcome = ?, receiver_reason = ?,
                    receiver_verification_state = 'unavailable',
                    receiver_completion_state = 'not_attempted'
                WHERE id = ?
                """,
                (
                    *self._metadata_values(assignment, profile),
                    outcome,
                    reason,
                    row["id"],
                ),
            )
        return ReceiverOutcomeRecord(
            run_id=assignment.envelope.run_id,
            outcome=outcome,
            reason=reason,
            verification_state="unavailable",
            evidence_references=(),
        )

    def accept(self, assignment: ReceiverAssignment, profile: WorkerAuthorityProfile) -> float:
        """Atomically consume one semantically valid revision and mark the run accepted."""

        accepted_at = time.time()
        envelope = assignment.envelope
        with self._connect() as connection:
            history_row = self._require_one_history_row(connection, envelope.run_id)
            if history_row["controlled_outcome"] is not None:
                raise WorkerRuntimeError("This run already has a controlled outcome.")
            if history_row["receiver_accepted_at"] is not None:
                raise WorkerRuntimeError("This run was already accepted by the receiver.")
            current = connection.execute(
                """
                SELECT last_processed_revision
                FROM worker_receiver_state
                WHERE worker_id = ? AND task_id = ?
                """,
                (envelope.worker_id, envelope.task_id),
            ).fetchone()
            if current is not None and envelope.task_revision <= int(
                current["last_processed_revision"]
            ):
                raise WorkerRuntimeError("Envelope revision is stale or already processed.")
            connection.execute(
                """
                INSERT INTO worker_receiver_state(
                    worker_id, task_id, last_processed_revision, last_run_id, updated_at
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(worker_id, task_id) DO UPDATE SET
                    last_processed_revision = excluded.last_processed_revision,
                    last_run_id = excluded.last_run_id,
                    updated_at = excluded.updated_at
                """,
                (
                    envelope.worker_id,
                    envelope.task_id,
                    envelope.task_revision,
                    envelope.run_id,
                    accepted_at,
                ),
            )
            connection.execute(
                """
                UPDATE execution_history SET
                    profile_version = ?, owning_department = ?, task_class = ?,
                    authorization_class = ?, procedure_checksum = ?,
                    parameters_checksum = ?, source_references_json = ?,
                    requested_read_scopes_json = ?, requested_write_scopes_json = ?,
                    receiver_accepted_at = ?, receiver_reason = ?
                WHERE id = ?
                """,
                (
                    *self._metadata_values(assignment, profile),
                    accepted_at,
                    "Semantic receiver validation passed.",
                    history_row["id"],
                ),
            )
        return accepted_at

    def finalize(
        self,
        assignment: ReceiverAssignment,
        outcome: ControlledOutcome,
        reason: str,
        evidence: ExecutionEvidence,
    ) -> ReceiverOutcomeRecord:
        if outcome not in ALLOWED_OUTCOMES:
            raise WorkerRuntimeError("Controlled outcome is invalid.")
        with self._connect() as connection:
            row = self._require_one_history_row(connection, assignment.envelope.run_id)
            if row["receiver_accepted_at"] is None:
                raise WorkerRuntimeError("Receiver outcome requires an accepted run.")
            if row["controlled_outcome"] is not None:
                raise WorkerRuntimeError("This run already has a controlled outcome.")
            receiver_state = connection.execute(
                """
                SELECT last_processed_revision, last_run_id
                FROM worker_receiver_state
                WHERE worker_id = ? AND task_id = ?
                """,
                (assignment.envelope.worker_id, assignment.envelope.task_id),
            ).fetchone()
            if (
                receiver_state is None
                or int(receiver_state["last_processed_revision"])
                != assignment.envelope.task_revision
                or str(receiver_state["last_run_id"] or "") != assignment.envelope.run_id
            ):
                raise WorkerRuntimeError("Receiver state does not match the accepted run.")
            connection.execute(
                """
                UPDATE execution_history SET
                    controlled_outcome = ?, receiver_reason = ?,
                    receiver_evidence_json = ?, receiver_verification_state = ?,
                    receiver_completion_state = ?, actual_read_scopes_json = ?,
                    actual_write_scopes_json = ?, actual_tools_json = ?,
                    external_actions_verified = ?
                WHERE id = ?
                """,
                (
                    outcome,
                    reason,
                    canonical_json(evidence.evidence_references),
                    evidence.verification_state,
                    evidence.completion_state,
                    canonical_json(evidence.actual_read_scopes),
                    canonical_json(evidence.actual_write_scopes),
                    canonical_json(evidence.actual_tools),
                    int(evidence.external_actions_verified),
                    row["id"],
                ),
            )
        return ReceiverOutcomeRecord(
            run_id=assignment.envelope.run_id,
            outcome=outcome,
            reason=reason,
            verification_state=evidence.verification_state,
            evidence_references=evidence.evidence_references,
        )
