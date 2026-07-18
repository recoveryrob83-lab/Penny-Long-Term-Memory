"""Foreground safety gate for physical ChatGPT automation input.

The UI Automation tree can remain readable while another application owns the
actual keyboard and mouse. Composer clicks may bring ChatGPT Classic forward,
but keyboard input must only verify foreground ownership so it does not steal
focus back from the composer text surface.
"""
from __future__ import annotations

import sys
import time
from types import ModuleType
from typing import Any

from . import command_center

try:  # Windows-only dependency; dashboard imports must remain portable.
    import win32gui  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - exercised only outside Windows.
    win32gui = None  # type: ignore[assignment]

FOREGROUND_TIMEOUT_SECONDS = 2.0
FOREGROUND_POLL_SECONDS = 0.05
_GUARD_FLAG = "_lifeos_foreground_guard_installed"


def _foreground_handle() -> int:
    if win32gui is None:
        return 0
    return int(win32gui.GetForegroundWindow() or 0)


def _chatgpt_window(base: ModuleType) -> Any:
    window = base.get_chatgpt_window()
    if not getattr(window, "handle", None):
        raise base.AutomationStopped(
            "ChatGPT Classic window handle was unavailable. "
            "No keyboard or mouse input was sent."
        )
    return window


def _focus_chatgpt_foreground(base: ModuleType) -> Any:
    """Bring ChatGPT forward for an upcoming composer click and prove ownership."""
    window = _chatgpt_window(base)
    expected_handle = int(window.handle)
    if _foreground_handle() == expected_handle:
        return window

    try:
        is_minimized = getattr(window, "is_minimized", None)
        if callable(is_minimized) and is_minimized():
            restore = getattr(window, "restore", None)
            if callable(restore):
                restore()
    except Exception:
        pass

    try:
        window.set_focus()
    except Exception as exc:
        raise base.AutomationStopped(
            "ChatGPT Classic could not become the foreground window. "
            "No keyboard or mouse input was sent."
        ) from exc

    deadline = time.monotonic() + FOREGROUND_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if _foreground_handle() == expected_handle:
            return window
        time.sleep(FOREGROUND_POLL_SECONDS)

    raise base.AutomationStopped(
        "ChatGPT Classic could not become the foreground window. "
        "No keyboard or mouse input was sent."
    )


def _verify_chatgpt_foreground(base: ModuleType) -> Any:
    """Require ChatGPT foreground ownership without changing child-control focus."""
    window = _chatgpt_window(base)
    if _foreground_handle() != int(window.handle):
        raise base.AutomationStopped(
            "ChatGPT Classic lost foreground focus before keyboard input. "
            "No keyboard input was sent."
        )
    return window


def install_base_guard(base: ModuleType) -> bool:
    """Wrap the base automation's physical-input functions exactly once."""
    if getattr(base, _GUARD_FLAG, False):
        return False

    original_focus_group_text_surface = base.focus_group_text_surface
    original_send_keys = base.send_keys

    def guarded_focus_group_text_surface(group: Any) -> None:
        _focus_chatgpt_foreground(base)
        original_focus_group_text_surface(group)
        _verify_chatgpt_foreground(base)

    def guarded_send_keys(*args: Any, **kwargs: Any) -> Any:
        _verify_chatgpt_foreground(base)
        return original_send_keys(*args, **kwargs)

    base.focus_group_text_surface = guarded_focus_group_text_surface
    base.send_keys = guarded_send_keys
    setattr(base, _GUARD_FLAG, True)
    return True


def explain_failure(stdout: str, stderr: str, exit_code: int | None) -> str:
    """Surface foreground refusal as a precise, actionable dashboard message."""
    diagnostic = f"{stderr}\n{stdout}".casefold()
    if (
        "foreground window" in diagnostic
        or "lost foreground focus" in diagnostic
        or "window handle was unavailable" in diagnostic
    ):
        return (
            "ChatGPT Classic could not safely retain foreground focus. "
            "Restore or bring ChatGPT Classic forward, then retry. Nothing was pasted or sent."
        )
    return _original_explain_failure(stdout, stderr, exit_code)


_original_explain_failure = command_center.explain_failure
command_center.explain_failure = explain_failure

_base = sys.modules.get("open_department_chat_group")
if isinstance(_base, ModuleType):
    install_base_guard(_base)
