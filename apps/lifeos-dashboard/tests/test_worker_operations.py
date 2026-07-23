import json
import sqlite3
import subprocess
import time
from dataclasses import replace
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import (
    WorkerCommandJob,
    WorkerExecutionHistoryStore,
)
from lifeos_dashboard.worker_dispatch_runtime import (
    BrowserDispatchEvidence,
    parse_browser_dispatch_receipt,
)
from lifeos_dashboard.worker_operations import (
    BrowserWorkerEvidenceStore,
    parse_reported_outcome,
    parse_synthetic_receipt,
    run_worker_browser_transport,
)
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService
from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerRegistryEntry,
    WorkerRuntimeError,
)


def envelope() -> ExecutionEnvelope:
    return ExecutionEnvelope(
        wrapper_id="WAKE-ADV-TEST-R1",
        run_id="RUN-ADV-TEST-R1",
        worker_id="engineering_worker",
        task_id="ADV-TEST",
        task_revision=1,
        procedure_id="engineering_worker_read_only_verification",
        procedure_version=1,
        authorization_source="ROB-TEST",
        verification_mode="IMMEDIATE_HQ",
    )


def entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="engineering_worker",
        chat_title="Engineering_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/engineering_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/g/project/c/engineering-worker",
        route_revision=1,
    )


def job() -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=envelope(),
        instruction="Execute only the bounded test assignment.",
        mode="send",
        confirm_send=True,
    )


def test_reported_outcome_parser_remains_historical_evidence_only() -> None:
    assert parse_reported_outcome("CONTROLLED_OUTCOME: IMPLEMENT") == "IMPLEMENT"
    assert parse_reported_outcome("Controlled Outcome - REPORT_AND_HOLD") == "REPORT_AND_HOLD"
    assert parse_reported_outcome("No final outcome marker") is None
    assert parse_reported_outcome(
        "CONTROLLED_OUTCOME: IMPLEMENT\nCONTROLLED_OUTCOME: REPORT_AND_HOLD"
    ) is None


def test_dispatch_receipt_requires_one_valid_payload() -> None:
    payload = {
        "status": "submitted",
        "request_marker": "WAKE-ADV-TEST-R1",
        "run_id": "RUN-ADV-TEST-R1",
        "submission_confirmed": True,
        "user_turn_id": "conversation-turn-20",
    }
    stdout = "BROWSER_DISPATCH_OK\nLIFEOS_BROWSER_DISPATCH_RECEIPT=" + json.dumps(payload)
    assert parse_browser_dispatch_receipt(stdout) == payload

    with pytest.raises(WorkerRuntimeError, match="exactly one"):
        parse_browser_dispatch_receipt("BROWSER_DISPATCH_OK")


def test_synthetic_receipt_requires_explicit_zero_authority() -> None:
    payload = {
        "status": "succeeded",
        "dispatch_state": "DISPATCH_SUBMITTED",
        "durable_authority_created": False,
        "returned_to_source": True,
    }
    stdout = (
        "SYNTHETIC_BROWSER_DISPATCH_OK\n"
        "LIFEOS_SYNTHETIC_BROWSER_RECEIPT=" + json.dumps(payload)
    )
    assert parse_synthetic_receipt(stdout) == payload

    payload["durable_authority_created"] = True
    unsafe = "LIFEOS_SYNTHETIC_BROWSER_RECEIPT=" + json.dumps(payload)
    with pytest.raises(WorkerRuntimeError, match="zero authority"):
        parse_synthetic_receipt(unsafe)


def test_legacy_worker_registry_migrates_route_columns(tmp_path: Path) -> None:
    database = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE worker_registry (
                worker_id TEXT PRIMARY KEY,
                chat_title TEXT NOT NULL UNIQUE,
                owning_department TEXT NOT NULL,
                profile_path TEXT NOT NULL UNIQUE,
                profile_version INTEGER NOT NULL,
                specialization TEXT NOT NULL,
                role TEXT NOT NULL,
                deployment_state TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        connection.execute(
            """
            INSERT INTO worker_registry VALUES (
                'engineering_worker',
                'Engineering_Worker',
                'engineering',
                'projects/engineering/workers/engineering_worker.md',
                1,
                'general',
                'worker',
                'enabled',
                1.0,
                1.0
            )
            """
        )

    runtime = WorkerRuntimeService(database)
    migrated = runtime.worker("engineering_worker")

    assert migrated.conversation_url is None
    assert migrated.route_revision == 0

    with sqlite3.connect(database) as connection:
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(worker_registry)"
            ).fetchall()
        }

    assert "conversation_url" in columns
    assert "route_revision" in columns


def test_browser_transport_refuses_missing_registered_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def should_not_run(*args, **kwargs):
        raise AssertionError("subprocess must not run without a registered URL")

    monkeypatch.setattr(
        "lifeos_dashboard.worker_dispatch_runtime.subprocess.run",
        should_not_run,
    )

    result, evidence = run_worker_browser_transport(
        job(),
        replace(entry(), conversation_url=None, route_revision=0),
        tmp_path,
        trigger="manual",
        timeout_seconds=120,
    )

    assert result.status == "refused"
    assert "registered exact conversation URL" in result.reason
    assert evidence.dispatch_state == "DISPATCH_PENDING"


def test_browser_transport_passes_registered_url_to_dispatch_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[str] = []

    def fake_run(command, **kwargs):
        del kwargs
        observed.extend(command)
        return subprocess.CompletedProcess(
            args=command,
            returncode=2,
            stdout="",
            stderr="STOPPED: synthetic pre-send stop",
        )

    monkeypatch.setattr(
        "lifeos_dashboard.worker_dispatch_runtime.subprocess.run",
        fake_run,
    )

    run_worker_browser_transport(
        job(),
        entry(),
        tmp_path,
        trigger="manual",
        timeout_seconds=120,
    )

    url_index = observed.index("--worker-url")
    assert observed[url_index + 1] == entry().conversation_url


def test_browser_transport_submits_without_waiting_for_worker_response(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "status": "submitted",
        "worker_url": "https://chatgpt.com/g/project/c/worker",
        "return_url": "https://chatgpt.com/g/project/c/hq",
        "request_marker": "WAKE-ADV-TEST-R1",
        "run_id": "RUN-ADV-TEST-R1",
        "baseline_turns": 5,
        "final_turns": 6,
        "user_turn_id": "conversation-turn-20",
        "submission_confirmed": True,
        "returned_to_source": True,
        "return_error": None,
        "submission_uncertain": False,
    }
    stdout = "BROWSER_DISPATCH_OK\nLIFEOS_BROWSER_DISPATCH_RECEIPT=" + json.dumps(receipt)
    monkeypatch.setattr(
        "lifeos_dashboard.worker_dispatch_runtime.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0], returncode=0, stdout=stdout, stderr=""
        ),
    )

    result, evidence = run_worker_browser_transport(
        job(),
        entry(),
        tmp_path,
        trigger="manual",
        timeout_seconds=120,
    )

    assert result.status == "succeeded"
    assert result.run_id == "RUN-ADV-TEST-R1"
    assert result.stdout == ""
    assert "Worker result remains pending" in result.reason
    assert evidence.dispatch_state == "DISPATCH_SUBMITTED"
    assert evidence.user_turn_id == "conversation-turn-20"
    assert evidence.returned_to_source is True
    assert "assistant_turn_id" not in evidence.__dict__
    assert result.controlled_outcome is None


def test_dispatch_evidence_updates_existing_execution_row(tmp_path: Path) -> None:
    database = tmp_path / "command_center.sqlite3"
    history = WorkerExecutionHistoryStore(database)
    now = time.time()
    active_job = job()
    result = __import__(
        "lifeos_dashboard.worker_operations", fromlist=["_base_result"]
    )._base_result(
        active_job,
        "Engineering_Worker",
        trigger="manual",
        status="succeeded",
        exit_code=0,
        started_at=now,
        stdout="",
        stderr="",
        reason="Dispatched.",
    )
    history.record(result)
    evidence_store = BrowserWorkerEvidenceStore(database)
    evidence_store.attach(
        result.run_id,
        BrowserDispatchEvidence(
            dispatch_state="DISPATCH_SUBMITTED",
            user_turn_id="conversation-turn-20",
            dispatch_receipt_json='{"status":"submitted"}',
            returned_to_source=True,
        ),
    )

    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT dispatch_state, user_turn_id, dispatch_receipt_json,
                   returned_to_source, controlled_outcome
            FROM execution_history WHERE run_id = ?
            """,
            (result.run_id,),
        ).fetchone()

    assert row is not None
    assert row["dispatch_state"] == "DISPATCH_SUBMITTED"
    assert row["user_turn_id"] == "conversation-turn-20"
    assert row["dispatch_receipt_json"] == '{"status":"submitted"}'
    assert row["returned_to_source"] == 1
    assert row["controlled_outcome"] is None


def test_submission_uncertainty_blocks_duplicate_send(tmp_path: Path) -> None:
    database = tmp_path / "command_center.sqlite3"
    history = WorkerExecutionHistoryStore(database)
    active_job = job()
    uncertain = __import__(
        "lifeos_dashboard.worker_operations", fromlist=["_base_result"]
    )._base_result(
        active_job,
        "Engineering_Worker",
        trigger="manual",
        status="failed",
        exit_code=3,
        started_at=time.time(),
        stdout="",
        stderr="STOPPED_AFTER_SEND: correlated turn could not be proven",
        reason="Inspect the Worker chat and do not retry blindly.",
    )
    history.record(uncertain)

    assert history.successful_send_exists(active_job.envelope.idempotency_key) is True
