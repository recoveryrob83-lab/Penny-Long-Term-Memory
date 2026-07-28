"""LifeOS dashboard package."""
# ruff: noqa: E402, F401, I001

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
