"""LifeOS dashboard package."""

__all__ = ["__version__"]

__version__ = "0.1.0"

# Import the runtime policy once at package load so every parser consumer,
# including FastAPI and tests, uses the same conservative live-repository rules.
from . import department_inspection_runtime as _department_inspection_runtime  # noqa: E402,F401
