"""LifeOS dashboard package."""
# ruff: noqa: E402, F401, I001

import sqlite3 as _sqlite3
import subprocess as _subprocess
from functools import wraps as _wraps

__all__ = ["__version__"]

__version__ = "0.1.0"

from . import schedule_ledger_runtime as _schedule_ledger_runtime
from . import (
    command_center_debug_schedule_runtime as _command_center_debug_schedule_runtime,
    command_center_runtime as _command_center_runtime,
    command_center_schedule_policy_runtime as _command_center_schedule_policy_runtime,
    department_inspection_runtime as _department_inspection_runtime,
)
from . import (
    command_center_canonical_prompt_runtime as _command_center_canonical_prompt_runtime,
)
from . import (
    automation_foreground_guard_runtime as _automation_foreground_guard_runtime,
)
from . import (
    automation_write_verification_runtime as _automation_write_verification_runtime,
)
from . import (
    command_center_timeout_diagnostics_runtime as _command_center_timeout_diagnostics_runtime,
)
from . import (
    command_center_failure_precision_runtime as _command_center_failure_precision_runtime,
)
from . import automation_logs_runtime as _automation_logs_runtime
from . import command_center_safety_pause_runtime as _command_center_safety_pause_runtime
from . import worker_verification_runtime as _worker_verification_runtime
from . import worker_response_receiver_runtime as _worker_response_receiver_runtime
from . import worker_dispatch_runtime as _worker_dispatch_runtime
from . import worker_result_ingester_runtime as _worker_result_ingester_runtime
from . import (
    worker_result_ingester_history_runtime as _worker_result_ingester_history_runtime,
)
from . import (
    worker_rob_validation_prerequisites_runtime as _worker_rob_validation_prerequisites_runtime,
)
from . import worker_hq_review_runtime as _worker_hq_review_runtime
from . import (
    worker_github_orchestrator_runtime as _worker_github_orchestrator_runtime,
)
from .worker_github_orchestrator import WorkerGitHubOrchestrator as _WorkerGitHubOrchestrator
from .worker_runtime import WorkerRuntimeError as _WorkerRuntimeError
from . import (
    worker_maintenance_relay_repair_runtime as _worker_maintenance_relay_repair_runtime,
)

_maintenance_send_hq_wake = _WorkerGitHubOrchestrator._send_hq_wake

from . import (
    worker_hq_review_state_repair_runtime as _worker_hq_review_state_repair_runtime,
)

_state_repair_ingest_hq_review = (
    _WorkerGitHubOrchestrator._ingest_hq_review_if_present
)

from . import (
    worker_hq_review_resume_runtime as _worker_hq_review_resume_runtime,
)

_resume_send_hq_wake = _WorkerGitHubOrchestrator._send_hq_wake
_resume_ingest_hq_review = _WorkerGitHubOrchestrator._ingest_hq_review_if_present


@_wraps(_maintenance_send_hq_wake)
def _composed_send_hq_wake(self, run_id: str, advisory_id: str) -> None:
    """Use the resume path while preserving the established relay interface."""

    _resume_send_hq_wake(self, run_id, advisory_id)


@_wraps(_state_repair_ingest_hq_review)
def _composed_ingest_hq_review(self, run_id: str, advisory_id: str) -> None:
    """Keep pre-migration fixtures on the prior reconciliation path."""

    row = self._row(run_id)
    row_keys = set(row.keys()) if row is not None else set()
    if "hq_review_resume_review_path" not in row_keys:
        _state_repair_ingest_hq_review(self, run_id, advisory_id)
        return
    _resume_ingest_hq_review(self, run_id, advisory_id)


_WorkerGitHubOrchestrator._send_hq_wake = _composed_send_hq_wake
_WorkerGitHubOrchestrator._ingest_hq_review_if_present = (
    _composed_ingest_hq_review
)

from . import (
    worker_report_repair_live_recovery_runtime as _worker_report_repair_live_recovery_runtime,
)
from . import (
    worker_activation_readiness_runtime as _worker_activation_readiness_runtime,
)

_base_orchestrator_run_once = _WorkerGitHubOrchestrator.run_once


def _successful_git_sync_for_cycle(self) -> bool:
    """Require a successful non-skipped sync from the cycle that just completed."""

    started_at = self._last_cycle_started_at
    if started_at is None:
        return False
    for event in reversed(self._events):
        if event.occurred_at < started_at:
            break
        if event.action == "git_sync":
            return event.status == "succeeded" and "skipped" not in event.detail
    return False


@_wraps(_base_orchestrator_run_once)
def _composed_orchestrator_run_once(self) -> dict[str, object]:
    """Advance an authorized existing-run review independently of Worker discovery."""

    status = _base_orchestrator_run_once(self)
    if self.operations.command_center.paused or self._last_error:
        return status
    if not _successful_git_sync_for_cycle(self):
        return status

    hq_review = getattr(self.operations, "hq_review", None)
    if hq_review is None:
        return status

    if not self._cycle_lock.acquire(blocking=False):
        return self.status()

    run_id = _worker_hq_review_resume_runtime._EXPECTED_RUN_ID
    advisory_id = _worker_hq_review_resume_runtime._ADVISORY_ID
    try:
        _worker_hq_review_resume_runtime._ensure_resume_columns(hq_review)
        row = self._row(run_id)
        if row is None:
            return self.status()
        if (
            str(row["result_state"] or "")
            == _worker_hq_review_resume_runtime._REPAIR_PENDING
            and str(row["hq_review_state"] or "")
            == _worker_hq_review_resume_runtime._REPAIR_REQUIRED
        ):
            _worker_hq_review_resume_runtime._send_resume_wake(
                self,
                run_id,
                advisory_id,
            )
            _worker_hq_review_resume_runtime._ingest_resume_if_present(
                self,
                run_id,
                advisory_id,
            )
    except (
        OSError,
        ValueError,
        _sqlite3.Error,
        _subprocess.TimeoutExpired,
        _WorkerRuntimeError,
    ) as exc:
        self._last_error = str(exc)
        self._event(
            "hq_review_resume_cycle",
            "stopped",
            str(exc),
            run_id=run_id,
            advisory_id=advisory_id,
        )
    finally:
        self._cycle_lock.release()
    return self.status()


_WorkerGitHubOrchestrator.run_once = _composed_orchestrator_run_once
