"""Source adapters for LifeOS dashboard data."""

from .base import DashboardSource
from .sample import SampleDashboardSource

__all__ = ["DashboardSource", "SampleDashboardSource"]
