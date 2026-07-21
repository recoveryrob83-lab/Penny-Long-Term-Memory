"""LifeOS dashboard package."""
# ruff: noqa: E402, F401, I001

__all__ = ["__version__"]

__version__ = "0.1.0"

from . import schedule_ledger_runtime as _schedule_ledger_runtime
from . import (
    command_center_debug_schedule_runtime as _command_center_debug_schedule_runtime,
    command_center_runtime as _command_center_runtime,
    command_center_schedule_policy_runtime as _command_center_schedule_policy_runtime,
    department_inspection_runtime as _department_inspection_runtime,
)
from . import command_center_canonical_prompt_runtime as _command_center_canonical_prompt_runtime
from . import automation_foreground_guard_runtime as _automation_foreground_guard_runtime
from . import automation_write_verification_runtime as _automation_write_verification_runtime
from . import command_center_timeout_diagnostics_runtime as _command_center_timeout_diagnostics_runtime
from . import command_center_failure_precision_runtime as _command_center_failure_precision_runtime
from . import automation_logs_runtime as _automation_logs_runtime
from . import worker_verification_runtime as _worker_verification_runtime
from . import worker_response_receiver_runtime as _worker_response_receiver_runtime
from . import worker_dispatch_runtime as _worker_dispatch_runtime
