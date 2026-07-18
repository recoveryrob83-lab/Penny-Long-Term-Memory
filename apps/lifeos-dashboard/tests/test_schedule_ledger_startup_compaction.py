from pathlib import Path

import pytest

from lifeos_dashboard import schedule_ledger_runtime
from lifeos_dashboard.command_center import CommandCenterService


class StartupLedger:
    def __init__(self) -> None:
        self.compact_calls = 0
        self.records: list[dict[str, object]] = []

    def compact(self) -> bool:
        self.compact_calls += 1
        return True

    def record_schedule(self, schedule: dict[str, object]) -> bool:
        self.records.append(dict(schedule))
        return True

    def remove_schedule(self, schedule_id: int) -> bool:
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


def test_empty_dashboard_startup_still_requests_sheet_compaction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ledger = StartupLedger()
    monkeypatch.setattr(
        schedule_ledger_runtime,
        "schedule_ledger_from_environment",
        lambda: ledger,
    )

    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )

    assert service.schedules() == []
    assert ledger.compact_calls == 1
    assert ledger.records == []
    assert service.status()["schedule_ledger"]["state"] == "synced"
