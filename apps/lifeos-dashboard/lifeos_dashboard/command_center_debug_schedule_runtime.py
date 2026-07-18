"""Bounded five-minute recurrence testing for the Automation Command Center.

This runtime policy adds one intentionally narrow cadence for scheduler validation:
``debug_5m``. It is draft-only, runs at most twice, and then disables itself.
The existing once, daily, and weekly scheduling behavior remains unchanged.
"""
from __future__ import annotations

from datetime import datetime

from . import command_center, command_center_schedule

DEBUG_CADENCE = "debug_5m"
DEBUG_INTERVAL_SECONDS = 5 * 60
DEBUG_COMPLETION_MARKER = "Debug recurrence test completed after two attempts."

_original_compute_next_run = command_center_schedule.compute_next_run
_original_prepare_schedule = command_center.CommandCenterService._prepare_schedule
_original_run_scheduled = command_center.CommandCenterService._run_scheduled
_original_set_schedule_enabled = command_center.CommandCenterService.set_schedule_enabled

command_center_schedule.VALID_CADENCES.add(DEBUG_CADENCE)


def compute_next_run(
    spec: command_center_schedule.ScheduleSpec,
    *,
    after_timestamp: float | None = None,
) -> float | None:
    """Return the next five-minute boundary for the bounded debug cadence."""
    if spec.cadence != DEBUG_CADENCE:
        return _original_compute_next_run(spec, after_timestamp=after_timestamp)

    start_date, run_time, timezone = command_center_schedule.validate_schedule_spec(spec)
    after = (
        datetime.fromtimestamp(after_timestamp, timezone)
        if after_timestamp is not None
        else datetime.now(timezone)
    )
    first_run = datetime.combine(start_date, run_time, timezone)
    if first_run > after:
        return first_run.timestamp()

    elapsed_seconds = after.timestamp() - first_run.timestamp()
    intervals_elapsed = int(elapsed_seconds // DEBUG_INTERVAL_SECONDS) + 1
    return first_run.timestamp() + intervals_elapsed * DEBUG_INTERVAL_SECONDS


def prepare_schedule(
    self: command_center.CommandCenterService,
    values: dict[str, object],
) -> dict[str, object]:
    """Require the five-minute recurrence test to remain draft-only."""
    if str(values.get("cadence") or "") == DEBUG_CADENCE:
        if str(values.get("mode") or "draft") != "draft" or bool(values.get("confirm_send")):
            raise ValueError("Five-minute recurrence tests are draft-only and cannot send live.")
    return _original_prepare_schedule(self, values)


def run_scheduled(
    self: command_center.CommandCenterService,
    schedule: dict[str, object],
) -> None:
    """Run normally, then stop the debug cadence after its second completed attempt."""
    if str(schedule.get("cadence") or "") != DEBUG_CADENCE:
        _original_run_scheduled(self, schedule)
        return

    prior_last_run = schedule.get("last_run_at")
    _original_run_scheduled(self, schedule)

    if prior_last_run is None:
        return

    updated = self.store.get_schedule(int(schedule["id"]))
    if updated is None or updated.get("last_run_at") == prior_last_run:
        return

    reason = str(updated.get("last_reason") or "").strip()
    if DEBUG_COMPLETION_MARKER not in reason:
        reason = f"{reason} {DEBUG_COMPLETION_MARKER}".strip()
    self.store.complete_schedule(
        int(schedule["id"]),
        enabled=False,
        next_run_at=None,
        result={
            "finished_at": updated["last_run_at"],
            "status": updated["last_status"],
            "reason": reason,
        },
    )
    ledger = getattr(self, "schedule_ledger", None)
    if ledger is not None and updated.get("next_run_at") is not None:
        ledger.record_state(updated, "canceled", reason)


def set_schedule_enabled(
    self: command_center.CommandCenterService,
    schedule_id: int,
    enabled: bool,
) -> dict[str, object] | None:
    """Do not allow a completed two-attempt debug test to be resumed."""
    schedule = self.store.get_schedule(schedule_id)
    if (
        enabled
        and schedule is not None
        and str(schedule.get("cadence") or "") == DEBUG_CADENCE
        and DEBUG_COMPLETION_MARKER in str(schedule.get("last_reason") or "")
    ):
        raise ValueError(
            "This five-minute recurrence test already completed two attempts. "
            "Create a new test schedule."
        )
    return _original_set_schedule_enabled(self, schedule_id, enabled)


command_center_schedule.compute_next_run = compute_next_run
command_center.compute_next_run = compute_next_run
command_center.CommandCenterService._prepare_schedule = prepare_schedule
command_center.CommandCenterService._run_scheduled = run_scheduled
command_center.CommandCenterService.set_schedule_enabled = set_schedule_enabled
