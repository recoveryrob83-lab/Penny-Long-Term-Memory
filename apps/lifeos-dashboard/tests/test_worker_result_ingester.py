from __future__ import annotations

import json
import sqlite3
import subprocess
import time
from pathlib import Path

import pytest

from lifeos_dashboard.worker_advisory_pipeline import ExecutionReadyAdvisory
from lifeos_dashboard.worker_command_center import (
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_dispatch_runtime import BrowserDispatchEvidence
from lifeos_dashboard.worker_operations import BrowserWorkerEvidenceStore
from lifeos_dashboard.worker_result_contract import (
    artifact_checksum,
    build_result_submission_contract,
    load_artifact_examples,
)
from lifeos_dashboard.worker_result_ingester import WorkerResultIngester
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService

RUN_ID = "RUN-ADV-TEST-R1"
REPORT_PATH = (
    "projects/engineering/worker-results/engineering_worker/"
    f"{RUN_ID}/report-001.json"
)
TARGETS = (
    "projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md",
    "apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-report.schema.json",
)


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def _advisory() -> ExecutionReadyAdvisory:
    return ExecutionReadyAdvisory(
        advisory_id="ADV-TEST",
        title="Validate immutable Worker result",
        board_path="coordination/boards/engineering.md",
        target_department="Engineering HQ",
        target_worker_id="engineering_worker",
        advisory_revision=1,
        task_class="engineering_read_only_verification",
        authorization_class="BOUNDED_WRITE",
        procedure_id="engineering_worker_result_outbox_validation",
        procedure_version=1,
        authorization_source="ROB-TEST-SLICE4",
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="OPEN",
        priority="NORMAL",
        source_references=TARGETS,
        requested_read_scopes=TARGETS,
        requested_write_scopes=(REPORT_PATH,),
        requested_tools=("GitHub",),
        result_contract=build_result_submission_contract(
            "engineering", "engineering_worker", RUN_ID
        ),
    )


def _transport_result(active: ExecutionReadyAdvisory) -> WorkerExecutionResult:
    envelope = active.envelope()
    return WorkerExecutionResult(
        status="succeeded",
        destination="Engineering_Worker",
        mode="send",
        exit_code=0,
        started_at=time.time() - 1,
        finished_at=time.time(),
        stdout="",
        stderr="",
        reason="Worker wake submitted and correlated.",
        trigger="manual",
        wrapper_id=envelope.wrapper_id,
        run_id=envelope.run_id,
        worker_id=envelope.worker_id,
        task_id=envelope.task_id,
        task_revision=envelope.task_revision,
        procedure_id=envelope.procedure_id,
        procedure_version=envelope.procedure_version,
        authorization_source=envelope.authorization_source,
        idempotency_key=envelope.idempotency_key,
        verification_mode=envelope.verification_mode,
    )


def _initialize_repository(root: Path) -> dict[str, str]:
    _git(root, "init")
    _git(root, "config", "user.email", "tests@lifeos.local")
    _git(root, "config", "user.name", "LifeOS Tests")
    for target in TARGETS:
        path = root / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"canonical source: {target}\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "Add canonical sources")
    return {target: _git(root, "rev-parse", f"HEAD:{target}") for target in TARGETS}


def _report_payload(blob_shas: dict[str, str], **overrides: object) -> dict[str, object]:
    payload = dict(load_artifact_examples()["worker_report"])
    payload.update(
        {
            "attempt": 1,
            "wrapper_id": "WAKE-ADV-TEST-R1",
            "run_id": RUN_ID,
            "worker_id": "engineering_worker",
            "profile_version": 1,
            "owning_department": "engineering",
            "task_id": "ADV-TEST",
            "task_revision": 1,
            "procedure_id": "engineering_worker_result_outbox_validation",
            "procedure_version": 1,
            "authorization_source": "ROB-TEST-SLICE4",
            "verification_mode": "IMMEDIATE_HQ",
            "requested_action": "Read the exact targets and create one immutable report.",
            "actual_action_attempted": "Read the exact targets and created the report.",
            "controlled_outcome": "IMPLEMENT",
            "completion_state": "completed",
            "evidence_references": [
                *(f"{path}@{blob_shas[path]}" for path in TARGETS),
                f"{REPORT_PATH}@preflight:not-found",
            ],
            "actual_read_scopes": [*TARGETS, REPORT_PATH],
            "actual_write_scopes": [REPORT_PATH],
            "actual_tools": ["GitHub"],
            "what_did_not_occur": ["No scope expansion occurred."],
            "unresolved_risks": ["Department HQ review remains pending."],
            "review_condition": "Engineering HQ must review the validated report.",
            "verification_state": "pending",
            "external_actions_verified": True,
            "approval_required_discovered": False,
            "failure_reason": None,
        }
    )
    payload.update(overrides)
    return payload


def _setup(tmp_path: Path, **report_overrides: object):
    blob_shas = _initialize_repository(tmp_path)
    active = _advisory()
    report = _report_payload(blob_shas, **report_overrides)
    report_file = tmp_path / REPORT_PATH
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    _git(tmp_path, "add", REPORT_PATH)
    _git(tmp_path, "commit", "-m", "Add immutable Worker report")

    database = tmp_path / "command-center.sqlite3"
    history = WorkerExecutionHistoryStore(database)
    runtime = WorkerRuntimeService(database)
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="engineering_worker",
            chat_title="Engineering_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/engineering_worker.md",
            profile_version=1,
        )
    )
    runtime.set_route_state("engineering_worker", "available")
    history.record(_transport_result(active))
    BrowserWorkerEvidenceStore(database).attach(
        RUN_ID,
        BrowserDispatchEvidence(
            dispatch_state="DISPATCH_SUBMITTED",
            user_turn_id="conversation-turn-42",
            dispatch_receipt_json='{"status":"submitted"}',
            returned_to_source=True,
        ),
    )
    return WorkerResultIngester(tmp_path, database, runtime=runtime), active, database, report


def _row(database: Path) -> sqlite3.Row:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()
    assert row is not None
    return row


def _table_names(database: Path) -> set[str]:
    with sqlite3.connect(database) as connection:
        return {
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }


def test_valid_report_advances_existing_row_and_calculates_checksum(tmp_path: Path) -> None:
    ingester, active, database, report = _setup(tmp_path)
    before_tables = _table_names(database)

    receipt = ingester.ingest(active)
    row = _row(database)

    assert receipt.report_state == "REPORT_VALIDATED"
    assert receipt.report_checksum == artifact_checksum(report)
    assert receipt.hq_review_required is True
    assert receipt.duplicate_suppressed is False
    assert row["result_state"] == "REPORT_VALIDATED"
    assert row["report_path"] == REPORT_PATH
    assert row["report_checksum"] == artifact_checksum(report)
    assert row["controlled_outcome"] == "IMPLEMENT"
    assert row["receiver_verification_state"] == "pending"
    assert row["worker_verification_state"] is None
    assert row["report_commit_sha"] == _git(
        tmp_path, "log", "-1", "--format=%H", "--", REPORT_PATH
    )
    assert row["report_blob_sha"] == _git(tmp_path, "rev-parse", f"HEAD:{REPORT_PATH}")
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()[0] == 1
    assert _table_names(database) == before_tables


def test_reingesting_identical_report_is_idempotent(tmp_path: Path) -> None:
    ingester, active, database, _ = _setup(tmp_path)

    first = ingester.ingest(active)
    second = ingester.ingest(active)

    assert first.report_checksum == second.report_checksum
    assert second.duplicate_suppressed is True
    assert _row(database)["result_state"] == "REPORT_VALIDATED"


def test_identity_mismatch_rejects_report_on_same_row(tmp_path: Path) -> None:
    ingester, active, database, _ = _setup(tmp_path, task_revision=2)

    with pytest.raises(WorkerRuntimeError, match="rejected"):
        ingester.ingest(active)

    row = _row(database)
    assert row["result_state"] == "REPORT_REJECTED"
    assert "task_revision" in row["report_validation_errors_json"]
    assert row["controlled_outcome"] is None
