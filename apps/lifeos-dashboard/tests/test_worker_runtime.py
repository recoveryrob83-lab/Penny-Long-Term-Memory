import pytest

from lifeos_dashboard.worker_runtime import (
    ExecutionEnvelope,
    WorkerReceiverState,
    WorkerRegistryEntry,
    WorkerRouteState,
    WorkerRuntimeError,
    copied_text_contains_wrapper,
    resolve_worker_by_title,
    validate_execution_ready,
)


def registry_entry(**overrides: object) -> WorkerRegistryEntry:
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
        "wrapper_id": "WRAP-20260719-001",
        "run_id": "RUN-20260719-001",
        "worker_id": "office_leaks_worker",
        "task_id": "ADV-20260719-044",
        "task_revision": 1,
        "procedure_id": "maintenance_reconcile",
        "procedure_version": 1,
        "authorization_source": "Rob via Engineering HQ",
        "verification_mode": "IMMEDIATE_HQ",
    }
    values.update(overrides)
    return ExecutionEnvelope.from_dict(values)


def test_registry_entry_separates_profile_authority_from_deployment_state() -> None:
    entry = registry_entry(deployment_state="paused")

    assert entry.profile_path.endswith("/workers/general.md")
    assert entry.deployment_state == "paused"
    assert "status" not in entry.to_dict()


def test_registry_entry_rejects_legacy_top_level_profile_path() -> None:
    with pytest.raises(WorkerRuntimeError, match="projects/<department>/workers"):
        registry_entry(profile_path="workers/office-leaks/WORKER_BOOT.md")


def test_exact_title_resolution_returns_one_enabled_worker() -> None:
    entry = registry_entry()

    assert resolve_worker_by_title([entry], "OfficeLeaks_Worker") == entry


def test_exact_title_resolution_fails_on_zero_matches() -> None:
    with pytest.raises(WorkerRuntimeError, match="No Worker matches"):
        resolve_worker_by_title([registry_entry()], "OfficeLeaksWorker")


def test_exact_title_resolution_fails_on_duplicate_matches() -> None:
    entries = [registry_entry(), registry_entry(worker_id="office_leaks_worker_two")]

    with pytest.raises(WorkerRuntimeError, match="Multiple Workers match"):
        resolve_worker_by_title(entries, "OfficeLeaks_Worker")


def test_exact_title_resolution_rejects_paused_worker() -> None:
    with pytest.raises(WorkerRuntimeError, match="paused, not enabled"):
        resolve_worker_by_title(
            [registry_entry(deployment_state="paused")], "OfficeLeaks_Worker"
        )


def test_envelope_idempotency_key_ignores_run_retry_identity() -> None:
    first = envelope(run_id="RUN-1")
    retry = envelope(run_id="RUN-2")

    assert first.idempotency_key == retry.idempotency_key
    assert first.idempotency_key == "office_leaks_worker:ADV-20260719-044:1"


def test_receiver_state_is_scoped_to_worker_and_task() -> None:
    state = WorkerReceiverState(
        worker_id="office_leaks_worker",
        task_id="ADV-20260719-044",
        last_processed_revision=1,
    )

    with pytest.raises(WorkerRuntimeError, match="stale or already processed"):
        validate_execution_ready(
            envelope(task_revision=1),
            registry_entry(),
            WorkerRouteState("office_leaks_worker", "available"),
            state,
        )


def test_different_task_revision_is_not_compared_to_unrelated_receiver_state() -> None:
    state = WorkerReceiverState(
        worker_id="office_leaks_worker",
        task_id="ADV-OTHER",
        last_processed_revision=99,
    )

    with pytest.raises(WorkerRuntimeError, match="does not belong to the envelope task"):
        validate_execution_ready(
            envelope(),
            registry_entry(),
            WorkerRouteState("office_leaks_worker", "available"),
            state,
        )


def test_unavailable_route_holds_before_execution() -> None:
    with pytest.raises(WorkerRuntimeError, match="execution must hold"):
        validate_execution_ready(
            envelope(),
            registry_entry(),
            WorkerRouteState("office_leaks_worker", "unavailable"),
        )


def test_wrapper_marker_is_the_minimal_composer_witness() -> None:
    copied = "Execute bounded work. wrapper_id=WRAP-20260719-001"

    assert copied_text_contains_wrapper(copied, "WRAP-20260719-001") is True
    assert copied_text_contains_wrapper(copied, "WRAP-OTHER") is False
    assert copied_text_contains_wrapper(copied, "") is False
