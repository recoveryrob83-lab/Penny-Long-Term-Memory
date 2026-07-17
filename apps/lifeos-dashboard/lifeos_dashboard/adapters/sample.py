"""Sample dashboard source used before live integrations are configured."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


class SampleDashboardSource:
    """Load a dashboard snapshot from packaged sample JSON."""

    name = "sample"

    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path

    def load(self) -> dict[str, Any]:
        """Read and return a defensive copy of the sample payload."""
        with self._data_path.open("r", encoding="utf-8") as source:
            payload = json.load(source)

        if not isinstance(payload, dict):
            raise ValueError("Sample dashboard data must contain a JSON object.")

        return deepcopy(payload)
