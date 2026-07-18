"""Small clipboard lifetime guard shared by desktop automation."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

_Result = TypeVar("_Result")


def run_with_restored_clipboard(
    value: str,
    get_text: Callable[[], str],
    set_text: Callable[[str], None],
    operation: Callable[[], _Result],
) -> _Result:
    """Keep ``value`` available for an operation, then restore the prior clipboard."""
    original = get_text()
    set_text(value)
    try:
        return operation()
    finally:
        set_text(original)
