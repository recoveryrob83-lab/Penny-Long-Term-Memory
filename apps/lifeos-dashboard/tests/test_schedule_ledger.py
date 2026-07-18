import httpx

from lifeos_dashboard.schedule_ledger import (
    AppsScriptScheduleLedger,
    google_datetime,
    schedule_state,
    utc_iso,
)


def schedule() -> dict[str, object]:
    return {
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


def test_row_values_leave_health_formula_to_bound_script() -> None:
    ledger = AppsScriptScheduleLedger(
        "sheet-id",
        "https://script.example/exec",
        "secret",
    )

    row = ledger._row_values(schedule())

    assert len(row) == 17
    assert row[0] == 4
    assert row[9] == "Active"
    assert row[12] == google_datetime(100.0)
    assert row[13] == google_datetime(90.0)


def test_signed_apps_script_upsert_and_redirect_handling(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_post(
        url: str,
        *,
        json: dict[str, object],
        timeout: float,
        follow_redirects: bool,
    ) -> httpx.Response:
        captured.update(
            {
                "url": url,
                "json": json,
                "timeout": timeout,
                "follow_redirects": follow_redirects,
            }
        )
        return httpx.Response(
            200,
            json={
                "ok": True,
                "spreadsheet_id": "sheet-id",
                "sheet_name": "Run Ledger",
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)
    ledger = AppsScriptScheduleLedger(
        "sheet-id",
        "https://script.example/exec",
        "secret",
    )

    assert ledger.record_schedule(schedule()) is True

    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["action"] == "upsert"
    assert payload["secret"] == "secret"
    assert len(payload["values"]) == 17
    assert captured["follow_redirects"] is True
    assert ledger.status()["state"] == "synced"


def test_rejected_apps_script_response_sets_visible_error(monkeypatch) -> None:
    def fake_post(url: str, **kwargs: object) -> httpx.Response:
        return httpx.Response(
            200,
            json={"ok": False, "error": "Unauthorized ledger request."},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)
    ledger = AppsScriptScheduleLedger(
        "sheet-id",
        "https://script.example/exec",
        "secret",
    )

    assert ledger.record_schedule(schedule()) is False
    assert ledger.status()["state"] == "error"
    assert "Unauthorized" in str(ledger.status()["last_error"])
