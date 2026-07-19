"""Preserve full backend context and the last physical stage for automation runs."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
import traceback
from pathlib import Path

from . import command_center

_STAGE_PREFIX = "LIFEOS_STAGE="
_BACKEND_PREFIX = "LIFEOS_BACKEND="
_STAGE_LABELS = {
    "foreground_request": "requesting the ChatGPT Classic foreground window",
    "foreground_verified": "verifying ChatGPT Classic as the foreground window",
    "composer_activation_start": "activating the destination composer",
    "composer_activation_verified": "verifying the destination composer focus",
    "keyboard_select_all_start": "selecting composer text",
    "keyboard_copy_start": "copying composer text for verification",
    "keyboard_paste_start": "pasting the prompt into the composer",
    "keyboard_right_start": "clearing the verification selection",
    "keyboard_other_start": "sending a guarded keyboard command",
}
_VERIFICATION_STAGES = {
    "keyboard_select_all_start",
    "keyboard_copy_start",
    "keyboard_right_start",
}


def _process_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _stages(stdout: str, stderr: str) -> list[str]:
    stages: list[str] = []
    for line in f"{stdout}\n{stderr}".splitlines():
        stripped = line.strip()
        if stripped.startswith(_STAGE_PREFIX):
            value = stripped.removeprefix(_STAGE_PREFIX).strip()
            if value:
                stages.append(value)
    return stages


def _last_stage(stdout: str, stderr: str) -> str | None:
    stages = _stages(stdout, stderr)
    return stages[-1] if stages else None


def _backend_event(event: str, **details: object) -> str:
    payload = {"event": event, "timestamp": round(time.time(), 3), **details}
    return _BACKEND_PREFIX + json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _prompt_placeholder(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"<redacted prompt length={len(value)} sha256={digest}>"


def _safe_command(command: list[str]) -> list[str]:
    """Retain executable and switches while never logging custom prompt contents."""
    safe: list[str] = []
    redact_next = False
    for value in command:
        if redact_next:
            safe.append(_prompt_placeholder(value))
            redact_next = False
            continue
        safe.append(value)
        if value == "--text":
            redact_next = True
    return safe


def _with_trace(trace: list[str], child_stdout: str, final_event: str) -> str:
    sections = [*trace]
    if child_stdout:
        sections.append(child_stdout.rstrip("\n"))
    sections.append(final_event)
    return "\n".join(sections) + "\n"


def _timeout_reason(
    stdout: str,
    stderr: str,
    *,
    timeout_seconds: int,
) -> str:
    stages = _stages(stdout, stderr)
    stage = stages[-1] if stages else None
    reached_paste = "keyboard_paste_start" in stages
    reached_verification = reached_paste and any(
        item in _VERIFICATION_STAGES
        for item in stages[stages.index("keyboard_paste_start") + 1 :]
    )
    captured = f"Captured {len(stdout)} stdout characters and {len(stderr)} stderr characters."

    if reached_verification:
        label = _STAGE_LABELS.get(stage or "", (stage or "unknown stage").replace("_", " "))
        return (
            f"The automation reached post-paste verification but exceeded {timeout_seconds}s while "
            f"{label}. The draft may be present; nothing was sent. {captured} "
            "Open Automation Logs for the complete backend trace before retrying."
        )
    if stage:
        label = _STAGE_LABELS.get(stage, stage.replace("_", " "))
        return (
            f"The automation exceeded {timeout_seconds}s while {label}. Nothing was sent. "
            f"{captured} Open Automation Logs for the complete backend trace before retrying."
        )
    return (
        f"The automation exceeded {timeout_seconds}s before reporting a physical-input stage. "
        f"Nothing was sent. {captured} Open Automation Logs to inspect command launch and child output."
    )


def _unexpected_failure(
    job: command_center.CommandJob,
    started_at: float,
    trace: list[str],
    *,
    event: str,
    exc: Exception,
) -> command_center.ExecutionResult:
    stderr = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    trace.append(
        _backend_event(
            event,
            exception_type=type(exc).__name__,
            exception_message=str(exc),
            stderr_characters=len(stderr),
        )
    )
    return command_center.ExecutionResult(
        "failed",
        job.destination,
        job.mode,
        job.prompt_type,
        None,
        started_at,
        time.time(),
        "\n".join(trace) + "\n",
        stderr,
        "The automation backend raised an unexpected exception. Nothing was sent. "
        "Open Automation Logs for the complete traceback before retrying.",
    )


def run_job(
    job: command_center.CommandJob,
    app_root: Path,
    timeout_seconds: int = 120,
) -> command_center.ExecutionResult:
    """Run one job while retaining safe command metadata and complete child output."""
    started_at = time.time()
    trace = [
        _backend_event(
            "job_received",
            destination=job.destination,
            mode=job.mode,
            prompt_type=job.prompt_type,
            timeout_seconds=timeout_seconds,
        )
    ]
    try:
        command = command_center.build_command(job, app_root)
    except command_center.CommandCenterError as exc:
        trace.append(_backend_event("job_refused", reason=str(exc)))
        return command_center.ExecutionResult(
            "refused",
            job.destination,
            job.mode,
            job.prompt_type,
            None,
            started_at,
            time.time(),
            "\n".join(trace) + "\n",
            "",
            str(exc),
        )
    except Exception as exc:
        return _unexpected_failure(
            job,
            started_at,
            trace,
            event="command_build_exception",
            exc=exc,
        )

    trace.append(
        _backend_event(
            "command_built",
            command=_safe_command(command),
            cwd=str(app_root),
        )
    )
    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"
    trace.append(_backend_event("subprocess_launch", unbuffered=True))

    try:
        completed = subprocess.run(
            command,
            cwd=app_root,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        child_stdout = _process_text(exc.stdout)
        stderr = _process_text(exc.stderr)
        elapsed = round(max(0.0, time.time() - started_at), 3)
        final_event = _backend_event(
            "subprocess_timeout",
            elapsed_seconds=elapsed,
            last_stage=_last_stage(child_stdout, stderr),
            stdout_characters=len(child_stdout),
            stderr_characters=len(stderr),
        )
        stdout = _with_trace(trace, child_stdout, final_event)
        return command_center.ExecutionResult(
            "failed",
            job.destination,
            job.mode,
            job.prompt_type,
            None,
            started_at,
            time.time(),
            stdout,
            stderr,
            _timeout_reason(stdout, stderr, timeout_seconds=timeout_seconds),
        )
    except Exception as exc:
        return _unexpected_failure(
            job,
            started_at,
            trace,
            event="subprocess_exception",
            exc=exc,
        )

    child_stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    elapsed = round(max(0.0, time.time() - started_at), 3)
    final_event = _backend_event(
        "subprocess_complete",
        elapsed_seconds=elapsed,
        exit_code=completed.returncode,
        last_stage=_last_stage(child_stdout, stderr),
        stdout_characters=len(child_stdout),
        stderr_characters=len(stderr),
    )
    stdout = _with_trace(trace, child_stdout, final_event)
    succeeded = completed.returncode == 0
    reason = (
        "Completed successfully."
        if succeeded
        else command_center.explain_failure(stdout, stderr, completed.returncode)
    )
    return command_center.ExecutionResult(
        "succeeded" if succeeded else "failed",
        job.destination,
        job.mode,
        job.prompt_type,
        completed.returncode,
        started_at,
        time.time(),
        stdout,
        stderr,
        reason,
    )


command_center.run_job = run_job
