"""Safely open a LifeOS department chat and place text in the composer.

Windows-only prototype using pywinauto and the ChatGPT Classic UI Automation tree.
Nothing is sent unless --send is explicitly provided together with --confirm-send SEND.
Existing composer text is preserved unless --replace-existing is explicitly provided.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass

from pywinauto import Desktop
from pywinauto.base_wrapper import BaseWrapper


APP_TITLE = "ChatGPT Classic"
DEFAULT_PROJECT = "Life OS"
DEFAULT_TIMEOUT_SECONDS = 5.0


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
            "Open an exact LifeOS department chat, verify the destination, and place "
            "text in the composer. Draft-only by default."
        )
    )
    parser.add_argument("chat_title", help="Exact sidebar chat title")
    parser.add_argument(
        "--project",
        default=DEFAULT_PROJECT,
        help=f"Project name used by ChatGPT accessibility labels (default: {DEFAULT_PROJECT})",
    )
    parser.add_argument(
        "--text",
        default="[AUTOMATION TEST - DO NOT SEND]",
        help="Text to place in the composer",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Seconds to wait for destination verification",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Replace existing composer text instead of stopping",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Submit the message after verification",
    )
    parser.add_argument(
        "--confirm-send",
        default="",
        help="Required value SEND when --send is used",
    )
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
    """Open the target chat only when it is not already active.

    Returns True when navigation was invoked and False when the target was
    already active.
    """
    if current_document_title(window) == target.document_title:
        return False

    link = window.child_window(title=target.link_title, control_type="Hyperlink")
    if not link.exists(timeout=2):
        raise AutomationStopped(
            "Exact chat link not found in the accessible sidebar: "
            f"{target.link_title!r}"
        )

    window.set_focus()
    link.invoke()
    return True


def wait_for_destination(
    window: BaseWrapper,
    expected_title: str,
    timeout_seconds: float,
) -> str:
    deadline = time.time() + timeout_seconds
    active_title = ""

    while time.time() < deadline:
        active_title = current_document_title(window)
        if active_title == expected_title:
            return active_title
        time.sleep(0.25)

    raise AutomationStopped(
        "Destination verification failed. "
        f"Expected {expected_title!r}, observed {active_title!r}."
    )


def find_visible_composer(window: BaseWrapper) -> BaseWrapper:
    """Find the visible message composer without relying on its current text.

    ChatGPT changes the Edit control's accessible name when text is present, so
    matching the literal title 'Ask ChatGPT' is not reliable. The composer is
    instead selected as the lowest visible Edit control inside the app window.
    """
    edits: list[BaseWrapper] = []
    window_rect = window.rectangle()

    for control in window.descendants():
        if control.element_info.control_type != "Edit":
            continue

        rect = control.rectangle()
        if rect.top < window_rect.top or rect.bottom > window_rect.bottom:
            continue
        if rect.left < window_rect.left or rect.right > window_rect.right:
            continue
        if rect.width() <= 0 or rect.height() <= 0:
            continue

        edits.append(control)

    if not edits:
        raise AutomationStopped("No visible Edit control was found after verification.")

    composer = max(edits, key=lambda control: control.rectangle().top)
    return composer


def read_composer_text(composer: BaseWrapper) -> str:
    try:
        return composer.get_value().strip()
    except Exception:
        return composer.window_text().strip()


def place_text(
    window: BaseWrapper,
    text: str,
    replace_existing: bool,
) -> BaseWrapper:
    composer = find_visible_composer(window)
    existing = read_composer_text(composer)

    if existing and existing != "Ask ChatGPT" and not replace_existing:
        raise AutomationStopped(
            "Composer already contains text. Existing draft was preserved. "
            "Use --replace-existing only when replacement is intentional."
        )

    composer.set_focus()
    composer.set_edit_text(text)
    return composer


def maybe_send(composer: BaseWrapper, send: bool, confirmation: str) -> None:
    if not send:
        print("Draft placed. Nothing sent.")
        return

    if confirmation != "SEND":
        raise AutomationStopped(
            "Send requested but confirmation was missing. "
            "Use --confirm-send SEND to authorize submission."
        )

    composer.type_keys("{ENTER}")
    print("Message submitted after explicit confirmation.")


def main() -> int:
    args = parse_args()
    target = Target(chat_title=args.chat_title, project_title=args.project)

    try:
        print(f"1. Finding window: {APP_TITLE}")
        window = get_chatgpt_window()

        print(f"2. Resolving exact chat: {target.link_title}")
        navigated = open_exact_chat(window, target)
        if navigated:
            print("   Navigation invoked.")
        else:
            print("   Target chat already active. Navigation skipped.")

        print(f"3. Verifying destination: {target.document_title}")
        active_title = wait_for_destination(
            window,
            expected_title=target.document_title,
            timeout_seconds=args.timeout,
        )
        print(f"   Verified active document: {active_title}")

        print("4. Locating visible composer and applying draft policy")
        composer = place_text(
            window,
            text=args.text,
            replace_existing=args.replace_existing,
        )

        print("5. Applying send policy")
        maybe_send(composer, send=args.send, confirmation=args.confirm_send)
        return 0
    except AutomationStopped as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # Defensive boundary for early prototype work.
        print(f"STOPPED: unexpected automation error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
