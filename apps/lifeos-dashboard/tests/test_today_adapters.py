from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import httpx

from lifeos_dashboard.adapters.calendar_ical import GoogleCalendarIcalDashboardSource
from lifeos_dashboard.adapters.todoist import TodoistDashboardSource

TIMEZONE = ZoneInfo("America/Chicago")
NOW = datetime(2026, 7, 16, 22, 30, tzinfo=TIMEZONE)


class StaticSource:
    name = "local-github+trello"

    def load(self) -> dict[str, Any]:
        return deepcopy(
            {
                "sources": [
                    {"name": "Todoist", "state": "stale", "freshness": "sample"},
                    {"name": "Calendar", "state": "healthy", "freshness": "sample"},
                ],
                "today": {
                    "date_label": "Old date",
                    "next_event": {
                        "time": "8:30 PM",
                        "title": "WTF Recovery Meeting",
                        "location": "Online",
                    },
                    "commitments": [
                        {"title": "Sample task", "state": "today", "source": "Todoist"}
                    ],
                },
            }
        )


def todoist_response(request: httpx.Request) -> httpx.Response:
    assert request.headers["Authorization"] == "Bearer private-token"
    return httpx.Response(
        200,
        json={
            "results": [
                {
                    "id": "daily-anchor",
                    "content": "Daily recovery anchors",
                    "priority": 3,
                    "due": {"date": "2026-07-17", "is_recurring": True},
                },
                {
                    "id": "daughter",
                    "content": "Call my daughter",
                    "priority": 3,
                    "due": {
                        "date": "2026-07-17T14:00:00",
                        "timezone": "America/Chicago",
                    },
                },
                {
                    "id": "cancel-trial",
                    "content": "Cancel Discovery+ free trial",
                    "priority": 3,
                    "due": {
                        "date": "2026-07-22T09:00:00",
                        "timezone": "America/Chicago",
                    },
                },
                {
                    "id": "future",
                    "content": "Far future task",
                    "priority": 1,
                    "due": {"date": "2026-08-30"},
                },
            ],
            "next_cursor": None,
        },
    )


def calendar_response(request: httpx.Request) -> httpx.Response:
    assert request.url.host == "calendar.test"
    return httpx.Response(
        200,
        text="""BEGIN:VCALENDAR\r
VERSION:2.0\r
BEGIN:VEVENT\r
UID:friday-meeting\r
DTSTART;TZID=America/Chicago:20260717T180000\r
DTEND;TZID=America/Chicago:20260717T193000\r
RRULE:FREQ=WEEKLY;BYDAY=FR\r
SUMMARY:NA Meeting - New Day Recovery Club\r
LOCATION:New Day Recovery Club\r
END:VEVENT\r
BEGIN:VEVENT\r
UID:overnight-work\r
DTSTART;TZID=America/Chicago:20260720T180000\r
DTEND;TZID=America/Chicago:20260721T060000\r
SUMMARY:Marqueto work overnight\r
LOCATION:Marqueto's\r
END:VEVENT\r
END:VCALENDAR\r
""",
    )


def test_todoist_overlays_upcoming_commitments_and_caches(tmp_path: Path) -> None:
    cache = tmp_path / "todoist.json"
    client = httpx.Client(transport=httpx.MockTransport(todoist_response))
    adapter = TodoistDashboardSource(
        StaticSource(),
        api_token="private-token",
        cache_path=cache,
        client=client,
        clock=lambda: NOW,
    )

    payload = adapter.load()

    assert adapter.name == "local-github+trello+todoist"
    assert payload["today"]["date_label"] == "Thursday, July 16"
    assert [item["title"] for item in payload["today"]["commitments"]] == [
        "Call my daughter",
        "Daily recovery anchors",
        "Cancel Discovery+ free trial",
    ]
    assert payload["today"]["commitments"][0]["state"] == "tomorrow · 2:00 PM"
    assert payload["today"]["commitments"][1]["state"] == "tomorrow"
    assert payload["todoist"]["counts"] == {
        "overdue": 0,
        "today": 0,
        "upcoming": 3,
        "shown": 3,
    }
    source = next(item for item in payload["sources"] if item["name"] == "Todoist")
    assert source["state"] == "healthy"
    assert cache.exists()
    client.close()


def test_todoist_uses_cache_without_exposing_token(tmp_path: Path) -> None:
    cache = tmp_path / "todoist.json"
    good = httpx.Client(transport=httpx.MockTransport(todoist_response))
    TodoistDashboardSource(
        StaticSource(),
        api_token="private-token",
        cache_path=cache,
        client=good,
        clock=lambda: NOW,
    ).load()
    good.close()

    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("private-token exploded", request=request)

    failed = httpx.Client(transport=httpx.MockTransport(fail))
    payload = TodoistDashboardSource(
        StaticSource(),
        api_token="private-token",
        cache_path=cache,
        client=failed,
        clock=lambda: NOW,
    ).load()

    assert payload["todoist"]["status"] == "cached"
    assert payload["todoist"]["last_error"] == "Todoist connection failed"
    assert "private-token" not in payload["todoist"]["last_error"]
    failed.close()


def test_calendar_replaces_sample_event_and_expands_recurrence(tmp_path: Path) -> None:
    cache = tmp_path / "calendar.json"
    client = httpx.Client(transport=httpx.MockTransport(calendar_response))
    adapter = GoogleCalendarIcalDashboardSource(
        StaticSource(),
        ical_url="https://calendar.test/private/basic.ics",
        cache_path=cache,
        client=client,
        clock=lambda: NOW,
        horizon_days=10,
    )

    payload = adapter.load()

    assert adapter.name == "local-github+trello+calendar"
    assert payload["today"]["next_event"] == {
        "time": "Tomorrow · 6:00 PM",
        "title": "NA Meeting - New Day Recovery Club",
        "location": "New Day Recovery Club",
    }
    assert payload["calendar"]["event_count"] == 3
    assert "WTF" not in payload["today"]["next_event"]["title"]
    source = next(item for item in payload["sources"] if item["name"] == "Calendar")
    assert source["state"] == "healthy"
    assert cache.exists()
    client.close()


def test_calendar_uses_cache_and_hides_secret_url(tmp_path: Path) -> None:
    cache = tmp_path / "calendar.json"
    good = httpx.Client(transport=httpx.MockTransport(calendar_response))
    GoogleCalendarIcalDashboardSource(
        StaticSource(),
        ical_url="https://calendar.test/private/secret.ics",
        cache_path=cache,
        client=good,
        clock=lambda: NOW,
    ).load()
    good.close()

    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(str(request.url), request=request)

    failed = httpx.Client(transport=httpx.MockTransport(fail))
    payload = GoogleCalendarIcalDashboardSource(
        StaticSource(),
        ical_url="https://calendar.test/private/secret.ics",
        cache_path=cache,
        client=failed,
        clock=lambda: NOW,
    ).load()

    assert payload["calendar"]["status"] == "cached"
    assert payload["calendar"]["last_error"] == "Calendar feed connection failed"
    assert "secret.ics" not in payload["calendar"]["last_error"]
    failed.close()


def test_unconfigured_adapters_preserve_samples(tmp_path: Path) -> None:
    todoist = TodoistDashboardSource(
        StaticSource(),
        api_token=None,
        cache_path=tmp_path / "todoist.json",
        clock=lambda: NOW,
    ).load()
    calendar = GoogleCalendarIcalDashboardSource(
        StaticSource(),
        ical_url=None,
        cache_path=tmp_path / "calendar.json",
        clock=lambda: NOW,
    ).load()

    assert todoist["today"]["commitments"][0]["title"] == "Sample task"
    assert calendar["today"]["next_event"]["title"] == "WTF Recovery Meeting"
    assert todoist["todoist"]["status"] == "not configured"
    assert calendar["calendar"]["status"] == "not configured"
