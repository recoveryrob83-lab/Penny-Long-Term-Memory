"""GitHub-first local orchestration for LifeOS Worker operations.

GitHub remains the operational desk and communication layer. SQLite is used only
for local dispatch deduplication, locks, restart recovery, and transport state.
This orchestrator does not create authority, close advisories, or report to
Chief of Staff. Chief of Staff reads GitHub directly.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from .worker_dispatch_runtime import parse_browser_dispatch_receipt
from .worker_runtime import WorkerRuntimeError

if TYPE_CHECKING:
    from .worker_advisory_pipeline import ExecutionReadyAdvisory
    from .worker_operations import WorkerOperationsService


@dataclass(frozen=True)
class WorkerOrchestratorEvent:
    occurred_at: float
    action: str
    status: str
    run_id: str | None
    advisory_id: str | None
    detail: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerGitHubOrchestrator:
    """Continuously connect GitHub advisories, Worker results, and HQ review."""

    def __init__(
        self,
        operations: WorkerOperationsService,
        repository_root: Path,
        database_path: Path,
        *,
        poll_seconds: int = 30,
        sync_branch: str = "main",
        timeout_seconds: int = 300,
    ) -> None:
        if poll_seconds < 10:
            raise WorkerRuntimeError("Worker orchestrator poll interval must be at least 10 seconds.")
        if timeout_seconds < 60 or timeout_seconds > 900:
            raise WorkerRuntimeError("Worker orchestrator timeout must be between 60 and 900 seconds.")
        self.operations = operations
        self.repository_root = repository_root.resolve()
        self.database_path = database_path
        self.app_root = Path(operations.command_center.app_root).resolve()
        self.poll_seconds = poll_seconds
        self.sync_branch = str(sync_branch or "main").strip()
        self.timeout_seconds = timeout_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._cycle_lock = threading.Lock()
        self._events: list[WorkerOrchestratorEvent] = []
        self._last_cycle_started_at: float | None = None
        self._last_cycle_finished_at: float | None = None
        self._last_error: str | None = None

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _event(
        self,
        action: str,
        status: str,
        detail: str,
        *,
        run_id: str | None = None,
        advisory_id: str | None = None,
    ) -> None:
        self._events.append(
            WorkerOrchestratorEvent(
                occurred_at=time.time(),
                action=action,
                status=status,
                run_id=run_id,
                advisory_id=advisory_id,
                detail=detail,
            )
        )
        del self._events[:-100]

    def _git(self, *arguments: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repository_root), *arguments],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

    def _safe_git_sync(self) -> str:
        status = self._git("status", "--porcelain")
        if status.returncode != 0:
            raise WorkerRuntimeError((status.stderr or status.stdout).strip() or "Git status failed.")
        if status.stdout.strip():
            return "Local repository has uncommitted changes; Git sync was skipped."

        fetched = self._git("fetch", "origin", self.sync_branch, timeout=120)
        if fetched.returncode != 0:
            raise WorkerRuntimeError((fetched.stderr or fetched.stdout).strip() or "Git fetch failed.")

        counts = self._git(
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...origin/{self.sync_branch}",
        )
        if counts.returncode != 0:
            raise WorkerRuntimeError(
                (counts.stderr or counts.stdout).strip() or "Git divergence check failed."
            )
        try:
            ahead_text, behind_text = counts.stdout.strip().split()
            ahead, behind = int(ahead_text), int(behind_text)
        except (ValueError, TypeError) as exc:
            raise WorkerRuntimeError("Git divergence check returned an invalid result.") from exc

        if ahead and behind:
            return "Local and remote branches diverged; automatic sync was safely skipped."
        if ahead:
            return "Local branch is ahead of remote; automatic sync was safely skipped."
        if not behind:
            return "Git repository is current."

        merged = self._git("merge", "--ff-only", f"origin/{self.sync_branch}", timeout=120)
        if merged.returncode != 0:
            raise WorkerRuntimeError(
                (merged.stderr or merged.stdout).strip() or "Fast-forward Git sync failed."
            )
        return f"Git repository fast-forwarded by {behind} commit(s)."

    def _row(self, run_id: str) -> sqlite3.Row | None:
        with self._connect() as connection:
            return connection.execute(
                """
                SELECT * FROM execution_history
                WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
                ORDER BY id DESC LIMIT 1
                """,
                (run_id,),
            ).fetchone()

    def _artifact_exists(self, relative_path: str | None) -> bool:
        if not relative_path:
            return False
        candidate = (self.repository_root / relative_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError:
            return False
        return candidate.is_file()

    def _dispatch_new(self, advisories: tuple[ExecutionReadyAdvisory, ...]) -> None:
        for advisory in advisories:
            envelope = advisory.envelope()
            if self.operations.worker_center.history.successful_send_exists(
                envelope.idempotency_key
            ):
                continue
            dispatch = self.operations.pipeline.dispatch(
                advisory.advisory_id,
                mode="send",
                confirm_send=True,
                trigger="scheduled",
                timeout_seconds=self.timeout_seconds,
            )
            self._event(
                "worker_dispatch",
                dispatch.result.status,
                dispatch.result.reason,
                run_id=advisory.run_id,
                advisory_id=advisory.advisory_id,
            )

    def _ingest_result_if_present(self, advisory: ExecutionReadyAdvisory) -> None:
        contract = advisory.result_contract
        if contract is None or not self._artifact_exists(contract.result_path):
            return
        row = self._row(advisory.run_id)
        if row is not None and str(row["result_state"] or "") in {
            "REPORT_VALIDATED",
            "REPORT_REJECTED",
            "REPORT_REPAIR_PENDING",
            "HQ_VERIFIED",
            "HQ_REJECTED",
            "ROB_VALIDATION_REQUIRED",
            "ROB_VERIFIED",
            "ROB_REJECTED",
            "READY_FOR_COS",
        }:
            return
        payload = self.operations.ingest_result(advisory.run_id)
        receipt = payload.get("receipt") or {}
        self._event(
            "result_ingestion",
            "succeeded",
            f"Worker result reached {receipt.get('report_state') or receipt.get('result_state')}.",
            run_id=advisory.run_id,
            advisory_id=advisory.advisory_id,
        )

    def _send_hq_wake(self, run_id: str, advisory_id: str) -> None:
        row = self._row(run_id)
        if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
            return
        if str(row["hq_wake_state"] or "") or str(row["hq_review_state"] or ""):
            return

        wake = self.operations.hq_review.build_wake(run_id)
        command_center = self.operations.command_center
        if command_center.paused:
            return
        run_lock = command_center._run_lock  # noqa: SLF001 - shared browser execution gate
        if not run_lock.acquire(blocking=False):
            return
        try:
            command = [
                sys.executable,
                str(self.app_root / "automation" / "chatgpt_worker_browser_dispatch.py"),
                "--worker-chat-title",
                wake.hq_chat_title,
                "--project-title",
                os.getenv("LIFEOS_CHATGPT_PROJECT_TITLE", "Life OS"),
                "--text",
                wake.instruction,
                "--request-marker",
                wake.marker,
                "--response-marker",
                wake.run_id,
                "--cdp-endpoint",
                self.operations.cdp_endpoint,
                "--timeout-seconds",
                str(self.timeout_seconds),
                "--send",
                "--confirm-send",
                "SEND",
            ]
            completed = subprocess.run(
                command,
                cwd=self.app_root,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds + 30,
                check=False,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise WorkerRuntimeError(detail or "Owning-HQ wake failed.")
            receipt = parse_browser_dispatch_receipt(completed.stdout)
            self.operations.hq_review.record_wake(run_id, receipt)
        finally:
            run_lock.release()
        self._event(
            "hq_review_wake",
            "succeeded",
            f"Owning HQ was woken for {run_id}.",
            run_id=run_id,
            advisory_id=advisory_id,
        )

    def _ingest_hq_review_if_present(self, run_id: str, advisory_id: str) -> None:
        row = self._row(run_id)
        if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
            return
        if str(row["hq_review_state"] or ""):
            return
        review_path = (
            f"projects/{row['owning_department']}/worker-results/{row['worker_id']}/"
            f"{run_id}/hq-review-001.json"
        )
        if not self._artifact_exists(review_path):
            return
        payload = self.operations.ingest_hq_review(run_id)
        receipt = payload.get("receipt") or {}
        self._event(
            "hq_review_ingestion",
            "succeeded",
            f"HQ review reached {receipt.get('result_state') or receipt.get('review_state')}.",
            run_id=run_id,
            advisory_id=advisory_id,
        )

    def _ingest_rob_validation_if_present(self, run_id: str, advisory_id: str) -> None:
        row = self._row(run_id)
        if row is None or not bool(row["requires_rob_validation"]):
            return
        if str(row["rob_validation_state"] or ""):
            return
        validation_path = (
            f"projects/{row['owning_department']}/worker-results/{row['worker_id']}/"
            f"{run_id}/rob-validation-001.json"
        )
        if not self._artifact_exists(validation_path):
            return
        payload = self.operations.ingest_rob_validation(run_id)
        receipt = payload.get("receipt") or {}
        self._event(
            "rob_validation_ingestion",
            "succeeded",
            f"Rob validation reached {receipt.get('result_state') or receipt.get('validation_state')}.",
            run_id=run_id,
            advisory_id=advisory_id,
        )

    def run_once(self) -> dict[str, object]:
        if not self._cycle_lock.acquire(blocking=False):
            return self.status()
        self._last_cycle_started_at = time.time()
        self._last_error = None
        try:
            if self.operations.command_center.paused:
                self._event("cycle", "paused", "Automation is paused.")
                return self.status()

            sync_detail = self._safe_git_sync()
            self._event("git_sync", "succeeded", sync_detail)
            if "skipped" in sync_detail:
                return self.status()

            advisories = self.operations.pipeline.discover()
            self._dispatch_new(advisories)

            for advisory in advisories:
                self._ingest_result_if_present(advisory)
                self._send_hq_wake(advisory.run_id, advisory.advisory_id)
                self._ingest_hq_review_if_present(advisory.run_id, advisory.advisory_id)
                self._ingest_rob_validation_if_present(advisory.run_id, advisory.advisory_id)
            return self.status()
        except (OSError, sqlite3.Error, subprocess.TimeoutExpired, WorkerRuntimeError, ValueError) as exc:
            self._last_error = str(exc)
            self._event("cycle", "stopped", str(exc))
            return self.status()
        finally:
            self._last_cycle_finished_at = time.time()
            self._cycle_lock.release()

    def _loop(self) -> None:
        while not self._stop.is_set():
            self.run_once()
            self._stop.wait(self.poll_seconds)

    def start(self) -> bool:
        if self._thread is not None and self._thread.is_alive():
            return False
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop,
            name="lifeos-worker-orchestrator",
            daemon=True,
        )
        self._thread.start()
        return True

    def stop(self, timeout: float = 5.0) -> bool:
        thread = self._thread
        if thread is None:
            return False
        self._stop.set()
        thread.join(timeout)
        self._thread = None
        return True

    def status(self) -> dict[str, object]:
        thread = self._thread
        return {
            "enabled": True,
            "running": bool(thread and thread.is_alive()),
            "poll_seconds": self.poll_seconds,
            "sync_branch": self.sync_branch,
            "last_cycle_started_at": self._last_cycle_started_at,
            "last_cycle_finished_at": self._last_cycle_finished_at,
            "last_error": self._last_error,
            "events": [event.to_dict() for event in reversed(self._events[-25:])],
        }


__all__ = ["WorkerGitHubOrchestrator", "WorkerOrchestratorEvent"]
