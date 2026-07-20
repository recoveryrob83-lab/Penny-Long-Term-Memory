"""Receiver-side semantic validation and controlled outcomes for LifeOS Workers."""
from __future__ import annotations

from pathlib import Path
from typing import cast

from .worker_receiver_models import (
    CanonicalProcedureSpec,
    ControlledOutcome,
    ExecutionEvidence,
    ReceiverAssignment,
    ReceiverOutcomeRecord,
    ReceiverPreflightResult,
    WorkerAuthorityProfile,
    checksum_parameters,
    parameter_matches,
    scope_allowed,
    sha256_text,
)
from .worker_receiver_store import WorkerReceiverStore
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService


class WorkerReceiverService:
    """Validate semantics, consume revisions, and record one controlled outcome."""

    def __init__(self, database_path: Path) -> None:
        self.runtime = WorkerRuntimeService(database_path)
        self.store = WorkerReceiverStore(database_path)

    @staticmethod
    def _decision(status: str, *reasons: str) -> ReceiverPreflightResult:
        return ReceiverPreflightResult(
            status=status, reasons=tuple(reasons)
        )  # type: ignore[arg-type]

    def evaluate(
        self,
        assignment: ReceiverAssignment,
        profile: WorkerAuthorityProfile,
        procedure: CanonicalProcedureSpec,
    ) -> ReceiverPreflightResult:
        try:
            entry = self.runtime.validate_envelope(assignment.envelope)
        except WorkerRuntimeError as exc:
            return self._decision("REPORT_AND_HOLD", str(exc))

        identity_errors = self._identity_errors(assignment, profile, procedure, entry)
        if identity_errors:
            return self._decision("REPORT_AND_HOLD", *identity_errors)
        if self._requires_elevation(assignment):
            return self._decision(
                "ELEVATE_FOR_APPROVAL",
                "The assignment requests authority or an exception that requires Rob's approval.",
            )
        semantic_errors = self._semantic_errors(assignment, profile, procedure)
        if semantic_errors:
            return self._decision("REPORT_AND_HOLD", *semantic_errors)
        return self._decision("READY", "Semantic receiver validation passed.")

    def receive(
        self,
        assignment: ReceiverAssignment,
        profile: WorkerAuthorityProfile,
        procedure: CanonicalProcedureSpec,
    ) -> ReceiverPreflightResult:
        decision = self.evaluate(assignment, profile, procedure)
        if decision.status != "READY":
            self.store.record_terminal_preflight(
                assignment,
                profile,
                cast(ControlledOutcome, decision.status),
                " ".join(decision.reasons),
            )
            return decision
        try:
            accepted_at = self.store.accept(assignment, profile)
        except WorkerRuntimeError as exc:
            hold = self._decision("REPORT_AND_HOLD", str(exc))
            self.store.record_terminal_preflight(
                assignment, profile, "REPORT_AND_HOLD", str(exc)
            )
            return hold
        return ReceiverPreflightResult(
            status="READY",
            reasons=decision.reasons,
            accepted_at=accepted_at,
        )

    @staticmethod
    def _identity_errors(
        assignment: ReceiverAssignment,
        profile: WorkerAuthorityProfile,
        procedure: CanonicalProcedureSpec,
        entry: WorkerRegistryEntry,
    ) -> tuple[str, ...]:
        errors: list[str] = []
        envelope = assignment.envelope
        if profile.worker_id != entry.worker_id:
            errors.append("Worker profile ID does not match the registered Worker.")
        if profile.profile_version != entry.profile_version:
            errors.append("Worker profile version does not match the registry.")
        if profile.owning_department != entry.owning_department:
            errors.append("Worker profile department does not match the registry.")
        if assignment.target_department != profile.owning_department:
            errors.append("Assignment target department does not own this Worker.")
        if envelope.procedure_id != procedure.procedure_id:
            errors.append("Envelope procedure ID does not match the canonical procedure.")
        if envelope.procedure_version != procedure.procedure_version:
            errors.append("Envelope procedure version does not match the canonical procedure.")
        if assignment.task_class != procedure.task_class:
            errors.append("Assignment task class does not match the canonical procedure.")
        return tuple(errors)

    @staticmethod
    def _requires_elevation(assignment: ReceiverAssignment) -> bool:
        new_scope = any(
            (
                assignment.requests_new_authority,
                assignment.requests_new_spending,
                assignment.requests_new_connector,
                assignment.requests_cross_department_authority,
                assignment.requests_material_exception,
            )
        )
        return (
            new_scope or assignment.authorization_class == "APPROVAL_REQUIRED"
        ) and not bool((assignment.approval_reference or "").strip())

    @staticmethod
    def _semantic_errors(
        assignment: ReceiverAssignment,
        profile: WorkerAuthorityProfile,
        procedure: CanonicalProcedureSpec,
    ) -> tuple[str, ...]:
        errors: list[str] = []
        envelope = assignment.envelope
        if assignment.transport_scope_change_detected:
            errors.append("Transport text materially changes the authoritative assignment.")
        if assignment.task_class in profile.prohibited_task_classes:
            errors.append("Task class is explicitly prohibited by the Worker profile.")
        if assignment.task_class not in profile.allowed_task_classes:
            errors.append("Task class is not allowed by the Worker profile.")
        source_classes = profile.calling_source_task_classes.get(
            envelope.authorization_source
        )
        if source_classes is None:
            errors.append("Calling source is not authorized by the Worker profile.")
        elif assignment.task_class not in source_classes:
            errors.append("Calling source may not request this task class.")
        if assignment.authorization_class not in procedure.allowed_authorization_classes:
            errors.append("Authorization class is not allowed by the canonical procedure.")
        if assignment.procedure_checksum != procedure.checksum:
            errors.append("Canonical procedure checksum does not match.")
        if assignment.parameters_checksum != checksum_parameters(assignment.parameters):
            errors.append("Parameter checksum does not match the canonical parameters.")
        if envelope.verification_mode != procedure.required_verification_mode:
            errors.append("Verification mode is weaker or different from the canonical procedure.")
        if envelope.verification_mode not in profile.allowed_verification_modes:
            errors.append("Verification mode is not allowed by the Worker profile.")
        if procedure.source_references_required and not assignment.source_references:
            errors.append("Required authoritative source references are missing.")
        if (
            assignment.approval_reference
            and assignment.approval_reference not in assignment.source_references
        ):
            errors.append("Approval reference is not present in authoritative source references.")
        missing = set(procedure.required_parameters) - set(assignment.parameters)
        if missing:
            errors.append(f"Required parameters are missing: {sorted(missing)}")
        unknown = set(assignment.parameters) - set(procedure.parameter_schema)
        if unknown:
            errors.append(f"Unknown parameters were supplied: {sorted(unknown)}")
        for name, expected_type in procedure.parameter_schema.items():
            if name in assignment.parameters and not parameter_matches(
                assignment.parameters[name], expected_type
            ):
                errors.append(f"Parameter {name!r} must be {expected_type}.")
        if assignment.authorization_class == "READ_ONLY" and assignment.requested_write_scopes:
            errors.append("READ_ONLY authorization cannot request write scope.")
        for scope in assignment.requested_read_scopes:
            if not scope_allowed(scope, profile.read_scope_prefixes):
                errors.append(f"Requested read scope is outside the Worker profile: {scope}")
        for scope in assignment.requested_write_scopes:
            if not scope_allowed(scope, profile.write_scope_prefixes):
                errors.append(f"Requested write scope is outside the Worker profile: {scope}")
        requested_tools = set(assignment.requested_tools)
        if not requested_tools.issubset(profile.approved_tools):
            errors.append("Assignment requests a tool not approved by the Worker profile.")
        if procedure.approved_tools and not requested_tools.issubset(procedure.approved_tools):
            errors.append("Assignment requests a tool not approved by the canonical procedure.")
        return tuple(errors)

    def finalize(
        self,
        assignment: ReceiverAssignment,
        profile: WorkerAuthorityProfile,
        evidence: ExecutionEvidence,
    ) -> ReceiverOutcomeRecord:
        if evidence.approval_required_discovered:
            return self.store.finalize(
                assignment,
                "ELEVATE_FOR_APPROVAL",
                "Execution discovered authority or judgment requiring Rob's approval.",
                evidence,
            )
        errors: list[str] = []
        if evidence.completion_state != "completed":
            errors.append(
                evidence.failure_reason
                or f"Execution ended with completion state {evidence.completion_state}."
            )
        if not evidence.evidence_references:
            errors.append("Required execution evidence is missing.")
        if not evidence.external_actions_verified:
            errors.append("External action success could not be verified.")
        if evidence.verification_state == "unavailable":
            errors.append("The required verification path is unavailable.")
        if (
            assignment.envelope.verification_mode == "AUTOMATIC"
            and evidence.verification_state != "verified"
        ):
            errors.append("AUTOMATIC work requires a verified machine postcondition.")
        for scope in evidence.actual_read_scopes:
            if not scope_allowed(scope, assignment.requested_read_scopes) or not scope_allowed(
                scope, profile.read_scope_prefixes
            ):
                errors.append(f"Actual read scope exceeded authorization: {scope}")
        for scope in evidence.actual_write_scopes:
            if not scope_allowed(scope, assignment.requested_write_scopes) or not scope_allowed(
                scope, profile.write_scope_prefixes
            ):
                errors.append(f"Actual write scope exceeded authorization: {scope}")
        if not set(evidence.actual_tools).issubset(assignment.requested_tools):
            errors.append("Execution used a tool outside the authorized assignment.")
        if errors:
            return self.store.finalize(
                assignment,
                "REPORT_AND_HOLD",
                " ".join(errors),
                evidence,
            )
        return self.store.finalize(
            assignment,
            "IMPLEMENT",
            "Authorized bounded work completed and required evidence was recorded.",
            evidence,
        )


__all__ = [
    "CanonicalProcedureSpec",
    "ExecutionEvidence",
    "ReceiverAssignment",
    "ReceiverOutcomeRecord",
    "ReceiverPreflightResult",
    "WorkerAuthorityProfile",
    "WorkerReceiverService",
    "checksum_parameters",
    "sha256_text",
]
