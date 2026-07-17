"""Read-only Todoist commitments adapter with a local last-good cache."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx

from .base import DashboardSource

TODOIST_API_BASE_URL = "https://api.todoist.com/api/v1"
DEFAULT_TIMEZONE = "America/Chicago"


class TodoistDashboardSource:
    """Overlay the dashboard Today commitments with live Todoist tasks."""

    def __init__(
        self,
        fallback_source: DashboardSource,
        *,
        api_token: str | None,
        cache_path: Path,
        timezone_name: str = DEFAULT_TIMEZONE,
        api_base_url: str = TODOIST_API_BASE_URL,
        client: httpx.Client | None = None,
        horizon_days: int = 7,
        commitment_limit: int = 6,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._fallback_source = fallback_source
        self._api_token = (api_token or "").strip()
        self._cache_path = cache_path
        self._timezone = self._load_timezone(timezone_name)
        self._api_base_url = api_base_url.rstrip("/")
        self._client = client
        self._horizon_days = max(1, horizon_days)
        self._commitment_limit = max(1, commitment_limit)
        self._clock = clock or (lambda: datetime.now(self._timezone))

    @classmethod
    def from_environment(
        cls,
        fallback_source: DashboardSource,
        *,
        cache_path: Path,
    ) -> TodoistDashboardSource:
        """Create a Todoist source from ignored local environment settings."""
        return cls(
            fallback_source,
            api_token=os.getenv("TODOIST_API_TOKEN"),
            cache_path=cache_path,
            timezone_name=os.getenv("LIFEOS_TIMEZONE", DEFAULT_TIMEZONE),
            api_base_url=os.getenv("TODOIST_API_BASE_URL", TODOIST_API_BASE_URL),
            horizon_days=cls._env_int("TODOIST_HORIZON_DAYS", 7),
            commitment_limit=cls._env_int("TODOIST_COMMITMENT_LIMIT", 6),
        )

    @property
    def configured(self) -> bool:
        return bool(self._api_token)

    @property
    def name(self) -> str:
        if self.configured:
            return f"{self._fallback_source.name}+todoist"
        return self._fallback_source.name

    def load(self) -> dict[str, Any]:
        payload = deepcopy(self._fallback_source.load())
        now = self._local_now()
        self._set_date_label(payload, now)

        if not self.configured:
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="stale",
                freshness="live access not configured; sample commitments shown",
            )
            payload["todoist"] = {"status": "not configured", "cache": "unused"}
            return payload

        try:
            snapshot = self._fetch_snapshot(now)
            self._write_cache(snapshot)
            self._apply_snapshot(payload, snapshot)
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
                self._apply_snapshot(payload, cached)
                payload["todoist"] = {
                    **deepcopy(cached["todoist"]),
                    "status": "cached",
                    "last_error": error_label,
                }
                payload["sources"] = self._replace_source(
                    payload.get("sources"),
                    state="stale",
                    freshness=f"cached {self._display_timestamp(cached['fetched_at'])}",
                )
                return payload

            payload["todoist"] = {"status": "unavailable", "last_error": error_label}
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="unavailable",
                freshness="live refresh failed; sample commitments shown",
            )
            return payload

    def _fetch_snapshot(self, now: datetime) -> dict[str, Any]:
        tasks = self._fetch_all_tasks()
        due_tasks = []
        horizon_end = now.date() + timedelta(days=self._horizon_days)

        for task in tasks:
            normalized = self._normalize_task(task, now)
            if normalized is None:
                continue
            if normalized["due_date"] > horizon_end and not normalized["overdue"]:
                continue
            due_tasks.append(normalized)

        due_tasks.sort(key=self._task_sort_key)
        commitments = [self._commitment(task) for task in due_tasks[: self._commitment_limit]]
        counts = {
            "overdue": sum(1 for task in due_tasks if task["overdue"]),
            "today": sum(1 for task in due_tasks if task["due_date"] == now.date()),
            "upcoming": sum(1 for task in due_tasks if task["due_date"] > now.date()),
            "shown": len(commitments),
        }
        fetched_at = datetime.now(UTC).isoformat()
        return {
            "fetched_at": fetched_at,
            "date_label": self._date_label(now),
            "commitments": commitments,
            "todoist": {
                "status": "live",
                "fetched_at": fetched_at,
                "horizon_days": self._horizon_days,
                "counts": counts,
            },
        }

    def _fetch_all_tasks(self) -> list[dict[str, Any]]:
        tasks: list[dict[str, Any]] = []
        cursor: str | None = None
        pages = 0
        with self._client_context() as client:
            while True:
                params: dict[str, object] = {"limit": 200}
                if cursor:
                    params["cursor"] = cursor
                response = client.get(
                    f"{self._api_base_url}/tasks",
                    headers={"Authorization": f"Bearer {self._api_token}"},
                    params=params,
                )
                response.raise_for_status()
                body = response.json()
                if not isinstance(body, dict) or not isinstance(body.get("results"), list):
                    raise ValueError("Todoist returned an unexpected payload shape.")
                tasks.extend(item for item in body["results"] if isinstance(item, dict))
                cursor_value = body.get("next_cursor")
                cursor = str(cursor_value) if cursor_value else None
                pages += 1
                if not cursor:
                    break
                if pages >= 20:
                    raise ValueError("Todoist pagination exceeded the safety limit.")
        return tasks

    def _normalize_task(self, task: dict[str, Any], now: datetime) -> dict[str, Any] | None:
        due = task.get("due")
        if not isinstance(due, dict):
            return None
        raw_date = due.get("date")
        if not isinstance(raw_date, str) or not raw_date.strip():
            return None

        due_datetime, due_date, timed = self._parse_due(raw_date, due.get("timezone"))
        overdue = due_datetime < now if timed else due_date < now.date()
        return {
            "id": str(task.get("id") or ""),
            "title": str(task.get("content") or "Untitled Todoist task"),
            "due_datetime": due_datetime,
            "due_date": due_date,
            "timed": timed,
            "overdue": overdue,
            "priority": self._priority_label(task.get("priority")),
        }

    def _parse_due(self, value: str, timezone_value: object) -> tuple[datetime, date, bool]:
        cleaned = value.strip()
        if "T" not in cleaned:
            due_date = date.fromisoformat(cleaned[:10])
            return datetime.combine(due_date, time.max, self._timezone), due_date, False

        parsed = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            timezone_name = str(timezone_value or "").strip()
            parsed = parsed.replace(tzinfo=self._load_timezone(timezone_name, self._timezone))
        local = parsed.astimezone(self._timezone)
        return local, local.date(), True

    def _commitment(self, task: dict[str, Any]) -> dict[str, str]:
        task_id = task["id"]
        return {
            "title": task["title"],
            "state": self._state_label(task),
            "source": f"Todoist · {task['priority']}",
            "url": f"https://app.todoist.com/app/task/{task_id}" if task_id else "",
        }

    def _state_label(self, task: dict[str, Any]) -> str:
        due_date = task["due_date"]
        now = self._local_now()
        time_label = self._format_time(task["due_datetime"]) if task["timed"] else ""
        suffix = f" · {time_label}" if time_label else ""
        if task["overdue"]:
            return f"overdue · {due_date.strftime('%b')} {due_date.day}{suffix}"
        if due_date == now.date():
            return f"today{suffix}"
        if due_date == now.date() + timedelta(days=1):
            return f"tomorrow{suffix}"
        return f"{due_date.strftime('%a, %b')} {due_date.day}{suffix}"

    @staticmethod
    def _task_sort_key(task: dict[str, Any]) -> tuple[object, ...]:
        priority_rank = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}.get(task["priority"], 4)
        return (0 if task["overdue"] else 1, task["due_datetime"], priority_rank, task["title"])

    @staticmethod
    def _priority_label(value: object) -> str:
        if isinstance(value, str) and value.lower() in {"p1", "p2", "p3", "p4"}:
            return value.upper()
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            return "P4"
        return {4: "P1", 3: "P2", 2: "P3", 1: "P4"}.get(numeric, "P4")

    def _apply_snapshot(self, payload: dict[str, Any], snapshot: dict[str, Any]) -> None:
        today = payload.setdefault("today", {})
        if not isinstance(today, dict):
            today = {}
            payload["today"] = today
        today["date_label"] = snapshot["date_label"]
        today["commitments"] = deepcopy(snapshot["commitments"])
        payload["todoist"] = deepcopy(snapshot["todoist"])

    def _set_date_label(self, payload: dict[str, Any], now: datetime) -> None:
        today = payload.setdefault("today", {})
        if isinstance(today, dict):
            today["date_label"] = self._date_label(now)

    @staticmethod
    def _date_label(now: datetime) -> str:
        return f"{now.strftime('%A, %B')} {now.day}"

    @staticmethod
    def _format_time(value: datetime) -> str:
        hour = value.strftime("%I").lstrip("0") or "0"
        return f"{hour}:{value.strftime('%M %p')}"

    def _local_now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None:
            value = value.replace(tzinfo=self._timezone)
        return value.astimezone(self._timezone)

    def _client_context(self) -> httpx.Client:
        if self._client is not None:
            return _BorrowedClientContext(self._client)
        return httpx.Client(
            timeout=httpx.Timeout(8.0),
            headers={"Accept": "application/json", "User-Agent": "LifeOS-Dashboard/0.1"},
        )

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
        target = {"name": "Todoist", "state": state, "freshness": freshness}
        for index, source in enumerate(normalized):
            if str(source.get("name", "")).casefold() == "todoist":
                normalized[index] = target
                return normalized
        return [*normalized, target]

    @staticmethod
    def _freshness(snapshot: dict[str, Any]) -> str:
        counts = snapshot["todoist"]["counts"]
        return (
            f"live · {counts['today']} today · {counts['overdue']} overdue · "
            f"{counts['upcoming']} upcoming"
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
        if not isinstance(payload.get("commitments"), list):
            return None
        if not isinstance(payload.get("todoist"), dict):
            return None
        if not isinstance(payload.get("fetched_at"), str):
            return None
        if not isinstance(payload.get("date_label"), str):
            return None
        return payload

    @staticmethod
    def _safe_error_label(error: Exception) -> str:
        if isinstance(error, httpx.HTTPStatusError):
            return f"Todoist returned HTTP {error.response.status_code}"
        if isinstance(error, httpx.TimeoutException):
            return "Todoist request timed out"
        if isinstance(error, httpx.RequestError):
            return "Todoist connection failed"
        if isinstance(error, (ValueError, TypeError)):
            return "Todoist returned invalid data"
        return "Todoist cache could not be updated"

    @staticmethod
    def _display_timestamp(value: str) -> str:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value
        local = parsed.astimezone()
        hour = local.strftime("%I").lstrip("0") or "0"
        return f"{local.strftime('%b')} {local.day}, {hour}:{local.strftime('%M %p')}"

    @staticmethod
    def _load_timezone(value: str, fallback: ZoneInfo | None = None) -> ZoneInfo:
        try:
            return ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            if fallback is not None:
                return fallback
            return ZoneInfo(DEFAULT_TIMEZONE)

    @staticmethod
    def _env_int(name: str, default: int) -> int:
        try:
            return int(os.getenv(name, str(default)))
        except ValueError:
            return default


class _BorrowedClientContext:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def __enter__(self) -> httpx.Client:
        return self._client

    def __exit__(self, *args: object) -> None:
        return None
