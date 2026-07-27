from __future__ import annotations

import sqlite3
import threading
from types import SimpleNamespace

import pytest

from lifeos_dashboard import worker_report_repair_dispatch as dispatch_module
from lifeos_dashboard.worker_report_repair_dispatch import WorkerReportRepairDispatchService
from lifeos_dashboard.worker_result_repair import WorkerReportRepairWake
from lifeos_dashboard.worker_runtime import (
    WorkerRegistryEntry,
    WorkerRouteState,
    WorkerRuntimeError,
)


RUN_ID = "RUN-ADV-20260726-053-R1"


class _Decision:
    reserved = True
    reason = ""


class _CommandCenter:
    def __init__(self, app_root) -> None:
        self.app_root = app_root
        self.paused = False
        self._run_lock = threading.Lock()
        self.reservations: list[tuple[str, str]] = []
        self.evidence: list[str] = []
        self.pauses: list[dict[str, object]] = []

    def reserve_send_budget(self, *, kind: str, run_id: str) -> _Decision:
        self.reservations.append((kind, run_id))
        return _Decision()

    def append_send_budget_evidence(self, *, run_id: str, decision: _Decision) -> None:
        self.evidence.append(run_id)

    def trip_safety_pause(self, **kwargs: object) -> None:
        self.pauses.append(kwargs)


class _Runtime:
    def __init__(self) -> None:
        self.entry = WorkerRegistryEntry(
            worker_id="maintenance_worker",
            chat_title="Maintenance_Worker",
            owning_department="maintenance",
            profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
            profile_version=1,
            conversation_url="https://chatgpt.com/c/maintenance-worker-test",
            route_revision=1,
        )
        self.store = SimpleNamespace(
            route_state=lambda worker_id: WorkerRouteState(worker_id, "available")
        )

    def worker(self, worker_id: str, *, require_enabled: bool = False):
        assert worker_id == "maintenance_worker"
        assert require_enabled is True
        return self.entry


def _wake() -> WorkerReportRepairWake:
    return WorkerReportRepairWake(
        wrapper_id="REPAIR-ADV-20260726-053-R1-A2",
        run_id=RUN_ID,
        worker_id="maintenance_worker",
        task_id="ADV-20260726-053",
        task_revision=1,
        rejected_report_attempt=1,
        rejected_report_path=(
            "projects/life-logistics-hq/worker-results/maintenance_worker/"
            f"{RUN_ID}/report-001.json"
        ),
        rejection_path=(
            "projects/life-logistics-hq/worker-results/maintenance_worker/"
            f"{RUN_ID}/rejection-001.json"
        ),
        next_report_attempt=2,
        corrected_report_path=(
            "projects/life-logistics-hq/worker-results/maintenance_worker/"
            f"{RUN_ID}/report-002.json"
        ),
        instruction="Correct only the report artifact. Do not repeat the underlying work.",
    )


def _operations(tmp_path):
    advisory = SimpleNamespace(
        run_id=RUN_ID,
        result_contract=SimpleNamespace(attempt=1),
        procedure_id="maintenance_coordinated_repository_repair",
        procedure_version=1,
        authorization_source="ROB",
        verification_mode="IMMEDIATE_HQ",
    )
    command_center = _CommandCenter(tmp_path)
    return SimpleNamespace(
        command_center=command_center,
        pipeline=SimpleNamespace(discover=lambda: (advisory,)),
        result_repair=SimpleNamespace(repair_wake=lambda run_id: _wake()),
        worker_center=SimpleNamespace(runtime=_Runtime()),
    )


def _database(tmp_path):
    path = tmp_path / "command_center.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history(
                id INTEGER PRIMARY KEY,
                run_id TEXT,
                mode TEXT,
                prompt_type TEXT,
                result_state TEXT,
                repair_state TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO execution_history(
                id, run_id, mode, prompt_type, result_state, repair_state
            ) VALUES(1, ?, 'send', 'worker', 'REPORT_REJECTED', 'REPORT_REPAIR_PENDING')
            """,
            (RUN_ID,),
        )
    return path


def test_report_repair_dispatch_records_one_separate_submission(monkeypatch, tmp_path) -> None:
    operations = _operations(tmp_path)
    database = _database(tmp_path)
    service = WorkerReportRepairDispatchService(operations, database)
    calls: list[str] = []

    def fake_dispatch(job, entry, app_root, *, trigger, timeout_seconds):
        calls.append(job.envelope.wrapper_id)
        assert job.envelope.run_id == RUN_ID
        assert job.instruction.startswith("Correct only")
        assert entry.worker_id == "maintenance_worker"
        assert trigger == "manual"
        return (
            SimpleNamespace(
                status="succeeded",
                exit_code=0,
                stderr="",
                reason="submitted",
            ),
            SimpleNamespace(
                user_turn_id="conversation-turn-repair-1",
                dispatch_receipt_json='{"status":"submitted"}',
                returned_to_source=True,
            ),
        )

    monkeypatch.setattr(dispatch_module, "run_worker_browser_dispatch", fake_dispatch)

    receipt = service.dispatch(RUN_ID)

    assert receipt.status == "submitted"
    assert receipt.wrapper_id == "REPAIR-ADV-20260726-053-R1-A2"
    assert calls == ["REPAIR-ADV-20260726-053-R1-A2"]
    assert operations.command_center.reservations == [("worker_report_repair", RUN_ID)]
    assert operations.command_center.evidence == [RUN_ID]
    assert operations.command_center.pauses == []
    status = service.status(RUN_ID)
    assert status["repair_dispatch_state"] == "REPAIR_DISPATCH_SUBMITTED"
    assert status["repair_dispatch_user_turn_id"] == "conversation-turn-repair-1"
    assert status["repair_dispatch_returned_to_source"] is True

    with pytest.raises(WorkerRuntimeError, match="already submitted"):
        service.dispatch(RUN_ID)
    assert calls == ["REPAIR-ADV-20260726-053-R1-A2"]


def test_report_repair_envelope_preserves_run_authority_and_uses_new_wrapper(tmp_path) -> None:
    operations = _operations(tmp_path)
    database = _database(tmp_path)
    service = WorkerReportRepairDispatchService(operations, database)
    advisory = operations.pipeline.discover()[0]
    envelope = service._repair_envelope(advisory, _wake())

    assert envelope.wrapper_id == "REPAIR-ADV-20260726-053-R1-A2"
    assert envelope.run_id == RUN_ID
    assert envelope.task_id == "ADV-20260726-053"
    assert envelope.task_revision == 1
    assert envelope.procedure_id == "maintenance_coordinated_repository_repair"
    assert envelope.authorization_source == "ROB"
