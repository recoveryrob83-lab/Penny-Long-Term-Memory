"""Send one pointer-only owning-HQ review wake for a validated Worker result."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.command_center_safety_pause import (
    safety_pause_reason_for_transport,
)
from lifeos_dashboard.worker_dispatch_runtime import parse_browser_dispatch_receipt
from lifeos_dashboard.worker_hq_review import WorkerHqReviewService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RECEIPT_PREFIX = "LIFEOS_HQ_REVIEW_WAKE_RECEIPT="
SEND_CONFIRMATION = "HQ_REVIEW_SEND"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repository-root")
    parser.add_argument("--database-path")
    parser.add_argument("--cdp-endpoint")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--confirm-send", default="")
    return parser.parse_args(argv)


def _resolved_path(
    explicit: str | None,
    environment_name: str,
    fallback: Path,
) -> Path:
    selected = explicit or os.getenv(environment_name)
    return Path(selected).expanduser().resolve() if selected else fallback.resolve()


def _trip_for_transport(
    command_center: CommandCenterService,
    *,
    run_id: str,
    exit_code: int | None,
    stderr: str,
    reason: str,
    claimed_success_without_valid_receipt: bool = False,
) -> None:
    pause_reason = safety_pause_reason_for_transport(
        exit_code=exit_code,
        stderr=stderr,
        reason=reason,
        claimed_success_without_valid_receipt=claimed_success_without_valid_receipt,
    )
    if pause_reason is None:
        return
    command_center.trip_safety_pause(
        reason=pause_reason,
        affected_run_id=run_id,
        trigger="hq_review_browser_transport",
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    app_root = Path(__file__).resolve().parents[1]
    load_dotenv(app_root / ".env", override=False)
    repository_root = _resolved_path(
        args.repository_root,
        "LIFEOS_REPOSITORY_ROOT",
        app_root.parents[1],
    )
    database_path = _resolved_path(
        args.database_path,
        "COMMAND_CENTER_DATABASE_PATH",
        app_root / ".local" / "command_center.sqlite3",
    )
    cdp_endpoint = args.cdp_endpoint or os.getenv(
        "LIFEOS_CHATGPT_CDP_ENDPOINT", "http://127.0.0.1:9222"
    )
    if not args.send or args.confirm_send != SEND_CONFIRMATION:
        print(
            "STOPPED: Live HQ review wake requires "
            f"--send --confirm-send {SEND_CONFIRMATION}.",
            file=sys.stderr,
        )
        return 2
    if args.timeout_seconds < 60 or args.timeout_seconds > 900:
        print("STOPPED: timeout-seconds must be between 60 and 900.", file=sys.stderr)
        return 2

    command_center = CommandCenterService(app_root, database_path=database_path)
    review = WorkerHqReviewService(repository_root, database_path)
    completed: subprocess.CompletedProcess[str] | None = None
    try:
        if command_center.paused:
            raise WorkerRuntimeError("Automation is paused. Resume it before waking an HQ.")
        run_lock = command_center._run_lock
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError("Another automation job is already running.")
        try:
            wake = review.build_wake(args.run_id)
            command = [
                sys.executable,
                str(app_root / "automation" / "chatgpt_worker_browser_dispatch.py"),
                "--worker-chat-title",
                wake.hq_chat_title,
                "--project-title",
                os.getenv("LIFEOS_CHATGPT_PROJECT_TITLE", "LifeOS"),
                "--text",
                wake.instruction,
                "--request-marker",
                wake.marker,
                "--response-marker",
                wake.run_id,
                "--cdp-endpoint",
                cdp_endpoint,
                "--timeout-seconds",
                str(args.timeout_seconds),
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
                    timeout=args.timeout_seconds + 30,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                _trip_for_transport(
                    command_center,
                    run_id=args.run_id,
                    exit_code=None,
                    stderr=str(exc.stderr or ""),
                    reason=(
                        "HQ review browser transport timed out before submission "
                        "could be proven."
                    ),
                )
                raise

            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                _trip_for_transport(
                    command_center,
                    run_id=args.run_id,
                    exit_code=completed.returncode,
                    stderr=completed.stderr,
                    reason=detail,
                )
                raise WorkerRuntimeError(
                    detail
                    or "HQ review courier stopped before a verified pointer-only wake completed."
                )

            try:
                browser_receipt = parse_browser_dispatch_receipt(completed.stdout)
                persisted = review.record_wake(args.run_id, browser_receipt)
            except WorkerRuntimeError as exc:
                _trip_for_transport(
                    command_center,
                    run_id=args.run_id,
                    exit_code=completed.returncode,
                    stderr=completed.stderr,
                    reason=str(exc),
                    claimed_success_without_valid_receipt=True,
                )
                raise

            if not bool(browser_receipt.get("returned_to_source")):
                _trip_for_transport(
                    command_center,
                    run_id=args.run_id,
                    exit_code=completed.returncode,
                    stderr=completed.stderr,
                    reason="HQ review courier could not verify return to the source chat.",
                )
        finally:
            run_lock.release()
    except (
        OSError,
        subprocess.TimeoutExpired,
        WorkerRuntimeError,
        ValueError,
    ) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        print(f"Repository: {repository_root}", file=sys.stderr)
        print(f"Database: {database_path}", file=sys.stderr)
        return 2

    payload = {
        "status": "succeeded",
        "wake": persisted.to_dict(),
        "browser_receipt": browser_receipt,
        "hq_review": review.status(limit=100),
        "pause": command_center.pause_state(),
    }
    print("HQ_REVIEW_WAKE_OK")
    print(
        f"{RECEIPT_PREFIX}"
        f"{json.dumps(payload, sort_keys=True, ensure_ascii=False)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
