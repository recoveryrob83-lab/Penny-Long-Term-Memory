"""Expose read-only Worker activation prerequisite reports through Worker Operations status."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from . import worker_operations
from .worker_activation_readiness import WorkerActivationReadinessService
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_activation_readiness_runtime_installed"
_GUARD_FLAG = "_lifeos_worker_activation_readiness_guards_installed"
_SERVICE_FLAG = "_lifeos_worker_activation_readiness_service_installed"


class _ClosingReadOnlyConnection(sqlite3.Connection):
    """Close the read-only SQLite handle when its context exits."""

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            return bool(super().__exit__(exc_type, exc_value, traceback))
        finally:
            self.close()


def _install_read_only_guards() -> None:
    service_class = WorkerActivationReadinessService
    if getattr(service_class, _GUARD_FLAG, False):
        return

    original_runtime_rows = service_class._runtime_rows

    def _connect_read_only(self) -> sqlite3.Connection:
        if not self.database_path.is_file():
            raise WorkerRuntimeError("Command Center database does not exist.")
        uri = self.database_path.as_uri() + "?mode=ro"
        try:
            connection = sqlite3.connect(
                uri,
                uri=True,
                factory=_ClosingReadOnlyConnection,
            )
        except sqlite3.Error as exc:
            raise WorkerRuntimeError(
                "Command Center database could not be opened read-only."
            ) from exc
        connection.row_factory = sqlite3.Row
        return connection

    def _runtime_rows(self, worker_id: str):
        try:
            with self._connect_read_only() as connection:
                if not self._table_exists(connection, "execution_history"):
                    return (
                        None,
                        None,
                        None,
                        [],
                        [
                            self._finding(
                                "runtime.tables",
                                "HOLD",
                                "Required runtime table is missing: execution_history",
                                "SQLite Command Center runtime state",
                            )
                        ],
                    )
        except WorkerRuntimeError as exc:
            return (
                None,
                None,
                None,
                [],
                [
                    self._finding(
                        "runtime.database",
                        "HOLD",
                        str(exc),
                        "SQLite Command Center runtime state",
                    )
                ],
            )
        return original_runtime_rows(self, worker_id)

    service_class._connect_read_only = _connect_read_only
    service_class._runtime_rows = _runtime_rows
    setattr(service_class, _GUARD_FLAG, True)


def _install_worker_operations_readiness() -> None:
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _SERVICE_FLAG, False):
        return

    original_init = service_class.__init__
    original_worker_rows = service_class._worker_rows
    original_status = service_class.status

    def __init__(self, *args, **kwargs) -> None:
        original_init(self, *args, **kwargs)
        database_path = Path(self.command_center.store.database_path)
        self.activation_readiness = WorkerActivationReadinessService(
            self.repository_root,
            database_path,
        )

    def activation_report(self, worker_id: str) -> dict[str, object]:
        return self.activation_readiness.report(worker_id).to_dict()

    def _worker_rows(self) -> list[dict[str, object]]:
        rows = original_worker_rows(self)
        for row in rows:
            worker_id = str(row.get("worker_id") or "")
            row["activation"] = activation_report(self, worker_id)
        return rows

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        workers = payload.get("workers")
        worker_rows = workers if isinstance(workers, list) else []
        readiness_rows = [
            row.get("activation")
            for row in worker_rows
            if isinstance(row, dict) and isinstance(row.get("activation"), dict)
        ]
        payload["activation_summary"] = {
            "report_version": 1,
            "registered": len(readiness_rows),
            "ready_for_authority_review": sum(
                report.get("state") == "READY_FOR_AUTHORITY_REVIEW"
                for report in readiness_rows
            ),
            "held": sum(report.get("state") == "HOLD" for report in readiness_rows),
            "activation_authorized": False,
        }
        return payload

    service_class.__init__ = __init__
    service_class.activation_report = activation_report
    service_class._worker_rows = _worker_rows
    service_class.status = status
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_activation_readiness_runtime() -> bool:
    """Install the status-only activation prerequisite report once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    _install_read_only_guards()
    _install_worker_operations_readiness()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_activation_readiness_runtime()


__all__ = ["install_worker_activation_readiness_runtime"]
