"""Semantic contracts for LifeOS Worker receiver validation."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal, Mapping, Sequence, cast

from .worker_runtime import ExecutionEnvelope, VerificationMode, WorkerRuntimeError

AuthorizationClass = Literal["READ_ONLY", "BOUNDED_WRITE", "APPROVAL_REQUIRED"]
ControlledOutcome = Literal["IMPLEMENT", "REPORT_AND_HOLD", "ELEVATE_FOR_APPROVAL"]
PreflightStatus = Literal["READY", "REPORT_AND_HOLD", "ELEVATE_FOR_APPROVAL"]
CompletionState = Literal["completed", "partial", "failed", "not_attempted"]
VerificationState = Literal["verified", "pending", "unavailable"]

ALLOWED_AUTHORIZATION_CLASSES = {"READ_ONLY", "BOUNDED_WRITE", "APPROVAL_REQUIRED"}
ALLOWED_OUTCOMES = {"IMPLEMENT", "REPORT_AND_HOLD", "ELEVATE_FOR_APPROVAL"}
ALLOWED_VERIFICATION_STATES = {"verified", "pending", "unavailable"}
PARAMETER_TYPES = {"string", "integer", "number", "boolean", "object", "array"}


def required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise WorkerRuntimeError(f"{field_name} cannot be empty.")
    return text


def canonical_json(value: object) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    except (TypeError, ValueError) as exc:
        raise WorkerRuntimeError("Receiver parameters must be canonical JSON values.") from exc


def sha256_text(value: str) -> str:
    return "SHA256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def checksum_parameters(parameters: Mapping[str, object]) -> str:
    return sha256_text(canonical_json(dict(parameters)))


def scope_allowed(requested: str, allowed_prefixes: Sequence[str]) -> bool:
    clean = requested.strip()
    if not clean:
        return False
    for prefix in allowed_prefixes:
        base = prefix.rstrip("/")
        if clean == base or clean.startswith(base + "/"):
            return True
        if prefix.endswith(":") and clean.startswith(prefix):
            return True
    return False


def parameter_matches(value: object, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "object":
        return isinstance(value, Mapping)
    if expected_type == "array":
        return isinstance(value, (list, tuple))
    return False


@dataclass(frozen=True)
class WorkerAuthorityProfile:
    """Normalized runtime view of one department-owned Worker profile."""

    worker_id: str
    owning_department: str
    profile_version: int
    allowed_task_classes: tuple[str, ...]
    read_scope_prefixes: tuple[str, ...]
    write_scope_prefixes: tuple[str, ...]
    approved_tools: tuple[str, ...]
    calling_source_task_classes: Mapping[str, tuple[str, ...]]
    allowed_verification_modes: tuple[VerificationMode, ...]
    prohibited_task_classes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        required_text(self.worker_id, "profile worker_id")
        required_text(self.owning_department, "profile owning_department")
        if self.profile_version < 1:
            raise WorkerRuntimeError("profile_version must be a positive integer.")
        for field_name in (
            "allowed_task_classes",
            "calling_source_task_classes",
            "allowed_verification_modes",
        ):
            if not getattr(self, field_name):
                raise WorkerRuntimeError(f"{field_name} cannot be empty.")
        if set(self.allowed_task_classes) & set(self.prohibited_task_classes):
            raise WorkerRuntimeError("A task class cannot be both allowed and prohibited.")


@dataclass(frozen=True)
class CanonicalProcedureSpec:
    """Canonical procedure identity and parameter contract used by the receiver."""

    procedure_id: str
    procedure_version: int
    task_class: str
    canonical_text: str
    parameter_schema: Mapping[str, str]
    required_parameters: tuple[str, ...]
    allowed_authorization_classes: tuple[AuthorizationClass, ...]
    required_verification_mode: VerificationMode
    approved_tools: tuple[str, ...] = ()
    source_references_required: bool = True

    def __post_init__(self) -> None:
        required_text(self.procedure_id, "procedure_id")
        required_text(self.task_class, "task_class")
        required_text(self.canonical_text, "canonical_text")
        if self.procedure_version < 1:
            raise WorkerRuntimeError("procedure_version must be a positive integer.")
        unknown_types = set(self.parameter_schema.values()) - PARAMETER_TYPES
        if unknown_types:
            raise WorkerRuntimeError(f"Unsupported parameter types: {sorted(unknown_types)}")
        if not set(self.required_parameters).issubset(self.parameter_schema):
            raise WorkerRuntimeError("required_parameters must exist in parameter_schema.")
        if not self.allowed_authorization_classes:
            raise WorkerRuntimeError("allowed_authorization_classes cannot be empty.")
        if not set(self.allowed_authorization_classes).issubset(
            ALLOWED_AUTHORIZATION_CLASSES
        ):
            raise WorkerRuntimeError("Procedure authorization class is invalid.")

    @property
    def checksum(self) -> str:
        return sha256_text(self.canonical_text)


@dataclass(frozen=True)
class ReceiverAssignment:
    """Semantic assignment resolved from the authoritative task and wrapper."""

    envelope: ExecutionEnvelope
    target_department: str
    task_class: str
    authorization_class: AuthorizationClass
    procedure_checksum: str
    parameters: Mapping[str, object]
    parameters_checksum: str
    source_references: tuple[str, ...]
    requested_read_scopes: tuple[str, ...]
    requested_write_scopes: tuple[str, ...]
    requested_tools: tuple[str, ...]
    approval_reference: str | None = None
    requests_new_authority: bool = False
    requests_new_spending: bool = False
    requests_new_connector: bool = False
    requests_cross_department_authority: bool = False
    requests_material_exception: bool = False
    transport_scope_change_detected: bool = False

    def __post_init__(self) -> None:
        required_text(self.target_department, "target_department")
        required_text(self.task_class, "task_class")
        if self.authorization_class not in ALLOWED_AUTHORIZATION_CLASSES:
            raise WorkerRuntimeError("authorization_class is invalid.")
        required_text(self.procedure_checksum, "procedure_checksum")
        required_text(self.parameters_checksum, "parameters_checksum")


@dataclass(frozen=True)
class ReceiverPreflightResult:
    status: PreflightStatus
    reasons: tuple[str, ...]
    accepted_at: float | None = None

    @property
    def outcome(self) -> ControlledOutcome | None:
        if self.status == "READY":
            return None
        return cast(ControlledOutcome, self.status)


@dataclass(frozen=True)
class ExecutionEvidence:
    completion_state: CompletionState
    evidence_references: tuple[str, ...]
    actual_read_scopes: tuple[str, ...] = ()
    actual_write_scopes: tuple[str, ...] = ()
    actual_tools: tuple[str, ...] = ()
    verification_state: VerificationState = "pending"
    external_actions_verified: bool = True
    approval_required_discovered: bool = False
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if self.completion_state not in {"completed", "partial", "failed", "not_attempted"}:
            raise WorkerRuntimeError("completion_state is invalid.")
        if self.verification_state not in ALLOWED_VERIFICATION_STATES:
            raise WorkerRuntimeError("verification_state is invalid.")


@dataclass(frozen=True)
class ReceiverOutcomeRecord:
    run_id: str
    outcome: ControlledOutcome
    reason: str
    verification_state: VerificationState
    evidence_references: tuple[str, ...]
