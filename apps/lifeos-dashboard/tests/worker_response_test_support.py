"""Fixtures for Package E Worker response receiver tests."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from lifeos_dashboard.worker_advisory_pipeline import ExecutionReadyAdvisory
from lifeos_dashboard.worker_command_center import (
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
)
from lifeos_dashboard.worker_operations import (
    BrowserTransportEvidence,
    BrowserWorkerEvidenceStore,
)
from lifeos_dashboard.worker_receiver import checksum_parameters, sha256_text
from lifeos_dashboard.worker_response_receiver import (
    WORKER_REPORT_PREFIX,
    WorkerResponseReceiver,
)
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService

PROFILE = """---
worker_id: engineering_worker
chat_title: Engineering_Worker
owning_department: engineering
role: worker
specialization: general
profile_version: 1
receiver_allowed_task_classes_json: ["engineering_read_only_verification"]
receiver_read_scope_prefixes_json: ["projects/engineering","apps/lifeos-dashboard","memory","coordination"]
receiver_write_scope_prefixes_json: ["projects/engineering","apps/lifeos-dashboard"]
receiver_approved_tools_json: ["GitHub"]
receiver_calling_source_task_classes_json: {"ROB-TEST":["engineering_read_only_verification"]}
receiver_allowed_verification_modes_json: ["IMMEDIATE_HQ"]
receiver_prohibited_task_classes_json: []
receiver_department_labels_json: ["engineering","Engineering HQ"]
---

# Engineering Worker Profile
"""

PROCEDURE = """---
procedure_id: engineering_worker_read_only_verification
procedure_version: 1
owning_department: engineering
task_class: engineering_read_only_verification
required_verification_mode: IMMEDIATE_HQ
receiver_parameter_schema_json: {"targets":"array","verification_questions":"array"}
receiver_required_parameters_json: ["targets","verification_questions"]
receiver_allowed_authorization_classes_json: ["READ_ONLY"]
receiver_approved_tools_json: ["GitHub"]
receiver_source_references_required: true
---

# Engineering Worker Read-Only Verification Procedure
"""


def advisory(revision: int = 1) -> ExecutionReadyAdvisory:
    return ExecutionReadyAdvisory(
        advisory_id="ADV-TEST",
        title="Verify Package E receiver integration",
        board_path="coordination/boards/engineering.md",
        target_department="Engineering HQ",
        target_worker_id="engineering_worker",
        advisory_revision=revision,
        task_class="engineering_read_only_verification",
        authorization_class="READ_ONLY",
        procedure_id="engineering_worker_read_only_verification",
        procedure_version=1,
        authorization_source="ROB-TEST",
        verification_mode="IMMEDIATE_HQ",
        lifecycle_state="OPEN",
        priority="NORMAL",
    )


def board_text(revision: int = 1, *, procedure_checksum: str | None = None) -> str:
    params = {
        "targets": ["projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md"],
        "verification_questions": ["Is Slice 2 bounded and receiver-owned?"],
    }
    checksum = procedure_checksum or sha256_text(PROCEDURE)
    sources = [
        "coordination/boards/engineering.md",
        "projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md",
    ]
    read_scopes = ["projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md"]
    return f"""# Engineering Advisory Board

### ADV-TEST — Verify Package E receiver integration

- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: {revision}
- Verification Mode: IMMEDIATE_HQ
- Target Department and Owner: Engineering HQ
- Target Worker ID: `engineering_worker`
- Task Class: `engineering_read_only_verification`
- Authorization Class: `READ_ONLY`
- Procedure ID: `engineering_worker_read_only_verification`
- Procedure Version: 1
- Procedure Checksum: `{checksum}`
- Authorization Source: `ROB-TEST`
- Parameters JSON: `{json.dumps(params, separators=(",", ":"))}`
- Parameters Checksum: `{checksum_parameters(params)}`
- Source References JSON: `{json.dumps(sources, separators=(",", ":"))}`
- Requested Read Scopes JSON: `{json.dumps(read_scopes, separators=(",", ":"))}`
- Requested Write Scopes JSON: `[]`
- Requested Tools JSON: `["GitHub"]`
- Completion Condition: Return one evidence-backed report for Immediate HQ review.
"""


def report_payload(revision: int = 1, **overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "wrapper_id": f"WAKE-ADV-TEST-R{revision}",
        "run_id": f"RUN-ADV-TEST-R{revision}",
        "worker_id": "engineering_worker",
        "profile_version": 1,
        "owning_department": "engineering",
        "task_id": "ADV-TEST",
        "task_revision": revision,
        "procedure_id": "engineering_worker_read_only_verification",
        "procedure_version": 1,
        "authorization_source": "ROB-TEST",
        "verification_mode": "IMMEDIATE_HQ",
        "controlled_outcome": "IMPLEMENT",
        "completion_state": "completed",
        "evidence_references": ["github:blob:package-e"],
        "actual_read_scopes": [
            "projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md"
        ],
        "actual_write_scopes": [],
        "actual_tools": ["GitHub"],
        "verification_state": "pending",
        "external_actions_verified": True,
        "approval_required_discovered": False,
        "failure_reason": None,
    }
    values.update(overrides)
    return values


def response_text(revision: int = 1, **overrides: object) -> str:
    return (
        f"Run ID: RUN-ADV-TEST-R{revision}\nBounded verification report.\n"
        + WORKER_REPORT_PREFIX
        + json.dumps(report_payload(revision, **overrides), separators=(",", ":"))
    )


def transport_result(
    active: ExecutionReadyAdvisory, stdout: str
) -> WorkerExecutionResult:
    envelope = active.envelope()
    return WorkerExecutionResult(
        status="succeeded",
        destination="Engineering_Worker",
        mode="send",
        exit_code=0,
        started_at=time.time() - 1,
        finished_at=time.time(),
        stdout=stdout,
        stderr="",
        reason="Worker response captured and correlated.",
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


def write_sources(
    root: Path, revision: int = 1, *, checksum: str | None = None
) -> None:
    (root / "projects/engineering/workers").mkdir(parents=True, exist_ok=True)
    (root / "projects/engineering/procedures").mkdir(parents=True, exist_ok=True)
    (root / "coordination/boards").mkdir(parents=True, exist_ok=True)
    (root / "projects/engineering/workers/engineering_worker.md").write_text(
        PROFILE, encoding="utf-8"
    )
    procedure_path = (
        root
        / "projects/engineering/procedures/engineering_worker_read_only_verification.md"
    )
    procedure_path.write_text(PROCEDURE, encoding="utf-8")
    (root / "coordination/boards/engineering.md").write_text(
        board_text(revision, procedure_checksum=checksum), encoding="utf-8"
    )


def setup_run(
    tmp_path: Path,
    *,
    revision: int = 1,
    stdout: str | None = None,
    checksum: str | None = None,
) -> tuple[WorkerResponseReceiver, ExecutionReadyAdvisory, WorkerRegistryEntry, Path]:
    write_sources(tmp_path, revision, checksum=checksum)
    database = tmp_path / "command-center.sqlite3"
    runtime = WorkerRuntimeService(database)
    entry = WorkerRegistryEntry(
        worker_id="engineering_worker",
        chat_title="Engineering_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/engineering_worker.md",
        profile_version=1,
    )
    runtime.register_worker(entry)
    runtime.set_route_state("engineering_worker", "available")
    active = advisory(revision)
    response = stdout if stdout is not None else response_text(revision)
    WorkerExecutionHistoryStore(database).record(transport_result(active, response))
    BrowserWorkerEvidenceStore(database).attach(
        active.run_id,
        BrowserTransportEvidence(
            reported_outcome=("IMPLEMENT" if "IMPLEMENT" in response else None),
            assistant_turn_id=f"conversation-turn-{revision}",
            browser_receipt_json=json.dumps({"response_text": response}),
        ),
    )
    return WorkerResponseReceiver(database, tmp_path), active, entry, database


def outcome_row(database: Path, run_id: str) -> sqlite3.Row:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM execution_history WHERE run_id = ?", (run_id,)
        ).fetchone()
    assert row is not None
    return row
