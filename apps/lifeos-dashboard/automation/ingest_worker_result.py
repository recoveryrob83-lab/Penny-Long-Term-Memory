"""Ingest one canonical immutable Worker result into its existing execution row."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_operations import WorkerOperationsService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RECEIPT_PREFIX = "LIFEOS_RESULT_INGESTION_RECEIPT="


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repository-root")
    parser.add_argument("--database-path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    app_root = Path(__file__).resolve().parents[1]
    repository_root = (
        Path(args.repository_root).expanduser().resolve()
        if args.repository_root
        else app_root.parents[1]
    )
    database_path = (
        Path(args.database_path).expanduser().resolve()
        if args.database_path
        else app_root / ".local" / "command_center.sqlite3"
    )
    try:
        command_center = CommandCenterService(app_root, database_path=database_path)
        service = WorkerOperationsService(command_center, repository_root)
        payload = service.ingest_result(args.run_id)
    except (OSError, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2
    print("WORKER_RESULT_INGESTION_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
