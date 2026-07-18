from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService, ExecutionResult
from lifeos_dashboard.schedule_ledger import schedule_state


class FakeLedger:
    def __init__(self) -> None:
        self.records: list[dict[str, object]] = []
        self.removed: list[int] = []

    def record_schedule(self, schedule: dict[str, object]) -> bool:
        self.records.append(dict(schedule))
        return True

    def remove_schedule(self, schedule_id: int) -> bool:
        self.removed.append(schedule_id)
        return True

    def status(self) -> dict[str, object]:
        return {
            "configured": True,
            "state": "synced",
            "spreadsheet_id": "sheet-id",
            "spreadsheet_url": "https://docs.google.com/spreadsheets/d/sheet-id/edit",
            "sheet_name": "Run Ledger",
            "last_attempt_at": 1.0,
            "last_success_at": 1.0,
            "last_error": "",
        }


def schedule_values(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "name": "Engineering Daily Sync",
        "destination": "engineering",
        "prompt_type": "custom",
        "custom_prompt": "Run the Engineering daily sync.",
        "mode": "draft",
        "confirm_send": False,
        "default_destination": "engineering",
        "confirm_destination": False,
        "source_type": "custom",
        "source_prompt_id": None,
        "cadence": "daily",
        "schedule_date": "2099-01-01",
        "schedule_time": "09:00",
        "weekdays": [],
        "timezone": "America/Chicago",
        "enabled": True,
    }
    values.update(overrides)
    return values


def build_service(tmp_path: Path) -> tuple[CommandCenterService, FakeLedger]:
    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    ledger = FakeLedger()
    service.schedule_ledger = ledger
    return service, ledger


def test_schedule_create_pause_and_delete_publish_current_row(tmp_path: Path) -> None:
    service, ledger = build_service(tmp_path)

    created = service.create_schedule(schedule_values())
    paused = service.set_schedule_enabled(int(created["id"]), False)
    deleted = service.delete_schedule(int(created["id"]))

    assert ledger.records[0]["id"] == created["id"]
    assert paused is not None
    assert ledger.records[-1]["enabled"] is False
    assert deleted is True
    assert ledger.removed == [int(created["id"])]


def test_scheduled_result_updates_same_schedule_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, ledger = build_service(tmp_path)
    created = service.create_schedule(schedule_values())
    ledger.records.clear()
    schedule = service.store.get_schedule(int(created["id"]))
    assert schedule is not None
    original_due = float(schedule["next_run_at"])
    result = ExecutionResult(
        status="succeeded",
        destination="engineering",
        mode="draft",
        prompt_type="custom",
        exit_code=0,
        started_at=100.0,
        finished_at=101.0,
        stdout="",
        stderr="",
        reason="Completed successfully.",
    )
    monkeypatch.setattr(service, "execute", lambda job: result)

    service._run_scheduled(schedule)

    latest = ledger.records[-1]
    assert latest["id"] == created["id"]
    assert latest["last_status"] == "succeeded"
    assert latest["last_run_at"] == 101.0
    assert float(latest["next_run_at"]) > original_due
    assert service.status()["schedule_ledger"]["state"] == "synced"


def test_debug_recurrence_publishes_final_completed_snapshot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, ledger = build_service(tmp_path)
    created = service.create_schedule(
        schedule_values(
            cadence="debug_5m",
            schedule_date="2099-01-01",
            schedule_time="09:00",
        )
    )
    ledger.records.clear()
    results = iter(
        [
            ExecutionResult(
                "succeeded",
                "engineering",
                "draft",
                "custom",
                0,
                100.0,
                101.0,
                "",
                "",
                "Completed successfully.",
            ),
            ExecutionResult(
                "succeeded",
                "engineering",
                "draft",
                "custom",
                0,
                200.0,
                201.0,
                "",
                "",
                "Completed successfully.",
            ),
        ]
    )
    monkeypatch.setattr(service, "execute", lambda job: next(results))

    first = service.store.get_schedule(int(created["id"]))
    assert first is not None
    service._run_scheduled(first)
    second = service.store.get_schedule(int(created["id"]))
    assert second is not None
    service._run_scheduled(second)

    final_snapshot = ledger.records[-1]
    assert final_snapshot["enabled"] is False
    assert final_snapshot["next_run_at"] is None
    assert schedule_state(final_snapshot) == "Completed"
