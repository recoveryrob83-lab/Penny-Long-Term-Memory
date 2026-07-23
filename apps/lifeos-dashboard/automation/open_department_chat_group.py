"""Safely open a LifeOS department chat and use the modern Group-based composer.

Windows-only automation using pywinauto and the ChatGPT Classic UI Automation tree.
Draft-only by default. Nothing is sent unless --send and --confirm-send SEND are both
provided. Existing composer text is preserved unless --replace-existing is explicit.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass

import win32clipboard
from pywinauto import Desktop
from pywinauto.base_wrapper import BaseWrapper
from pywinauto.keyboard import send_keys

APP_TITLE = "ChatGPT Classic"
DEFAULT_PROJECT = "LifeOS"
DEFAULT_TIMEOUT_SECONDS = 15.0
DEFAULT_READY_TIMEOUT_SECONDS = 20.0
DEFAULT_STABLE_SECONDS = 1.0
DEFAULT_WRITE_TIMEOUT_SECONDS = 8.0
POLL_SECONDS = 0.25
VERIFY_EDGE_CHARS = 120
CLIPBOARD_SENTINEL = "__LIFEOS_COMPOSER_COPY_SENTINEL__"
GENERIC_LOADING_TITLE = "ChatGPT"


class AutomationStopped(RuntimeError):
    """Raised when a safety check fails and automation must stop."""


@dataclass(frozen=True)
class Target:
    chat_title: str
    project_title: str

    @property
    def link_title(self) -> str:
        return f"{self.chat_title}, chat in project {self.project_title}"

    @property
    def document_title(self) -> str:
        return f"{self.project_title} - {self.chat_title}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Open an exact LifeOS department chat, verify the destination, wait for "
            "a stable Group composer, and place text. Draft-only by default."
        )
    )
    parser.add_argument("chat_title", help="Exact sidebar chat title")
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--text", default="[AUTOMATION TEST - DO NOT SEND]")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--ready-timeout", type=float, default=DEFAULT_READY_TIMEOUT_SECONDS)
    parser.add_argument("--stable-seconds", type=float, default=DEFAULT_STABLE_SECONDS)
    parser.add_argument("--write-timeout", type=float, default=DEFAULT_WRITE_TIMEOUT_SECONDS)
    parser.add_argument("--replace-existing", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--confirm-send", default="")
    return parser.parse_args()


def get_chatgpt_window() -> BaseWrapper:
    window = Desktop(backend="uia").window(title=APP_TITLE)
    if not window.exists(timeout=2):
        raise AutomationStopped(f"ChatGPT window not found: {APP_TITLE!r}")
    return window


def visible_document_titles(window: BaseWrapper) -> list[str]:
    titles: list[str] = []
    for control in window.descendants():
        if control.element_info.control_type != "Document":
            continue
        if control.rectangle().top < 0:
            continue
        text = control.window_text().strip()
        if text:
            titles.append(text)
    return titles


def current_document_title(window: BaseWrapper) -> str:
    titles = visible_document_titles(window)
    return titles[0] if titles else ""


def open_exact_chat(window: BaseWrapper, target: Target) -> bool:
    if current_document_title(window) == target.document_title:
        return False
    link = window.child_window(title=target.link_title, control_type="Hyperlink")
    if not link.exists(timeout=2):
        raise AutomationStopped(
            f"Exact chat link not found in the accessible sidebar: {target.link_title!r}"
        )
    window.set_focus()
    link.invoke()
    return True


def wait_for_exact_destination(window: BaseWrapper, target: Target, timeout_seconds: float) -> str:
    observed = current_document_title(window)
    if observed == target.document_title:
        return observed

    if observed == GENERIC_LOADING_TITLE:
        print(
            "   BOUNDED RETRY: generic ChatGPT loading state detected. "
            "Re-invoking the exact department link once."
        )
        open_exact_chat(window, target)

    deadline = time.monotonic() + timeout_seconds
    last_title = observed
    while time.monotonic() < deadline:
        observed = current_document_title(window)
        last_title = observed
        if observed == target.document_title:
            return observed
        if observed not in ("", GENERIC_LOADING_TITLE):
            raise AutomationStopped(
                f"Destination mismatch. Expected {target.document_title!r}, observed {observed!r}."
            )
        time.sleep(POLL_SECONDS)

    raise AutomationStopped(
        f"Destination verification failed. Expected {target.document_title!r}, observed {last_title!r}."
    )


def clipboard_get_text() -> str:
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            return str(win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT))
        return ""
    finally:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass


def clipboard_set_text(value: str) -> None:
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(value, win32clipboard.CF_UNICODETEXT)
    finally:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass


def find_composer_group(window: BaseWrapper) -> BaseWrapper:
    anchor = window.child_window(auto_id="composer-plus-btn", control_type="Button")
    if not anchor.exists(timeout=2):
        raise AutomationStopped("Persistent composer plus button was not found.")
    anchor_wrapper = anchor.wrapper_object()
    anchor_rect = anchor_wrapper.rectangle()
    candidates: list[BaseWrapper] = []
    for control in window.descendants():
        if control.element_info.control_type != "Group":
            continue
        rect = control.rectangle()
        if not control.is_visible() or not control.is_enabled():
            continue
        if rect.left <= anchor_rect.left <= rect.right and rect.top <= anchor_rect.top <= rect.bottom:
            candidates.append(control)
    if not candidates:
        raise AutomationStopped("No visible Group enclosing the composer plus button was found.")
    return min(candidates, key=lambda c: c.rectangle().width() * c.rectangle().height())


def group_signature(group: BaseWrapper) -> tuple[int, int, int, int]:
    rect = group.rectangle()
    return (rect.left, rect.top, rect.right, rect.bottom)


def wait_for_composer_ready(
    window: BaseWrapper,
    expected_document_title: str,
    timeout_seconds: float,
    stable_seconds: float,
) -> BaseWrapper:
    deadline = time.monotonic() + timeout_seconds
    stable_since: float | None = None
    last_signature: tuple[int, int, int, int] | None = None
    last_reason = "composer not yet observed"

    while time.monotonic() < deadline:
        if current_document_title(window) != expected_document_title:
            stable_since = None
            last_signature = None
            last_reason = "active document changed during readiness wait"
            time.sleep(POLL_SECONDS)
            continue
        try:
            group = find_composer_group(window)
            signature = group_signature(group)
            visible = group.is_visible()
            enabled = group.is_enabled()
        except Exception as exc:
            stable_since = None
            last_signature = None
            last_reason = f"composer unavailable: {exc}"
            time.sleep(POLL_SECONDS)
            continue
        if not visible or not enabled:
            stable_since = None
            last_signature = None
            last_reason = f"composer visible={visible}, enabled={enabled}"
            time.sleep(POLL_SECONDS)
            continue
        if signature != last_signature:
            last_signature = signature
            stable_since = time.monotonic()
            last_reason = "composer geometry is still settling"
            time.sleep(POLL_SECONDS)
            continue
        if stable_since is None:
            stable_since = time.monotonic()
        if time.monotonic() - stable_since >= stable_seconds:
            return group
        last_reason = "composer has not remained stable long enough"
        time.sleep(POLL_SECONDS)

    raise AutomationStopped(
        f"Composer readiness timed out after {timeout_seconds:.1f}s. Last state: {last_reason}."
    )


def focus_group_text_surface(group: BaseWrapper) -> None:
    rect = group.rectangle()
    x = rect.left + max(80, rect.width() // 2)
    y = max(rect.top + 30, rect.bottom - 70)
    group.click_input(coords=(x - rect.left, y - rect.top))
    time.sleep(0.20)


def copy_group_text(group: BaseWrapper, timeout_seconds: float = 1.5) -> str:
    original_clipboard = clipboard_get_text()
    try:
        focus_group_text_surface(group)
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
    finally:
        clipboard_set_text(original_clipboard)


def normalize_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = value.replace("\u00a0", " ")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    return value.strip()


def text_matches_expected(observed: str, expected: str) -> bool:
    observed_norm = normalize_text(observed)
    expected_norm = normalize_text(expected)
    if observed_norm == expected_norm:
        return True
    if not expected_norm or len(observed_norm) < len(expected_norm) * 0.9:
        return False
    edge = min(VERIFY_EDGE_CHARS, len(expected_norm))
    return (
        observed_norm.startswith(expected_norm[:edge])
        and observed_norm.endswith(expected_norm[-edge:])
        and abs(len(observed_norm) - len(expected_norm))
        <= max(12, len(expected_norm) // 50)
    )


def wait_for_written_text(
    window: BaseWrapper,
    expected_document_title: str,
    expected_text: str,
    timeout_seconds: float,
) -> BaseWrapper:
    deadline = time.monotonic() + timeout_seconds
    observed = ""
    while time.monotonic() < deadline:
        if current_document_title(window) != expected_document_title:
            raise AutomationStopped("Active destination changed during write verification. Nothing was sent.")
        try:
            group = find_composer_group(window)
            observed = copy_group_text(group)
            if text_matches_expected(observed, expected_text):
                return group
        except Exception:
            pass
        time.sleep(POLL_SECONDS)
    raise AutomationStopped(
        "Composer clipboard verification timed out. "
        f"Expected {len(normalize_text(expected_text))} normalized characters, "
        f"last copied {len(normalize_text(observed))}. Nothing was sent."
    )


def place_text(
    window: BaseWrapper,
    group: BaseWrapper,
    expected_document_title: str,
    text: str,
    replace_existing: bool,
    write_timeout_seconds: float,
) -> BaseWrapper:
    existing = normalize_text(copy_group_text(group))
    if existing and not replace_existing:
        raise AutomationStopped(
            "Composer already contains text. Existing draft was preserved. "
            "Use --replace-existing only when replacement is intentional."
        )

    focus_group_text_surface(group)
    original_clipboard = clipboard_get_text()
    try:
        if replace_existing:
            send_keys("^a", pause=0.10)
        clipboard_set_text(text)
        send_keys("^v", pause=0.10)
    finally:
        clipboard_set_text(original_clipboard)

    return wait_for_written_text(
        window,
        expected_document_title=expected_document_title,
        expected_text=text,
        timeout_seconds=write_timeout_seconds,
    )


def maybe_send(
    window: BaseWrapper,
    group: BaseWrapper,
    expected_document_title: str,
    send: bool,
    confirmation: str,
) -> None:
    if not send:
        print("Draft placed and clipboard-verified. Nothing sent.")
        return
    if confirmation != "SEND":
        raise AutomationStopped(
            "Send requested but confirmation was missing. Use --confirm-send SEND to authorize submission."
        )
    if current_document_title(window) != expected_document_title:
        raise AutomationStopped("Active destination changed before submission. Message was not sent.")
    if not group.is_visible() or not group.is_enabled():
        raise AutomationStopped("Composer lost readiness before submission. Message was not sent.")
    submit = window.child_window(auto_id="composer-submit-button", control_type="Button")
    if not submit.exists(timeout=2):
        raise AutomationStopped("Verified Send prompt button was not found. Message was not sent.")
    button = submit.wrapper_object()
    if not button.is_visible() or not button.is_enabled():
        raise AutomationStopped("Send prompt button was not ready. Message was not sent.")
    button.invoke()
    print("Message submitted after explicit confirmation and clipboard verification.")


def main() -> int:
    args = parse_args()
    target = Target(chat_title=args.chat_title, project_title=args.project)
    try:
        print(f"1. Finding window: {APP_TITLE}")
        window = get_chatgpt_window()

        print(f"2. Resolving exact chat: {target.link_title}")
        navigated = open_exact_chat(window, target)
        print("   Navigation invoked." if navigated else "   Target chat already active. Navigation skipped.")

        print(f"3. Verifying destination: {target.document_title}")
        active_title = wait_for_exact_destination(window, target, args.timeout)
        print(f"   Verified active document: {active_title}")

        print("4. Waiting for a stable, enabled Group composer")
        group = wait_for_composer_ready(
            window,
            expected_document_title=target.document_title,
            timeout_seconds=args.ready_timeout,
            stable_seconds=args.stable_seconds,
        )
        print("   Composer readiness verified.")

        print("5. Applying draft policy and clipboard-verifying the write")
        group = place_text(
            window,
            group,
            expected_document_title=target.document_title,
            text=args.text,
            replace_existing=args.replace_existing,
            write_timeout_seconds=args.write_timeout,
        )

        print("6. Applying send policy")
        maybe_send(
            window,
            group,
            expected_document_title=target.document_title,
            send=args.send,
            confirmation=args.confirm_send,
        )
        return 0
    except AutomationStopped as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"STOPPED: unexpected automation error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
