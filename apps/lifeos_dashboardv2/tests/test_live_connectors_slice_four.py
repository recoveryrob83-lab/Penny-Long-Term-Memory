from __future__ import annotations

import os
import json
from pathlib import Path

from lifeos_v2.connectors import CalendarConnector, ConnectorManager, TodoistConnector, TrelloConnector


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
    monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False); monkeypatch.delenv("GOOGLE_CLIENT_SECRET", raising=False); monkeypatch.delenv("GOOGLE_REFRESH_TOKEN", raising=False)
    result = CalendarConnector({"calendars": [{"id": "primary", "name": "Primary"}]}).refresh()
    assert result.status == "configuration_required" and result.records == []


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
