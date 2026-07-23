"""Package E Slice 7 Chief of Staff consumption over the existing execution ledger.

The service reads only signed consumption-ready Worker runs and stores delivery
deduplication on the same ``execution_history`` row. It does not change source
advisories, create a second queue, wake Chief of Staff, or treat raw reports as truth.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .worker_hq_review import WorkerHqReviewService
from .worker_result_ingester import WorkerResultIngester
from .worker_rob_validation import WorkerRobValidationService
from .worker_runtime import WorkerRuntimeError

_ELIGIBLE_RESULT_STATES = {"HQ_VERIFIED", "READY_FOR_COS"}
_CONSUMED = "CONSUMED"
_HEADING_PATTERN = re.compile(
    r"^### (?P<task_id>ADV-[A-Z0-9-]+)(?:\s+—\s+.*)?$", re.MULTILINE
)
_LIFECYCLE_PATTERN = re.compile(
    r"^- Lifecycle State:\s*(?P<state>[A-Z_]+)\s*$", re.MULTILINE
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256(value: object) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SourceAdvisoryPointer:
    task_id: str
    board_path: str
    lifecycle_state: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class WorkerCosConsumptionItem:
    history_id: int
    run_id: str
    worker_id: str
    task_id: str
    task_revision: int
    owning_department: str
    controlled_outcome: str
    result_state: str
    verification_actor: str
    verification_reason: str
    report_path: str
    report_checksum: str
    hq_review_path: str | None
    hq_review_state: str | None
    rob_validation_path: str | None
    rob_validation_state: str | None
    source_advisory: SourceAdvisoryPointer
    fingerprint: str

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["source_advisory"] = self.source_advisory.to_dict()
        return values


@dataclass(frozen=True)
class WorkerCosConsumptionPreview:
    status: str
    batch_id: str | None
    consumer: str
    items: tuple[WorkerCosConsumptionItem, ...]
    meaningful_change: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "batch_id": self.batch_id,
            "consumer": self.consumer,
            "items": [item.to_dict() for item in self.items],
            "meaningful_change": self.meaningful_change,
        }


@dataclass(frozen=True)
class WorkerCosConsumptionAcknowledgement:
    status: str
    batch_id: str
    consumer: str
    run_ids: tuple[str, ...]
    consumed_count: int
    duplicate_suppressed: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerCosConsumptionService:
    """Preview and acknowledge signed results without creating another ledger."""

    _COLUMNS = {
        "cos_consumption_state": "TEXT",
        "cos_consumption_fingerprint": "TEXT",
        "cos_consumption_batch_id": "TEXT",
        "cos_consumed_at": "REAL",
        "cos_consumed_by": "TEXT",
    }

    def __init__(self, repository_root: Path, database_path: Path) -> None:
        self.repository_root = repository_root.resolve()
        self.database_path = database_path
        if not (self.repository_root / ".git").exists():
            raise WorkerRuntimeError("Chief of Staff consumption requires a local Git repository.")
        WorkerResultIngester(self.repository_root, self.database_path)
        WorkerHqReviewService(self.repository_root, self.database_path)
        WorkerRobValidationService(self.repository_root, self.database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            existing = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(execution_history)").fetchall()
            }
            for column_name, column_type in self._COLUMNS.items():
                if column_name not in existing:
                    connection.execute(
                        f"ALTER TABLE execution_history ADD COLUMN {column_name} {column_type}"
                    )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_execution_history_cos_consumption
                ON execution_history(cos_consumption_state, ready_for_consumption, run_id)
                """
            )

    def _source_advisory(self, task_id: str) -> SourceAdvisoryPointer:
        matches: list[SourceAdvisoryPointer] = []
        boards_root = self.repository_root / "coordination" / "boards"
        for board_file in sorted(boards_root.glob("*.md")):
            text = board_file.read_text(encoding="utf-8")
            headings = list(_HEADING_PATTERN.finditer(text))
            for index, heading in enumerate(headings):
                if heading.group("task_id") != task_id:
                    continue
                start = heading.end()
                end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
                lifecycle = _LIFECYCLE_PATTERN.search(text[start:end])
                if lifecycle is None:
                    raise WorkerRuntimeError(
                        f"Source advisory {task_id} has no canonical lifecycle state."
                    )
                matches.append(
                    SourceAdvisoryPointer(
                        task_id=task_id,
                        board_path=board_file.relative_to(self.repository_root).as_posix(),
                        lifecycle_state=lifecycle.group("state"),
                    )
                )
        if not matches:
            raise WorkerRuntimeError(f"Source advisory {task_id} was not found on a source board.")
        if len(matches) > 1:
            raise WorkerRuntimeError(f"Source advisory {task_id} is duplicated across source boards.")
        return matches[0]

    @staticmethod
    def _fingerprint_payload(row: sqlite3.Row, source: SourceAdvisoryPointer) -> dict[str, object]:
        return {
            "run_id": str(row["run_id"]),
            "worker_id": str(row["worker_id"]),
            "task_id": str(row["task_id"]),
            "task_revision": int(row["task_revision"]),
            "result_state": str(row["result_state"]),
            "controlled_outcome": str(row["controlled_outcome"]),
            "report_checksum": str(row["report_checksum"] or ""),
            "hq_review_checksum": str(row["hq_review_checksum"] or ""),
            "rob_validation_checksum": str(row["rob_validation_checksum"] or ""),
            "verification_actor": str(row["worker_verification_actor"] or ""),
            "source_board_path": source.board_path,
            "source_lifecycle_state": source.lifecycle_state,
        }

    def _item_from_row(self, row: sqlite3.Row) -> WorkerCosConsumptionItem:
        if not bool(row["ready_for_consumption"]):
            raise WorkerRuntimeError("Chief of Staff consumption requires a consumption-ready row.")
        if str(row["result_state"] or "") not in _ELIGIBLE_RESULT_STATES:
            raise WorkerRuntimeError("Chief of Staff consumption found an ineligible result state.")
        if str(row["controlled_outcome"] or "") != "IMPLEMENT":
            raise WorkerRuntimeError("The initial Slice 7 consumer accepts verified IMPLEMENT only.")
        actor = str(row["worker_verification_actor"] or "").strip()
        reason = str(row["worker_verification_reason"] or "").strip()
        if not actor or not reason:
            raise WorkerRuntimeError("Consumption-ready result lacks final verification evidence.")
        source = self._source_advisory(str(row["task_id"]))
        fingerprint = _sha256(self._fingerprint_payload(row, source))
        return WorkerCosConsumptionItem(
            history_id=int(row["id"]),
            run_id=str(row["run_id"]),
            worker_id=str(row["worker_id"]),
            task_id=str(row["task_id"]),
            task_revision=int(row["task_revision"]),
            owning_department=str(row["owning_department"]),
            controlled_outcome=str(row["controlled_outcome"]),
            result_state=str(row["result_state"]),
            verification_actor=actor,
            verification_reason=reason,
            report_path=str(row["report_path"]),
            report_checksum=str(row["report_checksum"]),
            hq_review_path=str(row["hq_review_path"]) if row["hq_review_path"] else None,
            hq_review_state=str(row["hq_review_state"]) if row["hq_review_state"] else None,
            rob_validation_path=(
                str(row["rob_validation_path"]) if row["rob_validation_path"] else None
            ),
            rob_validation_state=(
                str(row["rob_validation_state"]) if row["rob_validation_state"] else None
            ),
            source_advisory=source,
            fingerprint=fingerprint,
        )

    @staticmethod
    def _clean_run_ids(run_ids: Iterable[str] | None) -> tuple[str, ...]:
        if run_ids is None:
            return ()
        cleaned = tuple(dict.fromkeys(str(value or "").strip() for value in run_ids))
        if any(not value for value in cleaned):
            raise WorkerRuntimeError("run_id cannot be empty.")
        return cleaned

    def _rows(self, run_ids: tuple[str, ...] = (), *, include_consumed: bool = False) -> list[sqlite3.Row]:
        clauses = [
            "mode = 'send'",
            "prompt_type = 'worker'",
            "ready_for_consumption = 1",
            "result_state IN ('HQ_VERIFIED', 'READY_FOR_COS')",
            "controlled_outcome = 'IMPLEMENT'",
        ]
        parameters: list[object] = []
        if not include_consumed:
            clauses.append("(cos_consumption_state IS NULL OR cos_consumption_state = '')")
        if run_ids:
            placeholders = ",".join("?" for _ in run_ids)
            clauses.append(f"run_id IN ({placeholders})")
            parameters.extend(run_ids)
        query = "SELECT * FROM execution_history WHERE " + " AND ".join(clauses)
        query += " ORDER BY id"
        with self._connect() as connection:
            return connection.execute(query, parameters).fetchall()

    @staticmethod
    def _batch_id(items: Iterable[WorkerCosConsumptionItem]) -> str:
        fingerprints = [item.fingerprint for item in sorted(items, key=lambda item: item.run_id)]
        if not fingerprints:
            raise WorkerRuntimeError("Cannot create a consumption batch without items.")
        digest = hashlib.sha256(_canonical_json(fingerprints).encode("utf-8")).hexdigest()
        return "COS-BATCH-" + digest[:16].upper()

    def preview(
        self,
        run_ids: Iterable[str] | None = None,
        *,
        consumer: str = "Chief of Staff HQ",
    ) -> WorkerCosConsumptionPreview:
        clean_run_ids = self._clean_run_ids(run_ids)
        items = tuple(self._item_from_row(row) for row in self._rows(clean_run_ids))
        batch_id = self._batch_id(items) if items else None
        return WorkerCosConsumptionPreview(
            status="succeeded",
            batch_id=batch_id,
            consumer=consumer,
            items=items,
            meaningful_change=bool(items),
        )

    def acknowledge(
        self,
        batch_id: str,
        run_ids: Iterable[str],
        *,
        consumer: str = "Chief of Staff HQ",
    ) -> WorkerCosConsumptionAcknowledgement:
        clean_batch_id = str(batch_id or "").strip()
        if not clean_batch_id:
            raise WorkerRuntimeError("batch_id cannot be empty.")
        clean_run_ids = self._clean_run_ids(run_ids)
        if not clean_run_ids:
            raise WorkerRuntimeError("At least one run_id is required.")
        rows = self._rows(clean_run_ids, include_consumed=True)
        if len(rows) != len(clean_run_ids):
            raise WorkerRuntimeError("Consumption acknowledgement could not resolve every run.")
        items = tuple(self._item_from_row(row) for row in rows)
        expected_batch_id = self._batch_id(items)
        if clean_batch_id != expected_batch_id:
            raise WorkerRuntimeError("Consumption batch ID does not match current signed evidence.")

        consumed = [str(row["cos_consumption_state"] or "") == _CONSUMED for row in rows]
        if any(consumed):
            if not all(consumed):
                raise WorkerRuntimeError("Consumption batch is partially acknowledged.")
            if all(
                str(row["cos_consumption_batch_id"] or "") == clean_batch_id
                and str(row["cos_consumed_by"] or "") == consumer
                for row in rows
            ):
                return WorkerCosConsumptionAcknowledgement(
                    status="succeeded",
                    batch_id=clean_batch_id,
                    consumer=consumer,
                    run_ids=clean_run_ids,
                    consumed_count=len(rows),
                    duplicate_suppressed=True,
                )
            raise WorkerRuntimeError("A conflicting consumption acknowledgement already exists.")

        now = time.time()
        with self._connect() as connection:
            for row, item in zip(rows, items, strict=True):
                updated = connection.execute(
                    """
                    UPDATE execution_history SET
                        cos_consumption_state = ?,
                        cos_consumption_fingerprint = ?,
                        cos_consumption_batch_id = ?,
                        cos_consumed_at = ?,
                        cos_consumed_by = ?
                    WHERE id = ?
                      AND (cos_consumption_state IS NULL OR cos_consumption_state = '')
                    """,
                    (
                        _CONSUMED,
                        item.fingerprint,
                        clean_batch_id,
                        now,
                        consumer,
                        int(row["id"]),
                    ),
                )
                if updated.rowcount != 1:
                    raise WorkerRuntimeError(
                        "Consumption state changed before acknowledgement completed."
                    )
        return WorkerCosConsumptionAcknowledgement(
            status="succeeded",
            batch_id=clean_batch_id,
            consumer=consumer,
            run_ids=clean_run_ids,
            consumed_count=len(rows),
        )

    def records(self, limit: int = 100) -> list[dict[str, object]]:
        if limit < 1:
            raise WorkerRuntimeError("Consumption record limit must be positive.")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, run_id, worker_id, task_id, task_revision, owning_department,
                       controlled_outcome, result_state, ready_for_consumption,
                       worker_verification_actor, cos_consumption_state,
                       cos_consumption_fingerprint, cos_consumption_batch_id,
                       cos_consumed_at, cos_consumed_by
                FROM execution_history
                WHERE ready_for_consumption = 1
                  AND result_state IN ('HQ_VERIFIED', 'READY_FOR_COS')
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def status(self, limit: int = 100) -> dict[str, object]:
        records = self.records(limit)
        return {
            "summary": {
                "total": len(records),
                "pending": sum(
                    not str(item.get("cos_consumption_state") or "") for item in records
                ),
                "consumed": sum(
                    item.get("cos_consumption_state") == _CONSUMED for item in records
                ),
            },
            "records": records,
        }


__all__ = [
    "SourceAdvisoryPointer",
    "WorkerCosConsumptionAcknowledgement",
    "WorkerCosConsumptionItem",
    "WorkerCosConsumptionPreview",
    "WorkerCosConsumptionService",
]
