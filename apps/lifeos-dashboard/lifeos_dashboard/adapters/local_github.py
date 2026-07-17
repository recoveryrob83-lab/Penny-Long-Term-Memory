"""Read-mostly adapter for LifeOS state in a local GitHub checkout.

The dashboard reads the repository already managed by GitHub Desktop. When
guarded auto-sync is enabled, it may fetch and fast-forward a clean main branch.
It never merges divergent history, rebases, resets, or discards local work.
"""

from __future__ import annotations

import re
import subprocess
import threading
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .base import DashboardSource

_NOTE_DATE = re.compile(r"NOTE-(\d{4})(\d{2})(\d{2})")
_MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]+\)")
_MARKDOWN_DECORATION = re.compile(r"[`*_]")


@dataclass(frozen=True)
class GitSyncResult:
    """Sanitized outcome from one guarded repository synchronization attempt."""

    status: str
    detail: str
    changed: bool = False
    commits: int = 0

    @property
    def healthy(self) -> bool:
        return self.status in {"disabled", "up-to-date", "synced"}


class LocalGitHubDashboardSource:
    """Overlay packaged sample data with live state from a local checkout."""

    name = "local-github"

    def __init__(
        self,
        repo_root: Path,
        fallback_source: DashboardSource,
        *,
        notebook_limit: int = 5,
        open_loop_limit: int = 5,
        commit_limit: int = 4,
        auto_sync: bool = False,
        sync_branch: str = "main",
    ) -> None:
        self._repo_root = repo_root.resolve()
        self._fallback_source = fallback_source
        self._notebook_limit = notebook_limit
        self._open_loop_limit = open_loop_limit
        self._commit_limit = commit_limit
        self._auto_sync = auto_sync
        self._sync_branch = sync_branch.strip() or "main"
        self._sync_lock = threading.Lock()

    def load(self) -> dict[str, Any]:
        """Return a dashboard payload with the GitHub portions made live."""
        sync_result = self._sync_checkout()
        payload = deepcopy(self._fallback_source.load())
        git_state = self._load_git_state()
        advisories = self._load_open_advisories()
        open_loops = self._load_open_loops()
        notebooks = self._load_notebooks()
        recent_activity = self._load_recent_activity()

        metadata = payload.setdefault("meta", {})
        metadata["status"] = "live local checkout"
        metadata["snapshot_at"] = datetime.now(UTC).isoformat()

        payload["sources"] = self._replace_github_source(
            payload.get("sources", []), git_state, sync_result
        )
        payload["notebooks"] = notebooks
        payload["github"] = {
            "repository": self._repo_root.name,
            "branch": git_state["branch"],
            "head": git_state["head"],
            "working_tree": git_state["working_tree"],
            "last_commit": git_state["last_commit"],
            "sync": {
                "status": sync_result.status,
                "detail": sync_result.detail,
                "changed": sync_result.changed,
                "commits": sync_result.commits,
            },
            "open_advisories": advisories,
            "open_loops": open_loops,
            "recent_activity": recent_activity,
        }
        return payload

    def _replace_github_source(
        self,
        sources: object,
        git_state: dict[str, str],
        sync_result: GitSyncResult,
    ) -> list[dict[str, str]]:
        normalized = (
            [dict(item) for item in sources if isinstance(item, dict)]
            if isinstance(sources, list)
            else []
        )
        state = (
            "healthy"
            if git_state["available"] == "yes" and sync_result.healthy
            else "partial"
        )
        if git_state["available"] == "yes":
            freshness = (
                f"{git_state['branch']} · {git_state['head']} · "
                f"{git_state['working_tree']}"
            )
            sync_label = self._sync_freshness(sync_result)
            if sync_label:
                freshness = f"{freshness} · {sync_label}"
        else:
            freshness = "local files available; Git command unavailable"

        github_source = {
            "name": "GitHub",
            "state": state,
            "freshness": freshness,
        }

        for index, source in enumerate(normalized):
            if str(source.get("name", "")).lower() == "github":
                normalized[index] = github_source
                return normalized

        return [github_source, *normalized]

    @staticmethod
    def _sync_freshness(sync_result: GitSyncResult) -> str:
        if sync_result.status == "disabled":
            return ""
        if sync_result.status == "up-to-date":
            return "up to date"
        if sync_result.status == "synced":
            suffix = "commit" if sync_result.commits == 1 else "commits"
            return f"synced {sync_result.commits} {suffix}"
        if sync_result.status == "blocked":
            return f"sync blocked: {sync_result.detail}"
        return f"sync error: {sync_result.detail}"

    def _sync_checkout(self) -> GitSyncResult:
        if not self._auto_sync:
            return GitSyncResult("disabled", "Automatic GitHub synchronization is disabled.")

        with self._sync_lock:
            return self._sync_checkout_locked()

    def _sync_checkout_locked(self) -> GitSyncResult:
        branch = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
        if branch is None:
            return GitSyncResult("error", "Git is unavailable.")

        if branch != self._sync_branch:
            return GitSyncResult(
                "blocked",
                f"expected {self._sync_branch}; on {branch}",
            )

        status = self._run_git("status", "--porcelain")
        if status is None:
            return GitSyncResult("error", "Working-tree state is unavailable.")
        if status.strip():
            return GitSyncResult("blocked", "local changes present")

        if self._run_git("fetch", "--quiet", "origin") is None:
            return GitSyncResult("error", f"unable to fetch origin/{self._sync_branch}")

        remote_ref = f"origin/{self._sync_branch}"
        if self._run_git("rev-parse", "--verify", remote_ref) is None:
            return GitSyncResult("error", f"{remote_ref} is unavailable")

        counts = self._run_git(
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{remote_ref}",
        )
        parsed_counts = self._parse_ahead_behind(counts)
        if parsed_counts is None:
            return GitSyncResult("error", "unable to compare local and remote history")
        ahead, behind = parsed_counts

        if ahead and behind:
            return GitSyncResult(
                "blocked",
                f"local and remote histories diverged ({ahead} ahead, {behind} behind)",
            )
        if ahead:
            suffix = "commit" if ahead == 1 else "commits"
            return GitSyncResult(
                "blocked",
                f"local branch is ahead by {ahead} {suffix}",
            )
        if behind == 0:
            return GitSyncResult(
                "up-to-date",
                f"{remote_ref} already matches local {self._sync_branch}",
            )

        status_after_fetch = self._run_git("status", "--porcelain")
        if status_after_fetch is None:
            return GitSyncResult("error", "Working-tree state changed unexpectedly.")
        if status_after_fetch.strip():
            return GitSyncResult("blocked", "local changes appeared after fetch")

        if self._run_git("merge", "--ff-only", remote_ref) is None:
            return GitSyncResult("error", "fast-forward update failed")

        final_status = self._run_git("status", "--porcelain")
        if final_status is None or final_status.strip():
            return GitSyncResult("error", "post-sync working-tree verification failed")

        suffix = "commit" if behind == 1 else "commits"
        return GitSyncResult(
            "synced",
            f"Fast-forwarded {behind} {suffix} from {remote_ref}.",
            changed=True,
            commits=behind,
        )

    @staticmethod
    def _parse_ahead_behind(value: str | None) -> tuple[int, int] | None:
        if value is None:
            return None
        parts = value.replace("\t", " ").split()
        if len(parts) != 2:
            return None
        try:
            ahead, behind = (int(part) for part in parts)
        except ValueError:
            return None
        if ahead < 0 or behind < 0:
            return None
        return ahead, behind

    def _load_git_state(self) -> dict[str, str]:
        branch = self._run_git("rev-parse", "--abbrev-ref", "HEAD")
        head = self._run_git("rev-parse", "--short", "HEAD")
        last_commit = self._run_git("log", "-1", "--format=%cI")
        status = self._run_git("status", "--porcelain")
        available = branch is not None and head is not None

        if status is None:
            working_tree = "unknown"
        elif not status.strip():
            working_tree = "clean"
        else:
            count = len([line for line in status.splitlines() if line.strip()])
            suffix = "s" if count != 1 else ""
            working_tree = f"{count} local change{suffix}"

        return {
            "available": "yes" if available else "no",
            "branch": branch or "unknown branch",
            "head": head or "unknown commit",
            "last_commit": last_commit or "unknown",
            "working_tree": working_tree,
        }

    def _load_open_advisories(self) -> list[dict[str, str]]:
        path = self._repo_root / "coordination" / "ADVISORY_INDEX.md"
        section = self._read_section(path, "Open / Unacknowledged Advisories")
        advisories: list[dict[str, str]] = []
        for line in section.splitlines():
            item = self._bullet_text(line)
            if not item or item.casefold().rstrip(".") == "none":
                continue
            advisory_id, separator, detail = item.partition(" — ")
            advisories.append(
                {
                    "title": advisory_id.strip(),
                    "detail": detail.strip() if separator else item,
                }
            )
        return advisories

    def _load_open_loops(self) -> list[dict[str, str]]:
        path = self._repo_root / "memory" / "05_OPEN_LOOPS.md"
        section = self._read_section(path, "Priority Open Loops")
        loops: list[dict[str, str]] = []
        for line in section.splitlines():
            item = self._bullet_text(line)
            if not item:
                continue
            title, separator, detail = item.partition(":")
            loops.append(
                {
                    "title": self._clean_markdown(title.strip()),
                    "detail": self._clean_markdown(
                        detail.strip() if separator else item
                    ),
                }
            )
            if len(loops) >= self._open_loop_limit:
                break
        return loops

    def _load_notebooks(self) -> list[dict[str, str]]:
        notes_root = self._repo_root / "projects"
        candidates = list(notes_root.glob("*/notebook/NOTE-*.md"))
        candidates.sort(key=self._notebook_sort_key, reverse=True)

        notebooks: list[dict[str, str]] = []
        for path in candidates[: self._notebook_limit]:
            text = self._read_text(path)
            department = path.parents[1].name.replace("-", " ").upper()
            notebooks.append(
                {
                    "department": department,
                    "title": self._heading(text)
                    or self._title_from_filename(path),
                    "date": self._date_from_filename(path),
                    "summary": self._summary(text),
                    "status": self._note_status(text),
                }
            )
        return notebooks

    def _load_recent_activity(self) -> list[dict[str, str]]:
        output = self._run_git(
            "log",
            f"-{self._commit_limit}",
            "--format=%h%x1f%cI%x1f%s",
            "--",
            "memory",
            "projects",
            "coordination",
        )
        if not output:
            return []

        activity: list[dict[str, str]] = []
        for line in output.splitlines():
            parts = line.split("\x1f", 2)
            if len(parts) != 3:
                continue
            commit, timestamp, title = parts
            activity.append(
                {
                    "title": title,
                    "detail": (
                        f"{commit} · {self._display_timestamp(timestamp)}"
                    ),
                }
            )
        return activity

    def _run_git(self, *args: str) -> str | None:
        timeout = 15 if args and args[0] in {"fetch", "merge"} else 4
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), *args],
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
            return None

        if result.returncode != 0:
            return None
        return result.stdout.strip()

    @staticmethod
    def _read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return ""

    def _read_section(self, path: Path, heading: str) -> str:
        text = self._read_text(path)
        marker = f"## {heading}"
        start = text.find(marker)
        if start < 0:
            return ""
        content_start = start + len(marker)
        next_heading = text.find("\n## ", content_start)
        if next_heading < 0:
            return text[content_start:]
        return text[content_start:next_heading]

    @staticmethod
    def _bullet_text(line: str) -> str:
        stripped = line.strip()
        return stripped[2:].strip() if stripped.startswith("- ") else ""

    @staticmethod
    def _heading(text: str) -> str:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        return ""

    def _summary(self, text: str) -> str:
        for paragraph in re.split(r"\n\s*\n", text):
            cleaned = " ".join(
                line.strip() for line in paragraph.splitlines()
            ).strip()
            if not cleaned or cleaned.startswith("#") or cleaned.startswith("-"):
                continue
            if cleaned.lower().startswith(("date:", "status:", "department:")):
                continue
            return self._truncate(self._clean_markdown(cleaned), 220)
        return "Captured LifeOS notebook entry."

    @staticmethod
    def _note_status(text: str) -> str:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.lower().startswith("status:"):
                return stripped.split(":", 1)[1].strip() or "Captured"
        return "Captured"

    @staticmethod
    def _date_from_filename(path: Path) -> str:
        match = _NOTE_DATE.search(path.name)
        if not match:
            return "Unknown date"
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"

    @classmethod
    def _notebook_sort_key(cls, path: Path) -> tuple[str, str]:
        date = cls._date_from_filename(path)
        return ("" if date == "Unknown date" else date), path.name

    @staticmethod
    def _title_from_filename(path: Path) -> str:
        stem = _NOTE_DATE.sub("", path.stem).strip("-")
        stem = re.sub(r"^\d+-", "", stem)
        return stem.replace("-", " ").title() or "Untitled note"

    @staticmethod
    def _display_timestamp(value: str) -> str:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value
        local = parsed.astimezone()
        date_part = f"{local.strftime('%b')} {local.day}"
        time_part = local.strftime("%I:%M %p").lstrip("0")
        return f"{date_part}, {time_part}"

    @staticmethod
    def _clean_markdown(value: str) -> str:
        value = _MARKDOWN_LINK.sub(r"\1", value)
        return _MARKDOWN_DECORATION.sub("", value).strip()

    @staticmethod
    def _truncate(value: str, limit: int) -> str:
        if len(value) <= limit:
            return value
        return value[: limit - 1].rstrip() + "…"
