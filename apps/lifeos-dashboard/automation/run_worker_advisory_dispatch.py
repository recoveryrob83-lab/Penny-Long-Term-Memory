"""One-shot canonical advisory scanner and Worker wake dispatcher.

Schedule this entrypoint when event-driven filesystem hooks are unavailable. It reads the
Advisory Index, resolves execution-ready Worker advisories from their source boards, and passes
reference-only wake jobs into the existing Worker Command Center. The Command Center remains
responsible for route, pause, exact-title, send confirmation, history, and duplicate suppression.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_advisory_pipeline import AdvisoryWakePipeline
from lifeos_dashboard.worker_command_center import WorkerCommandCenterService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    default_app_root = Path(__file__).resolve().parents[1]
    default_repository_root = default_app_root.parents[1]
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=default_repository_root,
        help="LifeOS repository root containing coordination/ADVISORY_INDEX.md.",
    )
    parser.add_argument(
        "--app-root",
        type=Path,
        default=default_app_root,
        help="LifeOS Dashboard app root.",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=None,
        help="Command Center SQLite path. Defaults to <app-root>/.local/command_center.sqlite3.",
    )
    parser.add_argument("--advisory-id", help="Dispatch one advisory instead of every candidate.")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument(
        "--trigger",
        choices=("manual", "scheduled"),
        default="scheduled",
    )
    parser.add_argument(
        "--mode",
        choices=("draft", "send"),
        default="draft",
        help="Draft is the safe inspection default. Scheduled operation normally uses send.",
    )
    parser.add_argument(
        "--confirm-send",
        default="",
        help="Required exact value SEND when --mode send is selected.",
    )
    return parser


def _summary(dispatch) -> dict[str, object]:
    return {
        "advisory_id": dispatch.advisory.advisory_id,
        "advisory_revision": dispatch.advisory.advisory_revision,
        "worker_id": dispatch.advisory.target_worker_id,
        "wrapper_id": dispatch.job.envelope.wrapper_id,
        "run_id": dispatch.job.envelope.run_id,
        "idempotency_key": dispatch.job.envelope.idempotency_key,
        "mode": dispatch.job.mode,
        "status": dispatch.result.status,
        "destination": dispatch.result.destination,
        "reason": dispatch.result.reason,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.mode == "send" and args.confirm_send != "SEND":
        print("STOPPED: send mode requires --confirm-send SEND.", file=sys.stderr)
        return 2
    if args.timeout_seconds < 1:
        print("STOPPED: --timeout-seconds must be positive.", file=sys.stderr)
        return 2

    command_center = CommandCenterService(
        args.app_root.resolve(),
        database_path=args.database.resolve() if args.database else None,
    )
    worker_center = WorkerCommandCenterService(command_center)
    pipeline = AdvisoryWakePipeline(args.repository_root.resolve(), worker_center)
    try:
        if args.advisory_id:
            dispatches = (
                pipeline.dispatch(
                    args.advisory_id,
                    mode=args.mode,
                    confirm_send=args.mode == "send",
                    trigger=args.trigger,
                    timeout_seconds=args.timeout_seconds,
                ),
            )
        else:
            dispatches = pipeline.dispatch_all(
                mode=args.mode,
                confirm_send=args.mode == "send",
                trigger=args.trigger,
                timeout_seconds=args.timeout_seconds,
            )
    except WorkerRuntimeError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2

    print(json.dumps([_summary(item) for item in dispatches], indent=2, sort_keys=True))
    if any(item.result.status != "succeeded" for item in dispatches):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
