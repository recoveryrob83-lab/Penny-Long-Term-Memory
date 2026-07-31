import json
import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from lifeos_v2.api import create_app
from lifeos_v2.contracts import CommandState, Route
from lifeos_v2.runtime import CourierService, RuntimeStore
from test_slice_one import advisories, write_source


_WORKER_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');
const scenario = JSON.parse(fs.readFileSync(0, 'utf8'));
const actions = [];
const storage = {...(scenario.storage || {})};
const tabs = new Map((scenario.tabs || []).map((tab) => [tab.id, {...tab}]));
const removedListeners = [];
let nextTabId = scenario.nextTabId || 100;
const ready = (url) => ({url, content_script:true, composer_ready:true, composer_empty:true, send_control:true});
const probeFor = (tab) => ({...(tab.probe || scenario.probes?.[tab.url] || ready(tab.url))});
const response = (payload) => ({ok:true, status:200, json:async () => payload});
const commandFor = (commandId) => scenario.commands.find((command) => command.command_id === commandId);
const chrome = {
  storage: {local: {
    get: async (defaults) => ({...defaults, ...storage}),
    set: async (values) => { Object.assign(storage, values); actions.push({kind:'storage-set', values}); },
    remove: async (key) => { delete storage[key]; actions.push({kind:'storage-remove', key}); },
  }},
  tabs: {
    query: async ({url}) => {
      const prefix = url.replace('*', '');
      return [...tabs.values()].filter((tab) => String(tab.url || '').startsWith(prefix)).map((tab) => ({...tab}));
    },
    get: async (tabId) => {
      const tab = tabs.get(tabId);
      if (!tab) throw new Error('No tab with id: ' + tabId);
      return {...tab};
    },
    create: async (properties) => {
      const tab = {id:nextTabId++, ...properties};
      tabs.set(tab.id, tab);
      actions.push({kind:'create', tab:{...tab}});
      return {...tab};
    },
    update: async (tabId, properties) => {
      const tab = tabs.get(tabId);
      if (!tab) throw new Error('No tab with id: ' + tabId);
      Object.assign(tab, properties);
      actions.push({kind:'update', tabId, properties});
      return {...tab};
    },
    sendMessage: async (tabId, message) => {
      const tab = tabs.get(tabId);
      if (!tab) throw new Error('No tab with id: ' + tabId);
      if (message.type === 'preflight') return probeFor(tab);
      if (message.type === 'dispatch') return scenario.delivery || {kind:'delivered'};
      throw new Error('Unsupported message');
    },
    onRemoved: {addListener: (listener) => removedListeners.push(listener)},
  },
  scripting: {executeScript: async () => { throw new Error('Unexpected direct probe'); }},
  alarms: {create: () => {}, onAlarm: {addListener: () => {}}},
  runtime: {getManifest: () => ({version:'test'}), onStartup: {addListener: () => {}}, onInstalled: {addListener: () => {}}, onMessage: {addListener: () => {}}},
};
const fetch = async (url, options = {}) => {
  const path = new URL(url).pathname;
  const method = options.method || 'GET';
  actions.push({kind:'fetch', method, path, body:options.body ? JSON.parse(options.body) : null});
  if (path.startsWith('/extension/commands/')) {
    const routeName = decodeURIComponent(path.split('/').at(-1));
    const command = scenario.commands.find((item) => item.route_name === routeName && item.state === 'PENDING') || null;
    return response({paused:false, command});
  }
  if (path.startsWith('/commands/') && path.endsWith('/begin')) {
    const command = commandFor(decodeURIComponent(path.split('/')[2]));
    if (!command || command.state !== 'PENDING') return {ok:false, status:409, json:async () => ({})};
    command.state = 'DISPATCHING'; command.attempts = (command.attempts || 0) + 1;
    return response(command);
  }
  if (path.startsWith('/commands/')) {
    const command = commandFor(decodeURIComponent(path.split('/')[2]));
    if (path.endsWith('/ack')) command.state = 'DELIVERED';
    if (path.endsWith('/uncertain')) command.state = 'UNCERTAIN';
    if (path.endsWith('/fail')) command.state = 'PENDING';
    return response(command || {});
  }
  return response({});
};
const context = {chrome, fetch, URL, setTimeout:(resolve) => { resolve(); return 1; }, clearTimeout:() => {}, console};
vm.createContext(context);
const source = fs.readFileSync(process.argv[1], 'utf8');
vm.runInContext(`${source}\nglobalThis.__lifeosTest = {poll};`, context, {filename:process.argv[1]});
(async () => {
  for (const step of scenario.steps) {
    if (step.storage) Object.assign(storage, step.storage);
    if (step.removeTabId !== undefined) {
      tabs.delete(step.removeTabId);
      removedListeners.forEach((listener) => listener(step.removeTabId));
      await Promise.resolve(); await Promise.resolve();
    }
    if (step.poll) await context.__lifeosTest.poll();
  }
  process.stdout.write(JSON.stringify({actions, storage, tabs:[...tabs.values()], commands:scenario.commands}));
})().catch((error) => { console.error(error.stack || error); process.exit(1); });
"""


def _node_binary() -> str | None:
    bundled = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe"
    found = shutil.which("node")
    if found:
        return found
    return str(bundled) if bundled.exists() else None


def run_worker_scenario(scenario: dict) -> dict:
    node = _node_binary()
    if not node:
        pytest.skip("Node.js is required to execute the extension service-worker regression harness.")
    worker = Path(__file__).parents[1] / "extension" / "service-worker.js"
    result = subprocess.run([node, "-e", _WORKER_HARNESS, str(worker)], input=json.dumps(scenario), text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def command(command_id: str, route_name: str) -> dict:
    return {"command_id":command_id, "route_name":route_name, "state":"PENDING", "attempts":0, "wake_payload":"Read the advisory."}


def ready_tab(tab_id: int, url: str) -> dict:
    return {"id":tab_id, "url":url, "active":False, "probe":{"url":url, "content_script":True, "composer_ready":True, "composer_empty":True, "send_control":True}}


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


def test_ready_production_route_claims_an_eligible_command_once_without_test_arm(tmp_path: Path, monkeypatch) -> None:
    """The production extension path must claim, not stop at an unarmed test gate."""
    write_source(tmp_path, [{"id": "ADV-303"}])
    calls: list[str] = []
    original_begin_attempt = CourierService.begin_attempt

    def record_begin_attempt(service: CourierService, command_id: str):
        calls.append(command_id)
        return original_begin_attempt(service, command_id)

    monkeypatch.setattr(CourierService, "begin_attempt", record_begin_attempt)
    client = TestClient(create_app(tmp_path, tmp_path / "state.json"))
    client.post("/routes", json={"route_name":"engineering", "target":"engineering", "chatgpt_url":"https://chatgpt.com/c/test"})
    client.get("/advisories")
    ready = client.post("/extension/readiness", json={"route_name":"engineering", "url":"https://chatgpt.com/c/test", "content_script":True, "composer_ready":True, "composer_empty":True, "send_control":True, "test_armed":False})
    assert ready.json()["state"] == "READY"
    command = client.get("/extension/commands/engineering").json()["command"]
    assert command["command_id"] == "ADV-303-r1" and command["state"] == CommandState.PENDING

    claimed = client.post(f"/commands/{command['command_id']}/begin")

    assert claimed.status_code == 200
    assert calls == ["ADV-303-r1"]
    assert claimed.json()["state"] == CommandState.DISPATCHING
    assert claimed.json()["attempts"] == 1
    assert client.post(f"/commands/{command['command_id']}/begin").status_code == 409
    stored = client.get(f"/commands/{command['command_id']}").json()
    assert stored["state"] == CommandState.DISPATCHING and stored["attempts"] == 1


def test_worker_reuses_an_exact_target_tab_without_creating_or_navigating() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":target, "testArmed":False},
        "tabs":[ready_tab(17, target)], "commands":[command("ADV-exact", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in result["actions"] if action["kind"] in {"create", "update"}]
    assert [action for action in result["actions"] if action.get("path") == "/commands/ADV-exact/begin"]


def test_worker_creates_one_background_courier_then_claims_only_after_ready() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":target, "testArmed":False},
        "tabs":[], "nextTabId":41, "commands":[command("ADV-create", "engineering")], "steps":[{"poll":True}],
    })
    created = [action for action in result["actions"] if action["kind"] == "create"]
    begins = [action for action in result["actions"] if action.get("path") == "/commands/ADV-create/begin"]
    ready_index = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/extension/readiness" and action["body"]["route_name"] == "engineering")
    begin_index = result["actions"].index(begins[0])
    assert len(created) == 1 and created[0]["tab"] == {"id":41, "url":target, "active":False}
    assert result["storage"]["courierTabId"] == 41 and len(begins) == 1 and ready_index < begin_index


def test_worker_reuses_one_courier_tab_when_switching_routes() -> None:
    engineering = "https://chatgpt.com/c/engineering"
    maintenance = "https://chatgpt.com/c/maintenance"
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":engineering, "testArmed":False},
        "tabs":[], "nextTabId":50,
        "commands":[command("ADV-engineering", "engineering"), command("ADV-maintenance", "maintenance")],
        "steps":[{"poll":True}, {"storage":{"routeName":"maintenance", "routeUrl":maintenance}, "poll":True}],
    })
    creates = [action for action in result["actions"] if action["kind"] == "create"]
    updates = [action for action in result["actions"] if action["kind"] == "update"]
    maintenance_ready = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/extension/readiness" and action["body"]["route_name"] == "maintenance")
    maintenance_begin = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/commands/ADV-maintenance/begin")
    assert len(creates) == 1 and len(updates) == 1
    assert updates[0] == {"kind":"update", "tabId":50, "properties":{"url":maintenance}}
    assert len(result["tabs"]) == 1 and maintenance_ready < maintenance_begin


def test_worker_replaces_a_stale_courier_tab_id_without_duplicates() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":target, "courierTabId":999, "testArmed":False},
        "tabs":[], "nextTabId":60, "commands":[], "steps":[{"poll":True}],
    })
    assert [action for action in result["actions"] if action["kind"] == "storage-remove"] == [{"kind":"storage-remove", "key":"courierTabId"}]
    assert [action["tab"]["id"] for action in result["actions"] if action["kind"] == "create"] == [60]
    assert result["storage"]["courierTabId"] == 60 and len(result["tabs"]) == 1


def test_worker_refuses_to_navigate_a_nonempty_courier_composer() -> None:
    old_route = "https://chatgpt.com/c/old"
    target = "https://chatgpt.com/c/engineering"
    tab = ready_tab(70, old_route)
    tab["probe"]["composer_empty"] = False
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":target, "courierTabId":70, "testArmed":False},
        "tabs":[tab], "commands":[command("ADV-preserve", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in result["actions"] if action["kind"] == "update"]
    assert not [action for action in result["actions"] if action.get("path") == "/commands/ADV-preserve/begin"]
    assert result["commands"][0]["state"] == "PENDING" and result["tabs"][0]["url"] == old_route


def test_worker_never_uses_or_focuses_an_unrelated_tab() -> None:
    target = "https://chatgpt.com/c/engineering"
    unrelated = ready_tab(80, "https://chatgpt.com/c/user-owned")
    unrelated["active"] = True
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":target, "testArmed":False},
        "tabs":[unrelated], "nextTabId":81, "commands":[], "steps":[{"poll":True}],
    })
    assert not [action for action in result["actions"] if action["kind"] == "update" and action["tabId"] == 80]
    assert result["tabs"] == [unrelated, {"id":81, "url":target, "active":False}]


def test_worker_keeps_test_routes_armed_but_allows_production() -> None:
    test_target = "https://chatgpt.com/c/test-route"
    blocked = run_worker_scenario({
        "storage":{"routeName":"slice_three_test-courier", "routeUrl":test_target, "testArmed":False},
        "tabs":[ready_tab(90, test_target)], "commands":[command("ADV-test", "slice_three_test-courier")], "steps":[{"poll":True}],
    })
    production_target = "https://chatgpt.com/c/production-route"
    allowed = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":production_target, "testArmed":False},
        "tabs":[ready_tab(91, production_target)], "commands":[command("ADV-production", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in blocked["actions"] if action.get("path") == "/commands/ADV-test/begin"]
    assert len([action for action in allowed["actions"] if action.get("path") == "/commands/ADV-production/begin"]) == 1


def test_worker_does_not_reclaim_an_uncertain_delivery() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"routeName":"engineering", "routeUrl":target, "testArmed":False},
        "tabs":[ready_tab(99, target)], "commands":[command("ADV-uncertain", "engineering")], "delivery":{"kind":"uncertain", "note":"delivery not proven"}, "steps":[{"poll":True}, {"poll":True}],
    })
    begins = [action for action in result["actions"] if action.get("path") == "/commands/ADV-uncertain/begin"]
    assert len(begins) == 1 and result["commands"][0]["state"] == "UNCERTAIN"


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
    assert "requiresTestArm(local.routeName) && !local.testArmed" in worker
    assert worker.count("/commands/${encodeURIComponent(command.command_id)}/begin") == 1
    assert "courierTabId" in worker and "resolveCourierTab" in worker and "chrome.tabs.onRemoved" in worker
