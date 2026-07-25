import sqlite3
from pathlib import Path

import pytest

from lifeos_dashboard.worker_activation_readiness import (
    WorkerActivationReadinessService,
)


def _write_database(
    database_path: Path,
    *,
    worker_id: str,
    chat_title: str,
    owning_department: str,
    profile_path: str,
) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE worker_registry (
                worker_id TEXT PRIMARY KEY,
                chat_title TEXT NOT NULL UNIQUE,
                owning_department TEXT NOT NULL,
                profile_path TEXT NOT NULL UNIQUE,
                profile_version INTEGER NOT NULL,
                conversation_url TEXT,
                route_revision INTEGER NOT NULL,
                specialization TEXT NOT NULL,
                role TEXT NOT NULL,
                deployment_state TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
            CREATE TABLE worker_route_state (
                worker_id TEXT PRIMARY KEY,
                availability TEXT NOT NULL,
                last_seen_at REAL,
                pause_reason TEXT,
                updated_at REAL NOT NULL
            );
            CREATE TABLE command_center_control (
                control_key TEXT PRIMARY KEY,
                paused INTEGER NOT NULL,
                pause_kind TEXT NOT NULL,
                reason TEXT NOT NULL,
                affected_run_id TEXT,
                trigger TEXT,
                recovery_condition TEXT,
                tripped_at REAL,
                updated_at REAL NOT NULL,
                send_budget_limit INTEGER NOT NULL,
                send_budget_used INTEGER NOT NULL,
                send_budget_epoch INTEGER NOT NULL
            );
            CREATE TABLE execution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id TEXT,
                run_id TEXT,
                result_state TEXT,
                hq_review_state TEXT,
                requires_rob_validation INTEGER,
                ready_for_consumption INTEGER
            );
            """
        )
        connection.execute(
            """
            INSERT INTO worker_registry VALUES (
                ?, ?, ?, ?, 1,
                'https://chatgpt.com/g/project/c/worker-route',
                1, 'general', 'worker', 'enabled', 1.0, 1.0
            )
            """,
            (worker_id, chat_title, owning_department, profile_path),
        )
        connection.execute(
            """
            INSERT INTO worker_route_state VALUES (?, 'available', 1.0, NULL, 1.0)
            """,
            (worker_id,),
        )
        connection.execute(
            """
            INSERT INTO command_center_control VALUES (
                'shared_pause', 0, 'none', '', NULL, NULL, NULL, NULL, 1.0, 3, 0, 1
            )
            """
        )


def _finding(report, code: str):
    return next(item for item in report.findings if item.code == code)


@pytest.mark.parametrize(
    (
        "worker_id",
        "chat_title",
        "owning_department",
        "profile_path",
        "review_procedure_path",
    ),
    [
        (
            "engineering_worker",
            "Engineering_Worker",
            "engineering",
            "projects/engineering/workers/engineering_worker.md",
            "projects/engineering/procedures/engineering_hq_worker_review_receipt.md",
        ),
        (
            "maintenance_worker",
            "Maintenance_Worker",
            "maintenance",
            "projects/life-logistics-hq/workers/maintenance_worker.md",
            "projects/life-logistics-hq/procedures/"
            "maintenance_hq_worker_review_receipt.md",
        ),
    ],
)
def test_current_worker_profiles_and_review_procedures_match_contract(
    tmp_path: Path,
    worker_id: str,
    chat_title: str,
    owning_department: str,
    profile_path: str,
    review_procedure_path: str,
) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    database_path = tmp_path / "command-center.sqlite3"
    _write_database(
        database_path,
        worker_id=worker_id,
        chat_title=chat_title,
        owning_department=owning_department,
        profile_path=profile_path,
    )
    before_database = database_path.read_bytes()
    profile = repository_root / profile_path
    review_procedure = repository_root / review_procedure_path
    before_profile = profile.read_bytes()
    before_procedure = review_procedure.read_bytes()
    service = WorkerActivationReadinessService(repository_root, database_path)

    report = service.report(worker_id)

    assert _finding(report, "profile.metadata").state == "PASS"
    assert _finding(report, "profile.sections").state == "PASS"
    assert _finding(report, "profile.retirement").state == "PASS"
    assert _finding(report, "review.worker_title").state == "PASS"
    assert _finding(report, "review.procedure_metadata").state == "PASS"
    assert _finding(report, "review.procedure_sections").state == "PASS"
    assert report.state == "READY_FOR_AUTHORITY_REVIEW"
    assert report.activation_authorized is False
    assert database_path.read_bytes() == before_database
    assert profile.read_bytes() == before_profile
    assert review_procedure.read_bytes() == before_procedure


def test_maintenance_profile_binds_immutable_result_submission_procedure() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    profile_path = repository_root / "projects/life-logistics-hq/workers/maintenance_worker.md"
    procedure_path = (
        repository_root
        / "projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md"
    )

    profile_text = profile_path.read_text(encoding="utf-8")
    procedure_text = procedure_path.read_text(encoding="utf-8")

    assert "maintenance_worker_result_submission" in profile_text
    assert "procedure_id: maintenance_worker_result_submission" in procedure_text
    assert "required_verification_mode: IMMEDIATE_HQ" in procedure_text
    assert "Result Overwrite Allowed: false" in procedure_text
    assert "Result Work Reexecution Authorized: false" in procedure_text
