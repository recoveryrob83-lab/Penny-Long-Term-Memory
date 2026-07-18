import pytest

from lifeos_dashboard.clipboard_runtime import run_with_restored_clipboard


def test_keeps_prompt_available_until_operation_finishes() -> None:
    state = {"clipboard": "i"}

    def get_text() -> str:
        return state["clipboard"]

    def set_text(value: str) -> None:
        state["clipboard"] = value

    def operation() -> str:
        assert state["clipboard"] == "[OVERDUE RESTART TEST]"
        return "verified"

    result = run_with_restored_clipboard(
        "[OVERDUE RESTART TEST]",
        get_text,
        set_text,
        operation,
    )

    assert result == "verified"
    assert state["clipboard"] == "i"


def test_restores_prior_clipboard_when_operation_fails() -> None:
    state = {"clipboard": "original"}

    def get_text() -> str:
        return state["clipboard"]

    def set_text(value: str) -> None:
        state["clipboard"] = value

    def operation() -> None:
        assert state["clipboard"] == "prompt"
        raise RuntimeError("verification failed")

    with pytest.raises(RuntimeError, match="verification failed"):
        run_with_restored_clipboard("prompt", get_text, set_text, operation)

    assert state["clipboard"] == "original"
