"""Browser-backed Worker operations surface for the LifeOS dashboard.

The service coordinates already-authorized canonical Worker advisories with the existing
Command Center lock, Worker registry, one-row execution history, browser round-trip transport,
and HQ verification view. It does not create advisory authority or change advisory lifecycle.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

from .command_center import CommandCenterService
from .worker_advisory_pipeline import AdvisoryWakePipeline
from .worker_command_center import (
    ExecutionTrigger,
    WorkerCommandJob,
    WorkerExecutionHistoryStore,
    WorkerExecutionResult,
    WorkerResultStatus,
    render_worker_prompt,
)
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService
from .worker_verification import WorkerVerificationService

DEFAULT_CDP_ENDPOINT = "http://127.0.0.1:9222"
_BROWSER_RECEIPT_PREFIX = "LIFEOS_BROWSER_ROUNDTRIP_RECEIPT="
_SYNTHETIC_RECEIPT_PREFIX = "LIFEOS_SYNTHETIC_BROWSER_RECEIPT="
_ALLOWED_REPORTED_OUTCOMES = (
    "IMPLEMENT",
    "REPORT_AND_HOLD",
    "ELEVATE_FOR_APPROVAL",
)
_OUTCOME_PATTERN = re.compile(
    r"(?:CONTROLLED_OUTCOME|Controlled Outcome|Final controlled outcome)\s*[:\-]\s*"
    r"(IMPLEMENT|REPORT_AND_HOLD|ELEVATE_FOR_APPROVAL)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class BrowserTransportEvidence:
    """Transport observations stored on the existing execution-history row."""

    reported_outcome: str | None = None
    assistant_turn_id: str | None = None
    browser_receipt_json: str | None = None


def parse_reported_outcome(response_text: str) -> str | None:
    """Extract one Worker-reported outcome without treating it as receiver acceptance."""

    matches = {match.upper() for match in _OUTCOME_PATTERN.findall(response_text or "")}
    if len(matches) == 1:
        return matches.pop()
    if len(matches) > 1:
        return None
    upper = (response_text or "").upper()
    terminal = [item for item in _ALLOWED_REPORTED_OUTCOMES if upper.rstrip().endswith(item)]
    return terminal[0] if len(terminal) == 1 else None


def parse_browser_receipt(stdout: str) -> dict[str, object]:
    """Return the unique browser receipt emitted by the transport subprocess."""

    lines = [
        line.removeprefix(_BROWSER_RECEIPT_PREFIX)
        for line in (stdout or "").splitlines()
        if line.startswith(_BROWSER_RECEIPT_PREFIX)
    ]
    if len(lines) != 1:
        raise WorkerRuntimeError(
            "Browser transport did not emit exactly one machine-readable round-trip receipt."
        )
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError("Browser round-trip receipt is not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise WorkerRuntimeError("Browser round-trip receipt has the wrong shape.")
    return payload


def parse_synthetic_receipt(stdout: str) -> dict[str, object]:
    """Return the unique zero-authority courier self-test receipt."""

    lines = [
        line.removeprefix(_SYNTHETIC_RECEIPT_PREFIX)
        for line in (stdout or "").splitlines()
        if line.startswith(_SYNTHETIC_RECEIPT_PREFIX)
    ]
    if len(lines) != 1:
        raise WorkerRuntimeError(
            "Courier self-test did not emit exactly one machine-readable receipt."
        )
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError("Courier self-test receipt is not valid JSON.") from exc
    if not isinstance(payload, dict) or payload.get("durable_authority_created") is not False:
        raise WorkerRuntimeError("Courier self-test receipt did not preserve zero authority.")
    return payload


def browser_health(cdp_endpoint: str = DEFAULT_CDP_ENDPOINT) -> dict[str, object]:
    """Probe the local loopback CDP endpoint without opening or controlling a page."""

    version_url = cdp_endpoint.rstrip("/") + "/json/version"
    try:
        with urllib.request.urlopen(version_url, timeout=1.5) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        return {
            "available": False,
            "endpoint": cdp_endpoint,
            "browser": None,
            "reason": str(exc),
        }
    websocket = str(payload.get("webSocketDebuggerUrl") or "")
    browser = str(payload.get("Browser") or "")
    reason = (
        "Loopback CDP endpoint is ready."
        if websocket and browser
        else "CDP metadata is incomplete."
    )
    return {
        "available": bool(websocket and browser),
        "endpoint": cdp_endpoint,
        "browser": browser or None,
        "reason": reason,
    }


def _base_result(
    job: WorkerCommandJob,
    destination: str,
    *,
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


def run_worker_browser_transport(
    job: WorkerCommandJob,
    entry: WorkerRegistryEntry,
    app_root: Path,
    *,
    trigger: ExecutionTrigger,
    timeout_seconds: int = 600,
) -> tuple[WorkerExecutionResult, BrowserTransportEvidence]:
    """Run one validated Worker send through the one-tab browser courier."""

    started_at = time.time()
    empty_evidence = BrowserTransportEvidence()
    if job.mode != "send" or not job.confirm_send:
        return (
            _base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="refused",
                exit_code=None,
                started_at=started_at,
                stdout="",
                stderr="",
                reason="Browser Worker transport accepts confirmed send jobs only.",
            ),
            empty_evidence,
        )
    command = [
        sys.executable,
        str(app_root / "automation" / "chatgpt_worker_browser_roundtrip.py"),
        "--worker-chat-title",
        entry.chat_title,
        "--project-title",
        os.getenv("LIFEOS_CHATGPT_PROJECT_TITLE", "LifeOS"),
        "--text",
        render_worker_prompt(job.envelope, job.instruction),
        "--request-marker",
        job.envelope.wrapper_id,
        "--response-marker",
        job.envelope.run_id,
        "--cdp-endpoint",
        os.getenv("LIFEOS_CHATGPT_CDP_ENDPOINT", DEFAULT_CDP_ENDPOINT),
        "--timeout-seconds",
        str(timeout_seconds),
        "--send",
        "--confirm-send",
        "SEND",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=app_root,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
            timeout=timeout_seconds + 30,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return (
            _base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="failed",
                exit_code=None,
                started_at=started_at,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                reason=(
                    "Browser courier timed out. Submission state may be uncertain; inspect the "
                    "Worker chat before any retry."
                ),
            ),
            empty_evidence,
        )

    if completed.returncode != 0:
        uncertain = completed.returncode == 3 or "STOPPED_AFTER_SEND:" in completed.stderr
        return (
            _base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="failed",
                exit_code=completed.returncode,
                started_at=started_at,
                stdout=completed.stdout,
                stderr=completed.stderr,
                reason=(
                    "Browser courier stopped after submission uncertainty. Inspect the Worker chat "
                    "and do not retry blindly."
                    if uncertain
                    else "Browser courier stopped safely before a verified round trip completed."
                ),
            ),
            empty_evidence,
        )

    try:
        receipt = parse_browser_receipt(completed.stdout)
        response_text = str(receipt.get("response_text") or "").strip()
        if str(receipt.get("request_marker") or "") != job.envelope.wrapper_id:
            raise WorkerRuntimeError("Browser receipt wrapper marker does not match the job.")
        if job.envelope.run_id not in str(receipt.get("response_marker") or ""):
            raise WorkerRuntimeError("Browser receipt response marker does not match the run.")
        if not bool(receipt.get("returned_to_source")):
            raise WorkerRuntimeError("Browser courier did not verify return to the source chat.")
    except WorkerRuntimeError as exc:
        return (
            _base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="failed",
                exit_code=completed.returncode,
                started_at=started_at,
                stdout=completed.stdout,
                stderr=completed.stderr,
                reason=str(exc),
            ),
            empty_evidence,
        )

    reported_outcome = parse_reported_outcome(response_text)
    reason = (
        "Worker response captured and correlated. Receiver validation and HQ review remain pending."
        if reported_outcome
        else (
            "Worker response captured, but no unique controlled outcome marker was found. "
            "Hold for inspection."
        )
    )
    evidence = BrowserTransportEvidence(
        reported_outcome=reported_outcome,
        assistant_turn_id=(
            str(receipt["assistant_turn_id"])
            if receipt.get("assistant_turn_id") is not None
            else None
        ),
        browser_receipt_json=json.dumps(receipt, sort_keys=True, ensure_ascii=False),
    )
    return (
        _base_result(
            job,
            entry.chat_title,
            trigger=trigger,
            status="succeeded",
            exit_code=completed.returncode,
            started_at=started_at,
            stdout=response_text,
            stderr=completed.stderr,
            reason=reason,
        ),
        evidence,
    )


class BrowserWorkerEvidenceStore:
    """Attach browser evidence to the existing execution-history row, never a second ledger."""

    _COLUMNS = {
        "worker_reported_outcome": "TEXT",
        "assistant_turn_id": "TEXT",
        "browser_receipt_json": "TEXT",
    }

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        WorkerExecutionHistoryStore(database_path)
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
            for column_name, column_type in self._COLUMNS.items():
                if column_name not in existing:
                    connection.execute(
                        f"ALTER TABLE execution_history ADD COLUMN {column_name} {column_type}"
                    )

    def attach(self, run_id: str, evidence: BrowserTransportEvidence) -> None:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id FROM execution_history
                WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
                ORDER BY id DESC
                """,
                (run_id,),
            ).fetchall()
            if len(rows) != 1:
                raise WorkerRuntimeError(
                    "Browser evidence requires exactly one authoritative Worker send row."
                )
            connection.execute(
                """
                UPDATE execution_history SET
                    worker_reported_outcome = ?, assistant_turn_id = ?, browser_receipt_json = ?
                WHERE id = ?
                """,
                (
                    evidence.reported_outcome,
                    evidence.assistant_turn_id,
                    evidence.browser_receipt_json,
                    int(rows[0]["id"]),
                ),
            )

    def history(self, limit: int = 50) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, status, destination, mode, prompt_type, exit_code,
                       started_at, finished_at, stdout, stderr, reason,
                       trigger, wrapper_id, run_id, worker_id, task_id,
                       task_revision, procedure_id, procedure_version,
                       authorization_source, idempotency_key, verification_mode,
                       controlled_outcome, worker_reported_outcome,
                       assistant_turn_id, browser_receipt_json,
                       receiver_verification_state, receiver_completion_state,
                       worker_verification_state
                FROM execution_history
                WHERE worker_id IS NOT NULL
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]


class BrowserWorkerCommandCenter:
    """Use existing pause, lock, registry, and history with browser transport."""

    def __init__(self, command_center: CommandCenterService) -> None:
        self.command_center = command_center
        database_path = Path(command_center.store.database_path)
        self.runtime = WorkerRuntimeService(database_path)
        self.history = WorkerExecutionHistoryStore(database_path)
        self.browser_evidence = BrowserWorkerEvidenceStore(database_path)

    @property
    def _run_lock(self) -> threading.Lock:
        return self.command_center._run_lock  # noqa: SLF001 - shared one-job execution gate

    def _refusal(
        self,
        job: WorkerCommandJob,
        *,
        trigger: ExecutionTrigger,
        started_at: float,
        reason: str,
        destination: str | None = None,
    ) -> WorkerExecutionResult:
        result = _base_result(
            job,
            destination or job.envelope.worker_id,
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

    def execute(
        self,
        job: WorkerCommandJob,
        *,
        trigger: ExecutionTrigger = "manual",
        timeout_seconds: int = 600,
    ) -> WorkerExecutionResult:
        if trigger not in {"manual", "scheduled"}:
            raise WorkerRuntimeError("Worker execution trigger must be manual or scheduled.")
        started_at = time.time()
        if self.command_center.paused:
            return self._refusal(
                job,
                trigger=trigger,
                started_at=started_at,
                reason="Automation is paused. Resume it before running a Worker job.",
            )
        if not self._run_lock.acquire(blocking=False):
            return self._refusal(
                job,
                trigger=trigger,
                started_at=started_at,
                reason=(
                    "Another automation job is running. "
                    "Let it finish before starting a Worker job."
                ),
            )
        try:
            try:
                entry = self.runtime.validate_envelope(job.envelope)
            except WorkerRuntimeError as exc:
                return self._refusal(
                    job,
                    trigger=trigger,
                    started_at=started_at,
                    reason=str(exc),
                )
            if job.mode == "send" and self.history.successful_send_exists(
                job.envelope.idempotency_key
            ):
                return self._refusal(
                    job,
                    trigger=trigger,
                    started_at=started_at,
                    reason="This Worker task revision already has a successful send record.",
                    destination=entry.chat_title,
                )
            result, evidence = run_worker_browser_transport(
                job,
                entry,
                self.command_center.app_root,
                trigger=trigger,
                timeout_seconds=timeout_seconds,
            )
            self.history.record(result)
            if result.status == "succeeded":
                self.browser_evidence.attach(result.run_id, evidence)
            return result
        finally:
            self._run_lock.release()


class WorkerOperationsService:
    """Dashboard-facing orchestration for canonical Worker advisories and HQ review."""

    def __init__(
        self,
        command_center: CommandCenterService,
        repository_root: Path,
        *,
        cdp_endpoint: str | None = None,
    ) -> None:
        self.command_center = command_center
        self.repository_root = repository_root.resolve()
        self.cdp_endpoint = cdp_endpoint or os.getenv(
            "LIFEOS_CHATGPT_CDP_ENDPOINT",
            DEFAULT_CDP_ENDPOINT,
        )
        self.worker_center = BrowserWorkerCommandCenter(command_center)
        self.pipeline = AdvisoryWakePipeline(self.repository_root, self.worker_center)
        self.verification = WorkerVerificationService(Path(command_center.store.database_path))

    def _worker_rows(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for entry in self.worker_center.runtime.workers():
            route = self.worker_center.runtime.store.route_state(entry.worker_id)
            values = entry.to_dict()
            values["route"] = asdict(route) if route is not None else {
                "worker_id": entry.worker_id,
                "availability": "unknown",
                "last_seen_at": None,
                "pause_reason": None,
            }
            rows.append(values)
        return rows

    def _advisory_rows(self) -> tuple[list[dict[str, object]], str | None]:
        try:
            advisories = self.pipeline.discover()
        except (OSError, WorkerRuntimeError) as exc:
            return [], str(exc)
        return [
            {
                "advisory_id": item.advisory_id,
                "title": item.title,
                "board_path": item.board_path,
                "target_department": item.target_department,
                "worker_id": item.target_worker_id,
                "revision": item.advisory_revision,
                "task_class": item.task_class,
                "authorization_class": item.authorization_class,
                "procedure_id": item.procedure_id,
                "procedure_version": item.procedure_version,
                "verification_mode": item.verification_mode,
                "priority": item.priority,
                "wrapper_id": item.wrapper_id,
                "run_id": item.run_id,
            }
            for item in advisories
        ], None

    def status(self) -> dict[str, object]:
        advisories, advisory_error = self._advisory_rows()
        legacy_status = self.command_center.status()
        return {
            "paused": self.command_center.paused,
            "running": self.command_center.running,
            "browser": browser_health(self.cdp_endpoint),
            "workers": self._worker_rows(),
            "advisories": advisories,
            "advisory_error": advisory_error,
            "history": self.worker_center.browser_evidence.history(limit=50),
            "verification": self.verification.status(limit=100),
            "legacy": {
                "scheduler_running": bool(legacy_status.get("scheduler_running")),
                "scheduled_jobs": len(legacy_status.get("scheduled_jobs") or []),
                "saved_prompts": len(legacy_status.get("saved_prompts") or []),
                "visible_ui": False,
            },
        }

    def run_advisory(
        self,
        advisory_id: str,
        *,
        confirm_send: bool,
        timeout_seconds: int = 600,
    ) -> dict[str, object]:
        clean_id = str(advisory_id or "").strip()
        if not clean_id:
            raise WorkerRuntimeError("advisory_id cannot be empty.")
        if not confirm_send:
            raise WorkerRuntimeError("Live Worker dispatch requires explicit send confirmation.")
        if timeout_seconds < 60 or timeout_seconds > 900:
            raise WorkerRuntimeError("timeout_seconds must be between 60 and 900.")
        dispatch = self.pipeline.dispatch(
            clean_id,
            mode="send",
            confirm_send=True,
            trigger="manual",
            timeout_seconds=timeout_seconds,
        )
        return {
            "advisory_id": dispatch.advisory.advisory_id,
            "revision": dispatch.advisory.advisory_revision,
            "worker_id": dispatch.advisory.target_worker_id,
            "wrapper_id": dispatch.job.envelope.wrapper_id,
            "run_id": dispatch.job.envelope.run_id,
            "result": dispatch.result.to_dict(),
            "status": self.status(),
        }

    def courier_self_test(
        self,
        *,
        confirm_send: bool,
        timeout_seconds: int = 300,
    ) -> dict[str, object]:
        """Run one explicit zero-authority browser test without creating a run row."""

        if not confirm_send:
            raise WorkerRuntimeError("Courier self-test requires explicit send confirmation.")
        if timeout_seconds < 60 or timeout_seconds > 900:
            raise WorkerRuntimeError("timeout_seconds must be between 60 and 900.")
        if self.command_center.paused:
            raise WorkerRuntimeError("Automation is paused. Resume it before running a self-test.")
        run_lock = self.command_center._run_lock  # noqa: SLF001 - shared execution gate
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError("Another automation job is already running.")
        try:
            command = [
                sys.executable,
                str(
                    self.command_center.app_root
                    / "automation"
                    / "run_synthetic_worker_browser_pilot.py"
                ),
                "--send",
                "--confirm-send",
                "SYNTHETIC_SEND",
                "--timeout-seconds",
                str(timeout_seconds),
                "--cdp-endpoint",
                self.cdp_endpoint,
            ]
            try:
                completed = subprocess.run(
                    command,
                    cwd=self.command_center.app_root,
                    env=os.environ.copy(),
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds + 30,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise WorkerRuntimeError(
                    "Courier self-test timed out. Inspect the Worker chat before retrying."
                ) from exc
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise WorkerRuntimeError(
                    detail or "Courier self-test stopped before a verified round trip completed."
                )
            receipt = parse_synthetic_receipt(completed.stdout)
        finally:
            run_lock.release()
        return {
            "status": "succeeded",
            "receipt": receipt,
            "operations": self.status(),
        }

    def review(
        self,
        run_id: str,
        state: str,
        *,
        actor: str,
        reason: str,
    ) -> dict[str, object]:
        record = self.verification.review(
            run_id,
            state,
            actor=actor,
            reason=reason,
        )
        return {"record": record.to_dict(), "status": self.status()}


__all__ = [
    "BrowserTransportEvidence",
    "BrowserWorkerCommandCenter",
    "WorkerOperationsService",
    "browser_health",
    "parse_browser_receipt",
    "parse_synthetic_receipt",
    "parse_reported_outcome",
    "run_worker_browser_transport",
]
