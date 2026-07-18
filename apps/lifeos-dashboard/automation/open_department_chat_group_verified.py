"""Production shim for Group composer verification across UI copy transforms.

The modern ChatGPT Classic composer applies deterministic presentation transforms when copying a
pasted prompt. This shim preserves the base engine's exact navigation and safety gates, adds bounded
sidebar and project recovery, translates retired chat titles to their canonical replacements, and
emits a structured result marker for stopped runs so dashboard reporting does not have to infer the
cause from incidental console text.
"""
from __future__ import annotations

import contextlib
import io
import re
import sys
import time

import open_department_chat_group as base
from lifeos_dashboard.clipboard_runtime import run_with_restored_clipboard

SIDEBAR_EXPANSION_TIMEOUT_SECONDS = 5.0
SIDEBAR_EXPANSION_POLL_SECONDS = 0.25
PROJECT_EXPANSION_TIMEOUT_SECONDS = 5.0
EXPAND_COLLAPSE_COLLAPSED = 0
RESULT_MARKER = "LIFEOS_RESULT_CODE="

CHAT_TITLE_ALIASES = {
    "Main Assistant HQ": "Chief of Staff HQ",
    "Logistics HQ": "Life OS Maintenance HQ",
    "Life Logistics HQ": "Life OS Maintenance HQ",
}


def canonical_chat_title(value: str) -> str:
    """Translate a retired exact title while leaving canonical and unknown titles unchanged."""
    return CHAT_TITLE_ALIASES.get(value, value)


def normalize_cli_chat_title() -> None:
    """Rewrite only the positional chat-title argument before the exact-navigation engine runs."""
    if len(sys.argv) < 2:
        return
    original = sys.argv[1]
    canonical = canonical_chat_title(original)
    if canonical != original:
        print(f"COMPATIBILITY MAPPING: {original!r} -> {canonical!r}")
        sys.argv[1] = canonical


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


def place_text_with_stable_clipboard(
    window,
    group,
    expected_document_title: str,
    text: str,
    replace_existing: bool,
    write_timeout_seconds: float,
):
    """Keep the intended prompt on the clipboard until composer verification finishes."""
    existing = base.normalize_text(base.copy_group_text(group))
    if existing and not replace_existing:
        raise base.AutomationStopped(
            "Composer already contains text. Existing draft was preserved. "
            "Use --replace-existing only when replacement is intentional."
        )

    base.focus_group_text_surface(group)
    if replace_existing:
        base.send_keys("^a", pause=0.10)

    def paste_and_verify():
        base.send_keys("^v", pause=0.10)
        return base.wait_for_written_text(
            window,
            expected_document_title=expected_document_title,
            expected_text=text,
            timeout_seconds=write_timeout_seconds,
        )

    return run_with_restored_clipboard(
        text,
        base.clipboard_get_text,
        base.clipboard_set_text,
        paste_and_verify,
    )


_original_open_exact_chat = base.open_exact_chat


def sidebar_right_limit(window) -> int:
    """Return the bounded horizontal limit used for left-sidebar controls."""
    window_rect = window.rectangle()
    return window_rect.left + max(360, int(window_rect.width() * 0.35))


def find_sidebar_show_more(window):
    """Return one visible, enabled Show more button from the left sidebar region."""
    right_limit = sidebar_right_limit(window)
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
        if rect.left <= right_limit:
            candidates.append(control)
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item.rectangle().left, item.rectangle().top))


def expand_collapse_state(control):
    """Read the UIA expand/collapse state without assuming one wrapper implementation."""
    getter = getattr(control, "get_expand_collapse_state", None)
    if callable(getter):
        try:
            return getter()
        except Exception:
            pass
    interface = getattr(control, "iface_expand_collapse", None)
    if interface is not None:
        try:
            return interface.CurrentExpandCollapseState
        except Exception:
            pass
    return None


def is_collapsed_state(value) -> bool:
    """Recognize the UIA collapsed state while rejecting expanded, partial, and unknown states."""
    if value is None:
        return False
    if isinstance(value, str):
        normalized = re.sub(r"[^a-z]", "", value.casefold())
        return normalized.endswith("collapsed") and "partially" not in normalized
    try:
        return int(value) == EXPAND_COLLAPSE_COLLAPSED
    except (TypeError, ValueError):
        return False


def project_label_matches(observed: str, project_title: str) -> bool:
    """Accept only exact accessibility labels for the requested project."""
    clean = observed.strip()
    return clean in {
        project_title,
        f"{project_title}, project",
        f"{project_title}, project, collapsed",
    }


def find_collapsed_project_control(window, project_title: str):
    """Return the exact collapsed project control from the left sidebar, if exposed by UIA."""
    right_limit = sidebar_right_limit(window)
    candidates = []
    for control in window.descendants():
        try:
            if not project_label_matches(control.window_text(), project_title):
                continue
            rect = control.rectangle()
            if rect.left > right_limit or not control.is_visible() or not control.is_enabled():
                continue
            if not is_collapsed_state(expand_collapse_state(control)):
                continue
        except Exception:
            continue
        candidates.append(control)
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item.rectangle().left, item.rectangle().top))


def project_chat_region_visible(window, project_title: str) -> bool:
    """Verify at least one visible exact chat link belongs to the expanded project."""
    right_limit = sidebar_right_limit(window)
    suffix = f", chat in project {project_title}"
    for control in window.descendants():
        try:
            if control.element_info.control_type != "Hyperlink":
                continue
            if not control.window_text().strip().endswith(suffix):
                continue
            rect = control.rectangle()
            if rect.left > right_limit or rect.top < 0:
                continue
            if control.is_visible() and control.is_enabled():
                return True
        except Exception:
            continue
    return False


def expand_project_control_once(control) -> None:
    """Use one explicit UIA expansion action after collapsed state was verified."""
    expand = getattr(control, "expand", None)
    if callable(expand):
        expand()
        return
    interface = getattr(control, "iface_expand_collapse", None)
    if interface is not None:
        expand_method = getattr(interface, "Expand", None)
        if callable(expand_method):
            expand_method()
            return
    control.invoke()


def expand_collapsed_project_once(window, target) -> bool:
    """Expand the exact folded project once and verify that its chat region becomes visible."""
    project = find_collapsed_project_control(window, target.project_title)
    if project is None:
        return False
    print(
        "   PROJECT RECOVERY: exact project is collapsed. "
        f"Expanding {target.project_title!r} once."
    )
    window.set_focus()
    expand_project_control_once(project)
    deadline = time.monotonic() + PROJECT_EXPANSION_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        exact_link = window.child_window(title=target.link_title, control_type="Hyperlink")
        if exact_link.exists(timeout=0.1) or project_chat_region_visible(window, target.project_title):
            print("   Project chat region became visible after one exact expansion.")
            return True
        time.sleep(SIDEBAR_EXPANSION_POLL_SECONDS)
    raise base.AutomationStopped(
        "Collapsed project expansion did not expose a verified project chat region: "
        f"{target.project_title!r}"
    )


def open_exact_chat_with_bounded_sidebar_expansion(window, target) -> bool:
    """Recover one folded project and one hidden-chat list, then require the exact chat link."""
    if base.current_document_title(window) == target.document_title:
        return False
    exact_link = window.child_window(title=target.link_title, control_type="Hyperlink")
    if exact_link.exists(timeout=0.5):
        return _original_open_exact_chat(window, target)

    project_expanded = expand_collapsed_project_once(window, target)
    if project_expanded:
        exact_link = window.child_window(title=target.link_title, control_type="Hyperlink")
        if exact_link.exists(timeout=0.5):
            return _original_open_exact_chat(window, target)

    show_more = find_sidebar_show_more(window)
    if show_more is None:
        recovery_detail = " after exact project expansion" if project_expanded else ""
        raise base.AutomationStopped(
            "Exact chat link was hidden or unavailable"
            f"{recovery_detail}, and no visible sidebar Show more button was found: "
            f"{target.link_title!r}"
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
        "Exact chat link did not become available after bounded project/sidebar recovery: "
        f"{target.link_title!r}"
    )


def classify_result(output: str) -> str:
    diagnostic = output.casefold()
    if "composer already contains text" in diagnostic or "existing draft was preserved" in diagnostic:
        return "composer_occupied"
    if "chatgpt window not found" in diagnostic:
        return "chatgpt_unavailable"
    if (
        "exact chat link" in diagnostic
        or "destination verification failed" in diagnostic
        or "project expansion" in diagnostic
        or "project chat region" in diagnostic
    ):
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
        normalize_cli_chat_title()
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
base.place_text = place_text_with_stable_clipboard
base.open_exact_chat = open_exact_chat_with_bounded_sidebar_expansion


if __name__ == "__main__":
    raise SystemExit(main())
