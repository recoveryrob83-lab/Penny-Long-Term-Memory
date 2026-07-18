"""Attach the Google Sheets occurrence ledger to the Command Center."""
from __future__ import annotations

from typing import Any

from . import command_center
from .schedule_ledger import (
    DisabledScheduleLedger,
    ScheduleLedger,
    occurrence_key,
    schedule_ledger_from_environment,
)

_original_init = command_center.CommandCenterService.__init__
_original_create_schedule = command_center.CommandCenterService.create_schedule
_original_update_schedule = command_center.CommandCenterService.update_schedule
_original_set_schedule_enabled = command_center.CommandCenterService.set_schedule_enabled
_original_delete_schedule = command_center.CommandCenterService.delete_schedule
_original_run_scheduled = command_center.CommandCenterService._run_scheduled
_original_status = command_center.CommandCenterService.status


def _ledger(service: command_center.CommandCenterService) -> ScheduleLedger:
    ledger = getattr(service, "schedule_ledger", None)
    return ledger if ledger is not None else DisabledScheduleLedger()


def _due_key(schedule: dict[str, object] | None) -> str | None:
    if schedule is None or schedule.get("next_run_at") is None:
        return None
    return occurrence_key(schedule["id"], float(schedule["next_run_at"]))


def initialize(
    self: command_center.CommandCenterService,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Initialize the local engine first, then attach its best-effort mirror."""
    _original_init(self, *args, **kwargs)
    self.schedule_ledger = schedule_ledger_from_environment()
    for schedule in self.schedules():
        if bool(schedule.get("enabled")) and schedule.get("next_run_at") is not None:
            self.schedule_ledger.record_planned(schedule)


def create_schedule(
    self: command_center.CommandCenterService,
    values: dict[str, object],
) -> dict[str, object]:
    created = _original_create_schedule(self, values)
    _ledger(self).record_planned(created)
    return created


def update_schedule(
    self: command_center.CommandCenterService,
    schedule_id: int,
    values: dict[str, object],
) -> dict[str, object] | None:
    previous = self.store.get_schedule(schedule_id)
    updated = _original_update_schedule(self, schedule_id, values)
    if updated is None:
        return None
    if _due_key(previous) is not None and _due_key(previous) != _due_key(updated):
        _ledger(self).record_state(
            previous or {},
            "canceled",
            "Schedule changed before this occurrence ran.",
        )
    _ledger(self).record_planned(updated)
    return updated


def set_schedule_enabled(
    self: command_center.CommandCenterService,
    schedule_id: int,
    enabled: bool,
) -> dict[str, object] | None:
    previous = self.store.get_schedule(schedule_id)
    updated = _original_set_schedule_enabled(self, schedule_id, enabled)
    if updated is None:
        return None
    if not enabled and previous is not None:
        _ledger(self).record_state(
            previous,
            "canceled",
            "Schedule paused before this occurrence ran.",
        )
    elif enabled:
        _ledger(self).record_planned(updated)
    return updated


def delete_schedule(
    self: command_center.CommandCenterService,
    schedule_id: int,
) -> bool:
    previous = self.store.get_schedule(schedule_id)
    deleted = _original_delete_schedule(self, schedule_id)
    if deleted and previous is not None:
        _ledger(self).record_state(
            previous,
            "canceled",
            "Schedule deleted before this occurrence ran.",
        )
    return deleted


def run_scheduled(
    self: command_center.CommandCenterService,
    schedule: dict[str, object],
) -> None:
    """Mirror the exact due occurrence after the local scheduler decides its result."""
    due_at = schedule.get("next_run_at")
    prior_last_run = schedule.get("last_run_at")
    _original_run_scheduled(self, schedule)
    updated = self.store.get_schedule(int(schedule["id"]))
    if updated is None or due_at is None:
        return

    if updated.get("last_run_at") == prior_last_run:
        if str(updated.get("last_status") or "") == "deferred":
            _ledger(self).record_state(
                schedule,
                "deferred",
                str(updated.get("last_reason") or ""),
            )
            _ledger(self).record_planned(updated)
        return

    latest = self.store.history(1)
    if latest:
        _ledger(self).record_result(schedule, float(due_at), latest[0])
    _ledger(self).record_planned(updated)


def status(self: command_center.CommandCenterService) -> dict[str, object]:
    current = _original_status(self)
    current["schedule_ledger"] = _ledger(self).status()
    return current


command_center.CommandCenterService.__init__ = initialize
command_center.CommandCenterService.create_schedule = create_schedule
command_center.CommandCenterService.update_schedule = update_schedule
command_center.CommandCenterService.set_schedule_enabled = set_schedule_enabled
command_center.CommandCenterService.delete_schedule = delete_schedule
command_center.CommandCenterService._run_scheduled = run_scheduled
command_center.CommandCenterService.status = status
