from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from lifeos_v2.api import create_app
from lifeos_v2.contracts import CommandState, Route
from lifeos_v2.reader import AdvisoryReader
from lifeos_v2.runtime import CourierService, RuntimeStore, redact


def write_source(root: Path, records: list[dict[str, str]]) -> None:
    board = root / "coordination/boards/engineering.md"
    board.parent.mkdir(parents=True, exist_ok=True)
    index = "# Index\n\n## Open Advisories\n\n" + "\n".join(
        f"- {r['id']} — OPEN — Posted Board: `coordination/boards/engineering.md`" for r in records
    )
    root.joinpath("coordination/ADVISORY_INDEX.md").write_text(index, encoding="utf-8")
    sections = []
    for r in records:
        sections.append(f"""### {r['id']} — {r.get('heading_summary', 'Fixture work')}

- Advisory Revision: {r.get('revision', '1')}
- Source Department: {r.get('source', 'chief_of_staff')}
- Target Department: {r.get('target', 'engineering')}
- Task Summary: {r.get('task_summary', 'Fixture work')}
- Authorized Scope: {r.get('scope', 'Read the fixture only')}
- Lifecycle State: {r.get('state', 'OPEN')}
- Outcome: {r.get('outcome', '')}
- Blocker: {r.get('blocker', '')}
- Updated At: {r.get('updated_at', '2026-07-29T12:00:00+00:00')}
""")
    board.write_text("\n".join(sections), encoding="utf-8")


def service(root: Path) -> CourierService:
    return CourierService(RuntimeStore(root / "state.json"))


def advisories(root: Path):
    return AdvisoryReader(root, "coordination/ADVISORY_INDEX.md", "https://example.test").read()


def test_valid_parsing_and_malformed_isolation(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100"}, {"id": "ADV-101", "scope": ""}])
    found, errors = advisories(tmp_path)
    assert [a.command_id for a in found] == ["ADV-100-r1"]
    assert found[0].task_summary == "Fixture work"
    assert "ADV-101" in errors


def test_exact_envelope_fields_are_required(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100"}])
    board = tmp_path / "coordination/boards/engineering.md"
    board.write_text(board.read_text(encoding="utf-8").replace("- Authorized Scope:", "- Scope:"), encoding="utf-8")
    found, errors = advisories(tmp_path)
    assert found == []
    assert "authorized scope" in errors["ADV-100"]


def test_route_identifiers_and_timestamp_are_validated(tmp_path: Path) -> None:
    write_source(tmp_path, [
        {"id": "ADV-100", "target": "Engineering_HQ"},
        {"id": "ADV-101", "updated_at": "2026-07-29"},
    ])
    found, errors = advisories(tmp_path)
    assert found == []
    assert "lowercase snake_case" in errors["ADV-100"]
    assert "timezone offset" in errors["ADV-101"]


def test_present_empty_outcome_and_blocker_are_valid(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100", "outcome": "", "blocker": ""}])
    found, errors = advisories(tmp_path)
    assert errors == {}
    assert found[0].outcome == ""
    assert found[0].blocker == ""


def test_idempotency_revision_and_route_blocker(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100"}])
    found, _ = advisories(tmp_path)
    courier = service(tmp_path)
    courier.reconcile(found)
    assert courier.commands()[0]["state"] == CommandState.BLOCKED_ROUTE
    courier.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/example", "now"))
    courier.reconcile(found)
    courier.reconcile(found)
    assert len(courier.commands()) == 1
    assert courier.commands()[0]["state"] == CommandState.PENDING
    write_source(tmp_path, [{"id": "ADV-100", "revision": "2"}])
    courier.reconcile(advisories(tmp_path)[0])
    assert {c["command_id"] for c in courier.commands()} == {"ADV-100-r1", "ADV-100-r2"}
    assert next(c for c in courier.commands() if c["command_id"] == "ADV-100-r1")["state"] == CommandState.STALE


def test_telemetry_only_changes_transport_and_restart_is_safe(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100"}])
    found, _ = advisories(tmp_path)
    courier = service(tmp_path)
    courier.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/example", "now"))
    courier.reconcile(found)
    courier.update_telemetry("ADV-100-r1", CommandState.DELIVERED, "Authorization: hidden-token")
    restarted = service(tmp_path)
    restarted.reconcile(found)
    assert len(restarted.commands()) == 1
    assert restarted.commands()[0]["state"] == CommandState.DELIVERED
    assert "hidden-token" not in str(restarted.store.data["events"])


def test_pause_resume_reconciles_current_truth_without_stale_replay(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100"}])
    courier = service(tmp_path)
    courier.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/example", "now"))
    courier.pause()
    courier.reconcile(advisories(tmp_path)[0])
    assert courier.commands() == []
    write_source(tmp_path, [{"id": "ADV-100", "state": "COMPLETED", "outcome": "done"}])
    courier.resume()
    courier.reconcile(advisories(tmp_path)[0])
    assert courier.commands() == []
    write_source(tmp_path, [{"id": "ADV-101"}])
    courier.reconcile(advisories(tmp_path)[0])
    assert [c["command_id"] for c in courier.commands()] == ["ADV-101-r1"]


def test_state_and_outcome_changes_are_visible_without_cosmetic_command_change(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100", "state": "IN_PROGRESS"}])
    courier = service(tmp_path)
    courier.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/example", "now"))
    courier.reconcile(advisories(tmp_path)[0])
    write_source(tmp_path, [{"id": "ADV-100", "state": "BLOCKED", "blocker": "Needs Rob", "outcome": "held"}])
    current, _ = advisories(tmp_path)
    assert current[0].blocker == "Needs Rob"
    courier.reconcile(current)
    assert courier.commands()[0]["state"] == CommandState.STALE
    assert redact("GITHUB_TOKEN=super-secret") == "GITHUB_TOKEN=[REDACTED]"


def test_api_validation_and_transport_endpoints(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-100"}])
    client = TestClient(create_app(tmp_path, tmp_path / "state.json"))
    assert client.post("/routes", json={"route_name": "engineering"}).status_code == 422
    assert client.post("/routes", json={"route_name": "engineering", "target": "engineering", "chatgpt_url": "https://chatgpt.com/c/example"}).status_code == 201
    assert client.get("/advisories").json()["items"][0]["advisory_id"] == "ADV-100"
    assert client.get("/commands").json()["items"][0]["state"] == "PENDING"
    assert client.post("/commands/ADV-100-r1/ack", json={"note": "seen"}).json()["state"] == "DELIVERED"
    assert client.post("/system/pause").json() == {"paused": True}
    assert client.post("/system/resume").json() == {"paused": False}
