import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from lifeos_dashboard import worker_operations
from lifeos_dashboard.worker_activation_readiness import WorkerActivationReadinessService
from lifeos_dashboard.worker_operations import WorkerOperationsService
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry, WorkerRouteState

VALID_PROFILE = """---
worker_id: engineering_worker
chat_title: Engineering_Worker
owning_department: engineering
role: worker
specialization: general
profile_version: 1
---

# Engineering_Worker Profile

## Purpose
Perform bounded Engineering execution.

## Allowed task classes
Read-only verification and exact authorized Engineering implementation.

## Explicitly prohibited work
The Worker must not activate, route, broaden, or retire itself.

## Read scope
Only exact authorized Engineering and canonical sources.

## Write scope
Only exact authorized Engineering-owned paths.

## Approved connectors and tools
Bounded GitHub, local file, terminal, code, and test tools.

## Required procedures
Load canonical Boot, execution protocol, Worker contract, department identity, and task.

## Required evidence
Preserve run identity, requested and actual action, sources, writes, tests, and outcome.

## Hold conditions
Hold on ambiguity, conflict, stale revision, unsafe scope, pause, or route failure.

## Elevation conditions
Elevate new authority, permissions, spending, cross-department scope, or deployment.

## Verification and completion path
Use the assigned verification mode and exactly one controlled outcome.

## Owning Department HQ
Engineering_HQ resolves holds, verifies work, and retires this profile.
"""

VALID_REVIEW_PROCEDURE = """# Engineering HQ Worker Review Receipt Procedure

Procedure ID: `engineering_hq_worker_review_receipt`
Procedure Version: 1
Owner: Engineering HQ
Lifecycle State: Active

## Purpose
Review one validated Engineering Worker result.

## Authority
This procedure does not activate a Worker or broaden authority.

## Required Inputs
Inspect the exact assignment, immutable report, checksums, authority, and evidence.

## Deterministic Receipt Path
Create one immutable schema-valid receipt under the existing Worker result path.

## Allowed Review States
VERIFIED, REJECTED, REPAIR_REQUIRED, or ROB_VALIDATION_REQUIRED.

## Ingestion
Validate and attach the receipt to the existing execution row.

## Completion Condition
The immutable receipt is read back, ingested, and visible in Worker Operations.
"""


def _write_repository(repository_root: Path, *, profile: str = VALID_PROFILE) -> None:
    profile_path = repository_root / "projects/engineering/workers/engineering_worker.md"
    procedure_path = (
        repository_root
        / "projects/engineering/procedures/engineering_hq_worker_review_receipt.md"
    )
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    procedure_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(profile, encoding="utf-8")
    procedure_path.write_text(VALID_REVIEW_PROCEDURE, encoding="utf-8")


def _write_database(
    database_path: Path,
    *,
    paused: bool = False,
    budget_used: int = 0,
    budget_limit: int = 3,
    deployment_state: str = "enabled",
    route_availability: str = "available",
    unresolved_run: bool = False,
    include_execution_history: bool = True,
) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
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
            """
        )
        if include_execution_history:
            connection.execute(
                """
                CREATE TABLE execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    worker_id TEXT,
                    run_id TEXT,
                    result_state TEXT,
                    hq_review_state TEXT,
                    requires_rob_validation INTEGER,
                    ready_for_consumption INTEGER
                )
                """
            )
        connection.execute(
            """
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
                ?,
                1.0,
                1.0
            )
            """,
            (deployment_state,),
        )
        connection.execute(
            """
            INSERT INTO worker_route_state VALUES (
                'engineering_worker', ?, 1.0, NULL, 1.0
            )
            """,
            (route_availability,),
        )
        connection.execute(
            """
            INSERT INTO command_center_control VALUES (
                'shared_pause', ?, 'none', '', NULL, NULL, NULL, NULL, 1.0, ?, ?, 1
            )
            """,
            (int(paused), budget_limit, budget_used),
        )
        if unresolved_run and include_execution_history:
            connection.execute(
                """
                INSERT INTO execution_history(
                    worker_id, run_id, result_state, hq_review_state,
                    requires_rob_validation, ready_for_consumption
                ) VALUES (
                    'engineering_worker', 'RUN-UNRESOLVED',
                    'ROB_VALIDATION_REQUIRED', 'ROB_VALIDATION_REQUIRED', 1, 0
                )
                """
            )


def _fixture(
    tmp_path: Path,
    **database_options,
) -> tuple[Path, Path, WorkerActivationReadinessService]:
    repository_root = tmp_path / "repository"
    database_path = tmp_path / "runtime" / "command-center.sqlite3"
    _write_repository(repository_root)
    _write_database(database_path, **database_options)
    return (
        repository_root,
        database_path,
        WorkerActivationReadinessService(repository_root, database_path),
    )


def _finding(report, code: str):
    return next(item for item in report.findings if item.code == code)


def test_valid_prerequisites_are_ready_but_never_authorized(tmp_path: Path) -> None:
    repository_root, database_path, service = _fixture(tmp_path)
    profile_path = repository_root / "projects/engineering/workers/engineering_worker.md"
    procedure_path = (
        repository_root
        / "projects/engineering/procedures/engineering_hq_worker_review_receipt.md"
    )
    before_database = database_path.read_bytes()
    before_profile = profile_path.read_bytes()
    before_procedure = procedure_path.read_bytes()

    report = service.report("engineering_worker")

    assert report.state == "READY_FOR_AUTHORITY_REVIEW"
    assert report.technical_ready is True
    assert report.activation_authorized is False
    assert _finding(report, "profile.metadata").state == "PASS"
    assert _finding(report, "review.procedure_sections").state == "PASS"
    assert _finding(report, "runtime.shared_pause").state == "PASS"
    assert _finding(report, "runtime.send_budget").state == "PASS"
    assert _finding(report, "authority.owning_department").state == "NOT_APPLICABLE"
    assert database_path.read_bytes() == before_database
    assert profile_path.read_bytes() == before_profile
    assert procedure_path.read_bytes() == before_procedure


@pytest.mark.parametrize(
    ("options", "finding_code"),
    (
        ({"paused": True}, "runtime.shared_pause"),
        ({"budget_used": 3}, "runtime.send_budget"),
        ({"deployment_state": "retired"}, "runtime.deployment_state"),
        ({"route_availability": "unavailable"}, "runtime.route_availability"),
        ({"unresolved_run": True}, "runtime.unresolved_holds"),
    ),
)
def test_runtime_hold_conditions_fail_closed(
    tmp_path: Path,
    options: dict[str, object],
    finding_code: str,
) -> None:
    _, _, service = _fixture(tmp_path, **options)

    report = service.report("engineering_worker")

    assert report.state == "HOLD"
    assert report.technical_ready is False
    assert report.activation_authorized is False
    assert _finding(report, finding_code).state == "HOLD"


def test_missing_profile_holds(tmp_path: Path) -> None:
    repository_root, _, service = _fixture(tmp_path)
    (repository_root / "projects/engineering/workers/engineering_worker.md").unlink()

    report = service.report("engineering_worker")

    assert report.state == "HOLD"
    assert _finding(report, "profile.path").state == "HOLD"


def test_profile_metadata_or_section_drift_holds(tmp_path: Path) -> None:
    repository_root = tmp_path / "repository"
    database_path = tmp_path / "runtime" / "command-center.sqlite3"
    broken_profile = VALID_PROFILE.replace("profile_version: 1", "profile_version: 2").replace(
        "## Required evidence", "## Evidence"
    )
    _write_repository(repository_root, profile=broken_profile)
    _write_database(database_path)
    service = WorkerActivationReadinessService(repository_root, database_path)

    report = service.report("engineering_worker")

    assert report.state == "HOLD"
    assert _finding(report, "profile.metadata").state == "HOLD"
    assert _finding(report, "profile.sections").state == "HOLD"


def test_missing_execution_history_is_a_hold(tmp_path: Path) -> None:
    _, _, service = _fixture(tmp_path, include_execution_history=False)

    report = service.report("engineering_worker")

    assert report.state == "HOLD"
    assert _finding(report, "runtime.tables").state == "HOLD"


def test_worker_operations_status_embeds_ephemeral_activation_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository_root, database_path, readiness = _fixture(tmp_path)
    entry = WorkerRegistryEntry(
        worker_id="engineering_worker",
        chat_title="Engineering_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/engineering_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/g/project/c/engineering-worker",
        route_revision=1,
    )
    route = WorkerRouteState(
        worker_id="engineering_worker",
        availability="available",
        last_seen_at=1.0,
    )
    runtime = SimpleNamespace(
        workers=lambda: [entry],
        store=SimpleNamespace(route_state=lambda worker_id: route),
    )
    service = object.__new__(WorkerOperationsService)
    service.repository_root = repository_root
    service.activation_readiness = readiness
    service.worker_center = SimpleNamespace(
        runtime=runtime,
        browser_evidence=SimpleNamespace(history=lambda limit: []),
    )
    service.command_center = SimpleNamespace(
        paused=False,
        running=False,
        status=lambda: {"scheduler_running": False, "scheduled_jobs": [], "saved_prompts": []},
        pause_state=lambda: {"paused": False, "pause_kind": "none"},
        send_budget_state=lambda: {
            "limit": 3,
            "used": 0,
            "remaining": 3,
            "epoch": 1,
        },
    )
    service.verification = SimpleNamespace(status=lambda limit: {"summary": {}, "records": []})
    service.result_ingester = SimpleNamespace(status=lambda limit: {})
    service.result_repair = SimpleNamespace(status=lambda limit: {})
    service.hq_review = SimpleNamespace(status=lambda limit: {})
    service.rob_validation = SimpleNamespace(status=lambda limit: {})
    service.orchestrator = SimpleNamespace(status=lambda: {})
    service.cdp_endpoint = "http://127.0.0.1:9222"
    service._advisory_rows = lambda: ([], None)
    monkeypatch.setattr(
        worker_operations,
        "browser_health",
        lambda endpoint: {"available": False, "endpoint": endpoint},
    )
    before_database = database_path.read_bytes()

    payload = service.status()

    activation = payload["workers"][0]["activation"]
    assert activation["state"] == "READY_FOR_AUTHORITY_REVIEW"
    assert activation["activation_authorized"] is False
    assert payload["activation_summary"] == {
        "report_version": 1,
        "registered": 1,
        "ready_for_authority_review": 1,
        "held": 0,
        "activation_authorized": False,
    }
    assert database_path.read_bytes() == before_database
