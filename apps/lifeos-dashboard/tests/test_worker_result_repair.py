from pathlib import Path
import subprocess
import sys

from lifeos_dashboard.worker_result_repair import structured_validation_errors
from lifeos_dashboard.worker_result_repair_pilot import (
    REPORT_2,
    RUN_ID,
    run_synthetic_repair_pilot,
)


def test_structured_errors_preserve_type_without_copying_string_value() -> None:
    errors = structured_validation_errors(
        ["$.profile_version: expected integer, observed string"],
        {"profile_version": "sensitive-looking-value"},
    )

    assert errors == [
        {
            "code": "WRONG_TYPE",
            "field": "profile_version",
            "message": "expected integer, observed string",
            "expected": "integer",
            "observed_type": "string",
            "observed_summary": "<string length 23>",
        }
    ]


def test_synthetic_report_repair_rejects_repairs_and_deduplicates(tmp_path: Path) -> None:
    receipt = run_synthetic_repair_pilot(tmp_path)

    assert receipt["status"] == "succeeded"
    assert receipt["run_id"] == RUN_ID
    assert receipt["malformed_attempt"] == 1
    assert str(receipt["rejection_path"]).endswith("/rejection-001.json")
    assert receipt["repair_wake"]["worker_id"] == "engineering_worker"
    assert receipt["repair_wake"]["run_id"] == receipt["run_id"]
    assert receipt["repair_wake"]["corrected_report_path"] == REPORT_2
    assert receipt["repair_wake"]["work_reexecution_authorized"] is False
    assert receipt["repair_wake"]["scope_expansion_authorized"] is False
    assert receipt["corrected_attempt"]["report_attempt"] == 2
    assert receipt["corrected_attempt"]["report_state"] == "REPORT_VALIDATED"
    assert receipt["duplicate_suppressed"] is True
    assert receipt["stale_attempt_ignored"] is True
    assert receipt["same_execution_row"] is True
    assert receipt["second_runtime_ledger_created"] is False
    assert receipt["repair_state"] == "REPORT_REPAIR_ACCEPTED"


def test_synthetic_repair_cli_releases_temporary_sqlite_handles() -> None:
    app_root = Path(__file__).resolve().parents[1]
    script = app_root / "automation" / "run_synthetic_worker_result_repair_pilot.py"

    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=app_root,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "SYNTHETIC_RESULT_REPAIR_OK" in completed.stdout
    assert "LIFEOS_SYNTHETIC_RESULT_REPAIR_RECEIPT=" in completed.stdout
