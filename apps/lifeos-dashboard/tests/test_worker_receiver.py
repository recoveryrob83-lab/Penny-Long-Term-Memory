import sqlite3
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import (
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_receiver import (
    CanonicalProcedureSpec,
    ExecutionEvidence,
    ReceiverAssignment,
    WorkerAuthorityProfile,
    WorkerReceiverService,
    checksum_parameters,
)
from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerRegistryEntry,
    WorkerRuntimeError,
)
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService


def envelope(**overrides: object) -> ExecutionEnvelope:
    values: dict[str, object] = {
        "wrapper_id": "WRAP-1",
        "run_id": "RUN-1",
        "worker_id": "office_leaks_worker",
        "task_id": "ADV-1",
        "task_revision": 1,
        "procedure_id": "lead_cleanup",
        "procedure_version": 1,
        "authorization_source": "Chief of Staff HQ",
        "verification_mode": "ROUTINE_BATCH",
    }
    values.update(overrides)
    return ExecutionEnvelope.from_dict(values)


def registry_entry(**overrides: object) -> WorkerRegistryEntry:
    values: dict[str, object] = {
        "worker_id": "office_leaks_worker",
        "chat_title": "OfficeLeaks_Worker",
        "owning_department": "office-leaks-consulting",
        "profile_path": "projects/office-leaks-consulting/workers/general.md",
        "profile_version": 1,
    }
    values.update(overrides)
    return WorkerRegistryEntry.from_dict(values)


def profile(**overrides: object) -> WorkerAuthorityProfile:
    values: dict[str, object] = {
        "worker_id": "office_leaks_worker",
        "owning_department": "office-leaks-consulting",
        "profile_version": 1,
        "allowed_task_classes": ("lead_cleanup",),
        "read_scope_prefixes": ("projects/office-leaks-consulting", "gmail:"),
        "write_scope_prefixes": ("projects/office-leaks-consulting",),
        "approved_tools": ("GitHub", "Gmail"),
        "calling_source_task_classes": {
            "Chief of Staff HQ": ("lead_cleanup",),
            "Office Leaks HQ": ("lead_cleanup",),
        },
        "allowed_verification_modes": ("ROUTINE_BATCH", "IMMEDIATE_HQ", "AUTOMATIC"),
        "prohibited_task_classes": ("strategy",),
    }
    values.update(overrides)
    return WorkerAuthorityProfile(**values)  # type: ignore[arg-type]


def procedure(**overrides: object) -> CanonicalProcedureSpec:
    values: dict[str, object] = {
        "procedure_id": "lead_cleanup",
        "procedure_version": 1,
        "task_class": "lead_cleanup",
        "canonical_text": "Clean one authorized lead record and preserve evidence.",
        "parameter_schema": {"lead_id": "string", "archive": "boolean"},
        "required_parameters": ("lead_id",),
        "allowed_authorization_classes": ("READ_ONLY", "BOUNDED_WRITE"),
        "required_verification_mode": "ROUTINE_BATCH",
        "approved_tools": ("GitHub",),
    }
    values.update(overrides)
    return CanonicalProcedureSpec(**values)  # type: ignore[arg-type]


def assignment(**overrides: object) -> ReceiverAssignment:
    active_procedure = procedure()
    params = {"lead_id": "LEAD-1", "archive": True}
    values: dict[str, object] = {
        "envelope": envelope(),
        "target_department": "office-leaks-consulting",
        "task_class": "lead_cleanup",
        "authorization_class": "BOUNDED_WRITE",
        "procedure_checksum": active_procedure.checksum,
        "parameters": params,
        "parameters_checksum": checksum_parameters(params),
        "source_references": ("ADV-1",),
        "requested_read_scopes": ("projects/office-leaks-consulting/leads/LEAD-1.md",),
        "requested_write_scopes": ("projects/office-leaks-consulting/leads/LEAD-1.md",),
        "requested_tools": ("GitHub",),
    }
    values.update(overrides)
    return ReceiverAssignment(**values)  # type: ignore[arg-type]


def transport_result(active_envelope: ExecutionEnvelope) -> WorkerExecutionResult:
    return WorkerExecutionResult(
        status="succeeded",
        destination="OfficeLeaks_Worker",
        mode="send",
        exit_code=0,
        started_at=1.0,
        finished_at=2.0,
        stdout="Wrapper delivered.",
        stderr="",
        reason="Worker transport completed successfully.",
        trigger="manual",
        wrapper_id=active_envelope.wrapper_id,
        run_id=active_envelope.run_id,
        worker_id=active_envelope.worker_id,
        task_id=active_envelope.task_id,
        task_revision=active_envelope.task_revision,
        procedure_id=active_envelope.procedure_id,
        procedure_version=active_envelope.procedure_version,
        authorization_source=active_envelope.authorization_source,
        idempotency_key=active_envelope.idempotency_key,
        verification_mode=active_envelope.verification_mode,
    )


def receiver(
    tmp_path: Path, active_assignment: ReceiverAssignment | None = None
) -> WorkerReceiverService:
    active_assignment = active_assignment or assignment()
    database = tmp_path / "command-center.sqlite3"
    runtime = WorkerRuntimeService(database)
    runtime.register_worker(registry_entry())
    runtime.set_route_state("office_leaks_worker", "available")
    WorkerExecutionHistoryStore(database).record(transport_result(active_assignment.envelope))
    return WorkerReceiverService(database)


def history_row(database: Path, run_id: str = "RUN-1") -> sqlite3.Row:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM execution_history WHERE run_id = ?", (run_id,)
        ).fetchone()
    assert row is not None
    return row


def test_valid_assignment_is_accepted_only_after_semantic_validation(tmp_path: Path) -> None:
    service = receiver(tmp_path)
    result = service.receive(assignment(), profile(), procedure())

    assert result.status == "READY"
    assert result.accepted_at is not None
    state = service.runtime.store.receiver_state("office_leaks_worker", "ADV-1")
    assert state is not None
    assert state.last_processed_revision == 1
    row = history_row(tmp_path / "command-center.sqlite3")
    assert row["profile_version"] == 1
    assert row["controlled_outcome"] is None


def test_profile_version_mismatch_reports_hold_without_consuming_revision(tmp_path: Path) -> None:
    service = receiver(tmp_path)
    result = service.receive(assignment(), profile(profile_version=2), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert service.runtime.store.receiver_state("office_leaks_worker", "ADV-1") is None
    assert history_row(tmp_path / "command-center.sqlite3")["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )


def test_wrong_calling_source_reports_hold(tmp_path: Path) -> None:
    active = assignment(envelope=envelope(authorization_source="Unknown HQ"))
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "Calling source" in " ".join(result.reasons)


def test_new_authority_without_approval_elevates(tmp_path: Path) -> None:
    active = assignment(requests_new_authority=True)
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "ELEVATE_FOR_APPROVAL"
    assert service.runtime.store.receiver_state("office_leaks_worker", "ADV-1") is None


def test_approval_reference_allows_preflight_to_continue(tmp_path: Path) -> None:
    active = assignment(
        requests_new_authority=True,
        approval_reference="ROB-APPROVAL-1",
        source_references=("ADV-1", "ROB-APPROVAL-1"),
    )
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "READY"


def test_procedure_checksum_mismatch_reports_hold(tmp_path: Path) -> None:
    active = assignment(procedure_checksum="SHA256:wrong")
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "checksum" in " ".join(result.reasons)


def test_parameter_checksum_and_schema_are_validated(tmp_path: Path) -> None:
    active = assignment(parameters_checksum="SHA256:wrong")
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "Parameter checksum" in " ".join(result.reasons)


def test_missing_required_parameter_reports_hold(tmp_path: Path) -> None:
    params = {"archive": True}
    active = assignment(parameters=params, parameters_checksum=checksum_parameters(params))
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "Required parameters" in " ".join(result.reasons)


def test_read_only_assignment_cannot_request_write_scope(tmp_path: Path) -> None:
    active = assignment(authorization_class="READ_ONLY")
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "READ_ONLY" in " ".join(result.reasons)


def test_scope_and_tool_must_stay_inside_profile_and_procedure(tmp_path: Path) -> None:
    active = assignment(
        requested_write_scopes=("projects/finance/private.md",),
        requested_tools=("Gmail",),
    )
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    reasons = " ".join(result.reasons)
    assert "write scope" in reasons
    assert "canonical procedure" in reasons


def test_missing_source_reference_reports_hold(tmp_path: Path) -> None:
    active = assignment(source_references=())
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "source references" in " ".join(result.reasons)


def test_transport_scope_change_reports_hold(tmp_path: Path) -> None:
    active = assignment(transport_scope_change_detected=True)
    service = receiver(tmp_path, active)
    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "Transport text" in " ".join(result.reasons)


def test_stale_revision_is_held_and_not_reaccepted(tmp_path: Path) -> None:
    first = assignment()
    service = receiver(tmp_path, first)
    assert service.receive(first, profile(), procedure()).status == "READY"

    second_envelope = envelope(run_id="RUN-2")
    second = assignment(envelope=second_envelope)
    WorkerExecutionHistoryStore(tmp_path / "command-center.sqlite3").record(
        transport_result(second_envelope)
    )
    result = service.receive(second, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    state = service.runtime.store.receiver_state("office_leaks_worker", "ADV-1")
    assert state is not None
    assert state.last_run_id == "RUN-1"


def test_completed_routine_batch_work_records_implement(tmp_path: Path) -> None:
    active = assignment()
    service = receiver(tmp_path, active)
    assert service.receive(active, profile(), procedure()).status == "READY"

    outcome = service.finalize(
        active,
        profile(),
        ExecutionEvidence(
            completion_state="completed",
            evidence_references=("github:commit:abc",),
            actual_read_scopes=active.requested_read_scopes,
            actual_write_scopes=active.requested_write_scopes,
            actual_tools=("GitHub",),
            verification_state="pending",
        ),
    )

    assert outcome.outcome == "IMPLEMENT"
    assert history_row(tmp_path / "command-center.sqlite3")["controlled_outcome"] == "IMPLEMENT"


def test_automatic_work_requires_verified_postcondition(tmp_path: Path) -> None:
    auto_envelope = envelope(verification_mode="AUTOMATIC")
    active = assignment(envelope=auto_envelope)
    auto_procedure = procedure(required_verification_mode="AUTOMATIC")
    service = receiver(tmp_path, active)
    assert service.receive(active, profile(), auto_procedure).status == "READY"

    outcome = service.finalize(
        active,
        profile(),
        ExecutionEvidence(
            completion_state="completed",
            evidence_references=("machine:result",),
            verification_state="pending",
        ),
    )

    assert outcome.outcome == "REPORT_AND_HOLD"
    assert "machine postcondition" in outcome.reason


def test_partial_or_unverified_external_work_reports_hold(tmp_path: Path) -> None:
    active = assignment()
    service = receiver(tmp_path, active)
    assert service.receive(active, profile(), procedure()).status == "READY"

    outcome = service.finalize(
        active,
        profile(),
        ExecutionEvidence(
            completion_state="partial",
            evidence_references=("log:partial",),
            verification_state="unavailable",
            external_actions_verified=False,
            failure_reason="Connector returned an ambiguous response.",
        ),
    )

    assert outcome.outcome == "REPORT_AND_HOLD"
    assert "ambiguous response" in outcome.reason


def test_execution_scope_expansion_reports_hold(tmp_path: Path) -> None:
    active = assignment()
    service = receiver(tmp_path, active)
    assert service.receive(active, profile(), procedure()).status == "READY"

    outcome = service.finalize(
        active,
        profile(),
        ExecutionEvidence(
            completion_state="completed",
            evidence_references=("log:1",),
            actual_write_scopes=("projects/office-leaks-consulting/other.md",),
            verification_state="pending",
        ),
    )

    assert outcome.outcome == "REPORT_AND_HOLD"
    assert "exceeded authorization" in outcome.reason


def test_discovered_approval_need_elevates(tmp_path: Path) -> None:
    active = assignment()
    service = receiver(tmp_path, active)
    assert service.receive(active, profile(), procedure()).status == "READY"

    outcome = service.finalize(
        active,
        profile(),
        ExecutionEvidence(
            completion_state="not_attempted",
            evidence_references=("review:1",),
            approval_required_discovered=True,
        ),
    )

    assert outcome.outcome == "ELEVATE_FOR_APPROVAL"


def test_second_outcome_for_same_run_is_refused(tmp_path: Path) -> None:
    active = assignment()
    service = receiver(tmp_path, active)
    assert service.receive(active, profile(), procedure()).status == "READY"
    evidence = ExecutionEvidence(
        completion_state="completed",
        evidence_references=("log:1",),
        verification_state="pending",
    )
    service.finalize(active, profile(), evidence)

    with pytest.raises(WorkerRuntimeError, match="already has a controlled outcome"):
        service.finalize(active, profile(), evidence)


def test_calling_source_must_be_authorized_for_exact_task_class(tmp_path: Path) -> None:
    restricted = profile(
        calling_source_task_classes={"Chief of Staff HQ": ("different_task",)}
    )
    service = receiver(tmp_path)

    result = service.receive(assignment(), restricted, procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "may not request this task class" in " ".join(result.reasons)


def test_approval_reference_must_be_in_authoritative_sources(tmp_path: Path) -> None:
    active = assignment(
        requests_new_authority=True,
        approval_reference="ROB-APPROVAL-1",
    )
    service = receiver(tmp_path, active)

    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    assert "Approval reference" in " ".join(result.reasons)


def test_unknown_and_wrong_type_parameters_report_hold(tmp_path: Path) -> None:
    params = {"lead_id": 7, "archive": True, "surprise": "scope drift"}
    active = assignment(
        parameters=params,
        parameters_checksum=checksum_parameters(params),
    )
    service = receiver(tmp_path, active)

    result = service.receive(active, profile(), procedure())

    assert result.status == "REPORT_AND_HOLD"
    reasons = " ".join(result.reasons)
    assert "Unknown parameters" in reasons
    assert "must be string" in reasons
