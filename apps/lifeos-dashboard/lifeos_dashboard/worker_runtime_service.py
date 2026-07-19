"""Service boundary for LifeOS Worker registration and execution readiness."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import cast

from .worker_runtime import (
    DeploymentState,
    ExecutionEnvelope,
    RouteAvailability,
    WorkerRegistryEntry,
    WorkerRouteState,
    WorkerRuntimeError,
    resolve_worker_by_title,
    validate_execution_ready,
)
from .worker_runtime_store import WorkerRuntimeStore


class WorkerRuntimeService:
    """Coordinate registry configuration, route state, and receiver acceptance."""

    def __init__(self, database_path: Path) -> None:
        self.store = WorkerRuntimeStore(database_path)

    def register_worker(self, entry: WorkerRegistryEntry) -> WorkerRegistryEntry:
        """Persist one already-authorized Worker registry entry."""

        return self.store.save_registry_entry(entry)

    def workers(self) -> list[WorkerRegistryEntry]:
        return self.store.list_registry()

    def worker(self, worker_id: str, *, require_enabled: bool = False) -> WorkerRegistryEntry:
        entry = self.store.registry_entry(worker_id)
        if entry is None:
            raise WorkerRuntimeError(f"Worker {worker_id!r} is not registered.")
        if require_enabled and entry.deployment_state != "enabled":
            raise WorkerRuntimeError(
                f"Worker {worker_id!r} is {entry.deployment_state}, not enabled."
            )
        return entry

    def resolve_title(self, chat_title: str) -> WorkerRegistryEntry:
        return resolve_worker_by_title(self.workers(), chat_title)

    def set_deployment_state(
        self, worker_id: str, deployment_state: DeploymentState
    ) -> WorkerRegistryEntry:
        entry = self.worker(worker_id)
        updated = replace(entry, deployment_state=deployment_state)
        return self.store.save_registry_entry(updated)

    def set_route_state(
        self,
        worker_id: str,
        availability: RouteAvailability,
        *,
        last_seen_at: float | None = None,
        pause_reason: str | None = None,
    ) -> WorkerRouteState:
        self.worker(worker_id)
        state = WorkerRouteState(
            worker_id=worker_id,
            availability=availability,
            last_seen_at=last_seen_at,
            pause_reason=pause_reason,
        )
        return self.store.save_route_state(state)

    def validate_envelope(self, envelope: ExecutionEnvelope) -> WorkerRegistryEntry:
        """Validate one envelope without mutating receiver revision state."""

        entry = self.worker(envelope.worker_id, require_enabled=True)
        route_state = self.store.route_state(envelope.worker_id)
        if route_state is None:
            route_state = WorkerRouteState(envelope.worker_id, "unknown")
        receiver_state = self.store.receiver_state(
            envelope.worker_id, envelope.task_id
        )
        validate_execution_ready(envelope, entry, route_state, receiver_state)
        return entry

    def accept_envelope(self, envelope: ExecutionEnvelope) -> WorkerRegistryEntry:
        """Validate and atomically accept one newer execution-ready revision."""

        entry = self.validate_envelope(envelope)
        self.store.accept_envelope(envelope)
        return entry

    def set_deployment_state_from_text(
        self, worker_id: str, deployment_state: str
    ) -> WorkerRegistryEntry:
        """Validate untyped API input before changing deployment state."""

        if deployment_state not in {"enabled", "paused", "retired"}:
            raise WorkerRuntimeError(
                "deployment_state must be enabled, paused, or retired."
            )
        return self.set_deployment_state(
            worker_id, cast(DeploymentState, deployment_state)
        )
