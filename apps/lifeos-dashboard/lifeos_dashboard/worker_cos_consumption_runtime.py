"""Install Package E Slice 7 Chief of Staff consumption services."""
from __future__ import annotations

from pathlib import Path

from . import worker_operations
from .worker_cos_consumption import WorkerCosConsumptionService
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_cos_consumption_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_cos_consumption_service_installed"


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
        self.cos_consumption = WorkerCosConsumptionService(
            repository_root,
            Path(command_center.store.database_path),
        )

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["cos_consumption"] = self.cos_consumption.status(limit=100)
        return payload

    def preview_cos_consumption(self, run_ids=None) -> dict[str, object]:
        preview = self.cos_consumption.preview(run_ids)
        return {
            "status": "succeeded",
            "preview": preview.to_dict(),
            "cos_consumption": self.cos_consumption.status(limit=100),
        }

    def acknowledge_cos_consumption(
        self, batch_id: str, run_ids, *, confirm: bool
    ) -> dict[str, object]:
        if not confirm:
            raise WorkerRuntimeError(
                "Chief of Staff consumption acknowledgement requires explicit confirmation."
            )
        receipt = self.cos_consumption.acknowledge(batch_id, run_ids)
        return {
            "status": "succeeded",
            "receipt": receipt.to_dict(),
            "cos_consumption": self.cos_consumption.status(limit=100),
        }

    service_class.__init__ = __init__
    service_class.status = status
    service_class.preview_cos_consumption = preview_cos_consumption
    service_class.acknowledge_cos_consumption = acknowledge_cos_consumption
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_cos_consumption_runtime() -> bool:
    """Install the Slice 7 same-row consumption extension once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    _install_service()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_cos_consumption_runtime()


__all__ = ["install_worker_cos_consumption_runtime"]
