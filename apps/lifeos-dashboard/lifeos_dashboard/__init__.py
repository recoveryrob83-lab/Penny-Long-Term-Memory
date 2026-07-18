"""LifeOS dashboard package."""

__all__ = ["__version__"]

__version__ = "0.1.0"

# Import runtime policies once at package load so FastAPI, tests, and direct
# package consumers share the same live-repository and automation guidance.
from . import command_center_runtime as _command_center_runtime  # noqa: E402,F401
from . import department_inspection_runtime as _department_inspection_runtime  # noqa: E402,F401
