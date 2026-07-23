"""Runtime policy tuning for the Department Inspection parser.

The core parser intentionally accepts broad legacy Markdown shapes. This module
applies the stricter display-time policy learned from live repository inspection
without mutating any source records.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

from . import department_inspection as parser
from .room_titles import CANONICAL_HQ_TITLES


if not getattr(parser, "_RUNTIME_POLICY_TUNED", False):
    # Underscores are meaningful inside file names and identifiers. Treating them
    # as generic Markdown decoration corrupted visible source references.
    parser.MARKDOWN_DECORATION = re.compile(r"[`*~]")

    # Scope IDs and project paths are stable compatibility identifiers. Presentation
    # labels use the canonical exact ChatGPT room titles through an explicit key bridge.
    _scope_title_keys = {"main-assistant": "main"}
    parser.SCOPES = tuple(
        (
            scope_id,
            CANONICAL_HQ_TITLES.get(_scope_title_keys.get(scope_id, scope_id), label),
            project_path,
        )
        for scope_id, label, project_path in parser.SCOPES
    )

    _original_parse_open_loops = parser.DepartmentInspectionSource._parse_open_loops
    _original_parse_notebook = parser.DepartmentInspectionSource._parse_notebook
    _original_table_record = parser.DepartmentInspectionSource._table_record
    _original_notebook_state = parser.DepartmentInspectionSource._notebook_state
    _original_findings = parser.DepartmentInspectionSource._findings

    _priority_map = {
        "critical": "critical",
        "high": "high",
        "medium": "normal",
        "normal": "normal",
        "low": "low",
        "none": "none",
        "unknown": "unknown",
    }

    def _notebook_state(source: str) -> tuple[str, str | None]:
        """Normalize only notebook statuses observed in the live repository."""
        value = source.strip().casefold()
        if not value:
            return _original_notebook_state(source)
        if "blocked" in value:
            return "blocked", None
        if (
            "success" in value
            or value in {"pass", "passed"}
            or "validated in production-like watched testing" in value
        ):
            return "completed", None
        if "deferred" in value or "captured for later" in value or "waiting" in value:
            return "waiting", None
        if value == "open" or "raw" in value or "unprocessed" in value:
            return "open", None
        return _original_notebook_state(source)

    def _parse_notebook(
        self: parser.DepartmentInspectionSource,
        department: str,
        owner: str,
        path: Any,
    ) -> dict[str, Any] | None:
        """Honor an exact Status field anywhere in a notebook document.

        The base metadata scan is intentionally bounded to the document header.
        Experiment notes sometimes place their authoritative Status field under a
        later Result section, so a whole-document exact-field lookup is needed.
        """
        record = _original_parse_notebook(self, department, owner, path)
        if record is None:
            return None

        text = self._read(path)
        exact_status = self._field(text, "Status")
        if not exact_status:
            return record

        state, warning = self._notebook_state(exact_status)
        record["state"] = state
        record["warnings"] = [
            item
            for item in record.get("warnings", [])
            if not (
                item == "Notebook status not explicitly provided."
                or item.startswith("Unrecognized notebook status:")
            )
        ]
        if warning:
            record["warnings"].append(warning)
        if "historical" in exact_status.casefold():
            record["source_authority"] = "historical"
        return record

    def _table_record(
        self: parser.DepartmentInspectionSource,
        department: str,
        owner: str,
        scope: str,
        authority: str,
        path: Any,
        section_title: str,
        semantics: dict[str, str],
        row: dict[str, str],
        updated_at: str | None,
        index: int,
    ) -> dict[str, Any] | None:
        record = _original_table_record(
            self,
            department,
            owner,
            scope,
            authority,
            path,
            section_title,
            semantics,
            row,
            updated_at,
            index,
        )
        if record is None:
            return None

        explicit_priority = next(
            (
                value.strip()
                for key, value in row.items()
                if key.strip().casefold() == "priority" and value.strip()
            ),
            "",
        )
        if not explicit_priority:
            return record

        normalized = _priority_map.get(explicit_priority.casefold())
        if normalized is None:
            record["priority"] = "unknown"
            record.setdefault("warnings", []).append(
                f"Unrecognized explicit priority: {explicit_priority}"
            )
            record["parse_confidence"] = "medium"
        else:
            record["priority"] = normalized
        return record

    def _parse_open_loops(
        self: parser.DepartmentInspectionSource,
        department: str,
        owner: str,
        path: Any,
        *,
        scope: str,
        authority: str,
    ) -> list[dict[str, Any]]:
        records = _original_parse_open_loops(
            self,
            department,
            owner,
            path,
            scope=scope,
            authority=authority,
        )
        for record in records:
            if (
                record.get("source_format") == "markdown-bullets"
                and record.get("record_type") == "work_item"
            ):
                record["warnings"] = [
                    warning
                    for warning in record.get("warnings", [])
                    if warning != "Priority not explicitly provided."
                ]
                if record.get("priority") == "normal":
                    record["priority"] = "unknown"
                record["parse_confidence"] = "medium"
        return records

    def _findings(
        self: parser.DepartmentInspectionSource,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        findings = _original_findings(self, records)
        by_id = {record["id"]: record for record in records}
        filtered: list[dict[str, Any]] = []

        for finding in findings:
            if finding.get("anomaly_type") != "possible_duplicate":
                filtered.append(finding)
                continue

            related = [
                by_id[record_id]
                for record_id in finding.get("records", [])
                if record_id in by_id
            ]
            if len(related) != 2:
                filtered.append(finding)
                continue

            left, right = related
            departments = {left.get("department"), right.get("department")}
            if "system" in departments or len(departments) == 1:
                filtered.append(finding)
                continue

            left_summary = parser.DepartmentInspectionSource._compare(
                left.get("summary", "")
            )
            right_summary = parser.DepartmentInspectionSource._compare(
                right.get("summary", "")
            )
            summary_ratio = SequenceMatcher(
                None,
                left_summary,
                right_summary,
            ).ratio()
            if summary_ratio >= 0.72:
                filtered.append(finding)

        return filtered

    parser.DepartmentInspectionSource._notebook_state = staticmethod(_notebook_state)
    parser.DepartmentInspectionSource._parse_notebook = _parse_notebook
    parser.DepartmentInspectionSource._table_record = _table_record
    parser.DepartmentInspectionSource._parse_open_loops = _parse_open_loops
    parser.DepartmentInspectionSource._findings = _findings
    parser._RUNTIME_POLICY_TUNED = True
