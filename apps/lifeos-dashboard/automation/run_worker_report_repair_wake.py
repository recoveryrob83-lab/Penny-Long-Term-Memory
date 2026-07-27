"""Send one prepared correction-only Worker report wake."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_operations import WorkerOperationsService
from lifeos_dashboard.worker_report_repair_dispatch import WorkerReportRepairDispatchService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RECEIPT_PREFIX = "LIFEOS_REPORT_REPAIR_DISPATCH="
SEND_CONFIRMATION = "REPORT_REPAIR_SEND"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repository-root")
    parser.add_argument("--database-path")
    parser.add_argument("--timeout-seconds", type=int, default=600)
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
    if not args.send or args.confirm_send != SEND_CONFIRMATION:
        print(
            "STOPPED: Live report repair wake requires "
            f"--send --confirm-send {SEND_CONFIRMATION}.",
            file=sys.stderr,
        )
        return 2

    try:
        command_center = CommandCenterService(app_root, database_path=database_path)
        operations = WorkerOperationsService(command_center, repository_root)
        service = WorkerReportRepairDispatchService(operations, database_path)
        receipt = service.dispatch(
            args.run_id,
            timeout_seconds=args.timeout_seconds,
        )
    except (OSError, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        print(f"Repository: {repository_root}", file=sys.stderr)
        print(f"Database: {database_path}", file=sys.stderr)
        return 2

    payload = {
        "status": "succeeded",
        "receipt": receipt.to_dict(),
        "repair": service.status(args.run_id),
        "pause": command_center.pause_state(),
        "send_budget": command_center.send_budget_state(),
    }
    print("WORKER_REPORT_REPAIR_WAKE_OK")
    print(RECEIPT_PREFIX + json.dumps(payload, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
