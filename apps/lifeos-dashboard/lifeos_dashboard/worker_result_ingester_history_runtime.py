"""Reconcile historical failed-after-send rows during deterministic result ingestion.

Early Package E courier runs could preserve a real Worker submission as a failed transport row when
return-to-HQ restoration failed. A later immutable, schema-valid, assignment-correlated Git report
is stronger evidence that the Worker received and completed that exact run. This compatibility layer
allows only one uniquely identified no-retry historical send row to be ingested. It does not rewrite
the original transport status or manufacture missing browser-turn evidence.
"""
from __future__ import annotations

import sqlite3

from . import worker_result_ingester
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_result_history_runtime_installed"
_LEGACY_PROTECTED_MARKERS = (
    "stopped_after_send:",
    "do not retry blindly",
    "did not verify return to the source chat",
    "could not verify return to hq",
    "courier did not return",
)


def _row_text(row: sqlite3.Row) -> str:
    return "\n".join(
        str(row[field] or "")
        for field in ("stdout", "stderr", "reason")
        if field in row.keys()
    ).casefold()


def _is_legacy_protected_send(row: sqlite3.Row) -> bool:
    if str(row["mode"] or "") != "send" or str(row["prompt_type"] or "") != "worker":
        return False
    if str(row["status"] or "") == "succeeded":
        return False
    text = _row_text(row)
    return any(marker in text for marker in _LEGACY_PROTECTED_MARKERS)


def _install_history_reconciliation() -> None:
    ingester_class = worker_result_ingester.WorkerResultIngester
    if getattr(ingester_class, _INSTALL_FLAG, False):
        return

    original_ingest = ingester_class.ingest

    @staticmethod
    def _require_history_row(
        connection: sqlite3.Connection,
        advisory: worker_result_ingester.ExecutionReadyAdvisory,
    ) -> sqlite3.Row:
        rows = connection.execute(
            """
            SELECT * FROM execution_history
            WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
            ORDER BY id
            """,
            (advisory.run_id,),
        ).fetchall()
        successful = [row for row in rows if str(row["status"] or "") == "succeeded"]
        if len(successful) == 1:
            return successful[0]
        if len(successful) > 1:
            raise WorkerRuntimeError(
                "Result ingestion found ambiguous duplicate successful Worker send rows."
            )
        protected = [row for row in rows if _is_legacy_protected_send(row)]
        if len(rows) == 1 and len(protected) == 1:
            return protected[0]
        if not rows:
            raise WorkerRuntimeError(
                "Result ingestion found no authoritative Worker send row in the selected database."
            )
        statuses = ", ".join(
            f"id={row['id']} status={row['status']!s} reason={str(row['reason'] or '')[:120]!r}"
            for row in rows
        )
        raise WorkerRuntimeError(
            "Result ingestion could not select one authoritative Worker send row. Observed: "
            + statuses
        )

    @classmethod
    def _validate_history_row(
        cls,
        row: sqlite3.Row,
        advisory: worker_result_ingester.ExecutionReadyAdvisory,
    ) -> None:
        errors: list[str] = []
        for field_name, expected in cls._expected_identity(advisory):
            del field_name, expected

    def _validate_history_row_impl(
        cls,
        row: sqlite3.Row,
        advisory: worker_result_ingester.ExecutionReadyAdvisory,
    ) -> None:
        errors: list[str] = []
        for field_name, expected in cls._expected_identity(advisory).items():
            observed = row[field_name]
            if field_name in {"task_revision", "procedure_version"}:
                matches = observed is not None and int(observed) == int(expected)
            else:
                matches = str(observed or "") == str(expected)
            if not matches:
                errors.append(f"runtime {field_name} does not match the assignment")
        if str(row["status"] or "") == "succeeded":
            if str(row["dispatch_state"] or "") != "DISPATCH_SUBMITTED":
                errors.append("runtime dispatch state is not DISPATCH_SUBMITTED")
            if not str(row["user_turn_id"] or "").strip():
                errors.append("runtime row has no correlated user turn ID")
        elif not _is_legacy_protected_send(row):
            errors.append("runtime row is neither a confirmed dispatch nor a protected historical send")
        if errors:
            raise WorkerRuntimeError("Runtime correlation failed: " + "; ".join(errors) + ".")

    def ingest(self, advisory):
        with self._connect() as connection:
            selected = _require_history_row(connection, advisory)
            legacy = _is_legacy_protected_send(selected)
            history_id = int(selected["id"])
        receipt = original_ingest(self, advisory)
        if legacy:
            with self._connect() as connection:
                connection.execute(
                    """
                    UPDATE execution_history SET receiver_reason = ?
                    WHERE id = ? AND result_state = 'REPORT_VALIDATED'
                    """,
                    (
                        "Deterministic immutable Worker report ingestion passed. Historical "
                        "failed-after-send transport evidence was reconciled by the exact "
                        "schema-valid, assignment-correlated immutable report; original transport "
                        "status remains preserved.",
                        history_id,
                    ),
                )
        return receipt

    ingester_class._require_history_row = _require_history_row
    ingester_class._validate_history_row = classmethod(_validate_history_row_impl)
    ingester_class.ingest = ingest
    setattr(ingester_class, _INSTALL_FLAG, True)


_install_history_reconciliation()


__all__ = ["_is_legacy_protected_send"]
