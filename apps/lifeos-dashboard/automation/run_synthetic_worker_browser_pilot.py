"""Run one zero-authority Engineering Worker browser dispatch pilot."""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from dataclasses import dataclass

from chatgpt_worker_browser_dispatch import run_dispatch
from chatgpt_worker_browser_roundtrip import (
    BrowserRoundTripError,
    BrowserRoundTripRequest,
    BrowserRoundTripUncertain,
)
from lifeos_dashboard.worker_command_center import render_worker_prompt
from lifeos_dashboard.worker_runtime import ExecutionEnvelope

WORKER_URL = (
    "https://chatgpt.com/g/g-p-6a43ef8989a08191961253952ffe1670/"
    "c/6a5df5b7-f6b8-83ea-8f8e-1633d53941fe"
)
WORKER_CHAT_TITLE = "Engineering_Worker"
PROJECT_TITLE = "LifeOS"
AUTHORIZATION_SOURCE = "ROB-BOUNDED-SYNTHETIC-BROWSER-PILOT-20260720"
SEND_CONFIRMATION = "SYNTHETIC_SEND"
RECEIPT_PREFIX = "LIFEOS_SYNTHETIC_BROWSER_RECEIPT="


class SyntheticBrowserPilotError(ValueError):
    """Raised when the synthetic browser pilot contract is violated."""


@dataclass(frozen=True)
class SyntheticBrowserPilotPlan:
    envelope: ExecutionEnvelope
    prompt_text: str
    expected_ack: str
    request: BrowserRoundTripRequest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--confirm-send", default="")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--cdp-endpoint", default="http://127.0.0.1:9222")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if args.timeout_seconds < 30 or args.timeout_seconds > 900:
        raise SyntheticBrowserPilotError("timeout-seconds must be between 30 and 900.")
    if args.send and args.confirm_send != SEND_CONFIRMATION:
        raise SyntheticBrowserPilotError(
            f"Synthetic send requires --confirm-send {SEND_CONFIRMATION}."
        )
    if not args.send and args.confirm_send:
        raise SyntheticBrowserPilotError(
            "--confirm-send is valid only when --send is also present."
        )
    if not args.send and not args.dry_run:
        raise SyntheticBrowserPilotError("Use --dry-run or explicitly authorize --send.")


def build_envelope(*, timestamp: int | None = None, nonce: str | None = None) -> ExecutionEnvelope:
    moment = int(time.time()) if timestamp is None else int(timestamp)
    clean_nonce = (nonce or uuid.uuid4().hex[:10]).strip().lower()
    if not clean_nonce or not clean_nonce.isalnum():
        raise SyntheticBrowserPilotError("Synthetic nonce must be non-empty and alphanumeric.")
    token = f"{moment}-{clean_nonce}"
    return ExecutionEnvelope(
        wrapper_id=f"SYNTH-BROWSER-WRAP-{token}",
        run_id=f"SYNTH-BROWSER-RUN-{token}",
        worker_id="engineering_worker",
        task_id=f"SYNTH-BROWSER-TASK-{token}",
        task_revision=1,
        procedure_id="synthetic_browser_transport",
        procedure_version=1,
        authorization_source=AUTHORIZATION_SOURCE,
        verification_mode="IMMEDIATE_HQ",
    )


def build_instruction(envelope: ExecutionEnvelope) -> tuple[str, str]:
    expected_ack = f"SYNTHETIC_BROWSER_WRAPPER_RECEIVED {envelope.wrapper_id}"
    instruction = (
        "SYNTHETIC BROWSER TRANSPORT PILOT. This wrapper carries no real authority and requests "
        "no file, connector, calendar, email, task, dashboard, database, GitHub, or "
        "external-system action. Do not create or modify durable records. Acknowledge receipt "
        f"only with: {expected_ack}"
    )
    return instruction, expected_ack


def build_plan(
    *,
    timestamp: int | None = None,
    nonce: str | None = None,
    timeout_seconds: int = 300,
    cdp_endpoint: str = "http://127.0.0.1:9222",
) -> SyntheticBrowserPilotPlan:
    envelope = build_envelope(timestamp=timestamp, nonce=nonce)
    instruction, expected_ack = build_instruction(envelope)
    prompt_text = render_worker_prompt(envelope, instruction)
    request = BrowserRoundTripRequest(
        worker_url=WORKER_URL,
        worker_chat_title=WORKER_CHAT_TITLE,
        project_title=PROJECT_TITLE,
        prompt_text=prompt_text,
        request_marker=envelope.wrapper_id,
        response_marker=envelope.run_id,
        cdp_endpoint=cdp_endpoint,
        timeout_seconds=timeout_seconds,
    )
    return SyntheticBrowserPilotPlan(
        envelope=envelope,
        prompt_text=prompt_text,
        expected_ack=expected_ack,
        request=request,
    )


def dry_run_receipt(plan: SyntheticBrowserPilotPlan) -> dict[str, object]:
    return {
        "status": "dry_run",
        "worker_url": WORKER_URL,
        "worker_chat_title": WORKER_CHAT_TITLE,
        "wrapper_id": plan.envelope.wrapper_id,
        "run_id": plan.envelope.run_id,
        "task_id": plan.envelope.task_id,
        "expected_ack": plan.expected_ack,
        "durable_authority_created": False,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_args(args)
        plan = build_plan(
            timeout_seconds=args.timeout_seconds,
            cdp_endpoint=args.cdp_endpoint,
        )
    except (SyntheticBrowserPilotError, BrowserRoundTripError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2

    print(f"Synthetic browser target: {PROJECT_TITLE} / {WORKER_CHAT_TITLE}")
    print(f"Wrapper: {plan.envelope.wrapper_id}")
    print("Durable Worker authority: none")

    if args.dry_run:
        print(f"{RECEIPT_PREFIX}{json.dumps(dry_run_receipt(plan), sort_keys=True)}")
        return 0

    try:
        receipt = run_dispatch(plan.request)
    except BrowserRoundTripUncertain as exc:
        print(f"STOPPED_AFTER_SEND: {exc}", file=sys.stderr)
        return 3
    except BrowserRoundTripError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2

    payload = {
        "status": "succeeded",
        "dispatch_state": "DISPATCH_SUBMITTED",
        "wrapper_id": plan.envelope.wrapper_id,
        "run_id": plan.envelope.run_id,
        "task_id": plan.envelope.task_id,
        "expected_ack": plan.expected_ack,
        "user_turn_id": receipt.user_turn_id,
        "returned_to_source": receipt.returned_to_source,
        "durable_authority_created": False,
    }
    print("SYNTHETIC_BROWSER_DISPATCH_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
