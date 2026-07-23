"""Canonical exact ChatGPT room titles and bounded active-state migration.

The durable naming authority remains ``memory/HQ_NAMING_STANDARD.md``. This module is the
Engineering-owned executable mapping used by routing, display, and active local-state repair.
It never rewrites historical execution evidence.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Final


CANONICAL_HQ_TITLES: Final[dict[str, str]] = {
    "hub": "LifeOS_HQ",
    "logistics": "Maintenance_HQ",
    "engineering": "Engineering_HQ",
    "business": "Business_HQ",
    "office-leaks": "Office_Leaks_HQ",
    "finance": "Finance_HQ",
    "main": "Chief_of_Staff_HQ",
    "wellness": "Wellness_HQ",
}

CANONICAL_WORKER_TITLES: Final[dict[str, str]] = {
    "engineering_worker": "Engineering_Worker",
}

EXACT_TITLE_ROLLOVER: Final[dict[str, str]] = {
    "LifeOS HQ": "LifeOS_HQ",
    "Life OS Maintenance HQ": "Maintenance_HQ",
    "Engineering HQ": "Engineering_HQ",
    "Business HQ": "Business_HQ",
    "Office Leaks HQ": "Office_Leaks_HQ",
    "Finance HQ": "Finance_HQ",
    "Chief of Staff HQ": "Chief_of_Staff_HQ",
    "Wellness HQ": "Wellness_HQ",
    "Engineering Worker": "Engineering_Worker",
    # Retired exact aliases already accepted by the desktop compatibility shim.
    "Main Assistant HQ": "Chief_of_Staff_HQ",
    "Logistics HQ": "Maintenance_HQ",
    "Life Logistics HQ": "Maintenance_HQ",
}


class RoomTitleMigrationError(RuntimeError):
    """Raised when an active title value cannot be migrated unambiguously."""


def canonical_room_title(value: str) -> str:
    """Translate one exact legacy room title and leave canonical or unknown values unchanged."""
    clean = str(value or "").strip()
    return EXACT_TITLE_ROLLOVER.get(clean, clean)


def migrate_title_text(value: str) -> str:
    """Replace exact known title tokens in one live text value, failing closed on mixed forms."""
    migrated = str(value or "")
    for old_title, canonical_title in sorted(
        EXACT_TITLE_ROLLOVER.items(), key=lambda item: len(item[0]), reverse=True
    ):
        if old_title not in migrated:
            continue
        if canonical_title in migrated:
            raise RoomTitleMigrationError(
                "Active title-bearing value contains both legacy and canonical forms: "
                f"{old_title!r} and {canonical_title!r}."
            )
        migrated = migrated.replace(old_title, canonical_title)
    return migrated


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _migrate_text_rows(
    connection: sqlite3.Connection,
    *,
    table: str,
    id_column: str,
    columns: tuple[str, ...],
    where_clause: str = "",
) -> int:
    selected = ", ".join((id_column, *columns))
    rows = connection.execute(
        f"SELECT {selected} FROM {table} {where_clause}"  # noqa: S608 - fixed internal identifiers
    ).fetchall()
    changed = 0
    for row in rows:
        updates: dict[str, str] = {}
        for index, column in enumerate(columns, start=1):
            original = str(row[index] or "")
            migrated = migrate_title_text(original)
            if migrated != original:
                updates[column] = migrated
        if not updates:
            continue
        assignments = ", ".join(f"{column} = ?" for column in updates)
        connection.execute(
            f"UPDATE {table} SET {assignments} WHERE {id_column} = ?",  # noqa: S608
            (*updates.values(), row[0]),
        )
        changed += 1
    return changed


def migrate_active_title_state(database_path: Path) -> dict[str, int]:
    """Idempotently migrate only live title-bearing SQLite state.

    Preserved by design: ``execution_history`` and every run, wrapper, receipt, checksum,
    lifecycle, and evidence field. Disabled schedule snapshots and retired Worker registry
    entries are also left untouched as inactive evidence/configuration.
    """
    counts = {
        "saved_prompts": 0,
        "enabled_schedules": 0,
        "worker_registry": 0,
    }
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        if _table_exists(connection, "saved_prompts"):
            counts["saved_prompts"] = _migrate_text_rows(
                connection,
                table="saved_prompts",
                id_column="id",
                columns=("name", "prompt"),
            )
        if _table_exists(connection, "scheduled_jobs"):
            counts["enabled_schedules"] = _migrate_text_rows(
                connection,
                table="scheduled_jobs",
                id_column="id",
                columns=("name", "custom_prompt"),
                where_clause="WHERE enabled = 1",
            )
        if _table_exists(connection, "worker_registry"):
            counts["worker_registry"] = _migrate_text_rows(
                connection,
                table="worker_registry",
                id_column="worker_id",
                columns=("chat_title",),
                where_clause="WHERE deployment_state != 'retired'",
            )
        connection.commit()
    except (sqlite3.DatabaseError, RoomTitleMigrationError) as exc:
        connection.rollback()
        raise RoomTitleMigrationError(
            f"Active room-title migration stopped without partial writes: {exc}"
        ) from exc
    finally:
        connection.close()
    return counts


__all__ = [
    "CANONICAL_HQ_TITLES",
    "CANONICAL_WORKER_TITLES",
    "EXACT_TITLE_ROLLOVER",
    "RoomTitleMigrationError",
    "canonical_room_title",
    "migrate_active_title_state",
    "migrate_title_text",
]
