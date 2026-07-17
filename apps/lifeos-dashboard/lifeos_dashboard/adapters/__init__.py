"""Source adapters for LifeOS dashboard data."""

from .base import DashboardSource
from .calendar_ical import GoogleCalendarIcalDashboardSource
from .local_github import LocalGitHubDashboardSource
from .sample import SampleDashboardSource
from .todoist import TodoistDashboardSource
from .trello import TrelloFlowDashboardSource

__all__ = [
    "DashboardSource",
    "GoogleCalendarIcalDashboardSource",
    "LocalGitHubDashboardSource",
    "SampleDashboardSource",
    "TodoistDashboardSource",
    "TrelloFlowDashboardSource",
]
