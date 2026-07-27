from pathlib import Path

from lifeos_dashboard.worker_advisory_pipeline import (
    parse_advisory_index,
    parse_execution_ready_advisory,
)
from lifeos_dashboard.worker_receiver import (
    WorkerReceiverService,
    checksum_parameters,
)
from lifeos_dashboard.worker_receiver_resolution import resolve_receiver_assignment
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry


ADVISORY_ID = "ADV-20260726-053"
APPROVAL_REFERENCE = "ROB-DIRECT-COORDINATED-REPAIR-20260726"


def test_repository_audit_advisory_resolves_as_exact_rob_approved_repair() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    index_text = (repository_root / "coordination/ADVISORY_INDEX.md").read_text(
        encoding="utf-8"
    )
    records = parse_advisory_index(index_text)
    record = next(item for item in records if item.advisory_id == ADVISORY_ID)
    board_text = (repository_root / record.board_path).read_text(encoding="utf-8")
    advisory = parse_execution_ready_advisory(board_text, record)

    assert advisory is not None
    assert advisory.target_worker_id == "maintenance_worker"
    assert advisory.task_class == "coordinated_repository_repair"
    assert advisory.authorization_source == "ROB"
    assert advisory.verification_mode == "IMMEDIATE_HQ"
    assert advisory.result_contract is not None
    assert (
        advisory.result_contract.submission_procedure_id
        == "maintenance_worker_result_submission"
    )
    assert advisory.result_contract.result_path == (
        "projects/life-logistics-hq/worker-results/maintenance_worker/"
        "RUN-ADV-20260726-053-R1/report-001.json"
    )

    entry = WorkerRegistryEntry(
        worker_id="maintenance_worker",
        chat_title="Maintenance_Worker",
        owning_department="maintenance",
        profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/g/project/c/maintenance-worker",
        route_revision=1,
    )
    resolution = resolve_receiver_assignment(repository_root, advisory, entry)
    assignment = resolution.assignment

    assert resolution.procedure_path == (
        "projects/life-logistics-hq/procedures/"
        "maintenance_coordinated_repository_repair.md"
    )
    assert assignment.approval_reference == APPROVAL_REFERENCE
    assert APPROVAL_REFERENCE in assignment.source_references
    assert assignment.requests_cross_department_authority is True
    assert assignment.requests_material_exception is True
    assert assignment.requests_new_spending is False
    assert assignment.requests_new_connector is False
    assert assignment.requested_read_scopes == (
        "memory",
        "coordination",
        "projects",
        "apps",
        "workers",
    )
    assert assignment.requested_write_scopes[:3] == (
        "memory",
        "coordination",
        "projects",
    )
    assert assignment.procedure_checksum == resolution.procedure.checksum
    assert assignment.parameters_checksum == checksum_parameters(assignment.parameters)
    assert WorkerReceiverService._requires_elevation(assignment) is False
    assert (
        WorkerReceiverService._semantic_errors(
            assignment,
            resolution.profile,
            resolution.procedure,
        )
        == ()
    )
