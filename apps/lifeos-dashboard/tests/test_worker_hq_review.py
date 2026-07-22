import json
import sqlite3
import subprocess
import time
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import (
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_hq_review import WorkerHqReviewService
from lifeos_dashboard.worker_result_contract import artifact_checksum, artifact_path
from lifeos_dashboard.worker_result_ingester import WorkerResultIngester
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RUN_ID = "RUN-ADV-HQ-REVIEW-R1"
REPORT_PATH = (
    "projects/engineering/worker-results/engineering_worker/"
    f"{RUN_ID}/report-001.json"
)
REVIEW_PATH = (
    "projects/engineering/worker-results/engineering_worker/"
    f"{RUN_ID}/hq-review-001.json"
)


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def _commit_json(root: Path, path: str, payload: dict[str, object], message: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _git(root, "add", "--", path)
    _git(root, "commit", "--only", "-m", message, "--", path)


def _transport_result() -> WorkerExecutionResult:
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
        wrapper_id="WAKE-ADV-HQ-REVIEW-R1",
        run_id=RUN_ID,
        worker_id="engineering_worker",
        task_id="ADV-HQ-REVIEW",
        task_revision=1,
        procedure_id="engineering_worker_result_outbox_validation",
        procedure_version=1,
        authorization_source="ENGINEERING_HQ_SLICE5_TEST",
        idempotency_key="engineering_worker:ADV-HQ-REVIEW:1",
        verification_mode="IMMEDIATE_HQ",
    )


def _setup(tmp_path: Path) -> tuple[WorkerHqReviewService, Path, dict[str, object]]:
    _git(tmp_path, "init")
    _git(tmp_path, "config", "user.email", "tests@lifeos.local")
    _git(tmp_path, "config", "user.name", "LifeOS Tests")
    report = {
        "schema_id": "lifeos_worker_result_report",
        "schema_version": 1,
        "artifact_type": "worker_report",
        "attempt": 1,
        "wrapper_id": "WAKE-ADV-HQ-REVIEW-R1",
        "run_id": RUN_ID,
        "worker_id": "engineering_worker",
        "profile_version": 1,
        "owning_department": "engineering",
        "task_id": "ADV-HQ-REVIEW",
        "task_revision": 1,
        "procedure_id": "engineering_worker_result_outbox_validation",
        "procedure_version": 1,
        "authorization_source": "ENGINEERING_HQ_SLICE5_TEST",
        "verification_mode": "IMMEDIATE_HQ",
        "requested_action": "Inspect one bounded synthetic target.",
        "actual_action_attempted": "Inspected one bounded synthetic target.",
        "controlled_outcome": "IMPLEMENT",
        "completion_state": "completed",
        "evidence_references": [f"{REPORT_PATH}@preflight:not-found"],
        "actual_read_scopes": [REPORT_PATH],
        "actual_write_scopes": [REPORT_PATH],
        "actual_tools": ["GitHub"],
        "what_did_not_occur": ["No lifecycle change occurred."],
        "unresolved_risks": ["HQ review remains pending."],
        "review_condition": "Engineering HQ reviews the report.",
        "verification_state": "pending",
        "external_actions_verified": True,
        "approval_required_discovered": False,
        "failure_reason": None,
    }
    _commit_json(tmp_path, REPORT_PATH, report, "Add synthetic validated Worker report")
    report_commit = _git(tmp_path, "log", "-1", "--format=%H", "--", REPORT_PATH)
    report_blob = _git(tmp_path, "rev-parse", f"HEAD:{REPORT_PATH}")

    database = tmp_path / "command-center.sqlite3"
    WorkerExecutionHistoryStore(database).record(_transport_result())
    WorkerResultIngester(tmp_path, database)
    service = WorkerHqReviewService(tmp_path, database)
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            UPDATE execution_history SET
                result_state = 'REPORT_VALIDATED', report_path = ?, report_attempt = 1,
                report_checksum = ?, report_commit_sha = ?, report_blob_sha = ?,
                report_validated_at = ?, profile_version = 1,
                owning_department = 'engineering', controlled_outcome = 'IMPLEMENT',
                receiver_reason = 'Deterministic immutable Worker report ingestion passed.',
                receiver_verification_state = 'pending',
                receiver_completion_state = 'completed'
            WHERE run_id = ?
            """,
            (
                REPORT_PATH,
                artifact_checksum(report),
                report_commit,
                report_blob,
                time.time(),
                RUN_ID,
            ),
        )
    return service, database, report


def _review_payload(state: str) -> dict[str, object]:
    values: dict[str, object] = {
        "schema_id": "lifeos_worker_hq_review",
        "schema_version": 1,
        "artifact_type": "hq_review",
        "attempt": 1,
        "run_id": RUN_ID,
        "worker_id": "engineering_worker",
        "reviewing_hq": "Engineering HQ",
        "report_path": REPORT_PATH,
        "review_state": state,
        "report_integrity_state": "valid",
        "authority_compliance_state": "compliant",
        "work_verification_state": "verified",
        "evidence_checked": [
            f"report:{REPORT_PATH}",
            "runtime:same-execution-row",
        ],
        "reason": "Synthetic report integrity, authority, evidence, and work were checked.",
        "ready_for_consumption": True,
        "requires_rob_validation": False,
    }
    if state == "REJECTED":
        values.update(
            work_verification_state="rejected",
            reason="Synthetic work evidence contradicted the report.",
            ready_for_consumption=False,
        )
    elif state == "REPAIR_REQUIRED":
        values.update(
            report_integrity_state="invalid",
            work_verification_state="unavailable",
            reason="Synthetic receipt requires a corrected report attempt.",
            ready_for_consumption=False,
        )
    elif state == "ROB_VALIDATION_REQUIRED":
        values.update(
            work_verification_state="unavailable",
            reason="Synthetic physical outcome is unavailable to HQ inspection.",
            ready_for_consumption=False,
            requires_rob_validation=True,
        )
    return values


def _record_wake(service: WorkerHqReviewService) -> None:
    wake = service.build_wake(RUN_ID)
    assert wake.hq_chat_title == "Engineering_HQ"
    assert wake.report_path == REPORT_PATH
    assert wake.review_path == REVIEW_PATH
    assert "close the source advisory" in wake.instruction
    service.record_wake(
        RUN_ID,
        {
            "status": "submitted",
            "submission_confirmed": True,
            "request_marker": wake.marker,
            "run_id": RUN_ID,
            "user_turn_id": "conversation-turn-hq-review",
            "returned_to_source": True,
        },
    )


def _row(database: Path) -> sqlite3.Row:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()
    assert row is not None
    return row


def test_verified_receipt_advances_same_row_and_is_idempotent(tmp_path: Path) -> None:
    service, database, _ = _setup(tmp_path)
    _record_wake(service)
    _commit_json(tmp_path, REVIEW_PATH, _review_payload("VERIFIED"), "Add synthetic HQ review")

    first = service.ingest_review(RUN_ID)
    second = service.ingest_review(RUN_ID)
    row = _row(database)

    assert first.review_state == "VERIFIED"
    assert first.result_state == "HQ_VERIFIED"
    assert first.ready_for_consumption is True
    assert second.duplicate_suppressed is True
    assert row["worker_verification_state"] == "verified"
    assert row["hq_wake_state"] == "HQ_WAKE_SUBMITTED"
    assert row["hq_review_path"] == REVIEW_PATH
    assert row["result_state"] == "HQ_VERIFIED"
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()[0] == 1


@pytest.mark.parametrize(
    ("state", "expected_runtime", "ready", "needs_rob"),
    [
        ("REJECTED", "HQ_REJECTED", False, False),
        ("REPAIR_REQUIRED", "REPORT_REPAIR_PENDING", False, False),
        ("ROB_VALIDATION_REQUIRED", "ROB_VALIDATION_REQUIRED", False, True),
    ],
)
def test_nonverified_review_branches_are_explicit(
    tmp_path: Path,
    state: str,
    expected_runtime: str,
    ready: bool,
    needs_rob: bool,
) -> None:
    service, database, _ = _setup(tmp_path)
    _record_wake(service)
    _commit_json(tmp_path, REVIEW_PATH, _review_payload(state), f"Add {state} HQ review")

    receipt = service.ingest_review(RUN_ID)
    row = _row(database)

    assert receipt.review_state == state
    assert receipt.result_state == expected_runtime
    assert receipt.ready_for_consumption is ready
    assert receipt.requires_rob_validation is needs_rob
    assert row["hq_review_state"] == state


def test_verified_receipt_cannot_self_sign_unavailable_work(tmp_path: Path) -> None:
    service, _, _ = _setup(tmp_path)
    payload = _review_payload("VERIFIED")
    payload["work_verification_state"] = "unavailable"
    _commit_json(tmp_path, REVIEW_PATH, payload, "Add inconsistent HQ review")

    with pytest.raises(WorkerRuntimeError, match="inconsistent"):
        service.ingest_review(RUN_ID)


def test_hq_wake_is_nonretryable_after_confirmed_submission(tmp_path: Path) -> None:
    service, _, _ = _setup(tmp_path)
    _record_wake(service)

    with pytest.raises(WorkerRuntimeError, match="already submitted"):
        service.build_wake(RUN_ID)


def test_review_path_helper_matches_canonical_artifact_path() -> None:
    assert REVIEW_PATH == artifact_path(
        "engineering", "engineering_worker", RUN_ID, "hq_review", 1
    )
