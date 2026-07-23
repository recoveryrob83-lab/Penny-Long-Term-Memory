import sqlite3
from pathlib import Path

from lifeos_dashboard.worker_command_center import (
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_verification import WorkerVerificationService


def test_exact_legacy_reviewer_title_is_canonicalized_before_persistence(
    tmp_path: Path,
) -> None:
    database = tmp_path / "command-center.sqlite3"
    WorkerExecutionHistoryStore(database).record(
        WorkerExecutionResult(
            status="succeeded",
            destination="Engineering_Worker",
            mode="send",
            exit_code=0,
            started_at=1.0,
            finished_at=2.0,
            stdout="",
            stderr="",
            reason="Synthetic Worker result.",
            trigger="manual",
            wrapper_id="WAKE-TITLE-R1",
            run_id="RUN-TITLE-R1",
            worker_id="engineering_worker",
            task_id="TITLE-ROLLOVER",
            task_revision=1,
            procedure_id="title_rollover_test",
            procedure_version=1,
            authorization_source="ENGINEERING_HQ_TEST",
            idempotency_key="engineering_worker:TITLE-ROLLOVER:1",
            verification_mode="IMMEDIATE_HQ",
            owning_department="engineering",
            controlled_outcome="IMPLEMENT",
        )
    )
    service = WorkerVerificationService(database)

    reviewed = service.review(
        "RUN-TITLE-R1",
        "verified",
        actor="Engineering HQ",
        reason="Exact legacy title accepted only through the bounded mapping.",
    )

    assert reviewed.verification_actor == "Engineering_HQ"
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT worker_verification_actor FROM execution_history WHERE run_id = ?",
            ("RUN-TITLE-R1",),
        ).fetchone() == ("Engineering_HQ",)
