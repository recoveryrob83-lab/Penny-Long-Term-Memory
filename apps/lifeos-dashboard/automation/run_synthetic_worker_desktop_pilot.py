"""Run one bounded synthetic Worker transport exercise through ChatGPT Classic.

This launcher is intentionally locked to one disposable visible chat title inside the Life OS
project. It creates no Worker profile, registry entry, route record, schedule, wake, or durable
authority. Draft-only is the default. Sending requires two explicit CLI flags.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from lifeos_dashboard.worker_command_center import render_worker_prompt
from lifeos_dashboard.worker_runtime import ExecutionEnvelope

SYNTHETIC_CHAT_TITLE = "Synthetic_Worker_Pilot"
SYNTHETIC_PROJECT_TITLE = "Life OS"
SYNTHETIC_WORKER_ID = "synthetic_desktop_worker"
SYNTHETIC_PROCEDURE_ID = "synthetic_desktop_transport"
SYNTHETIC_AUTHORIZATION_SOURCE = "ROB-BOUNDED-SYNTHETIC-DESKTOP-PILOT-20260719"
SEND_CONFIRMATION = "SYNTHETIC_SEND"
RECEIPT_PREFIX = "LIFEOS_SYNTHETIC_DESKTOP_RECEIPT="


class SyntheticDesktopPilotError(ValueError):
    """Raised when the bounded pilot's explicit safety contract is violated."""


@dataclass(frozen=True)
class SyntheticDesktopPilotPlan:
    """One disposable wrapper and exact UI transport command."""

    envelope: ExecutionEnvelope
    instruction: str
    command: tuple[str, ...]
    mode: str

    def receipt(self, *, status: str, exit_code: int | None) -> dict[str, object]:
        return {
            "status": status,
            "mode": self.mode,
            "exit_code": exit_code,
            "project_title": SYNTHETIC_PROJECT_TITLE,
            "chat_title": SYNTHETIC_CHAT_TITLE,
            "wrapper_id": self.envelope.wrapper_id,
            "run_id": self.envelope.run_id,
            "task_id": self.envelope.task_id,
            "worker_id": self.envelope.worker_id,
            "durable_authority_created": False,
        }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Exercise the verified Worker wrapper through one disposable ChatGPT Classic chat. "
            "The target is fixed and draft-only unless explicit send confirmation is supplied."
        )
    )
    parser.add_argument("--send", action="store_true", help="Submit the synthetic prompt.")
    parser.add_argument("--confirm-send", default="")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the bounded receipt and command metadata without opening ChatGPT Classic.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=90,
        help="Maximum time allowed for the verified UI transport subprocess.",
    )
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if args.timeout_seconds < 15 or args.timeout_seconds > 180:
        raise SyntheticDesktopPilotError("timeout-seconds must be between 15 and 180.")
    if args.send and args.confirm_send != SEND_CONFIRMATION:
        raise SyntheticDesktopPilotError(
            f"Synthetic send requires --confirm-send {SEND_CONFIRMATION}."
        )
    if not args.send and args.confirm_send:
        raise SyntheticDesktopPilotError(
            "--confirm-send is valid only when --send is also present."
        )


def build_envelope(*, timestamp: int | None = None, nonce: str | None = None) -> ExecutionEnvelope:
    moment = int(time.time()) if timestamp is None else int(timestamp)
    clean_nonce = (nonce or uuid.uuid4().hex[:10]).strip().lower()
    if not clean_nonce or not clean_nonce.isalnum():
        raise SyntheticDesktopPilotError("Synthetic nonce must be non-empty and alphanumeric.")
    token = f"{moment}-{clean_nonce}"
    return ExecutionEnvelope(
        wrapper_id=f"SYNTH-DESKTOP-WRAP-{token}",
        run_id=f"SYNTH-DESKTOP-RUN-{token}",
        worker_id=SYNTHETIC_WORKER_ID,
        task_id=f"SYNTH-DESKTOP-TASK-{token}",
        task_revision=1,
        procedure_id=SYNTHETIC_PROCEDURE_ID,
        procedure_version=1,
        authorization_source=SYNTHETIC_AUTHORIZATION_SOURCE,
        verification_mode="IMMEDIATE_HQ",
    )


def build_instruction(envelope: ExecutionEnvelope) -> str:
    return (
        "SYNTHETIC DESKTOP TRANSPORT PILOT. This wrapper carries no real authority and requests "
        "no file, connector, calendar, email, task, dashboard, or external-system action. Do not "
        "create or modify durable records. Acknowledge receipt only with: "
        f"SYNTHETIC_WRAPPER_RECEIVED {envelope.wrapper_id}"
    )


def build_plan(
    app_root: Path,
    *,
    send: bool,
    timestamp: int | None = None,
    nonce: str | None = None,
) -> SyntheticDesktopPilotPlan:
    envelope = build_envelope(timestamp=timestamp, nonce=nonce)
    instruction = build_instruction(envelope)
    rendered_prompt = render_worker_prompt(envelope, instruction)
    command = [
        sys.executable,
        str(app_root / "automation" / "open_worker_chat_group_verified.py"),
        SYNTHETIC_CHAT_TITLE,
        "--project",
        SYNTHETIC_PROJECT_TITLE,
        "--text",
        rendered_prompt,
        "--verify-marker",
        envelope.wrapper_id,
    ]
    mode = "send" if send else "draft"
    if send:
        command.extend(["--send", "--confirm-send", "SEND"])
    return SyntheticDesktopPilotPlan(
        envelope=envelope,
        instruction=instruction,
        command=tuple(command),
        mode=mode,
    )


def emit_receipt(plan: SyntheticDesktopPilotPlan, *, status: str, exit_code: int | None) -> None:
    payload = json.dumps(plan.receipt(status=status, exit_code=exit_code), sort_keys=True)
    print(f"{RECEIPT_PREFIX}{payload}")


def run_plan(
    plan: SyntheticDesktopPilotPlan,
    app_root: Path,
    *,
    timeout_seconds: int,
) -> int:
    try:
        completed = subprocess.run(
            list(plan.command),
            cwd=app_root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        if exc.stdout:
            print(exc.stdout, end="" if str(exc.stdout).endswith("\n") else "\n")
        if exc.stderr:
            print(exc.stderr, file=sys.stderr, end="" if str(exc.stderr).endswith("\n") else "\n")
        emit_receipt(plan, status="timed_out", exit_code=None)
        return 1

    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(
            completed.stderr,
            file=sys.stderr,
            end="" if completed.stderr.endswith("\n") else "\n",
        )
    status = "succeeded" if completed.returncode == 0 else "failed"
    emit_receipt(plan, status=status, exit_code=completed.returncode)
    return 0 if completed.returncode == 0 else 1


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_args(args)
    except SyntheticDesktopPilotError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2

    app_root = Path(__file__).resolve().parents[1]
    plan = build_plan(app_root, send=bool(args.send))
    print(f"Synthetic target: {SYNTHETIC_PROJECT_TITLE} / {SYNTHETIC_CHAT_TITLE}")
    print(f"Mode: {plan.mode}")
    print(f"Wrapper: {plan.envelope.wrapper_id}")
    print("Durable Worker authority: none")

    if args.dry_run:
        emit_receipt(plan, status="dry_run", exit_code=None)
        return 0
    return run_plan(plan, app_root, timeout_seconds=int(args.timeout_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
