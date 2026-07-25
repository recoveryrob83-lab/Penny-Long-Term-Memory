import sqlite3
from pathlib import Path

from lifeos_dashboard.worker_activation_readiness import (
    WorkerActivationReadinessService,
)


def _write_database(database_path: Path) -> None:
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
            INSERT INTO worker_registry VALUES (
                'engineering_worker',
                'Engineering_Worker',
                'engineering',
                'projects/engineering/workers/engineering_worker.md',
                1,
                'https://chatgpt.com/g/project/c/engineering-worker',
                1,
                'general',
                'worker',
                'enabled',
                1.0,
                1.0
            );
            INSERT INTO worker_route_state VALUES (
                'engineering_worker', 'available', 1.0, NULL, 1.0
            );
            INSERT INTO command_center_control VALUES (
                'shared_pause', 0, 'none', '', NULL, NULL, NULL, NULL, 1.0, 3, 0, 1
            );
            """
        )


def _finding(report, code: str):
    return next(item for item in report.findings if item.code == code)


def test_current_engineering_profile_and_review_procedure_match_contract(
    tmp_path: Path,
) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    database_path = tmp_path / "command-center.sqlite3"
    _write_database(database_path)
    before_database = database_path.read_bytes()
    profile_path = repository_root / "projects/engineering/workers/engineering_worker.md"
    procedure_path = (
        repository_root
        / "projects/engineering/procedures/engineering_hq_worker_review_receipt.md"
    )
    before_profile = profile_path.read_bytes()
    before_procedure = procedure_path.read_bytes()
    service = WorkerActivationReadinessService(repository_root, database_path)

    report = service.report("engineering_worker")

    assert _finding(report, "profile.metadata").state == "PASS"
    assert _finding(report, "profile.sections").state == "PASS"
    assert _finding(report, "profile.retirement").state == "PASS"
    assert _finding(report, "review.worker_title").state == "PASS"
    assert _finding(report, "review.procedure_metadata").state == "PASS"
    assert _finding(report, "review.procedure_sections").state == "PASS"
    assert report.activation_authorized is False
    assert database_path.read_bytes() == before_database
    assert profile_path.read_bytes() == before_profile
    assert procedure_path.read_bytes() == before_procedure
