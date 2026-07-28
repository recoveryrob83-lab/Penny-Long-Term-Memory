"""Recover one owning-HQ wake after a proven pre-submit orchestrator failure.

This command is intentionally narrow. It requires the global safety pause, an exact
active owning-HQ conversation witness, a validated report, one stale claim, and no
wake or review evidence. It releases only that empty claim and then performs one
explicitly confirmed pointer-only HQ review wake through the existing courier.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.command_center_safety_pause import safety_pause_reason_for_transport
from lifeos_dashboard.command_center_send_budget import BUDGET_RECOVERY_CONDITION
from lifeos_dashboard.worker_dispatch_runtime import parse_browser_dispatch_receipt
from lifeos_dashboard.worker_hq_review import WorkerHqReviewService
from lifeos_dashboard.worker_route_management import capture_chatgpt_conversation
from lifeos_dashboard.worker_runtime import WorkerRuntimeError, _conversation_url

SEND_CONFIRMATION = "HQ_WAKE_RECOVERY_SEND"
RECEIPT_PREFIX = "LIFEOS_HQ_WAKE_RECOVERY_RECEIPT="


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--hq-url", required=True)
    parser.add_argument("--repository-root")
    parser.add_argument("--database-path")
    parser.add_argument("--cdp-endpoint")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--confirm-recovery", default="")
    return parser.parse_args(argv)


def _resolved_path(
    explicit: str | None,
    environment_name: str,
    fallback: Path,
) -> Path:
    selected = explicit or os.getenv(environment_name)
    return Path(selected).expanduser().resolve() if selected else fallback.resolve()


def _release_pre_submit_claim(database_path: Path, run_id: str) -> dict[str, object]:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT * FROM execution_history
            WHERE run_id = ? AND mode = 'send' AND prompt_type = 'worker'
            ORDER BY id
            """,
            (run_id,),
        ).fetchall()
        if len(rows) != 1:
            raise WorkerRuntimeError(
                "HQ wake recovery requires exactly one authoritative Worker send row."
            )
        row = rows[0]
        if str(row["result_state"] or "") != "REPORT_VALIDATED":
            raise WorkerRuntimeError("HQ wake recovery requires REPORT_VALIDATED.")
        if row["hq_wake_claimed_at"] is None:
            raise WorkerRuntimeError("No stale owning-HQ wake claim exists to recover.")
        prohibited = {
            "hq_wake_state": row["hq_wake_state"],
            "hq_wake_user_turn_id": row["hq_wake_user_turn_id"],
            "hq_wake_receipt_json": row["hq_wake_receipt_json"],
            "hq_review_state": row["hq_review_state"],
        }
        present = [name for name, value in prohibited.items() if str(value or "").strip()]
        if present:
            raise WorkerRuntimeError(
                "HQ wake recovery found durable wake or review evidence: "
                + ", ".join(present)
                + ". The claim was not changed."
            )
        updated = connection.execute(
            """
            UPDATE execution_history
            SET hq_wake_claimed_at = NULL
            WHERE id = ?
              AND result_state = 'REPORT_VALIDATED'
              AND hq_wake_claimed_at IS NOT NULL
              AND COALESCE(hq_wake_state, '') = ''
              AND COALESCE(hq_wake_user_turn_id, '') = ''
              AND COALESCE(hq_wake_receipt_json, '') = ''
              AND COALESCE(hq_review_state, '') = ''
            """,
            (int(row["id"]),),
        )
        if updated.rowcount != 1:
            raise WorkerRuntimeError(
                "The owning-HQ wake state changed during recovery. The claim was not released."
            )
        return {
            "run_id": run_id,
            "row_id": int(row["id"]),
            "released_claimed_at": row["hq_wake_claimed_at"],
        }


def _require_exact_active_hq(
    *,
    cdp_endpoint: str,
    hq_url: str,
    hq_chat_title: str,
) -> dict[str, str]:
    captured = capture_chatgpt_conversation(cdp_endpoint)
    normalized = _conversation_url(hq_url)
    if normalized is None:
        raise WorkerRuntimeError("The supplied HQ URL is not a ChatGPT conversation URL.")
    if captured.url != normalized:
        raise WorkerRuntimeError(
            "The sole active ChatGPT conversation does not match --hq-url. Nothing was changed."
        )
    if hq_chat_title.casefold() not in captured.title.casefold():
        raise WorkerRuntimeError(
            "The sole active ChatGPT conversation does not match the owning-HQ title "
            f"{hq_chat_title!r}. Observed browser title: {captured.title!r}. Nothing was changed."
        )
    return {"url": normalized, "title": captured.title}


def _reserve_budget(command_center: CommandCenterService, run_id: str):
    decision = command_center.reserve_send_budget(kind="hq_review_wake", run_id=run_id)
    if not decision.reserved:
        command_center.trip_safety_pause(
            reason=decision.reason,
            affected_run_id=run_id,
            trigger="send_budget",
            recovery_condition=BUDGET_RECOVERY_CONDITION,
        )
        raise WorkerRuntimeError(decision.reason)
    command_center.append_send_budget_evidence(run_id=run_id, decision=decision)
    return decision


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
        "LIFEOS_CHATGPT_CDP_ENDPOINT",
        "http://127.0.0.1:9222",
    )
    if not args.send or args.confirm_recovery != SEND_CONFIRMATION:
        print(
            "STOPPED: HQ wake recovery requires --send --confirm-recovery "
            f"{SEND_CONFIRMATION}.",
            file=sys.stderr,
        )
        return 2
    if args.timeout_seconds < 60 or args.timeout_seconds > 900:
        print("STOPPED: timeout-seconds must be between 60 and 900.", file=sys.stderr)
        return 2

    command_center = CommandCenterService(app_root, database_path=database_path)
    review = WorkerHqReviewService(repository_root, database_path)
    try:
        pause = command_center.pause_state()
        if not pause.get("paused") or pause.get("pause_kind") != "safety":
            raise WorkerRuntimeError(
                "HQ wake recovery requires the persisted safety pause. Nothing was changed."
            )
        if str(pause.get("affected_run_id") or "") != args.run_id:
            raise WorkerRuntimeError(
                "The persisted safety pause belongs to a different run. Nothing was changed."
            )
        wake = review.build_wake(args.run_id)
        active_hq = _require_exact_active_hq(
            cdp_endpoint=cdp_endpoint,
            hq_url=args.hq_url,
            hq_chat_title=wake.hq_chat_title,
        )
        run_lock = command_center._run_lock
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError("Another automation job is already running.")
        try:
            released = _release_pre_submit_claim(database_path, args.run_id)
            budget = _reserve_budget(command_center, args.run_id)
            command = [
                sys.executable,
                str(app_root / "automation" / "chatgpt_worker_browser_dispatch.py"),
                "--worker-url",
                active_hq["url"],
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
                pause_reason = safety_pause_reason_for_transport(
                    exit_code=completed.returncode,
                    stderr=completed.stderr,
                    reason=detail,
                )
                command_center.trip_safety_pause(
                    reason=pause_reason or detail or "HQ wake recovery transport failed.",
                    affected_run_id=args.run_id,
                    trigger="hq_review_recovery",
                )
                raise WorkerRuntimeError(detail or "HQ wake recovery transport failed.")
            receipt = parse_browser_dispatch_receipt(completed.stdout)
            persisted = review.record_wake(args.run_id, receipt)
            if not bool(receipt.get("returned_to_source")):
                command_center.trip_safety_pause(
                    reason="Recovered HQ wake did not verify return to its source conversation.",
                    affected_run_id=args.run_id,
                    trigger="hq_review_recovery",
                )
                raise WorkerRuntimeError(
                    "Recovered HQ wake did not verify return to its source conversation."
                )
            command_center.set_paused(False)
        finally:
            run_lock.release()
    except (
        OSError,
        sqlite3.Error,
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
        "active_hq": active_hq,
        "released_claim": released,
        "browser_receipt": receipt,
        "pause": command_center.pause_state(),
        "send_budget": command_center.send_budget_state(),
        "send_budget_reservation": budget.to_dict(),
    }
    print("HQ_WAKE_RECOVERY_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())