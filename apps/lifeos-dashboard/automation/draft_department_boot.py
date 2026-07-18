"""Draft or explicitly submit canonical LifeOS HQ boot prompts."""
from __future__ import annotations

import argparse
import contextlib
import io
import sys
from dataclasses import dataclass

from open_department_chat_group_verified import main

GENERIC_LOADING_FAILURE = "observed 'ChatGPT'."


@dataclass(frozen=True)
class Department:
    key: str
    chat_title: str
    role_title: str
    project_folder: str | None
    report_name: str
    related_files_note: str


DEPARTMENTS: dict[str, Department] = {
    "hub": Department(
        key="hub",
        chat_title="LifeOS HQ",
        role_title="LifeOS HQ, the shared LifeOS meeting room",
        project_folder=None,
        report_name="LifeOS HQ",
        related_files_note=(
            "Read department project files only when current coordination, routing, or a named "
            "cross-department issue requires them. Do not absorb specialist department judgment."
        ),
    ),
    "logistics": Department(
        key="logistics",
        chat_title="Life OS Maintenance HQ",
        role_title="Life OS Maintenance HQ",
        project_folder="projects/life-logistics-hq",
        report_name="Life OS Maintenance",
        related_files_note=(
            "Read related Chief of Staff, Finance, Housing, Recovery Logistics, "
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
            "Read related Chief of Staff, Life OS Maintenance, Business, Finance, or "
            "infrastructure files only when the handoff or task requires "
            "cross-project coordination."
        ),
    ),
    "main": Department(
        key="main",
        chat_title="Chief of Staff HQ",
        role_title="Chief of Staff HQ",
        project_folder="projects/main-assistant",
        report_name="Chief of Staff",
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
            "Read related Chief of Staff, Life OS Maintenance, Housing, Business, or "
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
            "Read related Chief of Staff, Finance, Engineering, Office Leaks, or "
            "Life OS Maintenance files only when the handoff or task requires cross-project coordination."
        ),
    ),
    "office-leaks": Department(
        key="office-leaks",
        chat_title="Office Leaks HQ",
        role_title="Office Leaks HQ",
        project_folder="projects/office-leaks-consulting",
        report_name="Office Leaks",
        related_files_note=(
            "Read related Business, Engineering, Finance, or Life OS Maintenance files only "
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
    if department.project_folder is None:
        project_boot = """This is the shared meeting room rather than a specialist department. After the global boot files, read current shared coordination state from:

- memory/01_SESSION_HANDOFF.md
- memory/04_ACTIVE_PROJECTS.md
- memory/05_OPEN_LOOPS.md
- coordination/ADVISORY_INDEX.md when advisory routing or cross-department status is relevant

Use memory/HQ_NAMING_STANDARD.md as the canonical headquarters naming source. Chief of Staff HQ chairs this room, departments retain ownership of their work, and Rob remains the final authority."""
    else:
        folder = department.project_folder
        project_boot = f"""Then continue into this department's project boot files exactly as specified by the global routing instructions:

- {folder}/SESSION_HANDOFF.md
- {folder}/DEPARTMENT_IDENTITY.md
- {folder}/README.md
- {folder}/status.md when it exists or is maintained
- {folder}/open_loops.md

Read the Advisory Index when advisory routing or cross-department status is relevant. Read this department's advisory board when advisories need to be created, consumed, verified, or reconciled."""

    return f"""@GitHub boot and sync.

You are {department.role_title}.

Repository:
recoveryrob83-lab/Penny-Long-Term-Memory

Follow the canonical global boot sequence beginning with:

memory/STARTUP_BOOT.md

Read all required global boot files in order.

{project_boot}

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
            "Place a canonical LifeOS HQ boot prompt in the exact chat. "
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
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the selected canonical prompt and exit without opening ChatGPT.",
    )
    return parser.parse_args()


def run_engine_once(forwarded_args: list[str]) -> tuple[int, str]:
    """Run the Group-based engine once while preserving stderr for diagnostics."""
    captured_stderr = io.StringIO()
    sys.argv = forwarded_args
    with contextlib.redirect_stderr(captured_stderr):
        result = main()
    stderr_text = captured_stderr.getvalue()
    if stderr_text:
        print(stderr_text, file=sys.stderr, end="")
    return result, stderr_text


if __name__ == "__main__":
    args = parse_args()
    department = DEPARTMENTS[args.department]
    prompt = build_prompt(department)

    if args.print_prompt:
        print(prompt, end="")
        raise SystemExit(0)

    forwarded_args = [
        sys.argv[0],
        department.chat_title,
        "--text",
        prompt,
    ]

    if args.send:
        forwarded_args.extend(["--send", "--confirm-send", "SEND"])
        print(
            "SEND MODE: connector resolution is not verified; this relies on GitHub "
            "remaining active in the target chat context."
        )

    result, _ = run_engine_once(forwarded_args)
    raise SystemExit(result)
