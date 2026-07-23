"""Diagnose normalized differences between a canonical department prompt and composer copy.

Read-only. This script never writes, clears, replaces, or sends composer text. It verifies the
exact active department destination, reads the Group-based composer through the production copy
path, and prints compact diff statistics plus short escaped mismatch windows.
"""

from __future__ import annotations

import argparse
import difflib

from draft_department_boot import DEPARTMENTS, build_prompt
from open_department_chat_group import (
    APP_TITLE,
    Target,
    copy_group_text,
    current_document_title,
    find_composer_group,
    get_chatgpt_window,
    normalize_text,
)

WINDOW_RADIUS = 32
MAX_MISMATCHES = 8


def escaped_window(value: str, start: int, end: int) -> str:
    left = max(0, start - WINDOW_RADIUS)
    right = min(len(value), end + WINDOW_RADIUS)
    return value[left:right].encode("unicode_escape").decode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only canonical prompt diff diagnostic")
    parser.add_argument("department", choices=sorted(DEPARTMENTS))
    args = parser.parse_args()

    department = DEPARTMENTS[args.department]
    target = Target(chat_title=department.chat_title, project_title="LifeOS")
    expected = normalize_text(build_prompt(department))

    print(f"Finding window: {APP_TITLE}", flush=True)
    window = get_chatgpt_window()
    observed_title = current_document_title(window)
    if observed_title != target.document_title:
        print(
            "STOPPED: active destination mismatch. "
            f"Expected {target.document_title!r}, observed {observed_title!r}.",
            flush=True,
        )
        return 1

    group = find_composer_group(window)
    observed = normalize_text(copy_group_text(group))
    print(f"Expected normalized length: {len(expected)}", flush=True)
    print(f"Observed normalized length: {len(observed)}", flush=True)

    matcher = difflib.SequenceMatcher(a=expected, b=observed, autojunk=False)
    counts = {"equal": 0, "replace": 0, "delete": 0, "insert": 0}
    mismatches = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        counts[tag] += max(i2 - i1, j2 - j1)
        if tag != "equal" and len(mismatches) < MAX_MISMATCHES:
            mismatches.append((tag, i1, i2, j1, j2))

    ratio = matcher.ratio()
    print(f"Similarity ratio: {ratio:.6f}", flush=True)
    print(
        "Opcode totals: "
        f"equal={counts['equal']} replace={counts['replace']} "
        f"delete={counts['delete']} insert={counts['insert']}",
        flush=True,
    )

    if not mismatches:
        print("RESULT: normalized payloads are identical.", flush=True)
        return 0

    print(f"First {len(mismatches)} mismatch block(s):", flush=True)
    for index, (tag, i1, i2, j1, j2) in enumerate(mismatches, start=1):
        print(
            f"{index}. {tag} expected[{i1}:{i2}] observed[{j1}:{j2}]",
            flush=True,
        )
        print(f"   expected: {escaped_window(expected, i1, i2)}", flush=True)
        print(f"   observed: {escaped_window(observed, j1, j2)}", flush=True)

    print("RESULT: diff captured. Nothing was modified or sent.", flush=True)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
