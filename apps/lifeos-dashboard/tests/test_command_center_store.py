from pathlib import Path

from lifeos_dashboard.command_center import CommandCenterService, CommandJob, ExecutionResult
from lifeos_dashboard.command_center_store import CommandCenterStore


def test_saved_prompts_persist_across_store_instances(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    first = CommandCenterStore(database)
    saved = first.save_prompt("Nightly sync", "Run the nightly synchronization.")

    second = CommandCenterStore(database)
    prompts = second.list_prompts()

    assert saved["name"] == "Nightly sync"
    assert prompts == [saved]


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
    service.save_prompt("Check status", "Check current operational status.")

    status = service.status()

    assert status["saved_prompts"][0]["name"] == "Check status"
    assert len(status["destinations"]) == 8
