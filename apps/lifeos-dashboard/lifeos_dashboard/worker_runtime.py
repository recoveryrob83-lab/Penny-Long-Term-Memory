"""Core contracts for LifeOS Worker routing and receiver validation."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from urllib.parse import urlsplit, urlunsplit
from typing import Literal, Mapping, Sequence, cast

DeploymentState = Literal["enabled", "paused", "retired"]
RouteAvailability = Literal["available", "unavailable", "ambiguous", "unknown"]
VerificationMode = Literal["AUTOMATIC", "ROUTINE_BATCH", "IMMEDIATE_HQ"]

_WORKER_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_CHAT_TITLE_PATTERN = re.compile(r"^[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*$")
_ALLOWED_DEPLOYMENT_STATES = {"enabled", "paused", "retired"}
_ALLOWED_ROUTE_AVAILABILITY = {"available", "unavailable", "ambiguous", "unknown"}
_ALLOWED_VERIFICATION_MODES = {"AUTOMATIC", "ROUTINE_BATCH", "IMMEDIATE_HQ"}


class WorkerRuntimeError(ValueError):
    """Raised when Worker routing or receiver validation fails closed."""


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise WorkerRuntimeError(f"{field_name} cannot be empty.")
    return text


def _positive_int(value: object, field_name: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise WorkerRuntimeError(f"{field_name} must be a positive integer.") from exc
    if number < 1:
        raise WorkerRuntimeError(f"{field_name} must be a positive integer.")
    return number


def _nonnegative_int(value: object, field_name: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise WorkerRuntimeError(f"{field_name} must be a nonnegative integer.") from exc
    if number < 0:
        raise WorkerRuntimeError(f"{field_name} must be a nonnegative integer.")
    return number


def _conversation_url(value: object) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    parsed = urlsplit(text)
    if parsed.scheme != "https" or parsed.hostname != "chatgpt.com":
        raise WorkerRuntimeError(
            "conversation_url must be an https://chatgpt.com conversation URL."
        )
    path = parsed.path.rstrip("/")
    if "/c/" not in path:
        raise WorkerRuntimeError(
            "conversation_url must identify one ChatGPT conversation."
        )
    return urlunsplit(("https", "chatgpt.com", path, "", ""))


@dataclass(frozen=True)
class WorkerRegistryEntry:
    """Stable Worker identity plus Engineering-owned deployment state."""

    worker_id: str
    chat_title: str
    owning_department: str
    profile_path: str
    profile_version: int
    conversation_url: str | None = None
    route_revision: int = 0
    specialization: str = "general"
    role: str = "worker"
    deployment_state: DeploymentState = "enabled"

    def __post_init__(self) -> None:
        if not _WORKER_ID_PATTERN.fullmatch(self.worker_id):
            raise WorkerRuntimeError(
                "worker_id must use lowercase letters, numbers, and underscores only."
            )
        if not _CHAT_TITLE_PATTERN.fullmatch(self.chat_title):
            raise WorkerRuntimeError(
                "chat_title must use ASCII letters, numbers, and underscores only."
            )
        _required_text(self.owning_department, "owning_department")
        if not (
            self.profile_path.startswith("projects/")
            and "/workers/" in self.profile_path
            and self.profile_path.endswith(".md")
        ):
            raise WorkerRuntimeError(
                "profile_path must point to projects/<department>/workers/<profile>.md."
            )
        _positive_int(self.profile_version, "profile_version")
        normalized_url = _conversation_url(self.conversation_url)
        revision = _nonnegative_int(self.route_revision, "route_revision")
        object.__setattr__(self, "conversation_url", normalized_url)
        object.__setattr__(self, "route_revision", revision)
        if normalized_url is None and revision != 0:
            raise WorkerRuntimeError(
                "route_revision must be 0 when conversation_url is absent."
            )
        if normalized_url is not None and revision < 1:
            raise WorkerRuntimeError(
                "route_revision must be at least 1 when conversation_url is registered."
            )
        _required_text(self.specialization, "specialization")
        if self.role != "worker":
            raise WorkerRuntimeError("role must be worker.")
        if self.deployment_state not in _ALLOWED_DEPLOYMENT_STATES:
            raise WorkerRuntimeError("deployment_state must be enabled, paused, or retired.")

    @classmethod
    def from_dict(cls, values: Mapping[str, object]) -> WorkerRegistryEntry:
        return cls(
            worker_id=_required_text(values.get("worker_id"), "worker_id"),
            chat_title=_required_text(values.get("chat_title"), "chat_title"),
            owning_department=_required_text(
                values.get("owning_department"), "owning_department"
            ),
            profile_path=_required_text(values.get("profile_path"), "profile_path"),
            profile_version=_positive_int(values.get("profile_version"), "profile_version"),
            conversation_url=values.get("conversation_url") or None,
            route_revision=_nonnegative_int(
                values.get("route_revision", 0), "route_revision"
            ),
            specialization=_required_text(
                values.get("specialization", "general"), "specialization"
            ),
            role=_required_text(values.get("role", "worker"), "role"),
            deployment_state=cast(
                DeploymentState, str(values.get("deployment_state", "enabled"))
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class WorkerRouteState:
    """Observed route availability for one registered Worker."""

    worker_id: str
    availability: RouteAvailability = "unknown"
    last_seen_at: float | None = None
    pause_reason: str | None = None

    def __post_init__(self) -> None:
        if not _WORKER_ID_PATTERN.fullmatch(self.worker_id):
            raise WorkerRuntimeError("route-state worker_id is invalid.")
        if self.availability not in _ALLOWED_ROUTE_AVAILABILITY:
            raise WorkerRuntimeError(
                "availability must be available, unavailable, ambiguous, or unknown."
            )


@dataclass(frozen=True)
class WorkerReceiverState:
    """Duplicate-suppression state for one Worker and one authoritative task."""

    worker_id: str
    task_id: str
    last_processed_revision: int = 0
    last_run_id: str | None = None

    def __post_init__(self) -> None:
        if not _WORKER_ID_PATTERN.fullmatch(self.worker_id):
            raise WorkerRuntimeError("receiver-state worker_id is invalid.")
        _required_text(self.task_id, "task_id")
        if self.last_processed_revision < 0:
            raise WorkerRuntimeError("last_processed_revision cannot be negative.")


@dataclass(frozen=True)
class ExecutionEnvelope:
    """Compact machine-readable wrapper for one execution-ready assignment."""

    wrapper_id: str
    run_id: str
    worker_id: str
    task_id: str
    task_revision: int
    procedure_id: str
    procedure_version: int
    authorization_source: str
    verification_mode: VerificationMode

    def __post_init__(self) -> None:
        _required_text(self.wrapper_id, "wrapper_id")
        _required_text(self.run_id, "run_id")
        if not _WORKER_ID_PATTERN.fullmatch(self.worker_id):
            raise WorkerRuntimeError("worker_id is invalid.")
        _required_text(self.task_id, "task_id")
        _positive_int(self.task_revision, "task_revision")
        _required_text(self.procedure_id, "procedure_id")
        _positive_int(self.procedure_version, "procedure_version")
        _required_text(self.authorization_source, "authorization_source")
        if self.verification_mode not in _ALLOWED_VERIFICATION_MODES:
            raise WorkerRuntimeError(
                "verification_mode must be AUTOMATIC, ROUTINE_BATCH, or IMMEDIATE_HQ."
            )

    @property
    def idempotency_key(self) -> str:
        return f"{self.worker_id}:{self.task_id}:{self.task_revision}"

    @classmethod
    def from_dict(cls, values: Mapping[str, object]) -> ExecutionEnvelope:
        return cls(
            wrapper_id=_required_text(values.get("wrapper_id"), "wrapper_id"),
            run_id=_required_text(values.get("run_id"), "run_id"),
            worker_id=_required_text(values.get("worker_id"), "worker_id"),
            task_id=_required_text(values.get("task_id"), "task_id"),
            task_revision=_positive_int(values.get("task_revision"), "task_revision"),
            procedure_id=_required_text(values.get("procedure_id"), "procedure_id"),
            procedure_version=_positive_int(
                values.get("procedure_version"), "procedure_version"
            ),
            authorization_source=_required_text(
                values.get("authorization_source"), "authorization_source"
            ),
            verification_mode=cast(
                VerificationMode, str(values.get("verification_mode"))
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def resolve_worker_by_title(
    entries: Sequence[WorkerRegistryEntry], chat_title: str
) -> WorkerRegistryEntry:
    """Return one exact enabled title match or fail closed."""

    matches = [entry for entry in entries if entry.chat_title == chat_title]
    if not matches:
        raise WorkerRuntimeError(f"No Worker matches exact chat title {chat_title!r}.")
    if len(matches) > 1:
        raise WorkerRuntimeError(f"Multiple Workers match exact chat title {chat_title!r}.")
    entry = matches[0]
    if entry.deployment_state != "enabled":
        raise WorkerRuntimeError(
            f"Worker {entry.worker_id!r} is {entry.deployment_state}, not enabled."
        )
    return entry


def validate_execution_ready(
    envelope: ExecutionEnvelope,
    entry: WorkerRegistryEntry,
    route_state: WorkerRouteState,
    receiver_state: WorkerReceiverState | None = None,
) -> None:
    """Validate routing, availability, identity, and revision before execution."""

    if envelope.worker_id != entry.worker_id:
        raise WorkerRuntimeError("Envelope worker_id does not match the registry entry.")
    if route_state.worker_id != entry.worker_id:
        raise WorkerRuntimeError("Route state does not belong to the target Worker.")
    if route_state.availability != "available":
        raise WorkerRuntimeError(
            f"Worker route is {route_state.availability}; execution must hold."
        )
    if receiver_state is None:
        return
    if receiver_state.worker_id != entry.worker_id:
        raise WorkerRuntimeError("Receiver state does not belong to the target Worker.")
    if receiver_state.task_id != envelope.task_id:
        raise WorkerRuntimeError("Receiver state does not belong to the envelope task.")
    if envelope.task_revision <= receiver_state.last_processed_revision:
        raise WorkerRuntimeError("Envelope revision is stale or already processed.")


def copied_text_contains_wrapper(copied_text: str, expected_wrapper_id: str) -> bool:
    """Use the expected wrapper marker as the minimal composer write witness."""

    marker = expected_wrapper_id.strip()
    return bool(marker) and marker in copied_text
