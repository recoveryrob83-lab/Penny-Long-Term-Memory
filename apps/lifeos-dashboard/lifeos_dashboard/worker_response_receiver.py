"""Reconcile one captured Worker response through the semantic receiver."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import cast

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_receiver import (
    ExecutionEvidence,
    ReceiverAssignment,
    WorkerAuthorityProfile,
    WorkerReceiverService,
)
from .worker_receiver_models import ControlledOutcome
from .worker_receiver_resolution import resolve_receiver_assignment
from .worker_report import (
    WORKER_REPORT_PREFIX,
    WorkerExecutionReport,
    parse_worker_execution_report,
)
from .worker_response_store import WorkerResponseStore
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError


@dataclass(frozen=True)
class WorkerResponseReconciliation:
    run_id: str
    state: str
    controlled_outcome: ControlledOutcome
    reported_outcome: ControlledOutcome | None
    reason: str
    report_consistent: bool
    hq_review_required: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _report_identity_errors(
    report: WorkerExecutionReport,
    assignment: ReceiverAssignment,
    profile: WorkerAuthorityProfile,
) -> tuple[str, ...]:
    envelope = assignment.envelope
    expected: dict[str, object] = {
        "wrapper_id": envelope.wrapper_id,
        "run_id": envelope.run_id,
        "worker_id": envelope.worker_id,
        "profile_version": profile.profile_version,
        "owning_department": profile.owning_department,
        "task_id": envelope.task_id,
        "task_revision": envelope.task_revision,
        "procedure_id": envelope.procedure_id,
        "procedure_version": envelope.procedure_version,
        "authorization_source": envelope.authorization_source,
        "verification_mode": envelope.verification_mode,
    }
    errors: list[str] = []
    for field_name, expected_value in expected.items():
        if getattr(report, field_name) != expected_value:
            errors.append(
                f"Worker report {field_name} does not match the accepted assignment."
            )
    if (
        envelope.verification_mode == "IMMEDIATE_HQ"
        and report.verification_state != "pending"
    ):
        errors.append(
            "Worker report verification_state must remain pending until Immediate HQ review."
        )
    return tuple(errors)


class WorkerResponseReceiver:
    """Resolve, validate, and finalize one browser-captured Worker response."""

    def __init__(self, database_path: Path, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.receiver = WorkerReceiverService(database_path)
        self.store = WorkerResponseStore(database_path)

    def _already_reconciled(
        self, advisory: ExecutionReadyAdvisory
    ) -> WorkerResponseReconciliation | None:
        existing = self.store.existing_outcome(advisory.run_id)
        if existing is None or existing.controlled_outcome is None:
            return None
        controlled = existing.controlled_outcome
        reported = existing.reported_outcome
        return WorkerResponseReconciliation(
            run_id=advisory.run_id,
            state="already_reconciled",
            controlled_outcome=controlled,
            reported_outcome=reported,
            reason=existing.receiver_reason or "Run already reconciled.",
            report_consistent=bool(reported and reported == controlled),
            hq_review_required=(
                controlled == "IMPLEMENT"
                and existing.verification_mode == "IMMEDIATE_HQ"
            ),
        )

    def _unresolved_hold(
        self, run_id: str, reason: str
    ) -> WorkerResponseReconciliation:
        state, controlled, reported, final_reason = self.store.record_unresolved_hold(
            run_id, reason
        )
        return WorkerResponseReconciliation(
            run_id=run_id,
            state=state,
            controlled_outcome=controlled,
            reported_outcome=reported,
            reason=final_reason,
            report_consistent=bool(reported and reported == controlled),
            hq_review_required=False,
        )

    def reconcile(
        self,
        advisory: ExecutionReadyAdvisory,
        entry: WorkerRegistryEntry,
        response_text: str,
    ) -> WorkerResponseReconciliation:
        existing = self._already_reconciled(advisory)
        if existing is not None:
            return existing

        try:
            resolved = resolve_receiver_assignment(
                self.repository_root, advisory, entry
            )
        except (OSError, ValueError, WorkerRuntimeError) as exc:
            return self._unresolved_hold(
                advisory.run_id, f"Canonical receiver resolution failed: {exc}"
            )

        preflight = self.receiver.receive(
            resolved.assignment, resolved.profile, resolved.procedure
        )
        if preflight.status != "READY":
            current = self.store.existing_outcome(advisory.run_id)
            assert current is not None
            controlled = cast(ControlledOutcome, preflight.status)
            return WorkerResponseReconciliation(
                run_id=advisory.run_id,
                state="held" if controlled == "REPORT_AND_HOLD" else "elevated",
                controlled_outcome=controlled,
                reported_outcome=current.reported_outcome,
                reason=" ".join(preflight.reasons),
                report_consistent=bool(current.reported_outcome == controlled),
                hq_review_required=False,
            )

        try:
            report = parse_worker_execution_report(response_text)
        except WorkerRuntimeError as exc:
            evidence = ExecutionEvidence(
                completion_state="failed",
                evidence_references=(f"execution_history:{advisory.run_id}",),
                verification_state="unavailable",
                external_actions_verified=False,
                failure_reason=f"Worker report validation failed: {exc}",
            )
            outcome = self.receiver.finalize(
                resolved.assignment, resolved.profile, evidence
            )
            return WorkerResponseReconciliation(
                run_id=advisory.run_id,
                state="held",
                controlled_outcome=outcome.outcome,
                reported_outcome=None,
                reason=outcome.reason,
                report_consistent=False,
                hq_review_required=False,
            )

        prior_reported = self.store.record_machine_reported_outcome(
            advisory.run_id, report.controlled_outcome
        )
        identity_errors = list(
            _report_identity_errors(report, resolved.assignment, resolved.profile)
        )
        if prior_reported is not None and prior_reported != report.controlled_outcome:
            identity_errors.append(
                "Browser-parsed outcome conflicts with the machine-readable Worker report."
            )
        if identity_errors:
            evidence = ExecutionEvidence(
                completion_state="failed",
                evidence_references=report.evidence_references
                or (f"execution_history:{advisory.run_id}",),
                actual_read_scopes=report.actual_read_scopes,
                actual_write_scopes=report.actual_write_scopes,
                actual_tools=report.actual_tools,
                verification_state="unavailable",
                external_actions_verified=False,
                failure_reason=" ".join(identity_errors),
            )
        else:
            evidence = ExecutionEvidence(
                completion_state=cast(str, report.completion_state),
                evidence_references=report.evidence_references,
                actual_read_scopes=report.actual_read_scopes,
                actual_write_scopes=report.actual_write_scopes,
                actual_tools=report.actual_tools,
                verification_state=cast(str, report.verification_state),
                external_actions_verified=report.external_actions_verified,
                approval_required_discovered=(
                    report.approval_required_discovered
                    or report.controlled_outcome == "ELEVATE_FOR_APPROVAL"
                ),
                failure_reason=report.failure_reason,
            )
            if (
                report.controlled_outcome == "REPORT_AND_HOLD"
                and evidence.completion_state == "completed"
            ):
                evidence = replace(
                    evidence,
                    completion_state="partial",
                    failure_reason=report.failure_reason
                    or "Worker reported REPORT_AND_HOLD.",
                )

        outcome = self.receiver.finalize(
            resolved.assignment, resolved.profile, evidence
        )
        consistent = outcome.outcome == report.controlled_outcome
        return WorkerResponseReconciliation(
            run_id=advisory.run_id,
            state=(
                "accepted"
                if outcome.outcome == "IMPLEMENT"
                else "elevated"
                if outcome.outcome == "ELEVATE_FOR_APPROVAL"
                else "held"
            ),
            controlled_outcome=outcome.outcome,
            reported_outcome=report.controlled_outcome,
            reason=outcome.reason,
            report_consistent=consistent,
            hq_review_required=(
                outcome.outcome == "IMPLEMENT"
                and advisory.verification_mode == "IMMEDIATE_HQ"
            ),
        )


__all__ = [
    "WORKER_REPORT_PREFIX",
    "WorkerResponseReceiver",
    "WorkerResponseReconciliation",
    "parse_worker_execution_report",
]
