"""Production shim for Group composer verification with bounded UI-wrapper tolerance.

The modern ChatGPT Classic composer may place a small accessibility label around the exact
clipboard payload. Verification succeeds only when the complete normalized expected prompt
appears contiguously inside the copied text and the total surrounding text is tightly bounded.
All navigation, draft-preservation, readiness, and send gates remain owned by the base engine.
"""

from __future__ import annotations

import open_department_chat_group as base

MAX_ACCESSIBILITY_WRAPPER_CHARS = 64


def text_matches_expected(observed: str, expected: str) -> bool:
    observed_norm = base.normalize_text(observed)
    expected_norm = base.normalize_text(expected)

    if not expected_norm:
        return observed_norm == expected_norm
    if observed_norm == expected_norm:
        return True
    if expected_norm not in observed_norm:
        return False

    extra_chars = len(observed_norm) - len(expected_norm)
    return 0 <= extra_chars <= MAX_ACCESSIBILITY_WRAPPER_CHARS


base.text_matches_expected = text_matches_expected
main = base.main


if __name__ == "__main__":
    raise SystemExit(main())
