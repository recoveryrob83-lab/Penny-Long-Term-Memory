"""Run the canonical local GitHub-first LifeOS Worker orchestration loop."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_github_orchestrator import WorkerGitHubOrchestrator
from lifeos_dashboard.worker_operations import WorkerOperationsService
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


RECEIPT_PREFIX = "LIFEOS_GITHUB_ORCHESTRATION="


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root")
    parser.add_argument("--database-path")
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--once", action="store_true")
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
        command_center = CommandCenterService(app_root, database_path=database_path)
        operations = WorkerOperationsService(command_center, repository_root)
        orchestrator = WorkerGitHubOrchestrator(
            operations,
            repository_root,
            database_path,
            poll_seconds=args.poll_seconds,
            sync_branch=os.getenv("LIFEOS_GITHUB_SYNC_BRANCH", "main"),
            timeout_seconds=600,
        )
    except (OSError, WorkerRuntimeError, ValueError) as exc:
        print(f"ORCHESTRATION_STOPPED: {exc}", file=sys.stderr)
        return 2

    while True:
        payload = orchestrator.run_once()
        events = payload.get("events") or []
        if events:
            print(
                RECEIPT_PREFIX + json.dumps(payload, sort_keys=True, ensure_ascii=False),
                flush=True,
            )
        if args.once:
            return 0 if payload.get("last_error") is None else 2
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
