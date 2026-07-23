from __future__ import annotations

import sqlite3
import subprocess
import threading
from pathlib import Path
from types import SimpleNamespace

from lifeos_dashboard.worker_github_orchestrator import WorkerGitHubOrchestrator
from lifeos_dashboard.worker_github_orchestrator_runtime import (
    _claim_hq_wake,
    _ensure_hq_wake_claim_column,
)


def _git(path: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def test_safe_git_sync_fast_forwards_clean_checkout(tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    writer = tmp_path / "writer"
    reader = tmp_path / "reader"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "clone", str(remote), str(writer)], check=True, capture_output=True)
    _git(writer, "config", "user.email", "test@example.com")
    _git(writer, "config", "user.name", "Test")
    (writer / "memory").mkdir()
    (writer / "memory" / "STARTUP_BOOT.md").write_text("boot\n", encoding="utf-8")
    _git(writer, "add", ".")
    _git(writer, "commit", "-m", "initial")
    _git(writer, "branch", "-M", "main")
    _git(writer, "push", "-u", "origin", "main")
    subprocess.run(
        ["git", "--git-dir", str(remote), "symbolic-ref", "HEAD", "refs/heads/main"],
        check=True,
    )
    subprocess.run(["git", "clone", str(remote), str(reader)], check=True, capture_output=True)

    (writer / "coordination").mkdir()
    (writer / "coordination" / "ADVISORY_INDEX.md").write_text("index\n", encoding="utf-8")
    _git(writer, "add", ".")
    _git(writer, "commit", "-m", "add index")
    _git(writer, "push")

    orchestrator = WorkerGitHubOrchestrator.__new__(WorkerGitHubOrchestrator)
    orchestrator.repository_root = reader
    orchestrator.sync_branch = "main"
    detail = orchestrator._safe_git_sync()

    assert "fast-forwarded by 1 commit" in detail
    assert (reader / "coordination" / "ADVISORY_INDEX.md").read_text(encoding="utf-8") == "index\n"


def test_run_once_connects_existing_steps_without_new_policy(monkeypatch) -> None:
    advisory = SimpleNamespace(run_id="RUN-1", advisory_id="ADV-1")
    operations = SimpleNamespace(
        command_center=SimpleNamespace(paused=False),
        pipeline=SimpleNamespace(discover=lambda: (advisory,)),
    )
    orchestrator = WorkerGitHubOrchestrator.__new__(WorkerGitHubOrchestrator)
    orchestrator.operations = operations
    orchestrator._cycle_lock = threading.Lock()
    orchestrator._events = []
    orchestrator._last_cycle_started_at = None
    orchestrator._last_cycle_finished_at = None
    orchestrator._last_error = None
    orchestrator.poll_seconds = 30
    orchestrator.sync_branch = "main"
    orchestrator._thread = None
    calls: list[str] = []

    monkeypatch.setattr(orchestrator, "_safe_git_sync", lambda: "Git repository is current.")
    monkeypatch.setattr(orchestrator, "_dispatch_new", lambda items: calls.append("dispatch"))
    monkeypatch.setattr(orchestrator, "_ingest_result_if_present", lambda item: calls.append("result"))
    monkeypatch.setattr(orchestrator, "_send_hq_wake", lambda run_id, advisory_id: calls.append("hq"))
    monkeypatch.setattr(
        orchestrator,
        "_ingest_hq_review_if_present",
        lambda run_id, advisory_id: calls.append("review"),
    )
    monkeypatch.setattr(
        orchestrator,
        "_ingest_rob_validation_if_present",
        lambda run_id, advisory_id: calls.append("rob"),
    )

    result = orchestrator.run_once()

    assert calls == ["dispatch", "result", "hq", "review", "rob"]
    assert result["last_error"] is None


def test_hq_review_artifact_is_ingested_before_browser_wake(monkeypatch) -> None:
    row = {
        "id": 1,
        "run_id": "RUN-1",
        "result_state": "REPORT_VALIDATED",
        "owning_department": "engineering",
        "worker_id": "engineering_worker",
        "hq_wake_state": None,
        "hq_review_state": None,
    }
    orchestrator = WorkerGitHubOrchestrator.__new__(WorkerGitHubOrchestrator)
    calls: list[str] = []

    monkeypatch.setattr(orchestrator, "_row", lambda run_id: row)
    monkeypatch.setattr(
        orchestrator,
        "_artifact_exists",
        lambda path: path.endswith("RUN-1/hq-review-001.json"),
    )
    monkeypatch.setattr(
        orchestrator,
        "_ingest_hq_review_if_present",
        lambda run_id, advisory_id: calls.append(f"ingest:{run_id}:{advisory_id}"),
    )

    orchestrator._send_hq_wake("RUN-1", "ADV-1")

    assert calls == ["ingest:RUN-1:ADV-1"]


def test_hq_wake_claim_is_atomic_across_repeat_attempts(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history (
                id INTEGER PRIMARY KEY,
                run_id TEXT,
                mode TEXT,
                prompt_type TEXT,
                result_state TEXT,
                hq_wake_state TEXT,
                hq_review_state TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO execution_history (
                run_id, mode, prompt_type, result_state, hq_wake_state, hq_review_state
            ) VALUES ('RUN-1', 'send', 'worker', 'REPORT_VALIDATED', NULL, NULL)
            """
        )

    orchestrator = WorkerGitHubOrchestrator.__new__(WorkerGitHubOrchestrator)
    orchestrator.database_path = database
    _ensure_hq_wake_claim_column(orchestrator)
    first_row = orchestrator._row("RUN-1")

    assert first_row is not None
    assert _claim_hq_wake(orchestrator, first_row) is True

    second_row = orchestrator._row("RUN-1")
    assert second_row is not None
    assert second_row["hq_wake_claimed_at"] is not None
    assert _claim_hq_wake(orchestrator, second_row) is False


def test_run_once_stops_before_work_when_git_is_not_safe(monkeypatch) -> None:
    operations = SimpleNamespace(
        command_center=SimpleNamespace(paused=False),
        pipeline=SimpleNamespace(discover=lambda: (_ for _ in ()).throw(AssertionError("not called"))),
    )
    orchestrator = WorkerGitHubOrchestrator.__new__(WorkerGitHubOrchestrator)
    orchestrator.operations = operations
    orchestrator._cycle_lock = threading.Lock()
    orchestrator._events = []
    orchestrator._last_cycle_started_at = None
    orchestrator._last_cycle_finished_at = None
    orchestrator._last_error = None
    orchestrator.poll_seconds = 30
    orchestrator.sync_branch = "main"
    orchestrator._thread = None
    monkeypatch.setattr(
        orchestrator,
        "_safe_git_sync",
        lambda: "Local and remote branches diverged; automatic sync was safely skipped.",
    )

    result = orchestrator.run_once()

    assert result["last_error"] is None
    assert result["events"][0]["action"] == "git_sync"
