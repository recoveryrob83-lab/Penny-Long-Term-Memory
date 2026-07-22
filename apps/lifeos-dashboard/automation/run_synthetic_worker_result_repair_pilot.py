"""Run the disposable Package E malformed-report rejection and repair pilot."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from lifeos_dashboard.worker_result_repair_pilot import run_synthetic_repair_pilot
from lifeos_dashboard.worker_runtime import WorkerRuntimeError

RECEIPT_PREFIX = "LIFEOS_SYNTHETIC_RESULT_REPAIR_RECEIPT="


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="lifeos-result-repair-") as directory:
            payload = run_synthetic_repair_pilot(Path(directory))
    except (OSError, WorkerRuntimeError, ValueError) as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2
    print("SYNTHETIC_RESULT_REPAIR_OK")
    print(f"{RECEIPT_PREFIX}{json.dumps(payload, sort_keys=True, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
