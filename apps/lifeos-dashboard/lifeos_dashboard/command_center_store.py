"""SQLite persistence for Command Center prompts, schedules, and execution history."""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from .command_center_schedule import weekdays_from_storage, weekdays_to_storage


class CommandCenterStore:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS saved_prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    prompt TEXT NOT NULL,
                    default_destination TEXT,
                    origin_type TEXT,
                    origin_prompt_key TEXT,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    prompt_type TEXT NOT NULL,
                    exit_code INTEGER,
                    started_at REAL NOT NULL,
                    finished_at REAL NOT NULL,
                    stdout TEXT NOT NULL,
                    stderr TEXT NOT NULL,
                    reason TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS scheduled_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    destination TEXT NOT NULL,
                    prompt_type TEXT NOT NULL,
                    custom_prompt TEXT NOT NULL DEFAULT '',
                    mode TEXT NOT NULL,
                    confirm_send INTEGER NOT NULL DEFAULT 0,
                    default_destination TEXT,
                    confirm_destination INTEGER NOT NULL DEFAULT 0,
                    source_type TEXT NOT NULL,
                    source_prompt_id INTEGER,
                    cadence TEXT NOT NULL,
                    schedule_date TEXT NOT NULL,
                    schedule_time TEXT NOT NULL,
                    weekdays TEXT NOT NULL DEFAULT '',
                    timezone TEXT NOT NULL,
                    next_run_at REAL,
                    last_run_at REAL,
                    last_status TEXT,
                    last_reason TEXT NOT NULL DEFAULT '',
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_scheduled_jobs_due
                    ON scheduled_jobs(enabled, next_run_at);
                """
            )
            existing_columns = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(saved_prompts)").fetchall()
            }
            for column_name in ("default_destination", "origin_type", "origin_prompt_key"):
                if column_name not in existing_columns:
                    connection.execute(f"ALTER TABLE saved_prompts ADD COLUMN {column_name} TEXT")

    @staticmethod
    def _clean_optional(value: str | None) -> str | None:
        if value is None:
            return None
        clean_value = value.strip()
        return clean_value or None

    @staticmethod
    def _schedule_dict(row: sqlite3.Row | None) -> dict[str, object] | None:
        if row is None:
            return None
        item = dict(row)
        item["enabled"] = bool(item["enabled"])
        item["confirm_send"] = bool(item["confirm_send"])
        item["confirm_destination"] = bool(item["confirm_destination"])
        item["weekdays"] = list(weekdays_from_storage(str(item.get("weekdays") or "")))
        return item

    def list_prompts(self) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, prompt, default_destination, origin_type,
                       origin_prompt_key, created_at, updated_at
                FROM saved_prompts ORDER BY name COLLATE NOCASE
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def save_prompt(
        self,
        name: str,
        prompt: str,
        default_destination: str | None = None,
        origin_type: str | None = None,
        origin_prompt_key: str | None = None,
    ) -> dict[str, object]:
        clean_name = name.strip()
        clean_prompt = prompt.strip()
        if not clean_name:
            raise ValueError("Saved prompt name cannot be empty.")
        if not clean_prompt:
            raise ValueError("Saved prompt text cannot be empty.")
        clean_destination = self._clean_optional(default_destination)
        clean_origin_type = self._clean_optional(origin_type)
        clean_origin_prompt_key = self._clean_optional(origin_prompt_key)
        now = time.time()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO saved_prompts(
                    name, prompt, default_destination, origin_type,
                    origin_prompt_key, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    prompt=excluded.prompt,
                    default_destination=excluded.default_destination,
                    origin_type=excluded.origin_type,
                    origin_prompt_key=excluded.origin_prompt_key,
                    updated_at=excluded.updated_at
                """,
                (
                    clean_name,
                    clean_prompt,
                    clean_destination,
                    clean_origin_type,
                    clean_origin_prompt_key,
                    now,
                    now,
                ),
            )
            row = connection.execute(
                """
                SELECT id, name, prompt, default_destination, origin_type,
                       origin_prompt_key, created_at, updated_at
                FROM saved_prompts WHERE name = ?
                """,
                (clean_name,),
            ).fetchone()
        return dict(row) if row else {}

    def update_prompt(
        self,
        prompt_id: int,
        name: str,
        prompt: str,
        default_destination: str | None = None,
        origin_type: str | None = None,
        origin_prompt_key: str | None = None,
    ) -> dict[str, object] | None:
        clean_name = name.strip()
        clean_prompt = prompt.strip()
        if not clean_name:
            raise ValueError("Saved prompt name cannot be empty.")
        if not clean_prompt:
            raise ValueError("Saved prompt text cannot be empty.")
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    UPDATE saved_prompts SET
                        name = ?,
                        prompt = ?,
                        default_destination = COALESCE(?, default_destination),
                        origin_type = COALESCE(?, origin_type),
                        origin_prompt_key = COALESCE(?, origin_prompt_key),
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        clean_name,
                        clean_prompt,
                        self._clean_optional(default_destination),
                        self._clean_optional(origin_type),
                        self._clean_optional(origin_prompt_key),
                        time.time(),
                        prompt_id,
                    ),
                )
                if cursor.rowcount == 0:
                    return None
                row = connection.execute(
                    """
                    SELECT id, name, prompt, default_destination, origin_type,
                           origin_prompt_key, created_at, updated_at
                    FROM saved_prompts WHERE id = ?
                    """,
                    (prompt_id,),
                ).fetchone()
        except sqlite3.IntegrityError as exc:
            raise ValueError("Another saved prompt already uses that name.") from exc
        return dict(row) if row else None

    def delete_prompt(self, prompt_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM saved_prompts WHERE id = ?", (prompt_id,))
        return cursor.rowcount > 0

    def list_schedules(self) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM scheduled_jobs ORDER BY enabled DESC, next_run_at IS NULL, next_run_at, name COLLATE NOCASE"
            ).fetchall()
        return [self._schedule_dict(row) or {} for row in rows]

    def get_schedule(self, schedule_id: int) -> dict[str, object] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM scheduled_jobs WHERE id = ?", (schedule_id,)
            ).fetchone()
        return self._schedule_dict(row)

    def create_schedule(self, values: dict[str, object]) -> dict[str, object]:
        now = time.time()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO scheduled_jobs(
                    name, enabled, destination, prompt_type, custom_prompt, mode,
                    confirm_send, default_destination, confirm_destination,
                    source_type, source_prompt_id, cadence, schedule_date,
                    schedule_time, weekdays, timezone, next_run_at,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    values["name"],
                    int(bool(values["enabled"])),
                    values["destination"],
                    values["prompt_type"],
                    values["custom_prompt"],
                    values["mode"],
                    int(bool(values["confirm_send"])),
                    values.get("default_destination"),
                    int(bool(values["confirm_destination"])),
                    values["source_type"],
                    values.get("source_prompt_id"),
                    values["cadence"],
                    values["schedule_date"],
                    values["schedule_time"],
                    weekdays_to_storage(values.get("weekdays", [])),
                    values["timezone"],
                    values["next_run_at"],
                    now,
                    now,
                ),
            )
            row = connection.execute(
                "SELECT * FROM scheduled_jobs WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return self._schedule_dict(row) or {}

    def update_schedule(self, schedule_id: int, values: dict[str, object]) -> dict[str, object] | None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE scheduled_jobs SET
                    name = ?, enabled = ?, destination = ?, prompt_type = ?,
                    custom_prompt = ?, mode = ?, confirm_send = ?,
                    default_destination = ?, confirm_destination = ?,
                    source_type = ?, source_prompt_id = ?, cadence = ?,
                    schedule_date = ?, schedule_time = ?, weekdays = ?,
                    timezone = ?, next_run_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    values["name"],
                    int(bool(values["enabled"])),
                    values["destination"],
                    values["prompt_type"],
                    values["custom_prompt"],
                    values["mode"],
                    int(bool(values["confirm_send"])),
                    values.get("default_destination"),
                    int(bool(values["confirm_destination"])),
                    values["source_type"],
                    values.get("source_prompt_id"),
                    values["cadence"],
                    values["schedule_date"],
                    values["schedule_time"],
                    weekdays_to_storage(values.get("weekdays", [])),
                    values["timezone"],
                    values["next_run_at"],
                    time.time(),
                    schedule_id,
                ),
            )
            if cursor.rowcount == 0:
                return None
            row = connection.execute(
                "SELECT * FROM scheduled_jobs WHERE id = ?", (schedule_id,)
            ).fetchone()
        return self._schedule_dict(row)

    def set_schedule_enabled(
        self, schedule_id: int, enabled: bool, next_run_at: float | None
    ) -> dict[str, object] | None:
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE scheduled_jobs SET enabled = ?, next_run_at = ?, updated_at = ? WHERE id = ?",
                (int(enabled), next_run_at, time.time(), schedule_id),
            )
            if cursor.rowcount == 0:
                return None
            row = connection.execute(
                "SELECT * FROM scheduled_jobs WHERE id = ?", (schedule_id,)
            ).fetchone()
        return self._schedule_dict(row)

    def delete_schedule(self, schedule_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM scheduled_jobs WHERE id = ?", (schedule_id,))
        return cursor.rowcount > 0

    def due_schedules(self, now: float, limit: int = 5) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM scheduled_jobs
                WHERE enabled = 1 AND next_run_at IS NOT NULL AND next_run_at <= ?
                ORDER BY next_run_at LIMIT ?
                """,
                (now, limit),
            ).fetchall()
        return [self._schedule_dict(row) or {} for row in rows]

    def defer_schedule(self, schedule_id: int, next_run_at: float, reason: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE scheduled_jobs
                SET next_run_at = ?, last_status = 'deferred', last_reason = ?, updated_at = ?
                WHERE id = ?
                """,
                (next_run_at, reason, time.time(), schedule_id),
            )

    def complete_schedule(
        self,
        schedule_id: int,
        *,
        enabled: bool,
        next_run_at: float | None,
        result: dict[str, object],
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE scheduled_jobs SET
                    enabled = ?, next_run_at = ?, last_run_at = ?,
                    last_status = ?, last_reason = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    int(enabled),
                    next_run_at,
                    result["finished_at"],
                    result["status"],
                    result["reason"],
                    time.time(),
                    schedule_id,
                ),
            )

    def add_history(self, result: dict[str, object]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO execution_history(
                    status, destination, mode, prompt_type, exit_code,
                    started_at, finished_at, stdout, stderr, reason
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result["status"], result["destination"], result["mode"], result["prompt_type"],
                    result["exit_code"], result["started_at"], result["finished_at"],
                    result["stdout"], result["stderr"], result["reason"],
                ),
            )

    def history(self, limit: int = 25) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT status, destination, mode, prompt_type, exit_code,
                       started_at, finished_at, stdout, stderr, reason
                FROM execution_history ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
