"""Draft the canonical Maintenance_HQ boot prompt without sending it."""
from __future__ import annotations

import sys

from draft_department_boot import DEPARTMENTS, build_prompt, run_engine_once


if __name__ == "__main__":
    department = DEPARTMENTS["logistics"]
    forwarded_args = [
        sys.argv[0],
        department.chat_title,
        "--text",
        build_prompt(department),
    ]
    result, _ = run_engine_once(forwarded_args)
    raise SystemExit(result)
