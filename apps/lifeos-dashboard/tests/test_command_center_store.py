import sqlite3
from pathlib import Path

from lifeos_dashboard.command_center import CommandCenterService, ExecutionResult
from lifeos_dashboard.command_center_store import CommandCenterStore


def test_saved_prompts_persist_across_store_instances(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    first = CommandCenterStore(database)
    saved = first.save_prompt(
        "Nightly sync",
        "Run the nightly synchronization.",
        default_destination="logistics",
        origin_type="canonical",
        origin_prompt_key="boot",
    )

    second = CommandCenterStore(database)
    prompts = second.list_prompts()

    assert saved["name"] == "Nightly sync"
    assert saved["default_destination"] == "logistics"
    assert saved["origin_type"] == "canonical"
    assert saved["origin_prompt_key"] == "boot"
    assert prompts == [saved]


def test_existing_saved_prompt_table_is_migrated_without_data_loss(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE saved_prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                prompt TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT INTO saved_prompts(name, prompt, created_at, updated_at) VALUES (?, ?, ?, ?)",
            ("Existing prompt", "Keep this text.", 1.0, 1.0),
        )

    store = CommandCenterStore(database)
    prompts = store.list_prompts()

    assert prompts[0]["name"] == "Existing prompt"
    assert prompts[0]["prompt"] == "Keep this text."
    assert prompts[0]["default_destination"] is None
    assert prompts[0]["origin_type"] is None
    assert prompts[0]["origin_prompt_key"] is None


def test_updating_prompt_preserves_existing_destination_metadata(tmp_path: Path) -> None:
    store = CommandCenterStore(tmp_path / "command-center.sqlite3")
    saved = store.save_prompt(
        "Engineering boot copy",
        "Original text.",
        default_destination="engineering",
        origin_type="canonical",
        origin_prompt_key="boot",
    )

    updated = store.update_prompt(int(saved["id"]), "Engineering boot copy", "Updated text.")

    assert updated is not None
    assert updated["prompt"] == "Updated text."
    assert updated["default_destination"] == "engineering"
    assert updated["origin_type"] == "canonical"
    assert updated["origin_prompt_key"] == "boot"


def test_execution_history_persists_across_service_instances(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    first = CommandCenterService(tmp_path, database_path=database)
    result = ExecutionResult(
        status="succeeded",
        destination="hub",
        mode="draft",
        prompt_type="custom",
        exit_code=0,
        started_at=1.0,
        finished_at=2.0,
        stdout="Draft placed.",
        stderr="",
        reason="Completed successfully.",
    )
    first.store.add_history(result.to_dict())

    second = CommandCenterService(tmp_path, database_path=database)
    history = second.history()

    assert len(history) == 1
    assert history[0]["destination"] == "hub"
    assert history[0]["reason"] == "Completed successfully."


def test_saved_prompt_can_be_deleted(tmp_path: Path) -> None:
    store = CommandCenterStore(tmp_path / "command-center.sqlite3")
    saved = store.save_prompt("Temporary", "Do one temporary thing.")

    assert store.delete_prompt(int(saved["id"])) is True
    assert store.list_prompts() == []


def test_status_exposes_saved_prompts(tmp_path: Path) -> None:
    service = CommandCenterService(tmp_path, database_path=tmp_path / "command-center.sqlite3")
    service.save_prompt(
        "Check status",
        "Check current operational status.",
        default_destination="hub",
    )

    status = service.status()

    assert status["saved_prompts"][0]["name"] == "Check status"
    assert status["saved_prompts"][0]["default_destination"] == "hub"
    assert len(status["destinations"]) == 8
