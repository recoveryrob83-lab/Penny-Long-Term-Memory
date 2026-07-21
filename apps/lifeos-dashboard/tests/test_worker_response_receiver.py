import json
import sqlite3
from pathlib import Path

import pytest

from lifeos_dashboard.worker_command_center import WorkerExecutionHistoryStore
from lifeos_dashboard.worker_operations import (
    BrowserTransportEvidence,
    BrowserWorkerEvidenceStore,
)
from lifeos_dashboard.worker_response_receiver import (
    WORKER_REPORT_PREFIX,
    parse_worker_execution_report,
)
from lifeos_dashboard.worker_runtime import WorkerRuntimeError
from worker_response_test_support import (
    advisory,
    outcome_row,
    report_payload,
    response_text,
    setup_run,
    transport_result,
    write_sources,
)


def test_machine_report_parser_requires_exactly_one_marker() -> None:
    parsed = parse_worker_execution_report(response_text())
    assert parsed.controlled_outcome == "IMPLEMENT"
    with pytest.raises(WorkerRuntimeError, match="exactly one"):
        parse_worker_execution_report("No marker")


def test_valid_report_records_same_row_implement_and_pending_hq_review(
    tmp_path: Path,
) -> None:
    receiver, active, entry, database = setup_run(tmp_path)

    result = receiver.reconcile(active, entry, response_text())
    row = outcome_row(database, active.run_id)

    assert result.controlled_outcome == "IMPLEMENT"
    assert result.report_consistent is True
    assert result.hq_review_required is True
    assert row["controlled_outcome"] == "IMPLEMENT"
    assert row["receiver_accepted_at"] is not None
    assert row["receiver_verification_state"] == "pending"
    assert row["worker_reported_outcome"] == "IMPLEMENT"


def test_missing_or_duplicate_machine_report_holds_safely(tmp_path: Path) -> None:
    missing, active, entry, database = setup_run(
        tmp_path / "missing", stdout="CONTROLLED_OUTCOME: IMPLEMENT"
    )
    missing_result = missing.reconcile(active, entry, "CONTROLLED_OUTCOME: IMPLEMENT")
    assert missing_result.controlled_outcome == "REPORT_AND_HOLD"
    assert outcome_row(database, active.run_id)["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )

    duplicate_text = (
        response_text() + "\n" + WORKER_REPORT_PREFIX + json.dumps(report_payload())
    )
    duplicate, active2, entry2, database2 = setup_run(
        tmp_path / "duplicate", stdout=duplicate_text
    )
    duplicate_result = duplicate.reconcile(active2, entry2, duplicate_text)
    assert duplicate_result.controlled_outcome == "REPORT_AND_HOLD"
    assert outcome_row(database2, active2.run_id)["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )


def test_incomplete_implement_evidence_is_receiver_hold(tmp_path: Path) -> None:
    response = response_text(evidence_references=[])
    receiver, active, entry, database = setup_run(tmp_path, stdout=response)

    result = receiver.reconcile(active, entry, response)

    assert result.reported_outcome == "IMPLEMENT"
    assert result.controlled_outcome == "REPORT_AND_HOLD"
    assert result.report_consistent is False
    assert "evidence" in result.reason.lower()
    assert outcome_row(database, active.run_id)["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )


def test_report_identity_conflict_is_receiver_hold(tmp_path: Path) -> None:
    response = response_text(run_id="RUN-WRONG")
    receiver, active, entry, database = setup_run(tmp_path, stdout=response)

    result = receiver.reconcile(active, entry, response)

    assert result.controlled_outcome == "REPORT_AND_HOLD"
    assert "does not match" in result.reason
    assert outcome_row(database, active.run_id)["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )


def test_duplicate_reconciliation_returns_existing_outcome_without_second_write(
    tmp_path: Path,
) -> None:
    receiver, active, entry, database = setup_run(tmp_path)
    first = receiver.reconcile(active, entry, response_text())
    second = receiver.reconcile(active, entry, response_text())

    assert first.controlled_outcome == "IMPLEMENT"
    assert second.state == "already_reconciled"
    assert second.controlled_outcome == "IMPLEMENT"
    with sqlite3.connect(database) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM execution_history WHERE run_id = ?", (active.run_id,)
        ).fetchone()[0]
    assert count == 1


def test_stale_revision_is_held_without_overwriting_newer_receiver_state(
    tmp_path: Path,
) -> None:
    receiver2, active2, entry, database = setup_run(
        tmp_path, revision=2, stdout=response_text(2)
    )
    assert (
        receiver2.reconcile(active2, entry, response_text(2)).controlled_outcome
        == "IMPLEMENT"
    )

    write_sources(tmp_path, revision=1)
    active1 = advisory(1)
    old_response = response_text(1)
    WorkerExecutionHistoryStore(database).record(
        transport_result(active1, old_response)
    )
    BrowserWorkerEvidenceStore(database).attach(
        active1.run_id,
        BrowserTransportEvidence(
            reported_outcome="IMPLEMENT",
            assistant_turn_id="conversation-turn-old",
            browser_receipt_json=json.dumps({"response_text": old_response}),
        ),
    )

    stale = receiver2.reconcile(active1, entry, old_response)

    assert stale.controlled_outcome == "REPORT_AND_HOLD"
    state = receiver2.receiver.runtime.store.receiver_state(
        "engineering_worker", "ADV-TEST"
    )
    assert state is not None
    assert state.last_processed_revision == 2
    assert outcome_row(database, active1.run_id)["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )


def test_canonical_checksum_conflict_holds_before_report_acceptance(
    tmp_path: Path,
) -> None:
    receiver, active, entry, database = setup_run(tmp_path, checksum="SHA256:wrong")

    result = receiver.reconcile(active, entry, response_text())

    assert result.controlled_outcome == "REPORT_AND_HOLD"
    assert "checksum" in result.reason.lower()
    assert outcome_row(database, active.run_id)["receiver_accepted_at"] is None


def test_immediate_hq_report_cannot_self_verify(tmp_path: Path) -> None:
    response = response_text(verification_state="verified")
    receiver, active, entry, database = setup_run(tmp_path, stdout=response)

    result = receiver.reconcile(active, entry, response)

    assert result.controlled_outcome == "REPORT_AND_HOLD"
    assert "Immediate HQ review" in result.reason
    assert outcome_row(database, active.run_id)["controlled_outcome"] == (
        "REPORT_AND_HOLD"
    )
