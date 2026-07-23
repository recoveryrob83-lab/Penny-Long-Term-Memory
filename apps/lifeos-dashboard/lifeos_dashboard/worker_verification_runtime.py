"""Attach Worker verification views and canonical reviewer-title handling."""
from __future__ import annotations

from pathlib import Path

from . import command_center
from .room_titles import canonical_room_title
from .worker_verification import WorkerVerificationService, WorkerVerificationStore

_STATUS_INSTALL_FLAG = "_lifeos_worker_verification_status_installed"
_REVIEW_INSTALL_FLAG = "_lifeos_worker_verification_title_installed"
_SERVICE_ATTR = "_lifeos_worker_verification_service"


def install_worker_verification_status() -> bool:
    """Extend status once without creating another API or durable queue."""
    if getattr(command_center.CommandCenterService, _STATUS_INSTALL_FLAG, False):
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
    setattr(command_center.CommandCenterService, _STATUS_INSTALL_FLAG, True)
    return True


def install_reviewer_title_rollover() -> bool:
    """Translate an exact legacy reviewer title before any new verification row is written."""
    if getattr(WorkerVerificationStore, _REVIEW_INSTALL_FLAG, False):
        return False
    original_review = WorkerVerificationStore.review

    def review(
        self: WorkerVerificationStore,
        run_id: str,
        state,
        *,
        actor: str,
        reason: str,
    ):
        return original_review(
            self,
            run_id,
            state,
            actor=canonical_room_title(actor),
            reason=reason,
        )

    WorkerVerificationStore.review = review
    setattr(WorkerVerificationStore, _REVIEW_INSTALL_FLAG, True)
    return True


install_worker_verification_status()
install_reviewer_title_rollover()
