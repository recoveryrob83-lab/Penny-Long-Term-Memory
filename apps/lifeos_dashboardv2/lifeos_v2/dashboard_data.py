"""Read-only dashboard models. Live connectors remain deliberately opt-in."""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path


def overview_model() -> dict:
    now = datetime.now(UTC).isoformat()
    return {
        "generated_at": now,
        "fixture_backed": True,
        "sources": [
            {"name": "LifeOS server", "state": "healthy", "detail": "Local API available", "last_success": now},
            {"name": "GitHub", "state": "partial", "detail": "Configured paths; live token not set", "last_success": now},
            {"name": "Todoist", "state": "unavailable", "detail": "Fixture view — configure token to refresh", "last_success": None},
            {"name": "Calendar", "state": "stale", "detail": "Fixture view — primary calendar only", "last_success": "2026-07-29T12:00:00+00:00"},
            {"name": "Trello", "state": "healthy", "detail": "LifeOS Flow Board fixture", "last_success": now},
            {"name": "Google Drive", "state": "healthy", "detail": "Curated shortcuts only", "last_success": now},
        ],
        "today": {"date": "Today", "next_event": {"title": "LifeOS planning block", "time": "2:00 PM", "location": "Primary calendar", "url": "https://calendar.google.com"}, "tasks": [
            {"title": "Review V2 dashboard", "priority": "P1", "due": "Due today", "url": "https://todoist.com"},
            {"title": "Recovery walk", "priority": "P2", "due": "No due time", "url": "https://todoist.com"},
        ]},
        "flow": {"now": {"title": "LifeOS Version Two", "detail": "Build the advisory handoff loop", "url": "https://trello.com/b/QKXdwHup/lifeos-flow-board"}, "next": [{"title": "Review Slice Two", "url": "https://trello.com/b/QKXdwHup/lifeos-flow-board"}], "waiting": [{"title": "Route registration", "url": "https://trello.com/b/QKXdwHup/lifeos-flow-board"}]},
        "attention": [{"count": 1, "label": "Needs review", "detail": "Two legacy advisories need V2 contract fields."}, {"count": 0, "label": "Transport failures", "detail": "No fixture failures."}],
        "shortcuts": [{"title": "LifeOS Pointer Registry", "detail": "Working records directory", "url": "https://drive.google.com"}, {"title": "Chief Engineering Penny", "detail": "Approved visual references", "url": "https://drive.google.com"}],
        "github": {"open_advisories": [{"title": "Legacy advisory records", "detail": "Malformed records isolated from healthy dashboard panels.", "url": "https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory/blob/main/coordination/ADVISORY_INDEX.md"}], "open_loops": [{"title": "V2 dashboard review", "detail": "Engineering-owned implementation", "url": "https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory/tree/main/projects/engineering"}], "activity": [{"title": "V2 server contracts", "detail": "Slice One accepted", "url": "https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory/tree/main/apps/lifeos_dashboardv2"}]},
    }


def inspector_model(root: Path) -> dict:
    configured = [
        ("Engineering_HQ", "Operations", "status", "Active", "High", "Engineering V2 status", "projects/engineering/status.md"),
        ("Engineering_HQ", "Knowledge", "note", "Active", "High", "LifeOS V2 Final Design", "projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md"),
        ("System", "Findings", "finding", "Open", "Normal", "Legacy advisory records need V2 fields", "coordination/ADVISORY_INDEX.md"),
        ("Maintenance_HQ", "Operations", "rule", "Active", "Normal", "Startup Boot", "memory/STARTUP_BOOT.md"),
    ]
    records = []
    for department, category, record_type, state, priority, title, path in configured:
        file = root / path
        raw = file.read_text(encoding="utf-8") if file.exists() else "Configured source not present locally."
        records.append({"department": department, "category": category, "record_type": record_type, "state": state, "priority": priority, "title": title, "summary": raw.splitlines()[0][:180], "authority": "Authoritative" if category != "Findings" else "Review prompt", "confidence": "high", "date": "2026-07-29", "warnings": ["Legacy record is not dispatchable until it supplies Scope and Updated At."] if category == "Findings" else [], "source_path": path, "source_url": f"https://github.com/recoveryrob83-lab/Penny-Long-Term-Memory/blob/main/{path}", "raw": raw[:4000]})
    return {"records": records, "generated_at": datetime.now(UTC).isoformat(), "configured_paths": [item[-1] for item in configured]}
