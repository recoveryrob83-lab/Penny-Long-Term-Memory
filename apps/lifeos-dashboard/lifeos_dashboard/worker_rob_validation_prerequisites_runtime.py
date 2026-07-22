"""Ensure Slice 6 can initialize on a fresh execution-history database."""
from __future__ import annotations

from .worker_rob_validation import WorkerRobValidationService

_PREREQUISITE_COLUMNS = {
    "result_state": "TEXT",
    "report_path": "TEXT",
    "report_checksum": "TEXT",
    "hq_review_path": "TEXT",
    "hq_review_checksum": "TEXT",
    "hq_review_commit_sha": "TEXT",
    "hq_review_blob_sha": "TEXT",
    "hq_review_state": "TEXT",
    "hq_review_reason": "TEXT",
    "ready_for_consumption": "INTEGER",
    "requires_rob_validation": "INTEGER",
}

WorkerRobValidationService._COLUMNS = {
    **_PREREQUISITE_COLUMNS,
    **WorkerRobValidationService._COLUMNS,
}
