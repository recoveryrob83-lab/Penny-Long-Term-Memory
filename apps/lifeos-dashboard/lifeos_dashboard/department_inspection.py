"""Read-only normalized Department Inspection source."""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

SCOPES = (
    ("main-assistant", "Main Assistant HQ", "projects/main-assistant"),
    ("logistics", "Logistics HQ", "projects/life-logistics-hq"),
    ("engineering", "Engineering HQ", "projects/engineering"),
    ("business", "Business HQ", "projects/business-development"),
    ("office-leaks", "Office Leaks HQ", "projects/office-leaks-consulting"),
    ("finance", "Finance HQ", "projects/finance-benefits"),
    ("wellness", "Wellness HQ", "projects/wellness"),
)

STATE_MAP: dict[str, tuple[str, str, str | None]] = {
    "priority": (
        "open",
        "high",
        "Legacy field mixes urgency with workflow state.",
    ),
    "active": ("active", "normal", None),
    "open": ("open", "normal", None),
    "waiting": ("waiting", "normal", None),
    "paused": ("paused", "normal", None),
    "blocked": ("blocked", "normal", None),
    "closed": ("completed", "none", None),
    "completed": ("completed", "none", None),
    "done": ("completed", "none", None),
    "parked": (
        "paused",
        "low",
        "Legacy Parked state normalized to paused with low priority.",
    ),
}

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
METADATA = re.compile(
    r"^(Date|Updated|Status|Department|Owner|Project|Purpose):\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
NOTE_DATE = re.compile(r"NOTE-(\d{4})(\d{2})(\d{2})")
TABLE_SEPARATOR = re.compile(r"^\s*:?-{3,}:?\s*$")
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]+\)")
MARKDOWN_DECORATION = re.compile(r"[`*_~]")


class DepartmentInspectionSource:
    """Normalize department and system Markdown into a read-only model."""

    def __init__(self, repo_root: Path | None) -> None:
        self.repo_root = repo_root.resolve() if repo_root else None

    def load(self) -> dict[str, Any]:
        if self.repo_root is None or not self.repo_root.exists():
            return self._empty("Repository root is unavailable.")

        records: list[dict[str, Any]] = []
        source_warnings: list[str] = []

        for department, label, project_path in SCOPES:
            project_root = self.repo_root / project_path
            if not project_root.exists():
                source_warnings.append(
                    f"Missing department project path: {project_path}"
                )
                continue
            records.extend(
                self._department_records(
                    department,
                    label,
                    project_root,
                )
            )

        records.extend(self._system_records())
        findings = self._findings(records)
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "available": True,
            "detail": "Read-only normalized repository inspection.",
            "scopes": self._scope_payload(),
            "records": records,
            "findings": findings,
            "summary": self._summary(records, findings),
            "source_warnings": source_warnings,
        }

    def _empty(self, detail: str) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "available": False,
            "detail": detail,
            "scopes": self._scope_payload(),
            "records": [],
            "findings": [],
            "summary": {
                "records": 0,
                "findings": 0,
                "warnings": 0,
                "by_category": {
                    "work": 0,
                    "knowledge": 0,
                    "operations": 0,
                },
            },
            "source_warnings": [],
        }

    @staticmethod
    def _scope_payload() -> list[dict[str, str]]:
        payload = [
            {"id": item[0], "label": item[1], "scope": "department"}
            for item in SCOPES
        ]
        payload.append({"id": "system", "label": "System", "scope": "system"})
        return payload

    def _department_records(
        self,
        department: str,
        label: str,
        project_root: Path,
    ) -> list[dict[str, Any]]:
        records = self._parse_open_loops(
            department,
            label,
            project_root / "open_loops.md",
            scope="department",
            authority="authoritative",
        )
        records.extend(
            self._parse_sections(
                department,
                label,
                project_root / "status.md",
                scope="department",
                record_type="status",
                subtype="status_update",
                authority="authoritative",
            )
        )
        records.extend(
            self._parse_sections(
                department,
                label,
                project_root / "SESSION_HANDOFF.md",
                scope="department",
                record_type="handoff",
                subtype="session_handoff",
                authority="summary",
            )
        )

        notebook_root = project_root / "notebook"
        if notebook_root.exists():
            for path in sorted(notebook_root.glob("NOTE-*.md"), reverse=True):
                note = self._parse_notebook(department, label, path)
                if note:
                    records.append(note)

        logs_root = project_root / "logs"
        if logs_root.exists():
            for path in sorted(logs_root.glob("*.md"), reverse=True):
                records.extend(
                    self._parse_sections(
                        department,
                        label,
                        path,
                        scope="department",
                        record_type="log",
                        subtype="department_log",
                        authority="authoritative",
                    )
                )
        return records

    def _system_records(self) -> list[dict[str, Any]]:
        assert self.repo_root is not None
        memory = self.repo_root / "memory"
        records = self._parse_open_loops(
            "system",
            "System",
            memory / "05_OPEN_LOOPS.md",
            scope="system",
            authority="authoritative",
        )
        records.extend(
            self._parse_sections(
                "system",
                "System",
                memory / "01_SESSION_HANDOFF.md",
                scope="system",
                record_type="handoff",
                subtype="session_handoff",
                authority="summary",
            )
        )
        records.extend(
            self._parse_sections(
                "system",
                "System",
                memory / "02_BOOT_LOG.md",
                scope="system",
                record_type="log",
                subtype="boot_log",
                authority="historical",
            )
        )
        return records

    def _parse_open_loops(
        self,
        department: str,
        owner: str,
        path: Path,
        *,
        scope: str,
        authority: str,
    ) -> list[dict[str, Any]]:
        text = self._read(path)
        if not text:
            return []
        updated_at = self._metadata(text).get("updated")
        records: list[dict[str, Any]] = []

        for section in self._sections(text, 2, 2):
            semantics = self._section_semantics(section["title"])
            rows = self._table_rows(section["body"])
            if rows:
                for index, row in enumerate(rows):
                    record = self._table_record(
                        department,
                        owner,
                        scope,
                        authority,
                        path,
                        section["title"],
                        semantics,
                        row,
                        updated_at,
                        index,
                    )
                    if record:
                        records.append(record)
                continue

            for index, bullet in enumerate(self._bullets(section["body"])):
                title, summary = self._title_summary(bullet)
                warnings: list[str] = []
                confidence = "high"
                if semantics["record_type"] == "work_item":
                    warnings.append("Priority not explicitly provided.")
                    confidence = "medium"
                records.append(
                    self._record(
                        department=department,
                        scope=scope,
                        record_type=semantics["record_type"],
                        subtype=semantics["subtype"],
                        title=title,
                        summary=summary,
                        state=semantics["state"],
                        priority=semantics["priority"],
                        owner=owner,
                        source_path=self._relative(path),
                        source_section=section["title"],
                        source_format="markdown-bullets",
                        source_authority=authority,
                        raw_text=bullet,
                        parse_confidence=confidence,
                        warnings=warnings,
                        updated_at=updated_at,
                        identity=f"bullet-{index}",
                    )
                )
        return records

    def _table_record(
        self,
        department: str,
        owner: str,
        scope: str,
        authority: str,
        path: Path,
        section_title: str,
        semantics: dict[str, str],
        row: dict[str, str],
        updated_at: str | None,
        index: int,
    ) -> dict[str, Any] | None:
        lowered = {key.casefold(): value for key, value in row.items()}
        title = (
            lowered.get("item")
            or lowered.get("title")
            or lowered.get("open loop")
            or ""
        ).strip()
        if not title:
            return None

        state, priority, warning = self._state_priority(
            lowered.get("status", ""),
            semantics["state"],
            semantics["priority"],
        )
        closed_at = lowered.get("closed date", "").strip() or None
        if closed_at:
            state, priority = "completed", "none"

        summary = " ".join(
            value.strip()
            for value in (
                lowered.get("next action", ""),
                lowered.get("notes", ""),
                lowered.get("detail", ""),
            )
            if value.strip()
        )
        record_type = semantics["record_type"]
        subtype = semantics["subtype"]
        if closed_at or state == "completed":
            record_type, subtype = "milestone", "closed_item"

        return self._record(
            department=department,
            scope=scope,
            record_type=record_type,
            subtype=subtype,
            title=title,
            summary=summary or title,
            state=state,
            priority=priority,
            owner=owner,
            source_path=self._relative(path),
            source_section=section_title,
            source_format="markdown-table",
            source_authority=authority,
            raw_text=" | ".join(row.values()),
            parse_confidence="high",
            warnings=[warning] if warning else [],
            updated_at=updated_at,
            closed_at=closed_at,
            identity=f"table-{index}",
        )

    def _parse_notebook(
        self,
        department: str,
        owner: str,
        path: Path,
    ) -> dict[str, Any] | None:
        text = self._read(path)
        if not text:
            return None
        metadata = self._metadata(text)
        title = self._document_title(text) or path.stem
        source_status = metadata.get("status", "")
        state, warning = self._notebook_state(source_status)
        historical = (
            "historical" in source_status.casefold()
            or "historical" in text[:600].casefold()
        )
        subtype = (
            "validation_record"
            if any(word in title.casefold() for word in ("validation", "test"))
            else "notebook_entry"
        )
        return self._record(
            department=department,
            scope="department",
            record_type="note",
            subtype=subtype,
            title=title,
            summary=self._document_summary(text),
            state=state,
            priority="none",
            owner=metadata.get("owner") or owner,
            source_path=self._relative(path),
            source_section=None,
            source_format="markdown-document",
            source_authority="historical" if historical else "authoritative",
            raw_text=self._compact(text),
            parse_confidence="high" if self._note_date(path.name) else "medium",
            warnings=[warning] if warning else [],
            record_date=metadata.get("date") or self._note_date(path.name),
            updated_at=metadata.get("updated"),
            identity="note",
        )

    def _parse_sections(
        self,
        department: str,
        owner: str,
        path: Path,
        *,
        scope: str,
        record_type: str,
        subtype: str,
        authority: str,
    ) -> list[dict[str, Any]]:
        text = self._read(path)
        if not text:
            return []
        updated_at = self._metadata(text).get("updated")
        records: list[dict[str, Any]] = []

        for index, section in enumerate(self._sections(text, 2, 3)):
            body = section["body"].strip()
            if not body:
                continue
            source_status = self._field(body, "Status")
            state, warning = self._document_state(source_status)
            records.append(
                self._record(
                    department=department,
                    scope=scope,
                    record_type=record_type,
                    subtype=subtype,
                    title=section["title"],
                    summary=self._body_summary(body),
                    state=state,
                    priority="none",
                    owner=owner,
                    source_path=self._relative(path),
                    source_section=section["title"],
                    source_format="markdown-document",
                    source_authority=authority,
                    raw_text=self._compact(body),
                    parse_confidence="high" if updated_at else "medium",
                    warnings=[warning] if warning else [],
                    updated_at=updated_at,
                    identity=f"section-{index}",
                )
            )
        return records

    def _record(
        self,
        *,
        department: str,
        scope: str,
        record_type: str,
        subtype: str,
        title: str,
        summary: str,
        state: str,
        priority: str,
        owner: str | None,
        source_path: str,
        source_section: str | None,
        source_format: str,
        source_authority: str,
        raw_text: str,
        parse_confidence: str,
        warnings: list[str],
        identity: str,
        record_date: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        due_at: str | None = None,
        closed_at: str | None = None,
    ) -> dict[str, Any]:
        clean_title = self._clean(title) or "Untitled record"
        key = (
            f"{department}|{source_path}|{source_section}|"
            f"{clean_title}|{identity}"
        )
        digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]
        slug = self._slug(clean_title)[:56] or "record"
        return {
            "id": f"{department}:{record_type}:{slug}-{digest}",
            "schema_version": SCHEMA_VERSION,
            "department": department,
            "scope": scope,
            "record_type": record_type,
            "subtype": subtype,
            "title": clean_title,
            "summary": self._clean(summary),
            "state": state,
            "priority": priority,
            "owner": owner,
            "cross_department": False,
            "related_departments": [],
            "dependency_type": None,
            "record_date": self._date(record_date),
            "created_at": self._date(created_at),
            "updated_at": self._date(updated_at),
            "due_at": self._date(due_at),
            "closed_at": self._date(closed_at),
            "tags": [],
            "source_path": source_path,
            "source_section": source_section,
            "source_format": source_format,
            "source_authority": source_authority,
            "raw_text": raw_text.strip(),
            "parse_confidence": parse_confidence,
            "warnings": [item for item in warnings if item],
        }

    def _findings(
        self,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        for record in records:
            if any("mixes urgency" in item for item in record["warnings"]):
                findings.append(
                    self._finding(
                        "state_priority_mixed",
                        "medium",
                        [record],
                        "A legacy status mixes urgency with workflow state.",
                    )
                )

        candidates = [
            record
            for record in records
            if record["record_type"] in {"work_item", "milestone"}
            and len(record["title"]) >= 18
        ]
        for index, left in enumerate(candidates):
            for right in candidates[index + 1 :]:
                if left["source_path"] == right["source_path"]:
                    continue
                ratio = SequenceMatcher(
                    None,
                    self._compare(left["title"]),
                    self._compare(right["title"]),
                ).ratio()
                if ratio < 0.92:
                    continue
                states = {left["state"], right["state"]}
                departments = {left["department"], right["department"]}
                unfinished = {"open", "active", "waiting", "paused", "blocked"}
                finished = {"completed", "closed"}
                if (
                    "system" in departments
                    and states & unfinished
                    and states & finished
                ):
                    findings.append(
                        self._finding(
                            "stale_mirror",
                            "high",
                            [left, right],
                            "Possible stale mirror: similar work is closed "
                            "in one source but unfinished in another.",
                        )
                    )
                else:
                    findings.append(
                        self._finding(
                            "possible_duplicate",
                            "medium",
                            [left, right],
                            "Possible duplicate records have nearly "
                            "identical titles.",
                        )
                    )

        return list({finding["id"]: finding for finding in findings}.values())

    @staticmethod
    def _finding(
        anomaly_type: str,
        severity: str,
        records: list[dict[str, Any]],
        summary: str,
    ) -> dict[str, Any]:
        record_ids = sorted(record["id"] for record in records)
        key = f"{anomaly_type}|{'|'.join(record_ids)}"
        digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]
        return {
            "id": f"finding:{anomaly_type}:{digest}",
            "schema_version": SCHEMA_VERSION,
            "anomaly_type": anomaly_type,
            "severity": severity,
            "records": record_ids,
            "departments": sorted(
                {record["department"] for record in records}
            ),
            "summary": summary,
        }

    @staticmethod
    def _summary(
        records: list[dict[str, Any]],
        findings: list[dict[str, Any]],
    ) -> dict[str, Any]:
        categories = {"work": 0, "knowledge": 0, "operations": 0}
        for record in records:
            categories[DepartmentInspectionSource.category(
                record["record_type"]
            )] += 1
        return {
            "records": len(records),
            "findings": len(findings),
            "warnings": sum(bool(record["warnings"]) for record in records),
            "by_category": categories,
        }

    @staticmethod
    def category(record_type: str) -> str:
        if record_type in {"work_item", "milestone"}:
            return "work"
        if record_type in {"note", "decision"}:
            return "knowledge"
        return "operations"

    @staticmethod
    def _section_semantics(title: str) -> dict[str, str]:
        value = title.casefold()
        if any(word in value for word in ("done", "closed", "completed")):
            return {
                "record_type": "milestone",
                "subtype": "closed_item",
                "state": "completed",
                "priority": "none",
            }
        if (
            "standing" in value
            or "operating rule" in value
            or "completion standard" in value
        ):
            return {
                "record_type": "rule",
                "subtype": "standing_rule",
                "state": "active",
                "priority": "none",
            }
        if "watch" in value:
            return {
                "record_type": "watch",
                "subtype": "operating_watch",
                "state": "active",
                "priority": "none",
            }
        if "parking" in value or "parked" in value:
            return {
                "record_type": "work_item",
                "subtype": "parking_lot",
                "state": "paused",
                "priority": "low",
            }
        if "waiting" in value or "deferred" in value:
            return {
                "record_type": "work_item",
                "subtype": "waiting_item",
                "state": "waiting",
                "priority": "normal",
            }
        return {
            "record_type": "work_item",
            "subtype": "open_loop",
            "state": "open",
            "priority": "normal",
        }

    @staticmethod
    def _state_priority(
        source: str,
        default_state: str,
        default_priority: str,
    ) -> tuple[str, str, str | None]:
        value = source.strip().casefold()
        if not value:
            return default_state, default_priority, None
        return STATE_MAP.get(
            value,
            (
                default_state,
                default_priority,
                f"Unrecognized source status: {source.strip()}",
            ),
        )

    @staticmethod
    def _notebook_state(source: str) -> tuple[str, str | None]:
        value = source.casefold()
        if not value:
            return "unknown", "Notebook status not explicitly provided."
        if any(word in value for word in ("closed", "completed", "done")):
            return "completed", None
        if any(
            word in value
            for word in ("active", "approved", "implementation-ready")
        ):
            return "active", None
        if any(word in value for word in ("draft", "planned", "planning")):
            return "open", None
        if "historical" in value:
            return "completed", None
        return "unknown", f"Unrecognized notebook status: {source}"

    @staticmethod
    def _document_state(source: str | None) -> tuple[str, str | None]:
        if not source:
            return "unknown", None
        value = source.casefold()
        if any(word in value for word in ("implemented", "operational", "active")):
            return "active", None
        if "paused" in value:
            return "paused", None
        if "waiting" in value or "deferred" in value:
            return "waiting", None
        if "closed" in value or "completed" in value:
            return "completed", None
        return "unknown", f"Unrecognized explicit status: {source}"

    @staticmethod
    def _sections(
        text: str,
        minimum_level: int,
        maximum_level: int,
    ) -> list[dict[str, str | int]]:
        matches = [
            match
            for match in HEADING.finditer(text)
            if minimum_level <= len(match.group(1)) <= maximum_level
        ]
        sections: list[dict[str, str | int]] = []
        for index, match in enumerate(matches):
            end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(text)
            )
            sections.append(
                {
                    "level": len(match.group(1)),
                    "title": DepartmentInspectionSource._clean(match.group(2)),
                    "body": text[match.end():end].strip(),
                }
            )
        return sections

    @staticmethod
    def _table_rows(body: str) -> list[dict[str, str]]:
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        for index in range(len(lines) - 1):
            if "|" not in lines[index] or "|" not in lines[index + 1]:
                continue
            headers = DepartmentInspectionSource._cells(lines[index])
            separators = DepartmentInspectionSource._cells(lines[index + 1])
            if not headers or len(headers) != len(separators):
                continue
            if not all(TABLE_SEPARATOR.match(cell) for cell in separators):
                continue

            rows: list[dict[str, str]] = []
            for line in lines[index + 2:]:
                if "|" not in line:
                    break
                cells = DepartmentInspectionSource._cells(line)
                if len(cells) == len(headers):
                    rows.append(dict(zip(headers, cells, strict=True)))
            return rows
        return []

    @staticmethod
    def _cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    @staticmethod
    def _bullets(body: str) -> list[str]:
        return [
            line.strip()[2:].strip()
            for line in body.splitlines()
            if line.strip().startswith("- ")
        ]

    @staticmethod
    def _metadata(text: str) -> dict[str, str]:
        return {
            match.group(1).casefold(): match.group(2).strip()
            for match in METADATA.finditer(text[:1200])
        }

    @staticmethod
    def _field(text: str, name: str) -> str | None:
        match = re.search(
            rf"^{re.escape(name)}:\s*(.+?)\s*$",
            text,
            re.IGNORECASE | re.MULTILINE,
        )
        return match.group(1).strip() if match else None

    @staticmethod
    def _document_title(text: str) -> str | None:
        match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
        return (
            DepartmentInspectionSource._clean(match.group(1))
            if match
            else None
        )

    @staticmethod
    def _document_summary(text: str) -> str:
        for paragraph in re.split(r"\n\s*\n", text):
            value = paragraph.strip()
            if not value or value.startswith("#"):
                continue
            if all(METADATA.match(line) for line in value.splitlines()):
                continue
            summary = DepartmentInspectionSource._body_summary(value)
            if summary:
                return summary
        return "No summary available."

    @staticmethod
    def _body_summary(body: str) -> str:
        lines: list[str] = []
        for line in body.splitlines():
            value = line.strip()
            if not value or value.startswith(("```", "#", "|---")):
                continue
            value = re.sub(r"^[-*\d.]+\s+", "", value)
            lines.append(value)
            if sum(len(item) for item in lines) >= 280:
                break
        return DepartmentInspectionSource._clean(" ".join(lines))[:360]

    @staticmethod
    def _title_summary(text: str) -> tuple[str, str]:
        value = DepartmentInspectionSource._clean(text)
        if ":" in value:
            title, summary = value.split(":", 1)
            if 4 <= len(title) <= 90 and summary.strip():
                return title.strip(), summary.strip()
        title = value if len(value) <= 140 else f"{value[:137].rstrip()}..."
        return title, value

    @staticmethod
    def _compact(text: str, limit: int = 900) -> str:
        value = re.sub(r"\s+", " ", text).strip()
        return value if len(value) <= limit else f"{value[:limit - 3].rstrip()}..."

    @staticmethod
    def _clean(value: str) -> str:
        value = MARKDOWN_LINK.sub(r"\1", value)
        value = MARKDOWN_DECORATION.sub("", value)
        return re.sub(r"\s+", " ", value).strip()

    @staticmethod
    def _slug(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")

    @staticmethod
    def _compare(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()

    @staticmethod
    def _date(value: str | None) -> str | None:
        if not value:
            return None
        match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", value)
        return match.group(1) if match else value.strip()

    @staticmethod
    def _note_date(filename: str) -> str | None:
        match = NOTE_DATE.search(filename)
        if not match:
            return None
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    def _relative(self, path: Path) -> str:
        assert self.repo_root is not None
        return path.relative_to(self.repo_root).as_posix()

    @staticmethod
    def _read(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return ""
