"""Read-only Trello Flow Board adapter with a local last-good cache."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from .base import DashboardSource

TRELLO_API_BASE_URL = "https://api.trello.com/1"


class TrelloFlowDashboardSource:
    """Overlay a dashboard snapshot with live Trello Now, Next, and Waiting state."""

    def __init__(
        self,
        fallback_source: DashboardSource,
        *,
        board_id: str | None,
        api_key: str | None,
        api_token: str | None,
        cache_path: Path,
        api_base_url: str = TRELLO_API_BASE_URL,
        client: httpx.Client | None = None,
        next_limit: int = 3,
        waiting_limit: int = 3,
    ) -> None:
        self._fallback_source = fallback_source
        self._board_id = (board_id or "").strip()
        self._api_key = (api_key or "").strip()
        self._api_token = (api_token or "").strip()
        self._cache_path = cache_path
        self._api_base_url = api_base_url.rstrip("/")
        self._client = client
        self._next_limit = next_limit
        self._waiting_limit = waiting_limit

    @classmethod
    def from_environment(
        cls,
        fallback_source: DashboardSource,
        *,
        cache_path: Path,
    ) -> TrelloFlowDashboardSource:
        """Create a Trello source from ignored local environment settings."""
        return cls(
            fallback_source,
            board_id=os.getenv("TRELLO_BOARD_ID"),
            api_key=os.getenv("TRELLO_API_KEY"),
            api_token=os.getenv("TRELLO_API_TOKEN"),
            cache_path=cache_path,
            api_base_url=os.getenv("TRELLO_API_BASE_URL", TRELLO_API_BASE_URL),
        )

    @property
    def configured(self) -> bool:
        """Return whether all required read credentials are available."""
        return bool(self._board_id and self._api_key and self._api_token)

    @property
    def name(self) -> str:
        """Report Trello in the mode only after live access is configured."""
        if self.configured:
            return f"{self._fallback_source.name}+trello"
        return self._fallback_source.name

    def load(self) -> dict[str, Any]:
        """Return fallback dashboard data with Trello flow overlaid when possible."""
        payload = deepcopy(self._fallback_source.load())

        if not self.configured:
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="stale",
                freshness="live access not configured; sample flow shown",
            )
            payload["trello"] = {
                "status": "not configured",
                "cache": "unused",
            }
            return payload

        try:
            snapshot = self._fetch_snapshot()
            self._write_cache(snapshot)
            payload["flow"] = deepcopy(snapshot["flow"])
            payload["trello"] = deepcopy(snapshot["trello"])
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="healthy",
                freshness=self._freshness(snapshot),
            )
            return payload
        except (httpx.HTTPError, OSError, ValueError, TypeError) as error:
            cached = self._read_cache()
            error_label = self._safe_error_label(error)
            if cached is not None:
                payload["flow"] = deepcopy(cached["flow"])
                payload["trello"] = {
                    **deepcopy(cached["trello"]),
                    "status": "cached",
                    "last_error": error_label,
                }
                payload["sources"] = self._replace_source(
                    payload.get("sources"),
                    state="stale",
                    freshness=f"cached {self._display_timestamp(cached['fetched_at'])}",
                )
                return payload

            payload["trello"] = {
                "status": "unavailable",
                "last_error": error_label,
            }
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="unavailable",
                freshness="live refresh failed; sample flow shown",
            )
            return payload

    def _fetch_snapshot(self) -> dict[str, Any]:
        fetched_at = datetime.now(UTC).isoformat()
        with self._client_context() as client:
            board = self._get_json(client, f"boards/{self._board_id}", {"fields": "name,url"})
            lists = self._get_json(
                client,
                f"boards/{self._board_id}/lists",
                {"filter": "open", "fields": "name,pos"},
            )
            cards = self._get_json(
                client,
                f"boards/{self._board_id}/cards/open",
                {"fields": "name,desc,url,pos,idList,dateLastActivity"},
            )

        if not isinstance(board, dict) or not isinstance(lists, list) or not isinstance(cards, list):
            raise ValueError("Trello returned an unexpected payload shape.")

        list_names = {
            str(item.get("id")): str(item.get("name", ""))
            for item in lists
            if isinstance(item, dict) and item.get("id")
        }
        grouped: dict[str, list[dict[str, Any]]] = {}
        for card in cards:
            if not isinstance(card, dict):
                continue
            list_name = list_names.get(str(card.get("idList")), "Unknown")
            grouped.setdefault(list_name.casefold(), []).append(card)

        for group in grouped.values():
            group.sort(key=lambda card: self._position(card.get("pos")))

        now_cards = grouped.get("now", [])
        next_cards = grouped.get("next", [])[: self._next_limit]
        waiting_cards = grouped.get("waiting", [])[: self._waiting_limit]
        captured_cards = grouped.get("captured", [])

        flow = {
            "now": self._normalize_now(now_cards[0] if now_cards else None),
            "next": [self._normalize_next(card) for card in next_cards],
            "waiting": [self._normalize_waiting(card) for card in waiting_cards],
        }
        trello = {
            "status": "live",
            "board": str(board.get("name") or "Configured Trello board"),
            "board_url": str(board.get("url") or ""),
            "fetched_at": fetched_at,
            "counts": {
                "now": len(now_cards),
                "next": len(grouped.get("next", [])),
                "waiting": len(grouped.get("waiting", [])),
                "captured": len(captured_cards),
            },
        }
        return {"fetched_at": fetched_at, "flow": flow, "trello": trello}

    def _get_json(
        self,
        client: httpx.Client,
        path: str,
        extra_params: dict[str, str],
    ) -> object:
        params = {
            "key": self._api_key,
            "token": self._api_token,
            **extra_params,
        }
        response = client.get(f"{self._api_base_url}/{path}", params=params)
        response.raise_for_status()
        return response.json()

    def _client_context(self) -> httpx.Client:
        if self._client is not None:
            return _BorrowedClientContext(self._client)
        return httpx.Client(
            timeout=httpx.Timeout(8.0),
            headers={"Accept": "application/json", "User-Agent": "LifeOS-Dashboard/0.1"},
        )

    def _normalize_now(self, card: dict[str, Any] | None) -> dict[str, str]:
        if card is None:
            return {
                "title": "No active Now card",
                "lane": "Trello / Now",
                "status": "Now",
                "url": "",
            }
        return {
            "title": self._card_name(card),
            "lane": self._lane(card) or "Trello / Now",
            "status": "Now",
            "url": str(card.get("url") or ""),
        }

    def _normalize_next(self, card: dict[str, Any]) -> dict[str, str]:
        return {
            "title": self._card_name(card),
            "lane": self._lane(card) or "Trello / Next",
            "url": str(card.get("url") or ""),
        }

    def _normalize_waiting(self, card: dict[str, Any]) -> dict[str, str]:
        return {
            "title": self._card_name(card),
            "reason": self._waiting_reason(card),
            "url": str(card.get("url") or ""),
        }

    @staticmethod
    def _card_name(card: dict[str, Any]) -> str:
        return str(card.get("name") or "Untitled Trello card")

    @staticmethod
    def _lane(card: dict[str, Any]) -> str:
        for line in str(card.get("desc") or "").splitlines():
            stripped = line.strip()
            if stripped.casefold().startswith("lane:"):
                return stripped.split(":", 1)[1].strip()
        return ""

    @staticmethod
    def _waiting_reason(card: dict[str, Any]) -> str:
        lines = [line.strip() for line in str(card.get("desc") or "").splitlines()]
        for line in lines:
            if line.casefold().startswith("blocked by:"):
                reason = line.split(":", 1)[1].strip()
                return reason or "Waiting on an external condition"
        for line in lines:
            if line:
                return line
        return "Waiting on an external condition"

    @staticmethod
    def _position(value: object) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return float("inf")

    def _replace_source(
        self,
        sources: object,
        *,
        state: str,
        freshness: str,
    ) -> list[dict[str, str]]:
        normalized = (
            [dict(item) for item in sources if isinstance(item, dict)]
            if isinstance(sources, list)
            else []
        )
        trello_source = {"name": "Trello", "state": state, "freshness": freshness}
        for index, source in enumerate(normalized):
            if str(source.get("name", "")).casefold() == "trello":
                normalized[index] = trello_source
                return normalized
        return [*normalized, trello_source]

    @staticmethod
    def _freshness(snapshot: dict[str, Any]) -> str:
        counts = snapshot["trello"]["counts"]
        return (
            f"live · {counts['now']} Now · {counts['next']} Next · "
            f"{counts['waiting']} Waiting"
        )

    def _write_cache(self, snapshot: dict[str, Any]) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._cache_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        temporary.replace(self._cache_path)

    def _read_cache(self) -> dict[str, Any] | None:
        try:
            payload = json.loads(self._cache_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        if not isinstance(payload.get("flow"), dict):
            return None
        if not isinstance(payload.get("trello"), dict):
            return None
        if not isinstance(payload.get("fetched_at"), str):
            return None
        return payload

    @staticmethod
    def _safe_error_label(error: Exception) -> str:
        if isinstance(error, httpx.HTTPStatusError):
            return f"Trello returned HTTP {error.response.status_code}"
        if isinstance(error, httpx.TimeoutException):
            return "Trello request timed out"
        if isinstance(error, httpx.RequestError):
            return "Trello connection failed"
        if isinstance(error, (ValueError, TypeError)):
            return "Trello returned invalid data"
        return "Trello cache could not be updated"

    @staticmethod
    def _display_timestamp(value: str) -> str:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value
        local = parsed.astimezone()
        hour = local.strftime("%I").lstrip("0") or "0"
        return f"{local.strftime('%b')} {local.day}, {hour}:{local.strftime('%M %p')}"


class _BorrowedClientContext:
    """Use an injected test client without closing it after each snapshot."""

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def __enter__(self) -> httpx.Client:
        return self._client

    def __exit__(self, *args: object) -> None:
        return None
