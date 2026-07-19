"""Separate Command Center execution path for authorized LifeOS Worker envelopes."""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .command_center import CommandCenterService, explain_failure
from .command_center_store import CommandCenterStore
from .worker_runtime import ExecutionEnvelope, WorkerRegistryEntry, WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService

ExecutionMode = Literal["draft", "send"]
ExecutionTrigger = Literal["manual", "scheduled"]
WorkerResultStatus = Literal["succeeded", "failed", "refused"]


@dataclass(frozen=True)
class WorkerCommandJob:
    """One execution-ready Worker assignment plus its bounded instruction."""

    envelope: ExecutionEnvelope
    instruction: str
    mode: ExecutionMode = "draft"
    confirm_send: bool = False

    def __post_init__(self) -> None:
        if not self.instruction.strip():
            raise WorkerRuntimeError("Worker instruction cannot be empty.")
        if self.mode not in {"draft", "send"}:
            raise WorkerRuntimeError("Worker execution mode must be draft or send.")
        if self.mode == "send" and not self.confirm_send:
            raise WorkerRuntimeError("Worker send mode requires explicit confirmation.")


@dataclass(frozen=True)
class WorkerExecutionResult:
    """Transport result with durable Worker-envelope evidence."""

    status: WorkerResultStatus
    destination: str
    mode: ExecutionMode
    exit_code: int | None
    started_at: float
    finished_at: float
    stdout: str
    stderr: str
    reason: str
    trigger: ExecutionTrigger
    wrapper_id: str
    run_id: str
    worker_id: str
    task_id: str
    task_revision: int
    procedure_id: str
    procedure_version: int
    authorization_source: str
    idempotency_key: str
    verification_mode: str
    controlled_outcome: str | None = None

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["prompt_type"] = "worker"
        return values


def render_worker_prompt(envelope: ExecutionEnvelope, instruction: str) -> str:
    """Render a compact wrapper line followed by the bounded execution instruction."""

    clean_instruction = instruction.strip()
    if not clean_instruction:
        raise WorkerRuntimeError("Worker instruction cannot be empty.")
    wrapper = json.dumps(envelope.to_dict(), sort_keys=True, separators=(",", ":"))
    return f"LIFEOS_EXECUTION_WRAPPER={wrapper}\n\n{clean_instruction}"


def build_worker_command(
    job: WorkerCommandJob,
    entry: WorkerRegistryEntry,
    app_root: Path,
) -> list[str]:
    """Build the exact-title Worker transport command without changing HQ jobs."""

    command = [
        sys.executable,
        str(app_root / "automation" / "open_worker_chat_group_verified.py"),
        entry.chat_title,
        "--text",
        render_worker_prompt(job.envelope, job.instruction),
        "--verify-marker",
        job.envelope.wrapper_id,
    ]
    if job.mode == "send":
        command.extend(["--send", "--confirm-send", "SEND"])
    return command


class WorkerExecutionHistoryStore:
    """Extend the existing execution-history table with nullable Worker evidence."""

    _METADATA_COLUMNS = {
        "trigger": "TEXT",
        "wrapper_id": "TEXT",
        "run_id": "TEXT",
        "worker_id": "TEXT",
        "task_id": "TEXT",
        "task_revision": "INTEGER",
        "procedure_id": "TEXT",
        "procedure_version": "INTEGER",
        "authorization_source": "TEXT",
        "idempotency_key": "TEXT",
        "verification_mode": "TEXT",
        "controlled_outcome": "TEXT",
    }

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        CommandCenterStore(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            existing = {
                str(row["name"])
                for row in connection.execute("PRAGMA table_info(execution_history)").fetchall()
            }
            for column_name, column_type in self._METADATA_COLUMNS.items():
                if column_name not in existing:
                    connection.execute(
                        f"ALTER TABLE execution_history ADD COLUMN {column_name} {column_type}"
                    )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_execution_history_worker_idempotency
                ON execution_history(idempotency_key, status, mode)
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_execution_history_worker_run
                ON execution_history(run_id)
                """
            )

    def record(self, result: WorkerExecutionResult) -> None:
        values = result.to_dict()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO execution_history(
                    status, destination, mode, prompt_type, exit_code,
                    started_at, finished_at, stdout, stderr, reason,
                    trigger, wrapper_id, run_id, worker_id, task_id,
                    task_revision, procedure_id, procedure_version,
                    authorization_source, idempotency_key, verification_mode,
                    controlled_outcome
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    values["status"],
                    values["destination"],
                    values["mode"],
                    values["prompt_type"],
                    values["exit_code"],
                    values["started_at"],
                    values["finished_at"],
                    values["stdout"],
                    values["stderr"],
                    values["reason"],
                    values["trigger"],
                    values["wrapper_id"],
                    values["run_id"],
                    values["worker_id"],
                    values["task_id"],
                    values["task_revision"],
                    values["procedure_id"],
                    values["procedure_version"],
                    values["authorization_source"],
                    values["idempotency_key"],
                    values["verification_mode"],
                    values["controlled_outcome"],
                ),
            )

    def successful_send_exists(self, idempotency_key: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT 1 FROM execution_history
                WHERE idempotency_key = ? AND status = 'succeeded' AND mode = 'send'
                LIMIT 1
                """,
                (idempotency_key,),
            ).fetchone()
        return row is not None

    def worker_history(self, limit: int = 25) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, status, destination, mode, prompt_type, exit_code,
                       started_at, finished_at, stdout, stderr, reason,
                       trigger, wrapper_id, run_id, worker_id, task_id,
                       task_revision, procedure_id, procedure_version,
                       authorization_source, idempotency_key, verification_mode,
                       controlled_outcome
                FROM execution_history
                WHERE worker_id IS NOT NULL
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]


def run_worker_job(
    job: WorkerCommandJob,
    entry: WorkerRegistryEntry,
    app_root: Path,
    *,
    trigger: ExecutionTrigger,
    timeout_seconds: int = 120,
) -> WorkerExecutionResult:
    """Run one already-validated Worker transport attempt."""

    started_at = time.time()
    command = build_worker_command(job, entry, app_root)
    try:
        completed = subprocess.run(
            command,
            cwd=app_root,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return _result(
            job,
            destination=entry.chat_title,
            trigger=trigger,
            status="failed",
            exit_code=None,
            started_at=started_at,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            reason=(
                "Worker transport timed out. Confirm ChatGPT Classic is responsive and do not "
                "retry blindly if submission state is uncertain."
            ),
        )
    succeeded = completed.returncode == 0
    reason = (
        "Worker transport completed successfully."
        if succeeded
        else explain_failure(completed.stdout, completed.stderr, completed.returncode)
    )
    return _result(
        job,
        destination=entry.chat_title,
        trigger=trigger,
        status="succeeded" if succeeded else "failed",
        exit_code=completed.returncode,
        started_at=started_at,
        stdout=completed.stdout,
        stderr=completed.stderr,
        reason=reason,
    )


def _result(
    job: WorkerCommandJob,
    *,
    destination: str,
    trigger: ExecutionTrigger,
    status: WorkerResultStatus,
    exit_code: int | None,
    started_at: float,
    stdout: str,
    stderr: str,
    reason: str,
) -> WorkerExecutionResult:
    envelope = job.envelope
    return WorkerExecutionResult(
        status=status,
        destination=destination,
        mode=job.mode,
        exit_code=exit_code,
        started_at=started_at,
        finished_at=time.time(),
        stdout=stdout,
        stderr=stderr,
        reason=reason,
        trigger=trigger,
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


class WorkerCommandCenterService:
    """Share the Command Center pause and one-job lock while keeping Worker routing separate."""

    def __init__(self, command_center: CommandCenterService) -> None:
        self.command_center = command_center
        database_path = Path(command_center.store.database_path)
        self.runtime = WorkerRuntimeService(database_path)
        self.history = WorkerExecutionHistoryStore(database_path)

    @property
    def _run_lock(self) -> threading.Lock:
        return self.command_center._run_lock  # noqa: SLF001 - intentional shared execution gate

    def execute(
        self,
        job: WorkerCommandJob,
        *,
        trigger: ExecutionTrigger = "manual",
        timeout_seconds: int = 120,
    ) -> WorkerExecutionResult:
        if trigger not in {"manual", "scheduled"}:
            raise WorkerRuntimeError("Worker execution trigger must be manual or scheduled.")
        started_at = time.time()
        if self.command_center.paused:
            return self._record_refusal(
                job,
                trigger=trigger,
                started_at=started_at,
                reason="Automation is paused. Resume it before running a Worker job.",
            )
        if not self._run_lock.acquire(blocking=False):
            return self._record_refusal(
                job,
                trigger=trigger,
                started_at=started_at,
                reason="Another automation job is running. Let it finish before starting a Worker job.",
            )
        try:
            try:
                entry = self.runtime.validate_envelope(job.envelope)
            except WorkerRuntimeError as exc:
                return self._record_refusal(
                    job,
                    trigger=trigger,
                    started_at=started_at,
                    reason=str(exc),
                )
            if job.mode == "send" and self.history.successful_send_exists(
                job.envelope.idempotency_key
            ):
                return self._record_refusal(
                    job,
                    trigger=trigger,
                    started_at=started_at,
                    reason="This Worker task revision already has a successful send record.",
                    destination=entry.chat_title,
                )
            result = run_worker_job(
                job,
                entry,
                self.command_center.app_root,
                trigger=trigger,
                timeout_seconds=timeout_seconds,
            )
            self.history.record(result)
            return result
        finally:
            self._run_lock.release()

    def execute_scheduled(
        self, job: WorkerCommandJob, *, timeout_seconds: int = 120
    ) -> WorkerExecutionResult:
        """Scheduler adapter for one already-authorized execution-ready envelope."""

        return self.execute(job, trigger="scheduled", timeout_seconds=timeout_seconds)

    def _record_refusal(
        self,
        job: WorkerCommandJob,
        *,
        trigger: ExecutionTrigger,
        started_at: float,
        reason: str,
        destination: str | None = None,
    ) -> WorkerExecutionResult:
        result = _result(
            job,
            destination=destination or job.envelope.worker_id,
            trigger=trigger,
            status="refused",
            exit_code=None,
            started_at=started_at,
            stdout="",
            stderr="",
            reason=reason,
        )
        self.history.record(result)
        return result
