from pathlib import Path

from lifeos_dashboard.worker_advisory_pipeline import ExecutionReadyAdvisory, build_wake_job
from lifeos_dashboard.worker_profile_resolution import load_worker_authority_profile
from lifeos_dashboard.worker_report import WORKER_REPORT_PREFIX
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def advisory() -> ExecutionReadyAdvisory:
    return ExecutionReadyAdvisory(
        advisory_id="ADV-TEST",
        title="Verify receiver profile resolution",
        board_path="coordination/boards/engineering.md",
        target_department="Engineering HQ",
        target_worker_id="engineering_worker",
        advisory_revision=1,
        task_class="engineering_read_only_verification",
        authorization_class="READ_ONLY",
        procedure_id="engineering_worker_read_only_verification",
        procedure_version=1,
        authorization_source="ROB-TEST",
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="OPEN",
        priority="NORMAL",
    )


def entry() -> WorkerRegistryEntry:
    return WorkerRegistryEntry(
        worker_id="engineering_worker",
        chat_title="Engineering_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/engineering_worker.md",
        profile_version=1,
    )


def test_real_profile_keeps_shared_sources_read_only() -> None:
    profile, labels = load_worker_authority_profile(
        REPOSITORY_ROOT, entry(), advisory()
    )

    assert "Engineering HQ" in labels
    assert "memory" in profile.read_scope_prefixes
    assert "coordination" in profile.read_scope_prefixes
    assert "projects/engineering" in profile.write_scope_prefixes
    assert "apps/lifeos-dashboard" in profile.write_scope_prefixes
    assert "memory" not in profile.write_scope_prefixes
    assert "coordination" not in profile.write_scope_prefixes


def test_dispatch_wake_does_not_install_superseded_chat_report_contract() -> None:
    instruction = build_wake_job(advisory()).instruction

    assert WORKER_REPORT_PREFIX not in instruction
    assert "Package E response contract" not in instruction
