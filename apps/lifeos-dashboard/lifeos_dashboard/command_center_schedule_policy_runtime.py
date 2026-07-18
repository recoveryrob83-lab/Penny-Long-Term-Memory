"""Production scheduler policy for overdue, failed, and resumed jobs.

This layer loads after the ledger and bounded debug recurrence wrappers. It owns
one five-minute grace rule, prevents stale catch-up execution, pauses failed
runs, and makes manual resume explicitly calculate a new future due time.
"""
from __future__ import annotations

import time

from . import command_center, command_center_debug_schedule_runtime
from .command_center_store import CommandCenterStore

OVERDUE_GRACE_SECONDS = 5 * 60
OVERDUE_STATUS = "overdue"
OVERDUE_REASON = (
    "Paused without catch-up because the scheduled time was more than five minutes overdue."
)
REARMED_STATUS = "rearmed"
REARMED_REASON = "Resumed manually; next run recalculated from the current time."


def _publish_schedule(service: command_center.CommandCenterService, schedule_id: int) -> None:
    ledger = getattr(service, "schedule_ledger", None)
    schedule = service.store.get_schedule(schedule_id)
    if ledger is not None and schedule is not None:
        ledger.record_schedule(schedule)


def pause_without_run(
    self: CommandCenterStore,
    schedule_id: int,
    *,
    status: str,
    reason: str,
) -> dict[str, object] | None:
    """Pause a definition without pretending an execution occurred."""
    with self._connect() as connection:
        cursor = connection.execute(
            """
            UPDATE scheduled_jobs SET
                enabled = 0, next_run_at = NULL, last_status = ?,
                last_reason = ?, updated_at = ?
            WHERE id = ?
            """,
            (status, reason, time.time(), schedule_id),
        )
        if cursor.rowcount == 0:
            return None
    return self.get_schedule(schedule_id)


def rearm_schedule(
    self: CommandCenterStore,
    schedule_id: int,
    next_run_at: float,
) -> dict[str, object] | None:
    """Enable a definition with an explicitly recalculated future due time."""
    with self._connect() as connection:
        cursor = connection.execute(
            """
            UPDATE scheduled_jobs SET
                enabled = 1, next_run_at = ?, last_status = ?,
                last_reason = ?, updated_at = ?
            WHERE id = ?
            """,
            (next_run_at, REARMED_STATUS, REARMED_REASON, time.time(), schedule_id),
        )
        if cursor.rowcount == 0:
            return None
    return self.get_schedule(schedule_id)


def is_overdue(schedule: dict[str, object], now: float) -> bool:
    due_at = schedule.get("next_run_at")
    if due_at is None:
        return False
    return float(due_at) + OVERDUE_GRACE_SECONDS < now


def pause_overdue_schedule(
    self: command_center.CommandCenterService,
    schedule: dict[str, object],
    now: float,
) -> bool:
    """Pause one stale definition and publish the resulting mirror state."""
    if not is_overdue(schedule, now):
        return False
    schedule_id = int(schedule["id"])
    updated = self.store.pause_without_run(
        schedule_id,
        status=OVERDUE_STATUS,
        reason=OVERDUE_REASON,
    )
    if updated is not None:
        _publish_schedule(self, schedule_id)
        return True
    return False


def scheduler_loop(self: command_center.CommandCenterService) -> None:
    """Pause stale jobs instead of replaying them after downtime."""
    while not self._scheduler_stop.wait(self._scheduler_poll_seconds):
        if self.paused or self.running:
            continue
        now = time.time()
        for schedule in self.store.due_schedules(now):
            if self._scheduler_stop.is_set():
                return
            if self.paused:
                break
            if self._pause_overdue_schedule(schedule, now):
                continue
            self._run_scheduled(schedule)


def run_scheduled(
    self: command_center.CommandCenterService,
    schedule: dict[str, object],
) -> None:
    """Run once, pause any failure, and advance only successful recurrence."""
    schedule_id = int(schedule["id"])
    prior_last_run = schedule.get("last_run_at")
    result = self.execute(self._job_from_schedule(schedule))
    if result.status == "refused" and (
        "Another automation job is running" in result.reason
        or "Automation is paused" in result.reason
    ):
        self.store.defer_schedule(schedule_id, time.time() + 60, result.reason)
        _publish_schedule(self, schedule_id)
        return

    cadence = str(schedule["cadence"])
    succeeded = result.status == "succeeded"
    enabled = succeeded and cadence != "once"
    next_run_at = None
    if enabled:
        next_run_at = command_center.compute_next_run(
            self._schedule_spec(schedule),
            after_timestamp=max(time.time(), float(schedule.get("next_run_at") or 0)),
        )
    self.store.complete_schedule(
        schedule_id,
        enabled=enabled,
        next_run_at=next_run_at,
        result=result.to_dict(),
    )

    if (
        succeeded
        and cadence == command_center_debug_schedule_runtime.DEBUG_CADENCE
        and prior_last_run is not None
    ):
        updated = self.store.get_schedule(schedule_id)
        if updated is not None:
            reason = str(updated.get("last_reason") or "").strip()
            marker = command_center_debug_schedule_runtime.DEBUG_COMPLETION_MARKER
            if marker not in reason:
                reason = f"{reason} {marker}".strip()
            self.store.complete_schedule(
                schedule_id,
                enabled=False,
                next_run_at=None,
                result={
                    "finished_at": updated["last_run_at"],
                    "status": updated["last_status"],
                    "reason": reason,
                },
            )
    _publish_schedule(self, schedule_id)


def set_schedule_enabled(
    self: command_center.CommandCenterService,
    schedule_id: int,
    enabled: bool,
) -> dict[str, object] | None:
    """Pause directly or resume by calculating a new future due time."""
    schedule = self.store.get_schedule(schedule_id)
    if schedule is None:
        return None
    if (
        enabled
        and str(schedule.get("cadence") or "")
        == command_center_debug_schedule_runtime.DEBUG_CADENCE
        and command_center_debug_schedule_runtime.DEBUG_COMPLETION_MARKER
        in str(schedule.get("last_reason") or "")
    ):
        raise ValueError(
            "This five-minute recurrence test already completed two attempts. "
            "Create a new test schedule."
        )
    if not enabled:
        updated = self.store.set_schedule_enabled(schedule_id, False, None)
        _publish_schedule(self, schedule_id)
        return updated

    next_run_at = command_center.compute_next_run(self._schedule_spec(schedule))
    if next_run_at is None:
        raise ValueError(
            "This one-time schedule is already in the past. Edit it to a future time before resuming."
        )
    updated = self.store.rearm_schedule(schedule_id, next_run_at)
    _publish_schedule(self, schedule_id)
    return updated


CommandCenterStore.pause_without_run = pause_without_run
CommandCenterStore.rearm_schedule = rearm_schedule
command_center.CommandCenterService._pause_overdue_schedule = pause_overdue_schedule
command_center.CommandCenterService._scheduler_loop = scheduler_loop
command_center.CommandCenterService._run_scheduled = run_scheduled
command_center.CommandCenterService.set_schedule_enabled = set_schedule_enabled
