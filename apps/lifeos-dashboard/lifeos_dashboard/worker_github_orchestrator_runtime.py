"""Install the GitHub-first Worker orchestration loop on Worker Operations.

The runtime also installs a fail-closed HQ-wake guard. Immutable Git review
evidence is ingested before any browser wake is attempted, and an atomic local
claim prevents concurrent or uncertain wake attempts from ringing the same HQ
doorbell repeatedly.
"""
from __future__ import annotations

import atexit
import os
import time
from pathlib import Path

from . import worker_operations
from .worker_github_orchestrator import WorkerGitHubOrchestrator

_INSTALL_FLAG = "_lifeos_worker_github_orchestrator_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_github_orchestrator_service_installed"
_HQ_WAKE_GUARD_FLAG = "_lifeos_worker_hq_wake_guard_installed"
_HQ_WAKE_CLAIM_COLUMN = "hq_wake_claimed_at"


def _environment_int(name: str, default: int) -> int:
    value = str(os.getenv(name) or "").strip()
    if not value:
        return default
    return int(value)


def _hq_review_path(row, run_id: str) -> str:
    return (
        f"projects/{row['owning_department']}/worker-results/{row['worker_id']}/"
        f"{run_id}/hq-review-001.json"
    )


def _ensure_hq_wake_claim_column(orchestrator: WorkerGitHubOrchestrator) -> None:
    with orchestrator._connect() as connection:  # noqa: SLF001 - runtime schema extension
        existing = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(execution_history)").fetchall()
        }
        if _HQ_WAKE_CLAIM_COLUMN not in existing:
            connection.execute(
                f"ALTER TABLE execution_history ADD COLUMN {_HQ_WAKE_CLAIM_COLUMN} REAL"
            )


def _claim_hq_wake(orchestrator: WorkerGitHubOrchestrator, row) -> bool:
    """Atomically claim one pending HQ wake across threads and processes."""

    with orchestrator._connect() as connection:  # noqa: SLF001 - same-row transport guard
        updated = connection.execute(
            f"""
            UPDATE execution_history
            SET {_HQ_WAKE_CLAIM_COLUMN} = ?
            WHERE id = ?
              AND result_state = 'REPORT_VALIDATED'
              AND COALESCE(hq_wake_state, '') = ''
              AND COALESCE(hq_review_state, '') = ''
              AND {_HQ_WAKE_CLAIM_COLUMN} IS NULL
            """,
            (time.time(), int(row["id"])),
        )
    return updated.rowcount == 1


def _install_hq_wake_guard() -> None:
    orchestrator_class = WorkerGitHubOrchestrator
    if getattr(orchestrator_class, _HQ_WAKE_GUARD_FLAG, False):
        return

    original_initialize = orchestrator_class._initialize
    original_send_hq_wake = orchestrator_class._send_hq_wake

    def initialize(self: WorkerGitHubOrchestrator) -> None:
        original_initialize(self)
        _ensure_hq_wake_claim_column(self)

    def send_hq_wake(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
            return

        review_path = _hq_review_path(row, run_id)
        if self._artifact_exists(review_path):
            # Git is authoritative. Consume the immutable receipt before any
            # browser transport can repeat a stale HQ wake.
            self._ingest_hq_review_if_present(run_id, advisory_id)
            return

        if str(row["hq_wake_state"] or "") or str(row["hq_review_state"] or ""):
            return

        command_center = self.operations.command_center
        if command_center.paused:
            return
        run_lock = command_center._run_lock  # noqa: SLF001 - shared browser execution gate
        if run_lock.locked():
            return

        _ensure_hq_wake_claim_column(self)
        row = self._row(run_id)
        if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
            return
        if self._artifact_exists(_hq_review_path(row, run_id)):
            self._ingest_hq_review_if_present(run_id, advisory_id)
            return
        if str(row["hq_wake_state"] or "") or str(row["hq_review_state"] or ""):
            return

        claimed_at = row[_HQ_WAKE_CLAIM_COLUMN]
        if claimed_at is not None or not _claim_hq_wake(self, row):
            self._event(
                "hq_review_wake",
                "suppressed",
                "A prior HQ wake claim exists; automatic duplicate dispatch was suppressed.",
                run_id=run_id,
                advisory_id=advisory_id,
            )
            return

        try:
            original_send_hq_wake(self, run_id, advisory_id)
        except Exception:
            self._event(
                "hq_review_wake",
                "held",
                "HQ wake transport became uncertain after the atomic claim; automatic retry is suppressed.",
                run_id=run_id,
                advisory_id=advisory_id,
            )
            raise

        current = self._row(run_id)
        if (
            current is not None
            and not str(current["hq_wake_state"] or "")
            and not str(current["hq_review_state"] or "")
            and not self._artifact_exists(_hq_review_path(current, run_id))
        ):
            self._event(
                "hq_review_wake",
                "held",
                "HQ wake claim exists without persisted submission evidence; automatic retry is suppressed.",
                run_id=run_id,
                advisory_id=advisory_id,
            )

    orchestrator_class._initialize = initialize
    orchestrator_class._send_hq_wake = send_hq_wake
    setattr(orchestrator_class, _HQ_WAKE_GUARD_FLAG, True)


def _install_service() -> None:
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _SERVICE_FLAG, False):
        return
    original_init = service_class.__init__
    original_status = service_class.status

    def __init__(self, command_center, repository_root: Path, *, cdp_endpoint=None) -> None:
        original_init(
            self,
            command_center,
            repository_root,
            cdp_endpoint=cdp_endpoint,
        )
        self.orchestrator = WorkerGitHubOrchestrator(
            self,
            repository_root,
            Path(command_center.store.database_path),
            poll_seconds=_environment_int("LIFEOS_WORKER_ORCHESTRATOR_POLL_SECONDS", 30),
            sync_branch=os.getenv("LIFEOS_GITHUB_SYNC_BRANCH", "main"),
            timeout_seconds=_environment_int("LIFEOS_WORKER_ORCHESTRATOR_TIMEOUT_SECONDS", 300),
        )
        if str(os.getenv("LIFEOS_WORKER_ORCHESTRATOR_ENABLED") or "").strip().casefold() in {
            "1",
            "true",
            "yes",
            "on",
        }:
            self.orchestrator.start()
            atexit.register(self.orchestrator.stop)

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["orchestrator"] = self.orchestrator.status()
        return payload

    def start_orchestrator(self) -> bool:
        return self.orchestrator.start()

    def stop_orchestrator(self) -> bool:
        return self.orchestrator.stop()

    def run_orchestrator_once(self) -> dict[str, object]:
        return self.orchestrator.run_once()

    service_class.__init__ = __init__
    service_class.status = status
    service_class.start_orchestrator = start_orchestrator
    service_class.stop_orchestrator = stop_orchestrator
    service_class.run_orchestrator_once = run_orchestrator_once
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_github_orchestrator_runtime() -> bool:
    """Install the GitHub-first orchestration service once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    _install_hq_wake_guard()
    _install_service()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_github_orchestrator_runtime()


__all__ = [
    "_claim_hq_wake",
    "_ensure_hq_wake_claim_column",
    "_hq_review_path",
    "install_worker_github_orchestrator_runtime",
]
