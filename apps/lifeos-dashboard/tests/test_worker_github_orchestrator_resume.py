from __future__ import annotations

import sqlite3
from pathlib import Path
from types import SimpleNamespace

from lifeos_dashboard.worker_github_orchestrator import WorkerGitHubOrchestrator


def _row(**overrides):
    values = {
        "status": "failed",
        "stderr": "",
        "reason": "Browser courier stopped safely before a confirmed dispatch completed.",
        "dispatch_state": "DISPATCH_PENDING",
        "user_turn_id": "",
        "dispatch_resume_attempts": 0,
    }
    values.update(overrides)
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE sample(
            status TEXT, stderr TEXT, reason TEXT, dispatch_state TEXT,
            user_turn_id TEXT, dispatch_resume_attempts INTEGER
        )
        """
    )
    connection.execute(
        "INSERT INTO sample VALUES (?, ?, ?, ?, ?, ?)",
        tuple(values[key] for key in values),
    )
    return connection, connection.execute("SELECT * FROM sample").fetchone()


def test_safe_pre_submit_failure_is_resumable():
    connection, row = _row()
    try:
        assert WorkerGitHubOrchestrator._safe_resume_candidate(row)
    finally:
        connection.close()


def test_uncertain_or_exhausted_dispatch_is_not_resumed():
    connection, uncertain = _row(reason="Submission may have occurred; do not retry blindly.")
    try:
        assert not WorkerGitHubOrchestrator._safe_resume_candidate(uncertain)
    finally:
        connection.close()

    connection, exhausted = _row(dispatch_resume_attempts=2)
    try:
        assert not WorkerGitHubOrchestrator._safe_resume_candidate(exhausted)
    finally:
        connection.close()


def test_resume_updates_existing_row_instead_of_inserting(tmp_path: Path):
    database = tmp_path / "runtime.sqlite3"
    connection = sqlite3.connect(database)
    connection.execute(
        """
        CREATE TABLE execution_history(
            id INTEGER PRIMARY KEY,
            status TEXT,
            destination TEXT,
            exit_code INTEGER,
            started_at REAL,
            finished_at REAL,
            stdout TEXT,
            stderr TEXT,
            reason TEXT,
            trigger TEXT,
            dispatch_state TEXT,
            user_turn_id TEXT,
            dispatch_receipt_json TEXT,
            returned_to_source INTEGER,
            dispatched_at REAL,
            dispatch_resume_attempts INTEGER
        )
        """
    )
    connection.execute(
        """
        INSERT INTO execution_history(
            id, status, destination, reason, trigger, dispatch_state,
            returned_to_source, dispatch_resume_attempts
        ) VALUES (50, 'failed', 'Engineering_Worker',
                  'Browser courier stopped safely before a confirmed dispatch completed.',
                  'scheduled', 'DISPATCH_PENDING', 0, 0)
        """
    )
    connection.commit()
    connection.close()

    orchestrator = WorkerGitHubOrchestrator.__new__(WorkerGitHubOrchestrator)
    orchestrator.database_path = database
    result = SimpleNamespace(
        status="succeeded",
        destination="Engineering_Worker",
        exit_code=0,
        started_at=10.0,
        finished_at=11.0,
        stdout="",
        stderr="",
        reason="Worker wake submitted and correlated.",
        trigger="scheduled",
    )
    evidence = SimpleNamespace(
        dispatch_state="DISPATCH_SUBMITTED",
        user_turn_id="conversation-turn-50",
        dispatch_receipt_json='{"status":"submitted"}',
        returned_to_source=True,
    )

    orchestrator._persist_resumed_dispatch(50, result, evidence)

    connection = sqlite3.connect(database)
    rows = connection.execute("SELECT * FROM execution_history").fetchall()
    connection.close()
    assert len(rows) == 1
    assert rows[0][1] == "succeeded"
    assert rows[0][10] == "DISPATCH_SUBMITTED"
    assert rows[0][11] == "conversation-turn-50"
    assert rows[0][15] == 1
