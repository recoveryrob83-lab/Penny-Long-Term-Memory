from pathlib import Path

from lifeos_dashboard.department_inspection import DepartmentInspectionSource


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _base_repository(root: Path) -> None:
    _write(
        root / "memory" / "01_SESSION_HANDOFF.md",
        "# Session Handoff\n\nUpdated: 2026-07-18\n\n## Current\n\nSystem summary.\n",
    )
    _write(
        root / "memory" / "02_BOOT_LOG.md",
        "# Boot Log\n\nUpdated: 2026-07-18\n\n## Durable Lesson\n\nHistory.\n",
    )


def test_priority_table_and_notebook_normalize(tmp_path: Path) -> None:
    _base_repository(tmp_path)
    _write(
        tmp_path / "memory" / "05_OPEN_LOOPS.md",
        "# Open Loops\n\nUpdated: 2026-07-18\n\n## Priority Open Loops\n\n"
        "- System-only coordination item.\n",
    )
    engineering = tmp_path / "projects" / "engineering"
    _write(
        engineering / "open_loops.md",
        "# Engineering HQ Open Loops\n\nUpdated: 2026-07-18\n\n## Open\n\n"
        "| Status | Item | Next Action | Notes |\n"
        "|---|---|---|---|\n"
        "| Priority | Build Department Inspector | Implement parser | Read-only |\n",
    )
    _write(
        engineering / "status.md",
        "# Status\n\nUpdated: 2026-07-18\n\n## Current Phase\n\n"
        "Status: Active\n\nImplementation.\n",
    )
    _write(
        engineering / "SESSION_HANDOFF.md",
        "# Handoff\n\nUpdated: 2026-07-18\n\n## Current Work\n\nImplementation.\n",
    )
    _write(
        engineering / "notebook" / "NOTE-20260718-001-inspector.md",
        "# Inspector Data Contract\n\nDate: 2026-07-18\n"
        "Status: Approved / implementation-ready\nOwner: Engineering HQ\n\n"
        "## Purpose\n\nFreeze the parser contract.\n",
    )

    payload = DepartmentInspectionSource(tmp_path).load()

    record = next(
        item for item in payload["records"]
        if item["title"] == "Build Department Inspector"
    )
    assert record["state"] == "open"
    assert record["priority"] == "high"
    assert record["source_authority"] == "authoritative"
    assert "mixes urgency" in record["warnings"][0]

    note = next(
        item for item in payload["records"]
        if item["title"] == "Inspector Data Contract"
    )
    assert note["record_type"] == "note"
    assert note["record_date"] == "2026-07-18"
    assert note["state"] == "active"
    assert payload["summary"]["records"] >= 4


def test_closed_department_work_can_flag_stale_system_mirror(
    tmp_path: Path,
) -> None:
    _base_repository(tmp_path)
    _write(
        tmp_path / "memory" / "05_OPEN_LOOPS.md",
        "# Open Loops\n\nUpdated: 2026-07-18\n\n## Priority Open Loops\n\n"
        "- Build Department Inspector.\n",
    )
    engineering = tmp_path / "projects" / "engineering"
    _write(
        engineering / "open_loops.md",
        "# Engineering HQ Open Loops\n\nUpdated: 2026-07-18\n\n"
        "## Done / Recently Closed\n\n"
        "| Closed Date | Item | Notes |\n"
        "|---|---|---|\n"
        "| 2026-07-18 | Build Department Inspector | Complete |\n",
    )

    payload = DepartmentInspectionSource(tmp_path).load()

    assert any(
        finding["anomaly_type"] == "stale_mirror"
        for finding in payload["findings"]
    )


def test_unavailable_repository_returns_empty_contract() -> None:
    payload = DepartmentInspectionSource(None).load()

    assert payload["available"] is False
    assert payload["schema_version"] == 1
    assert payload["records"] == []
    assert payload["findings"] == []
