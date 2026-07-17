"""Read-only clipboard probe for the ChatGPT Classic composer group.

Anchors on the visible Send prompt button, locates the enclosing bottom composer Group,
clicks a safe text-surface point, and tests global Ctrl+A/Ctrl+C. The script preserves the
user's clipboard, never writes text, and never submits.
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
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe clipboard reads from the Group-based ChatGPT composer shell."
    )
    parser.add_argument("chat_title", help="Exact active chat title, such as Wellness HQ")
    parser.add_argument("--project", default="Life OS")
    return parser.parse_args()


def wait_for_clipboard_change(timeout_seconds: float = 1.5) -> str:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        value = clipboard_get_text()
        if value != CLIPBOARD_SENTINEL:
            return value
        time.sleep(0.05)
    return ""


def find_composer_group(window):
    submit = window.child_window(
        auto_id="composer-submit-button", control_type="Button"
    )
    if not submit.exists(timeout=2):
        raise RuntimeError("Visible Send prompt button was not found.")

    submit_wrapper = submit.wrapper_object()
    submit_rect = submit_wrapper.rectangle()
    candidates = []

    for control in window.descendants():
        if control.element_info.control_type != "Group":
            continue
        rect = control.rectangle()
        if not control.is_visible() or not control.is_enabled():
            continue
        if rect.left <= submit_rect.left and rect.right >= submit_rect.right:
            if rect.top <= submit_rect.top and rect.bottom >= submit_rect.bottom:
                candidates.append(control)

    if not candidates:
        raise RuntimeError("No visible Group enclosing the Send prompt button was found.")

    return min(candidates, key=lambda control: control.rectangle().width() * control.rectangle().height())


def main() -> int:
    args = parse_args()
    target = Target(chat_title=args.chat_title, project_title=args.project)
    original_clipboard = clipboard_get_text()

    try:
        print(f"Finding window: {APP_TITLE}", flush=True)
        window = get_chatgpt_window()
        observed = current_document_title(window)
        if observed != target.document_title:
            print(
                "STOPPED: active destination mismatch. "
                f"Expected {target.document_title!r}, observed {observed!r}.",
                flush=True,
            )
            return 1

        group = find_composer_group(window)
        rect = group.rectangle()
        print(
            "Composer group located: "
            f"rect=({rect.left},{rect.top},{rect.right},{rect.bottom})",
            flush=True,
        )

        # Click inside the text surface, safely above the bottom-row buttons.
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
