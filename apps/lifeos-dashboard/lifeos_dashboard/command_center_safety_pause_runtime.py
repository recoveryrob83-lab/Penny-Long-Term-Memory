"""Install the persisted shared pause and automatic Worker transport trip points."""
from __future__ import annotations

import time
from pathlib import Path

from . import command_center, worker_operations
from .command_center_safety_pause import (
    DEFAULT_RECOVERY_CONDITION,
    CommandCenterSafetyPauseStore,
    safety_pause_reason_for_transport,
)
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_command_center_safety_pause_runtime_installed"
_COMMAND_CENTER_FLAG = "_lifeos_command_center_safety_pause_service_installed"
_WORKER_CENTER_FLAG = "_lifeos_worker_safety_pause_service_installed"
_WORKER_STATUS_FLAG = "_lifeos_worker_safety_pause_status_installed"


def _install_command_center_pause() -> None:
    service_class = command_center.CommandCenterService
    if getattr(service_class, _COMMAND_CENTER_FLAG, False):
        return

    original_init = service_class.__init__
    original_status = service_class.status

    def __init__(self, *args, **kwargs) -> None:
        original_init(self, *args, **kwargs)
        database_path = Path(self.store.database_path)
        self.safety_pause_store = CommandCenterSafetyPauseStore(database_path)

    def paused(self) -> bool:
        return self.safety_pause_store.state().paused

    def set_paused(self, paused_value: bool) -> bool:
        with self._state_lock:
            state = (
                self.safety_pause_store.pause_manually()
                if paused_value
                else self.safety_pause_store.resume()
            )
            self._paused = state.paused
            return state.paused

    def trip_safety_pause(
        self,
        *,
        reason: str,
        affected_run_id: str | None,
        trigger: str,
        recovery_condition: str = DEFAULT_RECOVERY_CONDITION,
    ) -> dict[str, object]:
        with self._state_lock:
            state = self.safety_pause_store.trip(
                reason=reason,
                affected_run_id=affected_run_id,
                trigger=trigger,
                recovery_condition=recovery_condition,
            )
            self._paused = state.paused
            return state.to_dict()

    def pause_state(self) -> dict[str, object]:
        return self.safety_pause_store.state().to_dict()

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["pause"] = self.pause_state()
        payload["paused"] = bool(payload["pause"]["paused"])
        return payload

    service_class.__init__ = __init__
    service_class.paused = property(paused)
    service_class.set_paused = set_paused
    service_class.trip_safety_pause = trip_safety_pause
    service_class.pause_state = pause_state
    service_class.status = status
    setattr(service_class, _COMMAND_CENTER_FLAG, True)


def _trip_for_worker_result(
    center: worker_operations.BrowserWorkerCommandCenter,
    result: worker_operations.WorkerExecutionResult,
) -> None:
    pause_reason = safety_pause_reason_for_transport(
        exit_code=result.exit_code,
        stderr=result.stderr,
        reason=result.reason,
    )
    if pause_reason is None:
        return
    center.command_center.trip_safety_pause(
        reason=pause_reason,
        affected_run_id=result.run_id,
        trigger="worker_browser_transport",
    )


def _install_worker_center_pause() -> None:
    center_class = worker_operations.BrowserWorkerCommandCenter
    if getattr(center_class, _WORKER_CENTER_FLAG, False):
        return

    def execute(
        self: worker_operations.BrowserWorkerCommandCenter,
        job: worker_operations.WorkerCommandJob,
        *,
        trigger: worker_operations.ExecutionTrigger = "manual",
        timeout_seconds: int = 600,
    ) -> worker_operations.WorkerExecutionResult:
        if trigger not in {"manual", "scheduled"}:
            raise WorkerRuntimeError("Worker execution trigger must be manual or scheduled.")
        started_at = time.time()
        if self.command_center.paused:
            return self._refusal(
                job,
                trigger=trigger,
                started_at=started_at,
                reason="Automation is paused. Resume it before running a Worker job.",
            )
        if not self._run_lock.acquire(blocking=False):
            return self._refusal(
                job,
                trigger=trigger,
                started_at=started_at,
                reason=(
                    "Another automation job is running. "
                    "Let it finish before starting a Worker job."
                ),
            )
        try:
            try:
                entry = self.runtime.validate_envelope(job.envelope)
            except WorkerRuntimeError as exc:
                return self._refusal(
                    job,
                    trigger=trigger,
                    started_at=started_at,
                    reason=str(exc),
                )
            if job.mode == "send" and self.history.successful_send_exists(
                job.envelope.idempotency_key
            ):
                return self._refusal(
                    job,
                    trigger=trigger,
                    started_at=started_at,
                    reason="This Worker task revision already has a successful send record.",
                    destination=entry.chat_title,
                )
            result, evidence = worker_operations.run_worker_browser_transport(
                job,
                entry,
                self.command_center.app_root,
                trigger=trigger,
                timeout_seconds=timeout_seconds,
            )
            self.history.record(result)
            if result.status == "succeeded":
                self.browser_evidence.attach(result.run_id, evidence)
            _trip_for_worker_result(self, result)
            return result
        finally:
            self._run_lock.release()

    center_class.execute = execute
    setattr(center_class, _WORKER_CENTER_FLAG, True)


def _install_worker_status_pause() -> None:
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _WORKER_STATUS_FLAG, False):
        return
    original_status = service_class.status

    def status(self: worker_operations.WorkerOperationsService) -> dict[str, object]:
        payload = original_status(self)
        payload["pause"] = self.command_center.pause_state()
        payload["paused"] = bool(payload["pause"]["paused"])
        return payload

    service_class.status = status
    setattr(service_class, _WORKER_STATUS_FLAG, True)


def install_command_center_safety_pause_runtime() -> bool:
    """Install one persisted shared pause plus narrow automatic trip conditions."""

    if getattr(command_center, _INSTALL_FLAG, False):
        return False
    _install_command_center_pause()
    _install_worker_center_pause()
    _install_worker_status_pause()
    setattr(command_center, _INSTALL_FLAG, True)
    return True


install_command_center_safety_pause_runtime()


__all__ = ["install_command_center_safety_pause_runtime"]
