"""Explicit, dependency-free contracts for the V2 courier."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class AdvisoryState(StrEnum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    NEEDS_ROB = "NEEDS_ROB"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"


class CommandState(StrEnum):
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    UNCERTAIN = "UNCERTAIN"
    BLOCKED_ROUTE = "BLOCKED_ROUTE"
    STALE = "STALE"


@dataclass(frozen=True)
class Advisory:
    advisory_id: str
    revision: int
    source_department: str
    target_department: str
    task_summary: str
    scope: str
    state: AdvisoryState
    outcome: str
    blocker: str
    updated_at: str
    source_path: str
    source_url: str

    @property
    def command_id(self) -> str:
        return f"{self.advisory_id}-r{self.revision}"

    @property
    def actionable(self) -> bool:
        return self.state in {AdvisoryState.OPEN, AdvisoryState.IN_PROGRESS}

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        return data


@dataclass
class Route:
    route_name: str
    target: str
    chatgpt_url: str
    registered_at: str
    last_verified_at: str | None = None
    health: str = "AVAILABLE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DeliveryCommand:
    command_id: str
    advisory_id: str
    revision: int
    route_name: str
    target: str
    wake_payload: str
    state: CommandState
    created_at: str
    updated_at: str
    blocker: str = ""
    telemetry_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        return data


@dataclass
class ApiError:
    code: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {"error": asdict(self)}
