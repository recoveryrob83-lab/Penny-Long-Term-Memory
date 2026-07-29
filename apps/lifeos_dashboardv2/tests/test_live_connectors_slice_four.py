from __future__ import annotations

import os
import json
import urllib.error
from pathlib import Path

from lifeos_v2.connectors import CalendarConnector, ConnectorManager, RefreshResult, TodoistConnector, TrelloConnector
from lifeos_v2.dashboard_data import overview_from_connectors, overview_model
from lifeos_v2.github_status import GitHubStatusVerifier


def test_todoist_preserves_priority_and_isolates_bad_record(monkeypatch):
    monkeypatch.setenv("TODOIST_API_TOKEN", "test-token")
    connector = TodoistConnector({"projects": [{"id": "p", "name": "Inbox"}]}, lambda *_: {"results": [{"id": 1, "content": "Commitment", "priority": 4, "url": "https://todoist.test/1", "due": {"date": "2026-07-30"}}, {"id": 2}], "next_cursor": None})
    result = connector.refresh()
    assert result.status == "ok" and result.records[0]["extra"]["priority"] == 4
    assert result.records[1]["source_error"]


def test_todoist_current_v1_response_paginates_and_builds_missing_url(monkeypatch):
    monkeypatch.setenv("TODOIST_API_TOKEN", "test-token")
    fixtures = Path(__file__).parent / "fixtures" / "todoist"
    pages = [json.loads((fixtures / "tasks_page_one.json").read_text()), json.loads((fixtures / "tasks_page_two.json").read_text())]
    urls = []
    def transport(url, _headers): urls.append(url); return pages.pop(0)
    result = TodoistConnector({"projects": [{"id": "project-one", "name": "Inbox"}]}, transport).refresh()
    assert result.status == "ok" and [item["source_id"] for item in result.records] == ["task-one", "task-two"]
    assert result.records[0]["source_url"] == "https://app.todoist.com/app/task/task-one"
    assert all("https://api.todoist.com/api/v1/tasks" in url for url in urls)
    assert "project_id=project-one" in urls[0] and "cursor=next-page" in urls[1]


def test_calendar_requires_credentials_without_attempting_live_access(monkeypatch):
    monkeypatch.delenv("GOOGLE_CALENDAR_ICAL_URL", raising=False); monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False); monkeypatch.delenv("GOOGLE_CLIENT_SECRET", raising=False); monkeypatch.delenv("GOOGLE_REFRESH_TOKEN", raising=False)
    result = CalendarConnector({"calendars": [{"id": "primary", "name": "Primary"}]}).refresh()
    assert result.status == "configuration_required" and result.records == []


def test_calendar_ical_feed_normalizes_timed_all_day_cancelled_and_recurring_events(monkeypatch):
    monkeypatch.setenv("GOOGLE_CALENDAR_ICAL_URL", "https://private.example/calendar.ics")
    monkeypatch.setenv("OVERVIEW_PAST_DAYS", "1"); monkeypatch.setenv("OVERVIEW_FUTURE_DAYS", "14")
    feed = (Path(__file__).parent / "fixtures" / "calendar" / "private_feed.ics").read_text()
    result = CalendarConnector({"calendars": [{"id": "primary", "name": "Primary"}]}, ical_transport=lambda _url: feed).refresh()
    records = {item["source_id"]: item for item in result.records}
    assert result.status == "ok" and records["timed-event"]["start_at"].endswith("+00:00")
    assert records["all-day-event"]["start_at"] == "2026-07-30" and records["all-day-event"]["extra"]["all_day"]
    assert records["cancelled-event"]["state"] == "cancelled" and records["recurring-event"]["extra"]["recurrence"] == "FREQ=WEEKLY;COUNT=2"
    assert records["broken-event"]["source_error"] and all("private.example" not in str(item) for item in result.records)


def test_calendar_ical_temporary_failure_keeps_manager_cache_stale(monkeypatch):
    monkeypatch.setenv("GOOGLE_CALENDAR_ICAL_URL", "https://private.example/calendar.ics")
    def fail(_url): raise OSError("temporary failure")
    connector = CalendarConnector({"calendars": [{"id": "primary", "name": "Primary"}]}, ical_transport=fail)
    manager = ConnectorManager(Path(__file__).parents[1] / "config")
    manager.connectors = [connector]
    cached = RefreshResult("calendar", "ok", "2026-07-29T12:00:00+00:00", "2026-07-29T12:00:00+00:00", [{"source_id": "safe-last-known"}])
    manager.cache["calendar"] = cached
    result = manager.refresh_all(force=True)[0]
    assert result.status == "stale" and result.records == cached.records and "private.example" not in str(result)


def test_trello_keeps_flow_distinct_from_commitments(monkeypatch):
    monkeypatch.setenv("TRELLO_API_KEY", "key"); monkeypatch.setenv("TRELLO_API_TOKEN", "token")
    calls = iter([[{"id": "now", "name": "Now", "closed": False}], [{"id": "card", "idList": "now", "name": "Idea", "desc": "Possible", "url": "https://trello.test/card", "labels": [], "idMembers": []}]])
    result = TrelloConnector({"boards": [{"id": "board", "name": "LifeOS Flow Board", "enabled": True}]}, lambda *_: next(calls)).refresh()
    assert result.status == "ok" and result.records[0]["source_system"] == "trello" and result.records[0]["state"] == "open"


def test_missing_credentials_and_cache_are_honest(monkeypatch):
    monkeypatch.delenv("TODOIST_API_TOKEN", raising=False)
    config = Path(__file__).parents[1] / "config"; manager = ConnectorManager(config)
    first = manager.refresh_all()
    assert all(x.status == "configuration_required" for x in first)


def test_github_source_status_is_present_in_fixture_and_live_connector_modes(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert any(item["name"] == "GitHub" for item in overview_model()["sources"])
    results = [{"source_system": name, "status": "ok", "last_success_at": "2026-07-29T12:00:00+00:00", "records": [], "error": None, "recovery_hint": ""} for name in ("todoist", "calendar", "trello", "drive")]
    live = overview_from_connectors(results)
    github = next(item for item in live["sources"] if item["name"] == "GitHub")
    assert github["state"] == "partial"
    assert github["detail"] == "Configured local paths readable; GitHub token not set"


def test_github_verifier_without_token_keeps_local_partial_status(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert GitHubStatusVerifier().verify()["state"] == "partial"


def test_github_verifier_reports_success_only_after_metadata_get(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token"); monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    calls = []
    verifier = GitHubStatusVerifier(lambda url, headers: calls.append((url, headers)) or {"id": 1})
    result = verifier.verify()
    assert result["state"] == "ok" and result["last_success"] and calls[0][0] == "https://api.github.com/repos/owner/repo"
    assert calls[0][1]["Authorization"] == "Bearer test-token"


def test_github_verifier_reports_authentication_failure(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token"); monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    def reject(*_): raise urllib.error.HTTPError("https://api.github.com", 401, "Unauthorized", {}, None)
    assert GitHubStatusVerifier(reject).verify()["state"] == "authentication_required"


def test_github_verifier_keeps_local_partial_status_on_network_failure(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token"); monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    def fail(*_): raise OSError("network unavailable")
    result = GitHubStatusVerifier(fail).verify()
    assert result["state"] == "partial" and "local paths readable" in result["detail"]
