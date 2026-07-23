"""Backward-compatible launcher for the canonical Maintenance_HQ boot draft."""
from __future__ import annotations

import sys

from draft_department_boot import main


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "logistics", *sys.argv[1:]]
    raise SystemExit(main())
