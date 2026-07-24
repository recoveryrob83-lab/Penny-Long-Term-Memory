import importlib.util
import json
import sqlite3
from pathlib import Path
from types import ModuleType

import pytest

import lifeos_dashboard.command_center_safety_pause_runtime  # noqa: F401
from lifeos_dashboard import worker_operations
from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.command_center_send_budget import (
    DEFAULT_SEND_BUDGET_LIMIT,
    configured_send_budget_limit,
)
from lifeos_dashboard.worker_command_center import (
    WorkerCommandJob,
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_operations import BrowserWorkerCommandCenter
from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerRegistryEntry,
    WorkerRuntimeError,
)


def _service(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    limit: int = DEFAULT_SEND_BUDGET_LIMIT,
) -> CommandCenterService:
    monkeypatch.setenv("LIFEOS_GLOBAL_SEND_BUDGET_LIMIT", str(limit))
    return CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )


def _job(*, mode: str = "send") -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=ExecutionEnvelope(
            wrapper_id="WRAP-SEND-BUDGET-1",
            run_id="RUN-SEND-BUDGET-1",
            worker_id="synthetic_worker",
            task_id="TASK-SEND-BUDGET-1",
            task_revision=1,
            procedure_id="synthetic_send_budget",
            procedure_version=1,
            authorization_source="TEST-ONLY",
            verification_mode="IMMEDIATE_HQ",
        ),
        instruction="Synthetic test only. Create no durable authority.",
        mode=mode,
        confirm_send=mode == "send",
    )


def _entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="synthetic_worker",
        chat_title="Synthetic_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/synthetic_worker.md",
        profile_version=1,
        conversation_url=(
            "https://chatgpt.com/c/00000000-0000-0000-0000-000000000001"
        ),
        route_revision=1,
    )


def _result(
    job: WorkerCommandJob,
    *,
    status: str = "failed",
    exit_code: int | None = 2,
    reason: str = "Deterministic pre-send stop after transport entry.",
) -> WorkerExecutionResult:
    return worker_operations._base_result(
        job,
        "Synthetic_Worker",
        trigger="manual",
        status=status,
        exit_code=exit_code,
        started_at=1.0,
        stdout="",
        stderr="STOPPED: exact draft preserved",
        reason=reason,
    )


def _prepared_center(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    limit: int = DEFAULT_SEND_BUDGET_LIMIT,
) -> tuple[CommandCenterService, BrowserWorkerCommandCenter]:
    service = _service(tmp_path, monkeypatch, limit=limit)
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
    monkeypatch.setattr(
        center.browser_evidence,
        "attach",
        lambda _run_id, _evidence: None,
    )
    return service, center


def _wake_module() -> ModuleType:
    script = (
        Path(__file__).resolve().parents[1]
        / "automation"
        / "run_worker_hq_review_wake.py"
    )
    spec = importlib.util.spec_from_file_location("test_run_worker_hq_review_budget", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("configured", "expected"),
    [
        (None, DEFAULT_SEND_BUDGET_LIMIT),
        ("1", 1),
        ("20", 20),
    ],
)
def test_configured_send_budget_limit(configured: str | None, expected: int) -> None:
    assert configured_send_budget_limit(configured) == expected


@pytest.mark.parametrize("configured", ["zero", "0", "21", "-1"])
def test_invalid_send_budget_limit_fails_closed(configured: str) -> None:
    with pytest.raises(ValueError):
        configured_send_budget_limit(configured)


def test_budget_persists_and_never_refills_with_time(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first = _service(tmp_path, monkeypatch, limit=2)

    one = first.reserve_send_budget(kind="worker_dispatch", run_id="RUN-1")
    two = first.reserve_send_budget(kind="hq_review_wake", run_id="RUN-1")
    second = _service(tmp_path, monkeypatch, limit=2)
    held = second.reserve_send_budget(kind="worker_dispatch", run_id="RUN-2")

    assert one.reserved is True
    assert one.sequence == 1
    assert two.reserved is True
    assert two.sequence == 2
    assert second.send_budget_state()["used"] == 2
    assert second.send_budget_state()["exhausted"] is True
    assert held.reserved is False
    assert held.state.used == 2
    assert held.state.held_count == 1


def test_budget_reset_requires_pause_and_does_not_resume(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service(tmp_path, monkeypatch, limit=2)
    service.reserve_send_budget(kind="worker_dispatch", run_id="RUN-1")

    with pytest.raises(ValueError, match="explicit confirmation"):
        service.reset_send_budget(confirm_reset=False)
    with pytest.raises(ValueError, match="Pause automation"):
        service.reset_send_budget(confirm_reset=True)

    service.set_paused(True)
    reset = service.reset_send_budget(confirm_reset=True)

    assert reset["epoch"] == 2
    assert reset["used"] == 0
    assert reset["held_operations"]["count"] == 0
    assert service.paused is True


def test_worker_and_hq_reservations_share_one_execution_row(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service(tmp_path, monkeypatch, limit=3)
    history = WorkerExecutionHistoryStore(service.store.database_path)
    job = _job()
    history.record(_result(job))

    worker = service.reserve_send_budget(
        kind="worker_dispatch",
        run_id=job.envelope.run_id,
    )
    service.append_send_budget_evidence(
        run_id=job.envelope.run_id,
        decision=worker,
    )
    hq = service.reserve_send_budget(
        kind="hq_review_wake",
        run_id=job.envelope.run_id,
    )
    service.append_send_budget_evidence(
        run_id=job.envelope.run_id,
        decision=hq,
    )

    with sqlite3.connect(service.store.database_path) as connection:
        raw = connection.execute(
            "SELECT send_budget_reservations_json FROM execution_history WHERE run_id = ?",
            (job.envelope.run_id,),
        ).fetchone()[0]
    evidence = json.loads(raw)

    assert [item["kind"] for item in evidence] == [
        "worker_dispatch",
        "hq_review_wake",
    ]
    assert [item["sequence"] for item in evidence] == [1, 2]


def test_duplicate_worker_refusal_does_not_consume_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch, limit=1)
    monkeypatch.setattr(
        center.history,
        "successful_send_exists",
        lambda _key: True,
    )

    result = center.execute(_job())

    assert result.status == "refused"
    assert service.send_budget_state()["used"] == 0


def test_draft_worker_path_does_not_consume_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch, limit=1)
    job = _job(mode="draft")

    monkeypatch.setattr(
        worker_operations,
        "run_worker_browser_transport",
        lambda *_args, **_kwargs: (_result(job), object()),
    )

    center.execute(job)

    assert service.send_budget_state()["used"] == 0


def test_worker_transport_attempt_consumes_budget_and_records_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch, limit=2)
    job = _job()

    monkeypatch.setattr(
        worker_operations,
        "run_worker_browser_transport",
        lambda *_args, **_kwargs: (_result(job), object()),
    )

    result = center.execute(job)
    row = center.browser_evidence.history(limit=1)[0]
    evidence = json.loads(row["send_budget_reservations_json"])

    assert result.status == "failed"
    assert service.send_budget_state()["used"] == 1
    assert evidence[0]["kind"] == "worker_dispatch"
    assert evidence[0]["sequence"] == 1


def test_exhausted_worker_budget_pauses_before_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, center = _prepared_center(tmp_path, monkeypatch, limit=1)
    service.reserve_send_budget(kind="hq_review_wake", run_id="RUN-OTHER")

    def unexpected_transport(*_args, **_kwargs):
        raise AssertionError("Budget exhaustion must stop before transport.")

    monkeypatch.setattr(
        worker_operations,
        "run_worker_browser_transport",
        unexpected_transport,
    )

    result = center.execute(_job())

    assert result.status == "refused"
    assert "budget exhausted" in result.reason.casefold()
    assert service.paused is True
    assert service.pause_state()["trigger"] == "send_budget"
    assert service.send_budget_state()["held_operations"]["count"] == 1


def test_hq_wake_uses_same_budget_and_attaches_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _wake_module()
    service = _service(tmp_path, monkeypatch, limit=2)
    history = WorkerExecutionHistoryStore(service.store.database_path)
    job = _job()
    history.record(_result(job))

    decision = module._reserve_hq_wake_budget(
        service,
        run_id=job.envelope.run_id,
    )

    row = history.worker_history(limit=1)[0]
    with sqlite3.connect(service.store.database_path) as connection:
        raw = connection.execute(
            "SELECT send_budget_reservations_json FROM execution_history WHERE run_id = ?",
            (job.envelope.run_id,),
        ).fetchone()[0]

    assert decision.kind == "hq_review_wake"
    assert service.send_budget_state()["used"] == 1
    assert json.loads(raw)[0]["kind"] == "hq_review_wake"
    assert row["run_id"] == job.envelope.run_id


def test_exhausted_hq_wake_budget_pauses_before_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _wake_module()
    service = _service(tmp_path, monkeypatch, limit=1)
    history = WorkerExecutionHistoryStore(service.store.database_path)
    job = _job()
    history.record(_result(job))
    service.reserve_send_budget(kind="worker_dispatch", run_id="RUN-OTHER")

    with pytest.raises(WorkerRuntimeError, match="budget exhausted"):
        module._reserve_hq_wake_budget(
            service,
            run_id=job.envelope.run_id,
        )

    assert service.paused is True
    assert service.pause_state()["trigger"] == "send_budget"
    assert service.send_budget_state()["held_operations"]["count"] == 1
