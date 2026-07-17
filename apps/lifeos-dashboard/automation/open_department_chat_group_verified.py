"""Production shim for Group composer verification with bounded UI-text tolerance.

The modern ChatGPT Classic composer can interleave a small amount of accessibility text
inside the clipboard payload. Verification succeeds only when every normalized expected
character appears in order with no deletions or substitutions, and the copied payload has
at most a tightly bounded number of extra UI characters. Navigation, draft preservation,
readiness, and send gates remain owned by the base engine.
"""

from __future__ import annotations

import open_department_chat_group as base

MAX_ACCESSIBILITY_EXTRA_CHARS = 64


def expected_is_insertion_only_subsequence(observed: str, expected: str) -> bool:
    """Return True only when observed equals expected plus bounded inserted characters."""
    expected_index = 0
    for character in observed:
        if expected_index < len(expected) and character == expected[expected_index]:
            expected_index += 1
    return expected_index == len(expected)


def text_matches_expected(observed: str, expected: str) -> bool:
    observed_norm = base.normalize_text(observed)
    expected_norm = base.normalize_text(expected)

    if not expected_norm:
        return observed_norm == expected_norm
    if observed_norm == expected_norm:
        return True

    extra_chars = len(observed_norm) - len(expected_norm)
    if extra_chars < 0 or extra_chars > MAX_ACCESSIBILITY_EXTRA_CHARS:
        return False

    return expected_is_insertion_only_subsequence(observed_norm, expected_norm)


base.text_matches_expected = text_matches_expected
main = base.main


if __name__ == "__main__":
    raise SystemExit(main())
