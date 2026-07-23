"""Run the local GitHub-first Life OS Worker orchestration loop.

GitHub is the operational desk and department communication layer. SQLite is used only
for local transport memory, locks, duplicate suppression, and restart recovery.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_operations import WorkerOperationsService
from lifeos_dashboard.worker_result_contract import artifact_path
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


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


def _run(command: list[str], *, cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _git(repository_root: Path, *arguments: str, timeout: int = 60) -> str:
    completed = _run(["git", *arguments], cwd=repository_root, timeout=timeout)
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise WorkerRuntimeError(f"Git command failed: {detail or arguments!r}")
    return completed.stdout.strip()


def sync_repository(repository_root: Path) -> dict[str, object]:
    """Fast-forward a clean checkout; stop on local work or divergence."""

    if _git(repository_root, "status", "--porcelain"):
        raise WorkerRuntimeError("Local Git checkout has uncommitted changes; orchestration paused.")
    branch = _git(repository_root, "branch", "--show-current")
    if not branch:
        raise WorkerRuntimeError("Local Git checkout is detached; orchestration paused.")
    _git(repository_root, "fetch", "origin", branch, timeout=120)
    counts = _git(
        repository_root,
        "rev-list",
        "--left-right",
        "--count",
        f"HEAD...origin/{branch}",
    ).split()
    if len(counts) != 2:
        raise WorkerRuntimeError("Could not determine local and remote Git relationship.")
    ahead, behind = (int(value) for value in counts)
    if ahead and behind:
        raise WorkerRuntimeError("Local and remote Git histories diverged; orchestration paused.")
    if ahead:
        raise WorkerRuntimeError("Local Git has unpushed commits; orchestration paused.")
    if behind:
        _git(repository_root, "merge", "--ff-only", f"origin/{branch}", timeout=120)
    return {"branch": branch, "ahead": ahead, "behind_applied": behind}


def _history_row(service: WorkerOperationsService, run_id: str) -> dict[str, object] | None:
    return next(
        (
            row
            for row in service.worker_center.browser_evidence.history(limit=500)
            if str(row.get("run_id") or "") == run_id
        ),
        None,
    )


def _run_hq_wake(app_root: Path, run_id: str) -> dict[str, object]:
    completed = _run(
        [
            sys.executable,
            str(app_root / "automation" / "run_worker_hq_review_wake.py"),
            "--run-id",
            run_id,
            "--send",
            "--confirm-send",
            "HQ_REVIEW_SEND",
        ],
        cwd=app_root,
        timeout=360,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise WorkerRuntimeError(detail or f"HQ wake failed for {run_id}.")
    return {"run_id": run_id, "action": "hq_wake_submitted"}


def tick(
    repository_root: Path,
    database_path: Path,
    app_root: Path,
) -> dict[str, object]:
    sync = sync_repository(repository_root)
    command_center = CommandCenterService(app_root, database_path=database_path)
    service = WorkerOperationsService(command_center, repository_root)
    events: list[dict[str, object]] = []

    advisories = service.pipeline.discover()

    # Dispatch at most one new advisory per tick. The shared browser gate and persisted
    # idempotency key remain the final duplicate protection.
    for advisory in advisories:
        if _history_row(service, advisory.run_id) is not None:
            continue
        payload = service.run_advisory(
            advisory.advisory_id,
            confirm_send=True,
            timeout_seconds=600,
        )
        events.append(
            {
                "action": "worker_dispatched",
                "advisory_id": advisory.advisory_id,
                "run_id": advisory.run_id,
                "worker_id": advisory.target_worker_id,
                "result": payload.get("result"),
            }
        )
        break

    # Process committed result and review evidence through the existing services.
    for advisory in advisories:
        row = _history_row(service, advisory.run_id)
        if row is None or advisory.result_contract is None:
            continue

        report_file = repository_root / advisory.result_contract.result_path
        result_state = str(row.get("result_state") or "")
        if report_file.is_file() and result_state not in {
            "REPORT_VALIDATED",
            "HQ_REVIEW_PENDING",
            "HQ_VERIFIED",
            "ROB_VALIDATION_REQUIRED",
            "READY_FOR_COS",
        }:
            receipt = service.ingest_result(advisory.run_id)
            events.append(
                {
                    "action": "worker_result_ingested",
                    "run_id": advisory.run_id,
                    "receipt": receipt.get("receipt"),
                }
            )
            row = _history_row(service, advisory.run_id) or row

        result_state = str(row.get("result_state") or "")
        hq_wake_state = str(row.get("hq_wake_state") or "")
        if result_state == "REPORT_VALIDATED" and not hq_wake_state:
            events.append(_run_hq_wake(app_root, advisory.run_id))
            row = _history_row(service, advisory.run_id) or row

        hq_review_path = artifact_path(
            str(row.get("owning_department") or ""),
            advisory.target_worker_id,
            advisory.run_id,
            "hq_review",
            1,
        )
        if (
            (repository_root / hq_review_path).is_file()
            and not str(row.get("hq_review_state") or "")
        ):
            receipt = service.ingest_hq_review(advisory.run_id)
            events.append(
                {
                    "action": "hq_review_ingested",
                    "run_id": advisory.run_id,
                    "receipt": receipt.get("receipt"),
                }
            )
            row = _history_row(service, advisory.run_id) or row

        rob_validation_path = artifact_path(
            str(row.get("owning_department") or ""),
            advisory.target_worker_id,
            advisory.run_id,
            "rob_validation",
            1,
        )
        if (
            (repository_root / rob_validation_path).is_file()
            and bool(row.get("requires_rob_validation"))
            and not str(row.get("rob_validation_state") or "")
        ):
            receipt = service.ingest_rob_validation(advisory.run_id)
            events.append(
                {
                    "action": "rob_validation_ingested",
                    "run_id": advisory.run_id,
                    "receipt": receipt.get("receipt"),
                }
            )

    return {"status": "succeeded", "sync": sync, "events": events}


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
    if args.poll_seconds < 10:
        print("STOPPED: poll-seconds must be at least 10.", file=sys.stderr)
        return 2

    while True:
        try:
            payload = tick(repository_root, database_path, app_root)
            if payload["events"]:
                print(
                    "LIFEOS_GITHUB_ORCHESTRATION="
                    + json.dumps(payload, sort_keys=True, ensure_ascii=False),
                    flush=True,
                )
        except (OSError, subprocess.TimeoutExpired, WorkerRuntimeError, ValueError) as exc:
            print(f"ORCHESTRATION_PAUSED: {exc}", file=sys.stderr, flush=True)
        if args.once:
            return 0
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
