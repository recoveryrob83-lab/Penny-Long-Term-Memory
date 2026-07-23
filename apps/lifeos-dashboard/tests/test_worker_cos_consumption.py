import sqlite3
import subprocess
import time
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import (
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_cos_consumption import WorkerCosConsumptionService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RUN_ID = "RUN-ADV-20260722-049-R1"
TASK_ID = "ADV-20260722-049"
WORKER_ID = "engineering_worker"


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )


def _transport_result() -> WorkerExecutionResult:
    return WorkerExecutionResult(
        status="succeeded",
        destination="Engineering_Worker",
        mode="send",
        exit_code=0,
        started_at=time.time() - 1,
        finished_at=time.time(),
        stdout="",
        stderr="",
        reason="Synthetic dispatch succeeded.",
        trigger="manual",
        wrapper_id="WAKE-ADV-20260722-049-R1",
        run_id=RUN_ID,
        worker_id=WORKER_ID,
        task_id=TASK_ID,
        task_revision=1,
        procedure_id="engineering_worker_rob_validation_pilot",
        procedure_version=1,
        authorization_source="ENGINEERING_HQ_SLICE7_TEST",
        idempotency_key=f"{WORKER_ID}:{TASK_ID}:1",
        verification_mode="IMMEDIATE_HQ",
        controlled_outcome="IMPLEMENT",
    )


def _setup(tmp_path: Path) -> tuple[WorkerCosConsumptionService, Path, Path]:
    _git(tmp_path, "init")
    board = tmp_path / "coordination" / "boards" / "engineering.md"
    board.parent.mkdir(parents=True, exist_ok=True)
    board.write_text(
        "\n".join(
            (
                "# Engineering Advisory Board",
                "",
                f"### {TASK_ID} — Synthetic Slice 7 source",
                "",
                "- Lifecycle State: OPEN",
                "- Priority: NORMAL",
                "",
            )
        ),
        encoding="utf-8",
    )
    database = tmp_path / "command-center.sqlite3"
    service = WorkerCosConsumptionService(tmp_path, database)
    WorkerExecutionHistoryStore(database).record(_transport_result())
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            UPDATE execution_history SET
                owning_department = 'engineering',
                result_state = 'READY_FOR_COS',
                report_path = ?, report_checksum = ?,
                hq_review_path = ?, hq_review_checksum = ?,
                hq_review_state = 'ROB_VALIDATION_REQUIRED',
                rob_validation_path = ?, rob_validation_checksum = ?,
                rob_validation_state = 'VERIFIED',
                ready_for_consumption = 1, requires_rob_validation = 0,
                worker_verification_state = 'verified',
                worker_verification_actor = 'Rob',
                worker_verification_reason = ?
            WHERE run_id = ?
            """,
            (
                f"projects/engineering/worker-results/{WORKER_ID}/{RUN_ID}/report-001.json",
                "sha256:" + "1" * 64,
                f"projects/engineering/worker-results/{WORKER_ID}/{RUN_ID}/hq-review-001.json",
                "sha256:" + "2" * 64,
                f"projects/engineering/worker-results/{WORKER_ID}/{RUN_ID}/rob-validation-001.json",
                "sha256:" + "3" * 64,
                "Rob observed the exact synthetic marker.",
                RUN_ID,
            ),
        )
    return service, database, board


def _row(database: Path) -> sqlite3.Row:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()
    assert row is not None
    return row


def test_preview_is_read_only_and_reports_source_state(tmp_path: Path) -> None:
    service, database, _ = _setup(tmp_path)

    preview = service.preview([RUN_ID])
    row = _row(database)

    assert preview.meaningful_change is True
    assert preview.batch_id is not None
    assert len(preview.items) == 1
    assert preview.items[0].source_advisory.lifecycle_state == "OPEN"
    assert preview.items[0].verification_actor == "Rob"
    assert row["cos_consumption_state"] is None
    assert row["cos_consumption_batch_id"] is None


def test_acknowledgement_uses_same_row_and_suppresses_duplicate(tmp_path: Path) -> None:
    service, database, _ = _setup(tmp_path)
    preview = service.preview([RUN_ID])
    assert preview.batch_id is not None

    first = service.acknowledge(preview.batch_id, [RUN_ID])
    second = service.acknowledge(preview.batch_id, [RUN_ID])
    row = _row(database)

    assert first.consumed_count == 1
    assert first.duplicate_suppressed is False
    assert second.duplicate_suppressed is True
    assert row["cos_consumption_state"] == "CONSUMED"
    assert row["cos_consumption_batch_id"] == preview.batch_id
    assert row["cos_consumed_by"] == "Chief of Staff HQ"
    assert service.preview([RUN_ID]).meaningful_change is False
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM execution_history WHERE run_id = ?", (RUN_ID,)
        ).fetchone()[0] == 1


def test_acknowledgement_rejects_source_state_drift(tmp_path: Path) -> None:
    service, _, board = _setup(tmp_path)
    preview = service.preview([RUN_ID])
    assert preview.batch_id is not None
    board.write_text(
        board.read_text(encoding="utf-8").replace(
            "- Lifecycle State: OPEN", "- Lifecycle State: IMPLEMENTED"
        ),
        encoding="utf-8",
    )

    with pytest.raises(WorkerRuntimeError, match="batch ID"):
        service.acknowledge(preview.batch_id, [RUN_ID])


def test_unverified_result_is_not_previewed(tmp_path: Path) -> None:
    service, database, _ = _setup(tmp_path)
    with sqlite3.connect(database) as connection:
        connection.execute(
            "UPDATE execution_history SET ready_for_consumption = 0 WHERE run_id = ?",
            (RUN_ID,),
        )

    preview = service.preview([RUN_ID])

    assert preview.meaningful_change is False
    assert preview.batch_id is None
    assert preview.items == ()
