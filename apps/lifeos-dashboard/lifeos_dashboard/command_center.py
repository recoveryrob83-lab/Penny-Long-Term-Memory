"""Safe manual execution boundary for the LifeOS Automation Command Center."""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .command_center_store import CommandCenterStore

DestinationKey = Literal["hub", "main", "engineering", "logistics", "business", "office-leaks", "finance", "wellness"]
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
        command = [sys.executable, str(automation_root / "draft_department_boot.py"), destination.key]
    else:
        command = [sys.executable, str(automation_root / "open_department_chat_group_verified.py"), destination.chat_title, "--text", job.custom_prompt]
    if job.mode == "send":
        command.extend(["--send", "--confirm-send", "SEND"])
    return command


def run_job(job: CommandJob, app_root: Path, timeout_seconds: int = 120) -> ExecutionResult:
    started_at = time.time()
    try:
        command = build_command(job, app_root)
    except CommandCenterError as exc:
        return ExecutionResult("refused", job.destination, job.mode, job.prompt_type, None, started_at, time.time(), "", "", str(exc))
    try:
        completed = subprocess.run(command, cwd=app_root, env=os.environ.copy(), capture_output=True, text=True, timeout=timeout_seconds, check=False)
    except subprocess.TimeoutExpired as exc:
        return ExecutionResult("failed", job.destination, job.mode, job.prompt_type, None, started_at, time.time(), exc.stdout or "", exc.stderr or "", f"Automation timed out after {timeout_seconds} seconds.")
    succeeded = completed.returncode == 0
    return ExecutionResult("succeeded" if succeeded else "failed", job.destination, job.mode, job.prompt_type, completed.returncode, started_at, time.time(), completed.stdout, completed.stderr, "Completed successfully." if succeeded else "Automation process returned an error.")


class CommandCenterService:
    """Own pause state, one-job locking, saved prompts, and durable activity history."""

    def __init__(self, app_root: Path, database_path: Path | None = None, history_limit: int = 25) -> None:
        self.app_root = app_root
        self.history_limit = history_limit
        self.store = CommandCenterStore(database_path or app_root / ".local" / "command_center.sqlite3")
        self._paused = False
        self._state_lock = threading.Lock()
        self._run_lock = threading.Lock()

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

    def save_prompt(self, name: str, prompt: str) -> dict[str, object]:
        return self.store.save_prompt(name, prompt)

    def update_prompt(self, prompt_id: int, name: str, prompt: str) -> dict[str, object] | None:
        return self.store.update_prompt(prompt_id, name, prompt)

    def delete_prompt(self, prompt_id: int) -> bool:
        return self.store.delete_prompt(prompt_id)

    def canonical_prompt(self, destination_key: str) -> dict[str, str]:
        destination = DESTINATIONS.get(destination_key)
        if destination is None:
            raise CommandCenterError("Unknown destination. Exact LifeOS destination required.")
        completed = subprocess.run([sys.executable, str(self.app_root / "automation" / "draft_department_boot.py"), destination.key, "--print-prompt"], cwd=self.app_root, env=os.environ.copy(), capture_output=True, text=True, timeout=30, check=False)
        if completed.returncode != 0:
            raise CommandCenterError(completed.stderr.strip() or "Canonical prompt preview failed.")
        return {"name": f"{destination.label} canonical boot", "prompt": completed.stdout}

    def history(self) -> list[dict[str, object]]:
        return self.store.history(self.history_limit)

    def status(self) -> dict[str, object]:
        return {"paused": self.paused, "running": self.running, "destinations": [asdict(destination) for destination in DESTINATIONS.values()], "saved_prompts": self.store.list_prompts(), "history": self.history()}

    def _record(self, result: ExecutionResult) -> ExecutionResult:
        self.store.add_history(result.to_dict())
        return result

    def execute(self, job: CommandJob, timeout_seconds: int = 120) -> ExecutionResult:
        started_at = time.time()
        if self.paused:
            return self._record(ExecutionResult("refused", job.destination, job.mode, job.prompt_type, None, started_at, time.time(), "", "", "Automation Command Center is globally paused."))
        if not self._run_lock.acquire(blocking=False):
            return self._record(ExecutionResult("refused", job.destination, job.mode, job.prompt_type, None, started_at, time.time(), "", "", "Another automation job is already running."))
        try:
            return self._record(run_job(job, self.app_root, timeout_seconds=timeout_seconds))
        finally:
            self._run_lock.release()
