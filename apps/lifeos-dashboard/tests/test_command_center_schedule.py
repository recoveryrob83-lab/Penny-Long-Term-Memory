from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from lifeos_dashboard.command_center import CommandCenterError, CommandCenterService, ExecutionResult
from lifeos_dashboard.command_center_schedule import ScheduleSpec, compute_next_run

CHICAGO = ZoneInfo("America/Chicago")


def timestamp(value: str) -> float:
    return datetime.fromisoformat(value).replace(tzinfo=CHICAGO).timestamp()


def schedule_values(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "name": "Nightly Logistics",
        "destination": "logistics",
        "prompt_type": "custom",
        "custom_prompt": "Run the nightly Logistics sync.",
        "mode": "draft",
        "confirm_send": False,
        "default_destination": "logistics",
        "confirm_destination": False,
        "source_type": "custom",
        "source_prompt_id": None,
        "cadence": "daily",
        "schedule_date": "2099-01-01",
        "schedule_time": "19:00",
        "weekdays": [],
        "timezone": "America/Chicago",
        "enabled": True,
    }
    values.update(overrides)
    return values


def test_once_schedule_returns_future_timestamp_and_then_expires() -> None:
    spec = ScheduleSpec("once", "2099-01-02", "09:30")

    run_at = compute_next_run(spec, after_timestamp=timestamp("2099-01-01T12:00:00"))

    assert run_at == timestamp("2099-01-02T09:30:00")
    assert compute_next_run(spec, after_timestamp=run_at) is None


def test_daily_schedule_advances_to_next_local_day() -> None:
    spec = ScheduleSpec("daily", "2099-01-01", "07:00")

    run_at = compute_next_run(spec, after_timestamp=timestamp("2099-01-03T08:00:00"))

    assert run_at == timestamp("2099-01-04T07:00:00")


def test_weekly_schedule_uses_selected_weekdays() -> None:
    spec = ScheduleSpec("weekly", "2099-01-01", "18:00", weekdays=(0, 4))

    run_at = compute_next_run(spec, after_timestamp=timestamp("2099-01-06T19:00:00"))

    assert datetime.fromtimestamp(run_at, CHICAGO).weekday() in {0, 4}
    assert datetime.fromtimestamp(run_at, CHICAGO) > datetime.fromisoformat(
        "2099-01-06T19:00:00"
    ).replace(tzinfo=CHICAGO)


def test_weekly_schedule_requires_a_weekday() -> None:
    spec = ScheduleSpec("weekly", "2099-01-01", "18:00")

    with pytest.raises(ValueError, match="at least one weekday"):
        compute_next_run(spec, after_timestamp=timestamp("2099-01-01T12:00:00"))


def test_service_persists_and_pauses_schedule(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    first = CommandCenterService(tmp_path, database_path=database)
    created = first.create_schedule(schedule_values())

    second = CommandCenterService(tmp_path, database_path=database)
    schedules = second.schedules()

    assert schedules[0]["id"] == created["id"]
    assert schedules[0]["enabled"] is True
    paused = second.set_schedule_enabled(int(created["id"]), False)
    assert paused is not None
    assert paused["enabled"] is False
    assert paused["next_run_at"] is None


def test_schedule_requires_live_send_confirmation(tmp_path: Path) -> None:
    service = CommandCenterService(tmp_path, database_path=tmp_path / "command-center.sqlite3")

    with pytest.raises(CommandCenterError, match="explicit confirmation"):
        service.create_schedule(schedule_values(mode="send", confirm_send=False))


def test_schedule_requires_destination_mismatch_confirmation(tmp_path: Path) -> None:
    service = CommandCenterService(tmp_path, database_path=tmp_path / "command-center.sqlite3")

    with pytest.raises(CommandCenterError, match="Destination mismatch"):
        service.create_schedule(
            schedule_values(destination="engineering", default_destination="logistics")
        )


def test_one_time_schedule_disables_after_execution(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    service = CommandCenterService(tmp_path, database_path=tmp_path / "command-center.sqlite3")
    created = service.create_schedule(
        schedule_values(cadence="once", schedule_date="2099-01-02", schedule_time="09:30")
    )
    schedule = service.store.get_schedule(int(created["id"]))
    assert schedule is not None

    result = ExecutionResult(
        status="succeeded",
        destination="logistics",
        mode="draft",
        prompt_type="custom",
        exit_code=0,
        started_at=1.0,
        finished_at=2.0,
        stdout="",
        stderr="",
        reason="Completed successfully.",
    )
    monkeypatch.setattr(service, "execute", lambda job: result)

    service._run_scheduled(schedule)

    completed = service.store.get_schedule(int(created["id"]))
    assert completed is not None
    assert completed["enabled"] is False
    assert completed["next_run_at"] is None
    assert completed["last_status"] == "succeeded"
