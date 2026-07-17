"""Production shim for Group composer verification across UI copy transforms.

The modern ChatGPT Classic composer applies two deterministic presentation transforms when
copying a pasted prompt: paragraph separators may expand into additional newlines, and a leading
@GitHub token may be represented as an accessible GitHub mention whose clipboard text omits the
literal @. Verification therefore compares the exact non-whitespace character stream and permits
only that one narrowly scoped leading-at omission. Navigation, draft preservation, readiness, and
send gates remain owned by the base engine.
"""

from __future__ import annotations

import re

import open_department_chat_group as base


def compact_non_whitespace(value: str) -> str:
    """Remove only whitespace while preserving every other character exactly and in order."""
    return re.sub(r"\s+", "", value)


def text_matches_expected(observed: str, expected: str) -> bool:
    observed_compact = compact_non_whitespace(base.normalize_text(observed))
    expected_compact = compact_non_whitespace(base.normalize_text(expected))

    if observed_compact == expected_compact:
        return True

    # ChatGPT may render the leading literal @GitHub token as a mention object. Its accessible
    # clipboard representation then begins with GitHub while preserving every remaining character.
    if expected_compact.startswith("@GitHub"):
        return observed_compact == expected_compact[1:]

    return False


base.text_matches_expected = text_matches_expected
main = base.main


if __name__ == "__main__":
    raise SystemExit(main())
