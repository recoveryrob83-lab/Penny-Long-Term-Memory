import sqlite3
from pathlib import Path

import pytest

from lifeos_dashboard.worker_runtime import WorkerRuntimeError
from lifeos_dashboard.worker_verification import (
    WorkerVerificationService,
    record_from_row,
)


def row(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "id": 1,
        "run_id": "RUN-1",
        "worker_id": "office_leaks_worker",
        "task_id": "ADV-1",
        "task_revision": 1,
        "owning_department": "office-leaks-consulting",
        "controlled_outcome": "IMPLEMENT",
        "verification_mode": "ROUTINE_BATCH",
        "receiver_verification_state": "pending",
        "worker_verification_state": None,
        "receiver_reason": "Authorized work completed.",
        "finished_at": 10.0,
        "worker_verification_updated_at": None,
        "worker_verification_actor": None,
        "worker_verification_reason": None,
    }
    values.update(overrides)
    return values


def insert_run(database: Path, **overrides: object) -> WorkerVerificationService:
    service = WorkerVerificationService(database)
    values = row(**overrides)
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            INSERT INTO execution_history(
                status, destination, mode, prompt_type, exit_code,
                started_at, finished_at, stdout, stderr, reason,
                run_id, worker_id, task_id, task_revision,
                owning_department, controlled_outcome, verification_mode,
                receiver_verification_state, receiver_reason
            ) VALUES (
                'succeeded', 'OfficeLeaks_Worker', 'send', 'worker', 0,
                1.0, ?, '', '', 'Worker transport completed successfully.',
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                values["finished_at"],
                values["run_id"],
                values["worker_id"],
                values["task_id"],
                values["task_revision"],
                values["owning_department"],
                values["controlled_outcome"],
                values["verification_mode"],
                values["receiver_verification_state"],
                values["receiver_reason"],
            ),
        )
    return service


def test_routine_batch_pending_is_queued_without_immediate_wake() -> None:
    record = record_from_row(row())
    assert record.verification_state == "pending"
    assert record.queue_eligible is True
    assert record.review_route == "routine_batch"
    assert record.wake_required is False
    assert "batched" in record.wake_reason


def test_verified_automatic_work_suppresses_wake() -> None:
    record = record_from_row(
        row(verification_mode="AUTOMATIC", receiver_verification_state="verified")
    )
    assert record.receiver_evidence_state == "verified"
    assert record.verification_state == "verified"
    assert record.review_route == "automatic"
    assert record.wake_disposition == "suppressed"


def test_receiver_evidence_does_not_replace_immediate_hq_review() -> None:
    record = record_from_row(
        row(verification_mode="IMMEDIATE_HQ", receiver_verification_state="verified")
    )
    assert record.receiver_evidence_state == "verified"
    assert record.verification_state == "pending"
    assert record.wake_required is True


def test_unverified_automatic_work_fails_safe_to_department_hq() -> None:
    record = record_from_row(row(verification_mode="AUTOMATIC"))
    assert record.verification_state == "pending"
    assert record.wake_disposition == "owning_department_hq"
    assert record.wake_target == "office-leaks-consulting"
    assert "postcondition" in record.wake_reason


def test_immediate_hq_implementation_requires_department_wake() -> None:
    record = record_from_row(row(verification_mode="IMMEDIATE_HQ"))
    assert record.review_route == "immediate_hq"
    assert record.wake_required is True
    assert record.wake_target == "office-leaks-consulting"


def test_hold_is_rejected_and_routes_to_owning_department() -> None:
    record = record_from_row(
        row(
            controlled_outcome="REPORT_AND_HOLD",
            receiver_verification_state="unavailable",
        )
    )
    assert record.verification_state == "rejected"
    assert record.queue_eligible is False
    assert record.wake_disposition == "owning_department_hq"


def test_elevation_is_rejected_and_routes_to_chief_of_staff() -> None:
    record = record_from_row(
        row(
            controlled_outcome="ELEVATE_FOR_APPROVAL",
            receiver_verification_state="unavailable",
        )
    )
    assert record.verification_state == "rejected"
    assert record.wake_disposition == "chief_of_staff_hq"
    assert record.wake_target == "Chief_of_Staff_HQ"


@pytest.mark.parametrize("lifecycle", ["SOURCE_VERIFIED", "CLOSED"])
def test_terminal_canonical_lifecycle_suppresses_wake(lifecycle: str) -> None:
    record = record_from_row(
        row(controlled_outcome="REPORT_AND_HOLD"),
        authoritative_lifecycle_state=lifecycle,
    )
    assert record.wake_disposition == "suppressed"
    assert lifecycle in record.wake_reason


def test_status_filters_existing_history_without_new_queue_table(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    service = insert_run(database)
    insert_run(
        database,
        run_id="RUN-2",
        controlled_outcome="REPORT_AND_HOLD",
        receiver_verification_state="unavailable",
    )
    status = service.status()
    assert status["summary"] == {
        "total": 2,
        "pending": 1,
        "verified": 0,
        "rejected": 1,
        "routine_queue": 1,
        "wake_required": 1,
        "wake_suppressed": 1,
    }
    assert len(status["records"]) == 2
    with sqlite3.connect(database) as connection:
        tables = {
            item[0]
            for item in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    assert "worker_verification" not in tables
    assert "verification_queue" not in tables


def test_routine_review_updates_same_history_row(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    service = insert_run(database)
    reviewed = service.review(
        "RUN-1",
        "verified",
        actor="Office_Leaks_HQ",
        reason="Evidence read back successfully.",
    )
    assert reviewed.verification_state == "verified"
    assert reviewed.queue_eligible is False
    assert reviewed.wake_required is False
    assert reviewed.verification_actor == "Office_Leaks_HQ"
    assert reviewed.verification_reason == "Evidence read back successfully."
    with sqlite3.connect(database) as connection:
        stored = connection.execute(
            "SELECT worker_verification_state FROM execution_history WHERE run_id = 'RUN-1'"
        ).fetchone()
    assert stored == ("verified",)


def test_immediate_hq_review_suppresses_repeat_wake(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    service = insert_run(database, verification_mode="IMMEDIATE_HQ")
    before = service.store.record("RUN-1")
    assert before is not None
    assert before.wake_required is True
    reviewed = service.review(
        "RUN-1",
        "verified",
        actor="Office_Leaks_HQ",
        reason="Immediate review completed.",
    )
    assert reviewed.verification_state == "verified"
    assert reviewed.wake_required is False


def test_review_cannot_override_automatic_machine_verification(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    service = insert_run(database, verification_mode="AUTOMATIC")
    with pytest.raises(WorkerRuntimeError, match="machine postcondition"):
        service.review(
            "RUN-1",
            "verified",
            actor="Engineering_HQ",
            reason="Manual override attempted.",
        )


def test_terminal_review_cannot_be_reversed(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    service = insert_run(database)
    service.review(
        "RUN-1",
        "verified",
        actor="Office_Leaks_HQ",
        reason="Evidence accepted.",
    )
    with pytest.raises(WorkerRuntimeError, match="already terminal"):
        service.review(
            "RUN-1",
            "rejected",
            actor="Office_Leaks_HQ",
            reason="Conflicting second decision.",
        )
