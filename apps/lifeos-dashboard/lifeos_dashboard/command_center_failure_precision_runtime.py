"""Final precision layer for Automation Command Center failure guidance."""
from __future__ import annotations

from . import command_center


_original_explain_failure = command_center.explain_failure


def explain_failure(stdout: str, stderr: str, exit_code: int | None) -> str:
    """Prefer exact foreground evidence over broad ChatGPT-window wording."""
    diagnostic = f"{stderr}\n{stdout}".casefold()
    if (
        "could not become the foreground window" in diagnostic
        or "lost foreground focus" in diagnostic
        or "window handle was unavailable" in diagnostic
        or "could not safely retain foreground focus" in diagnostic
    ):
        return (
            "ChatGPT Classic could not safely retain foreground focus. "
            "Nothing was pasted or sent. Bring ChatGPT Classic forward, clear any modal, and retry."
        )
    if "chatgpt window not found" in diagnostic:
        return "ChatGPT Classic was not available. Open the desktop app, leave it signed in, and retry."
    return _original_explain_failure(stdout, stderr, exit_code)


command_center.explain_failure = explain_failure
