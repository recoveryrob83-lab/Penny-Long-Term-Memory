from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_registration import WorkerRegistrationService
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry, WorkerRuntimeError


PROFILE_PATH = "projects/life-logistics-hq/workers/maintenance_worker.md"


def write_profile(repository_root: Path, *, owning_department: str) -> None:
    profile = repository_root / PROFILE_PATH
    profile.parent.mkdir(parents=True)
    profile.write_text(
        "\n".join(
            (
                "---",
                "worker_id: maintenance_worker",
                "chat_title: Maintenance_Worker",
                f"owning_department: {owning_department}",
                "role: worker",
                "specialization: general",
                "profile_version: 1",
                "---",
                "",
                "# Maintenance Worker",
            )
        ),
        encoding="utf-8",
    )


def test_profile_title_must_match_owning_department(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    write_profile(repository_root, owning_department="engineering")
    command_center = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    service = WorkerRegistrationService(command_center, repository_root)
    command_center.set_paused(True)

    with pytest.raises(WorkerRuntimeError, match="owning department"):
        service.register_profile(PROFILE_PATH, confirm_registration=True)

    assert service.runtime.workers() == []


def test_status_reports_existing_registry_identity_drift(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    write_profile(repository_root, owning_department="maintenance")
    command_center = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    service = WorkerRegistrationService(command_center, repository_root)
    service.runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="maintenance_worker",
            chat_title="Maintenance_Worker",
            owning_department="maintenance",
            profile_path=PROFILE_PATH,
            profile_version=2,
        )
    )

    status = service.status()

    assert status["candidates"] == []
    assert status["errors"] == [
        {
            "profile_path": PROFILE_PATH,
            "reason": "Existing registry identity conflicts with its canonical profile.",
        }
    ]
