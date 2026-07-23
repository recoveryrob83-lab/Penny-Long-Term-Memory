"""Install the GitHub-first Worker orchestration loop on Worker Operations."""
from __future__ import annotations

import atexit
import os
from pathlib import Path

from . import worker_operations
from .worker_github_orchestrator import WorkerGitHubOrchestrator

_INSTALL_FLAG = "_lifeos_worker_github_orchestrator_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_github_orchestrator_service_installed"


def _environment_int(name: str, default: int) -> int:
    value = str(os.getenv(name) or "").strip()
    if not value:
        return default
    return int(value)


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
    _install_service()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_github_orchestrator_runtime()


__all__ = ["install_worker_github_orchestrator_runtime"]
