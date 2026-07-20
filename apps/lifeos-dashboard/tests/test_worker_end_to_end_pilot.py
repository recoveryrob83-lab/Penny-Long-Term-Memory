import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard import worker_command_center
from lifeos_dashboard.worker_command_center import (
    WorkerCommandCenterService,
    WorkerCommandJob,
    WorkerExecutionResult,
    render_worker_prompt,
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
    copied_text_contains_wrapper,
    resolve_worker_by_title,
)
from lifeos_dashboard.worker_verification import WorkerVerificationService


@dataclass
class FakeTransport:
    status: str = "succeeded"
    composer_contains_wrapper: bool = True
    reported_wrapper_id: str | None = None
    calls: int = 0

    def __call__(
        self,
        job: WorkerCommandJob,
        entry: WorkerRegistryEntry,
        app_root: Path,
        *,
        trigger: str,
        timeout_seconds: int = 120,
    ) -> WorkerExecutionResult:
        del app_root, timeout_seconds
        self.calls += 1
        started_at = time.time()
        rendered = render_worker_prompt(job.envelope, job.instruction)
        observed = rendered if self.composer_contains_wrapper else "Synthetic composer text without marker."
        marker_verified = copied_text_contains_wrapper(observed, job.envelope.wrapper_id)
        succeeded = self.status == "succeeded" and marker_verified
        return WorkerExecutionResult(
            status="succeeded" if succeeded else "failed",
            destination=entry.chat_title,
            mode=job.mode,
            exit_code=0 if succeeded else 1,
            started_at=started_at,
            finished_at=time.time(),
            stdout=observed,
            stderr="" if succeeded else "Synthetic wrapper verification failed.",
            reason=(
                "Worker transport completed successfully."
                if succeeded
                else "Synthetic Worker transport failed closed."
            ),
            trigger=trigger,  # type: ignore[arg-type]
            wrapper_id=self.reported_wrapper_id or job.envelope.wrapper_id,
            run_id=job.envelope.run_id,
            worker_id=job.envelope.worker_id,
            task_id=job.envelope.task_id,
            task_revision=job.envelope.task_revision,
            procedure_id=job.envelope.procedure_id,
            procedure_version=job.envelope.procedure_version,
            authorization_source=job.envelope.authorization_source,
            idempotency_key=job.envelope.idempotency_key,
            verification_mode=job.envelope.verification_mode,
        )


@dataclass
class SyntheticPilot:
    database: Path
    worker_center: WorkerCommandCenterService
    receiver: WorkerReceiverService
    verification: WorkerVerificationService
    transport: FakeTransport
    entry: WorkerRegistryEntry
    profile: WorkerAuthorityProfile
    procedure: CanonicalProcedureSpec


def synthetic_entry(**overrides: object) -> WorkerRegistryEntry:
    values: dict[str, object] = {
        "worker_id": "synthetic_worker",
        "chat_title": "Synthetic_Worker",
        "owning_department": "engineering",
        "profile_path": "projects/engineering/workers/synthetic_pilot.md",
        "profile_version": 1,
        "specialization": "synthetic_package_d_pilot",
    }
    values.update(overrides)
    return WorkerRegistryEntry.from_dict(values)


def synthetic_profile(**overrides: object) -> WorkerAuthorityProfile:
    values: dict[str, object] = {
        "worker_id": "synthetic_worker",
        "owning_department": "engineering",
        "profile_version": 1,
        "allowed_task_classes": ("synthetic_write",),
        "read_scope_prefixes": ("synthetic/read",),
        "write_scope_prefixes": ("synthetic/write",),
        "approved_tools": ("FakeTransport", "SyntheticStore"),
        "calling_source_task_classes": {
            "SYNTHETIC-PILOT": ("synthetic_write",),
        },
        "allowed_verification_modes": ("ROUTINE_BATCH",),
        "prohibited_task_classes": ("real_world_write",),
    }
    values.update(overrides)
    return WorkerAuthorityProfile(**values)  # type: ignore[arg-type]


def synthetic_procedure(**overrides: object) -> CanonicalProcedureSpec:
    values: dict[str, object] = {
        "procedure_id": "synthetic_write",
        "procedure_version": 1,
        "task_class": "synthetic_write",
        "canonical_text": "Write one synthetic value to disposable pilot state and preserve evidence.",
        "parameter_schema": {"value": "string"},
        "required_parameters": ("value",),
        "allowed_authorization_classes": ("BOUNDED_WRITE",),
        "required_verification_mode": "ROUTINE_BATCH",
        "approved_tools": ("FakeTransport", "SyntheticStore"),
    }
    values.update(overrides)
    return CanonicalProcedureSpec(**values)  # type: ignore[arg-type]


def synthetic_envelope(**overrides: object) -> ExecutionEnvelope:
    values: dict[str, object] = {
        "wrapper_id": "SYNTH-WRAP-1",
        "run_id": "SYNTH-RUN-1",
        "worker_id": "synthetic_worker",
        "task_id": "SYNTH-TASK-1",
        "task_revision": 1,
        "procedure_id": "synthetic_write",
        "procedure_version": 1,
        "authorization_source": "SYNTHETIC-PILOT",
        "verification_mode": "ROUTINE_BATCH",
    }
    values.update(overrides)
    return ExecutionEnvelope.from_dict(values)


def synthetic_assignment(
    active_procedure: CanonicalProcedureSpec,
    *,
    envelope: ExecutionEnvelope | None = None,
    **overrides: object,
) -> ReceiverAssignment:
    parameters = {"value": "synthetic-result"}
    values: dict[str, object] = {
        "envelope": envelope or synthetic_envelope(),
        "target_department": "engineering",
        "task_class": "synthetic_write",
        "authorization_class": "BOUNDED_WRITE",
        "procedure_checksum": active_procedure.checksum,
        "parameters": parameters,
        "parameters_checksum": checksum_parameters(parameters),
        "source_references": ("SYNTHETIC-PILOT",),
        "requested_read_scopes": ("synthetic/read/input",),
        "requested_write_scopes": ("synthetic/write/output",),
        "requested_tools": ("FakeTransport", "SyntheticStore"),
    }
    values.update(overrides)
    return ReceiverAssignment(**values)  # type: ignore[arg-type]


def build_pilot(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    transport: FakeTransport | None = None,
) -> SyntheticPilot:
    database = tmp_path / "synthetic-package-d.sqlite3"
    command_center = CommandCenterService(tmp_path, database_path=database)
    worker_center = WorkerCommandCenterService(command_center)
    active_transport = transport or FakeTransport()
    monkeypatch.setattr(worker_command_center, "run_worker_job", active_transport)
    entry = synthetic_entry()
    worker_center.runtime.register_worker(entry)
    worker_center.runtime.set_route_state(entry.worker_id, "available")
    return SyntheticPilot(
        database=database,
        worker_center=worker_center,
        receiver=WorkerReceiverService(database),
        verification=WorkerVerificationService(database),
        transport=active_transport,
        entry=entry,
        profile=synthetic_profile(),
        procedure=synthetic_procedure(),
    )


def execute_transport(
    pilot: SyntheticPilot,
    envelope: ExecutionEnvelope | None = None,
) -> WorkerExecutionResult:
    return pilot.worker_center.execute(
        WorkerCommandJob(
            envelope=envelope or synthetic_envelope(),
            instruction="Execute only the synthetic disposable assignment.",
            mode="send",
            confirm_send=True,
        )
    )


def history_rows(database: Path) -> list[sqlite3.Row]:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        return connection.execute("SELECT * FROM execution_history ORDER BY id").fetchall()


def test_zero_exact_title_match_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)

    with pytest.raises(WorkerRuntimeError, match="No Worker matches exact chat title"):
        pilot.worker_center.runtime.resolve_title("Missing_Synthetic_Worker")


def test_duplicate_exact_title_match_fails_closed() -> None:
    entries = [
        synthetic_entry(),
        synthetic_entry(
            worker_id="synthetic_worker_two",
            profile_path="projects/engineering/workers/synthetic_pilot_two.md",
        ),
    ]

    with pytest.raises(WorkerRuntimeError, match="Multiple Workers match exact chat title"):
        resolve_worker_by_title(entries, "Synthetic_Worker")


def test_paused_worker_refuses_before_transport(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)
    pilot.worker_center.runtime.set_deployment_state("synthetic_worker", "paused")

    result = execute_transport(pilot)

    assert result.status == "refused"
    assert "paused" in result.reason
    assert pilot.transport.calls == 0


def test_unavailable_route_refuses_before_transport(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)
    pilot.worker_center.runtime.set_route_state("synthetic_worker", "unavailable")

    result = execute_transport(pilot)

    assert result.status == "refused"
    assert "unavailable" in result.reason
    assert pilot.transport.calls == 0


def test_missing_wrapper_marker_fails_transport_and_is_not_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(
        tmp_path,
        monkeypatch,
        transport=FakeTransport(composer_contains_wrapper=False),
    )
    active_assignment = synthetic_assignment(pilot.procedure)

    transport = execute_transport(pilot)
    preflight = pilot.receiver.receive(active_assignment, pilot.profile, pilot.procedure)

    assert transport.status == "failed"
    assert preflight.status == "REPORT_AND_HOLD"
    assert "transport status" in " ".join(preflight.reasons)
    assert pilot.receiver.runtime.store.receiver_state("synthetic_worker", "SYNTH-TASK-1") is None
    assert history_rows(pilot.database)[0]["controlled_outcome"] is None


def test_receiver_rejects_corrupted_successful_wrapper_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(
        tmp_path,
        monkeypatch,
        transport=FakeTransport(reported_wrapper_id="CORRUPTED-WRAPPER"),
    )
    active_assignment = synthetic_assignment(pilot.procedure)

    transport = execute_transport(pilot)
    preflight = pilot.receiver.receive(active_assignment, pilot.profile, pilot.procedure)

    assert transport.status == "succeeded"
    assert preflight.status == "REPORT_AND_HOLD"
    assert "wrapper_id" in " ".join(preflight.reasons)
    assert pilot.receiver.runtime.store.receiver_state("synthetic_worker", "SYNTH-TASK-1") is None


def test_unauthorized_scope_records_hold_without_consuming_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)
    active_assignment = synthetic_assignment(
        pilot.procedure,
        requested_write_scopes=("real/write/outside-authority",),
    )

    assert execute_transport(pilot).status == "succeeded"
    preflight = pilot.receiver.receive(active_assignment, pilot.profile, pilot.procedure)

    assert preflight.status == "REPORT_AND_HOLD"
    assert "write scope" in " ".join(preflight.reasons)
    assert pilot.receiver.runtime.store.receiver_state("synthetic_worker", "SYNTH-TASK-1") is None
    verification = pilot.verification.status()
    assert verification["summary"]["rejected"] == 1
    assert verification["records"][0]["wake_target"] == "engineering"


def test_successful_pilot_reaches_verified_same_row_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)
    active_assignment = synthetic_assignment(pilot.procedure)

    transport = execute_transport(pilot)
    preflight = pilot.receiver.receive(active_assignment, pilot.profile, pilot.procedure)
    outcome = pilot.receiver.finalize(
        active_assignment,
        pilot.profile,
        ExecutionEvidence(
            completion_state="completed",
            evidence_references=("synthetic://evidence/SYNTH-RUN-1",),
            actual_read_scopes=("synthetic/read/input",),
            actual_write_scopes=("synthetic/write/output",),
            actual_tools=("FakeTransport", "SyntheticStore"),
            verification_state="pending",
            external_actions_verified=True,
        ),
    )
    pending = pilot.verification.status()
    reviewed = pilot.verification.review(
        "SYNTH-RUN-1",
        "verified",
        actor="Engineering HQ synthetic pilot",
        reason="Disposable evidence and postconditions were read back.",
    )
    final = pilot.verification.status()

    assert transport.status == "succeeded"
    assert preflight.status == "READY"
    assert outcome.outcome == "IMPLEMENT"
    assert pending["summary"]["routine_queue"] == 1
    assert pending["summary"]["wake_required"] == 0
    assert reviewed.verification_state == "verified"
    assert final["summary"] == {
        "total": 1,
        "pending": 0,
        "verified": 1,
        "rejected": 0,
        "routine_queue": 0,
        "wake_required": 0,
        "wake_suppressed": 1,
    }
    rows = history_rows(pilot.database)
    assert len(rows) == 1
    assert rows[0]["controlled_outcome"] == "IMPLEMENT"
    assert rows[0]["receiver_evidence_json"] == '["synthetic://evidence/SYNTH-RUN-1"]'
    assert rows[0]["receiver_verification_state"] == "pending"
    assert rows[0]["worker_verification_state"] == "verified"


def test_duplicate_retry_with_new_run_id_never_reaches_transport(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)
    first_assignment = synthetic_assignment(pilot.procedure)

    assert execute_transport(pilot).status == "succeeded"
    assert pilot.receiver.receive(first_assignment, pilot.profile, pilot.procedure).status == "READY"
    pilot.receiver.finalize(
        first_assignment,
        pilot.profile,
        ExecutionEvidence(
            completion_state="completed",
            evidence_references=("synthetic://evidence/first",),
            actual_read_scopes=("synthetic/read/input",),
            actual_write_scopes=("synthetic/write/output",),
            actual_tools=("FakeTransport", "SyntheticStore"),
            verification_state="pending",
        ),
    )
    retry_envelope = synthetic_envelope(
        wrapper_id="SYNTH-WRAP-RETRY",
        run_id="SYNTH-RUN-RETRY",
    )

    retry = execute_transport(pilot, retry_envelope)

    assert retry.status == "refused"
    assert "stale or already processed" in retry.reason
    assert pilot.transport.calls == 1
    rows = history_rows(pilot.database)
    assert sum(row["status"] == "succeeded" and row["mode"] == "send" for row in rows) == 1
    assert sum(row["controlled_outcome"] == "IMPLEMENT" for row in rows) == 1


def test_second_controlled_outcome_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pilot = build_pilot(tmp_path, monkeypatch)
    active_assignment = synthetic_assignment(pilot.procedure)
    evidence = ExecutionEvidence(
        completion_state="completed",
        evidence_references=("synthetic://evidence/once",),
        actual_read_scopes=("synthetic/read/input",),
        actual_write_scopes=("synthetic/write/output",),
        actual_tools=("FakeTransport", "SyntheticStore"),
        verification_state="pending",
    )

    assert execute_transport(pilot).status == "succeeded"
    assert pilot.receiver.receive(active_assignment, pilot.profile, pilot.procedure).status == "READY"
    assert pilot.receiver.finalize(active_assignment, pilot.profile, evidence).outcome == "IMPLEMENT"

    with pytest.raises(WorkerRuntimeError, match="already has a controlled outcome"):
        pilot.receiver.finalize(active_assignment, pilot.profile, evidence)
