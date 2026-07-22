"""Ingest one immutable Rob-validation receipt into its existing execution row."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from lifeos_dashboard.worker_rob_validation import WorkerRobValidationService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RECEIPT_PREFIX = "LIFEOS_ROB_VALIDATION_INGESTION_RECEIPT="


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repository-root")
    parser.add_argument("--database-path")
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
    try:
        service = WorkerRobValidationService(repository_root, database_path)
        receipt = service.ingest_validation(args.run_id)
    except (OSError, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        print(f"Repository: {repository_root}", file=sys.stderr)
        print(f"Database: {database_path}", file=sys.stderr)
        return 2
    payload = {
        "status": "succeeded",
        "receipt": receipt.to_dict(),
        "rob_validation": service.status(limit=100),
        "verification": service.verification.status(limit=100),
    }
    print("ROB_VALIDATION_INGESTION_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
