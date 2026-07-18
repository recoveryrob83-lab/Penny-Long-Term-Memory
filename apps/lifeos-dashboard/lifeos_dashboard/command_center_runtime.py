"""Runtime result-code policy for Automation Command Center failures."""

from __future__ import annotations

from . import command_center

RESULT_MARKER = "LIFEOS_RESULT_CODE="

_RESULT_MESSAGES = {
    "composer_occupied": (
        "The target composer already contains text. Clear or save that draft, then run the job again."
    ),
    "chatgpt_unavailable": (
        "ChatGPT Classic was not available. Open the desktop app, leave it signed in, and retry."
    ),
    "destination_unverified": (
        "The exact LifeOS chat could not be verified. Open the sidebar, confirm the chat name, "
        "and retry without renaming it."
    ),
    "write_verification_failed": (
        "The prompt was only partially written or could not be verified. Nothing was sent. "
        "Clear any partial composer text, focus ChatGPT Classic, and retry."
    ),
    "send_uncertain": (
        "The draft was verified, but send readiness could not be confirmed. Nothing was sent."
    ),
    "timeout": (
        "The automation timed out. Make sure ChatGPT Classic is responsive and no modal window "
        "is blocking it, then retry."
    ),
}

_original_explain_failure = command_center.explain_failure


def structured_result_code(stdout: str, stderr: str) -> str | None:
    """Return the final explicit automation result code, when one was emitted."""
    for line in reversed(f"{stderr}\n{stdout}".splitlines()):
        stripped = line.strip()
        if stripped.startswith(RESULT_MARKER):
            return stripped.removeprefix(RESULT_MARKER).strip() or None
    return None


def explain_failure(stdout: str, stderr: str, exit_code: int | None) -> str:
    """Prefer explicit automation result codes over broad diagnostic keyword guesses."""
    code = structured_result_code(stdout, stderr)
    if code in _RESULT_MESSAGES:
        return _RESULT_MESSAGES[code]
    return _original_explain_failure(stdout, stderr, exit_code)


command_center.explain_failure = explain_failure
