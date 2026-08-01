from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from lifeos_v2.advisory_source import AdvisorySource, REMOTE_GITHUB, SourceSyncError
from lifeos_v2.api import create_app
from lifeos_v2.runtime import RuntimeStore


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


def mixed_documents(*, legacy_valid: bool = False, include_legacy: bool = True) -> dict[str, str]:
    path = "coordination/boards/engineering.md"
    valid = documents("ADV-VALID")[path]
    legacy = documents("ADV-20260726-053")[path] if legacy_valid else "### ADV-20260726-053 — Legacy advisory\n\n- Lifecycle State: OPEN\n"
    index_lines = [f"- ADV-VALID — OPEN — Posted Board: `{path}`"]
    if include_legacy:
        index_lines.append(f"- ADV-20260726-053 — OPEN — Posted Board: `{path}`")
    return {
        "coordination/ADVISORY_INDEX.md": "# Index\n\n## Open Advisories\n\n" + "\n".join(index_lines) + "\n",
        path: valid + "\n" + legacy,
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


def test_legacy_advisory_is_quarantined_without_blocking_a_verified_snapshot(tmp_path: Path) -> None:
    fake = FakeGitHub({"sha-mixed": mixed_documents()}, "sha-mixed")
    source = remote_source(fake)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json", advisory_source=source))
    client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/remote"})

    advisories = client.get("/advisories").json()
    status = client.get("/status").json()

    assert [item["advisory_id"] for item in advisories["items"]] == ["ADV-VALID"]
    assert advisories["quarantined_advisory_count"] == 1
    quarantine = advisories["advisory_parse_errors"]["ADV-20260726-053"]
    assert quarantine["source_path"] == "coordination/boards/engineering.md"
    assert "V2 Courier Envelope" in quarantine["message"]
    assert status["source"]["sync_state"] == "CURRENT"
    assert status["source"]["current_verified_commit_sha"] == "sha-mixed"
    assert status["source"]["last_successful_sync_at"]
    assert [command["command_id"] for command in client.get("/commands").json()["items"]] == ["ADV-VALID-r1"]


def test_quarantine_does_not_stale_an_existing_command_for_that_advisory(tmp_path: Path) -> None:
    path = "coordination/boards/engineering.md"
    initial = documents("ADV-20260726-053")
    fake = FakeGitHub({"sha-valid": initial, "sha-legacy": mixed_documents()}, "sha-valid")
    source = remote_source(fake)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json", advisory_source=source))
    client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/remote"})
    client.get("/advisories")
    before = client.get("/commands/ADV-20260726-053-r1").json()
    fake.head = "sha-legacy"
    client.get("/advisories")
    after = client.get("/commands/ADV-20260726-053-r1").json()

    assert before["state"] == after["state"] == "PENDING"
    assert after["source_path"] == path
    assert "ADV-20260726-053" in client.get("/status").json()["advisory_parse_errors"]


def test_corrected_or_removed_advisory_leaves_quarantine_at_a_new_sha() -> None:
    fake = FakeGitHub({
        "sha-legacy": mixed_documents(),
        "sha-fixed": mixed_documents(legacy_valid=True),
        "sha-removed": mixed_documents(include_legacy=False),
    }, "sha-legacy")
    source = remote_source(fake)
    assert "ADV-20260726-053" in source.refresh().quarantined_advisories
    fake.head = "sha-fixed"
    fixed = source.refresh()
    assert not fixed.quarantined_advisories and {item.advisory_id for item in fixed.advisories} == {"ADV-VALID", "ADV-20260726-053"}
    fake.head = "sha-removed"
    removed = source.refresh()
    assert not removed.quarantined_advisories and [item.advisory_id for item in removed.advisories] == ["ADV-VALID"]


def test_unchanged_sha_reuses_quarantine_map_and_local_mode_matches_remote(tmp_path: Path) -> None:
    fake = FakeGitHub({"sha-legacy": mixed_documents()}, "sha-legacy")
    remote = remote_source(fake)
    first = remote.refresh(force=True)
    assert remote.refresh(force=True) is first and len(fake.fetch_log) == 2
    for path, text in mixed_documents().items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    local = AdvisorySource("LOCAL_DEVELOPMENT", repository_root=tmp_path)
    snapshot = local.refresh()
    assert [item.advisory_id for item in snapshot.advisories] == ["ADV-VALID"]
    assert "ADV-20260726-053" in snapshot.quarantined_advisories


@pytest.mark.parametrize("index", [
    "# Index\n\n## Open Advisories\n\n- ADV-DUP — OPEN — Posted Board: `coordination/boards/a.md`\n- ADV-DUP — OPEN — Posted Board: `coordination/boards/b.md`\n",
    "# Index\n\n## Open Advisories\n\n- ADV-BROKEN — OPEN\n",
])
def test_duplicate_or_malformed_open_references_fail_closed(index: str) -> None:
    fake = FakeGitHub({"sha-invalid": {"coordination/ADVISORY_INDEX.md": index}}, "sha-invalid")
    with pytest.raises(SourceSyncError):
        remote_source(fake).refresh()


def test_live_existing_command_ids_remain_untouched_by_a_mixed_snapshot(tmp_path: Path) -> None:
    persistence = tmp_path / "state.json"
    store = RuntimeStore(persistence)
    store.data["commands"] = {
        "ADV-20260728-054-r2": {"command_id": "ADV-20260728-054-r2", "advisory_id": "ADV-20260728-054", "revision": 2, "route_name": "engineering", "target": "engineering", "wake_payload": "prior", "state": "DELIVERED", "created_at": "before", "updated_at": "before"},
        "ADV-20260801-055-r1": {"command_id": "ADV-20260801-055-r1", "advisory_id": "ADV-20260801-055", "revision": 1, "route_name": "maintenance", "target": "maintenance", "wake_payload": "prior", "state": "UNCERTAIN", "created_at": "before", "updated_at": "before"},
        "ADV-20260801-055-r2": {"command_id": "ADV-20260801-055-r2", "advisory_id": "ADV-20260801-055", "revision": 2, "route_name": "maintenance", "target": "maintenance", "wake_payload": "prior", "state": "DELIVERED", "created_at": "before", "updated_at": "before"},
    }
    store.save()
    before = deepcopy(store.data["commands"])
    fake = FakeGitHub({"sha-mixed": mixed_documents()}, "sha-mixed")
    client = TestClient(create_app(tmp_path, persistence, advisory_source=remote_source(fake)))

    client.get("/advisories")

    after = {item["command_id"]: item for item in client.get("/commands").json()["items"] if item["command_id"] in before}
    assert after == before
