"""Bounded Markdown reader for the Advisory Index and referenced source records."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .contracts import Advisory, AdvisoryState

_INDEX = re.compile(r"^-\s+(ADV-[\w-]+).*?`(?P<path>coordination/boards/[^`]+\.md)`", re.M)
_FIELD = re.compile(r"^-[ \t]+(?P<name>[^:\r\n]+):[ \t]*(?P<value>[^\r\n]*)$", re.M)
# Accept canonical em dashes and the legacy mojibake sequence in historical fixtures.
_HEADING = re.compile(r"^#{2,4}\s+(?P<id>ADV-[\w-]+)\s+(?:[-\u2014]|\u00e2\u20ac\u201d)+\s*(?P<summary>.+)$", re.M)
_ENVELOPE_HEADING = re.compile(r"^####\s+V2 Courier Envelope\s*$", re.M | re.I)
_SUBHEADING = re.compile(r"^####\s+.+$", re.M)
_ROUTE_ID = re.compile(r"^[a-z][a-z0-9_]*$")

_CANONICAL_FIELDS = {
    "advisory revision": "revision",
    "source department": "source_department",
    "target department": "target_department",
    "task summary": "task_summary",
    "authorized scope": "scope",
    "lifecycle state": "state",
    "outcome": "outcome",
    "blocker": "blocker",
    "updated at": "updated_at",
}


class AdvisoryParseError(ValueError):
    pass


def _clean(value: str) -> str:
    return value.strip().strip("`").strip()


def _parse_timestamp(value: str, advisory_id: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AdvisoryParseError(f"{advisory_id}: Updated At must be ISO 8601") from exc
    if parsed.tzinfo is None:
        raise AdvisoryParseError(f"{advisory_id}: Updated At must include a timezone offset")
    return value


def _envelope_body(advisory_body: str, advisory_id: str) -> str:
    heading = _ENVELOPE_HEADING.search(advisory_body)
    if not heading:
        raise AdvisoryParseError(f"{advisory_id}: V2 Courier Envelope subsection not found")
    following = advisory_body[heading.end():]
    next_subheading = _SUBHEADING.search(following)
    return following[: next_subheading.start()] if next_subheading else following


def parse_advisory_document(text: str, advisory_id: str, source_path: str, source_url: str) -> Advisory:
    match = next((m for m in _HEADING.finditer(text) if m.group("id") == advisory_id), None)
    if not match:
        raise AdvisoryParseError(f"{advisory_id}: heading not found")

    following = text[match.end():]
    next_heading = _HEADING.search(following)
    advisory_body = following[: next_heading.start()] if next_heading else following
    body = _envelope_body(advisory_body, advisory_id)

    collected: dict[str, list[str]] = {}
    for field_match in _FIELD.finditer(body):
        name = field_match.group("name").strip().lower()
        if name in _CANONICAL_FIELDS:
            collected.setdefault(name, []).append(_clean(field_match.group("value")))

    duplicates = [name for name, values in collected.items() if len(values) > 1]
    if duplicates:
        raise AdvisoryParseError(f"{advisory_id}: duplicate V2 envelope fields: {', '.join(sorted(duplicates))}")

    missing = [name for name in _CANONICAL_FIELDS if name not in collected]
    if missing:
        raise AdvisoryParseError(f"{advisory_id}: missing V2 envelope fields: {', '.join(missing)}")

    values = {_CANONICAL_FIELDS[name]: field_values[0] for name, field_values in collected.items()}
    required_nonempty = ("revision", "source_department", "target_department", "task_summary", "scope", "state", "updated_at")
    empty = [name for name in required_nonempty if not values[name]]
    if empty:
        raise AdvisoryParseError(f"{advisory_id}: empty V2 envelope fields: {', '.join(empty)}")

    try:
        revision = int(values["revision"])
        if revision < 1:
            raise ValueError
        state = AdvisoryState(values["state"].upper())
    except (ValueError, KeyError) as exc:
        raise AdvisoryParseError(f"{advisory_id}: invalid revision or state") from exc

    for field_name in ("source_department", "target_department"):
        if not _ROUTE_ID.fullmatch(values[field_name]):
            raise AdvisoryParseError(f"{advisory_id}: {field_name} must be a lowercase snake_case route identifier")

    updated_at = _parse_timestamp(values["updated_at"], advisory_id)

    return Advisory(
        advisory_id=advisory_id,
        revision=revision,
        source_department=values["source_department"],
        target_department=values["target_department"],
        task_summary=values["task_summary"],
        scope=values["scope"],
        state=state,
        outcome=values["outcome"],
        blocker=values["blocker"],
        updated_at=updated_at,
        source_path=source_path,
        source_url=source_url,
    )


class AdvisoryReader:
    def __init__(self, repository_root: Path, index_path: str, source_url_base: str = "") -> None:
        self.root, self.index_path, self.source_url_base = repository_root, index_path, source_url_base.rstrip("/")

    def read(self) -> tuple[list[Advisory], dict[str, str]]:
        index = (self.root / self.index_path).read_text(encoding="utf-8")
        advisories: list[Advisory] = []
        errors: dict[str, str] = {}
        for item in _INDEX.finditer(index):
            advisory_id, source_path = item.group(0).split()[1], item.group("path")
            try:
                path = self.root / source_path
                source_url = f"{self.source_url_base}/{source_path}" if self.source_url_base else source_path
                advisories.append(parse_advisory_document(path.read_text(encoding="utf-8"), advisory_id, source_path, source_url))
            except (OSError, AdvisoryParseError) as exc:
                errors[advisory_id] = str(exc)
        return advisories, errors
