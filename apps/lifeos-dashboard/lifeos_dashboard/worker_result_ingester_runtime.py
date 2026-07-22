"""Install Package E Slice 4 deterministic Worker result ingestion and repair."""
from __future__ import annotations

from pathlib import Path

from . import worker_operations
from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_result_ingester import WorkerResultIngester
from .worker_result_repair import WorkerResultRepairCoordinator
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_result_ingester_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_result_ingester_service_installed"

# Execution-ready advisories use ``advisory_id`` as the canonical task ID in their envelope.
# Keep one read-only alias for repair-wake rendering without introducing another identifier.
if not hasattr(ExecutionReadyAdvisory, "task_id"):
    setattr(ExecutionReadyAdvisory, "task_id", property(lambda self: self.advisory_id))


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
        database_path = Path(command_center.store.database_path)
        self.result_ingester = WorkerResultIngester(
            repository_root,
            database_path,
            runtime=self.worker_center.runtime,
        )
        self.result_repair = WorkerResultRepairCoordinator(self.result_ingester)

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["result_ingestion"] = self.result_ingester.status(limit=100)
        payload["result_repair"] = self.result_repair.status(limit=100)
        return payload

    def ingest_result(self, run_id: str) -> dict[str, object]:
        clean_run_id = str(run_id or "").strip()
        if not clean_run_id:
            raise WorkerRuntimeError("run_id cannot be empty.")
        matches = [
            advisory
            for advisory in self.pipeline.discover()
            if advisory.run_id == clean_run_id and advisory.result_contract is not None
        ]
        if not matches:
            raise WorkerRuntimeError(
                f"No OPEN execution-ready Worker result assignment matches {clean_run_id}."
            )
        if len(matches) > 1:
            raise WorkerRuntimeError(f"Worker result assignment {clean_run_id} is ambiguous.")
        receipt = self.result_repair.ingest_next(matches[0])
        return {
            "status": "succeeded",
            "receipt": receipt.to_dict(),
            "result_ingestion": self.result_ingester.status(limit=100),
            "result_repair": self.result_repair.status(limit=100),
            "verification": self.verification.status(limit=100),
        }

    service_class.__init__ = __init__
    service_class.status = status
    service_class.ingest_result = ingest_result
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_result_ingester_runtime() -> bool:
    """Install deterministic result ingestion and correction-only repair once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    _install_service()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_result_ingester_runtime()


__all__ = ["install_worker_result_ingester_runtime"]
