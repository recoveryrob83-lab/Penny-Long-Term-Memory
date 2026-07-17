"""SQLite persistence for Command Center saved prompts and execution history."""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path


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
                """
            )

    def list_prompts(self) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, name, prompt, created_at, updated_at FROM saved_prompts ORDER BY name COLLATE NOCASE"
            ).fetchall()
        return [dict(row) for row in rows]

    def save_prompt(self, name: str, prompt: str) -> dict[str, object]:
        clean_name = name.strip()
        clean_prompt = prompt.strip()
        if not clean_name:
            raise ValueError("Saved prompt name cannot be empty.")
        if not clean_prompt:
            raise ValueError("Saved prompt text cannot be empty.")
        now = time.time()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO saved_prompts(name, prompt, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET prompt=excluded.prompt, updated_at=excluded.updated_at
                """,
                (clean_name, clean_prompt, now, now),
            )
            row = connection.execute(
                "SELECT id, name, prompt, created_at, updated_at FROM saved_prompts WHERE name = ?",
                (clean_name,),
            ).fetchone()
        return dict(row) if row else {}

    def update_prompt(self, prompt_id: int, name: str, prompt: str) -> dict[str, object] | None:
        clean_name = name.strip()
        clean_prompt = prompt.strip()
        if not clean_name:
            raise ValueError("Saved prompt name cannot be empty.")
        if not clean_prompt:
            raise ValueError("Saved prompt text cannot be empty.")
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    "UPDATE saved_prompts SET name = ?, prompt = ?, updated_at = ? WHERE id = ?",
                    (clean_name, clean_prompt, time.time(), prompt_id),
                )
                if cursor.rowcount == 0:
                    return None
                row = connection.execute(
                    "SELECT id, name, prompt, created_at, updated_at FROM saved_prompts WHERE id = ?",
                    (prompt_id,),
                ).fetchone()
        except sqlite3.IntegrityError as exc:
            raise ValueError("Another saved prompt already uses that name.") from exc
        return dict(row) if row else None

    def delete_prompt(self, prompt_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM saved_prompts WHERE id = ?", (prompt_id,))
        return cursor.rowcount > 0

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
