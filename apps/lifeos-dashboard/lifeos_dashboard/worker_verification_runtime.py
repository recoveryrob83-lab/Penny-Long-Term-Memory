"""Attach the Worker verification view to existing Command Center status output."""
from __future__ import annotations

from pathlib import Path

from . import command_center
from .worker_verification import WorkerVerificationService

_INSTALL_FLAG = "_lifeos_worker_verification_status_installed"
_SERVICE_ATTR = "_lifeos_worker_verification_service"


def install_worker_verification_status() -> bool:
    """Extend status once without creating another API or durable queue."""

    if getattr(command_center.CommandCenterService, _INSTALL_FLAG, False):
        return False
    original_status = command_center.CommandCenterService.status

    def status(self: command_center.CommandCenterService) -> dict[str, object]:
        payload = original_status(self)
        service = getattr(self, _SERVICE_ATTR, None)
        if not isinstance(service, WorkerVerificationService):
            service = WorkerVerificationService(Path(self.store.database_path))
            setattr(self, _SERVICE_ATTR, service)
        payload["worker_verification"] = service.status(limit=max(100, self.history_limit))
        return payload

    command_center.CommandCenterService.status = status
    setattr(command_center.CommandCenterService, _INSTALL_FLAG, True)
    return True


install_worker_verification_status()
