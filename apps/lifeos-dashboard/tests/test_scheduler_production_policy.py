import time
from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService, ExecutionResult
from lifeos_dashboard.command_center_debug_schedule_runtime import (
    DEBUG_CADENCE,
    DEBUG_COMPLETION_MARKER,
)
from lifeos_dashboard.command_center_schedule_policy_runtime import (
    OVERDUE_GRACE_SECONDS,
    OVERDUE_REASON,
    REARMED_REASON,
)


def schedule_values(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "name": "Production scheduler policy test",
        "destination": "engineering",
        "prompt_type": "custom",
        "custom_prompt": "Scheduler policy test. Do not send.",
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


def result(status: str, reason: str) -> ExecutionResult:
    return ExecutionResult(
        status=status,  # type: ignore[arg-type]
        destination="engineering",
        mode="draft",
        prompt_type="custom",
        exit_code=0 if status == "succeeded" else 1,
        started_at=1.0,
        finished_at=2.0,
        stdout="",
        stderr="",
        reason=reason,
    )


def service(tmp_path: Path) -> CommandCenterService:
    return CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )


def test_overdue_schedule_pauses_without_fake_execution_history(tmp_path: Path) -> None:
    command_center = service(tmp_path)
    created = command_center.create_schedule(schedule_values())
    now = time.time()
    command_center.store.defer_schedule(
        int(created["id"]),
        now - OVERDUE_GRACE_SECONDS - 1,
        "Prepared overdue test.",
    )
    overdue = command_center.store.get_schedule(int(created["id"]))
    assert overdue is not None

    assert command_center._pause_overdue_schedule(overdue, now) is True

    paused = command_center.store.get_schedule(int(created["id"]))
    assert paused is not None
    assert paused["enabled"] is False
    assert paused["next_run_at"] is None
    assert paused["last_status"] == "overdue"
    assert paused["last_reason"] == OVERDUE_REASON
    assert paused["last_run_at"] is None
    assert command_center.history() == []


def test_schedule_inside_grace_window_remains_due_and_enabled(tmp_path: Path) -> None:
    command_center = service(tmp_path)
    created = command_center.create_schedule(schedule_values())
    now = time.time()
    command_center.store.defer_schedule(
        int(created["id"]),
        now - OVERDUE_GRACE_SECONDS + 1,
        "Prepared grace-window test.",
    )
    due = command_center.store.get_schedule(int(created["id"]))
    assert due is not None

    assert command_center._pause_overdue_schedule(due, now) is False

    unchanged = command_center.store.get_schedule(int(created["id"]))
    assert unchanged is not None
    assert unchanged["enabled"] is True
    assert unchanged["next_run_at"] is not None


def test_failed_recurring_run_pauses_immediately(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    command_center = service(tmp_path)
    created = command_center.create_schedule(schedule_values())
    schedule = command_center.store.get_schedule(int(created["id"]))
    assert schedule is not None
    monkeypatch.setattr(
        command_center,
        "execute",
        lambda _job: result("failed", "Destination verification failed."),
    )

    command_center._run_scheduled(schedule)

    paused = command_center.store.get_schedule(int(created["id"]))
    assert paused is not None
    assert paused["enabled"] is False
    assert paused["next_run_at"] is None
    assert paused["last_status"] == "failed"
    assert paused["last_reason"] == "Destination verification failed."


def test_successful_recurring_run_advances_normally(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    command_center = service(tmp_path)
    created = command_center.create_schedule(schedule_values())
    schedule = command_center.store.get_schedule(int(created["id"]))
    assert schedule is not None
    prior_due = float(schedule["next_run_at"])
    monkeypatch.setattr(
        command_center,
        "execute",
        lambda _job: result("succeeded", "Completed successfully."),
    )

    command_center._run_scheduled(schedule)

    advanced = command_center.store.get_schedule(int(created["id"]))
    assert advanced is not None
    assert advanced["enabled"] is True
    assert float(advanced["next_run_at"]) > prior_due
    assert advanced["last_status"] == "succeeded"


def test_manual_resume_rearms_recurring_schedule_from_now(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command_center = service(tmp_path)
    created = command_center.create_schedule(schedule_values())
    schedule = command_center.store.get_schedule(int(created["id"]))
    assert schedule is not None
    monkeypatch.setattr(
        command_center,
        "execute",
        lambda _job: result("failed", "Composer occupied."),
    )
    command_center._run_scheduled(schedule)

    resumed = command_center.set_schedule_enabled(int(created["id"]), True)

    assert resumed is not None
    assert resumed["enabled"] is True
    assert resumed["next_run_at"] is not None
    assert resumed["last_status"] == "rearmed"
    assert resumed["last_reason"] == REARMED_REASON


def test_expired_one_time_schedule_requires_edit_before_resume(tmp_path: Path) -> None:
    command_center = service(tmp_path)
    prepared = command_center._prepare_schedule(
        schedule_values(
            cadence="once",
            schedule_date="2099-01-02",
            schedule_time="09:30",
            enabled=False,
        )
    )
    prepared["schedule_date"] = "2000-01-01"
    prepared["next_run_at"] = None
    created = command_center.store.create_schedule(prepared)

    with pytest.raises(ValueError, match="Edit it to a future time"):
        command_center.set_schedule_enabled(int(created["id"]), True)


def test_failed_debug_attempt_pauses_without_completion_marker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command_center = service(tmp_path)
    created = command_center.create_schedule(
        schedule_values(cadence=DEBUG_CADENCE, mode="draft")
    )
    schedule = command_center.store.get_schedule(int(created["id"]))
    assert schedule is not None
    monkeypatch.setattr(
        command_center,
        "execute",
        lambda _job: result("failed", "Write verification failed."),
    )

    command_center._run_scheduled(schedule)

    paused = command_center.store.get_schedule(int(created["id"]))
    assert paused is not None
    assert paused["enabled"] is False
    assert paused["last_status"] == "failed"
    assert DEBUG_COMPLETION_MARKER not in str(paused["last_reason"])
