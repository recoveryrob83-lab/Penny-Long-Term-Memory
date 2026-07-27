"""Install durable stale-draft proof for correction-only Worker dispatch.

Ordinary Worker dispatch remains unchanged. This runtime replaces only the transport
function imported by ``worker_report_repair_dispatch``. The replacement requires the
original execution row to prove one submitted wrapper and correlated user turn before
it allows the browser courier to clear that exact stale draft.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

from . import worker_dispatch_runtime, worker_operations, worker_report_repair_dispatch
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_report_repair_live_recovery_installed"


def _database_path(app_root: Path) -> Path:
    configured = str(os.getenv("COMMAND_CENTER_DATABASE_PATH") or "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    return (app_root / ".local" / "command_center.sqlite3").resolve()


def _trusted_stale_markers(database_path: Path, run_id: str) -> tuple[str, str]:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT wrapper_id, dispatch_state, user_turn_id
            FROM execution_history
            WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
            ORDER BY id
            """,
            (run_id,),
        ).fetchall()
    if len(rows) != 1:
        raise WorkerRuntimeError(
            "Trusted stale-draft proof requires exactly one authoritative Worker send row."
        )
    row = rows[0]
    wrapper_id = str(row["wrapper_id"] or "").strip()
    dispatch_state = str(row["dispatch_state"] or "").strip()
    user_turn_id = str(row["user_turn_id"] or "").strip()
    if dispatch_state != "DISPATCH_SUBMITTED" or not wrapper_id or not user_turn_id:
        raise WorkerRuntimeError(
            "The original Worker dispatch lacks durable wrapper and correlated user-turn proof. "
            "No composer text may be cleared."
        )
    return wrapper_id, run_id


def _safe_stop_detail(stderr: str, stdout: str) -> str:
    detail = str(stderr or stdout or "").strip()
    for prefix in ("STOPPED: ", "STOPPED_AFTER_SEND: "):
        if detail.startswith(prefix):
            detail = detail.removeprefix(prefix).strip()
    return detail


def run_worker_report_repair_browser_dispatch(
    job: worker_operations.WorkerCommandJob,
    entry: worker_operations.WorkerRegistryEntry,
    app_root: Path,
    *,
    trigger: worker_operations.ExecutionTrigger,
    timeout_seconds: int = 600,
) -> tuple[
    worker_operations.WorkerExecutionResult,
    worker_dispatch_runtime.BrowserDispatchEvidence,
]:
    """Submit one correction-only wake using durable proof for one stale draft."""

    started_at = time.time()
    empty_evidence = worker_dispatch_runtime.BrowserDispatchEvidence(
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

    try:
        stale_wrapper_id, stale_run_id = _trusted_stale_markers(
            _database_path(app_root),
            job.envelope.run_id,
        )
    except (OSError, sqlite3.Error, WorkerRuntimeError) as exc:
        return (
            worker_operations._base_result(
                job,
                entry.chat_title,
                trigger=trigger,
                status="failed",
                exit_code=None,
                started_at=started_at,
                stdout="",
                stderr=str(exc),
                reason=f"Durable stale-draft proof was unavailable. Nothing was sent. {exc}",
            ),
            empty_evidence,
        )

    command = [
        sys.executable,
        str(app_root / "automation" / "chatgpt_worker_report_repair_dispatch.py"),
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
        "--trusted-stale-wrapper-id",
        stale_wrapper_id,
        "--trusted-stale-run-id",
        stale_run_id,
        "--cdp-endpoint",
        os.getenv(
            "LIFEOS_CHATGPT_CDP_ENDPOINT",
            worker_operations.DEFAULT_CDP_ENDPOINT,
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
        detail = _safe_stop_detail(completed.stderr, completed.stdout)
        reason = (
            "Browser courier stopped after submission uncertainty. Inspect the Worker chat and "
            "do not retry blindly."
            if uncertain
            else "Browser courier stopped safely before a confirmed dispatch completed."
        )
        if detail:
            reason = f"{reason} Detail: {detail}"
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
                reason=reason,
            ),
            empty_evidence,
        )

    try:
        receipt = worker_dispatch_runtime.parse_browser_dispatch_receipt(completed.stdout)
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
    evidence = worker_dispatch_runtime.BrowserDispatchEvidence(
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


def install_worker_report_repair_live_recovery_runtime() -> bool:
    """Install the correction-only transport override once."""

    if getattr(worker_report_repair_dispatch, _INSTALL_FLAG, False):
        return False
    worker_report_repair_dispatch.run_worker_browser_dispatch = (
        run_worker_report_repair_browser_dispatch
    )
    setattr(worker_report_repair_dispatch, _INSTALL_FLAG, True)
    return True


install_worker_report_repair_live_recovery_runtime()


__all__ = [
    "_safe_stop_detail",
    "_trusted_stale_markers",
    "install_worker_report_repair_live_recovery_runtime",
    "run_worker_report_repair_browser_dispatch",
]
