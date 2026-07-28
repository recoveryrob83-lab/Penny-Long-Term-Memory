"""Repair drift between immutable HQ review evidence and local runtime state.

A validated HQ ``REPAIR_REQUIRED`` receipt maps to ``REPORT_REPAIR_PENDING``. The
Maintenance relay previously allowed the next orchestrator cycle to re-ingest the
original rejected Worker report, which moved the same execution row backward to
``REPORT_REJECTED`` while retaining the immutable HQ review evidence.

This compatibility layer is intentionally narrow. It blocks Worker-result ingestion
while an HQ repair is pending and reconciles only the proven drift pair
``REPAIR_REQUIRED`` + ``REPORT_REJECTED`` back to its canonical runtime state.
"""
from __future__ import annotations

from dataclasses import replace

from .worker_github_orchestrator import WorkerGitHubOrchestrator
from .worker_hq_review import (
    WorkerHqReviewIngestionReceipt,
    WorkerHqReviewService,
)
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_hq_review_state_repair_runtime_installed"
_SERVICE_FLAG = "_lifeos_hq_review_duplicate_reconciliation_installed"
_ORCHESTRATOR_FLAG = "_lifeos_hq_review_orchestrator_reconciliation_installed"
_REPAIR_REQUIRED = "REPAIR_REQUIRED"
_REPORT_REJECTED = "REPORT_REJECTED"
_REPORT_REPAIR_PENDING = "REPORT_REPAIR_PENDING"


def _reconcile_duplicate_repair_required(
    service: WorkerHqReviewService,
    receipt: WorkerHqReviewIngestionReceipt,
) -> WorkerHqReviewIngestionReceipt:
    """Restore the canonical runtime state for one already-ingested immutable review."""

    if not (
        receipt.duplicate_suppressed
        and receipt.review_state == _REPAIR_REQUIRED
        and receipt.result_state == _REPORT_REJECTED
    ):
        return receipt

    with service._connect() as connection:  # noqa: SLF001 - same-row compatibility repair
        updated = connection.execute(
            """
            UPDATE execution_history
            SET result_state = ?
            WHERE run_id = ?
              AND worker_id = ?
              AND mode = 'send'
              AND prompt_type = 'worker'
              AND result_state = ?
              AND hq_review_state = ?
              AND hq_review_path = ?
              AND hq_review_checksum = ?
              AND hq_review_commit_sha = ?
              AND hq_review_blob_sha = ?
            """,
            (
                _REPORT_REPAIR_PENDING,
                receipt.run_id,
                receipt.worker_id,
                _REPORT_REJECTED,
                _REPAIR_REQUIRED,
                receipt.review_path,
                receipt.review_checksum,
                receipt.review_commit_sha,
                receipt.review_blob_sha,
            ),
        )
        if updated.rowcount != 1:
            raise WorkerRuntimeError(
                "HQ review runtime reconciliation found changed or conflicting state. "
                "Nothing was overwritten."
            )

    return replace(receipt, result_state=_REPORT_REPAIR_PENDING)


def _install_service_reconciliation() -> None:
    service_class = WorkerHqReviewService
    if getattr(service_class, _SERVICE_FLAG, False):
        return

    original_ingest_review = service_class.ingest_review

    def ingest_review(
        self: WorkerHqReviewService,
        run_id: str,
    ) -> WorkerHqReviewIngestionReceipt:
        receipt = original_ingest_review(self, run_id)
        return _reconcile_duplicate_repair_required(self, receipt)

    service_class.ingest_review = ingest_review
    setattr(service_class, _SERVICE_FLAG, True)


def _install_orchestrator_reconciliation() -> None:
    orchestrator_class = WorkerGitHubOrchestrator
    if getattr(orchestrator_class, _ORCHESTRATOR_FLAG, False):
        return

    original_ingest_result = orchestrator_class._ingest_result_if_present
    original_ingest_hq_review = orchestrator_class._ingest_hq_review_if_present

    def ingest_result_if_present(
        self: WorkerGitHubOrchestrator,
        advisory,
    ) -> None:
        row = self._row(advisory.run_id)
        if (
            row is not None
            and str(row["result_state"] or "") == _REPORT_REPAIR_PENDING
        ):
            return
        original_ingest_result(self, advisory)

    def ingest_hq_review_if_present(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if (
            row is not None
            and str(row["result_state"] or "") == _REPORT_REJECTED
            and str(row["hq_review_state"] or "") == _REPAIR_REQUIRED
        ):
            payload = self.operations.ingest_hq_review(run_id)
            receipt = payload.get("receipt") or {}
            self._event(
                "hq_review_reconciliation",
                "succeeded",
                "Immutable HQ review restored runtime state to "
                f"{receipt.get('result_state') or _REPORT_REPAIR_PENDING}.",
                run_id=run_id,
                advisory_id=advisory_id,
            )
            return
        original_ingest_hq_review(self, run_id, advisory_id)

    orchestrator_class._ingest_result_if_present = ingest_result_if_present
    orchestrator_class._ingest_hq_review_if_present = ingest_hq_review_if_present
    setattr(orchestrator_class, _ORCHESTRATOR_FLAG, True)


def install_worker_hq_review_state_repair_runtime() -> bool:
    """Install the bounded HQ-review state reconciliation once."""

    if getattr(WorkerHqReviewService, _INSTALL_FLAG, False):
        return False
    _install_service_reconciliation()
    _install_orchestrator_reconciliation()
    setattr(WorkerHqReviewService, _INSTALL_FLAG, True)
    return True


install_worker_hq_review_state_repair_runtime()


__all__ = [
    "_reconcile_duplicate_repair_required",
    "install_worker_hq_review_state_repair_runtime",
]
