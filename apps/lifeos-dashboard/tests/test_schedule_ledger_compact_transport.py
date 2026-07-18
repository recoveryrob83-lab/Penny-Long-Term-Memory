import httpx

from lifeos_dashboard.schedule_ledger import AppsScriptScheduleLedger


def test_compact_posts_explicit_action(monkeypatch) -> None:
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
                "action": "compact",
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

    assert ledger.compact() is True
    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["action"] == "compact"
    assert payload["secret"] == "secret"
    assert captured["follow_redirects"] is True
    assert ledger.status()["state"] == "synced"
