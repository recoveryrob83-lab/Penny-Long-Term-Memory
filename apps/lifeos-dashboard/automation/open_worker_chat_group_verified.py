"""Worker-only ChatGPT transport using one wrapper-ID composer witness.

This entrypoint preserves the established exact-title, empty-composer, clipboard-restoration,
explicit-send, and stop-on-uncertainty safeguards. After paste it copies the composer once and
requires the expected wrapper marker instead of performing full-text equality.
"""
from __future__ import annotations

import sys

from lifeos_dashboard.worker_runtime import copied_text_contains_wrapper


def extract_verify_marker(argv: list[str]) -> tuple[str, list[str]]:
    """Remove one required Worker-only marker option before the base CLI parses arguments."""

    marker: str | None = None
    forwarded = [argv[0]]
    index = 1
    while index < len(argv):
        value = argv[index]
        if value != "--verify-marker":
            forwarded.append(value)
            index += 1
            continue
        if marker is not None:
            raise ValueError("Worker transport accepts exactly one --verify-marker value.")
        if index + 1 >= len(argv):
            raise ValueError("Worker transport requires a value after --verify-marker.")
        marker = argv[index + 1].strip()
        if not marker:
            raise ValueError("Worker verification marker cannot be empty.")
        index += 2
    if marker is None:
        raise ValueError("Worker transport requires --verify-marker.")
    return marker, forwarded


def main() -> int:
    try:
        marker, forwarded = extract_verify_marker(list(sys.argv))
    except ValueError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2

    sys.argv = forwarded

    import open_department_chat_group as base
    import open_department_chat_group_verified as verified

    def verify_wrapper_once(
        window,
        expected_document_title: str,
        expected_text: str,
        timeout_seconds: float,
    ):
        del expected_text, timeout_seconds
        if base.current_document_title(window) != expected_document_title:
            raise base.AutomationStopped(
                "Active destination changed during Worker wrapper verification. Nothing was sent."
            )
        group = base.find_composer_group(window)
        observed = base.copy_group_text(group)
        if not copied_text_contains_wrapper(observed, marker):
            raise base.AutomationStopped(
                "Composer clipboard verification failed. Expected Worker wrapper marker was not "
                "copied. Nothing was sent."
            )
        return group

    base.wait_for_written_text = verify_wrapper_once
    return verified.main()


if __name__ == "__main__":
    raise SystemExit(main())
