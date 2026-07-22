from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

from lifeos_dashboard.worker_runtime import WorkerRuntimeError


SUPPORT_PATH = Path(__file__).with_name("test_worker_result_ingester.py")
SUPPORT_SPEC = importlib.util.spec_from_file_location(
    "worker_result_ingester_history_test_support", SUPPORT_PATH
)
assert SUPPORT_SPEC is not None and SUPPORT_SPEC.loader is not None
support = importlib.util.module_from_spec(SUPPORT_SPEC)
sys.modules[SUPPORT_SPEC.name] = support
SUPPORT_SPEC.loader.exec_module(support)


def _mark_legacy_return_failure(database: Path, *, reason: str) -> None:
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            UPDATE execution_history SET
                status = 'failed', exit_code = 2, reason = ?,
                dispatch_state = NULL, user_turn_id = NULL,
                dispatch_receipt_json = NULL, returned_to_source = 0
            WHERE run_id = ?
            """,
            (reason, support.RUN_ID),
        )


def test_valid_report_reconciles_unique_historical_return_failure(tmp_path: Path) -> None:
    ingester, active, database, report = support._setup(tmp_path)
    _mark_legacy_return_failure(
        database,
        reason="Browser courier did not verify return to the source chat.",
    )

    receipt = ingester.ingest(active)
    row = support._row(database)

    assert receipt.report_state == "REPORT_VALIDATED"
    assert receipt.report_checksum == support.artifact_checksum(report)
    assert receipt.hq_review_required is True
    assert row["status"] == "failed"
    assert row["dispatch_state"] is None
    assert row["user_turn_id"] is None
    assert row["controlled_outcome"] == "IMPLEMENT"
    assert row["receiver_verification_state"] == "pending"
    assert "Historical failed-after-send transport evidence" in row["receiver_reason"]
    assert "original transport status remains preserved" in row["receiver_reason"]


def test_unrelated_failed_send_is_not_reconciled(tmp_path: Path) -> None:
    ingester, active, database, _ = support._setup(tmp_path)
    _mark_legacy_return_failure(
        database,
        reason="Browser courier stopped safely before anything was submitted.",
    )

    with pytest.raises(WorkerRuntimeError, match="could not select one authoritative"):
        ingester.ingest(active)

    row = support._row(database)
    assert row["status"] == "failed"
    assert row["result_state"] is None
    assert row["controlled_outcome"] is None


def test_ingestion_cli_loads_dashboard_environment_and_reports_selected_paths() -> None:
    script = (
        Path(__file__).parents[1] / "automation" / "ingest_worker_result.py"
    ).read_text(encoding="utf-8")

    assert 'load_dotenv(app_root / ".env", override=False)' in script
    assert '"COMMAND_CENTER_DATABASE_PATH"' in script
    assert 'print(f"Database: {database_path}"' in script
    assert 'print(f"Repository: {repository_root}"' in script
