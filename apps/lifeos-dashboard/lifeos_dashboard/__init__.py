"""LifeOS dashboard package."""

__all__ = ["__version__"]

__version__ = "0.1.0"

# Import runtime policies once at package load so FastAPI, tests, and direct
# package consumers share the same live-repository and automation guidance.
from . import (  # noqa: E402,F401
    command_center_debug_schedule_runtime as _command_center_debug_schedule_runtime,
    command_center_runtime as _command_center_runtime,
    department_inspection_runtime as _department_inspection_runtime,
)
