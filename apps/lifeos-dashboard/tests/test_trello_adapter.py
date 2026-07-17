from __future__ import annotations

from pathlib import Path

import httpx

from lifeos_dashboard.adapters import SampleDashboardSource, TrelloFlowDashboardSource
from lifeos_dashboard.main import PACKAGE_ROOT


def _sample_source() -> SampleDashboardSource:
    return SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")


def _trello_payload(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path.endswith("/boards/board-1"):
        return httpx.Response(
            200,
            json={"id": "board-1", "name": "LifeOS Flow Board", "url": "https://trello.test/b/1"},
        )
    if path.endswith("/boards/board-1/lists"):
        return httpx.Response(
            200,
            json=[
                {"id": "list-now", "name": "Now", "pos": 1},
                {"id": "list-next", "name": "Next", "pos": 2},
                {"id": "list-waiting", "name": "Waiting", "pos": 3},
                {"id": "list-captured", "name": "Captured", "pos": 4},
            ],
        )
    if path.endswith("/boards/board-1/cards/open"):
        return httpx.Response(
            200,
            json=[
                {
                    "id": "card-now",
                    "idList": "list-now",
                    "name": "Build the live Trello adapter",
                    "desc": "Lane: Engineering / LifeOS",
                    "url": "https://trello.test/c/now",
                    "pos": 1,
                },
                {
                    "id": "card-next-2",
                    "idList": "list-next",
                    "name": "Second next card",
                    "desc": "Lane: Main / Logistics",
                    "url": "https://trello.test/c/next-2",
                    "pos": 2,
                },
                {
                    "id": "card-next-1",
                    "idList": "list-next",
                    "name": "First next card",
                    "desc": "Lane: Business / Office Leaks",
                    "url": "https://trello.test/c/next-1",
                    "pos": 1,
                },
                {
                    "id": "card-waiting",
                    "idList": "list-waiting",
                    "name": "Wait for a real signal",
                    "desc": "Blocked by: enough real-world evidence\n\nDo not overbuild.",
                    "url": "https://trello.test/c/waiting",
                    "pos": 1,
                },
                {
                    "id": "card-captured",
                    "idList": "list-captured",
                    "name": "Future idea",
                    "desc": "",
                    "url": "https://trello.test/c/captured",
                    "pos": 1,
                },
            ],
        )
    return httpx.Response(404, json={"error": "not found"})


def _configured_adapter(cache_path: Path, client: httpx.Client) -> TrelloFlowDashboardSource:
    return TrelloFlowDashboardSource(
        _sample_source(),
        board_id="board-1",
        api_key="key-secret",
        api_token="token-secret",
        cache_path=cache_path,
        api_base_url="https://trello.test/1",
        client=client,
    )


def test_live_trello_overlays_flow_and_writes_cache(tmp_path: Path) -> None:
    cache_path = tmp_path / "trello.json"
    client = httpx.Client(transport=httpx.MockTransport(_trello_payload))
    adapter = _configured_adapter(cache_path, client)

    payload = adapter.load()

    assert adapter.name == "sample+trello"
    assert payload["flow"]["now"]["title"] == "Build the live Trello adapter"
    assert [item["title"] for item in payload["flow"]["next"]] == [
        "First next card",
        "Second next card",
    ]
    assert payload["flow"]["waiting"][0]["reason"] == "enough real-world evidence"
    assert payload["trello"]["counts"] == {
        "now": 1,
        "next": 2,
        "waiting": 1,
        "captured": 1,
    }
    trello_source = next(item for item in payload["sources"] if item["name"] == "Trello")
    assert trello_source["state"] == "healthy"
    assert cache_path.exists()
    client.close()


def test_trello_uses_last_good_cache_after_connection_failure(tmp_path: Path) -> None:
    cache_path = tmp_path / "trello.json"
    good_client = httpx.Client(transport=httpx.MockTransport(_trello_payload))
    _configured_adapter(cache_path, good_client).load()
    good_client.close()

    def fail(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection exploded", request=request)

    failed_client = httpx.Client(transport=httpx.MockTransport(fail))
    payload = _configured_adapter(cache_path, failed_client).load()

    assert payload["flow"]["now"]["title"] == "Build the live Trello adapter"
    assert payload["trello"]["status"] == "cached"
    assert payload["trello"]["last_error"] == "Trello connection failed"
    assert "key-secret" not in payload["trello"]["last_error"]
    assert "token-secret" not in payload["trello"]["last_error"]
    trello_source = next(item for item in payload["sources"] if item["name"] == "Trello")
    assert trello_source["state"] == "stale"
    failed_client.close()


def test_unconfigured_trello_keeps_sample_flow_and_marks_source_stale(tmp_path: Path) -> None:
    adapter = TrelloFlowDashboardSource(
        _sample_source(),
        board_id=None,
        api_key=None,
        api_token=None,
        cache_path=tmp_path / "unused.json",
    )

    payload = adapter.load()

    assert adapter.name == "sample"
    assert payload["flow"]["now"]["title"] == (
        "Define $20 offer boundaries and scope-control response"
    )
    trello_source = next(item for item in payload["sources"] if item["name"] == "Trello")
    assert trello_source == {
        "name": "Trello",
        "state": "stale",
        "freshness": "live access not configured; sample flow shown",
    }
