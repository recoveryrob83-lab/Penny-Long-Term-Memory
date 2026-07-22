"""Disposable synthetic proof for Package E report rejection and repair."""
from __future__ import annotations

import json
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_command_center import WorkerExecutionHistoryStore, WorkerExecutionResult
from .worker_dispatch_runtime import BrowserDispatchEvidence
from .worker_operations import BrowserWorkerEvidenceStore
from .worker_result_contract import build_result_submission_contract, load_artifact_examples
from .worker_result_ingester import WorkerResultIngester
from .worker_result_repair import WorkerReportRepairWake, WorkerResultRepairCoordinator
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService

RUN_ID = "SYNTH-RESULT-REPAIR-RUN-1"
REPORT_1 = (
    "projects/engineering/worker-results/engineering_worker/"
    f"{RUN_ID}/report-001.json"
)
REPORT_2 = (
    "projects/engineering/worker-results/engineering_worker/"
    f"{RUN_ID}/report-002.json"
)
TARGETS = (
    "projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md",
    "apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-report.schema.json",
)


@dataclass(frozen=True)
class SyntheticRepairCourierReceipt:
    """Synthetic evidence that a correction-only wake targeted the same Worker."""

    status: str
    worker_id: str
    run_id: str
    wrapper_id: str
    idempotency_key: str
    corrected_report_path: str
    work_reexecution_authorized: bool
    scope_expansion_authorized: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "worker_id": self.worker_id,
            "run_id": self.run_id,
            "wrapper_id": self.wrapper_id,
            "idempotency_key": self.idempotency_key,
            "corrected_report_path": self.corrected_report_path,
            "work_reexecution_authorized": self.work_reexecution_authorized,
            "scope_expansion_authorized": self.scope_expansion_authorized,
        }


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise WorkerRuntimeError(f"Synthetic Git command failed: {detail or arguments!r}")
    return completed.stdout.strip()


def _initialize_repository(root: Path) -> dict[str, str]:
    _git(root, "init")
    _git(root, "config", "user.email", "synthetic-worker@lifeos.local")
    _git(root, "config", "user.name", "LifeOS Synthetic Worker")
    for target in TARGETS:
        path = root / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"synthetic canonical source: {target}\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "Add synthetic canonical sources")
    return {target: _git(root, "rev-parse", f"HEAD:{target}") for target in TARGETS}


def _advisory() -> ExecutionReadyAdvisory:
    return ExecutionReadyAdvisory(
        advisory_id="SYNTH-RESULT-REPAIR",
        title="Synthetic immutable report repair proof",
        board_path="projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md",
        target_department="Engineering HQ",
        target_worker_id="engineering_worker",
        advisory_revision=1,
        task_class="engineering_read_only_verification",
        authorization_class="BOUNDED_WRITE",
        procedure_id="engineering_worker_result_outbox_validation",
        procedure_version=1,
        authorization_source="ENGINEERING_HQ_PACKAGE_E_SLICE4_SYNTHETIC_REPAIR",
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="OPEN",
        priority="NORMAL",
        source_references=TARGETS,
        requested_read_scopes=TARGETS,
        requested_write_scopes=(REPORT_1,),
        requested_tools=("GitHub",),
        result_contract=build_result_submission_contract(
            "engineering", "engineering_worker", RUN_ID, attempt=1
        ),
    )


def _transport_result(active: ExecutionReadyAdvisory) -> WorkerExecutionResult:
    envelope = active.envelope()
    return WorkerExecutionResult(
        status="succeeded",
        destination="Engineering_Worker",
        mode="send",
        exit_code=0,
        started_at=time.time() - 1,
        finished_at=time.time(),
        stdout="",
        stderr="",
        reason="Synthetic Worker wake submitted and correlated.",
        trigger="manual",
        wrapper_id=envelope.wrapper_id,
        run_id=envelope.run_id,
        worker_id=envelope.worker_id,
        task_id=envelope.task_id,
        task_revision=envelope.task_revision,
        procedure_id=envelope.procedure_id,
        procedure_version=envelope.procedure_version,
        authorization_source=envelope.authorization_source,
        idempotency_key=envelope.idempotency_key,
        verification_mode=envelope.verification_mode,
    )


def _report_payload(
    blob_shas: dict[str, str],
    *,
    attempt: int,
    profile_version: object,
) -> dict[str, object]:
    report_path = REPORT_1 if attempt == 1 else REPORT_2
    payload = dict(load_artifact_examples()["worker_report"])
    payload.update(
        {
            "attempt": attempt,
            "wrapper_id": "WAKE-SYNTH-RESULT-REPAIR-R1",
            "run_id": RUN_ID,
            "worker_id": "engineering_worker",
            "profile_version": profile_version,
            "owning_department": "engineering",
            "task_id": "SYNTH-RESULT-REPAIR",
            "task_revision": 1,
            "procedure_id": "engineering_worker_result_outbox_validation",
            "procedure_version": 1,
            "authorization_source": "ENGINEERING_HQ_PACKAGE_E_SLICE4_SYNTHETIC_REPAIR",
            "verification_mode": "IMMEDIATE_HQ",
            "requested_action": "Read the exact synthetic targets and create one immutable report.",
            "actual_action_attempted": (
                "Reused the completed synthetic inspection and corrected only the report artifact."
                if attempt > 1
                else "Read the exact synthetic targets and created the first report artifact."
            ),
            "controlled_outcome": "IMPLEMENT",
            "completion_state": "completed",
            "evidence_references": [
                *(f"{path}@{blob_shas[path]}" for path in TARGETS),
                f"{report_path}@preflight:not-found",
            ],
            "actual_read_scopes": [*TARGETS, report_path],
            "actual_write_scopes": [report_path],
            "actual_tools": ["GitHub"],
            "what_did_not_occur": [
                "No underlying work was re-executed.",
                "No scope expansion or advisory lifecycle change occurred.",
            ],
            "unresolved_risks": ["Synthetic Department HQ review remains pending."],
            "review_condition": "Engineering HQ must inspect the synthetic repair evidence.",
            "verification_state": "pending",
            "external_actions_verified": True,
            "approval_required_discovered": False,
            "failure_reason": None,
        }
    )
    return payload


def _commit_report(root: Path, path: str, payload: dict[str, object], message: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise WorkerRuntimeError(f"Synthetic report path already exists: {path}")
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _git(root, "add", "--", path)
    _git(root, "commit", "--only", "-m", message, "--", path)


def _table_names(database: Path) -> set[str]:
    with sqlite3.connect(database) as connection:
        return {
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }


def _synthetic_wake(wake: WorkerReportRepairWake) -> SyntheticRepairCourierReceipt:
    if wake.worker_id != "engineering_worker" or wake.run_id != RUN_ID:
        raise WorkerRuntimeError("Synthetic repair wake did not target the original Worker and run.")
    if wake.work_reexecution_authorized or wake.scope_expansion_authorized:
        raise WorkerRuntimeError("Synthetic repair wake granted prohibited authority.")
    if "Do not repeat" not in wake.instruction or REPORT_2 not in wake.instruction:
        raise WorkerRuntimeError("Synthetic repair wake lacks correction-only instructions.")
    return SyntheticRepairCourierReceipt(
        status="submitted",
        worker_id=wake.worker_id,
        run_id=wake.run_id,
        wrapper_id=wake.wrapper_id,
        idempotency_key=wake.idempotency_key,
        corrected_report_path=wake.corrected_report_path,
        work_reexecution_authorized=wake.work_reexecution_authorized,
        scope_expansion_authorized=wake.scope_expansion_authorized,
    )


def run_synthetic_repair_pilot(root: Path) -> dict[str, object]:
    """Exercise malformed rejection, correction-only wake, repair, and deduplication."""

    root.mkdir(parents=True, exist_ok=True)
    blob_shas = _initialize_repository(root)
    active = _advisory()
    malformed = _report_payload(blob_shas, attempt=1, profile_version="1")
    _commit_report(root, REPORT_1, malformed, "Add malformed synthetic Worker report")

    database = root / "command-center.sqlite3"
    runtime = WorkerRuntimeService(database)
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="engineering_worker",
            chat_title="Engineering_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/engineering_worker.md",
            profile_version=1,
        )
    )
    runtime.set_route_state("engineering_worker", "available")
    WorkerExecutionHistoryStore(database).record(_transport_result(active))
    BrowserWorkerEvidenceStore(database).attach(
        RUN_ID,
        BrowserDispatchEvidence(
            dispatch_state="DISPATCH_SUBMITTED",
            user_turn_id="conversation-turn-synthetic-repair",
            dispatch_receipt_json='{"status":"submitted"}',
            returned_to_source=True,
        ),
    )

    ingester = WorkerResultIngester(root, database, runtime=runtime)
    coordinator = WorkerResultRepairCoordinator(ingester)
    before_tables = _table_names(database)
    rejection_error = ""
    try:
        coordinator.ingest_next(active)
    except WorkerRuntimeError as exc:
        rejection_error = str(exc)
    if "correction-only repair was prepared" not in rejection_error:
        raise WorkerRuntimeError(
            "Synthetic malformed report did not produce deterministic repair preparation."
        )
    wake = coordinator.repair_wake(RUN_ID)
    if wake is None:
        raise WorkerRuntimeError("Synthetic rejection did not queue a repair wake.")
    courier = _synthetic_wake(wake)

    corrected = _report_payload(blob_shas, attempt=2, profile_version=1)
    _commit_report(root, REPORT_2, corrected, "Add corrected synthetic Worker report")
    accepted = coordinator.ingest_next(active)
    duplicate = coordinator.ingest_next(active)
    row = coordinator._row(RUN_ID)  # noqa: SLF001 - synthetic evidence inspection
    after_tables = _table_names(database)

    if accepted.report_state != "REPORT_VALIDATED" or accepted.report_attempt != 2:
        raise WorkerRuntimeError("Corrected synthetic report was not accepted as attempt two.")
    if not duplicate.duplicate_suppressed:
        raise WorkerRuntimeError("Identical corrected report was not duplicate-suppressed.")
    if str(row["repair_state"] or "") != "REPORT_REPAIR_ACCEPTED":
        raise WorkerRuntimeError("Synthetic repair state did not advance to accepted.")
    if before_tables != after_tables:
        raise WorkerRuntimeError("Synthetic repair created a competing runtime table.")
    with sqlite3.connect(database) as connection:
        row_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM execution_history WHERE run_id = ?", (RUN_ID,)
            ).fetchone()[0]
        )
    if row_count != 1:
        raise WorkerRuntimeError("Synthetic repair created a competing execution row.")

    return {
        "status": "succeeded",
        "run_id": RUN_ID,
        "malformed_attempt": 1,
        "rejection_path": str(row["rejection_path"]),
        "repair_wake": courier.to_dict(),
        "corrected_attempt": accepted.to_dict(),
        "duplicate_suppressed": duplicate.duplicate_suppressed,
        "stale_attempt_ignored": str(row["report_path"]) == REPORT_2,
        "same_execution_row": row_count == 1,
        "second_runtime_ledger_created": False,
        "repair_state": str(row["repair_state"]),
    }


__all__ = [
    "RUN_ID",
    "SyntheticRepairCourierReceipt",
    "run_synthetic_repair_pilot",
]
