from pathlib import Path

from lifeos_dashboard.worker_advisory_pipeline import ExecutionReadyAdvisory
from lifeos_dashboard.worker_profile_resolution import load_worker_authority_profile
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry


def _advisory(
    *,
    task_class: str = "read_only_governance_audit",
    authorization_source: str = "MAINTENANCE_HQ",
) -> ExecutionReadyAdvisory:
    return ExecutionReadyAdvisory(
        advisory_id="ADV-MAINTENANCE-WORKER-PROFILE-TEST",
        title="Maintenance Worker profile test",
        board_path="coordination/boards/maintenance.md",
        target_department="maintenance",
        target_worker_id="maintenance_worker",
        advisory_revision=1,
        task_class=task_class,
        authorization_class="BOUNDED_WRITE",
        procedure_id="maintenance_worker_result_submission",
        procedure_version=1,
        authorization_source=authorization_source,
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="EXECUTION_READY",
        priority="NORMAL",
        requested_read_scopes=("memory/STARTUP_BOOT.md",),
        requested_write_scopes=(
            "projects/life-logistics-hq/worker-results/maintenance_worker/"
            "RUN-TEST/report-001.json",
        ),
        requested_tools=("GitHub",),
    )


def _entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="maintenance_worker",
        chat_title="Maintenance_Worker",
        owning_department="maintenance",
        profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
        profile_version=1,
        conversation_url="https://chatgpt.com/g/project/c/maintenance-worker",
        route_revision=1,
    )


def test_maintenance_profile_loads_explicit_receiver_contract() -> None:
    repository_root = Path(__file__).resolve().parents[3]

    profile, labels = load_worker_authority_profile(
        repository_root,
        _entry(),
        _advisory(),
    )

    assert profile.allowed_task_classes == (
        "read_only_verification",
        "read_only_governance_audit",
    )
    assert profile.calling_source_task_classes["MAINTENANCE_HQ"] == (
        "read_only_verification",
        "read_only_governance_audit",
    )
    assert profile.read_scope_prefixes == ("memory", "coordination", "projects")
    assert profile.write_scope_prefixes == (
        "projects/life-logistics-hq/worker-results/maintenance_worker",
    )
    assert profile.approved_tools == ("GitHub",)
    assert profile.allowed_verification_modes == ("IMMEDIATE_HQ",)
    assert "maintenance_write" in profile.prohibited_task_classes
    assert labels == ("maintenance", "logistics", "Maintenance_HQ")


def test_maintenance_profile_authorizes_rob_for_same_bounded_task_classes() -> None:
    repository_root = Path(__file__).resolve().parents[3]

    profile, _ = load_worker_authority_profile(
        repository_root,
        _entry(),
        _advisory(authorization_source="ROB"),
    )

    assert profile.calling_source_task_classes["ROB"] == (
        "read_only_verification",
        "read_only_governance_audit",
    )
