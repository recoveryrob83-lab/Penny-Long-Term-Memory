from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import WorkerCommandJob
from lifeos_dashboard.worker_report_repair_live_recovery_runtime import (
    _trusted_stale_markers,
    run_worker_report_repair_browser_dispatch,
)
from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerRegistryEntry,
    WorkerRuntimeError,
)

AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

SCRIPT = AUTOMATION / "chatgpt_worker_report_repair_dispatch.py"
SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_report_repair_dispatch_test",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
repair_script = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = repair_script
SPEC.loader.exec_module(repair_script)

RUN_ID = "RUN-ADV-20260726-053-R1"
ORIGINAL_WRAPPER = "WAKE-ADV-20260726-053-R1"
REPAIR_WRAPPER = "REPAIR-ADV-20260726-053-R1-A2"


class FakePrompt:
    def __init__(self, text: str) -> None:
        self.text = text
        self.fill_calls: list[str] = []

    def evaluate(self, _script: str) -> str:
        return self.text

    def fill(self, value: str) -> None:
        self.fill_calls.append(value)
        self.text = value


class FakeUserNodes:
    def filter(self, *, has_text: str):
        return self

    def count(self) -> int:
        return 0

    def nth(self, index: int):
        raise IndexError(index)


class FakePage:
    def locator(self, _selector: str):
        return FakeUserNodes()


def _lifeos_draft(wrapper_id: str, run_id: str) -> str:
    payload = json.dumps(
        {
            "wrapper_id": wrapper_id,
            "run_id": run_id,
            "worker_id": "maintenance_worker",
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"LIFEOS_EXECUTION_WRAPPER={payload}\n\nOld bounded instruction"


def _database(tmp_path: Path, *, user_turn_id: str = "conversation-turn-original") -> Path:
    database = tmp_path / "command_center.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history(
                id INTEGER PRIMARY KEY,
                run_id TEXT,
                mode TEXT,
                prompt_type TEXT,
                wrapper_id TEXT,
                dispatch_state TEXT,
                user_turn_id TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO execution_history(
                id, run_id, mode, prompt_type, wrapper_id, dispatch_state, user_turn_id
            ) VALUES(1, ?, 'send', 'worker', ?, 'DISPATCH_SUBMITTED', ?)
            """,
            (RUN_ID, ORIGINAL_WRAPPER, user_turn_id),
        )
    return database


def _job() -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=ExecutionEnvelope(
            wrapper_id=REPAIR_WRAPPER,
            run_id=RUN_ID,
            worker_id="maintenance_worker",
            task_id="ADV-20260726-053",
            task_revision=1,
            procedure_id="maintenance_coordinated_repository_repair",
            procedure_version=1,
            authorization_source="ROB-DIRECT-COORDINATED-REPAIR-20260726",
            verification_mode="IMMEDIATE_HQ",
        ),
        instruction="Correct only report-002.json. Do not rerun the audit.",
        mode="send",
        confirm_send=True,
    )


def _entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="maintenance_worker",
        chat_title="Maintenance_Worker",
        owning_department="maintenance",
        profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/c/maintenance-worker-test",
        route_revision=1,
    )


def test_database_proof_returns_original_stale_markers(tmp_path: Path) -> None:
    database = _database(tmp_path)

    assert _trusted_stale_markers(database, RUN_ID) == (ORIGINAL_WRAPPER, RUN_ID)


def test_database_proof_requires_correlated_user_turn(tmp_path: Path) -> None:
    database = _database(tmp_path, user_turn_id="")

    with pytest.raises(WorkerRuntimeError, match="correlated user-turn proof"):
        _trusted_stale_markers(database, RUN_ID)


def test_trusted_stale_draft_clears_without_rendered_original_turn() -> None:
    stale = _lifeos_draft(ORIGINAL_WRAPPER, RUN_ID)
    prompt = FakePrompt(stale)

    repair_script._install_trusted_stale_clear(
        wrapper_id=ORIGINAL_WRAPPER,
        run_id=RUN_ID,
    )

    assert repair_script.browser_dispatch._prepare_existing_draft(
        FakePage(),
        prompt,
        repair_script.BrowserRoundTripRequest(
            worker_url="https://chatgpt.com/c/maintenance-worker-test",
            worker_chat_title="Maintenance_Worker",
            project_title="LifeOS",
            prompt_text=f"{REPAIR_WRAPPER} {RUN_ID}",
            request_marker=REPAIR_WRAPPER,
            response_marker=RUN_ID,
        ),
    ) is False
    assert prompt.text == ""
    assert prompt.fill_calls == [""]


def test_correction_transport_uses_trusted_markers_and_returns_receipt(
    monkeypatch,
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    monkeypatch.setenv("COMMAND_CENTER_DATABASE_PATH", str(database))
    captured: list[str] = []

    def fake_run(command, **_kwargs):
        captured.extend(command)
        receipt = {
            "status": "submitted",
            "request_marker": REPAIR_WRAPPER,
            "run_id": RUN_ID,
            "submission_confirmed": True,
            "user_turn_id": "conversation-turn-repair",
            "returned_to_source": True,
        }
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=(
                "BROWSER_DISPATCH_OK\n"
                "LIFEOS_BROWSER_DISPATCH_RECEIPT="
                + json.dumps(receipt)
                + "\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    result, evidence = run_worker_report_repair_browser_dispatch(
        _job(),
        _entry(),
        tmp_path,
        trigger="manual",
    )

    assert result.status == "succeeded"
    assert evidence.user_turn_id == "conversation-turn-repair"
    assert "chatgpt_worker_report_repair_dispatch.py" in " ".join(captured)
    stale_wrapper_index = captured.index("--trusted-stale-wrapper-id")
    stale_run_index = captured.index("--trusted-stale-run-id")
    assert captured[stale_wrapper_index + 1] == ORIGINAL_WRAPPER
    assert captured[stale_run_index + 1] == RUN_ID


def test_safe_stop_includes_underlying_browser_detail(monkeypatch, tmp_path: Path) -> None:
    database = _database(tmp_path)
    monkeypatch.setenv("COMMAND_CENTER_DATABASE_PATH", str(database))

    def fake_run(command, **_kwargs):
        return subprocess.CompletedProcess(
            command,
            2,
            stdout="",
            stderr=(
                "STOPPED: Worker composer contains a different unsent draft. "
                "It was preserved.\n"
            ),
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    result, _evidence = run_worker_report_repair_browser_dispatch(
        _job(),
        _entry(),
        tmp_path,
        trigger="manual",
    )

    assert result.status == "failed"
    assert "stopped safely before" in result.reason
    assert "different unsent draft" in result.reason
