"""Safely test writing to the Group-based ChatGPT Classic composer.

The probe permits one bounded loading-state re-navigation, locates the composer Group by
its Send button, refuses to overwrite existing text, pastes a harmless marker into an
empty composer, verifies the result through clipboard readback, restores the user's
clipboard, and never submits.
"""

from __future__ import annotations

import argparse
import time

from pywinauto.keyboard import send_keys

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
from probe_composer_group_clipboard import find_composer_group

GENERIC_LOADING_TITLE = "ChatGPT"
DEFAULT_TIMEOUT_SECONDS = 15.0
POLL_SECONDS = 0.5
MARKER = "[GROUP COMPOSER WRITE TEST - DO NOT SEND]"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely verify writing to the Group-based ChatGPT composer shell."
    )
    parser.add_argument("chat_title", help="Exact chat title, such as Wellness HQ")
    parser.add_argument("--project", default="Life OS")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    return parser.parse_args()


def wait_for_exact_destination(window, expected_title: str, timeout_seconds: float) -> bool:
    started = time.monotonic()
    last_title: str | None = None
    while time.monotonic() - started < timeout_seconds:
        elapsed = time.monotonic() - started
        try:
            observed = current_document_title(window)
        except Exception as exc:
            observed = f"<UIA read error: {exc}>"
        if observed != last_title:
            print(f"  {elapsed:4.1f}s observed document: {observed!r}", flush=True)
            last_title = observed
        if observed == expected_title:
            return True
        time.sleep(POLL_SECONDS)
    return False


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
        "BOUNDED RETRY: generic ChatGPT loading state detected. "
        "Re-invoking the exact department link once.",
        flush=True,
    )
    try:
        invoked = open_exact_chat(window, target)
    except Exception as exc:
        print(f"STOPPED: exact re-navigation failed: {exc}", flush=True)
        return False

    print(f"Navigation invoked: {invoked}. Waiting up to {timeout_seconds:.1f}s.", flush=True)
    if not wait_for_exact_destination(window, target.document_title, timeout_seconds):
        print("STOPPED: destination did not become exact after bounded wait.", flush=True)
        return False
    print(f"Verified active document after retry: {target.document_title}", flush=True)
    return True


def focus_group_text_surface(group) -> None:
    rect = group.rectangle()
    x = rect.left + max(80, rect.width() // 2)
    y = max(rect.top + 30, rect.bottom - 70)
    group.click_input(coords=(x - rect.left, y - rect.top))
    time.sleep(0.20)


def copy_focused_text(timeout_seconds: float = 1.5) -> str:
    clipboard_set_text(CLIPBOARD_SENTINEL)
    send_keys("^a", pause=0.10)
    send_keys("^c", pause=0.10)
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        value = clipboard_get_text()
        if value != CLIPBOARD_SENTINEL:
            send_keys("{RIGHT}", pause=0.05)
            return value
        time.sleep(0.05)
    send_keys("{RIGHT}", pause=0.05)
    return ""


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
        focus_group_text_surface(group)
        existing = copy_focused_text()
        if existing.strip():
            print(
                f"STOPPED: composer already contains {len(existing)} characters. "
                "Existing draft was preserved.",
                flush=True,
            )
            return 1

        clipboard_set_text(MARKER)
        focus_group_text_surface(group)
        send_keys("^v", pause=0.10)
        time.sleep(0.30)

        focus_group_text_surface(group)
        observed = copy_focused_text()
        if observed.strip() != MARKER:
            print(
                "STOPPED: Group composer write verification failed. "
                f"Expected {len(MARKER)} characters, copied {len(observed)}. Nothing was sent.",
                flush=True,
            )
            return 2

        print(
            f"RESULT: Group composer write succeeded and verified ({len(observed)} characters). "
            "Nothing was sent.",
            flush=True,
        )
        return 0
    finally:
        try:
            send_keys("{RIGHT}", pause=0.05)
        except Exception:
            pass
        clipboard_set_text(original_clipboard)


if __name__ == "__main__":
    raise SystemExit(main())
