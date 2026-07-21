import copy

import pytest

from lifeos_dashboard.worker_advisory_pipeline import (
    AdvisoryIndexRecord,
    build_wake_job,
    parse_execution_ready_advisory,
)
from lifeos_dashboard.worker_result_contract import (
    WorkerResultContractError,
    artifact_checksum,
    artifact_path,
    build_result_submission_contract,
    load_artifact_examples,
    validate_artifact,
)
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


def test_result_paths_are_deterministic_and_zero_padded() -> None:
    assert artifact_path(
        "engineering",
        "engineering_worker",
        "RUN-ADV-TEST-R1",
        "worker_report",
        1,
    ) == (
        "projects/engineering/worker-results/engineering_worker/"
        "RUN-ADV-TEST-R1/report-001.json"
    )
    assert artifact_path(
        "engineering",
        "engineering_worker",
        "RUN-ADV-TEST-R1",
        "hq_review",
        12,
    ).endswith("/hq-review-012.json")


def test_submission_contract_rejects_wrong_path_or_broader_flags() -> None:
    contract = build_result_submission_contract(
        "engineering", "engineering_worker", "RUN-ADV-TEST-R1"
    )
    assert contract.result_path.endswith("/report-001.json")
    assert contract.create_only is True
    assert contract.overwrite_allowed is False

    with pytest.raises(WorkerResultContractError, match="deterministic path"):
        type(contract)(
            **{
                **contract.to_dict(),
                "result_path": "projects/engineering/worker-results/wrong.json",
            }
        )
    with pytest.raises(WorkerResultContractError, match="re-execution"):
        type(contract)(**{**contract.to_dict(), "work_reexecution_authorized": True})


def test_all_canonical_examples_validate_with_exact_json_types() -> None:
    examples = load_artifact_examples()

    for artifact_kind in ("worker_report", "rejection", "hq_review", "rob_validation"):
        payload = examples[artifact_kind]
        assert validate_artifact(artifact_kind, payload) is payload
        assert artifact_checksum(payload).startswith("sha256:")


def test_worker_report_rejects_string_profile_version_and_unknown_fields() -> None:
    examples = load_artifact_examples()
    wrong_type = copy.deepcopy(examples["worker_report"])
    wrong_type["profile_version"] = "1"

    with pytest.raises(WorkerResultContractError) as exc_info:
        validate_artifact("worker_report", wrong_type)
    assert any(
        "profile_version" in error and "observed string" in error
        for error in exc_info.value.errors
    )

    unknown = copy.deepcopy(examples["worker_report"])
    unknown["surprise_field"] = "drift"
    with pytest.raises(WorkerResultContractError) as unknown_exc:
        validate_artifact("worker_report", unknown)
    assert any("unknown field" in error for error in unknown_exc.value.errors)


def _board(*, result_path: str, authorization_class: str = "BOUNDED_WRITE") -> str:
    return f"""### ADV-TEST — Validate the immutable result outbox

- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Target Department and Owner: Engineering HQ
- Target Worker ID: engineering_worker
- Task Class: engineering_read_only_verification
- Authorization Class: {authorization_class}
- Procedure ID: engineering_worker_result_outbox_validation
- Procedure Version: 1
- Authorization Source: ENGINEERING_HQ_PACKAGE_E_SLICE3_VALIDATION
- Parameters JSON: {{"targets":["projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md"],"verification_questions":["Is Slice 3 bounded?"]}}
- Source References JSON: ["projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md"]
- Requested Read Scopes JSON: ["projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md"]
- Requested Write Scopes JSON: ["{result_path}"]
- Requested Tools JSON: ["GitHub"]
- Completion Condition: Answer the bounded question and create the exact report artifact.
- Result Contract ID: lifeos_worker_result
- Result Contract Version: 1
- Result Submission Procedure ID: engineering_worker_result_submission
- Result Submission Procedure Version: 1
- Result Owning Department: engineering
- Result Attempt: 1
- Result Path: {result_path}
- Result Create Only: true
- Result Overwrite Allowed: false
- Result Work Reexecution Authorized: false
- Result Scope Expansion Authorized: false
"""


def _index() -> AdvisoryIndexRecord:
    return AdvisoryIndexRecord(
        advisory_id="ADV-TEST",
        board_path="coordination/boards/engineering.md",
        target_department="Engineering HQ",
        summary="Validate result outbox",
    )


def test_advisory_accepts_exact_result_contract_and_renders_reminder() -> None:
    result_path = (
        "projects/engineering/worker-results/engineering_worker/"
        "RUN-ADV-TEST-R1/report-001.json"
    )
    advisory = parse_execution_ready_advisory(_board(result_path=result_path), _index())

    assert advisory is not None
    assert advisory.result_contract is not None
    assert advisory.result_contract.result_path == result_path
    assert advisory.requested_write_scopes == (result_path,)
    instruction = build_wake_job(advisory).instruction
    assert "Result submission contract" in instruction
    assert result_path in instruction
    assert "Do not place the machine report only in chat" in instruction


def test_advisory_rejects_wrong_path_or_read_only_authorization() -> None:
    wrong_path = (
        "projects/engineering/worker-results/engineering_worker/"
        "RUN-SOME-OTHER-RUN/report-001.json"
    )
    with pytest.raises(WorkerRuntimeError, match="deterministic path"):
        parse_execution_ready_advisory(_board(result_path=wrong_path), _index())

    expected_path = (
        "projects/engineering/worker-results/engineering_worker/"
        "RUN-ADV-TEST-R1/report-001.json"
    )
    with pytest.raises(WorkerRuntimeError, match="BOUNDED_WRITE"):
        parse_execution_ready_advisory(
            _board(result_path=expected_path, authorization_class="READ_ONLY"),
            _index(),
        )
