import sqlite3
from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_registration import WorkerRegistrationService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


PROFILE_PATH = "projects/life-logistics-hq/workers/maintenance_worker.md"


def write_profile(
    repository_root: Path,
    *,
    worker_id: str = "maintenance_worker",
    chat_title: str = "Maintenance_Worker",
) -> Path:
    profile = repository_root / PROFILE_PATH
    profile.parent.mkdir(parents=True)
    profile.write_text(
        "\n".join(
            (
                "---",
                f"worker_id: {worker_id}",
                f"chat_title: {chat_title}",
                "owning_department: maintenance",
                "role: worker",
                "specialization: general",
                "profile_version: 1",
                "---",
                "",
                "# Maintenance Worker",
                "",
                "## Purpose",
                "",
                "Read-only bounded audit profile.",
            )
        ),
        encoding="utf-8",
    )
    return profile


def registration_fixture(
    tmp_path: Path,
) -> tuple[CommandCenterService, WorkerRegistrationService, Path]:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    (repository_root / ".git").mkdir()
    profile = write_profile(repository_root)
    database = tmp_path / "command-center.sqlite3"
    command_center = CommandCenterService(tmp_path, database_path=database)
    service = WorkerRegistrationService(command_center, repository_root)
    return command_center, service, profile


def test_status_lists_only_canonical_unregistered_profiles(tmp_path: Path) -> None:
    _, service, _ = registration_fixture(tmp_path)

    status = service.status()

    assert status["errors"] == []
    assert status["candidates"] == [
        {
            "worker_id": "maintenance_worker",
            "chat_title": "Maintenance_Worker",
            "owning_department": "maintenance",
            "profile_path": PROFILE_PATH,
            "profile_version": 1,
            "specialization": "general",
            "role": "worker",
        }
    ]


def test_registration_requires_confirmation_and_pause(tmp_path: Path) -> None:
    command_center, service, _ = registration_fixture(tmp_path)

    with pytest.raises(WorkerRuntimeError, match="explicit confirmation"):
        service.register_profile(PROFILE_PATH, confirm_registration=False)

    with pytest.raises(WorkerRuntimeError, match="Pause automation"):
        service.register_profile(PROFILE_PATH, confirm_registration=True)

    assert service.runtime.workers() == []
    assert command_center.paused is False


def test_registration_creates_one_route_less_row_and_unknown_hold(tmp_path: Path) -> None:
    command_center, service, profile = registration_fixture(tmp_path)
    before_profile = profile.read_bytes()
    command_center.set_paused(True)

    result = service.register_profile(PROFILE_PATH, confirm_registration=True)

    entry = service.runtime.worker("maintenance_worker")
    route = service.runtime.store.route_state("maintenance_worker")
    assert result["changed"] is True
    assert result["activation_authorized"] is False
    assert entry.chat_title == "Maintenance_Worker"
    assert entry.owning_department == "maintenance"
    assert entry.profile_path == PROFILE_PATH
    assert entry.profile_version == 1
    assert entry.conversation_url is None
    assert entry.route_revision == 0
    assert entry.deployment_state == "enabled"
    assert route is not None
    assert route.availability == "unknown"
    assert route.last_seen_at is None
    assert route.pause_reason == (
        "Registered from canonical profile; exact route not yet linked."
    )
    assert profile.read_bytes() == before_profile

    with sqlite3.connect(service.database_path) as connection:
        registry_count = connection.execute(
            "SELECT COUNT(*) FROM worker_registry WHERE worker_id = ?",
            ("maintenance_worker",),
        ).fetchone()[0]
        history_count = connection.execute(
            "SELECT COUNT(*) FROM execution_history"
        ).fetchone()[0]
    assert registry_count == 1
    assert history_count == 0


def test_exact_repeat_is_idempotent_and_creates_no_second_row(tmp_path: Path) -> None:
    command_center, service, _ = registration_fixture(tmp_path)
    command_center.set_paused(True)
    service.register_profile(PROFILE_PATH, confirm_registration=True)

    repeated = service.register_profile(PROFILE_PATH, confirm_registration=True)

    assert repeated["changed"] is False
    assert "already registered" in repeated["message"]
    with sqlite3.connect(service.database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM worker_registry WHERE worker_id = ?",
            ("maintenance_worker",),
        ).fetchone()[0]
    assert count == 1


def test_noncanonical_title_fails_before_runtime_write(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    write_profile(repository_root, chat_title="Maintenance Worker")
    command_center = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    service = WorkerRegistrationService(command_center, repository_root)
    command_center.set_paused(True)

    with pytest.raises(WorkerRuntimeError, match="canonical exact title"):
        service.register_profile(PROFILE_PATH, confirm_registration=True)

    assert service.runtime.workers() == []


def test_unknown_worker_id_fails_closed(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    write_profile(
        repository_root,
        worker_id="speculative_worker",
        chat_title="Speculative_Worker",
    )
    command_center = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    service = WorkerRegistrationService(command_center, repository_root)
    command_center.set_paused(True)

    with pytest.raises(WorkerRuntimeError, match="canonical title map"):
        service.register_profile(PROFILE_PATH, confirm_registration=True)

    assert service.runtime.workers() == []
