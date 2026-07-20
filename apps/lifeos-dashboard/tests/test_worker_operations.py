import json
import subprocess
import time
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import (
    WorkerCommandJob,
    WorkerExecutionHistoryStore,
)
from lifeos_dashboard.worker_operations import (
    BrowserTransportEvidence,
    BrowserWorkerEvidenceStore,
    parse_browser_receipt,
    parse_reported_outcome,
    parse_synthetic_receipt,
    run_worker_browser_transport,
)
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
    )


def job() -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=envelope(),
        instruction="Execute only the bounded test assignment.",
        mode="send",
        confirm_send=True,
    )


def test_reported_outcome_is_evidence_not_invented() -> None:
    assert parse_reported_outcome("CONTROLLED_OUTCOME: IMPLEMENT") == "IMPLEMENT"
    assert parse_reported_outcome("Controlled Outcome - REPORT_AND_HOLD") == "REPORT_AND_HOLD"
    assert parse_reported_outcome("No final outcome marker") is None
    assert parse_reported_outcome(
        "CONTROLLED_OUTCOME: IMPLEMENT\nCONTROLLED_OUTCOME: REPORT_AND_HOLD"
    ) is None


def test_browser_receipt_requires_one_valid_payload() -> None:
    payload = {
        "request_marker": "WAKE-ADV-TEST-R1",
        "response_marker": "RUN-ADV-TEST-R1",
    }
    stdout = "BROWSER_ROUNDTRIP_OK\nLIFEOS_BROWSER_ROUNDTRIP_RECEIPT=" + json.dumps(payload)
    assert parse_browser_receipt(stdout) == payload

    with pytest.raises(WorkerRuntimeError, match="exactly one"):
        parse_browser_receipt("BROWSER_ROUNDTRIP_OK")


def test_synthetic_receipt_requires_explicit_zero_authority() -> None:
    payload = {
        "status": "succeeded",
        "durable_authority_created": False,
        "returned_to_source": True,
    }
    stdout = (
        "SYNTHETIC_BROWSER_ROUNDTRIP_OK\n"
        "LIFEOS_SYNTHETIC_BROWSER_RECEIPT=" + json.dumps(payload)
    )
    assert parse_synthetic_receipt(stdout) == payload

    payload["durable_authority_created"] = True
    unsafe = "LIFEOS_SYNTHETIC_BROWSER_RECEIPT=" + json.dumps(payload)
    with pytest.raises(WorkerRuntimeError, match="zero authority"):
        parse_synthetic_receipt(unsafe)


def test_browser_transport_captures_response_and_turn_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "status": "succeeded",
        "worker_url": "https://chatgpt.com/g/project/c/worker",
        "return_url": "https://chatgpt.com/g/project/c/hq",
        "request_marker": "WAKE-ADV-TEST-R1",
        "response_marker": "RUN-ADV-TEST-R1",
        "baseline_turns": 5,
        "final_turns": 7,
        "user_turn_id": "conversation-turn-20",
        "assistant_turn_id": "conversation-turn-21",
        "response_text": (
            "Run ID: RUN-ADV-TEST-R1\n"
            "Required evidence present.\n"
            "CONTROLLED_OUTCOME: IMPLEMENT"
        ),
        "returned_to_source": True,
        "submission_uncertain": False,
    }
    stdout = "BROWSER_ROUNDTRIP_OK\nLIFEOS_BROWSER_ROUNDTRIP_RECEIPT=" + json.dumps(receipt)
    monkeypatch.setattr(
        "lifeos_dashboard.worker_operations.subprocess.run",
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
    assert "CONTROLLED_OUTCOME: IMPLEMENT" in result.stdout
    assert evidence.reported_outcome == "IMPLEMENT"
    assert evidence.assistant_turn_id == "conversation-turn-21"
    assert evidence.browser_receipt_json is not None
    assert result.controlled_outcome is None


def test_browser_evidence_updates_existing_execution_row(tmp_path: Path) -> None:
    database = tmp_path / "command_center.sqlite3"
    history = WorkerExecutionHistoryStore(database)
    now = time.time()
    active_job = job()
    result = run_result = __import__(
        "lifeos_dashboard.worker_operations", fromlist=["_base_result"]
    )._base_result(
        active_job,
        "Engineering_Worker",
        trigger="manual",
        status="succeeded",
        exit_code=0,
        started_at=now,
        stdout="CONTROLLED_OUTCOME: IMPLEMENT",
        stderr="",
        reason="Captured.",
    )
    history.record(run_result)
    evidence_store = BrowserWorkerEvidenceStore(database)
    evidence_store.attach(
        result.run_id,
        BrowserTransportEvidence(
            reported_outcome="IMPLEMENT",
            assistant_turn_id="conversation-turn-21",
            browser_receipt_json='{"status":"succeeded"}',
        ),
    )

    rows = evidence_store.history()
    assert len(rows) == 1
    assert rows[0]["worker_reported_outcome"] == "IMPLEMENT"
    assert rows[0]["assistant_turn_id"] == "conversation-turn-21"
    assert rows[0]["controlled_outcome"] is None
