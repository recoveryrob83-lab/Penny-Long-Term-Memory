from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

from lifeos_dashboard.worker_route_management import CapturedConversation
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

SCRIPT = AUTOMATION / "recover_worker_hq_review_wake.py"
SPEC = importlib.util.spec_from_file_location("recover_worker_hq_review_wake_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
recovery = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = recovery
SPEC.loader.exec_module(recovery)

RUN_ID = "RUN-ADV-20260726-053-R1"
HQ_URL = "https://chatgpt.com/c/maintenance-hq-test"


def _database(tmp_path: Path, **overrides) -> Path:
    database = tmp_path / "command_center.sqlite3"
    values = {
        "result_state": "REPORT_VALIDATED",
        "hq_wake_claimed_at": 123.0,
        "hq_wake_state": None,
        "hq_wake_user_turn_id": None,
        "hq_wake_receipt_json": None,
        "hq_review_state": None,
    }
    values.update(overrides)
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE execution_history(
                id INTEGER PRIMARY KEY,
                run_id TEXT,
                mode TEXT,
                prompt_type TEXT,
                result_state TEXT,
                hq_wake_claimed_at REAL,
                hq_wake_state TEXT,
                hq_wake_user_turn_id TEXT,
                hq_wake_receipt_json TEXT,
                hq_review_state TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO execution_history(
                id, run_id, mode, prompt_type, result_state,
                hq_wake_claimed_at, hq_wake_state, hq_wake_user_turn_id,
                hq_wake_receipt_json, hq_review_state
            ) VALUES(1, ?, 'send', 'worker', ?, ?, ?, ?, ?, ?)
            """,
            (
                RUN_ID,
                values["result_state"],
                values["hq_wake_claimed_at"],
                values["hq_wake_state"],
                values["hq_wake_user_turn_id"],
                values["hq_wake_receipt_json"],
                values["hq_review_state"],
            ),
        )
    return database


def test_release_pre_submit_claim_clears_only_claim(tmp_path: Path) -> None:
    database = _database(tmp_path)

    receipt = recovery._release_pre_submit_claim(database, RUN_ID)

    assert receipt["run_id"] == RUN_ID
    assert receipt["released_claimed_at"] == 123.0
    with sqlite3.connect(database) as connection:
        row = connection.execute(
            "SELECT hq_wake_claimed_at, result_state FROM execution_history WHERE id = 1"
        ).fetchone()
    assert row == (None, "REPORT_VALIDATED")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("hq_wake_state", "HQ_WAKE_SUBMITTED"),
        ("hq_wake_user_turn_id", "conversation-turn-1"),
        ("hq_wake_receipt_json", "{}"),
        ("hq_review_state", "VERIFIED"),
    ],
)
def test_release_pre_submit_claim_refuses_durable_evidence(
    tmp_path: Path,
    field: str,
    value: str,
) -> None:
    database = _database(tmp_path, **{field: value})

    with pytest.raises(WorkerRuntimeError, match="durable wake or review evidence"):
        recovery._release_pre_submit_claim(database, RUN_ID)

    with sqlite3.connect(database) as connection:
        claimed_at = connection.execute(
            "SELECT hq_wake_claimed_at FROM execution_history WHERE id = 1"
        ).fetchone()[0]
    assert claimed_at == 123.0


def test_release_pre_submit_claim_requires_validated_report(tmp_path: Path) -> None:
    database = _database(tmp_path, result_state="REPORT_REJECTED")

    with pytest.raises(WorkerRuntimeError, match="REPORT_VALIDATED"):
        recovery._release_pre_submit_claim(database, RUN_ID)


def test_exact_active_hq_accepts_matching_route_and_title(monkeypatch) -> None:
    monkeypatch.setattr(
        recovery,
        "capture_chatgpt_conversation",
        lambda _endpoint: CapturedConversation(
            url=HQ_URL,
            title="Maintenance_HQ, chat in project LifeOS",
        ),
    )

    result = recovery._require_exact_active_hq(
        cdp_endpoint="http://127.0.0.1:9222",
        hq_url=HQ_URL,
        hq_chat_title="Maintenance_HQ",
    )

    assert result["url"] == HQ_URL


def test_exact_active_hq_refuses_wrong_route(monkeypatch) -> None:
    monkeypatch.setattr(
        recovery,
        "capture_chatgpt_conversation",
        lambda _endpoint: CapturedConversation(
            url="https://chatgpt.com/c/engineering-hq-test",
            title="Engineering_HQ, chat in project LifeOS",
        ),
    )

    with pytest.raises(WorkerRuntimeError, match="does not match --hq-url"):
        recovery._require_exact_active_hq(
            cdp_endpoint="http://127.0.0.1:9222",
            hq_url=HQ_URL,
            hq_chat_title="Maintenance_HQ",
        )


def test_exact_active_hq_refuses_wrong_title(monkeypatch) -> None:
    monkeypatch.setattr(
        recovery,
        "capture_chatgpt_conversation",
        lambda _endpoint: CapturedConversation(
            url=HQ_URL,
            title="Engineering_HQ, chat in project LifeOS",
        ),
    )

    with pytest.raises(WorkerRuntimeError, match="does not match the owning-HQ title"):
        recovery._require_exact_active_hq(
            cdp_endpoint="http://127.0.0.1:9222",
            hq_url=HQ_URL,
            hq_chat_title="Maintenance_HQ",
        )
