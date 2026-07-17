"""Schedule calculations for persistent Command Center jobs."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

VALID_CADENCES = {"once", "daily", "weekly"}
DEFAULT_TIMEZONE = "America/Chicago"


@dataclass(frozen=True)
class ScheduleSpec:
    cadence: str
    schedule_date: str
    schedule_time: str
    weekdays: tuple[int, ...] = ()
    timezone: str = DEFAULT_TIMEZONE


def validate_schedule_spec(spec: ScheduleSpec) -> tuple[date, time, ZoneInfo]:
    if spec.cadence not in VALID_CADENCES:
        raise ValueError("Schedule cadence must be once, daily, or weekly.")
    try:
        start_date = date.fromisoformat(spec.schedule_date)
    except ValueError as exc:
        raise ValueError("Schedule date must use YYYY-MM-DD.") from exc
    try:
        run_time = time.fromisoformat(spec.schedule_time)
    except ValueError as exc:
        raise ValueError("Schedule time must use HH:MM.") from exc
    try:
        timezone = ZoneInfo(spec.timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError("Schedule timezone is not recognized.") from exc
    if spec.cadence == "weekly":
        if not spec.weekdays:
            raise ValueError("Weekly schedules require at least one weekday.")
        if any(day < 0 or day > 6 for day in spec.weekdays):
            raise ValueError("Weekdays must use Monday=0 through Sunday=6.")
    return start_date, run_time, timezone


def compute_next_run(spec: ScheduleSpec, *, after_timestamp: float | None = None) -> float | None:
    """Return the next UTC timestamp strictly after ``after_timestamp``.

    ``schedule_date`` acts as the one-time date or the earliest date for a recurring schedule.
    Local wall-clock time is interpreted in the schedule timezone so DST changes remain natural.
    """
    start_date, run_time, timezone = validate_schedule_spec(spec)
    after = (
        datetime.fromtimestamp(after_timestamp, timezone)
        if after_timestamp is not None
        else datetime.now(timezone)
    )

    if spec.cadence == "once":
        candidate = datetime.combine(start_date, run_time, timezone)
        return candidate.timestamp() if candidate > after else None

    candidate_date = max(start_date, after.date())
    if spec.cadence == "daily":
        candidate = datetime.combine(candidate_date, run_time, timezone)
        if candidate <= after:
            candidate = datetime.combine(candidate_date + timedelta(days=1), run_time, timezone)
        return candidate.timestamp()

    weekdays = set(spec.weekdays)
    for offset in range(15):
        day = candidate_date + timedelta(days=offset)
        if day < start_date or day.weekday() not in weekdays:
            continue
        candidate = datetime.combine(day, run_time, timezone)
        if candidate > after:
            return candidate.timestamp()
    raise ValueError("Could not calculate the next weekly run.")


def weekdays_to_storage(weekdays: tuple[int, ...] | list[int]) -> str:
    return ",".join(str(day) for day in sorted(set(weekdays)))


def weekdays_from_storage(value: str | None) -> tuple[int, ...]:
    if not value:
        return ()
    return tuple(int(item) for item in value.split(",") if item != "")
