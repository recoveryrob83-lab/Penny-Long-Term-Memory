"""Install Package E Slice 2 dispatch-only Worker transport.

The browser courier submits one correlated Worker wake, proves the user turn exists,
returns to the source HQ, and releases the shared gate without waiting for Worker output.
Dispatch evidence is stored on the existing execution_history row.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from . import worker_operations
from .worker_runtime import WorkerRuntimeError

_DISPATCH_RECEIPT_PREFIX = "LIFEOS_BROWSER_DISPATCH_RECEIPT="
_INSTALL_FLAG = "_lifeos_worker_dispatch_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_dispatch_service_installed"


@dataclass(frozen=True)
class BrowserDispatchEvidence:
    """Submission evidence attached to the authoritative execution row."""

    dispatch_state: str
    user_turn_id: str
    dispatch_receipt_json: str
    returned_to_source: bool


def parse_browser_dispatch_receipt(stdout: str) -> dict[str, object]:
    """Return the unique machine-readable dispatch receipt."""

    lines = [
        line.removeprefix(_DISPATCH_RECEIPT_PREFIX)
        for line in (stdout or "").splitlines()
        if line.startswith(_DISPATCH_RECEIPT_PREFIX)
    ]
    if len(lines) != 1:
        raise WorkerRuntimeError(
            "Browser dispatch did not emit exactly one machine-readable receipt."
        )
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError("Browser dispatch receipt is not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise WorkerRuntimeError("Browser dispatch receipt has the wrong shape.")
    return payload


def run_worker_browser_dispatch(
    job: worker_operations.WorkerCommandJob,
    entry: worker_operations.WorkerRegistryEntry,
    app_root: Path,
    *,
    trigger: worker_operations.ExecutionTrigger,
    timeout_seconds: int = 600,
) -> tuple[worker_operations.WorkerExecutionResult, BrowserDispatchEvidence]:
    """Submit one Worker wake and return without waiting for its response."""

    started_at = time.time()
    empty_evidence = BrowserDispatchEvidence(
        dispatch_state="DISPATCH_PENDING",
        user_turn_id="",
        dispatch_receipt_json="",
        returned_to_source=False,
    )
    if job.mode != "send" or not job.confirm_send:
        return (
            worker_operations._base_result(
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

    worker_url = str(entry.conversation_url or "").strip()
    if not worker_url:
        return (
            worker_operations._base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="refused",
                exit_code=None,
                started_at=started_at,
                stdout="",
                stderr="",
                reason=(
                    "Worker browser dispatch requires a registered exact conversation URL. "
                    "Nothing was sent."
                ),
            ),
            empty_evidence,
        )

    command = [
        sys.executable,
        str(app_root / "automation" / "chatgpt_worker_browser_dispatch.py"),
        "--worker-url",
        worker_url,
        "--worker-chat-title",
        entry.chat_title,
        "--project-title",
        os.getenv("LIFEOS_CHATGPT_PROJECT_TITLE", "LifeOS"),
        "--text",
        worker_operations.render_worker_prompt(job.envelope, job.instruction),
        "--request-marker",
        job.envelope.wrapper_id,
        "--response-marker",
        job.envelope.run_id,
        "--cdp-endpoint",
        os.getenv(
            "LIFEOS_CHATGPT_CDP_ENDPOINT", worker_operations.DEFAULT_CDP_ENDPOINT
        ),
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
            worker_operations._base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="failed",
                exit_code=None,
                started_at=started_at,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                reason=(
                    "Browser courier timed out before submission could be proven. "
                    "Inspect the Worker chat and do not retry blindly."
                ),
            ),
            empty_evidence,
        )

    if completed.returncode != 0:
        uncertain = completed.returncode == 3 or "STOPPED_AFTER_SEND:" in completed.stderr
        return (
            worker_operations._base_result(
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
                    else "Browser courier stopped safely before a confirmed dispatch completed."
                ),
            ),
            empty_evidence,
        )

    try:
        receipt = parse_browser_dispatch_receipt(completed.stdout)
        if str(receipt.get("request_marker") or "") != job.envelope.wrapper_id:
            raise WorkerRuntimeError("Browser dispatch wrapper marker does not match the job.")
        if str(receipt.get("run_id") or "") != job.envelope.run_id:
            raise WorkerRuntimeError("Browser dispatch run ID does not match the job.")
        if receipt.get("status") != "submitted" or receipt.get("submission_confirmed") is not True:
            raise WorkerRuntimeError("Browser dispatch did not prove a submitted user turn.")
        user_turn_id = str(receipt.get("user_turn_id") or "").strip()
        if not user_turn_id:
            raise WorkerRuntimeError("Browser dispatch receipt has no correlated user turn ID.")
    except WorkerRuntimeError as exc:
        return (
            worker_operations._base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="failed",
                exit_code=completed.returncode,
                started_at=started_at,
                stdout=completed.stdout,
                stderr=completed.stderr,
                reason=(
                    f"{exc} Submission may have occurred; inspect the Worker chat and "
                    "do not retry blindly."
                ),
            ),
            empty_evidence,
        )

    returned_to_source = bool(receipt.get("returned_to_source"))
    reason = (
        "Worker wake submitted and correlated. Courier returned to HQ and released the gate; "
        "Worker result remains pending."
        if returned_to_source
        else (
            "Worker wake submitted and correlated, so duplicate dispatch is blocked. "
            "The courier could not verify return to HQ; inspect the browser before another wake."
        )
    )
    evidence = BrowserDispatchEvidence(
        dispatch_state="DISPATCH_SUBMITTED",
        user_turn_id=user_turn_id,
        dispatch_receipt_json=json.dumps(receipt, sort_keys=True, ensure_ascii=False),
        returned_to_source=returned_to_source,
    )
    return (
        worker_operations._base_result(
            job,
            entry.chat_title,
            trigger=trigger,
            status="succeeded",
            exit_code=completed.returncode,
            started_at=started_at,
            stdout="",
            stderr=completed.stderr,
            reason=reason,
        ),
        evidence,
    )


def _install_uncertain_send_suppression() -> None:
    history_class = worker_operations.WorkerExecutionHistoryStore

    def successful_send_exists(self, idempotency_key: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT 1 FROM execution_history
                WHERE idempotency_key = ? AND mode = 'send'
                  AND (
                    status = 'succeeded'
                    OR stderr LIKE '%STOPPED_AFTER_SEND:%'
                    OR reason LIKE '%do not retry blindly%'
                  )
                LIMIT 1
                """,
                (idempotency_key,),
            ).fetchone()
        return row is not None

    history_class.successful_send_exists = successful_send_exists


def _install_evidence_store() -> None:
    store_class = worker_operations.BrowserWorkerEvidenceStore
    store_class._COLUMNS = {
        **store_class._COLUMNS,
        "dispatch_state": "TEXT",
        "user_turn_id": "TEXT",
        "dispatch_receipt_json": "TEXT",
        "returned_to_source": "INTEGER",
        "dispatched_at": "REAL",
    }
    original_attach = store_class.attach

    def attach(self, run_id: str, evidence: object) -> None:
        if not isinstance(evidence, BrowserDispatchEvidence):
            original_attach(self, run_id, evidence)
            return
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
                    "Dispatch evidence requires exactly one authoritative Worker send row."
                )
            connection.execute(
                """
                UPDATE execution_history SET
                    dispatch_state = ?, user_turn_id = ?, dispatch_receipt_json = ?,
                    returned_to_source = ?, dispatched_at = ?
                WHERE id = ?
                """,
                (
                    evidence.dispatch_state,
                    evidence.user_turn_id,
                    evidence.dispatch_receipt_json,
                    int(evidence.returned_to_source),
                    time.time(),
                    int(rows[0]["id"]),
                ),
            )

    def history(self, limit: int = 50) -> list[dict[str, object]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM execution_history
                WHERE worker_id IS NOT NULL
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    store_class.attach = attach
    store_class.history = history


def _install_service_payload() -> None:
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _SERVICE_FLAG, False):
        return
    original_run_advisory = service_class.run_advisory

    def run_advisory(
        self: worker_operations.WorkerOperationsService,
        advisory_id: str,
        *,
        confirm_send: bool,
        timeout_seconds: int = 600,
    ) -> dict[str, object]:
        payload = original_run_advisory(
            self,
            advisory_id,
            confirm_send=confirm_send,
            timeout_seconds=timeout_seconds,
        )
        result = payload.get("result")
        run_id = str(payload.get("run_id") or "")
        if not isinstance(result, dict) or result.get("status") != "succeeded" or not run_id:
            return payload
        row = next(
            (
                item
                for item in self.worker_center.browser_evidence.history(limit=100)
                if str(item.get("run_id") or "") == run_id
            ),
            None,
        )
        if row is None:
            raise WorkerRuntimeError("Confirmed dispatch row was not readable after persistence.")
        dispatch = {
            "state": row.get("dispatch_state"),
            "user_turn_id": row.get("user_turn_id"),
            "returned_to_source": bool(row.get("returned_to_source")),
            "result_state": "RESULT_PENDING",
        }
        payload["dispatch"] = dispatch
        result["dispatch_state"] = dispatch["state"]
        result["user_turn_id"] = dispatch["user_turn_id"]
        result["returned_to_source"] = dispatch["returned_to_source"]
        result["result_state"] = dispatch["result_state"]
        payload["status"] = self.status()
        return payload

    service_class.run_advisory = run_advisory
    setattr(service_class, _SERVICE_FLAG, True)


def install_worker_dispatch_runtime() -> bool:
    """Install dispatch-only transport once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    worker_operations.run_worker_browser_transport = run_worker_browser_dispatch
    _install_uncertain_send_suppression()
    _install_evidence_store()
    _install_service_payload()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_dispatch_runtime()


__all__ = [
    "BrowserDispatchEvidence",
    "install_worker_dispatch_runtime",
    "parse_browser_dispatch_receipt",
    "run_worker_browser_dispatch",
]
