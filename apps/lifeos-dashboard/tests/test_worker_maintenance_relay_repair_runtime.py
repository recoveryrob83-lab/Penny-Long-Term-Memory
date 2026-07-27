from __future__ import annotations

from types import SimpleNamespace

import pytest

from lifeos_dashboard.worker_github_orchestrator import (
    WorkerGitHubOrchestrator,
)
from lifeos_dashboard.worker_maintenance_relay_repair_runtime import (
    _canonical_hq_review_path,
    _canonical_rob_validation_path,
    _normalized_scope,
    _parse_evidence_reference,
    _reserve_automatic_hq_wake_budget,
    _scope_allows,
    _unauthorized_scopes,
    _uncovered_scopes,
)
from lifeos_dashboard.worker_result_ingester import WorkerResultIngester
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


COMMIT_SHA = "0123456789abcdef0123456789abcdef01234567"
BLOB_SHA = "89abcdef0123456789abcdef0123456789abcdef"
RUN_ID = "RUN-ADV-20260726-053-R1"


def test_scope_containment_accepts_descendants_and_annotations() -> None:
    assert _normalized_scope(
        "apps (read-only schema evidence)"
    ) == "apps"
    assert _scope_allows(
        "memory",
        "memory/HQ_NAMING_STANDARD.md",
    )
    assert _scope_allows(
        "apps",
        "apps (read-only schema evidence)",
    )
    assert not _scope_allows(
        "memory",
        "coordination/ADVISORY_INDEX.md",
    )
    assert _unauthorized_scopes(
        ("memory", "coordination"),
        (
            "memory/01_SESSION_HANDOFF.md",
            "coordination/ADVISORY_INDEX.md",
        ),
    ) == []
    assert _uncovered_scopes(
        ("memory", "coordination"),
        (
            "memory/01_SESSION_HANDOFF.md",
            "coordination/ADVISORY_INDEX.md",
        ),
    ) == []


def test_evidence_parser_accepts_canonical_git_witnesses() -> None:
    assert _parse_evidence_reference(
        f"memory/file.md@{BLOB_SHA}"
    ) == (
        "memory/file.md",
        None,
        BLOB_SHA,
    )
    assert _parse_evidence_reference(
        f"memory/file.md@blob:{BLOB_SHA}"
    ) == (
        "memory/file.md",
        None,
        BLOB_SHA,
    )
    assert _parse_evidence_reference(
        f"memory/file.md@commit:{COMMIT_SHA}@blob:{BLOB_SHA}"
    ) == (
        "memory/file.md",
        COMMIT_SHA,
        BLOB_SHA,
    )
    assert _parse_evidence_reference(
        "projects/result.json@preflight:not-found"
    ) == (
        "projects/result.json",
        None,
        None,
    )
    with pytest.raises(WorkerRuntimeError, match="witness is invalid"):
        _parse_evidence_reference(
            "memory/file.md@sha256:example"
        )


def test_maintenance_paths_use_life_logistics_project_root() -> None:
    row = {
        "owning_department": "maintenance",
        "worker_id": "maintenance_worker",
    }
    assert _canonical_hq_review_path(row, RUN_ID) == (
        "projects/life-logistics-hq/worker-results/maintenance_worker/"
        f"{RUN_ID}/hq-review-001.json"
    )
    assert _canonical_rob_validation_path(row, RUN_ID) == (
        "projects/life-logistics-hq/worker-results/maintenance_worker/"
        f"{RUN_ID}/rob-validation-001.json"
    )


def _correlation_fixture():
    ingester = object.__new__(WorkerResultIngester)

    def git_object_type(*arguments: str) -> str:
        return "commit" if arguments[-1] == COMMIT_SHA else "blob"

    ingester._git = git_object_type
    result_path = (
        "projects/life-logistics-hq/worker-results/maintenance_worker/"
        f"{RUN_ID}/report-001.json"
    )
    envelope = SimpleNamespace(
        wrapper_id="WAKE-ADV-20260726-053-R1",
        run_id=RUN_ID,
        worker_id="maintenance_worker",
        task_id="ADV-20260726-053",
        task_revision=1,
        procedure_id="maintenance_coordinated_repository_repair",
        procedure_version=1,
        authorization_source="ROB",
        verification_mode="IMMEDIATE_HQ",
    )
    advisory = SimpleNamespace(
        result_contract=SimpleNamespace(
            attempt=1,
            result_path=result_path,
        ),
        requested_read_scopes=(
            "memory",
            "coordination",
            "projects",
            "apps",
            "workers",
        ),
        requested_write_scopes=(
            "memory",
            "coordination",
            "projects",
            result_path,
        ),
        requested_tools=("GitHub",),
        source_references=("memory/HQ_NAMING_STANDARD.md",),
        target_worker_id="maintenance_worker",
        envelope=lambda: envelope,
    )
    profile = SimpleNamespace(
        profile_version=1,
        owning_department="maintenance",
        worker_id="maintenance_worker",
    )
    payload = {
        "wrapper_id": envelope.wrapper_id,
        "run_id": envelope.run_id,
        "worker_id": envelope.worker_id,
        "task_id": envelope.task_id,
        "task_revision": envelope.task_revision,
        "procedure_id": envelope.procedure_id,
        "procedure_version": envelope.procedure_version,
        "authorization_source": envelope.authorization_source,
        "verification_mode": envelope.verification_mode,
        "profile_version": 1,
        "owning_department": "maintenance",
        "attempt": 1,
        "actual_read_scopes": [
            "memory/HQ_NAMING_STANDARD.md",
            "coordination/ADVISORY_INDEX.md",
            "projects/life-logistics-hq/status.md",
            "apps (read-only schema evidence)",
            "workers (read-only search-index evidence)",
        ],
        "actual_write_scopes": [
            "memory/HQ_NAMING_STANDARD.md",
            result_path,
        ],
        "actual_tools": ["GitHub"],
        "controlled_outcome": "REPORT_AND_HOLD",
        "completion_state": "partial",
        "verification_state": "pending",
        "failure_reason": "One bounded hold remains.",
        "evidence_references": [
            "memory/HQ_NAMING_STANDARD.md@"
            f"commit:{COMMIT_SHA}@blob:{BLOB_SHA}"
        ],
    }
    return ingester, advisory, profile, payload


def test_report_correlation_accepts_broad_scopes_and_git_evidence() -> None:
    ingester, advisory, profile, payload = _correlation_fixture()

    ingester._validate_report_correlation(
        advisory,
        profile,
        payload,
    )


def test_report_correlation_retains_exact_tool_boundary() -> None:
    ingester, advisory, profile, payload = _correlation_fixture()
    payload["actual_tools"] = [
        "GitHub",
        "local non-mutating validation",
    ]

    with pytest.raises(
        WorkerRuntimeError,
        match="actual tools exceed assignment",
    ):
        ingester._validate_report_correlation(
            advisory,
            profile,
            payload,
        )


class _Decision:
    def __init__(
        self,
        *,
        reserved: bool,
        reason: str = "",
    ) -> None:
        self.reserved = reserved
        self.reason = reason


class _CommandCenter:
    def __init__(self, decision: _Decision) -> None:
        self.decision = decision
        self.reservations: list[tuple[str, str]] = []
        self.evidence: list[tuple[str, _Decision]] = []
        self.pauses: list[dict[str, object]] = []

    def reserve_send_budget(
        self,
        *,
        kind: str,
        run_id: str,
    ) -> _Decision:
        self.reservations.append((kind, run_id))
        return self.decision

    def append_send_budget_evidence(
        self,
        *,
        run_id: str,
        decision: _Decision,
    ) -> None:
        self.evidence.append((run_id, decision))

    def trip_safety_pause(self, **kwargs: object) -> None:
        self.pauses.append(kwargs)


def test_automatic_hq_wake_reserves_budget_and_persists_evidence() -> None:
    command_center = _CommandCenter(_Decision(reserved=True))
    orchestrator = SimpleNamespace(
        operations=SimpleNamespace(command_center=command_center)
    )

    decision = _reserve_automatic_hq_wake_budget(
        orchestrator,
        "RUN-1",
    )

    assert decision.reserved is True
    assert command_center.reservations == [
        ("hq_review_wake", "RUN-1")
    ]
    assert command_center.evidence == [("RUN-1", decision)]
    assert command_center.pauses == []


def test_automatic_hq_wake_budget_refusal_trips_pause() -> None:
    command_center = _CommandCenter(
        _Decision(
            reserved=False,
            reason="Budget exhausted.",
        )
    )
    orchestrator = SimpleNamespace(
        operations=SimpleNamespace(command_center=command_center)
    )

    with pytest.raises(WorkerRuntimeError, match="Budget exhausted"):
        _reserve_automatic_hq_wake_budget(
            orchestrator,
            "RUN-2",
        )

    assert command_center.evidence == []
    assert command_center.pauses[0]["affected_run_id"] == "RUN-2"


def test_orchestrator_ingests_prepared_report_attempt_two() -> None:
    corrected_path = (
        "projects/life-logistics-hq/worker-results/maintenance_worker/"
        f"{RUN_ID}/report-002.json"
    )
    events: list[tuple[str, str]] = []
    ingested: list[str] = []
    row = {
        "result_state": "REPORT_REJECTED",
        "repair_state": "REPORT_REPAIR_PENDING",
    }
    wake = SimpleNamespace(corrected_report_path=corrected_path)
    orchestrator = SimpleNamespace(
        _row=lambda run_id: row,
        _artifact_exists=lambda path: path == corrected_path,
        operations=SimpleNamespace(
            result_repair=SimpleNamespace(
                repair_wake=lambda run_id: wake
            ),
            ingest_result=lambda run_id: (
                ingested.append(run_id)
                or {
                    "receipt": {
                        "report_state": "REPORT_VALIDATED"
                    }
                }
            ),
        ),
        _event=lambda action, status, detail, **kwargs: events.append(
            (action, status)
        ),
    )
    advisory = SimpleNamespace(
        advisory_id="ADV-20260726-053",
        run_id=RUN_ID,
        result_contract=SimpleNamespace(
            result_path="ignored-report-001.json"
        ),
    )

    WorkerGitHubOrchestrator._ingest_result_if_present(
        orchestrator,
        advisory,
    )

    assert ingested == [RUN_ID]
    assert events == [("result_ingestion", "succeeded")]
    assert WorkerGitHubOrchestrator._send_hq_wake.__module__.endswith(
        "worker_maintenance_relay_repair_runtime"
    )
