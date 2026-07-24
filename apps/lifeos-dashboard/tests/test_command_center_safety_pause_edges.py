from pathlib import Path

import pytest

import lifeos_dashboard.command_center_safety_pause_runtime  # noqa: F401
from lifeos_dashboard import worker_operations
from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_command_center import WorkerCommandJob
from lifeos_dashboard.worker_operations import BrowserWorkerCommandCenter
from lifeos_dashboard.worker_runtime import ExecutionEnvelope, WorkerRegistryEntry


def _job() -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=ExecutionEnvelope(
            wrapper_id="WRAP-SAFETY-EDGE-1",
            run_id="RUN-SAFETY-EDGE-1",
            worker_id="synthetic_worker",
            task_id="TASK-SAFETY-EDGE-1",
            task_revision=1,
            procedure_id="synthetic_safety_edge",
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
        conversation_url=(
            "https://chatgpt.com/c/00000000-0000-0000-0000-000000000002"
        ),
        route_revision=1,
    )


def _center(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[CommandCenterService, BrowserWorkerCommandCenter]:
    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    center = BrowserWorkerCommandCenter(service)
    monkeypatch.setattr(
        center.runtime,
        "validate_envelope",
        lambda _envelope: _entry(),
    )
    monkeypatch.setattr(
        center.history,
        "successful_send_exists",
        lambda _key: False,
    )
    return service, center


def test_scheduler_start_occurs_after_pause_store_exists(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observations: list[bool] = []

    def fake_start_scheduler(service: CommandCenterService) -> None:
        observations.append(hasattr(service, "safety_pause_store"))

    monkeypatch.setattr(
        CommandCenterService,
        "start_scheduler",
        fake_start_scheduler,
    )

    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
        start_scheduler=True,
    )

    assert observations == [True]
    assert service.pause_state()["pause_kind"] == "none"


def test_confirmed_send_evidence_failure_trips_before_unlock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _center(tmp_path, monkeypatch)
    job = _job()

    def successful_transport(*_args, **_kwargs):
        result = worker_operations._base_result(
            job,
            "Synthetic_Worker",
            trigger="manual",
            status="succeeded",
            exit_code=0,
            started_at=1.0,
            stdout="",
            stderr="",
            reason=(
                "Worker wake submitted and correlated. Courier returned to HQ and released "
                "the gate."
            ),
        )
        return result, object()

    def fail_history(_result) -> None:
        raise RuntimeError("Synthetic evidence persistence failure.")

    monkeypatch.setattr(
        worker_operations,
        "run_worker_browser_transport",
        successful_transport,
    )
    monkeypatch.setattr(center.history, "record", fail_history)

    with pytest.raises(RuntimeError, match="evidence persistence failure"):
        center.execute(job)

    assert service.paused is True
    assert "could not be persisted" in str(service.pause_state()["reason"])
    assert service.running is False


def test_unclassified_transport_exception_trips_pause(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _center(tmp_path, monkeypatch)
    job = _job()

    def broken_transport(*_args, **_kwargs):
        raise RuntimeError("Synthetic unclassified transport failure.")

    monkeypatch.setattr(
        worker_operations,
        "run_worker_browser_transport",
        broken_transport,
    )

    with pytest.raises(RuntimeError, match="unclassified transport failure"):
        center.execute(job)

    assert service.paused is True
    assert "unclassified exception" in str(service.pause_state()["reason"])
    assert service.running is False
