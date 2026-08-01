from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from lifeos_v2.advisory_source import AdvisorySource, REMOTE_GITHUB, SourceSyncError
from lifeos_v2.api import create_app


def documents(advisory_id: str = "ADV-REMOTE", revision: int = 1, state: str = "OPEN") -> dict[str, str]:
    path = "coordination/boards/engineering.md"
    return {
        "coordination/ADVISORY_INDEX.md": f"# Index\n\n## Open Advisories\n\n- {advisory_id} — OPEN — Posted Board: `{path}`\n",
        path: f"""### {advisory_id} — Remote work

#### V2 Courier Envelope

- Advisory Revision: {revision}
- Source Department: chief_of_staff
- Target Department: engineering
- Task Summary: Remote-only fixture
- Authorized Scope: Read only this snapshot
- Lifecycle State: {state}
- Outcome:
- Blocker:
- Updated At: 2026-08-01T12:00:00+00:00
""",
    }


class FakeGitHub:
    def __init__(self, commits: dict[str, dict[str, str]], head: str) -> None:
        self.commits, self.head, self.resolve_calls, self.fetch_log = commits, head, 0, []
        self.failure: Exception | None = None

    def resolve_commit(self, branch: str) -> str:
        self.resolve_calls += 1
        if self.failure:
            raise self.failure
        assert branch == "main"
        return self.head

    def fetch_text(self, path: str, commit_sha: str) -> str:
        self.fetch_log.append((path, commit_sha))
        if self.failure:
            raise self.failure
        try:
            return self.commits[commit_sha][path]
        except KeyError as exc:
            raise SourceSyncError("GitHub source path or commit was not found") from exc


def remote_source(fake: FakeGitHub, ttl: float = 0) -> AdvisorySource:
    return AdvisorySource(REMOTE_GITHUB, github=fake, refresh_ttl_seconds=ttl)


def test_remote_advisory_is_discovered_while_local_checkout_is_behind(tmp_path: Path) -> None:
    (tmp_path / "coordination").mkdir()
    local_index = tmp_path / "coordination" / "ADVISORY_INDEX.md"
    local_index.write_text("# local checkout deliberately behind\n", encoding="utf-8")
    fake = FakeGitHub({"sha-remote": documents()}, "sha-remote")
    source = remote_source(fake)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json", advisory_source=source))
    client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/remote"})

    response = client.get("/advisories").json()

    assert response["items"][0]["advisory_id"] == "ADV-REMOTE"
    assert local_index.read_text(encoding="utf-8") == "# local checkout deliberately behind\n"
    command = client.get("/commands").json()["items"][0]
    assert command["source_commit_sha"] == "sha-remote"
    assert command["source_repository"] == "recoveryrob83-lab/Penny-Long-Term-Memory"


def test_remote_snapshot_pins_index_and_boards_to_one_resolved_sha() -> None:
    fake = FakeGitHub({"sha-one": documents()}, "sha-one")
    snapshot = remote_source(fake).refresh()
    assert snapshot.commit_sha == "sha-one"
    assert fake.fetch_log == [("coordination/ADVISORY_INDEX.md", "sha-one"), ("coordination/boards/engineering.md", "sha-one")]
    assert snapshot.advisories[0].source_url.endswith("/sha-one/coordination/boards/engineering.md")


def test_head_change_during_fetch_does_not_mix_snapshots() -> None:
    fake = FakeGitHub({"sha-one": documents("ADV-ONE"), "sha-two": documents("ADV-TWO")}, "sha-one")
    original_fetch = fake.fetch_text

    def switch_head(path: str, sha: str) -> str:
        result = original_fetch(path, sha)
        fake.head = "sha-two"
        return result

    fake.fetch_text = switch_head  # type: ignore[method-assign]
    snapshot = remote_source(fake).refresh()
    assert snapshot.commit_sha == "sha-one" and [a.advisory_id for a in snapshot.advisories] == ["ADV-ONE"]
    assert {sha for _, sha in fake.fetch_log} == {"sha-one"}


def test_unchanged_head_reuses_the_verified_snapshot_without_refetching_files() -> None:
    fake = FakeGitHub({"sha-one": documents()}, "sha-one")
    source = remote_source(fake)
    first = source.refresh(force=True)
    second = source.refresh(force=True)
    assert first is second and fake.resolve_calls == 2
    assert len(fake.fetch_log) == 2


def test_revision_and_closed_remote_truth_reconcile_atomically(tmp_path: Path) -> None:
    fake = FakeGitHub({"sha-one": documents(revision=1), "sha-two": documents(revision=2), "sha-three": documents(revision=2, state="CLOSED")}, "sha-one")
    source = remote_source(fake)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json", advisory_source=source))
    client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/remote"})
    client.get("/advisories")
    assert [c["command_id"] for c in client.get("/commands").json()["items"]] == ["ADV-REMOTE-r1"]
    fake.head = "sha-two"
    client.get("/advisories")
    commands = {c["command_id"]: c for c in client.get("/commands").json()["items"]}
    assert commands["ADV-REMOTE-r1"]["state"] == "STALE" and commands["ADV-REMOTE-r2"]["state"] == "PENDING"
    fake.head = "sha-three"
    client.get("/advisories")
    assert client.get("/commands").json()["items"][-1]["state"] == "STALE"


@pytest.mark.parametrize("failure", [SourceSyncError("GitHub network request failed"), SourceSyncError("GitHub authentication or authorization failed"), SourceSyncError("GitHub rate limit reached")])
def test_remote_failures_never_change_or_dispatch_existing_commands(tmp_path: Path, failure: Exception) -> None:
    fake = FakeGitHub({"sha-one": documents()}, "sha-one")
    source = remote_source(fake)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json", advisory_source=source))
    client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/remote"})
    client.get("/advisories")
    fake.failure = failure
    result = client.get("/advisories").json()
    assert result["parse_errors"]["source_sync"] == str(failure)
    assert client.get("/commands").json()["items"][0]["state"] == "PENDING"
    assert client.get("/extension/commands/engineering").json()["command"] is None
    assert client.post("/commands/ADV-REMOTE-r1/begin").status_code == 409


def test_malformed_or_missing_remote_board_fails_closed_without_staling_commands(tmp_path: Path) -> None:
    fake = FakeGitHub({"sha-one": documents(), "sha-bad": {"coordination/ADVISORY_INDEX.md": documents()["coordination/ADVISORY_INDEX.md"]}}, "sha-one")
    source = remote_source(fake)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json", advisory_source=source))
    client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/remote"})
    client.get("/advisories")
    fake.head = "sha-bad"
    assert "source_sync" in client.get("/advisories").json()["parse_errors"]
    assert client.get("/commands").json()["items"][0]["state"] == "PENDING"


def test_production_mode_defaults_to_remote_and_local_mode_is_explicit(tmp_path: Path) -> None:
    production = TestClient(create_app(tmp_path, tmp_path / "production.json"))
    assert production.get("/health").json()["source"]["source_mode"] == "REMOTE_GITHUB"
    local = AdvisorySource("LOCAL_DEVELOPMENT", repository_root=tmp_path)
    with pytest.raises(SourceSyncError):
        local.refresh()


def test_status_exposes_verified_remote_commit_and_no_git_worktree_operation() -> None:
    fake = FakeGitHub({"sha-one": documents()}, "sha-one")
    source = remote_source(fake)
    source.refresh()
    status = source.status
    assert status["sync_state"] == "CURRENT" and status["current_verified_commit_sha"] == "sha-one"
    implementation = Path(__file__).parents[1] / "lifeos_v2" / "advisory_source.py"
    text = implementation.read_text(encoding="utf-8")
    assert all(operation not in text for operation in ("git pull", "git fetch", "git checkout", "git reset", "git merge"))
