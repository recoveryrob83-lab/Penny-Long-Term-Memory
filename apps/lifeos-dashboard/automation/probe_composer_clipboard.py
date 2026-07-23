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
    AutomationStopped,
    Target,
    clipboard_get_text,
    clipboard_set_text,
    current_document_title,
    get_chatgpt_window,
    open_exact_chat,
    wait_for_composer_ready,
)


GENERIC_LOADING_TITLE = "ChatGPT"
DEFAULT_DESTINATION_TIMEOUT_SECONDS = 15.0
DEFAULT_READY_TIMEOUT_SECONDS = 20.0
DEFAULT_STABLE_SECONDS = 1.0
DESTINATION_POLL_SECONDS = 0.5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe safe clipboard-copy methods for the active ChatGPT composer."
    )
    parser.add_argument("chat_title", help="Exact active chat title, such as Wellness HQ")
    parser.add_argument("--project", default="LifeOS")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_DESTINATION_TIMEOUT_SECONDS,
        help="Seconds to wait after the one bounded loading-state re-navigation",
    )
    parser.add_argument(
        "--ready-timeout",
        type=float,
        default=DEFAULT_READY_TIMEOUT_SECONDS,
        help="Seconds to wait for a stable, visible, enabled composer",
    )
    parser.add_argument(
        "--stable-seconds",
        type=float,
        default=DEFAULT_STABLE_SECONDS,
        help="Continuous seconds the composer must remain ready before probing",
    )
    return parser.parse_args()


def wait_for_clipboard_change(timeout_seconds: float = 1.0) -> str:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
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
    print(f"{label}: copied {len(copied)} characters", flush=True)
    return len(copied)


def wait_for_exact_destination(window, expected_title: str, timeout_seconds: float) -> str:
    """Poll visibly for the exact destination and report elapsed time and title changes."""
    started = time.monotonic()
    last_title: str | None = None

    while True:
        elapsed = time.monotonic() - started
        if elapsed >= timeout_seconds:
            try:
                observed = current_document_title(window)
            except Exception as exc:
                observed = f"<UIA read error: {exc}>"
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
    """Verify the target, allowing one exact re-navigation from the generic loading title."""
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


def main() -> int:
    args = parse_args()
    target = Target(chat_title=args.chat_title, project_title=args.project)
    original_clipboard = clipboard_get_text()

    try:
        print(f"Finding window: {APP_TITLE}", flush=True)
        window = get_chatgpt_window()
        if not verify_or_recover_destination(window, target, args.timeout):
            return 1

        print(
            f"Waiting up to {args.ready_timeout:.1f}s for a stable composer...",
            flush=True,
        )
        try:
            composer = wait_for_composer_ready(
                window,
                expected_document_title=target.document_title,
                timeout_seconds=args.ready_timeout,
                stable_seconds=args.stable_seconds,
            )
        except AutomationStopped as exc:
            print(f"STOPPED: {exc}", flush=True)
            return 1

        print("Composer readiness verified. Beginning read-only copy probe.", flush=True)

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
            print("RESULT: all safe copy methods returned zero characters.", flush=True)
            return 2

        best = results.index(max(results)) + 1
        print(f"RESULT: method {best} copied the largest composer payload.", flush=True)
        return 0
    finally:
        try:
            send_keys("{RIGHT}", pause=0.05)
        except Exception:
            pass
        clipboard_set_text(original_clipboard)


if __name__ == "__main__":
    raise SystemExit(main())
