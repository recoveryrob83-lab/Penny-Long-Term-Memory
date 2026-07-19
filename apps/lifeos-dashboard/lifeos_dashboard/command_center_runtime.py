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
    "send_uncertain": (
        "The draft was verified, but send readiness could not be confirmed. Nothing was sent."
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


def _last_matching_line(stdout: str, stderr: str, fragments: tuple[str, ...]) -> str | None:
    for line in reversed(f"{stderr}\n{stdout}".splitlines()):
        clean = line.strip()
        lowered = clean.casefold()
        if clean and any(fragment in lowered for fragment in fragments):
            return clean
    return None


def _write_verification_message(stdout: str, stderr: str) -> str:
    detail = _last_matching_line(
        stdout,
        stderr,
        (
            "composer write verification timed out",
            "last clipboard copy had",
            "longest accessible composer value",
        ),
    )
    message = (
        "The prompt reached the composer, but post-paste verification could not confirm the draft. "
        "The draft may be present; nothing was sent. Leave the composer untouched. "
        "Open Automation Logs before retrying."
    )
    return f"{message} Detail: {detail}" if detail else message


def _timeout_message(stdout: str, stderr: str) -> str:
    diagnostic = f"{stderr}\n{stdout}".casefold()
    if (
        "composer write verification timed out" in diagnostic
        or "keyboard_copy_start" in diagnostic
        or "keyboard_select_all_start" in diagnostic
        or "last clipboard copy had" in diagnostic
    ):
        return _write_verification_message(stdout, stderr)
    if "composer readiness timed out" in diagnostic:
        detail = _last_matching_line(stdout, stderr, ("composer readiness timed out",))
        message = (
            "The destination opened, but the composer never became stably ready before the "
            "internal timeout. Nothing was pasted or sent. Open Automation Logs to inspect the "
            "readiness stages."
        )
        return f"{message} Detail: {detail}" if detail else message
    if "destination verification failed" in diagnostic or "generic chatgpt loading state" in diagnostic:
        return (
            "ChatGPT Classic did not finish rendering the exact destination before the internal "
            "timeout. Nothing was pasted or sent. Switch chats only to recover the app, then open "
            "Automation Logs before retrying."
        )
    return (
        "The automation reached an internal timeout. Nothing was sent. Open Automation Logs for "
        "the exact backend stage, stdout, and stderr instead of guessing from a generic timeout."
    )


def explain_failure(stdout: str, stderr: str, exit_code: int | None) -> str:
    """Prefer explicit result codes and stage evidence over broad keyword guesses."""
    code = structured_result_code(stdout, stderr)
    if code == "write_verification_failed":
        return _write_verification_message(stdout, stderr)
    if code == "timeout":
        return _timeout_message(stdout, stderr)
    if code in _RESULT_MESSAGES:
        return _RESULT_MESSAGES[code]
    return _original_explain_failure(stdout, stderr, exit_code)


command_center.explain_failure = explain_failure
