"""Read-only Google Calendar iCal adapter with recurrence expansion and local cache."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx
from dateutil.rrule import rrulestr

from .base import DashboardSource

DEFAULT_TIMEZONE = "America/Chicago"


@dataclass(frozen=True)
class _CalendarEvent:
    uid: str
    title: str
    location: str
    start: datetime
    end: datetime
    all_day: bool
    rrule: str
    exdates: tuple[datetime, ...]
    rdates: tuple[datetime, ...]
    recurrence_id: datetime | None
    cancelled: bool


class GoogleCalendarIcalDashboardSource:
    """Overlay the dashboard next event with a private Google Calendar iCal feed."""

    def __init__(
        self,
        fallback_source: DashboardSource,
        *,
        ical_url: str | None,
        cache_path: Path,
        timezone_name: str = DEFAULT_TIMEZONE,
        client: httpx.Client | None = None,
        horizon_days: int = 14,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._fallback_source = fallback_source
        self._ical_url = (ical_url or "").strip()
        self._cache_path = cache_path
        self._timezone = self._load_timezone(timezone_name)
        self._client = client
        self._horizon_days = max(1, horizon_days)
        self._clock = clock or (lambda: datetime.now(self._timezone))

    @classmethod
    def from_environment(
        cls,
        fallback_source: DashboardSource,
        *,
        cache_path: Path,
    ) -> GoogleCalendarIcalDashboardSource:
        """Create a Calendar source from ignored local environment settings."""
        return cls(
            fallback_source,
            ical_url=os.getenv("GOOGLE_CALENDAR_ICAL_URL"),
            cache_path=cache_path,
            timezone_name=os.getenv("LIFEOS_TIMEZONE", DEFAULT_TIMEZONE),
            horizon_days=cls._env_int("CALENDAR_HORIZON_DAYS", 14),
        )

    @property
    def configured(self) -> bool:
        return bool(self._ical_url)

    @property
    def name(self) -> str:
        if self.configured:
            return f"{self._fallback_source.name}+calendar"
        return self._fallback_source.name

    def load(self) -> dict[str, Any]:
        payload = deepcopy(self._fallback_source.load())
        now = self._local_now()
        self._set_date_label(payload, now)

        if not self.configured:
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="stale",
                freshness="live access not configured; sample event shown",
            )
            payload["calendar"] = {"status": "not configured", "cache": "unused"}
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
                payload["calendar"] = {
                    **deepcopy(cached["calendar"]),
                    "status": "cached",
                    "last_error": error_label,
                }
                payload["sources"] = self._replace_source(
                    payload.get("sources"),
                    state="stale",
                    freshness=f"cached {self._display_timestamp(cached['fetched_at'])}",
                )
                return payload

            payload["calendar"] = {"status": "unavailable", "last_error": error_label}
            payload["sources"] = self._replace_source(
                payload.get("sources"),
                state="unavailable",
                freshness="live refresh failed; sample event shown",
            )
            return payload

    def _fetch_snapshot(self, now: datetime) -> dict[str, Any]:
        with self._client_context() as client:
            response = client.get(self._ical_url)
            response.raise_for_status()
            body = response.text

        if "BEGIN:VCALENDAR" not in body:
            raise ValueError("Calendar feed did not contain a VCALENDAR payload.")

        end = now + timedelta(days=self._horizon_days)
        events = self._expand_events(body, now, end)
        next_event = self._normalize_next_event(events[0], now) if events else self._empty_event()
        fetched_at = datetime.now(UTC).isoformat()
        return {
            "fetched_at": fetched_at,
            "date_label": self._date_label(now),
            "next_event": next_event,
            "calendar": {
                "status": "live",
                "fetched_at": fetched_at,
                "horizon_days": self._horizon_days,
                "event_count": len(events),
                "next_start": events[0].start.isoformat() if events else None,
            },
        }

    def _expand_events(
        self,
        ics_text: str,
        window_start: datetime,
        window_end: datetime,
    ) -> list[_CalendarEvent]:
        parsed = [self._parse_event(block) for block in self._event_blocks(ics_text)]
        events = [event for event in parsed if event is not None]
        overrides = {
            (event.uid, self._occurrence_key(event.recurrence_id)): event
            for event in events
            if event.recurrence_id is not None
        }
        output: dict[tuple[str, str], _CalendarEvent] = {}

        for event in events:
            if event.recurrence_id is not None or event.cancelled:
                continue
            duration = event.end - event.start
            occurrences = self._event_occurrences(event, window_start, window_end)
            for occurrence_start in occurrences:
                key = (event.uid, self._occurrence_key(occurrence_start))
                if key in overrides:
                    continue
                occurrence = _CalendarEvent(
                    uid=event.uid,
                    title=event.title,
                    location=event.location,
                    start=occurrence_start,
                    end=occurrence_start + duration,
                    all_day=event.all_day,
                    rrule="",
                    exdates=(),
                    rdates=(),
                    recurrence_id=None,
                    cancelled=False,
                )
                if self._intersects(occurrence, window_start, window_end):
                    output[key] = occurrence

        for key, event in overrides.items():
            if event.cancelled:
                output.pop(key, None)
                continue
            if self._intersects(event, window_start, window_end):
                output[key] = event

        return sorted(output.values(), key=lambda event: (event.start, event.end, event.title))

    def _event_occurrences(
        self,
        event: _CalendarEvent,
        window_start: datetime,
        window_end: datetime,
    ) -> list[datetime]:
        duration = event.end - event.start
        generation_start = window_start - max(duration, timedelta(days=2))
        candidates: set[datetime] = set()

        if event.rrule:
            try:
                rule = rrulestr(event.rrule, dtstart=event.start)
                candidates.update(rule.between(generation_start, window_end, inc=True))
            except (TypeError, ValueError, OverflowError):
                candidates.add(event.start)
        else:
            candidates.add(event.start)

        candidates.update(event.rdates)
        excluded = {self._occurrence_key(value) for value in event.exdates}
        return sorted(
            value.astimezone(self._timezone)
            for value in candidates
            if self._occurrence_key(value) not in excluded
        )

    def _parse_event(self, block: list[str]) -> _CalendarEvent | None:
        properties: dict[str, list[tuple[dict[str, str], str]]] = {}
        for line in block:
            name, params, value = self._parse_property(line)
            if name:
                properties.setdefault(name, []).append((params, value))

        start_entry = self._first(properties, "DTSTART")
        if start_entry is None:
            return None
        start, all_day = self._parse_datetime(*start_entry)

        end_entry = self._first(properties, "DTEND")
        if end_entry is not None:
            end, _ = self._parse_datetime(*end_entry)
        else:
            end = start + (timedelta(days=1) if all_day else timedelta(hours=1))

        uid = self._text_value(properties, "UID") or f"event-{start.isoformat()}"
        recurrence_entry = self._first(properties, "RECURRENCE-ID")
        recurrence_id = self._parse_datetime(*recurrence_entry)[0] if recurrence_entry else None
        exdates = self._multi_datetimes(properties.get("EXDATE", []))
        rdates = self._multi_datetimes(properties.get("RDATE", []))
        status = self._text_value(properties, "STATUS").casefold()
        return _CalendarEvent(
            uid=uid,
            title=self._unescape(self._text_value(properties, "SUMMARY") or "Untitled event"),
            location=self._unescape(self._text_value(properties, "LOCATION")),
            start=start,
            end=end,
            all_day=all_day,
            rrule=self._text_value(properties, "RRULE"),
            exdates=tuple(exdates),
            rdates=tuple(rdates),
            recurrence_id=recurrence_id,
            cancelled=status == "cancelled",
        )

    def _multi_datetimes(
        self,
        entries: list[tuple[dict[str, str], str]],
    ) -> list[datetime]:
        values: list[datetime] = []
        for params, raw in entries:
            for item in raw.split(","):
                parsed, _ = self._parse_datetime(params, item)
                values.append(parsed)
        return values

    def _parse_datetime(self, params: dict[str, str], value: str) -> tuple[datetime, bool]:
        cleaned = value.strip()
        is_date = params.get("VALUE", "").upper() == "DATE" or "T" not in cleaned
        timezone_name = params.get("TZID", "")
        timezone = self._load_timezone(timezone_name, self._timezone)

        if is_date:
            parsed_date = datetime.strptime(cleaned[:8], "%Y%m%d").date()
            return datetime.combine(parsed_date, time.min, self._timezone), True

        utc_value = cleaned.endswith("Z")
        raw = cleaned[:-1] if utc_value else cleaned
        pattern = "%Y%m%dT%H%M%S" if len(raw) >= 15 else "%Y%m%dT%H%M"
        parsed = datetime.strptime(raw, pattern)
        parsed = parsed.replace(tzinfo=UTC if utc_value else timezone)
        return parsed.astimezone(self._timezone), False

    @staticmethod
    def _event_blocks(ics_text: str) -> list[list[str]]:
        unfolded: list[str] = []
        for raw_line in ics_text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
            if raw_line.startswith((" ", "\t")) and unfolded:
                unfolded[-1] += raw_line[1:]
            else:
                unfolded.append(raw_line)

        blocks: list[list[str]] = []
        current: list[str] | None = None
        for line in unfolded:
            if line == "BEGIN:VEVENT":
                current = []
            elif line == "END:VEVENT" and current is not None:
                blocks.append(current)
                current = None
            elif current is not None:
                current.append(line)
        return blocks

    @staticmethod
    def _parse_property(line: str) -> tuple[str, dict[str, str], str]:
        if ":" not in line:
            return "", {}, ""
        left, value = line.split(":", 1)
        pieces = left.split(";")
        name = pieces[0].upper()
        params: dict[str, str] = {}
        for piece in pieces[1:]:
            if "=" in piece:
                key, parameter_value = piece.split("=", 1)
                params[key.upper()] = parameter_value.strip('"')
        return name, params, value

    @staticmethod
    def _first(
        properties: dict[str, list[tuple[dict[str, str], str]]],
        name: str,
    ) -> tuple[dict[str, str], str] | None:
        entries = properties.get(name, [])
        return entries[0] if entries else None

    @staticmethod
    def _text_value(
        properties: dict[str, list[tuple[dict[str, str], str]]],
        name: str,
    ) -> str:
        entry = GoogleCalendarIcalDashboardSource._first(properties, name)
        return entry[1].strip() if entry else ""

    def _normalize_next_event(self, event: _CalendarEvent, now: datetime) -> dict[str, str]:
        if event.all_day:
            time_label = "All day"
        elif event.start <= now < event.end:
            time_label = f"Now · until {self._format_time(event.end)}"
        elif event.start.date() == now.date():
            time_label = self._format_time(event.start)
        elif event.start.date() == now.date() + timedelta(days=1):
            time_label = f"Tomorrow · {self._format_time(event.start)}"
        elif event.start.date() <= now.date() + timedelta(days=6):
            time_label = f"{event.start.strftime('%A')} · {self._format_time(event.start)}"
        else:
            time_label = (
                f"{event.start.strftime('%b')} {event.start.day} · "
                f"{self._format_time(event.start)}"
            )
        return {
            "time": time_label,
            "title": event.title,
            "location": event.location,
        }

    def _empty_event(self) -> dict[str, str]:
        return {
            "time": f"Next {self._horizon_days} days",
            "title": "No upcoming calendar events",
            "location": "Calendar horizon is clear",
        }

    @staticmethod
    def _intersects(
        event: _CalendarEvent,
        window_start: datetime,
        window_end: datetime,
    ) -> bool:
        return event.end > window_start and event.start <= window_end

    def _apply_snapshot(self, payload: dict[str, Any], snapshot: dict[str, Any]) -> None:
        today = payload.setdefault("today", {})
        if not isinstance(today, dict):
            today = {}
            payload["today"] = today
        today["date_label"] = snapshot["date_label"]
        today["next_event"] = deepcopy(snapshot["next_event"])
        payload["calendar"] = deepcopy(snapshot["calendar"])

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
            headers={"Accept": "text/calendar", "User-Agent": "LifeOS-Dashboard/0.1"},
            follow_redirects=True,
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
        target = {"name": "Calendar", "state": state, "freshness": freshness}
        for index, source in enumerate(normalized):
            if str(source.get("name", "")).casefold() == "calendar":
                normalized[index] = target
                return normalized
        return [*normalized, target]

    @staticmethod
    def _freshness(snapshot: dict[str, Any]) -> str:
        calendar = snapshot["calendar"]
        next_event = snapshot["next_event"]
        return f"live · {calendar['event_count']} upcoming · next {next_event['time']}"

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
        if not isinstance(payload.get("next_event"), dict):
            return None
        if not isinstance(payload.get("calendar"), dict):
            return None
        if not isinstance(payload.get("fetched_at"), str):
            return None
        if not isinstance(payload.get("date_label"), str):
            return None
        return payload

    @staticmethod
    def _safe_error_label(error: Exception) -> str:
        if isinstance(error, httpx.HTTPStatusError):
            return f"Calendar feed returned HTTP {error.response.status_code}"
        if isinstance(error, httpx.TimeoutException):
            return "Calendar feed request timed out"
        if isinstance(error, httpx.RequestError):
            return "Calendar feed connection failed"
        if isinstance(error, (ValueError, TypeError)):
            return "Calendar feed returned invalid data"
        return "Calendar cache could not be updated"

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
    def _occurrence_key(value: datetime | None) -> str:
        if value is None:
            return ""
        return value.astimezone(UTC).isoformat()

    @staticmethod
    def _unescape(value: str) -> str:
        return (
            value.replace("\\n", " ")
            .replace("\\N", " ")
            .replace("\\,", ",")
            .replace("\\;", ";")
            .replace("\\\\", "\\")
        )

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
