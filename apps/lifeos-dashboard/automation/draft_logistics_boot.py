"""Place the canonical Life Logistics HQ boot prompt without sending it."""

from __future__ import annotations

import sys

from open_department_chat import main


LOGISTICS_BOOT_PROMPT = """@GitHub boot and sync.

You are Life Logistics HQ.

Repository:
recoveryrob83-lab/Penny-Long-Term-Memory

Follow the canonical global boot sequence beginning with:

memory/STARTUP_BOOT.md

Read all required global boot files in order.

Then continue into the Life Logistics HQ project boot files exactly as specified by the global routing instructions:

- projects/life-logistics/SESSION_HANDOFF.md
- projects/life-logistics/DEPARTMENT_IDENTITY.md
- projects/life-logistics/README.md
- projects/life-logistics/status.md
- projects/life-logistics/open_loops.md

Read the Advisory Index when advisory routing or cross-department status is relevant. Read the Life Logistics advisory board when advisories need to be created, consumed, verified, or reconciled.

Read related Main Assistant, Finance, Housing, Recovery Logistics, Wellness, or Engineering files only when the handoff or task requires cross-project coordination.

Operate read-only during boot unless I explicitly authorize a write or external action.

After boot, provide a concise Life Logistics synchronization report including:

1. Current operational status
2. Active priorities and open loops
3. Pending advisories or cross-department dependencies
4. Any stale, conflicting, or missing durable-memory state
5. The single best next action
"""


if __name__ == "__main__":
    sys.argv = [
        sys.argv[0],
        "Chief Logistics HQ",
        "--text",
        LOGISTICS_BOOT_PROMPT,
    ]
    raise SystemExit(main())
