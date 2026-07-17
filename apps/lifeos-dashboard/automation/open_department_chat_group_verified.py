"""Production shim for Group composer verification across UI copy transforms.

The modern ChatGPT Classic composer applies two deterministic presentation transforms when
copying a pasted prompt: paragraph separators may expand into additional newlines, and a leading
@GitHub token may be represented as an accessible GitHub mention whose clipboard text omits the
literal @. Verification therefore compares the exact non-whitespace character stream and permits
only that one narrowly scoped leading-at omission.

Exact chat navigation also permits one bounded sidebar expansion. When the exact project-chat link
is not initially exposed, the shim invokes one visible Show more button in the left sidebar region,
waits briefly for the exact accessible link to appear, and then delegates to the base engine. No
fuzzy chat matching or unbounded clicking is allowed. All other navigation, draft preservation,
readiness, and send gates remain owned by the base engine.
"""

from __future__ import annotations

import re
import time

import open_department_chat_group as base

SIDEBAR_EXPANSION_TIMEOUT_SECONDS = 5.0
SIDEBAR_EXPANSION_POLL_SECONDS = 0.25


def compact_non_whitespace(value: str) -> str:
    """Remove only whitespace while preserving every other character exactly and in order."""
    return re.sub(r"\s+", "", value)


def text_matches_expected(observed: str, expected: str) -> bool:
    observed_compact = compact_non_whitespace(base.normalize_text(observed))
    expected_compact = compact_non_whitespace(base.normalize_text(expected))

    if observed_compact == expected_compact:
        return True

    # ChatGPT may render the leading literal @GitHub token as a mention object. Its accessible
    # clipboard representation then begins with GitHub while preserving every remaining character.
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

    # Prefer the left-most candidate, then the upper-most one. This stays deterministic when the
    # accessibility tree exposes more than one matching button elsewhere in the application.
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


base.text_matches_expected = text_matches_expected
base.open_exact_chat = open_exact_chat_with_bounded_sidebar_expansion
main = base.main


if __name__ == "__main__":
    raise SystemExit(main())
