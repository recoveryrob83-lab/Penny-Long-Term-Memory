from lifeos_dashboard.schedule_ledger import (
    GoogleSheetsScheduleLedger,
    google_datetime,
    schedule_state,
    utc_iso,
)


def test_google_datetime_uses_sheets_serial_date() -> None:
    assert google_datetime(0) == 25569.0
    assert google_datetime(None) == ""


def test_utc_iso_is_unambiguous() -> None:
    assert utc_iso(0) == "1970-01-01T00:00:00Z"
    assert utc_iso(None) == ""


def test_schedule_state_distinguishes_active_paused_and_completed() -> None:
    assert schedule_state({"enabled": True}) == "Active"
    assert schedule_state({"enabled": False, "cadence": "daily"}) == "Paused"
    assert schedule_state(
        {"enabled": False, "cadence": "once", "last_status": "succeeded"}
    ) == "Completed"


def test_row_values_include_dynamic_overdue_health_formula() -> None:
    ledger = GoogleSheetsScheduleLedger("sheet-id")
    schedule = {
        "id": 4,
        "name": "Engineering Daily Sync",
        "destination": "engineering",
        "cadence": "daily",
        "schedule_date": "2099-01-01",
        "schedule_time": "09:00",
        "weekdays": [],
        "timezone": "America/Chicago",
        "enabled": True,
        "mode": "draft",
        "prompt_type": "custom",
        "next_run_at": 100.0,
        "last_run_at": 90.0,
        "last_status": "succeeded",
        "last_reason": "Completed successfully.",
    }

    row = ledger._row_values(schedule, 2)

    assert row[0] == 4
    assert row[9] == "Active"
    assert row[12] == google_datetime(100.0)
    assert row[13] == google_datetime(90.0)
    assert row[17] == (
        '=IF(J2<>"Active",J2,IF(M2="","No future run",'
        'IF(M2+TIME(0,5,0)<NOW(),"OVERDUE","On schedule")))'
    )
