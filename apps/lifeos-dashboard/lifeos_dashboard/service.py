"""Dashboard snapshot aggregation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .adapters import DashboardSource


class DashboardService:
    """Build dashboard responses from the configured source adapter."""

    def __init__(self, source: DashboardSource) -> None:
        self._source = source

    @property
    def mode(self) -> str:
        """Return the active source mode."""
        return self._source.name

    def get_snapshot(self) -> dict[str, Any]:
        """Load a snapshot and attach serving metadata."""
        payload = self._source.load()
        metadata = payload.setdefault("meta", {})
        if not isinstance(metadata, dict):
            raise ValueError("Dashboard 'meta' value must be a JSON object.")

        metadata["mode"] = self.mode
        metadata["served_at"] = datetime.now(UTC).isoformat()
        return payload
