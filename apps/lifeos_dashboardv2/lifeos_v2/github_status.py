"""Bounded, read-only GitHub repository metadata verification."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import UTC, datetime
from typing import Any, Callable


class GitHubStatusVerifier:
    def __init__(self, transport: Callable[[str, dict[str, str]], Any] | None = None):
        self.transport = transport or self._get
        self.last_success: str | None = None

    @staticmethod
    def _get(url: str, headers: dict[str, str]) -> Any:
        request = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))

    def verify(self) -> dict[str, str | None]:
        token, repository = os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPOSITORY")
        if not token:
            return {"state": "partial", "detail": "Configured local paths readable; GitHub token not set", "last_success": self.last_success}
        if not repository:
            return {"state": "partial", "detail": "Configured local paths readable; GITHUB_REPOSITORY is not set", "last_success": self.last_success}
        try:
            self.transport(f"https://api.github.com/repos/{repository}", {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"})
            self.last_success = datetime.now(UTC).isoformat()
            return {"state": "ok", "detail": "Repository metadata verified with configured GitHub token", "last_success": self.last_success}
        except urllib.error.HTTPError as error:
            if error.code in (401, 403):
                return {"state": "authentication_required", "detail": "GitHub authentication was rejected; check token access to the configured repository", "last_success": self.last_success}
            return {"state": "partial", "detail": "Configured local paths readable; GitHub metadata API is unavailable", "last_success": self.last_success}
        except Exception:
            return {"state": "partial", "detail": "Configured local paths readable; GitHub metadata API could not be reached", "last_success": self.last_success}
