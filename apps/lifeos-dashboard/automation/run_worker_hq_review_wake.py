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


def _resolved_path(explicit: str | None, environment_name: str, fallback: Path) -> Path:
    selected = explicit or os.getenv(environment_name)
    return Path(selected).expanduser().resolve() if selected else fallback.resolve()


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
            f"STOPPED: Live HQ review wake requires --send --confirm-send {SEND_CONFIRMATION}.",
            file=sys.stderr,
        )
        return 2
    if args.timeout_seconds < 60 or args.timeout_seconds > 900:
        print("STOPPED: timeout-seconds must be between 60 and 900.", file=sys.stderr)
        return 2

    command_center = CommandCenterService(app_root, database_path=database_path)
    review = WorkerHqReviewService(repository_root, database_path)
    try:
        if command_center.paused:
            raise WorkerRuntimeError("Automation is paused. Resume it before waking an HQ.")
        run_lock = command_center._run_lock  # noqa: SLF001 - shared one-job execution gate
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
                os.getenv("LIFEOS_CHATGPT_PROJECT_TITLE", "Life OS"),
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
            completed = subprocess.run(
                command,
                cwd=app_root,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=args.timeout_seconds + 30,
                check=False,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise WorkerRuntimeError(
                    detail
                    or "HQ review courier stopped before a verified pointer-only wake completed."
                )
            browser_receipt = parse_browser_dispatch_receipt(completed.stdout)
            persisted = review.record_wake(args.run_id, browser_receipt)
        finally:
            run_lock.release()
    except (OSError, subprocess.TimeoutExpired, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        print(f"Repository: {repository_root}", file=sys.stderr)
        print(f"Database: {database_path}", file=sys.stderr)
        return 2

    payload = {
        "status": "succeeded",
        "wake": persisted.to_dict(),
        "browser_receipt": browser_receipt,
        "hq_review": review.status(limit=100),
    }
    print("HQ_REVIEW_WAKE_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
