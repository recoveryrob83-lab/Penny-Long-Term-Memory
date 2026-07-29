from pathlib import Path

from fastapi.testclient import TestClient

from lifeos_v2.api import create_app
from lifeos_v2.contracts import CommandState, Route
from lifeos_v2.runtime import CourierService, RuntimeStore
from test_slice_one import advisories, write_source


def test_attempt_limit_and_uncertainty_survive_restart(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-300"}])
    service = CourierService(RuntimeStore(tmp_path / "state.json"))
    service.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/test", "now"))
    service.reconcile(advisories(tmp_path)[0])
    service.report_readiness("engineering", "https://chatgpt.com/c/test", True, True, True, True, False)
    assert service.begin_attempt("ADV-300-r1")["attempts"] == 1
    service.update_telemetry("ADV-300-r1", CommandState.FAILED, "send absent")
    assert service.eligible_command("engineering")
    assert service.begin_attempt("ADV-300-r1")["attempts"] == 2
    service.update_telemetry("ADV-300-r1", CommandState.UNCERTAIN, "post-send navigation")
    restarted = CourierService(RuntimeStore(tmp_path / "state.json"))
    assert restarted.store.data["commands"]["ADV-300-r1"]["state"] == "UNCERTAIN"
    assert restarted.eligible_command("engineering") is None


def test_extension_api_pause_and_heartbeat(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-301"}])
    client = TestClient(create_app(tmp_path, tmp_path / "state.json"))
    client.post("/routes", json={"route_name":"engineering", "target":"engineering", "chatgpt_url":"https://chatgpt.com/c/test"})
    client.get("/advisories")
    client.post("/extension/readiness", json={"route_name":"engineering", "url":"https://chatgpt.com/c/test", "content_script":True, "composer_ready":True, "composer_empty":True, "send_control":True})
    assert client.get("/extension/commands/engineering").json()["command"]["command_id"] == "ADV-301-r1"
    assert client.post("/extension/heartbeat", json={"version":"0.1.0"}).json()["connected"] is True
    client.post("/system/pause")
    assert client.get("/extension/commands/engineering").json()["command"] is None


def test_exact_tab_readiness_and_test_arm_gate_dispatch(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-302", "target": "slice_three_test"}])
    service = CourierService(RuntimeStore(tmp_path / "state.json"))
    service.register_route(Route("slice_three_test", "slice_three_test", "https://chatgpt.com/c/test", "now"))
    service.reconcile(advisories(tmp_path)[0])
    assert service.eligible_command("slice_three_test") is None
    not_ready = service.report_readiness("slice_three_test", "https://chatgpt.com/c/wrong", True, True, True, True, True)
    assert not_ready["state"] == "NOT_READY" and service.eligible_command("slice_three_test") is None
    ready_unarmed = service.report_readiness("slice_three_test", "https://chatgpt.com/c/test", True, True, True, True, False)
    assert ready_unarmed["state"] == "READY" and service.eligible_command("slice_three_test") is None
    service.report_readiness("slice_three_test", "https://chatgpt.com/c/test", True, True, True, True, True)
    assert service.eligible_command("slice_three_test")["command_id"] == "ADV-302-r1"
    assert service.begin_attempt("ADV-302-r1")["attempts"] == 1


def test_extension_keeps_scope_narrow_and_protects_composer() -> None:
    root = Path(__file__).parents[1] / "extension"
    manifest = (root / "manifest.json").read_text(encoding="utf-8")
    content = (root / "content.js").read_text(encoding="utf-8")
    worker = (root / "service-worker.js").read_text(encoding="utf-8")
    assert "https://chatgpt.com/*" in manifest and "scripting" in manifest and "<all_urls>" not in manifest
    assert "Composer contains unrelated text; preserved." in content
    assert "data-message-author-role=\"user\"" in content
    assert "assistant" not in content.lower()
    assert "/uncertain" in worker and "emergencyStop" in worker and "/begin" in worker
    assert "preflight" in worker and "/extension/readiness" in worker and "testArmed" in worker and "Registered tab is not open" in worker and "executeScript" in worker and "pageDispatch" in worker
    assert "VOICE_EMPTY" in content and "voiceSelectors" in content
