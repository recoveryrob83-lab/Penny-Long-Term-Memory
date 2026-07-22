"""Install Package E Slice 5 HQ review and Slice 6 Rob-validation services."""
from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path

from . import worker_operations
from .worker_hq_review import (
    WorkerHqReviewIngestionReceipt,
    WorkerHqReviewService,
)
from .worker_result_contract import artifact_path, validate_artifact
from .worker_rob_validation import WorkerRobValidationService
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_hq_review_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_hq_review_service_installed"
_DUPLICATE_FLAG = "_lifeos_worker_hq_review_duplicate_patch_installed"
_SEMANTICS_FLAG = "_lifeos_worker_hq_review_semantics_patch_installed"
_WAKE_FLAG = "_lifeos_worker_hq_review_wake_procedure_patch_installed"
_REVIEW_PROCEDURE_PATH = (
    "projects/engineering/procedures/engineering_hq_worker_review_receipt.md"
)
_AUTOMATION_HQ_CHAT_TITLES = {
    "engineering": "Engineering_HQ",
}


def _automation_hq_chat_title(owning_department: str) -> str:
    department = str(owning_department or "").strip().casefold()
    environment_name = f"LIFEOS_{department.upper()}_HQ_AUTOMATION_TITLE"
    configured = str(os.getenv(environment_name) or "").strip()
    if configured:
        if " " in configured:
            raise WorkerRuntimeError(
                f"{environment_name} must use the automation chat-title convention without spaces."
            )
        return configured
    title = _AUTOMATION_HQ_CHAT_TITLES.get(department)
    if title is None:
        raise WorkerRuntimeError(
            "Cross-department HQ routing is not authorized by the Engineering-only Slice 5 pilot."
        )
    return title


def _install_wake_procedure_pointer() -> None:
    service_class = WorkerHqReviewService
    if getattr(service_class, _WAKE_FLAG, False):
        return
    original_build = service_class.build_wake

    def build_wake(self: WorkerHqReviewService, run_id: str):
        wake = original_build(self, run_id)
        return replace(
            wake,
            hq_chat_title=_automation_hq_chat_title(wake.owning_department),
            instruction=(
                wake.instruction
                + f" Follow the canonical Engineering HQ review procedure at "
                f"`{_REVIEW_PROCEDURE_PATH}`."
            ),
        )

    service_class.build_wake = build_wake
    setattr(service_class, _WAKE_FLAG, True)


def _install_review_semantics() -> None:
    service_class = WorkerHqReviewService
    if getattr(service_class, _SEMANTICS_FLAG, False):
        return
    original_validate = service_class._validate_review_semantics

    def validate(payload: dict[str, object]) -> None:
        original_validate(payload)
        state = str(payload.get("review_state") or "")
        integrity = str(payload.get("report_integrity_state") or "")
        authority = str(payload.get("authority_compliance_state") or "")
        work = str(payload.get("work_verification_state") or "")
        if state == "REJECTED" and not (
            integrity == "invalid" or authority == "noncompliant" or work == "rejected"
        ):
            raise WorkerRuntimeError(
                "REJECTED HQ receipt must identify an invalid, noncompliant, or rejected dimension."
            )
        if state == "REPAIR_REQUIRED" and (
            integrity == "valid" and authority == "compliant" and work == "verified"
        ):
            raise WorkerRuntimeError(
                "REPAIR_REQUIRED HQ receipt cannot claim every review dimension is verified."
            )

    service_class._validate_review_semantics = staticmethod(validate)
    setattr(service_class, _SEMANTICS_FLAG, True)


def _install_duplicate_receipt_suppression() -> None:
    service_class = WorkerHqReviewService
    if getattr(service_class, _DUPLICATE_FLAG, False):
        return
    original_ingest = service_class.ingest_review

    def ingest_review(self: WorkerHqReviewService, run_id: str):
        row = self._row(run_id)  # noqa: SLF001 - same-row compatibility wrapper
        existing_state = str(row["hq_review_state"] or "").strip()
        if not existing_state:
            return original_ingest(self, run_id)
        review_path = artifact_path(
            str(row["owning_department"]),
            str(row["worker_id"]),
            str(row["run_id"]),
            "hq_review",
            1,
        )
        review_file = self._safe_path(review_path)  # noqa: SLF001
        if not review_file.is_file():
            raise WorkerRuntimeError("Previously ingested HQ review receipt is missing from Git.")
        try:
            payload = json.loads(review_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkerRuntimeError("Previously ingested HQ review receipt is unreadable.") from exc
        if not isinstance(payload, dict):
            raise WorkerRuntimeError("Previously ingested HQ review receipt has the wrong shape.")
        validate_artifact("hq_review", payload)
        self._validate_review_semantics(payload)  # noqa: SLF001
        commit_sha, blob_sha, checksum = self._git_review_evidence(  # noqa: SLF001
            review_path, payload
        )
        if (
            str(row["hq_review_path"] or "") != review_path
            or str(row["hq_review_checksum"] or "") != checksum
            or str(row["hq_review_commit_sha"] or "") != commit_sha
            or str(row["hq_review_blob_sha"] or "") != blob_sha
            or existing_state != str(payload.get("review_state") or "")
        ):
            raise WorkerRuntimeError("A conflicting immutable HQ review is already ingested.")
        return WorkerHqReviewIngestionReceipt(
            status="succeeded",
            run_id=str(row["run_id"]),
            worker_id=str(row["worker_id"]),
            review_state=existing_state,
            review_path=review_path,
            review_checksum=checksum,
            review_commit_sha=commit_sha,
            review_blob_sha=blob_sha,
            result_state=str(row["result_state"]),
            ready_for_consumption=bool(row["ready_for_consumption"]),
            requires_rob_validation=bool(row["requires_rob_validation"]),
            duplicate_suppressed=True,
        )

    service_class.ingest_review = ingest_review
    setattr(service_class, _DUPLICATE_FLAG, True)


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
        self.hq_review = WorkerHqReviewService(repository_root, database_path)
        self.rob_validation = WorkerRobValidationService(repository_root, database_path)

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["hq_review"] = self.hq_review.status(limit=100)
        payload["rob_validation"] = self.rob_validation.status(limit=100)
        return payload

    def build_hq_review_wake(self, run_id: str) -> dict[str, object]:
        return self.hq_review.build_wake(run_id).to_dict()

    def record_hq_review_wake(
        self, run_id: str, browser_receipt: dict[str, object]
    ) -> dict[str, object]:
        wake = self.hq_review.record_wake(run_id, browser_receipt)
        return {
            "status": "succeeded",
            "wake": wake.to_dict(),
            "hq_review": self.hq_review.status(limit=100),
        }

    def ingest_hq_review(self, run_id: str) -> dict[str, object]:
        receipt = self.hq_review.ingest_review(run_id)
        return {
            "status": "succeeded",
            "receipt": receipt.to_dict(),
            "hq_review": self.hq_review.status(limit=100),
            "verification": self.verification.status(limit=100),
        }

    def ingest_rob_validation(self, run_id: str) -> dict[str, object]:
        receipt = self.rob_validation.ingest_validation(run_id)
        return {
            "status": "succeeded",
            "receipt": receipt.to_dict(),
            "rob_validation": self.rob_validation.status(limit=100),
            "verification": self.rob_validation.verification.status(limit=100),
        }

    service_class.__init__ = __init__
    service_class.status = status
    service_class.build_hq_review_wake = build_hq_review_wake
    service_class.record_hq_review_wake = record_hq_review_wake
    service_class.ingest_hq_review = ingest_hq_review
    service_class.ingest_rob_validation = ingest_rob_validation
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_hq_review_runtime() -> bool:
    """Install Slice 5 and Slice 6 review-state extensions once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    _install_wake_procedure_pointer()
    _install_review_semantics()
    _install_duplicate_receipt_suppression()
    _install_service()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_hq_review_runtime()


__all__ = ["install_worker_hq_review_runtime"]
