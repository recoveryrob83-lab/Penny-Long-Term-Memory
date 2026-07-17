"""Safe manual execution boundary for the LifeOS Automation Command Center.

Phase 1 intentionally supports manual Run Now jobs only. This module validates an exact
LifeOS destination, prompt source, and send authorization before constructing or executing a
single existing desktop-automation command. Scheduling and background recurrence do not live
here.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

DestinationKey = Literal[
    "hub",
    "main",
    "engineering",
    "logistics",
    "business",
    "office-leaks",
    "finance",
    "wellness",
]
PromptType = Literal["canonical", "custom"]
ExecutionMode = Literal["draft", "send"]


@dataclass(frozen=True)
class Destination:
    key: DestinationKey
    label: str
    chat_title: str


DESTINATIONS: dict[str, Destination] = {
    "hub": Destination("hub", "LifeOS HQ", "LifeOS HQ"),
    "main": Destination("main", "Main Assistant HQ", "Main Assistant HQ"),
    "engineering": Destination("engineering", "Engineering HQ", "Engineering HQ"),
    "logistics": Destination("logistics", "Logistics HQ", "Logistics HQ"),
    "business": Destination("business", "Business HQ", "Business HQ"),
    "office-leaks": Destination("office-leaks", "Office Leaks HQ", "Office Leaks HQ"),
    "finance": Destination("finance", "Finance HQ", "Finance HQ"),
    "wellness": Destination("wellness", "Wellness HQ", "Wellness HQ"),
}


@dataclass(frozen=True)
class CommandJob:
    destination: str
    prompt_type: PromptType
    mode: ExecutionMode = "draft"
    custom_prompt: str = ""
    confirm_send: bool = False


@dataclass(frozen=True)
class ExecutionResult:
    status: Literal["succeeded", "failed", "refused"]
    destination: str
    mode: ExecutionMode
    prompt_type: PromptType
    exit_code: int | None
    started_at: float
    finished_at: float
    stdout: str
    stderr: str
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class CommandCenterError(ValueError):
    """Raised when a requested job violates the Phase 1 contract."""


def validate_job(job: CommandJob) -> Destination:
    destination = DESTINATIONS.get(job.destination)
    if destination is None:
        raise CommandCenterError("Unknown destination. Exact LifeOS destination required.")

    if job.prompt_type not in {"canonical", "custom"}:
        raise CommandCenterError("Prompt type must be canonical or custom.")

    if job.mode not in {"draft", "send"}:
        raise CommandCenterError("Execution mode must be draft or send.")

    if job.prompt_type == "custom" and not job.custom_prompt.strip():
        raise CommandCenterError("Custom prompt cannot be empty.")

    if job.mode == "send" and not job.confirm_send:
        raise CommandCenterError("Send mode requires explicit confirmation.")

    return destination


def summarize_job(job: CommandJob) -> str:
    destination = validate_job(job)
    prompt_label = "canonical boot prompt" if job.prompt_type == "canonical" else "custom prompt"
    action = "send" if job.mode == "send" else "place as a verified draft"
    return f"{action.capitalize()} the {prompt_label} in {destination.label}."


def build_command(job: CommandJob, app_root: Path) -> list[str]:
    destination = validate_job(job)
    automation_root = app_root / "automation"

    if job.prompt_type == "canonical":
        command = [
            sys.executable,
            str(automation_root / "draft_department_boot.py"),
            destination.key,
        ]
    else:
        command = [
            sys.executable,
            str(automation_root / "open_department_chat_group_verified.py"),
            destination.chat_title,
            "--text",
            job.custom_prompt,
        ]

    if job.mode == "send":
        command.extend(["--send", "--confirm-send", "SEND"])

    return command


def run_job(job: CommandJob, app_root: Path, timeout_seconds: int = 120) -> ExecutionResult:
    """Execute one validated foreground job and return a structured result."""
    started_at = time.time()
    try:
        command = build_command(job, app_root)
    except CommandCenterError as exc:
        finished_at = time.time()
        return ExecutionResult(
            status="refused",
            destination=job.destination,
            mode=job.mode,
            prompt_type=job.prompt_type,
            exit_code=None,
            started_at=started_at,
            finished_at=finished_at,
            stdout="",
            stderr="",
            reason=str(exc),
        )

    environment = os.environ.copy()
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
        finished_at = time.time()
        return ExecutionResult(
            status="failed",
            destination=job.destination,
            mode=job.mode,
            prompt_type=job.prompt_type,
            exit_code=None,
            started_at=started_at,
            finished_at=finished_at,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            reason=f"Automation timed out after {timeout_seconds} seconds.",
        )

    finished_at = time.time()
    succeeded = completed.returncode == 0
    return ExecutionResult(
        status="succeeded" if succeeded else "failed",
        destination=job.destination,
        mode=job.mode,
        prompt_type=job.prompt_type,
        exit_code=completed.returncode,
        started_at=started_at,
        finished_at=finished_at,
        stdout=completed.stdout,
        stderr=completed.stderr,
        reason="Completed successfully." if succeeded else "Automation process returned an error.",
    )


class CommandCenterService:
    """Own the Phase 1 pause switch, one-job lock, and bounded in-memory activity history."""

    def __init__(self, app_root: Path, history_limit: int = 25) -> None:
        self.app_root = app_root
        self._paused = False
        self._state_lock = threading.Lock()
        self._run_lock = threading.Lock()
        self._history: deque[ExecutionResult] = deque(maxlen=history_limit)

    @property
    def paused(self) -> bool:
        with self._state_lock:
            return self._paused

    @property
    def running(self) -> bool:
        acquired = self._run_lock.acquire(blocking=False)
        if acquired:
            self._run_lock.release()
            return False
        return True

    def set_paused(self, paused: bool) -> bool:
        with self._state_lock:
            self._paused = paused
            return self._paused

    def history(self) -> list[dict[str, object]]:
        with self._state_lock:
            return [result.to_dict() for result in reversed(self._history)]

    def status(self) -> dict[str, object]:
        return {
            "paused": self.paused,
            "running": self.running,
            "destinations": [asdict(destination) for destination in DESTINATIONS.values()],
            "history": self.history(),
        }

    def execute(self, job: CommandJob, timeout_seconds: int = 120) -> ExecutionResult:
        started_at = time.time()
        if self.paused:
            return ExecutionResult(
                status="refused",
                destination=job.destination,
                mode=job.mode,
                prompt_type=job.prompt_type,
                exit_code=None,
                started_at=started_at,
                finished_at=time.time(),
                stdout="",
                stderr="",
                reason="Automation Command Center is globally paused.",
            )

        if not self._run_lock.acquire(blocking=False):
            return ExecutionResult(
                status="refused",
                destination=job.destination,
                mode=job.mode,
                prompt_type=job.prompt_type,
                exit_code=None,
                started_at=started_at,
                finished_at=time.time(),
                stdout="",
                stderr="",
                reason="Another automation job is already running.",
            )

        try:
            result = run_job(job, self.app_root, timeout_seconds=timeout_seconds)
            with self._state_lock:
                self._history.append(result)
            return result
        finally:
            self._run_lock.release()
