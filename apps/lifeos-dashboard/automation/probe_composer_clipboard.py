"""Safely diagnose clipboard reads from the ChatGPT Classic composer.

This script never writes, clears, replaces, or sends composer text. It preserves the
user's clipboard, tests several focus/copy paths, prints copied character counts only,
and collapses any selection before exiting.
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
    find_visible_composer,
    get_chatgpt_window,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe safe clipboard-copy methods for the active ChatGPT composer."
    )
    parser.add_argument("chat_title", help="Exact active chat title, such as Wellness HQ")
    parser.add_argument("--project", default="Life OS")
    return parser.parse_args()


def wait_for_clipboard_change(timeout_seconds: float = 1.0) -> str:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        value = clipboard_get_text()
        if value != CLIPBOARD_SENTINEL:
            return value
        time.sleep(0.05)
    return ""


def run_probe(label: str, composer, action) -> int:
    clipboard_set_text(CLIPBOARD_SENTINEL)
    action()
    copied = wait_for_clipboard_change()
    try:
        send_keys("{RIGHT}", pause=0.05)
    except Exception:
        pass
    print(f"{label}: copied {len(copied)} characters")
    return len(copied)


def main() -> int:
    args = parse_args()
    target = Target(chat_title=args.chat_title, project_title=args.project)
    original_clipboard = clipboard_get_text()

    try:
        print(f"Finding window: {APP_TITLE}")
        window = get_chatgpt_window()
        observed = current_document_title(window)
        if observed != target.document_title:
            print(
                "STOPPED: active destination mismatch. "
                f"Expected {target.document_title!r}, observed {observed!r}."
            )
            return 1

        composer = find_visible_composer(window)
        if not composer.is_visible() or not composer.is_enabled():
            print("STOPPED: composer is not visible and enabled.")
            return 1

        results = []
        results.append(
            run_probe(
                "A wrapper focus + wrapper keys",
                composer,
                lambda: (
                    composer.set_focus(),
                    composer.type_keys("^a", set_foreground=True),
                    composer.type_keys("^c", set_foreground=True),
                ),
            )
        )
        results.append(
            run_probe(
                "B click + wrapper keys",
                composer,
                lambda: (
                    composer.click_input(),
                    composer.type_keys("^a", set_foreground=True),
                    composer.type_keys("^c", set_foreground=True),
                ),
            )
        )
        results.append(
            run_probe(
                "C click + global keys",
                composer,
                lambda: (
                    composer.click_input(),
                    send_keys("^a", pause=0.10),
                    send_keys("^c", pause=0.10),
                ),
            )
        )

        if max(results, default=0) == 0:
            print("RESULT: all safe copy methods returned zero characters.")
            return 2

        best = results.index(max(results)) + 1
        print(f"RESULT: method {best} copied the largest composer payload.")
        return 0
    finally:
        try:
            send_keys("{RIGHT}", pause=0.05)
        except Exception:
            pass
        clipboard_set_text(original_clipboard)


if __name__ == "__main__":
    raise SystemExit(main())
