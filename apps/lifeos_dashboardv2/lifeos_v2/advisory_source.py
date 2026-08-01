"""Read-only, commit-pinned advisory source synchronization."""
from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .contracts import Advisory
from .reader import AdvisoryReader, read_advisory_documents

REMOTE_GITHUB = "REMOTE_GITHUB"
LOCAL_DEVELOPMENT = "LOCAL_DEVELOPMENT"
CANONICAL_REPOSITORY = "recoveryrob83-lab/Penny-Long-Term-Memory"
CANONICAL_BRANCH = "main"
_OPEN_SECTION = re.compile(r"^##\s+Open Advisories\s*$", re.M | re.I)
_INDEX_LINE = re.compile(r"^-\s+ADV-[\w-]+.*?`coordination/boards/[^`]+\.md`", re.M)


class SourceSyncError(RuntimeError):
    """A source snapshot could not be completely verified."""


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def _bounded(message: str, limit: int = 240) -> str:
    return message.replace("\n", " ").replace("\r", " ")[:limit]


@dataclass(frozen=True)
class AdvisorySnapshot:
    advisories: list[Advisory]
    repository: str
    branch: str
    commit_sha: str
    verified_at: str


class GitHubContentsClient:
    """Small GitHub REST client that never invokes Git or writes local files."""
    def __init__(self, repository: str = CANONICAL_REPOSITORY, token: str | None = None, http_get: Callable[[str, dict[str, str]], tuple[int, dict[str, str], bytes]] | None = None) -> None:
        self.repository = repository
        self.token = token if token is not None else self._credential()
        self.http_get = http_get or self._http_get

    @staticmethod
    def _credential() -> str | None:
        """Use an environment token first, then the existing gh credential store."""
        token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if token:
            return token
        gh = shutil.which("gh")
        if not gh:
            return None
        try:
            result = subprocess.run([gh, "auth", "token"], capture_output=True, text=True, timeout=3, check=False)
        except (OSError, subprocess.SubprocessError):
            return None
        return result.stdout.strip() or None

    def _http_get(self, url: str, headers: dict[str, str]) -> tuple[int, dict[str, str], bytes]:
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=12) as response:  # noqa: S310 - fixed GitHub API origin
                return response.status, dict(response.headers.items()), response.read()
        except HTTPError as exc:
            return exc.code, dict(exc.headers.items()) if exc.headers else {}, exc.read()
        except URLError as exc:
            raise SourceSyncError("GitHub network request failed") from exc

    def _get_json(self, endpoint: str) -> Any:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "LifeOS-V2-advisory-sync"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        status, response_headers, body = self.http_get("https://api.github.com" + endpoint, headers)
        if status != 200:
            if status in {401, 403} and response_headers.get("X-RateLimit-Remaining") == "0":
                raise SourceSyncError("GitHub rate limit reached")
            if status in {401, 403}:
                raise SourceSyncError("GitHub authentication or authorization failed")
            if status == 404:
                raise SourceSyncError("GitHub source path or commit was not found")
            raise SourceSyncError(f"GitHub request failed (HTTP {status})")
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SourceSyncError("GitHub returned an invalid JSON response") from exc

    def resolve_commit(self, branch: str) -> str:
        response = self._get_json(f"/repos/{self.repository}/commits/{quote(branch, safe='')}")
        sha = response.get("sha") if isinstance(response, dict) else None
        if not isinstance(sha, str) or not sha:
            raise SourceSyncError("GitHub commit response did not include a SHA")
        return sha

    def fetch_text(self, path: str, commit_sha: str) -> str:
        response = self._get_json(f"/repos/{self.repository}/contents/{quote(path, safe='/')}?ref={quote(commit_sha, safe='')}")
        encoded = response.get("content") if isinstance(response, dict) else None
        if not isinstance(encoded, str):
            raise SourceSyncError("GitHub file response did not include content")
        try:
            return base64.b64decode(encoded, validate=False).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise SourceSyncError("GitHub file content could not be decoded") from exc


class AdvisorySource:
    """Expose only fully parsed source snapshots, with a bounded verified cache."""
    def __init__(
        self,
        mode: str,
        *,
        repository_root: Path | None = None,
        index_path: str = "coordination/ADVISORY_INDEX.md",
        repository: str = CANONICAL_REPOSITORY,
        branch: str = CANONICAL_BRANCH,
        github: GitHubContentsClient | None = None,
        refresh_ttl_seconds: float = 20,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if mode not in {REMOTE_GITHUB, LOCAL_DEVELOPMENT}:
            raise ValueError("source mode must be REMOTE_GITHUB or LOCAL_DEVELOPMENT")
        self.mode, self.index_path, self.repository, self.branch = mode, index_path, repository, branch
        self._local_reader = AdvisoryReader(repository_root, index_path) if mode == LOCAL_DEVELOPMENT and repository_root else None
        if mode == LOCAL_DEVELOPMENT and not self._local_reader:
            raise ValueError("LOCAL_DEVELOPMENT requires repository_root")
        self._github = github or GitHubContentsClient(repository)
        self._ttl, self._clock, self._last_attempt = refresh_ttl_seconds, clock, float("-inf")
        self._snapshot: AdvisorySnapshot | None = None
        self._status: dict[str, str | None] = {
            "source_mode": mode, "repository": repository, "branch": branch, "last_checked_at": None,
            "last_successful_sync_at": None, "current_verified_commit_sha": None, "sync_state": "CHECKING", "error": "",
        }

    @property
    def status(self) -> dict[str, str | None]:
        return dict(self._status)

    @property
    def snapshot(self) -> AdvisorySnapshot | None:
        return self._snapshot

    def refresh(self, force: bool = False) -> AdvisorySnapshot:
        if self._snapshot and not force and self._clock() - self._last_attempt < self._ttl:
            self._status.update({"last_checked_at": _timestamp(), "sync_state": "CURRENT", "error": ""})
            return self._snapshot
        self._last_attempt = self._clock()
        self._status.update({"last_checked_at": _timestamp(), "sync_state": "CHECKING", "error": ""})
        try:
            snapshot = self._read_local() if self.mode == LOCAL_DEVELOPMENT else self._read_remote()
        except (OSError, SourceSyncError, ValueError) as exc:
            self._status.update({"sync_state": "DEGRADED" if self._snapshot else "FAILED", "error": _bounded(str(exc))})
            raise SourceSyncError(self._status["error"] or "GitHub source verification failed") from exc
        self._snapshot = snapshot
        self._status.update({
            "last_successful_sync_at": snapshot.verified_at,
            "current_verified_commit_sha": snapshot.commit_sha,
            "sync_state": "CURRENT", "error": "",
        })
        return snapshot

    def _read_local(self) -> AdvisorySnapshot:
        assert self._local_reader is not None
        advisories, errors = self._local_reader.read()
        if errors:
            raise SourceSyncError("local development snapshot parse failed: " + "; ".join(sorted(errors.values())))
        verified_at = _timestamp()
        return AdvisorySnapshot(advisories, "local-development", "local", "local-development", verified_at)

    def _read_remote(self) -> AdvisorySnapshot:
        commit_sha = self._github.resolve_commit(self.branch)
        if self._snapshot and self._snapshot.commit_sha == commit_sha:
            return self._snapshot
        index = self._github.fetch_text(self.index_path, commit_sha)
        open_heading = _OPEN_SECTION.search(index)
        if not open_heading:
            raise SourceSyncError("GitHub Advisory Index is malformed: Open Advisories section is missing")
        following = index[open_heading.end():]
        next_section = re.search(r"^##\s+", following, re.M)
        open_section = following[:next_section.start()] if next_section else following
        open_lines = [line for line in open_section.splitlines() if line.lstrip().startswith("- ADV-")]
        if any(not _INDEX_LINE.match(line) for line in open_lines):
            raise SourceSyncError("GitHub Advisory Index contains a malformed open advisory reference")
        paths = sorted({re.search(r"`(coordination/boards/[^`]+\.md)`", line).group(1) for line in open_lines})
        documents = {path: self._github.fetch_text(path, commit_sha) for path in paths}
        verified_at = _timestamp()
        advisories, errors = read_advisory_documents(
            "# Advisory Index\n\n## Open Advisories\n" + open_section,
            documents.__getitem__,
            lambda path: f"https://github.com/{self.repository}/blob/{commit_sha}/{path}",
            source_repository=self.repository,
            source_branch=self.branch,
            source_commit_sha=commit_sha,
            source_verified_at=verified_at,
        )
        if errors:
            raise SourceSyncError("GitHub snapshot parse failed: " + "; ".join(f"{key}: {value}" for key, value in sorted(errors.items())))
        return AdvisorySnapshot(advisories, self.repository, self.branch, commit_sha, verified_at)
