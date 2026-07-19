import importlib.util
import threading
from dataclasses import replace
from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService, ExecutionResult
from lifeos_dashboard.worker_command_center import (
    WorkerCommandCenterService,
    WorkerCommandJob,
    WorkerExecutionResult,
    build_worker_command,
    render_worker_prompt,
)
from lifeos_dashboard.worker_runtime import ExecutionEnvelope, WorkerRegistryEntry, WorkerRuntimeError


APP_ROOT = Path("C:/LifeOS/apps/lifeos-dashboard")


def entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="office_leaks_worker",
        chat_title="OfficeLeaks_Worker",
        owning_department="office-leaks-consulting",
        profile_path="projects/office-leaks-consulting/workers/general.md",
        profile_version=1,
    )


def envelope(**overrides: object) -> ExecutionEnvelope:
    values: dict[str, object] = {
        "wrapper_id": "WRAP-20260719-001",
        "run_id": "RUN-20260719-001",
        "worker_id": "office_leaks_worker",
        "task_id": "ADV-20260719-044",
        "task_revision": 1,
        "procedure_id": "maintenance_reconcile",
        "procedure_version": 1,
        "authorization_source": "Rob via Engineering HQ",
        "verification_mode": "IMMEDIATE_HQ",
    }
    values.update(overrides)
    return ExecutionEnvelope.from_dict(values)


def job(**overrides: object) -> WorkerCommandJob:
    values: dict[str, object] = {
        "envelope": envelope(),
        "instruction": "Read the authoritative advisory and execute only its bounded scope.",
        "mode": "draft",
        "confirm_send": False,
    }
    values.update(overrides)
    return WorkerCommandJob(**values)  # type: ignore[arg-type]


def service(tmp_path: Path) -> WorkerCommandCenterService:
    command_center = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    worker = WorkerCommandCenterService(command_center)
    worker.runtime.register_worker(entry())
    worker.runtime.set_route_state("office_leaks_worker", "available")
    return worker


def successful_result(
    worker_job: WorkerCommandJob,
    *,
    trigger: str = "manual",
) -> WorkerExecutionResult:
    active_entry = entry()
    active_envelope = worker_job.envelope
    return WorkerExecutionResult(
        status="succeeded",
        destination=active_entry.chat_title,
        mode=worker_job.mode,
        exit_code=0,
        started_at=1.0,
        finished_at=2.0,
        stdout="Worker transport completed.",
        stderr="",
        reason="Worker transport completed successfully.",
        trigger=trigger,  # type: ignore[arg-type]
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


def test_worker_prompt_contains_compact_wrapper_and_instruction() -> None:
    rendered = render_worker_prompt(envelope(), "Do the bounded work.")

    assert rendered.startswith("LIFEOS_EXECUTION_WRAPPER={")
    assert '"wrapper_id":"WRAP-20260719-001"' in rendered
    assert rendered.endswith("Do the bounded work.")


def test_worker_command_uses_exact_title_and_wrapper_marker() -> None:
    command = build_worker_command(job(), entry(), APP_ROOT)

    assert "OfficeLeaks_Worker" in command
    assert "open_worker_chat_group_verified.py" in " ".join(command)
    marker_index = command.index("--verify-marker")
    assert command[marker_index + 1] == "WRAP-20260719-001"
    assert "--send" not in command


def test_worker_send_requires_explicit_confirmation() -> None:
    with pytest.raises(WorkerRuntimeError, match="explicit confirmation"):
        job(mode="send", confirm_send=False)


def test_worker_history_columns_do_not_break_legacy_history(tmp_path: Path) -> None:
    command_center = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    command_center.store.add_history(
        ExecutionResult(
            status="succeeded",
            destination="hub",
            mode="draft",
            prompt_type="custom",
            exit_code=0,
            started_at=1.0,
            finished_at=2.0,
            stdout="Legacy run.",
            stderr="",
            reason="Completed successfully.",
        ).to_dict()
    )

    WorkerCommandCenterService(command_center)

    assert command_center.store.history()[0]["destination"] == "hub"


def test_successful_manual_worker_run_records_envelope_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker = service(tmp_path)

    def fake_run(worker_job, active_entry, app_root, *, trigger, timeout_seconds):
        del active_entry, app_root, timeout_seconds
        return successful_result(worker_job, trigger=trigger)

    monkeypatch.setattr(
        "lifeos_dashboard.worker_command_center.run_worker_job",
        fake_run,
    )

    result = worker.execute(job())
    history = worker.history.worker_history()

    assert result.status == "succeeded"
    assert history[0]["wrapper_id"] == "WRAP-20260719-001"
    assert history[0]["worker_id"] == "office_leaks_worker"
    assert history[0]["task_revision"] == 1
    assert history[0]["idempotency_key"] == "office_leaks_worker:ADV-20260719-044:1"
    assert history[0]["trigger"] == "manual"


def test_successful_send_suppresses_same_task_revision_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker = service(tmp_path)
    calls = 0

    def fake_run(worker_job, active_entry, app_root, *, trigger, timeout_seconds):
        nonlocal calls
        del active_entry, app_root, timeout_seconds
        calls += 1
        return successful_result(worker_job, trigger=trigger)

    monkeypatch.setattr(
        "lifeos_dashboard.worker_command_center.run_worker_job",
        fake_run,
    )
    send_job = job(mode="send", confirm_send=True)

    first = worker.execute(send_job)
    second = worker.execute(send_job)

    assert first.status == "succeeded"
    assert second.status == "refused"
    assert "already has a successful send record" in second.reason
    assert calls == 1


def test_failed_send_does_not_block_bounded_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker = service(tmp_path)
    statuses = ["failed", "succeeded"]

    def fake_run(worker_job, active_entry, app_root, *, trigger, timeout_seconds):
        del active_entry, app_root, timeout_seconds
        status = statuses.pop(0)
        result = successful_result(worker_job, trigger=trigger)
        if status == "succeeded":
            return result
        return replace(
            result,
            status="failed",
            exit_code=1,
            reason="Transport stopped safely.",
        )

    monkeypatch.setattr(
        "lifeos_dashboard.worker_command_center.run_worker_job",
        fake_run,
    )
    send_job = job(mode="send", confirm_send=True)

    assert worker.execute(send_job).status == "failed"
    assert worker.execute(send_job).status == "succeeded"


def test_scheduled_adapter_records_scheduled_trigger(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker = service(tmp_path)

    def fake_run(worker_job, active_entry, app_root, *, trigger, timeout_seconds):
        del active_entry, app_root, timeout_seconds
        return successful_result(worker_job, trigger=trigger)

    monkeypatch.setattr(
        "lifeos_dashboard.worker_command_center.run_worker_job",
        fake_run,
    )

    result = worker.execute_scheduled(job())

    assert result.trigger == "scheduled"
    assert worker.history.worker_history()[0]["trigger"] == "scheduled"


def test_unavailable_worker_route_refuses_before_transport(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    worker = service(tmp_path)
    worker.runtime.set_route_state("office_leaks_worker", "unavailable")

    def should_not_run(*args, **kwargs):
        raise AssertionError("transport should not run")

    monkeypatch.setattr(
        "lifeos_dashboard.worker_command_center.run_worker_job",
        should_not_run,
    )

    result = worker.execute(job())

    assert result.status == "refused"
    assert "execution must hold" in result.reason


def test_worker_path_shares_command_center_one_job_lock(tmp_path: Path) -> None:
    worker = service(tmp_path)
    lock: threading.Lock = worker.command_center._run_lock  # noqa: SLF001
    lock.acquire()
    try:
        result = worker.execute(job())
    finally:
        lock.release()

    assert result.status == "refused"
    assert "Another automation job is running" in result.reason


def test_worker_marker_cli_requires_exactly_one_marker() -> None:
    script = Path(__file__).parents[1] / "automation" / "open_worker_chat_group_verified.py"
    spec = importlib.util.spec_from_file_location("worker_marker_cli", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    marker, forwarded = module.extract_verify_marker(
        ["worker.py", "OfficeLeaks_Worker", "--verify-marker", "WRAP-1", "--send"]
    )

    assert marker == "WRAP-1"
    assert forwarded == ["worker.py", "OfficeLeaks_Worker", "--send"]
    with pytest.raises(ValueError, match="requires --verify-marker"):
        module.extract_verify_marker(["worker.py", "OfficeLeaks_Worker"])
