from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from lifeos_dashboard.adapters import (
    GoogleCalendarIcalDashboardSource,
    LocalGitHubDashboardSource,
)
from lifeos_dashboard.main import build_default_source


class StaticDashboardSource:
    name = "static"

    def load(self) -> dict[str, Any]:
        return deepcopy(
            {
                "meta": {"status": "sample"},
                "sources": [
                    {
                        "name": "GitHub",
                        "state": "healthy",
                        "freshness": "sample data",
                    },
                    {
                        "name": "Trello",
                        "state": "healthy",
                        "freshness": "sample data",
                    },
                ],
                "flow": {"now": {"title": "Keep this fallback panel"}},
                "notebooks": [],
            }
        )


def write_checkout_fixture(repo_root: Path) -> None:
    (repo_root / ".git").mkdir(parents=True)
    (repo_root / "coordination").mkdir()
    (repo_root / "memory").mkdir()
    notebook_dir = repo_root / "projects" / "engineering" / "notebook"
    notebook_dir.mkdir(parents=True)

    (repo_root / "coordination" / "ADVISORY_INDEX.md").write_text(
        """# Advisory Index

## Open / Unacknowledged Advisories

- ADV-20260717-040 — Test the live dashboard adapter.

## Acknowledged / Implemented Advisories

- None.
""",
        encoding="utf-8",
    )
    (repo_root / "memory" / "05_OPEN_LOOPS.md").write_text(
        """# Open Loops

## Priority Open Loops

- Main Assistant / Daily Operations: Keep the conversational hub moving.
- Chief Engineering Penny: Validate the live GitHub panel.

## Waiting On

- Nothing for this fixture.
""",
        encoding="utf-8",
    )
    (notebook_dir / "NOTE-20260717-008-live-dashboard.md").write_text(
        """# Live Dashboard Adapter

Status: Active reference

The dashboard now reads meaningful LifeOS state from the local checkout.
""",
        encoding="utf-8",
    )


def test_local_github_source_overlays_live_checkout_state(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_checkout_fixture(tmp_path)
    source = LocalGitHubDashboardSource(tmp_path, StaticDashboardSource())

    def fake_git(*args: str) -> str | None:
        responses = {
            ("rev-parse", "--abbrev-ref", "HEAD"): "main",
            ("rev-parse", "--short", "HEAD"): "abc1234",
            ("log", "-1", "--format=%cI"): "2026-07-17T02:00:00+00:00",
            ("status", "--porcelain"): "",
        }
        if args in responses:
            return responses[args]
        if args[:2] == ("log", "-4"):
            return (
                "abc1234\x1f2026-07-17T02:00:00+00:00\x1f"
                "Synchronize dashboard state"
            )
        return None

    monkeypatch.setattr(source, "_run_git", fake_git)
    payload = source.load()

    assert payload["meta"]["status"] == "live local checkout"
    assert payload["flow"]["now"]["title"] == "Keep this fallback panel"
    assert payload["sources"][0] == {
        "name": "GitHub",
        "state": "healthy",
        "freshness": "main · abc1234 · clean",
    }
    assert payload["github"]["branch"] == "main"
    assert payload["github"]["working_tree"] == "clean"
    assert payload["github"]["sync"]["status"] == "disabled"
    assert payload["github"]["open_advisories"][0]["title"] == "ADV-20260717-040"
    assert payload["github"]["open_loops"][0]["title"] == (
        "Main Assistant / Daily Operations"
    )
    assert payload["github"]["recent_activity"][0]["title"] == (
        "Synchronize dashboard state"
    )
    assert payload["notebooks"][0]["title"] == "Live Dashboard Adapter"
    assert payload["notebooks"][0]["status"] == "Active reference"


def test_guarded_auto_sync_fast_forwards_clean_main(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_checkout_fixture(tmp_path)
    source = LocalGitHubDashboardSource(
        tmp_path,
        StaticDashboardSource(),
        auto_sync=True,
    )
    calls: list[tuple[str, ...]] = []
    merged = False

    def fake_git(*args: str) -> str | None:
        nonlocal merged
        calls.append(args)
        if args == ("rev-parse", "--abbrev-ref", "HEAD"):
            return "main"
        if args == ("status", "--porcelain"):
            return ""
        if args == ("fetch", "--quiet", "origin"):
            return ""
        if args == ("rev-parse", "--verify", "origin/main"):
            return "def5678"
        if args == (
            "rev-list",
            "--left-right",
            "--count",
            "HEAD...origin/main",
        ):
            return "0\t2"
        if args == ("merge", "--ff-only", "origin/main"):
            merged = True
            return "Updating abc1234..def5678"
        if args == ("rev-parse", "--short", "HEAD"):
            return "def5678" if merged else "abc1234"
        if args == ("log", "-1", "--format=%cI"):
            return "2026-07-17T03:00:00+00:00"
        if args[:2] == ("log", "-4"):
            return (
                "def5678\x1f2026-07-17T03:00:00+00:00\x1f"
                "Fast-forward LifeOS memory"
            )
        return None

    monkeypatch.setattr(source, "_run_git", fake_git)
    payload = source.load()

    assert ("fetch", "--quiet", "origin") in calls
    assert ("merge", "--ff-only", "origin/main") in calls
    assert payload["sources"][0] == {
        "name": "GitHub",
        "state": "healthy",
        "freshness": "main · def5678 · clean · synced 2 commits",
    }
    assert payload["github"]["sync"] == {
        "status": "synced",
        "detail": "Fast-forwarded 2 commits from origin/main.",
        "changed": True,
        "commits": 2,
    }


def test_guarded_auto_sync_refuses_dirty_checkout(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_checkout_fixture(tmp_path)
    source = LocalGitHubDashboardSource(
        tmp_path,
        StaticDashboardSource(),
        auto_sync=True,
    )
    calls: list[tuple[str, ...]] = []

    def fake_git(*args: str) -> str | None:
        calls.append(args)
        responses = {
            ("rev-parse", "--abbrev-ref", "HEAD"): "main",
            ("rev-parse", "--short", "HEAD"): "abc1234",
            ("log", "-1", "--format=%cI"): "2026-07-17T02:00:00+00:00",
            ("status", "--porcelain"): "?? generated-file.txt",
        }
        return responses.get(args)

    monkeypatch.setattr(source, "_run_git", fake_git)
    payload = source.load()

    assert not any(call and call[0] == "fetch" for call in calls)
    assert not any(call and call[0] == "merge" for call in calls)
    assert payload["sources"][0] == {
        "name": "GitHub",
        "state": "partial",
        "freshness": (
            "main · abc1234 · 1 local change · "
            "sync blocked: local changes present"
        ),
    }
    assert payload["github"]["sync"]["status"] == "blocked"
    assert payload["github"]["sync"]["detail"] == "local changes present"


def test_guarded_auto_sync_refuses_diverged_history(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_checkout_fixture(tmp_path)
    source = LocalGitHubDashboardSource(
        tmp_path,
        StaticDashboardSource(),
        auto_sync=True,
    )
    calls: list[tuple[str, ...]] = []

    def fake_git(*args: str) -> str | None:
        calls.append(args)
        responses = {
            ("rev-parse", "--abbrev-ref", "HEAD"): "main",
            ("rev-parse", "--short", "HEAD"): "abc1234",
            ("log", "-1", "--format=%cI"): "2026-07-17T02:00:00+00:00",
            ("status", "--porcelain"): "",
            ("fetch", "--quiet", "origin"): "",
            ("rev-parse", "--verify", "origin/main"): "def5678",
            (
                "rev-list",
                "--left-right",
                "--count",
                "HEAD...origin/main",
            ): "1 2",
        }
        return responses.get(args)

    monkeypatch.setattr(source, "_run_git", fake_git)
    payload = source.load()

    assert ("fetch", "--quiet", "origin") in calls
    assert not any(call and call[0] == "merge" for call in calls)
    assert payload["sources"][0]["state"] == "partial"
    assert payload["github"]["sync"]["status"] == "blocked"
    assert payload["github"]["sync"]["detail"] == (
        "local and remote histories diverged (1 ahead, 2 behind)"
    )


def test_default_source_detects_configured_checkout(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    write_checkout_fixture(tmp_path)
    monkeypatch.setenv("LIFEOS_REPOSITORY_ROOT", str(tmp_path))
    for name in (
        "TRELLO_API_KEY",
        "TRELLO_API_TOKEN",
        "TRELLO_BOARD_ID",
        "TODOIST_API_TOKEN",
        "GOOGLE_CALENDAR_ICAL_URL",
    ):
        monkeypatch.delenv(name, raising=False)

    source = build_default_source()

    assert isinstance(source, GoogleCalendarIcalDashboardSource)
    assert source.name == "local-github"
