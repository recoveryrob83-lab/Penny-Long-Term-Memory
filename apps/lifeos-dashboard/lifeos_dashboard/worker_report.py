"""Strict machine-readable evidence report emitted by a LifeOS Worker."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Mapping, cast

from .worker_receiver_models import ControlledOutcome
from .worker_runtime import WorkerRuntimeError

WORKER_REPORT_PREFIX = "LIFEOS_WORKER_REPORT="
_ALLOWED_OUTCOMES = {"IMPLEMENT", "REPORT_AND_HOLD", "ELEVATE_FOR_APPROVAL"}
_ALLOWED_COMPLETION_STATES = {"completed", "partial", "failed", "not_attempted"}
_ALLOWED_VERIFICATION_STATES = {"verified", "pending", "unavailable"}


@dataclass(frozen=True)
class WorkerExecutionReport:
    """One structured report emitted by a specialized ChatGPT Worker."""

    wrapper_id: str
    run_id: str
    worker_id: str
    profile_version: int
    owning_department: str
    task_id: str
    task_revision: int
    procedure_id: str
    procedure_version: int
    authorization_source: str
    verification_mode: str
    controlled_outcome: ControlledOutcome
    completion_state: str
    evidence_references: tuple[str, ...]
    actual_read_scopes: tuple[str, ...]
    actual_write_scopes: tuple[str, ...]
    actual_tools: tuple[str, ...]
    verification_state: str
    external_actions_verified: bool
    approval_required_discovered: bool
    failure_reason: str | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "WorkerExecutionReport":
        required = {
            "wrapper_id",
            "run_id",
            "worker_id",
            "profile_version",
            "owning_department",
            "task_id",
            "task_revision",
            "procedure_id",
            "procedure_version",
            "authorization_source",
            "verification_mode",
            "controlled_outcome",
            "completion_state",
            "evidence_references",
            "actual_read_scopes",
            "actual_write_scopes",
            "actual_tools",
            "verification_state",
            "external_actions_verified",
            "approval_required_discovered",
        }
        missing = sorted(required - set(payload))
        unknown = sorted(set(payload) - required - {"failure_reason"})
        if missing:
            raise WorkerRuntimeError(f"Worker report is missing fields: {missing}")
        if unknown:
            raise WorkerRuntimeError(
                f"Worker report contains unknown fields: {unknown}"
            )

        def text(name: str) -> str:
            value = payload.get(name)
            if not isinstance(value, str) or not value.strip():
                raise WorkerRuntimeError(
                    f"Worker report field {name} must be non-empty text."
                )
            return value.strip()

        def positive_int(name: str) -> int:
            value = payload.get(name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise WorkerRuntimeError(
                    f"Worker report field {name} must be a positive integer."
                )
            return value

        def text_tuple(name: str) -> tuple[str, ...]:
            value = payload.get(name)
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                raise WorkerRuntimeError(
                    f"Worker report field {name} must be an array of non-empty strings."
                )
            return tuple(item.strip() for item in value)

        def boolean(name: str) -> bool:
            value = payload.get(name)
            if not isinstance(value, bool):
                raise WorkerRuntimeError(f"Worker report field {name} must be boolean.")
            return value

        outcome = text("controlled_outcome").upper()
        if outcome not in _ALLOWED_OUTCOMES:
            raise WorkerRuntimeError("Worker report controlled_outcome is invalid.")
        completion_state = text("completion_state").lower()
        if completion_state not in _ALLOWED_COMPLETION_STATES:
            raise WorkerRuntimeError("Worker report completion_state is invalid.")
        verification_state = text("verification_state").lower()
        if verification_state not in _ALLOWED_VERIFICATION_STATES:
            raise WorkerRuntimeError("Worker report verification_state is invalid.")
        failure = payload.get("failure_reason")
        if failure is not None and (
            not isinstance(failure, str) or not failure.strip()
        ):
            raise WorkerRuntimeError(
                "Worker report failure_reason must be null or non-empty text."
            )

        return cls(
            wrapper_id=text("wrapper_id"),
            run_id=text("run_id"),
            worker_id=text("worker_id"),
            profile_version=positive_int("profile_version"),
            owning_department=text("owning_department"),
            task_id=text("task_id"),
            task_revision=positive_int("task_revision"),
            procedure_id=text("procedure_id"),
            procedure_version=positive_int("procedure_version"),
            authorization_source=text("authorization_source"),
            verification_mode=text("verification_mode").upper(),
            controlled_outcome=cast(ControlledOutcome, outcome),
            completion_state=completion_state,
            evidence_references=text_tuple("evidence_references"),
            actual_read_scopes=text_tuple("actual_read_scopes"),
            actual_write_scopes=text_tuple("actual_write_scopes"),
            actual_tools=text_tuple("actual_tools"),
            verification_state=verification_state,
            external_actions_verified=boolean("external_actions_verified"),
            approval_required_discovered=boolean("approval_required_discovered"),
            failure_reason=failure.strip() if isinstance(failure, str) else None,
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def parse_worker_execution_report(response_text: str) -> WorkerExecutionReport:
    """Parse exactly one strict machine-readable report from a Worker response."""

    lines = [
        line.strip()[len(WORKER_REPORT_PREFIX) :]
        for line in (response_text or "").splitlines()
        if line.strip().startswith(WORKER_REPORT_PREFIX)
    ]
    if len(lines) != 1:
        raise WorkerRuntimeError(
            "Worker response must contain exactly one LIFEOS_WORKER_REPORT line."
        )
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError("LIFEOS_WORKER_REPORT is not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise WorkerRuntimeError("LIFEOS_WORKER_REPORT must contain a JSON object.")
    return WorkerExecutionReport.from_dict(payload)


__all__ = [
    "WORKER_REPORT_PREFIX",
    "WorkerExecutionReport",
    "parse_worker_execution_report",
]
