"""Public Package E report-repair surface.

The implementation lives in ``worker_result_repair_core`` so callers retain one stable import path
while the correction-only contract remains isolated from runtime installation glue.
"""
from .worker_result_repair_core import (
    REPAIR_ACCEPTED,
    REPAIR_EXHAUSTED,
    REPAIR_PENDING,
    WorkerReportRejectionReceipt,
    WorkerReportRepairWake,
    WorkerResultRepairCoordinator,
    render_repair_instruction,
    structured_validation_errors,
)

__all__ = [
    "REPAIR_ACCEPTED",
    "REPAIR_EXHAUSTED",
    "REPAIR_PENDING",
    "WorkerReportRejectionReceipt",
    "WorkerReportRepairWake",
    "WorkerResultRepairCoordinator",
    "render_repair_instruction",
    "structured_validation_errors",
]
