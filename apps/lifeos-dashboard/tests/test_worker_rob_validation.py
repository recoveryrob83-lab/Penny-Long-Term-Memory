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
from lifeos_dashboard.worker_result_contract import artifact_checksum, artifact_path
from lifeos_dashboard.worker_rob_validation import WorkerRobValidationService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RUN_ID = "RUN-ADV-ROB-VALIDATION-R1"
WORKER_ID = "engineering_worker"
MARKER = "LIFEOS_ROB_OBSERVATION=SLICE6_TEST_MARKER"
HQ_REVIEW_PATH = artifact_path(
    "engineering", WORKER_ID, RUN_ID, "hq_review", 1
)
VALIDATION_PATH = artifact_path(
    "engineering", WORKER_ID, RUN_ID, "rob_validation", 1
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
        reason="Synthetic Worker wake submitted and correlated.",
        trigger="manual",
        wrapper_id="WAKE-ADV-ROB-VALIDATION-R1",
        run_id=RUN_ID,
        worker_id=WORKER_ID,
        task_id="ADV-ROB-VALIDATION",
        task_revision=1,
        procedure_id="engineering_worker_rob_validation_pilot",
        procedure_version=1,
        authorization_source="ENGINEERING_HQ_SLICE6_TEST",
        idempotency_key="engineering_worker:ADV-ROB-VALIDATION:1",
        verification_mode="IMMEDIATE_HQ",
    )


def _setup(tmp_path: Path) -> tuple[WorkerRobValidationService, Path, str]:
    _git(tmp_path, "init")
    _git(tmp_path, "config", "user.email", "tests@lifeos.local")
    _git(tmp_path, "config", "user.name", "LifeOS Tests")

    hq_review = {
        "schema_id": "lifeos_worker_hq_review",
        "schema_version": 1,
        "artifact_type": "hq_review",
        "attempt": 1,
        "run_id": RUN_ID,
        "worker_id": WORKER_ID,
        "reviewing_hq": "Engineering HQ",
        "report_path": (
            "projects/engineering/worker-results/engineering_worker/"
            f"{RUN_ID}/report-001.json"
        ),
        "review_state": "ROB_VALIDATION_REQUIRED",
        "report_integrity_state": "valid",
        "authority_compliance_state": "compliant",
        "work_verification_state": "unavailable",
        "evidence_checked": ["synthetic:report-and-authority-checked"],
        "reason": f"Rob must confirm the exact Worker-chat marker {MARKER}.",
        "ready_for_consumption": False,
        "requires_rob_validation": True,
    }
    _commit_json(tmp_path, HQ_REVIEW_PATH, hq_review, "Add synthetic HQ review")
    hq_commit = _git(tmp_path, "log", "-1", "--format=%H", "--", HQ_REVIEW_PATH)
    hq_blob = _git(tmp_path, "rev-parse", f"HEAD:{HQ_REVIEW_PATH}")

    database = tmp_path / "command-center.sqlite3"
    WorkerExecutionHistoryStore(database).record(_transport_result())
    service = WorkerRobValidationService(tmp_path, database)
    report_path = str(hq_review["report_path"])
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            UPDATE execution_history SET
                result_state = 'ROB_VALIDATION_REQUIRED',
                report_path = ?, report_checksum = ?,
                owning_department = 'engineering', controlled_outcome = 'IMPLEMENT',
                hq_review_path = ?, hq_review_checksum = ?,
                hq_review_commit_sha = ?, hq_review_blob_sha = ?,
                hq_review_state = 'ROB_VALIDATION_REQUIRED',
                hq_review_reason = ?, ready_for_consumption = 0,
                requires_rob_validation = 1
            WHERE run_id = ?
            """,
            (
                report_path,
                "sha256:" + "1" * 64,
                HQ_REVIEW_PATH,
                artifact_checksum(hq_review),
                hq_commit,
                hq_blob,
                hq_review["reason"],
                RUN_ID,
            ),
        )
    return service, database, hq_blob


def _validation_payload(state: str, hq_blob: str) -> dict[str, object]:
    return {
        "schema_id": "lifeos_worker_rob_validation",
        "schema_version": 1,
        "artifact_type": "rob_validation",
        "attempt": 1,
        "run_id": RUN_ID,
        "worker_id": WORKER_ID,
        "validator": "Rob",
        "validation_state": state,
        "observation": (
            f"Rob observed {MARKER} in the exact Engineering_Worker conversation."
            if state == "VERIFIED"
            else f"Rob did not observe the expected marker {MARKER}."
        ),
        "evidence_references": [
            f"hq-review:{HQ_REVIEW_PATH}@{hq_blob}",
            f"rob-observation:{MARKER}",
        ],
        "ready_for_consumption": state == "VERIFIED",
    }


def _row(database: Path) -> sqlite3.Row:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()
    assert row is not None
    return row


def test_verified_rob_validation_reaches_ready_for_cos_and_is_idempotent(
    tmp_path: Path,
) -> None:
    service, database, hq_blob = _setup(tmp_path)
    _commit_json(
        tmp_path,
        VALIDATION_PATH,
        _validation_payload("VERIFIED", hq_blob),
        "Add synthetic Rob validation",
    )

    first = service.ingest_validation(RUN_ID)
    second = service.ingest_validation(RUN_ID)
    row = _row(database)

    assert first.validation_state == "VERIFIED"
    assert first.validation_runtime_state == "ROB_VERIFIED"
    assert first.result_state == "READY_FOR_COS"
    assert first.ready_for_consumption is True
    assert second.duplicate_suppressed is True
    assert row["result_state"] == "READY_FOR_COS"
    assert row["rob_validation_runtime_state"] == "ROB_VERIFIED"
    assert row["worker_verification_state"] == "verified"
    assert row["worker_verification_actor"] == "Rob"
    assert row["requires_rob_validation"] == 0
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()[0] == 1


def test_rejected_rob_validation_is_not_consumption_ready(tmp_path: Path) -> None:
    service, database, hq_blob = _setup(tmp_path)
    _commit_json(
        tmp_path,
        VALIDATION_PATH,
        _validation_payload("REJECTED", hq_blob),
        "Add rejected synthetic Rob validation",
    )

    receipt = service.ingest_validation(RUN_ID)
    row = _row(database)

    assert receipt.validation_state == "REJECTED"
    assert receipt.validation_runtime_state == "ROB_REJECTED"
    assert receipt.result_state == "ROB_REJECTED"
    assert receipt.ready_for_consumption is False
    assert row["worker_verification_state"] == "rejected"
    assert row["ready_for_consumption"] == 0


def test_rob_validation_requires_exact_hq_marker(tmp_path: Path) -> None:
    service, _, hq_blob = _setup(tmp_path)
    payload = _validation_payload("VERIFIED", hq_blob)
    payload["observation"] = "Rob observed a different marker."
    _commit_json(tmp_path, VALIDATION_PATH, payload, "Add mismatched Rob validation")

    with pytest.raises(WorkerRuntimeError, match="exact HQ-requested marker"):
        service.ingest_validation(RUN_ID)


def test_verified_validation_cannot_claim_not_ready(tmp_path: Path) -> None:
    service, _, hq_blob = _setup(tmp_path)
    payload = _validation_payload("VERIFIED", hq_blob)
    payload["ready_for_consumption"] = False
    _commit_json(tmp_path, VALIDATION_PATH, payload, "Add inconsistent Rob validation")

    with pytest.raises(WorkerRuntimeError, match="must be ready"):
        service.ingest_validation(RUN_ID)


def test_rob_validation_path_matches_canonical_artifact_path() -> None:
    assert VALIDATION_PATH == artifact_path(
        "engineering", WORKER_ID, RUN_ID, "rob_validation", 1
    )
