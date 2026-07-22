from pathlib import Path

from lifeos_dashboard.worker_advisory_pipeline import (
    build_wake_job,
    parse_advisory_index,
    parse_execution_ready_advisory,
)

ADVISORY_ID = "ADV-20260722-049"
RUN_ID = "RUN-ADV-20260722-049-R1"
MARKER = "LIFEOS_ROB_OBSERVATION=SLICE6_ADV_20260722_049_VISIBLE"
REPORT_PATH = (
    "projects/engineering/worker-results/engineering_worker/"
    f"{RUN_ID}/report-001.json"
)


def test_slice6_advisory_resolves_through_canonical_index_and_board() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    index_text = (repository_root / "coordination/ADVISORY_INDEX.md").read_text(
        encoding="utf-8"
    )
    records = parse_advisory_index(index_text)
    record = next(item for item in records if item.advisory_id == ADVISORY_ID)
    board_text = (repository_root / record.board_path).read_text(encoding="utf-8")

    advisory = parse_execution_ready_advisory(board_text, record)

    assert advisory is not None
    assert advisory.run_id == RUN_ID
    assert advisory.target_worker_id == "engineering_worker"
    assert advisory.procedure_id == "engineering_worker_rob_validation_pilot"
    assert advisory.verification_mode == "IMMEDIATE_HQ"
    assert advisory.authorization_class == "BOUNDED_WRITE"
    assert advisory.parameters["rob_observation_marker"] == MARKER
    assert advisory.result_contract is not None
    assert advisory.result_contract.result_path == REPORT_PATH
    assert advisory.result_contract.create_only is True
    assert advisory.result_contract.overwrite_allowed is False
    assert advisory.result_contract.work_reexecution_authorized is False
    assert advisory.result_contract.scope_expansion_authorized is False

    job = build_wake_job(advisory)
    assert job.envelope.run_id == RUN_ID
    assert MARKER not in job.instruction
    assert "Do not execute from this transport text" in job.instruction
