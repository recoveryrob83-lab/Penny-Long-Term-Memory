import sqlite3
from pathlib import Path

import pytest

from lifeos_dashboard.room_titles import (
    CANONICAL_HQ_TITLES,
    RoomTitleMigrationError,
    canonical_room_title,
    migrate_active_title_state,
)


EXPECTED_HQ_TITLES = {
    "hub": "LifeOS_HQ",
    "logistics": "Maintenance_HQ",
    "engineering": "Engineering_HQ",
    "business": "Business_HQ",
    "office-leaks": "Office_Leaks_HQ",
    "finance": "Finance_HQ",
    "main": "Chief_of_Staff_HQ",
    "wellness": "Wellness_HQ",
}


def initialize(database: Path) -> None:
    with sqlite3.connect(database) as connection:
        connection.executescript(
            """
            CREATE TABLE saved_prompts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                prompt TEXT
            );
            CREATE TABLE scheduled_jobs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                custom_prompt TEXT,
                enabled INTEGER NOT NULL
            );
            CREATE TABLE worker_registry (
                worker_id TEXT PRIMARY KEY,
                chat_title TEXT,
                deployment_state TEXT NOT NULL
            );
            CREATE TABLE execution_history (
                id INTEGER PRIMARY KEY,
                destination TEXT,
                hq_wake_target TEXT
            );
            """
        )


def test_canonical_title_map_preserves_stable_destination_keys() -> None:
    assert CANONICAL_HQ_TITLES == EXPECTED_HQ_TITLES
    assert canonical_room_title("Engineering HQ") == "Engineering_HQ"
    assert canonical_room_title("Engineering_HQ") == "Engineering_HQ"
    assert canonical_room_title("Unrelated title") == "Unrelated title"


def test_active_migration_is_idempotent_and_preserves_history(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    initialize(database)
    with sqlite3.connect(database) as connection:
        connection.execute(
            "INSERT INTO saved_prompts VALUES (1, ?, ?)",
            ("Engineering HQ boot", "Review in Chief of Staff HQ."),
        )
        connection.execute(
            "INSERT INTO scheduled_jobs VALUES (1, ?, ?, 1)",
            ("LifeOS HQ morning", "Draft in Office Leaks HQ."),
        )
        connection.execute(
            "INSERT INTO scheduled_jobs VALUES (2, ?, ?, 0)",
            ("Finance HQ archived", "Draft in Wellness HQ."),
        )
        connection.execute(
            "INSERT INTO worker_registry VALUES (?, ?, ?)",
            ("engineering_worker", "Engineering Worker", "enabled"),
        )
        connection.execute(
            "INSERT INTO worker_registry VALUES (?, ?, ?)",
            ("retired_worker", "Engineering Worker", "retired"),
        )
        connection.execute(
            "INSERT INTO execution_history VALUES (1, ?, ?)",
            ("Engineering HQ", "Chief of Staff HQ"),
        )

    first = migrate_active_title_state(database)
    second = migrate_active_title_state(database)

    assert first == {
        "saved_prompts": 1,
        "enabled_schedules": 1,
        "worker_registry": 1,
    }
    assert second == {
        "saved_prompts": 0,
        "enabled_schedules": 0,
        "worker_registry": 0,
    }
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT name, prompt FROM saved_prompts WHERE id = 1"
        ).fetchone() == ("Engineering_HQ boot", "Review in Chief_of_Staff_HQ.")
        assert connection.execute(
            "SELECT name, custom_prompt FROM scheduled_jobs WHERE id = 1"
        ).fetchone() == ("LifeOS_HQ morning", "Draft in Office_Leaks_HQ.")
        assert connection.execute(
            "SELECT name, custom_prompt FROM scheduled_jobs WHERE id = 2"
        ).fetchone() == ("Finance HQ archived", "Draft in Wellness HQ.")
        assert connection.execute(
            "SELECT chat_title FROM worker_registry WHERE worker_id = 'engineering_worker'"
        ).fetchone() == ("Engineering_Worker",)
        assert connection.execute(
            "SELECT chat_title FROM worker_registry WHERE worker_id = 'retired_worker'"
        ).fetchone() == ("Engineering Worker",)
        assert connection.execute(
            "SELECT destination, hq_wake_target FROM execution_history WHERE id = 1"
        ).fetchone() == ("Engineering HQ", "Chief of Staff HQ")


def test_ambiguous_active_value_rolls_back_every_change(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    initialize(database)
    with sqlite3.connect(database) as connection:
        connection.execute(
            "INSERT INTO saved_prompts VALUES (1, ?, ?)",
            ("Business HQ safe row", "Normal prompt."),
        )
        connection.execute(
            "INSERT INTO saved_prompts VALUES (2, ?, ?)",
            ("Ambiguous", "Use Engineering HQ and Engineering_HQ."),
        )

    with pytest.raises(RoomTitleMigrationError, match="without partial writes"):
        migrate_active_title_state(database)

    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT name, prompt FROM saved_prompts ORDER BY id"
        ).fetchall() == [
            ("Business HQ safe row", "Normal prompt."),
            ("Ambiguous", "Use Engineering HQ and Engineering_HQ."),
        ]
