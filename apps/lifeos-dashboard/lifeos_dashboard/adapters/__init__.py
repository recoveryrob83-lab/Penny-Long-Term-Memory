"""Source adapters for LifeOS dashboard data."""

from .base import DashboardSource
from .local_github import LocalGitHubDashboardSource
from .sample import SampleDashboardSource

__all__ = [
    "DashboardSource",
    "LocalGitHubDashboardSource",
    "SampleDashboardSource",
]
