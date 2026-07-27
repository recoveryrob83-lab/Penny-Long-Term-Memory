from __future__ import annotations

import sqlite3
import subprocess
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

import run_dashboard
from lifeos_dashboard import worker_pipeline_reliability_runtime as reliability
from lifeos_dashboard.worker_advisory_pipeline import ExecutionReadyAdvisory
from lifeos_dashboard.worker_result_contract import build_result_submission_contract
from lifeos_dashboard.worker_result_ingester import WorkerResultIngester
from lifeos_dashboard.worker_result_repair import REPAIR_ACCEPTED, WorkerResultRepairCoordinator
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry, WorkerRuntimeError


def _maintenance_advisory() -> ExecutionReadyAdvisory:
    contract = build_result_submission_contract(
        "maintenance",
        "maintenance_worker",
        "RUN-ADV-TEST-R1",
    )
    return ExecutionReadyAdvisory(
        advisory_id="ADV-TEST",
        title="Repository audit",
        board_path="coordination/boards/engineering.md",
        target_department="Maintenance HQ",
        target_worker_id="maintenance_worker",
        advisory_revision=1,
        task_class="coordinated_repository_repair",
        authorization_class="BOUNDED_WRITE",
        procedure_id="maintenance_coordinated_repository_repair",
        procedure_version=1,
        authorization_source="ROB",
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="OPEN",
        priority="NORMAL",
        source_references=("memory/HQ_NAMING_STANDARD.md",),
        requested_read_scopes=("memory", "coordination", "projects", "apps", "workers"),
        requested_write_scopes=("memory", "coordination", "projects", contract.result_path),
        requested_tools=("GitHub",),
        result_contract=contract,
    )


def _maintenance_profile() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="maintenance_worker",
        chat_title="Maintenance_Worker",
        owning_department="maintenance",
        profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
        profile_version=1,
    )


def _report_payload(advisory: ExecutionReadyAdvisory) -> dict[str, object]:
    contract = advisory.result_contract
    assert contract is not None
    return {
        "attempt": 1,
        "wrapper_id": "WAKE-ADV-TEST-R1",
        "run_id": "RUN-ADV-TEST-R1",
        "worker_id": "maintenance_worker",
        "profile_version": 1,
        "owning_department": "maintenance",
        "task_id": "ADV-TEST",
        "task_revision": 1,
        "procedure_id": "maintenance_coordinated_repository_repair",
        "procedure_version": 1,
        "authorization_source": "ROB",
        "verification_mode": "IMMEDIATE_HQ",
        "controlled_outcome": "REPORT_AND_HOLD",
        "completion_state": "partial",
        "verification_state": "pending",
        "failure_reason": "A bounded hold remains.",
        "actual_read_scopes": [
            "memory",
            "apps (read-only schema inspection)",
            "memory/HQ_NAMING_STANDARD.md",
        ],
        "actual_write_scopes": [
            "memory/HQ_NAMING_STANDARD.md",
            contract.result_path,
        ],
        "actual_tools": [
            "GitHub",
            "local non-mutating JSON schema and checksum validation",
        ],
        "evidence_references": [],
    }


def test_scope_matching_accepts_descendants_and_read_only_annotations() -> None:
    assert reliability._scope_allows("memory", "memory/HQ_NAMING_STANDARD.md") is True
    assert reliability._scope_allows("apps", "apps (read-only inspection)") is True
    assert reliability._scope_allows("memory", "coordination/ADVISORY_INDEX.md") is False


def test_evidence_parser_accepts_blob_and_commit_blob_witnesses() -> None:
    commit_sha = "a" * 40
    blob_sha = "b" * 40

    assert reliability._parse_evidence_reference(
        f"memory/file.md@commit:{commit_sha}@blob:{blob_sha}"
    ) == ("memory/file.md", commit_sha, blob_sha, False)
    assert reliability._parse_evidence_reference(
        f"memory/file.md@blob:{blob_sha}"
    ) == ("memory/file.md", None, blob_sha, False)
    assert reliability._parse_evidence_reference(
        "projects/result.json@preflight:not-found"
    ) == ("projects/result.json", None, None, True)


def test_maintenance_report_with_root_scopes_and_pinned_evidence_validates() -> None:
    advisory = _maintenance_advisory()
    commit_sha = "a" * 40
    blob_sha = "b" * 40
    ingester = WorkerResultIngester.__new__(WorkerResultIngester)

    def fake_git(*arguments: str) -> str:
        if arguments[:2] == ("cat-file", "-t"):
            return "commit" if arguments[2] == commit_sha else "blob"
        if arguments[0] == "rev-parse":
            return blob_sha
        raise AssertionError(arguments)

    ingester._git = fake_git  # type: ignore[method-assign]
    payload = _report_payload(advisory)
    payload["evidence_references"] = [
        f"memory/HQ_NAMING_STANDARD.md@commit:{commit_sha}@blob:{blob_sha}",
    ]

    reliability._validate_report_correlation(
        ingester,
        advisory,
        _maintenance_profile(),
        payload,
    )


def test_out_of_scope_write_still_fails_closed() -> None:
    advisory = _maintenance_advisory()
    contract = advisory.result_contract
    assert contract is not None
    ingester = WorkerResultIngester.__new__(WorkerResultIngester)
    ingester._git = lambda *arguments: "blob"  # type: ignore[method-assign]
    payload = _report_payload(advisory)
    payload["actual_write_scopes"] = ["apps/unsafe.py", contract.result_path]

    with pytest.raises(WorkerRuntimeError, match="actual write scopes exceed assignment"):
        reliability._validate_report_correlation(
            ingester,
            advisory,
            _maintenance_profile(),
            payload,
        )


def test_maintenance_artifact_paths_use_canonical_project_root() -> None:
    row = {"owning_department": "maintenance", "worker_id": "maintenance_worker"}

    assert reliability._canonical_artifact_path(
        row,
        "RUN-ADV-TEST-R1",
        "hq_review",
    ) == (
        "projects/life-logistics-hq/worker-results/maintenance_worker/"
        "RUN-ADV-TEST-R1/hq-review-001.json"
    )


def test_rejected_report_can_be_revalidated_without_creating_attempt_two(
    tmp_path: Path,
) -> None:
    advisory = _maintenance_advisory()
    database = tmp_path / "command-center.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history (
                id INTEGER PRIMARY KEY,
                run_id TEXT,
                result_state TEXT,
                report_attempt INTEGER,
                repair_state TEXT,
                next_report_attempt INTEGER
            )
            """
        )
        connection.execute(
            """
            INSERT INTO execution_history (
                run_id, result_state, report_attempt, repair_state, next_report_attempt
            ) VALUES (?, 'REPORT_REJECTED', 1, 'REPORT_REPAIR_PENDING', 2)
            """,
            (advisory.run_id,),
        )

    expected_receipt = SimpleNamespace(report_state="REPORT_VALIDATED")
    ingester = SimpleNamespace(
        _safe_path=lambda relative: tmp_path / relative,
        ingest=lambda active: expected_receipt,
    )
    coordinator = WorkerResultRepairCoordinator.__new__(WorkerResultRepairCoordinator)
    coordinator.ingester = ingester
    coordinator._row = lambda run_id: {
        "id": 1,
        "run_id": run_id,
        "result_state": "REPORT_REJECTED",
        "report_attempt": 1,
    }
    coordinator._connect = lambda: sqlite3.connect(database)

    receipt = coordinator.revalidate_rejected(advisory)

    assert receipt is expected_receipt
    with sqlite3.connect(database) as connection:
        state = connection.execute(
            "SELECT repair_state, next_report_attempt FROM execution_history"
        ).fetchone()
    assert state == (REPAIR_ACCEPTED, None)


def test_automatic_hq_wake_uses_guarded_budgeted_cli(monkeypatch, tmp_path: Path) -> None:
    state = {"hq_wake_state": None}
    row = {
        "id": 1,
        "run_id": "RUN-ADV-TEST-R1",
        "result_state": "REPORT_VALIDATED",
        "owning_department": "maintenance",
        "worker_id": "maintenance_worker",
        "hq_wake_state": None,
        "hq_review_state": None,
        "hq_wake_claimed_at": None,
    }
    events: list[tuple[str, str]] = []
    commands: list[list[str]] = []
    command_center = SimpleNamespace(
        paused=False,
        _run_lock=threading.Lock(),
        trip_safety_pause=lambda **kwargs: (_ for _ in ()).throw(AssertionError(kwargs)),
    )
    orchestrator = reliability.WorkerGitHubOrchestrator.__new__(
        reliability.WorkerGitHubOrchestrator
    )
    orchestrator.operations = SimpleNamespace(
        command_center=command_center,
        cdp_endpoint="http://127.0.0.1:9222",
    )
    orchestrator.app_root = tmp_path
    orchestrator.repository_root = tmp_path.parent
    orchestrator.database_path = tmp_path / "command-center.sqlite3"
    orchestrator.timeout_seconds = 300
    orchestrator._artifact_exists = lambda path: False
    orchestrator._ingest_hq_review_if_present = lambda run_id, advisory_id: None
    orchestrator._event = (
        lambda action, status, detail, **kwargs: events.append((action, status))
    )

    def current_row(run_id: str):
        current = dict(row)
        current["hq_wake_state"] = state["hq_wake_state"]
        return current

    orchestrator._row = current_row
    monkeypatch.setattr(reliability, "_ensure_hq_wake_claim_column", lambda item: None)
    monkeypatch.setattr(reliability, "_claim_hq_wake", lambda item, item_row: True)

    def fake_run(command, **kwargs):
        commands.append(command)
        state["hq_wake_state"] = "HQ_WAKE_SUBMITTED"
        return subprocess.CompletedProcess(command, 0, stdout="HQ_REVIEW_WAKE_OK\n", stderr="")

    monkeypatch.setattr(reliability.subprocess, "run", fake_run)

    reliability._send_hq_wake(orchestrator, "RUN-ADV-TEST-R1", "ADV-TEST")

    assert commands
    assert Path(commands[0][1]).name == "run_worker_hq_review_wake.py"
    assert commands[0][-2:] == ["--confirm-send", "HQ_REVIEW_SEND"]
    assert events[-1] == ("hq_review_wake", "succeeded")


def test_plain_dashboard_start_enables_continuation_not_auto_dispatch(monkeypatch) -> None:
    monkeypatch.delenv("LIFEOS_WORKER_ORCHESTRATOR_ENABLED", raising=False)
    monkeypatch.delenv("LIFEOS_WORKER_AUTO_DISPATCH_ENABLED", raising=False)
    monkeypatch.setenv("LIFEOS_OPEN_BROWSER", "0")
    observed: dict[str, object] = {}
    monkeypatch.setattr(
        run_dashboard.uvicorn,
        "run",
        lambda *args, **kwargs: observed.update(kwargs),
    )

    run_dashboard.main()

    assert observed["host"] == "127.0.0.1"
    assert observed["port"] == 8765
    assert reliability._truthy_environment(
        "LIFEOS_WORKER_ORCHESTRATOR_ENABLED"
    ) is True
    assert reliability._truthy_environment(
        "LIFEOS_WORKER_AUTO_DISPATCH_ENABLED"
    ) is False
