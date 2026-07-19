"""Strict dual-witness verification for ChatGPT composer writes.

Clipboard copy remains available, but a complete accessible UIA value from the
already-verified composer may also prove the draft was written. Both witnesses
must pass the automation engine's exact text comparison policy.
"""
from __future__ import annotations

import sys
import time
from types import ModuleType
from typing import Any, Iterable

_UIA_CONTROL_TYPES = {"Edit", "Document"}
_CLIPBOARD_RETRY_SECONDS = 1.0
_INSTALL_FLAG = "_lifeos_dual_write_verification_installed"


def _control_type(control: Any) -> str:
    try:
        return str(control.element_info.control_type or "")
    except Exception:
        return ""


def _visible(control: Any) -> bool:
    try:
        return bool(control.is_visible())
    except Exception:
        return False


def _text_pattern_value(control: Any) -> str:
    try:
        interface = getattr(control, "iface_text", None)
        document_range = getattr(interface, "DocumentRange", None)
        get_text = getattr(document_range, "GetText", None)
        if callable(get_text):
            value = get_text(-1)
            if value is not None:
                return str(value)
    except Exception:
        pass
    return ""


def _control_values(control: Any) -> Iterable[str]:
    readers = (
        lambda: control.get_value(),
        lambda: control.iface_value.CurrentValue,
        lambda: _text_pattern_value(control),
        lambda: control.window_text(),
    )
    seen: set[str] = set()
    for reader in readers:
        try:
            value = reader()
        except Exception:
            continue
        if value is None:
            continue
        text = str(value)
        if text in seen:
            continue
        seen.add(text)
        yield text


def composer_uia_values(group: Any) -> list[str]:
    """Read only visible Edit or Document controls inside the verified composer."""
    controls = [group]
    try:
        controls.extend(group.descendants())
    except Exception:
        pass

    values: list[str] = []
    for control in controls:
        if _control_type(control) not in _UIA_CONTROL_TYPES:
            continue
        if not _visible(control):
            continue
        values.extend(_control_values(control))
    return values


def _best_length(base: ModuleType, values: Iterable[str]) -> int:
    lengths = []
    for value in values:
        try:
            lengths.append(len(base.normalize_text(value)))
        except Exception:
            continue
    return max(lengths, default=0)


def install_base_write_verification(base: ModuleType) -> bool:
    """Replace write verification once while preserving all navigation and send gates."""
    if getattr(base, _INSTALL_FLAG, False):
        return False

    def wait_for_written_text(
        window: Any,
        expected_document_title: str,
        expected_text: str,
        timeout_seconds: float,
    ) -> Any:
        deadline = time.monotonic() + timeout_seconds
        next_clipboard_attempt = 0.0
        last_clipboard = ""
        last_uia_values: list[str] = []

        while time.monotonic() < deadline:
            if base.current_document_title(window) != expected_document_title:
                raise base.AutomationStopped(
                    "Active destination changed during write verification. Nothing was sent."
                )

            try:
                group = base.find_composer_group(window)
            except Exception:
                time.sleep(base.POLL_SECONDS)
                continue

            last_uia_values = composer_uia_values(group)
            for observed in last_uia_values:
                if base.text_matches_expected(observed, expected_text):
                    print(
                        "   WRITE VERIFICATION: accessible composer text matched the expected draft."
                    )
                    return group

            now = time.monotonic()
            if now >= next_clipboard_attempt:
                next_clipboard_attempt = now + _CLIPBOARD_RETRY_SECONDS
                try:
                    last_clipboard = base.copy_group_text(group)
                    if base.text_matches_expected(last_clipboard, expected_text):
                        print(
                            "   WRITE VERIFICATION: clipboard copy matched the expected draft."
                        )
                        return group
                except Exception:
                    pass

            time.sleep(base.POLL_SECONDS)

        expected_length = len(base.normalize_text(expected_text))
        clipboard_length = len(base.normalize_text(last_clipboard))
        uia_length = _best_length(base, last_uia_values)
        raise base.AutomationStopped(
            "Composer write verification timed out. "
            f"Expected {expected_length} normalized characters, "
            f"last clipboard copy had {clipboard_length}, "
            f"and the longest accessible composer value had {uia_length}. Nothing was sent."
        )

    base.wait_for_written_text = wait_for_written_text
    setattr(base, _INSTALL_FLAG, True)
    return True


_base = sys.modules.get("open_department_chat_group")
if isinstance(_base, ModuleType):
    install_base_write_verification(_base)
