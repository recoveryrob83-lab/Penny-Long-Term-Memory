"""Authoritative detailed logging policy for Automation Command Center runs.

Execution history remains the single durable record. This runtime adds stable run
identifiers, manual-versus-scheduled context, safe prompt fingerprints, and a larger
inspection window without logging prompt contents, environment variables, or secrets.
"""
from __future__ import annotations

import hashlib
import json
import threading
import uuid
from dataclasses import replace
from typing import Any

from . import command_center
from .command_center_store import CommandCenterStore

AUTOMATION_LOG_HISTORY_LIMIT = 250
_CONTEXT_PREFIX = "LIFEOS_RUN_CONTEXT="
_CONTEXT = threading.local()
_STORE_HISTORY_FLAG = "_lifeos_automation_log_history_installed"
_SERVICE_LOGGING_FLAG = "_lifeos_automation_logging_installed"


def _prompt_fingerprint(job: command_center.CommandJob) -> dict[str, object]:
    """Describe prompt identity without storing the prompt body in diagnostic metadata."""
    if job.prompt_type != "custom":
        return {"prompt_length": None, "prompt_sha256": None}
    encoded = job.custom_prompt.encode("utf-8")
    return {
        "prompt_length": len(job.custom_prompt),
        "prompt_sha256": hashlib.sha256(encoded).hexdigest()[:16],
    }


def _new_context(
    job: command_center.CommandJob,
    *,
    trigger: str,
    timeout_seconds: int,
    schedule: dict[str, object] | None = None,
) -> dict[str, object]:
    context: dict[str, object] = {
        "run_id": str(uuid.uuid4()),
        "trigger": trigger,
        "destination": job.destination,
        "mode": job.mode,
        "prompt_type": job.prompt_type,
        "timeout_seconds": timeout_seconds,
        **_prompt_fingerprint(job),
    }
    if schedule is not None:
        context.update(
            {
                "schedule_id": schedule.get("id"),
                "schedule_name": schedule.get("name"),
                "cadence": schedule.get("cadence"),
            }
        )
    return context


def current_context() -> dict[str, object] | None:
    value = getattr(_CONTEXT, "value", None)
    return dict(value) if isinstance(value, dict) else None


def _context_line(result: command_center.ExecutionResult) -> str:
    context = current_context() or {
        "run_id": str(uuid.uuid4()),
        "trigger": "unknown",
        "destination": result.destination,
        "mode": result.mode,
        "prompt_type": result.prompt_type,
    }
    context.update(
        {
            "status": result.status,
            "exit_code": result.exit_code,
            "started_at": result.started_at,
            "finished_at": result.finished_at,
            "duration_seconds": round(max(0.0, result.finished_at - result.started_at), 3),
        }
    )
    return _CONTEXT_PREFIX + json.dumps(context, sort_keys=True, separators=(",", ":"))


def _annotate_result(result: command_center.ExecutionResult) -> command_center.ExecutionResult:
    line = _context_line(result)
    stdout = f"{line}\n{result.stdout}" if result.stdout else line
    return replace(result, stdout=stdout)


def _history_with_ids(self: CommandCenterStore, limit: int = 25) -> list[dict[str, object]]:
    """Return existing execution-history rows with their stable local record IDs."""
    with self._connect() as connection:  # noqa: SLF001 - same-package persistence extension
        rows = connection.execute(
            """
            SELECT id, status, destination, mode, prompt_type, exit_code,
                   started_at, finished_at, stdout, stderr, reason
            FROM execution_history ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def install_store_history() -> bool:
    if getattr(CommandCenterStore, _STORE_HISTORY_FLAG, False):
        return False
    CommandCenterStore.history = _history_with_ids
    setattr(CommandCenterStore, _STORE_HISTORY_FLAG, True)
    return True


def install_service_logging() -> bool:
    if getattr(command_center.CommandCenterService, _SERVICE_LOGGING_FLAG, False):
        return False

    original_execute = command_center.CommandCenterService.execute
    original_run_scheduled = command_center.CommandCenterService._run_scheduled

    def history(self: command_center.CommandCenterService) -> list[dict[str, object]]:
        limit = max(int(self.history_limit), AUTOMATION_LOG_HISTORY_LIMIT)
        return self.store.history(limit)

    def record(
        self: command_center.CommandCenterService,
        result: command_center.ExecutionResult,
    ) -> command_center.ExecutionResult:
        annotated = _annotate_result(result)
        self.store.add_history(annotated.to_dict())
        return annotated

    def execute(
        self: command_center.CommandCenterService,
        job: command_center.CommandJob,
        timeout_seconds: int = 120,
    ) -> command_center.ExecutionResult:
        previous = getattr(_CONTEXT, "value", None)
        owns_context = previous is None
        if owns_context:
            _CONTEXT.value = _new_context(
                job,
                trigger="manual",
                timeout_seconds=timeout_seconds,
            )
        try:
            return original_execute(self, job, timeout_seconds=timeout_seconds)
        finally:
            if owns_context:
                try:
                    delattr(_CONTEXT, "value")
                except AttributeError:
                    pass

    def run_scheduled(
        self: command_center.CommandCenterService,
        schedule: dict[str, object],
    ) -> None:
        previous = getattr(_CONTEXT, "value", None)
        job = self._job_from_schedule(schedule)
        _CONTEXT.value = _new_context(
            job,
            trigger="scheduled",
            timeout_seconds=120,
            schedule=schedule,
        )
        try:
            original_run_scheduled(self, schedule)
        finally:
            if previous is None:
                try:
                    delattr(_CONTEXT, "value")
                except AttributeError:
                    pass
            else:
                _CONTEXT.value = previous

    command_center.CommandCenterService.history = history
    command_center.CommandCenterService._record = record
    command_center.CommandCenterService.execute = execute
    command_center.CommandCenterService._run_scheduled = run_scheduled
    setattr(command_center.CommandCenterService, _SERVICE_LOGGING_FLAG, True)
    return True


install_store_history()
install_service_logging()
