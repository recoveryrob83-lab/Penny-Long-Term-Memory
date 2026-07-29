"""Bounded Markdown reader for the Advisory Index and referenced source records."""
from __future__ import annotations

import re
from pathlib import Path

from .contracts import Advisory, AdvisoryState

_INDEX = re.compile(r"^-\s+(ADV-[\w-]+).*?`(?P<path>coordination/boards/[^`]+\.md)`", re.M)
_HEADING = re.compile(r"^#{2,4}\s+(?P<id>ADV-[\w-]+)\s+[—-]+\s*(?P<summary>.+)$", re.M)
_FIELD = re.compile(r"^-\s+(?P<name>[^:]+):\s*(?P<value>.*)$", re.M)
# Accept canonical em dashes and the legacy mojibake sequence in historical fixtures.
_HEADING = re.compile(r"^#{2,4}\s+(?P<id>ADV-[\w-]+)\s+(?:[-\u2014]|\u00e2\u20ac\u201d)+\s*(?P<summary>.+)$", re.M)


class AdvisoryParseError(ValueError):
    pass


def _clean(value: str) -> str:
    return value.strip().strip("`").strip()


def parse_advisory_document(text: str, advisory_id: str, source_path: str, source_url: str) -> Advisory:
    match = next((m for m in _HEADING.finditer(text) if m.group("id") == advisory_id), None)
    if not match:
        raise AdvisoryParseError(f"{advisory_id}: heading not found")
    following = text[match.end():]
    next_heading = _HEADING.search(following)
    body = following[: next_heading.start()] if next_heading else following
    fields = {m.group("name").strip().lower(): _clean(m.group("value")) for m in _FIELD.finditer(body)}
    values = {
        "revision": fields.get("advisory revision", fields.get("revision", "")),
        "source_department": fields.get("source department", fields.get("from", "")),
        "target_department": fields.get("target department", fields.get("target department and owner", fields.get("to", ""))),
        "scope": fields.get("scope", fields.get("authorized scope", "")),
        "state": fields.get("lifecycle state", fields.get("state", "")),
        "updated_at": fields.get("updated at", fields.get("updated", "")),
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise AdvisoryParseError(f"{advisory_id}: missing V2 fields: {', '.join(missing)}")
    try:
        state = AdvisoryState(values["state"].upper())
        revision = int(values["revision"])
    except (ValueError, KeyError) as exc:
        raise AdvisoryParseError(f"{advisory_id}: invalid revision or state") from exc
    return Advisory(
        advisory_id=advisory_id, revision=revision, source_department=values["source_department"],
        target_department=values["target_department"], task_summary=match.group("summary").strip(),
        scope=values["scope"], state=state, outcome=fields.get("outcome", ""),
        blocker=fields.get("blocker", ""), updated_at=values["updated_at"],
        source_path=source_path, source_url=source_url,
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
