"""SQLite persistence for LifeOS Worker registry and receiver state."""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from .worker_runtime import (
    ExecutionEnvelope,
    WorkerReceiverState,
    WorkerRegistryEntry,
    WorkerRouteState,
    WorkerRuntimeError,
)


class WorkerRuntimeStore:
    """Persist Worker configuration separately from observed runtime state."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS worker_registry (
                    worker_id TEXT PRIMARY KEY,
                    chat_title TEXT NOT NULL UNIQUE,
                    owning_department TEXT NOT NULL,
                    profile_path TEXT NOT NULL UNIQUE,
                    profile_version INTEGER NOT NULL CHECK(profile_version > 0),
                    specialization TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role = 'worker'),
                    deployment_state TEXT NOT NULL
                        CHECK(deployment_state IN ('enabled', 'paused', 'retired')),
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_worker_registry_deployment
                    ON worker_registry(deployment_state, chat_title);

                CREATE TABLE IF NOT EXISTS worker_route_state (
                    worker_id TEXT PRIMARY KEY,
                    availability TEXT NOT NULL
                        CHECK(availability IN (
                            'available', 'unavailable', 'ambiguous', 'unknown'
                        )),
                    last_seen_at REAL,
                    pause_reason TEXT,
                    updated_at REAL NOT NULL,
                    FOREIGN KEY(worker_id) REFERENCES worker_registry(worker_id)
                );

                CREATE TABLE IF NOT EXISTS worker_receiver_state (
                    worker_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    last_processed_revision INTEGER NOT NULL DEFAULT 0
                        CHECK(last_processed_revision >= 0),
                    last_run_id TEXT,
                    updated_at REAL NOT NULL,
                    PRIMARY KEY(worker_id, task_id),
                    FOREIGN KEY(worker_id) REFERENCES worker_registry(worker_id)
                );
                """
            )

    @staticmethod
    def _registry_from_row(row: sqlite3.Row | None) -> WorkerRegistryEntry | None:
        if row is None:
            return None
        return WorkerRegistryEntry.from_dict(dict(row))

    @staticmethod
    def _route_from_row(row: sqlite3.Row | None) -> WorkerRouteState | None:
        if row is None:
            return None
        return WorkerRouteState(
            worker_id=str(row["worker_id"]),
            availability=str(row["availability"]),  # type: ignore[arg-type]
            last_seen_at=(
                float(row["last_seen_at"]) if row["last_seen_at"] is not None else None
            ),
            pause_reason=(
                str(row["pause_reason"]) if row["pause_reason"] is not None else None
            ),
        )

    @staticmethod
    def _receiver_from_row(row: sqlite3.Row | None) -> WorkerReceiverState | None:
        if row is None:
            return None
        return WorkerReceiverState(
            worker_id=str(row["worker_id"]),
            task_id=str(row["task_id"]),
            last_processed_revision=int(row["last_processed_revision"]),
            last_run_id=(str(row["last_run_id"]) if row["last_run_id"] is not None else None),
        )

    def save_registry_entry(self, entry: WorkerRegistryEntry) -> WorkerRegistryEntry:
        now = time.time()
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO worker_registry(
                        worker_id, chat_title, owning_department, profile_path,
                        profile_version, specialization, role, deployment_state,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(worker_id) DO UPDATE SET
                        chat_title = excluded.chat_title,
                        owning_department = excluded.owning_department,
                        profile_path = excluded.profile_path,
                        profile_version = excluded.profile_version,
                        specialization = excluded.specialization,
                        role = excluded.role,
                        deployment_state = excluded.deployment_state,
                        updated_at = excluded.updated_at
                    """,
                    (
                        entry.worker_id,
                        entry.chat_title,
                        entry.owning_department,
                        entry.profile_path,
                        entry.profile_version,
                        entry.specialization,
                        entry.role,
                        entry.deployment_state,
                        now,
                        now,
                    ),
                )
                row = connection.execute(
                    "SELECT * FROM worker_registry WHERE worker_id = ?",
                    (entry.worker_id,),
                ).fetchone()
        except sqlite3.IntegrityError as exc:
            raise WorkerRuntimeError(
                "Worker registry entry conflicts with an existing ID, title, or profile path."
            ) from exc
        saved = self._registry_from_row(row)
        if saved is None:
            raise WorkerRuntimeError("Worker registry entry was not persisted.")
        return saved

    def registry_entry(self, worker_id: str) -> WorkerRegistryEntry | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM worker_registry WHERE worker_id = ?", (worker_id,)
            ).fetchone()
        return self._registry_from_row(row)

    def list_registry(self) -> list[WorkerRegistryEntry]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM worker_registry ORDER BY chat_title COLLATE NOCASE"
            ).fetchall()
        return [entry for row in rows if (entry := self._registry_from_row(row)) is not None]

    def save_route_state(self, state: WorkerRouteState) -> WorkerRouteState:
        now = time.time()
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO worker_route_state(
                        worker_id, availability, last_seen_at, pause_reason, updated_at
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(worker_id) DO UPDATE SET
                        availability = excluded.availability,
                        last_seen_at = excluded.last_seen_at,
                        pause_reason = excluded.pause_reason,
                        updated_at = excluded.updated_at
                    """,
                    (
                        state.worker_id,
                        state.availability,
                        state.last_seen_at,
                        state.pause_reason,
                        now,
                    ),
                )
                row = connection.execute(
                    "SELECT * FROM worker_route_state WHERE worker_id = ?",
                    (state.worker_id,),
                ).fetchone()
        except sqlite3.IntegrityError as exc:
            raise WorkerRuntimeError(
                "Route state requires an existing Worker registry entry."
            ) from exc
        saved = self._route_from_row(row)
        if saved is None:
            raise WorkerRuntimeError("Worker route state was not persisted.")
        return saved

    def route_state(self, worker_id: str) -> WorkerRouteState | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM worker_route_state WHERE worker_id = ?", (worker_id,)
            ).fetchone()
        return self._route_from_row(row)

    def receiver_state(self, worker_id: str, task_id: str) -> WorkerReceiverState | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM worker_receiver_state
                WHERE worker_id = ? AND task_id = ?
                """,
                (worker_id, task_id),
            ).fetchone()
        return self._receiver_from_row(row)

    def accept_envelope(self, envelope: ExecutionEnvelope) -> WorkerReceiverState:
        """Atomically accept one newer task revision and suppress retries."""

        now = time.time()
        try:
            with self._connect() as connection:
                row = connection.execute(
                    """
                    SELECT * FROM worker_receiver_state
                    WHERE worker_id = ? AND task_id = ?
                    """,
                    (envelope.worker_id, envelope.task_id),
                ).fetchone()
                current = self._receiver_from_row(row)
                if (
                    current is not None
                    and envelope.task_revision <= current.last_processed_revision
                ):
                    raise WorkerRuntimeError(
                        "Envelope revision is stale or already processed."
                    )
                connection.execute(
                    """
                    INSERT INTO worker_receiver_state(
                        worker_id, task_id, last_processed_revision,
                        last_run_id, updated_at
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
                        now,
                    ),
                )
                accepted_row = connection.execute(
                    """
                    SELECT * FROM worker_receiver_state
                    WHERE worker_id = ? AND task_id = ?
                    """,
                    (envelope.worker_id, envelope.task_id),
                ).fetchone()
        except sqlite3.IntegrityError as exc:
            raise WorkerRuntimeError(
                "Envelope acceptance requires an existing Worker registry entry."
            ) from exc
        accepted = self._receiver_from_row(accepted_row)
        if accepted is None:
            raise WorkerRuntimeError("Worker receiver state was not persisted.")
        return accepted
