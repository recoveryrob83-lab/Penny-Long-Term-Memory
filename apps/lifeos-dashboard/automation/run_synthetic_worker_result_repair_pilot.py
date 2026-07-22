"""Run the disposable Package E malformed-report rejection and repair pilot."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from lifeos_dashboard.worker_result_repair_pilot import run_synthetic_repair_pilot
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RECEIPT_PREFIX = "LIFEOS_SYNTHETIC_RESULT_REPAIR_RECEIPT="
_CHILD_RECEIPT_PREFIX = "LIFEOS_SYNTHETIC_RESULT_REPAIR_CHILD_RECEIPT="


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child-workdir", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def _run_child(workdir: Path) -> int:
    try:
        payload = run_synthetic_repair_pilot(workdir)
    except (OSError, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2
    print(f"{_CHILD_RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


def _parse_child_receipt(stdout: str) -> dict[str, object]:
    lines = [
        line.removeprefix(_CHILD_RECEIPT_PREFIX)
        for line in stdout.splitlines()
        if line.startswith(_CHILD_RECEIPT_PREFIX)
    ]
    if len(lines) != 1:
        raise WorkerRuntimeError(
            "Synthetic result-repair child did not emit exactly one machine-readable receipt."
        )
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError("Synthetic result-repair child receipt is invalid JSON.") from exc
    if not isinstance(payload, dict):
        raise WorkerRuntimeError("Synthetic result-repair child receipt has the wrong shape.")
    return payload


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.child_workdir:
        return _run_child(Path(args.child_workdir).resolve())

    script = Path(__file__).resolve()
    app_root = script.parents[1]
    try:
        # Windows may keep SQLite handles alive until the owning process exits. Run the disposable
        # proof in a child process so all database handles are released before sandbox cleanup.
        with tempfile.TemporaryDirectory(prefix="lifeos-result-repair-") as directory:
            completed = subprocess.run(
                [sys.executable, str(script), "--child-workdir", directory],
                cwd=app_root,
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise WorkerRuntimeError(
                    detail or "Synthetic result-repair child process stopped without a receipt."
                )
            payload = _parse_child_receipt(completed.stdout)
    except (OSError, subprocess.TimeoutExpired, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2

    print("SYNTHETIC_RESULT_REPAIR_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
