from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from lifeos_dashboard.command_center import CommandCenterService, ExecutionResult
from lifeos_dashboard.command_center_debug_schedule_runtime import (
    DEBUG_CADENCE,
    DEBUG_COMPLETION_MARKER,
)
from lifeos_dashboard.command_center_schedule import ScheduleSpec, compute_next_run

CHICAGO = ZoneInfo("America/Chicago")


def timestamp(value: str) -> float:
    return datetime.fromisoformat(value).replace(tzinfo=CHICAGO).timestamp()


def schedule_values(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "name": "Five-minute recurrence test",
        "destination": "engineering",
        "prompt_type": "custom",
        "custom_prompt": "[FIVE-MINUTE RECURRENCE TEST - DO NOT SEND]",
        "mode": "draft",
        "confirm_send": False,
        "default_destination": "engineering",
        "confirm_destination": False,
        "source_type": "custom",
        "source_prompt_id": None,
        "cadence": DEBUG_CADENCE,
        "schedule_date": "2099-01-01",
        "schedule_time": "09:00",
        "weekdays": [],
        "timezone": "America/Chicago",
        "enabled": True,
    }
    values.update(overrides)
    return values


def test_debug_cadence_advances_on_five_minute_boundaries() -> None:
    spec = ScheduleSpec(DEBUG_CADENCE, "2099-01-01", "09:00")

    first = compute_next_run(spec, after_timestamp=timestamp("2099-01-01T09:02:00"))
    second = compute_next_run(spec, after_timestamp=first)

    assert first == timestamp("2099-01-01T09:05:00")
    assert second == timestamp("2099-01-01T09:10:00")


def test_debug_cadence_rejects_live_send(tmp_path: Path) -> None:
    service = CommandCenterService(tmp_path, database_path=tmp_path / "command-center.sqlite3")

    with pytest.raises(ValueError, match="draft-only"):
        service.create_schedule(schedule_values(mode="send", confirm_send=True))


def test_debug_cadence_stops_after_two_completed_attempts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = CommandCenterService(tmp_path, database_path=tmp_path / "command-center.sqlite3")
    created = service.create_schedule(schedule_values())
    finishes = iter((2.0, 4.0))

    def execute(_job: object) -> ExecutionResult:
        finished_at = next(finishes)
        return ExecutionResult(
            status="succeeded",
            destination="engineering",
            mode="draft",
            prompt_type="custom",
            exit_code=0,
            started_at=finished_at - 1,
            finished_at=finished_at,
            stdout="",
            stderr="",
            reason="Completed successfully.",
        )

    monkeypatch.setattr(service, "execute", execute)

    first = service.store.get_schedule(int(created["id"]))
    assert first is not None
    service._run_scheduled(first)

    after_first = service.store.get_schedule(int(created["id"]))
    assert after_first is not None
    assert after_first["enabled"] is True
    assert after_first["next_run_at"] is not None

    service._run_scheduled(after_first)

    completed = service.store.get_schedule(int(created["id"]))
    assert completed is not None
    assert completed["enabled"] is False
    assert completed["next_run_at"] is None
    assert DEBUG_COMPLETION_MARKER in str(completed["last_reason"])

    with pytest.raises(ValueError, match="already completed two attempts"):
        service.set_schedule_enabled(int(created["id"]), True)
