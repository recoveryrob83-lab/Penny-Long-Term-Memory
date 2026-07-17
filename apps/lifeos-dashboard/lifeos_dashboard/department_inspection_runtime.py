"""Runtime policy tuning for the Department Inspection parser.

The core parser intentionally accepts broad legacy Markdown shapes. This module
applies the stricter display-time policy learned from the first live repository
inspection without mutating any source records.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

from . import department_inspection as parser


if not getattr(parser, "_RUNTIME_POLICY_TUNED", False):
    # Underscores are meaningful inside file names and identifiers. Treating them
    # as generic Markdown decoration corrupted visible source references.
    parser.MARKDOWN_DECORATION = re.compile(r"[`*~]")

    _original_parse_open_loops = parser.DepartmentInspectionSource._parse_open_loops
    _original_findings = parser.DepartmentInspectionSource._findings

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

    parser.DepartmentInspectionSource._parse_open_loops = _parse_open_loops
    parser.DepartmentInspectionSource._findings = _findings
    parser._RUNTIME_POLICY_TUNED = True
