from pathlib import Path

import pytest

import lifeos_dashboard.command_center_safety_pause_runtime  # noqa: F401
from lifeos_dashboard import worker_operations
from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.command_center_safety_pause import safety_pause_reason_for_transport
from lifeos_dashboard.worker_command_center import WorkerCommandJob, WorkerExecutionResult
from lifeos_dashboard.worker_operations import BrowserWorkerCommandCenter
from lifeos_dashboard.worker_runtime import ExecutionEnvelope, WorkerRegistryEntry


def _service(tmp_path: Path) -> CommandCenterService:
    return CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )


def _job() -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=ExecutionEnvelope(
            wrapper_id="WRAP-SAFETY-PAUSE-1",
            run_id="RUN-SAFETY-PAUSE-1",
            worker_id="synthetic_worker",
            task_id="TASK-SAFETY-PAUSE-1",
            task_revision=1,
            procedure_id="synthetic_safety_pause",
            procedure_version=1,
            authorization_source="TEST-ONLY",
            verification_mode="IMMEDIATE_HQ",
        ),
        instruction="Synthetic test only. Create no durable authority.",
        mode="send",
        confirm_send=True,
    )


def _entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="synthetic_worker",
        chat_title="Synthetic_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/synthetic_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/c/00000000-0000-0000-0000-000000000001",
        route_revision=1,
    )


def _result(
    job: WorkerCommandJob,
    *,
    status: str,
    exit_code: int | None,
    stderr: str,
    reason: str,
) -> WorkerExecutionResult:
    return worker_operations._base_result(  # noqa: SLF001 - focused transport harness
        job,
        "Synthetic_Worker",
        trigger="manual",
        status=status,
        exit_code=exit_code,
        started_at=1.0,
        stdout="",
        stderr=stderr,
        reason=reason,
    )


def _prepared_center(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[CommandCenterService, BrowserWorkerCommandCenter]:
    service = _service(tmp_path)
    center = BrowserWorkerCommandCenter(service)
    monkeypatch.setattr(center.runtime, "validate_envelope", lambda _envelope: _entry())
    monkeypatch.setattr(center.history, "successful_send_exists", lambda _key: False)
    monkeypatch.setattr(center.browser_evidence, "attach", lambda _run_id, _evidence: None)
    return service, center


def test_safety_pause_persists_and_requires_explicit_resume(tmp_path: Path) -> None:
    first = _service(tmp_path)
    state = first.trip_safety_pause(
        reason="Submission could not be reconciled.",
        affected_run_id="RUN-SAFETY-PAUSE-1",
        trigger="worker_browser_transport",
    )

    second = _service(tmp_path)

    assert state["paused"] is True
    assert second.paused is True
    assert second.pause_state()["pause_kind"] == "safety"
    assert second.pause_state()["affected_run_id"] == "RUN-SAFETY-PAUSE-1"

    first.set_paused(True)
    assert second.pause_state()["reason"] == "Submission could not be reconciled."

    second.set_paused(False)
    assert first.paused is False
    assert first.pause_state()["pause_kind"] == "none"


def test_manual_pause_uses_the_same_persisted_record(tmp_path: Path) -> None:
    first = _service(tmp_path)
    first.set_paused(True)

    second = _service(tmp_path)

    assert second.paused is True
    assert second.pause_state()["pause_kind"] == "manual"
    assert second.status()["pause"]["trigger"] == "manual"


@pytest.mark.parametrize(
    ("exit_code", "stderr", "reason", "claimed_success", "should_trip"),
    [
        (3, "STOPPED_AFTER_SEND: uncertain", "", False, True),
        (None, "", "Submission state may be uncertain; inspect before retry.", False, True),
        (0, "", "Receipt marker mismatch.", True, True),
        (0, "", "Courier could not verify return to HQ.", False, True),
        (2, "STOPPED: exact draft preserved", "Safe pre-send refusal.", False, False),
        (2, "", "Unknown Worker route; nothing was sent.", False, False),
    ],
)
def test_transport_classifier_is_conservative(
    exit_code: int | None,
    stderr: str,
    reason: str,
    claimed_success: bool,
    should_trip: bool,
) -> None:
    pause_reason = safety_pause_reason_for_transport(
        exit_code=exit_code,
        stderr=stderr,
        reason=reason,
        claimed_success_without_valid_receipt=claimed_success,
    )

    assert (pause_reason is not None) is should_trip


def test_worker_uncertainty_trips_before_execute_returns(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch)
    job = _job()

    def uncertain_transport(*_args, **_kwargs):
        return (
            _result(
                job,
                status="failed",
                exit_code=3,
                stderr="STOPPED_AFTER_SEND: strict witness missing",
                reason="Browser courier stopped after submission uncertainty.",
            ),
            object(),
        )

    monkeypatch.setattr(worker_operations, "run_worker_browser_transport", uncertain_transport)

    result = center.execute(job)

    assert result.status == "failed"
    assert service.paused is True
    assert service.pause_state()["affected_run_id"] == job.envelope.run_id
    assert service.pause_state()["trigger"] == "worker_browser_transport"
    assert service.running is False


def test_confirmed_send_with_unknown_return_state_trips_pause(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch)
    job = _job()

    def unknown_return_transport(*_args, **_kwargs):
        return (
            _result(
                job,
                status="succeeded",
                exit_code=0,
                stderr="",
                reason=(
                    "Worker wake submitted and correlated. The courier could not verify return "
                    "to HQ; inspect the browser before another wake."
                ),
            ),
            object(),
        )

    monkeypatch.setattr(worker_operations, "run_worker_browser_transport", unknown_return_transport)

    result = center.execute(job)

    assert result.status == "succeeded"
    assert service.paused is True
    assert "verified source state" in str(service.pause_state()["reason"])


def test_deterministic_presend_failure_does_not_trip_global_pause(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch)
    job = _job()

    def safe_refusal_transport(*_args, **_kwargs):
        return (
            _result(
                job,
                status="failed",
                exit_code=2,
                stderr="STOPPED: exact draft preserved",
                reason="Browser courier stopped safely before a confirmed dispatch completed.",
            ),
            object(),
        )

    monkeypatch.setattr(worker_operations, "run_worker_browser_transport", safe_refusal_transport)

    result = center.execute(job)

    assert result.status == "failed"
    assert service.paused is False
    assert service.pause_state()["pause_kind"] == "none"
