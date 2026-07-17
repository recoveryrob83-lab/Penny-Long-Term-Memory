"""Contracts for dashboard data sources."""

from __future__ import annotations

from typing import Any, Protocol


class DashboardSource(Protocol):
    """A provider that returns one normalized dashboard snapshot."""

    name: str

    def load(self) -> dict[str, Any]:
        """Return a dashboard-shaped payload."""
        ...
