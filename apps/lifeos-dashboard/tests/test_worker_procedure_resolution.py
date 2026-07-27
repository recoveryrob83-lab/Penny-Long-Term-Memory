from pathlib import Path

from lifeos_dashboard.worker_advisory_pipeline import ExecutionReadyAdvisory
from lifeos_dashboard.worker_procedure_resolution import load_canonical_procedure
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry


def test_maintenance_procedure_resolves_through_canonical_project_mapping() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    entry = WorkerRegistryEntry(
        worker_id="maintenance_worker",
        chat_title="Maintenance_Worker",
        owning_department="maintenance",
        profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/g/project/c/maintenance-worker",
        route_revision=1,
    )
    advisory = ExecutionReadyAdvisory(
        advisory_id="ADV-MAINTENANCE-PROCEDURE-PATH-TEST",
        title="Maintenance procedure path test",
        board_path="coordination/boards/engineering.md",
        target_department="maintenance",
        target_worker_id="maintenance_worker",
        advisory_revision=1,
        task_class="coordinated_repository_repair",
        authorization_class="BOUNDED_WRITE",
        procedure_id="maintenance_coordinated_repository_repair",
        procedure_version=1,
        authorization_source="ROB",
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="OPEN",
        priority="NORMAL",
    )

    procedure, path = load_canonical_procedure(
        repository_root,
        entry,
        advisory,
    )

    assert path == (
        "projects/life-logistics-hq/procedures/"
        "maintenance_coordinated_repository_repair.md"
    )
    assert procedure.procedure_id == "maintenance_coordinated_repository_repair"
    assert procedure.task_class == "coordinated_repository_repair"
    assert procedure.required_verification_mode == "IMMEDIATE_HQ"
