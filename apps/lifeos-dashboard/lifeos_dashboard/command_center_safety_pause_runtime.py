"""Install the persisted shared pause, send budget, and Worker transport trip points."""
from __future__ import annotations

import os
import time
from pathlib import Path

from . import command_center, worker_operations
from .command_center_safety_pause import (
    DEFAULT_RECOVERY_CONDITION,
    CommandCenterSafetyPauseStore,
    safety_pause_reason_for_transport,
)
from .command_center_send_budget import (
    BUDGET_RECOVERY_CONDITION,
    CommandCenterSendBudgetStore,
    SendBudgetDecision,
    configured_send_budget_limit,
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
        start_scheduler = bool(kwargs.get("start_scheduler", False))
        if start_scheduler:
            kwargs = dict(kwargs)
            kwargs["start_scheduler"] = False
        original_init(self, *args, **kwargs)
        database_path = Path(self.store.database_path)
        self.safety_pause_store = CommandCenterSafetyPauseStore(database_path)
        self.send_budget_store = CommandCenterSendBudgetStore(
            database_path,
            limit=configured_send_budget_limit(
                os.getenv("LIFEOS_GLOBAL_SEND_BUDGET_LIMIT")
            ),
        )
        if start_scheduler:
            self.start_scheduler()

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

    def send_budget_state(self) -> dict[str, object]:
        return self.send_budget_store.state().to_dict()

    def reserve_send_budget(self, *, kind: str, run_id: str) -> SendBudgetDecision:
        return self.send_budget_store.reserve(kind=kind, run_id=run_id)

    def append_send_budget_evidence(
        self,
        *,
        run_id: str,
        decision: SendBudgetDecision,
    ) -> None:
        self.send_budget_store.append_execution_evidence(
            run_id=run_id,
            decision=decision,
        )

    def reset_send_budget(self, *, confirm_reset: bool) -> dict[str, object]:
        if not confirm_reset:
            raise ValueError("Resetting the global send budget requires explicit confirmation.")
        if not self.paused:
            raise ValueError("Pause automation before resetting the global send budget.")
        if not self._run_lock.acquire(blocking=False):
            raise ValueError("Another automation job is running; the send budget was not reset.")
        try:
            return self.send_budget_store.reset().to_dict()
        finally:
            self._run_lock.release()

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["pause"] = self.pause_state()
        payload["paused"] = bool(payload["pause"]["paused"])
        payload["send_budget"] = self.send_budget_state()
        return payload

    service_class.__init__ = __init__
    service_class.paused = property(paused)
    service_class.set_paused = set_paused
    service_class.trip_safety_pause = trip_safety_pause
    service_class.pause_state = pause_state
    service_class.send_budget_state = send_budget_state
    service_class.reserve_send_budget = reserve_send_budget
    service_class.append_send_budget_evidence = append_send_budget_evidence
    service_class.reset_send_budget = reset_send_budget
    service_class.status = status
    setattr(service_class, _COMMAND_CENTER_FLAG, True)


def _pause_reason_for_worker_result(
    result: worker_operations.WorkerExecutionResult,
) -> str | None:
    return safety_pause_reason_for_transport(
        exit_code=result.exit_code,
        stderr=result.stderr,
        reason=result.reason,
    )


def _trip_worker_pause(
    center: worker_operations.BrowserWorkerCommandCenter,
    result: worker_operations.WorkerExecutionResult,
    *,
    reason: str,
) -> None:
    center.command_center.trip_safety_pause(
        reason=reason,
        affected_run_id=result.run_id,
        trigger="worker_browser_transport",
    )


def _trip_for_worker_result(
    center: worker_operations.BrowserWorkerCommandCenter,
    result: worker_operations.WorkerExecutionResult,
) -> None:
    pause_reason = _pause_reason_for_worker_result(result)
    if pause_reason is not None:
        _trip_worker_pause(center, result, reason=pause_reason)


def _reserve_worker_budget(
    center: worker_operations.BrowserWorkerCommandCenter,
    job: worker_operations.WorkerCommandJob,
    *,
    trigger: worker_operations.ExecutionTrigger,
    started_at: float,
    destination: str,
) -> SendBudgetDecision | worker_operations.WorkerExecutionResult:
    decision = center.command_center.reserve_send_budget(
        kind="worker_dispatch",
        run_id=job.envelope.run_id,
    )
    if decision.reserved:
        return decision
    center.command_center.trip_safety_pause(
        reason=decision.reason,
        affected_run_id=job.envelope.run_id,
        trigger="send_budget",
        recovery_condition=BUDGET_RECOVERY_CONDITION,
    )
    return center._refusal(
        job,
        trigger=trigger,
        started_at=started_at,
        reason=(
            f"{decision.reason} Reset the budget explicitly while paused before another send."
        ),
        destination=destination,
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

            budget = _reserve_worker_budget(
                self,
                job,
                trigger=trigger,
                started_at=started_at,
                destination=entry.chat_title,
            )
            if isinstance(budget, worker_operations.WorkerExecutionResult):
                return budget

            try:
                result, evidence = worker_operations.run_worker_browser_transport(
                    job,
                    entry,
                    self.command_center.app_root,
                    trigger=trigger,
                    timeout_seconds=timeout_seconds,
                )
            except Exception:
                self.command_center.trip_safety_pause(
                    reason=(
                        "Worker browser transport raised an unclassified exception after entering "
                        "the confirmed send path."
                    ),
                    affected_run_id=job.envelope.run_id,
                    trigger="worker_browser_transport",
                )
                raise

            try:
                self.history.record(result)
                self.command_center.append_send_budget_evidence(
                    run_id=result.run_id,
                    decision=budget,
                )
                if result.status == "succeeded":
                    self.browser_evidence.attach(result.run_id, evidence)
            except Exception:
                pause_reason = _pause_reason_for_worker_result(result)
                if result.status == "succeeded" and pause_reason is None:
                    pause_reason = (
                        "A confirmed Worker send completed, but authoritative runtime evidence "
                        "could not be persisted."
                    )
                if pause_reason is not None:
                    _trip_worker_pause(self, result, reason=pause_reason)
                raise

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
        payload["send_budget"] = self.command_center.send_budget_state()
        return payload

    service_class.status = status
    setattr(service_class, _WORKER_STATUS_FLAG, True)


def install_command_center_safety_pause_runtime() -> bool:
    """Install one persisted shared pause, budget, and narrow automatic trip conditions."""

    if getattr(command_center, _INSTALL_FLAG, False):
        return False
    _install_command_center_pause()
    _install_worker_center_pause()
    _install_worker_status_pause()
    setattr(command_center, _INSTALL_FLAG, True)
    return True


install_command_center_safety_pause_runtime()


__all__ = ["install_command_center_safety_pause_runtime"]
