"""Read-only clipboard probe for the ChatGPT Classic composer group.

Reuses the production composer Group selector, clicks the same safe text-surface point,
and tests global Ctrl+A/Ctrl+C. The script preserves the user's clipboard, never writes
text, and never submits.
"""

from __future__ import annotations

import argparse
import time

from pywinauto.keyboard import send_keys

import open_department_chat_group as production_group
from lifeos_dashboard import automation_write_verification_runtime as _write_verification_runtime
from open_department_chat import (
    APP_TITLE,
    CLIPBOARD_SENTINEL,
    Target,
    clipboard_get_text,
    clipboard_set_text,
    current_document_title,
    get_chatgpt_window,
    open_exact_chat,
)

GENERIC_LOADING_TITLE = "ChatGPT"
DEFAULT_DESTINATION_TIMEOUT_SECONDS = 15.0
DESTINATION_POLL_SECONDS = 0.5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe clipboard reads from the production Group-based composer shell."
    )
    parser.add_argument("chat_title", help="Exact active chat title, such as Wellness HQ")
    parser.add_argument("--project", default="Life OS")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_DESTINATION_TIMEOUT_SECONDS,
        help="Seconds to wait after one bounded loading-state re-navigation",
    )
    return parser.parse_args()


def wait_for_clipboard_change(timeout_seconds: float = 1.5) -> str:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        value = clipboard_get_text()
        if value != CLIPBOARD_SENTINEL:
            return value
        time.sleep(0.05)
    return ""


def wait_for_exact_destination(window, expected_title: str, timeout_seconds: float) -> str:
    started = time.monotonic()
    last_title: str | None = None

    while True:
        elapsed = time.monotonic() - started
        if elapsed >= timeout_seconds:
            observed = current_document_title(window)
            print(
                f"WAIT EXPIRED after {elapsed:.1f}s. Last observed title: {observed!r}.",
                flush=True,
            )
            return ""

        try:
            observed = current_document_title(window)
        except Exception as exc:
            observed = f"<UIA read error: {exc}>"

        if observed != last_title:
            print(f"  {elapsed:4.1f}s observed document: {observed!r}", flush=True)
            last_title = observed

        if observed == expected_title:
            return observed

        time.sleep(DESTINATION_POLL_SECONDS)


def verify_or_recover_destination(window, target: Target, timeout_seconds: float) -> bool:
    observed = current_document_title(window)
    if observed == target.document_title:
        return True

    if observed != GENERIC_LOADING_TITLE:
        print(
            "STOPPED: active destination mismatch. "
            f"Expected {target.document_title!r}, observed {observed!r}.",
            flush=True,
        )
        return False

    print(
        "BOUNDED RETRY: active document is the generic ChatGPT loading state. "
        "Re-invoking the exact department link once.",
        flush=True,
    )
    try:
        invoked = open_exact_chat(window, target)
    except Exception as exc:
        print(f"STOPPED: exact re-navigation failed: {exc}", flush=True)
        return False

    print(f"Navigation invoked: {invoked}. Waiting up to {timeout_seconds:.1f}s.", flush=True)
    verified = wait_for_exact_destination(
        window,
        expected_title=target.document_title,
        timeout_seconds=timeout_seconds,
    )
    if not verified:
        print(
            "STOPPED: destination did not become exact after the bounded wait. "
            "No composer inspection occurred.",
            flush=True,
        )
        return False

    print(f"Verified active document after retry: {verified}", flush=True)
    return True


def find_composer_group(window):
    """Use the exact production selector installed by the write-verification runtime."""
    return production_group.find_composer_group(window)


def main() -> int:
    args = parse_args()
    target = Target(chat_title=args.chat_title, project_title=args.project)
    original_clipboard = clipboard_get_text()

    try:
        print(f"Finding window: {APP_TITLE}", flush=True)
        window = get_chatgpt_window()
        if not verify_or_recover_destination(window, target, args.timeout):
            return 1

        group = find_composer_group(window)
        rect = group.rectangle()
        print(
            "Composer group located: "
            f"rect=({rect.left},{rect.top},{rect.right},{rect.bottom})",
            flush=True,
        )

        x = rect.left + max(80, rect.width() // 2)
        y = max(rect.top + 30, rect.bottom - 70)
        group.click_input(coords=(x - rect.left, y - rect.top))
        time.sleep(0.20)

        clipboard_set_text(CLIPBOARD_SENTINEL)
        send_keys("^a", pause=0.10)
        send_keys("^c", pause=0.10)
        copied = wait_for_clipboard_change()
        send_keys("{RIGHT}", pause=0.05)

        print(f"Global click/select/copy: copied {len(copied)} characters", flush=True)
        if not copied:
            print("RESULT: composer group focus did not yield clipboard text.", flush=True)
            return 2

        print("RESULT: composer group clipboard read succeeded.", flush=True)
        return 0
    finally:
        try:
            send_keys("{RIGHT}", pause=0.05)
        except Exception:
            pass
        clipboard_set_text(original_clipboard)


if __name__ == "__main__":
    raise SystemExit(main())
