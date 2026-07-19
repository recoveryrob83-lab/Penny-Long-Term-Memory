from pathlib import Path

import pytest

from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerRegistryEntry,
    WorkerRouteState,
    WorkerRuntimeError,
)
from lifeos_dashboard.worker_runtime_store import WorkerRuntimeStore


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


def test_registry_persists_across_store_instances(tmp_path: Path) -> None:
    database = tmp_path / "command-center.sqlite3"
    first = WorkerRuntimeStore(database)
    first.save_registry_entry(entry())

    second = WorkerRuntimeStore(database)

    assert second.registry_entry("office_leaks_worker") == entry()
    assert second.list_registry() == [entry()]


def test_registry_rejects_duplicate_chat_titles(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")
    store.save_registry_entry(entry())

    with pytest.raises(WorkerRuntimeError, match="conflicts"):
        store.save_registry_entry(entry(worker_id="other_worker"))


def test_route_state_is_separate_from_deployment_state(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")
    store.save_registry_entry(entry(deployment_state="enabled"))
    saved = store.save_route_state(
        WorkerRouteState("office_leaks_worker", "unavailable", pause_reason="App closed")
    )

    registry = store.registry_entry("office_leaks_worker")
    assert saved.availability == "unavailable"
    assert saved.pause_reason == "App closed"
    assert registry is not None
    assert registry.deployment_state == "enabled"


def test_route_state_requires_registered_worker(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")

    with pytest.raises(WorkerRuntimeError, match="existing Worker registry entry"):
        store.save_route_state(WorkerRouteState("office_leaks_worker", "available"))


def test_receiver_state_is_scoped_by_worker_and_task(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")
    store.save_registry_entry(entry())

    first = store.accept_envelope(envelope(task_id="ADV-1", task_revision=8))
    second = store.accept_envelope(envelope(task_id="ADV-2", task_revision=1))

    assert first.last_processed_revision == 8
    assert second.last_processed_revision == 1


def test_retry_run_id_does_not_reauthorize_same_revision(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")
    store.save_registry_entry(entry())
    store.accept_envelope(envelope(run_id="RUN-1", task_revision=1))

    with pytest.raises(WorkerRuntimeError, match="stale or already processed"):
        store.accept_envelope(envelope(run_id="RUN-2", task_revision=1))


def test_newer_revision_updates_receiver_state(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")
    store.save_registry_entry(entry())
    store.accept_envelope(envelope(run_id="RUN-1", task_revision=1))

    accepted = store.accept_envelope(envelope(run_id="RUN-2", task_revision=2))

    assert accepted.last_processed_revision == 2
    assert accepted.last_run_id == "RUN-2"


def test_envelope_requires_registered_worker(tmp_path: Path) -> None:
    store = WorkerRuntimeStore(tmp_path / "command-center.sqlite3")

    with pytest.raises(WorkerRuntimeError, match="existing Worker registry entry"):
        store.accept_envelope(envelope())
