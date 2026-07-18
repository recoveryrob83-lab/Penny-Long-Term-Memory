from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService, ExecutionResult
from lifeos_dashboard.command_center_debug_schedule_runtime import DEBUG_COMPLETION_MARKER


class FakeLedger:
    def __init__(self) -> None:
        self.planned: list[dict[str, object]] = []
        self.states: list[tuple[dict[str, object], str, str]] = []
        self.results: list[tuple[dict[str, object], float, dict[str, object]]] = []

    def record_planned(self, schedule: dict[str, object]) -> bool:
        self.planned.append(dict(schedule))
        return True

    def record_state(
        self,
        schedule: dict[str, object],
        state: str,
        reason: str,
    ) -> bool:
        self.states.append((dict(schedule), state, reason))
        return True

    def record_result(
        self,
        schedule: dict[str, object],
        due_at: float,
        result: dict[str, object],
    ) -> bool:
        self.results.append((dict(schedule), due_at, dict(result)))
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


def test_schedule_create_and_pause_publish_occurrence_state(tmp_path: Path) -> None:
    service, ledger = build_service(tmp_path)

    created = service.create_schedule(schedule_values())
    service.set_schedule_enabled(int(created["id"]), False)

    assert ledger.planned[0]["id"] == created["id"]
    assert ledger.states[-1][1] == "canceled"
    assert "paused" in ledger.states[-1][2].casefold()


def test_scheduled_result_and_next_occurrence_are_published(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, ledger = build_service(tmp_path)
    created = service.create_schedule(schedule_values())
    ledger.planned.clear()
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

    def execute_and_record(job: object) -> ExecutionResult:
        service.store.add_history(result.to_dict())
        return result

    monkeypatch.setattr(service, "execute", execute_and_record)

    service._run_scheduled(schedule)

    assert ledger.results[0][1] == original_due
    assert ledger.results[0][2]["status"] == "succeeded"
    assert len(ledger.planned) == 1
    assert float(ledger.planned[0]["next_run_at"]) > original_due
    assert service.status()["schedule_ledger"]["state"] == "synced"


def test_debug_recurrence_cancels_the_unused_third_occurrence(
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
    ledger.planned.clear()
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

    def execute_and_record(job: object) -> ExecutionResult:
        result = next(results)
        service.store.add_history(result.to_dict())
        return result

    monkeypatch.setattr(service, "execute", execute_and_record)

    first = service.store.get_schedule(int(created["id"]))
    assert first is not None
    service._run_scheduled(first)
    second = service.store.get_schedule(int(created["id"]))
    assert second is not None
    service._run_scheduled(second)

    completed = service.store.get_schedule(int(created["id"]))
    assert completed is not None
    assert completed["enabled"] is False
    assert ledger.states[-1][1] == "canceled"
    assert DEBUG_COMPLETION_MARKER in ledger.states[-1][2]
