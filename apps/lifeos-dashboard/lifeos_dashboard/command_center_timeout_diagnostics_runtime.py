"""Preserve the last physical automation stage when a subprocess times out."""
from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

from . import command_center

_STAGE_PREFIX = "LIFEOS_STAGE="
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


def _process_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _last_stage(stdout: str, stderr: str) -> str | None:
    for line in reversed(f"{stderr}\n{stdout}".splitlines()):
        stripped = line.strip()
        if stripped.startswith(_STAGE_PREFIX):
            return stripped.removeprefix(_STAGE_PREFIX).strip() or None
    return None


def _timeout_reason(stdout: str, stderr: str) -> str:
    stage = _last_stage(stdout, stderr)
    if stage:
        label = _STAGE_LABELS.get(stage, stage.replace("_", " "))
        return (
            f"The automation timed out while {label}. "
            "Nothing was sent. Review the latest stage detail before retrying."
        )
    return (
        "The automation timed out before it reported a physical-input stage. "
        "Nothing was sent. Make sure ChatGPT Classic is responsive and no modal window is blocking it."
    )


def run_job(
    job: command_center.CommandJob,
    app_root: Path,
    timeout_seconds: int = 120,
) -> command_center.ExecutionResult:
    """Run one job while retaining direct stage traces on timeout."""
    started_at = time.time()
    try:
        command = command_center.build_command(job, app_root)
    except command_center.CommandCenterError as exc:
        return command_center.ExecutionResult(
            "refused",
            job.destination,
            job.mode,
            job.prompt_type,
            None,
            started_at,
            time.time(),
            "",
            "",
            str(exc),
        )

    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"
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
        stdout = _process_text(exc.stdout)
        stderr = _process_text(exc.stderr)
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
            _timeout_reason(stdout, stderr),
        )

    succeeded = completed.returncode == 0
    reason = (
        "Completed successfully."
        if succeeded
        else command_center.explain_failure(
            completed.stdout,
            completed.stderr,
            completed.returncode,
        )
    )
    return command_center.ExecutionResult(
        "succeeded" if succeeded else "failed",
        job.destination,
        job.mode,
        job.prompt_type,
        completed.returncode,
        started_at,
        time.time(),
        completed.stdout,
        completed.stderr,
        reason,
    )


command_center.run_job = run_job
