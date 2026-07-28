from __future__ import annotations

import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from lifeos_dashboard.worker_github_orchestrator import WorkerGitHubOrchestrator
from lifeos_dashboard.worker_hq_review import WorkerHqReviewIngestionReceipt
from lifeos_dashboard.worker_hq_review_state_repair_runtime import (
    _reconcile_duplicate_repair_required,
)
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RUN_ID = "RUN-ADV-20260726-053-R1"
WORKER_ID = "maintenance_worker"
REVIEW_PATH = (
    "projects/life-logistics-hq/worker-results/maintenance_worker/"
    f"{RUN_ID}/hq-review-001.json"
)
CHECKSUM = "sha256:review"
COMMIT_SHA = "1" * 40
BLOB_SHA = "2" * 40


class _Service:
    def __init__(self, database: Path) -> None:
        self.database = database

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)


def _database(tmp_path: Path, *, checksum: str = CHECKSUM) -> Path:
    database = tmp_path / "command-center.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history(
                id INTEGER PRIMARY KEY,
                run_id TEXT NOT NULL,
                worker_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                prompt_type TEXT NOT NULL,
                result_state TEXT,
                hq_review_state TEXT,
                hq_review_path TEXT,
                hq_review_checksum TEXT,
                hq_review_commit_sha TEXT,
                hq_review_blob_sha TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO execution_history(
                run_id, worker_id, mode, prompt_type, result_state,
                hq_review_state, hq_review_path, hq_review_checksum,
                hq_review_commit_sha, hq_review_blob_sha
            ) VALUES (?, ?, 'send', 'worker', 'REPORT_REJECTED',
                      'REPAIR_REQUIRED', ?, ?, ?, ?)
            """,
            (
                RUN_ID,
                WORKER_ID,
                REVIEW_PATH,
                checksum,
                COMMIT_SHA,
                BLOB_SHA,
            ),
        )
    return database


def _receipt() -> WorkerHqReviewIngestionReceipt:
    return WorkerHqReviewIngestionReceipt(
        status="succeeded",
        run_id=RUN_ID,
        worker_id=WORKER_ID,
        review_state="REPAIR_REQUIRED",
        review_path=REVIEW_PATH,
        review_checksum=CHECKSUM,
        review_commit_sha=COMMIT_SHA,
        review_blob_sha=BLOB_SHA,
        result_state="REPORT_REJECTED",
        ready_for_consumption=False,
        requires_rob_validation=False,
        duplicate_suppressed=True,
    )


def test_duplicate_repair_required_receipt_restores_canonical_state(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)

    receipt = _reconcile_duplicate_repair_required(
        _Service(database),
        _receipt(),
    )

    with sqlite3.connect(database) as connection:
        state = connection.execute(
            "SELECT result_state FROM execution_history WHERE run_id = ?",
            (RUN_ID,),
        ).fetchone()[0]
    assert receipt.result_state == "REPORT_REPAIR_PENDING"
    assert state == "REPORT_REPAIR_PENDING"


def test_reconciliation_refuses_conflicting_review_evidence(tmp_path: Path) -> None:
    database = _database(tmp_path, checksum="sha256:different")

    with pytest.raises(WorkerRuntimeError, match="changed or conflicting"):
        _reconcile_duplicate_repair_required(
            _Service(database),
            _receipt(),
        )

    with sqlite3.connect(database) as connection:
        state = connection.execute(
            "SELECT result_state FROM execution_history WHERE run_id = ?",
            (RUN_ID,),
        ).fetchone()[0]
    assert state == "REPORT_REJECTED"


def test_orchestrator_does_not_reingest_result_while_hq_repair_is_pending() -> None:
    orchestrator = SimpleNamespace(
        _row=lambda run_id: {"result_state": "REPORT_REPAIR_PENDING"},
    )
    advisory = SimpleNamespace(run_id=RUN_ID)

    WorkerGitHubOrchestrator._ingest_result_if_present(
        orchestrator,
        advisory,
    )


def test_orchestrator_reconciles_known_hq_review_drift() -> None:
    ingested: list[str] = []
    events: list[tuple[str, str]] = []
    orchestrator = SimpleNamespace(
        _row=lambda run_id: {
            "result_state": "REPORT_REJECTED",
            "hq_review_state": "REPAIR_REQUIRED",
        },
        operations=SimpleNamespace(
            ingest_hq_review=lambda run_id: (
                ingested.append(run_id)
                or {
                    "receipt": {
                        "result_state": "REPORT_REPAIR_PENDING",
                    }
                }
            ),
        ),
        _event=lambda action, status, detail, **kwargs: events.append(
            (action, status)
        ),
    )

    WorkerGitHubOrchestrator._ingest_hq_review_if_present(
        orchestrator,
        RUN_ID,
        "ADV-20260726-053",
    )

    assert ingested == [RUN_ID]
    assert events == [("hq_review_reconciliation", "succeeded")]
