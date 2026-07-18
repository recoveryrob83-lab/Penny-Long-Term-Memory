from lifeos_dashboard.schedule_ledger import (
    GoogleSheetsScheduleLedger,
    occurrence_key,
    utc_iso,
)


def test_occurrence_key_uses_schedule_and_due_timestamp() -> None:
    assert occurrence_key(7, 1234.9) == "v1:7:1234"


def test_utc_iso_is_unambiguous() -> None:
    assert utc_iso(0) == "1970-01-01T00:00:00Z"
    assert utc_iso(None) == ""


def test_row_values_preserve_penny_audit_fields() -> None:
    ledger = GoogleSheetsScheduleLedger("sheet-id")
    schedule = {
        "id": 4,
        "name": "Engineering Daily Sync",
        "destination": "engineering",
        "cadence": "daily",
        "timezone": "America/Chicago",
        "mode": "draft",
        "prompt_type": "custom",
    }
    existing = [""] * 14 + ["2026-07-18T15:00:00Z", "Marked missed by CoS."]

    row = ledger._row_values(
        schedule,
        due_at=100.0,
        state="succeeded",
        started_at=101.0,
        finished_at=102.0,
        reason="Completed successfully.",
        existing=existing,
    )

    assert row[0] == "v1:4:100"
    assert row[7] == "succeeded"
    assert row[14] == "2026-07-18T15:00:00Z"
    assert row[15] == "Marked missed by CoS."
