"""Safe execution boundary for the LifeOS Automation Command Center."""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .command_center_schedule import ScheduleSpec, compute_next_run
from .command_center_store import CommandCenterStore

DestinationKey = Literal[
    "hub", "main", "engineering", "logistics", "business", "office-leaks", "finance", "wellness"
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
    default_destination: str | None = None
    confirm_destination: bool = False


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
    """Raised when a requested job violates the Command Center contract."""


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
    if job.default_destination is not None:
        default_destination = DESTINATIONS.get(job.default_destination)
        if default_destination is None:
            raise CommandCenterError("Saved prompt default destination is not recognized.")
        if default_destination.key != destination.key and not job.confirm_destination:
            raise CommandCenterError(
                "Destination mismatch requires explicit confirmation. "
                f"This prompt defaults to {default_destination.label}, not {destination.label}."
            )
    return destination


def summarize_job(job: CommandJob) -> str:
    destination = validate_job(job)
    prompt_label = "canonical boot prompt" if job.prompt_type == "canonical" else "custom prompt"
    action = "send" if job.mode == "send" else "place as a verified draft"
    return f"{action.capitalize()} the {prompt_label} in {destination.label}."


def explain_failure(stdout: str, stderr: str, exit_code: int | None) -> str:
    diagnostic = f"{stderr}\n{stdout}".casefold()
    if "composer" in diagnostic and any(
        word in diagnostic for word in ("occupied", "contains", "not empty", "existing")
    ):
        return "The target composer already contains text. Clear or save that draft, then run the job again."
    if "show more" in diagnostic and ("match" in diagnostic or "elements" in diagnostic):
        return "ChatGPT exposed multiple sidebar controls. Pull the latest automation patch, restart the dashboard, and retry."
    if "chatgpt classic" in diagnostic and any(
        word in diagnostic for word in ("not found", "window", "connect")
    ):
        return "ChatGPT Classic was not available. Open the desktop app, leave it signed in, and retry."
    if "exact chat" in diagnostic or "exact link" in diagnostic or (
        "destination" in diagnostic and "not found" in diagnostic
    ):
        return "The exact LifeOS chat could not be verified. Open the sidebar, confirm the chat name, and retry without renaming it."
    if "document title" in diagnostic or "title verification" in diagnostic:
        return "The destination opened, but its exact title could not be verified. Stop and confirm the selected chat before retrying."
    if "clipboard" in diagnostic or "write verification" in diagnostic:
        return "The prompt could not be verified after writing. Leave the composer untouched, focus ChatGPT Classic, and retry."
    if "timed out" in diagnostic:
        return "The automation timed out. Make sure ChatGPT Classic is responsive and no modal window is blocking it, then retry."
    return f"Automation stopped safely with exit code {exit_code}. Review the technical details below before retrying."


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
    started_at = time.time()
    try:
        command = build_command(job, app_root)
    except CommandCenterError as exc:
        return ExecutionResult(
            "refused", job.destination, job.mode, job.prompt_type, None,
            started_at, time.time(), "", "", str(exc)
        )
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
        return ExecutionResult(
            "failed",
            job.destination,
            job.mode,
            job.prompt_type,
            None,
            started_at,
            time.time(),
            exc.stdout or "",
            exc.stderr or "",
            "The automation timed out. Make sure ChatGPT Classic is responsive and no modal window is blocking it, then retry.",
        )
    succeeded = completed.returncode == 0
    reason = (
        "Completed successfully."
        if succeeded
        else explain_failure(completed.stdout, completed.stderr, completed.returncode)
    )
    return ExecutionResult(
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


class CommandCenterService:
    """Own manual runs, persistent schedules, saved prompts, and durable history."""

    def __init__(
        self,
        app_root: Path,
        database_path: Path | None = None,
        history_limit: int = 25,
        *,
        start_scheduler: bool = False,
        scheduler_poll_seconds: float = 15.0,
    ) -> None:
        self.app_root = app_root
        self.history_limit = history_limit
        self.store = CommandCenterStore(
            database_path or app_root / ".local" / "command_center.sqlite3"
        )
        self._paused = False
        self._state_lock = threading.Lock()
        self._run_lock = threading.Lock()
        self._scheduler_poll_seconds = scheduler_poll_seconds
        self._scheduler_stop = threading.Event()
        self._scheduler_thread: threading.Thread | None = None
        if start_scheduler:
            self.start_scheduler()

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

    @property
    def scheduler_running(self) -> bool:
        return bool(self._scheduler_thread and self._scheduler_thread.is_alive())

    def set_paused(self, paused: bool) -> bool:
        with self._state_lock:
            self._paused = paused
            return self._paused

    def save_prompt(
        self,
        name: str,
        prompt: str,
        default_destination: str | None = None,
        origin_type: str | None = None,
        origin_prompt_key: str | None = None,
    ) -> dict[str, object]:
        if default_destination is not None and default_destination not in DESTINATIONS:
            raise ValueError("Saved prompt default destination is not recognized.")
        return self.store.save_prompt(
            name,
            prompt,
            default_destination=default_destination,
            origin_type=origin_type,
            origin_prompt_key=origin_prompt_key,
        )

    def update_prompt(
        self,
        prompt_id: int,
        name: str,
        prompt: str,
        default_destination: str | None = None,
        origin_type: str | None = None,
        origin_prompt_key: str | None = None,
    ) -> dict[str, object] | None:
        if default_destination is not None and default_destination not in DESTINATIONS:
            raise ValueError("Saved prompt default destination is not recognized.")
        return self.store.update_prompt(
            prompt_id,
            name,
            prompt,
            default_destination=default_destination,
            origin_type=origin_type,
            origin_prompt_key=origin_prompt_key,
        )

    def delete_prompt(self, prompt_id: int) -> bool:
        return self.store.delete_prompt(prompt_id)

    def canonical_prompt(self, destination_key: str) -> dict[str, str]:
        destination = DESTINATIONS.get(destination_key)
        if destination is None:
            raise CommandCenterError("Unknown destination. Exact LifeOS destination required.")
        completed = subprocess.run(
            [
                sys.executable,
                str(self.app_root / "automation" / "draft_department_boot.py"),
                destination.key,
                "--print-prompt",
            ],
            cwd=self.app_root,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if completed.returncode != 0:
            raise CommandCenterError(completed.stderr.strip() or "Canonical prompt preview failed.")
        return {"name": f"{destination.label} canonical boot", "prompt": completed.stdout}

    def _schedule_spec(self, values: dict[str, object]) -> ScheduleSpec:
        return ScheduleSpec(
            cadence=str(values["cadence"]),
            schedule_date=str(values["schedule_date"]),
            schedule_time=str(values["schedule_time"]),
            weekdays=tuple(int(day) for day in values.get("weekdays", [])),
            timezone=str(values.get("timezone") or "America/Chicago"),
        )

    def _prepare_schedule(self, values: dict[str, object]) -> dict[str, object]:
        clean_name = str(values.get("name") or "").strip()
        if not clean_name:
            raise ValueError("Schedule name cannot be empty.")
        source_type = str(values.get("source_type") or "")
        if source_type not in {"canonical", "saved", "custom"}:
            raise ValueError("Schedule source must be canonical, saved, or custom.")
        job = CommandJob(
            destination=str(values.get("destination") or ""),
            prompt_type=str(values.get("prompt_type") or "custom"),  # type: ignore[arg-type]
            mode=str(values.get("mode") or "draft"),  # type: ignore[arg-type]
            custom_prompt=str(values.get("custom_prompt") or ""),
            confirm_send=bool(values.get("confirm_send")),
            default_destination=(
                str(values["default_destination"])
                if values.get("default_destination") is not None
                else None
            ),
            confirm_destination=bool(values.get("confirm_destination")),
        )
        validate_job(job)
        if source_type == "canonical" and job.prompt_type != "canonical":
            raise ValueError("Canonical schedules must use the canonical prompt type.")
        if source_type != "canonical" and job.prompt_type != "custom":
            raise ValueError("Saved and custom schedules must snapshot custom prompt text.")
        spec = self._schedule_spec(values)
        next_run_at = compute_next_run(spec)
        if next_run_at is None:
            raise ValueError("That scheduled time is already in the past.")
        return {
            "name": clean_name,
            "enabled": bool(values.get("enabled", True)),
            "destination": job.destination,
            "prompt_type": job.prompt_type,
            "custom_prompt": job.custom_prompt,
            "mode": job.mode,
            "confirm_send": job.confirm_send,
            "default_destination": job.default_destination,
            "confirm_destination": job.confirm_destination,
            "source_type": source_type,
            "source_prompt_id": values.get("source_prompt_id"),
            "cadence": spec.cadence,
            "schedule_date": spec.schedule_date,
            "schedule_time": spec.schedule_time,
            "weekdays": list(spec.weekdays),
            "timezone": spec.timezone,
            "next_run_at": next_run_at if bool(values.get("enabled", True)) else None,
        }

    def create_schedule(self, values: dict[str, object]) -> dict[str, object]:
        return self.store.create_schedule(self._prepare_schedule(values))

    def update_schedule(
        self, schedule_id: int, values: dict[str, object]
    ) -> dict[str, object] | None:
        return self.store.update_schedule(schedule_id, self._prepare_schedule(values))

    def set_schedule_enabled(
        self, schedule_id: int, enabled: bool
    ) -> dict[str, object] | None:
        schedule = self.store.get_schedule(schedule_id)
        if schedule is None:
            return None
        next_run_at = None
        if enabled:
            next_run_at = compute_next_run(self._schedule_spec(schedule))
            if next_run_at is None:
                raise ValueError("This one-time schedule is already in the past and cannot be resumed.")
        return self.store.set_schedule_enabled(schedule_id, enabled, next_run_at)

    def delete_schedule(self, schedule_id: int) -> bool:
        return self.store.delete_schedule(schedule_id)

    def schedules(self) -> list[dict[str, object]]:
        return self.store.list_schedules()

    def _job_from_schedule(self, schedule: dict[str, object]) -> CommandJob:
        return CommandJob(
            destination=str(schedule["destination"]),
            prompt_type=str(schedule["prompt_type"]),  # type: ignore[arg-type]
            mode=str(schedule["mode"]),  # type: ignore[arg-type]
            custom_prompt=str(schedule.get("custom_prompt") or ""),
            confirm_send=bool(schedule.get("confirm_send")),
            default_destination=(
                str(schedule["default_destination"])
                if schedule.get("default_destination") is not None
                else None
            ),
            confirm_destination=bool(schedule.get("confirm_destination")),
        )

    def start_scheduler(self) -> None:
        if self.scheduler_running:
            return
        self._scheduler_stop.clear()
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            name="lifeos-command-scheduler",
            daemon=True,
        )
        self._scheduler_thread.start()

    def stop_scheduler(self, timeout: float = 3.0) -> None:
        self._scheduler_stop.set()
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduler_thread.join(timeout=timeout)

    def _scheduler_loop(self) -> None:
        while not self._scheduler_stop.wait(self._scheduler_poll_seconds):
            if self.paused or self.running:
                continue
            for schedule in self.store.due_schedules(time.time()):
                if self._scheduler_stop.is_set() or self.paused:
                    return
                self._run_scheduled(schedule)

    def _run_scheduled(self, schedule: dict[str, object]) -> None:
        schedule_id = int(schedule["id"])
        result = self.execute(self._job_from_schedule(schedule))
        if result.status == "refused" and (
            "Another automation job is running" in result.reason
            or "Automation is paused" in result.reason
        ):
            self.store.defer_schedule(schedule_id, time.time() + 60, result.reason)
            return
        cadence = str(schedule["cadence"])
        enabled = cadence != "once"
        next_run_at = None
        if enabled:
            next_run_at = compute_next_run(
                self._schedule_spec(schedule),
                after_timestamp=max(time.time(), float(schedule.get("next_run_at") or 0)),
            )
        self.store.complete_schedule(
            schedule_id,
            enabled=enabled,
            next_run_at=next_run_at,
            result=result.to_dict(),
        )

    def history(self) -> list[dict[str, object]]:
        return self.store.history(self.history_limit)

    def status(self) -> dict[str, object]:
        return {
            "paused": self.paused,
            "running": self.running,
            "scheduler_running": self.scheduler_running,
            "destinations": [asdict(destination) for destination in DESTINATIONS.values()],
            "saved_prompts": self.store.list_prompts(),
            "scheduled_jobs": self.schedules(),
            "history": self.history(),
        }

    def _record(self, result: ExecutionResult) -> ExecutionResult:
        self.store.add_history(result.to_dict())
        return result

    def execute(self, job: CommandJob, timeout_seconds: int = 120) -> ExecutionResult:
        started_at = time.time()
        if self.paused:
            return self._record(
                ExecutionResult(
                    "refused", job.destination, job.mode, job.prompt_type, None,
                    started_at, time.time(), "", "",
                    "Automation is paused. Resume it before running a job.",
                )
            )
        if not self._run_lock.acquire(blocking=False):
            return self._record(
                ExecutionResult(
                    "refused", job.destination, job.mode, job.prompt_type, None,
                    started_at, time.time(), "", "",
                    "Another automation job is running. Let it finish before starting a new one.",
                )
            )
        try:
            return self._record(run_job(job, self.app_root, timeout_seconds=timeout_seconds))
        finally:
            self._run_lock.release()
