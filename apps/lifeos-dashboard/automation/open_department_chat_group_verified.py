"""Production shim for Group composer verification across UI copy transforms.

The modern ChatGPT Classic composer applies deterministic presentation transforms when copying a
pasted prompt. This shim preserves the base engine's exact navigation and safety gates, adds one
bounded sidebar expansion, and emits a structured result marker for stopped runs so dashboard
reporting does not have to infer the cause from incidental console text.
"""
from __future__ import annotations

import contextlib
import io
import re
import sys
import time

import open_department_chat_group as base

SIDEBAR_EXPANSION_TIMEOUT_SECONDS = 5.0
SIDEBAR_EXPANSION_POLL_SECONDS = 0.25
RESULT_MARKER = "LIFEOS_RESULT_CODE="


def compact_non_whitespace(value: str) -> str:
    """Remove only whitespace while preserving every other character exactly and in order."""
    return re.sub(r"\s+", "", value)


def text_matches_expected(observed: str, expected: str) -> bool:
    observed_compact = compact_non_whitespace(base.normalize_text(observed))
    expected_compact = compact_non_whitespace(base.normalize_text(expected))
    if observed_compact == expected_compact:
        return True
    if expected_compact.startswith("@GitHub"):
        return observed_compact == expected_compact[1:]
    return False


_original_open_exact_chat = base.open_exact_chat


def find_sidebar_show_more(window):
    """Return one visible, enabled Show more button from the left sidebar region."""
    window_rect = window.rectangle()
    sidebar_right_limit = window_rect.left + max(360, int(window_rect.width() * 0.35))
    candidates = []
    for control in window.descendants():
        if control.element_info.control_type != "Button":
            continue
        if control.window_text().strip() != "Show more":
            continue
        try:
            rect = control.rectangle()
            if not control.is_visible() or not control.is_enabled():
                continue
        except Exception:
            continue
        if rect.left <= sidebar_right_limit:
            candidates.append(control)
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item.rectangle().left, item.rectangle().top))


def open_exact_chat_with_bounded_sidebar_expansion(window, target) -> bool:
    """Expose hidden chats with one sidebar Show more invocation, then require the exact link."""
    if base.current_document_title(window) == target.document_title:
        return False
    exact_link = window.child_window(title=target.link_title, control_type="Hyperlink")
    if exact_link.exists(timeout=0.5):
        return _original_open_exact_chat(window, target)
    show_more = find_sidebar_show_more(window)
    if show_more is None:
        raise base.AutomationStopped(
            "Exact chat link was hidden or unavailable, and no visible sidebar Show more button "
            f"was found: {target.link_title!r}"
        )
    print("   SIDEBAR EXPANSION: exact chat link is hidden. Invoking Show more once.")
    window.set_focus()
    show_more.invoke()
    deadline = time.monotonic() + SIDEBAR_EXPANSION_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        exact_link = window.child_window(title=target.link_title, control_type="Hyperlink")
        if exact_link.exists(timeout=0.1):
            print("   Exact chat link became available after one sidebar expansion.")
            return _original_open_exact_chat(window, target)
        time.sleep(SIDEBAR_EXPANSION_POLL_SECONDS)
    raise base.AutomationStopped(
        "Exact chat link did not become available after one bounded sidebar Show more expansion: "
        f"{target.link_title!r}"
    )


def classify_result(output: str) -> str:
    diagnostic = output.casefold()
    if "composer already contains text" in diagnostic or "existing draft was preserved" in diagnostic:
        return "composer_occupied"
    if "chatgpt window not found" in diagnostic:
        return "chatgpt_unavailable"
    if "exact chat link" in diagnostic or "destination verification failed" in diagnostic:
        return "destination_unverified"
    if "clipboard verification" in diagnostic:
        return "write_verification_failed"
    if "send prompt button" in diagnostic or "before submission" in diagnostic:
        return "send_uncertain"
    if "timed out" in diagnostic:
        return "timeout"
    return "automation_stopped"


def main() -> int:
    """Run the base engine and append one stable result marker on failure."""
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
        exit_code = base.main()
    stdout = stdout_buffer.getvalue()
    stderr = stderr_buffer.getvalue()
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    if exit_code != 0:
        code = classify_result(f"{stderr}\n{stdout}")
        print(f"{RESULT_MARKER}{code}", file=sys.stderr)
        if code == "composer_occupied":
            print("Composer already contains text. Existing draft was preserved.", file=sys.stderr)
    return exit_code


base.text_matches_expected = text_matches_expected
base.open_exact_chat = open_exact_chat_with_bounded_sidebar_expansion


if __name__ == "__main__":
    raise SystemExit(main())
