from pathlib import Path

import pytest

from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerRegistryEntry,
    WorkerRuntimeError,
)
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService


def entry(**overrides: object) -> WorkerRegistryEntry:
    values: dict[str, object] = {
        "worker_id": "office_leaks_worker",
        "chat_title": "OfficeLeaks_Worker",
        "owning_department": "office-leaks-consulting",
        "profile_path": "projects/office-leaks-consulting/workers/general.md",
        "profile_version": 1,
    }
    values.update(overrides)
    return WorkerRegistryEntry.from_dict(values)


def envelope(**overrides: object) -> ExecutionEnvelope:
    values: dict[str, object] = {
        "wrapper_id": "WRAP-1",
        "run_id": "RUN-1",
        "worker_id": "office_leaks_worker",
        "task_id": "ADV-1",
        "task_revision": 1,
        "procedure_id": "test_procedure",
        "procedure_version": 1,
        "authorization_source": "Rob",
        "verification_mode": "ROUTINE_BATCH",
    }
    values.update(overrides)
    return ExecutionEnvelope.from_dict(values)


def service(tmp_path: Path) -> WorkerRuntimeService:
    return WorkerRuntimeService(tmp_path / "command-center.sqlite3")


def test_service_registers_and_resolves_exact_title(tmp_path: Path) -> None:
    runtime = service(tmp_path)
    runtime.register_worker(entry())

    assert runtime.resolve_title("OfficeLeaks_Worker").worker_id == "office_leaks_worker"


def test_service_fails_closed_for_unknown_route(tmp_path: Path) -> None:
    runtime = service(tmp_path)
    runtime.register_worker(entry())

    with pytest.raises(WorkerRuntimeError, match="route is unknown"):
        runtime.validate_envelope(envelope())


def test_service_accepts_available_new_revision(tmp_path: Path) -> None:
    runtime = service(tmp_path)
    runtime.register_worker(entry())
    runtime.set_route_state("office_leaks_worker", "available", last_seen_at=1.0)

    accepted = runtime.accept_envelope(envelope())

    assert accepted.worker_id == "office_leaks_worker"
    state = runtime.store.receiver_state("office_leaks_worker", "ADV-1")
    assert state is not None
    assert state.last_processed_revision == 1


def test_service_suppresses_duplicate_revision(tmp_path: Path) -> None:
    runtime = service(tmp_path)
    runtime.register_worker(entry())
    runtime.set_route_state("office_leaks_worker", "available")
    runtime.accept_envelope(envelope(run_id="RUN-1"))

    with pytest.raises(WorkerRuntimeError, match="stale or already processed"):
        runtime.accept_envelope(envelope(run_id="RUN-2"))


def test_paused_deployment_blocks_execution(tmp_path: Path) -> None:
    runtime = service(tmp_path)
    runtime.register_worker(entry())
    runtime.set_route_state("office_leaks_worker", "available")
    runtime.set_deployment_state("office_leaks_worker", "paused")

    with pytest.raises(WorkerRuntimeError, match="paused, not enabled"):
        runtime.validate_envelope(envelope())


def test_service_validates_untyped_deployment_state(tmp_path: Path) -> None:
    runtime = service(tmp_path)
    runtime.register_worker(entry())

    with pytest.raises(WorkerRuntimeError, match="enabled, paused, or retired"):
        runtime.set_deployment_state_from_text("office_leaks_worker", "active")
