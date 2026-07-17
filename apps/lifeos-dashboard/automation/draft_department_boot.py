"""Draft or explicitly submit canonical LifeOS department boot prompts."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

from open_department_chat import main


@dataclass(frozen=True)
class Department:
    key: str
    chat_title: str
    role_title: str
    project_folder: str
    report_name: str
    related_files_note: str


DEPARTMENTS: dict[str, Department] = {
    "logistics": Department(
        key="logistics",
        chat_title="Logistics HQ",
        role_title="Logistics HQ",
        project_folder="projects/life-logistics",
        report_name="Logistics",
        related_files_note=(
            "Read related Main Assistant, Finance, Housing, Recovery Logistics, "
            "Wellness, or Engineering files only when the handoff or task requires "
            "cross-project coordination."
        ),
    ),
    "engineering": Department(
        key="engineering",
        chat_title="Engineering HQ",
        role_title="Engineering HQ",
        project_folder="projects/engineering",
        report_name="Engineering",
        related_files_note=(
            "Read related Main Assistant, Logistics, Business, Finance, or "
            "infrastructure files only when the handoff or task requires "
            "cross-project coordination."
        ),
    ),
    "main": Department(
        key="main",
        chat_title="Main Assistant HQ",
        role_title="Main Assistant HQ",
        project_folder="projects/main-assistant",
        report_name="Main Assistant",
        related_files_note=(
            "Read related departmental files only when the handoff or task requires "
            "cross-project coordination."
        ),
    ),
    "finance": Department(
        key="finance",
        chat_title="Finance HQ",
        role_title="Finance HQ",
        project_folder="projects/finance-benefits",
        report_name="Finance",
        related_files_note=(
            "Read related Main Assistant, Logistics, Housing, Business, or "
            "Wellness files only when the handoff or task requires cross-project coordination."
        ),
    ),
    "business": Department(
        key="business",
        chat_title="Business HQ",
        role_title="Business HQ",
        project_folder="projects/business-development",
        report_name="Business",
        related_files_note=(
            "Read related Main Assistant, Finance, Engineering, Office Leaks, or "
            "Logistics files only when the handoff or task requires cross-project coordination."
        ),
    ),
    "office-leaks": Department(
        key="office-leaks",
        chat_title="Office Leaks HQ",
        role_title="Office Leaks HQ",
        project_folder="projects/office-leaks-consulting",
        report_name="Office Leaks",
        related_files_note=(
            "Read related Business, Engineering, Finance, or Logistics files only "
            "when the handoff or task requires cross-project coordination."
        ),
    ),
    "wellness": Department(
        key="wellness",
        chat_title="Wellness HQ",
        role_title="Wellness HQ",
        project_folder="projects/wellness",
        report_name="Wellness",
        related_files_note=(
            "Read Health Medical HQ files only when a matter involves medical care, "
            "symptoms, appointments, diagnoses, treatment, or medication. Read Recovery "
            "Logistics files only when wellness work overlaps recovery stability or daily anchors."
        ),
    ),
}


def build_prompt(department: Department) -> str:
    folder = department.project_folder
    return f"""@GitHub boot and sync.

You are {department.role_title}.

Repository:
recoveryrob83-lab/Penny-Long-Term-Memory

Follow the canonical global boot sequence beginning with:

memory/STARTUP_BOOT.md

Read all required global boot files in order.

Then continue into this department's project boot files exactly as specified by the global routing instructions:

- {folder}/SESSION_HANDOFF.md
- {folder}/DEPARTMENT_IDENTITY.md
- {folder}/README.md
- {folder}/status.md
- {folder}/open_loops.md

Read the Advisory Index when advisory routing or cross-department status is relevant. Read this department's advisory board when advisories need to be created, consumed, verified, or reconciled.

{department.related_files_note}

Operate read-only during boot unless I explicitly authorize a write or external action.

After boot, provide a concise {department.report_name} synchronization report including:

1. Current operational status
2. Active priorities and open loops
3. Pending advisories or cross-department dependencies
4. Any stale, conflicting, or missing durable-memory state
5. The single best next action
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Place a canonical department boot prompt in the exact LifeOS chat. "
            "Draft-only unless --send is explicitly supplied."
        )
    )
    parser.add_argument("department", choices=sorted(DEPARTMENTS))
    parser.add_argument(
        "--send",
        action="store_true",
        help=(
            "Submit after destination, readiness, and write verification. "
            "The literal @GitHub text may rely on connector context already being active."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    department = DEPARTMENTS[args.department]

    forwarded_args = [
        sys.argv[0],
        department.chat_title,
        "--text",
        build_prompt(department),
    ]

    if args.send:
        forwarded_args.extend(["--send", "--confirm-send", "SEND"])
        print(
            "SEND MODE: connector resolution is not verified; this relies on GitHub "
            "remaining active in the target chat context."
        )

    sys.argv = forwarded_args
    raise SystemExit(main())
