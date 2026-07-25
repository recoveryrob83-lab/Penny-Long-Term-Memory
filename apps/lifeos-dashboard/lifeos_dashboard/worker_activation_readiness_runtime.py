"""Expose read-only Worker activation prerequisite reports through Worker Operations status."""
from __future__ import annotations

from pathlib import Path

from . import worker_operations
from .worker_activation_readiness import WorkerActivationReadinessService

_INSTALL_FLAG = "_lifeos_worker_activation_readiness_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_activation_readiness_service_installed"


def _install_worker_operations_readiness() -> None:
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _SERVICE_FLAG, False):
        return

    original_init = service_class.__init__
    original_worker_rows = service_class._worker_rows
    original_status = service_class.status

    def __init__(self, *args, **kwargs) -> None:
        original_init(self, *args, **kwargs)
        database_path = Path(self.command_center.store.database_path)
        self.activation_readiness = WorkerActivationReadinessService(
            self.repository_root,
            database_path,
        )

    def activation_report(self, worker_id: str) -> dict[str, object]:
        return self.activation_readiness.report(worker_id).to_dict()

    def _worker_rows(self) -> list[dict[str, object]]:
        rows = original_worker_rows(self)
        for row in rows:
            worker_id = str(row.get("worker_id") or "")
            row["activation"] = activation_report(self, worker_id)
        return rows

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        workers = payload.get("workers")
        worker_rows = workers if isinstance(workers, list) else []
        readiness_rows = [
            row.get("activation")
            for row in worker_rows
            if isinstance(row, dict) and isinstance(row.get("activation"), dict)
        ]
        payload["activation_summary"] = {
            "report_version": 1,
            "registered": len(readiness_rows),
            "ready_for_authority_review": sum(
                report.get("state") == "READY_FOR_AUTHORITY_REVIEW"
                for report in readiness_rows
            ),
            "held": sum(report.get("state") == "HOLD" for report in readiness_rows),
            "activation_authorized": False,
        }
        return payload

    service_class.__init__ = __init__
    service_class.activation_report = activation_report
    service_class._worker_rows = _worker_rows
    service_class.status = status
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_activation_readiness_runtime() -> bool:
    """Install the status-only activation prerequisite report once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    _install_worker_operations_readiness()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_activation_readiness_runtime()


__all__ = ["install_worker_activation_readiness_runtime"]
