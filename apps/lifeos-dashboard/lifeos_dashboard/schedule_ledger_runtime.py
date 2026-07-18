"""Attach the Google Sheets schedule mirror to the Command Center."""
from __future__ import annotations

from typing import Any

from . import command_center
from .schedule_ledger import (
    DisabledScheduleLedger,
    ScheduleLedger,
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


def initialize(
    self: command_center.CommandCenterService,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Initialize the local engine first, then attach and compact its mirror."""
    _original_init(self, *args, **kwargs)
    self.schedule_ledger = schedule_ledger_from_environment()
    self.schedule_ledger.compact()
    for schedule in self.schedules():
        if not self.schedule_ledger.record_schedule(schedule):
            break


def create_schedule(
    self: command_center.CommandCenterService,
    values: dict[str, object],
) -> dict[str, object]:
    created = _original_create_schedule(self, values)
    _ledger(self).record_schedule(created)
    return created


def update_schedule(
    self: command_center.CommandCenterService,
    schedule_id: int,
    values: dict[str, object],
) -> dict[str, object] | None:
    updated = _original_update_schedule(self, schedule_id, values)
    if updated is not None:
        _ledger(self).record_schedule(updated)
    return updated


def set_schedule_enabled(
    self: command_center.CommandCenterService,
    schedule_id: int,
    enabled: bool,
) -> dict[str, object] | None:
    updated = _original_set_schedule_enabled(self, schedule_id, enabled)
    if updated is not None:
        _ledger(self).record_schedule(updated)
    return updated


def delete_schedule(
    self: command_center.CommandCenterService,
    schedule_id: int,
) -> bool:
    """Clear a configured mirror row before deleting its local definition.

    Schedule execution remains independent from the Sheet, but an explicit delete
    should not knowingly leave a stale cloud row. When the mirror is configured and
    cannot confirm removal, preserve the local definition so the action can be retried.
    """
    ledger = _ledger(self)
    ledger_status = ledger.status()
    if bool(ledger_status.get("configured")) and not ledger.remove_schedule(schedule_id):
        return False
    return _original_delete_schedule(self, schedule_id)


def run_scheduled(
    self: command_center.CommandCenterService,
    schedule: dict[str, object],
) -> None:
    """Publish the current schedule row after the local scheduler updates it."""
    _original_run_scheduled(self, schedule)
    updated = self.store.get_schedule(int(schedule["id"]))
    if updated is not None:
        _ledger(self).record_schedule(updated)


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
