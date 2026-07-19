"""Foreground safety gate for physical ChatGPT automation input.

The UI Automation tree can remain readable while another application owns the
actual keyboard and mouse. Composer clicks may bring ChatGPT Classic forward,
but keyboard input verifies a cached top-level window handle so it never runs a
fresh UI Automation search between composer activation and paste.
"""
from __future__ import annotations

import os
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
_HANDLE_ATTR = "_lifeos_chatgpt_foreground_handle"
_STAGE_PREFIX = "LIFEOS_STAGE="


def _trace(stage: str) -> None:
    """Write one immediate non-sensitive stage marker outside redirected buffers."""
    payload = f"{_STAGE_PREFIX}{stage}\n".encode("utf-8", errors="replace")
    try:
        os.write(sys.__stderr__.fileno(), payload)
    except Exception:
        pass


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
    setattr(base, _HANDLE_ATTR, int(window.handle))
    return window


def _expected_handle(base: ModuleType) -> int:
    handle = int(getattr(base, _HANDLE_ATTR, 0) or 0)
    if handle:
        return handle
    return int(_chatgpt_window(base).handle)


def _focus_chatgpt_foreground(base: ModuleType) -> Any:
    """Bring ChatGPT forward for an upcoming composer click and cache its handle."""
    window = _chatgpt_window(base)
    expected_handle = int(window.handle)
    if _foreground_handle() == expected_handle:
        _trace("foreground_verified")
        return window

    _trace("foreground_request")
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
            _trace("foreground_verified")
            return window
        time.sleep(FOREGROUND_POLL_SECONDS)

    raise base.AutomationStopped(
        "ChatGPT Classic could not become the foreground window. "
        "No keyboard or mouse input was sent."
    )


def _verify_chatgpt_foreground(base: ModuleType) -> int:
    """Require cached ChatGPT foreground ownership without a fresh UIA lookup."""
    expected_handle = _expected_handle(base)
    if _foreground_handle() != expected_handle:
        raise base.AutomationStopped(
            "ChatGPT Classic lost foreground focus before keyboard input. "
            "No keyboard input was sent."
        )
    return expected_handle


def _keyboard_stage(args: tuple[Any, ...]) -> str:
    keys = str(args[0]) if args else ""
    return {
        "^a": "keyboard_select_all_start",
        "^c": "keyboard_copy_start",
        "^v": "keyboard_paste_start",
        "{RIGHT}": "keyboard_right_start",
    }.get(keys, "keyboard_other_start")


def install_base_guard(base: ModuleType) -> bool:
    """Wrap the base automation's physical-input functions exactly once."""
    if getattr(base, _GUARD_FLAG, False):
        return False

    original_focus_group_text_surface = base.focus_group_text_surface
    original_send_keys = base.send_keys

    def guarded_focus_group_text_surface(group: Any) -> None:
        _focus_chatgpt_foreground(base)
        _trace("composer_activation_start")
        original_focus_group_text_surface(group)
        _verify_chatgpt_foreground(base)
        _trace("composer_activation_verified")

    def guarded_send_keys(*args: Any, **kwargs: Any) -> Any:
        _verify_chatgpt_foreground(base)
        _trace(_keyboard_stage(args))
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
