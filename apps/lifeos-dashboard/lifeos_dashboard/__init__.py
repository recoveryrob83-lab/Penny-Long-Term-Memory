"""LifeOS dashboard package."""
# ruff: noqa: E402, F401, I001

__all__ = ["__version__"]

__version__ = "0.1.0"

# Import runtime policies once at package load so FastAPI, tests, and direct
# package consumers share the same live-repository and automation guidance.
# The ledger wrapper loads before the bounded debug recurrence wrapper so the
# latter can publish its final auto-stop state through the same boundary.
from . import schedule_ledger_runtime as _schedule_ledger_runtime
from . import (
    command_center_debug_schedule_runtime as _command_center_debug_schedule_runtime,
    command_center_runtime as _command_center_runtime,
    department_inspection_runtime as _department_inspection_runtime,
)
