import json
import shutil
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from lifeos_v2.api import create_app
from lifeos_v2.contracts import CommandState, DeliveryCommand, Route
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
const commandFor = (commandId) => (scenario.commands || []).find((command) => command.command_id === commandId);
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
      actions.push({kind:'create', tab:{...tab}, commandStates:(scenario.commands || []).map((command) => ({command_id:command.command_id, state:command.state}))});
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
  if (path === '/routes') return response({items:scenario.routes || []});
  if (path.startsWith('/extension/commands/')) {
    const routeName = decodeURIComponent(path.split('/').at(-1));
    const command = (scenario.commands || []).find((item) => item.route_name === routeName && item.state === 'PENDING') || null;
    return response({paused:!!scenario.paused, command});
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


_POPUP_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');
const scenario = JSON.parse(fs.readFileSync(0, 'utf8'));
const actions = [];
const confirms = [];
const routes = [...(scenario.routes || [])];
const storage = {...(scenario.storage || {})};
const elements = Object.fromEntries(['route', 'register', 'poll', 'arm', 'stop', 'routes', 'courier', 'status'].map((id) => [`#${id}`, {textContent:'', value:id === 'route' ? (scenario.routeName || '') : '', onclick:null}]));
const response = (payload) => ({ok:true, status:200, json:async () => payload});
const fetch = async (url, options = {}) => {
  const path = new URL(url).pathname;
  const method = options.method || 'GET';
  const body = options.body ? JSON.parse(options.body) : null;
  actions.push({method, path, body});
  if (path === '/routes' && method === 'GET') return response({items:routes});
  if (path === '/routes' && method === 'POST') { const index = routes.findIndex((route) => route.route_name === body.route_name); if (index >= 0) routes[index] = {...routes[index], ...body, health:'AVAILABLE'}; else routes.push({...body, health:'AVAILABLE'}); return response(routes.find((route) => route.route_name === body.route_name)); }
  return response({});
};
const chrome = {
  storage: {local: {get:async (defaults) => ({...defaults, ...storage}), set:async (values) => Object.assign(storage, values)}},
  tabs: {query:async () => [scenario.activeTab], get:async (id) => ({id, url:scenario.courierUrl || 'https://chatgpt.com/c/courier'})},
  runtime: {sendMessage:async () => ({reason:'No dispatch-eligible command.'})},
};
const context = {chrome, fetch, URL, document:{querySelector:(selector) => elements[selector]}, confirm:(message) => { confirms.push(message); return scenario.confirm !== false; }, console};
vm.createContext(context);
const source = fs.readFileSync(process.argv[1], 'utf8');
vm.runInContext(`${source}\nglobalThis.__popupTest = {render};`, context, {filename:process.argv[1]});
(async () => {
  await context.__popupTest.render();
  for (const step of scenario.steps || []) {
    if (step.routeName !== undefined) elements['#route'].value = step.routeName;
    if (step.register) await elements['#register'].onclick();
  }
  process.stdout.write(JSON.stringify({actions, confirms, routes, storage, elements}));
})().catch((error) => { console.error(error.stack || error); process.exit(1); });
"""


_DISPATCH_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');
const scenario = JSON.parse(fs.readFileSync(0, 'utf8'));
let ticks = 0; let clickTick = null; let clicks = 0; let listener = null;
const messages = (scenario.baseline || []).map((text) => ({innerText:text}));
const composer = {value:'', innerText:'', disabled:false, focus:() => {}, getAttribute:() => null, getClientRects:() => [{}], closest:() => null, dispatchEvent:(event) => { if (event.type === 'input' && scenario.accepted === false) button.forceUnavailable = true; if (event.type === 'input' && scenario.rejectText === true) composer.value = ''; }};
const button = {forceUnavailable:false, get disabled() { return this.forceUnavailable || scenario.validSend === false || ticks < (scenario.sendAfterTicks || 0); }, getAttribute:(name) => name === 'data-testid' ? 'send-button' : null, getClientRects:() => button.disabled ? [] : [{}], closest:() => null, click:() => { clicks += 1; clickTick = ticks; }};
const unrelated = {get disabled() { return false; }, getAttribute:(name) => name === 'aria-label' ? 'Send attachment' : null, getClientRects:() => [{}], closest:() => null, click:() => { throw new Error('Unrelated control clicked'); }};
const document = {
  querySelector:(selector) => ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'].includes(selector) ? composer : null,
  querySelectorAll:(selector) => {
    if (selector === '[data-message-author-role="user"]') return messages;
    if (['button[data-testid="send-button"]', 'button[aria-label="Send prompt"]', 'button[aria-label="Send message"]'].includes(selector)) return scenario.validSend === false ? [] : [button];
    if (selector.includes('send')) return [unrelated];
    return [];
  },
  execCommand:(_command, _ui, text) => { composer.innerText = text; return true; },
};
const setTimeout = (resolve) => { ticks += 1; if (clickTick !== null && ticks - clickTick >= (scenario.deliveryAfterTicks ?? Number.MAX_SAFE_INTEGER) && !messages.some((node) => node.__new)) { messages.push({innerText:scenario.wake, __new:true}); } resolve(); return ticks; };
const event = (type, options = {}) => ({type, ...options});
const chrome = {
  runtime:{onMessage:{addListener:(handler) => { listener = handler; }}, getManifest:() => ({version:'test'}), onStartup:{addListener:() => {}}, onInstalled:{addListener:() => {}}},
  tabs:{onRemoved:{addListener:() => {}}, query:async () => [], get:async () => null, sendMessage:async () => { throw new Error('not used'); }, create:async () => null, update:async () => null},
  alarms:{create:() => {}, onAlarm:{addListener:() => {}}}, storage:{local:{get:async (defaults) => defaults, remove:async () => {}}}, scripting:{executeScript:async () => []},
};
const context = {chrome, document, location:{href:scenario.routeUrl}, URL, Event:function(type, options) { return event(type, options); }, InputEvent:function(type, options) { return event(type, options); }, setTimeout, clearTimeout:() => {}, console};
vm.createContext(context);
const source = fs.readFileSync(process.argv[1], 'utf8');
if (process.argv[2] === 'fallback') vm.runInContext(`${source}\nglobalThis.__dispatchTest = pageDispatch;`, context, {filename:process.argv[1]});
else vm.runInContext(source, context, {filename:process.argv[1]});
(async () => {
  const result = process.argv[2] === 'fallback' ? await context.__dispatchTest(scenario.wake, scenario.routeUrl) : await new Promise((resolve) => listener({type:'dispatch', wake:scenario.wake, routeUrl:scenario.routeUrl}, null, resolve));
  process.stdout.write(JSON.stringify({result, clicks, messages:messages.map((node) => node.innerText), ticks}));
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


def run_popup_scenario(scenario: dict) -> dict:
    node = _node_binary()
    if not node:
        pytest.skip("Node.js is required to execute the extension popup regression harness.")
    popup = Path(__file__).parents[1] / "extension" / "popup.js"
    result = subprocess.run([node, "-e", _POPUP_HARNESS, str(popup)], input=json.dumps(scenario), text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def run_dispatch_scenario(scenario: dict, mode: str = "content") -> dict:
    node = _node_binary()
    if not node:
        pytest.skip("Node.js is required to execute the courier dispatch regression harness.")
    source = Path(__file__).parents[1] / "extension" / ("service-worker.js" if mode == "fallback" else "content.js")
    result = subprocess.run([node, "-e", _DISPATCH_HARNESS, str(source), mode], input=json.dumps(scenario), text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def command(command_id: str, route_name: str) -> dict:
    return {"command_id":command_id, "route_name":route_name, "state":"PENDING", "attempts":0, "wake_payload":"Read the advisory."}


def route(route_name: str, url: str, health: str = "AVAILABLE") -> dict:
    return {"route_name":route_name, "target":route_name, "chatgpt_url":url, "health":health}


def ready_tab(tab_id: int, url: str) -> dict:
    return {"id":tab_id, "url":url, "active":False, "probe":{"url":url, "content_script":True, "composer_ready":True, "composer_empty":True, "send_control":True}}


def dispatch_case(**overrides) -> dict:
    scenario = {"routeUrl":"https://chatgpt.com/c/maintenance", "wake":"Read the advisory.", "deliveryAfterTicks":1}
    scenario.update(overrides)
    return scenario


def test_attempt_limit_and_uncertainty_survive_restart(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-300"}])
    service = CourierService(RuntimeStore(tmp_path / "state.json"))
    service.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/test", "now"))
    service.reconcile(advisories(tmp_path)[0])
    service.report_readiness("engineering", "https://chatgpt.com/c/test", True, True, True, True, False)
    assert service.begin_attempt("ADV-300-r1")["attempts"] == 1
    service.update_telemetry("ADV-300-r1", CommandState.FAILED, "send absent")
    assert service.discover_candidate("engineering")
    assert service.begin_attempt("ADV-300-r1")["attempts"] == 2
    service.update_telemetry("ADV-300-r1", CommandState.UNCERTAIN, "post-send navigation")
    restarted = CourierService(RuntimeStore(tmp_path / "state.json"))
    assert restarted.store.data["commands"]["ADV-300-r1"]["state"] == "UNCERTAIN"
    assert restarted.discover_candidate("engineering") is None


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


def test_maintenance_candidate_discovery_precedes_readiness_but_begin_does_not(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id":"ADV-304", "target":"maintenance"}])
    client = TestClient(create_app(tmp_path, tmp_path / "state.json"))
    client.post("/routes", json={"route_name":"maintenance", "target":"maintenance", "chatgpt_url":"https://chatgpt.com/c/maintenance"})
    client.get("/advisories")

    candidate = client.get("/extension/commands/maintenance").json()["command"]

    assert candidate["command_id"] == "ADV-304-r1" and candidate["state"] == CommandState.PENDING
    assert client.post("/commands/ADV-304-r1/begin").status_code == 409
    client.post("/extension/readiness", json={"route_name":"maintenance", "url":"https://chatgpt.com/c/maintenance", "content_script":True, "composer_ready":True, "composer_empty":True, "send_control":True, "test_armed":False})
    assert client.post("/commands/ADV-304-r1/begin").status_code == 200
    assert client.post("/commands/ADV-304-r1/begin").status_code == 409


def test_discovery_requires_available_registered_route_but_not_readiness(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id":"ADV-305", "target":"maintenance"}, {"id":"ADV-306", "target":"missing"}])
    client = TestClient(create_app(tmp_path, tmp_path / "state.json"))
    client.post("/routes", json={"route_name":"maintenance", "target":"maintenance", "chatgpt_url":"https://chatgpt.com/c/maintenance", "health":"UNAVAILABLE"})
    client.get("/advisories")
    assert client.get("/extension/commands/maintenance").json()["command"] is None
    assert client.get("/extension/commands/missing").json()["command"] is None
    client.post("/system/pause")
    assert client.get("/extension/commands/maintenance").json() == {"paused":True, "command":None}


def test_discovery_excludes_terminal_and_exhausted_commands_without_cross_route_readiness(tmp_path: Path) -> None:
    service = CourierService(RuntimeStore(tmp_path / "state.json"))
    service.register_route(Route("engineering", "engineering", "https://chatgpt.com/c/engineering", "now"))
    service.register_route(Route("maintenance", "maintenance", "https://chatgpt.com/c/maintenance", "now"))
    service.report_readiness("engineering", "https://chatgpt.com/c/wrong", True, True, True, True, False)
    for state in (CommandState.DELIVERED, CommandState.STALE, CommandState.UNCERTAIN, CommandState.DISPATCHING):
        command_id = f"ADV-{state}-r1"
        service.store.data["commands"][command_id] = DeliveryCommand(command_id, "ADV", 1, "maintenance", "maintenance", "wake", state, "now", "now").to_dict()
        assert service.discover_candidate("maintenance") is None
        service.store.data["commands"].clear()
    exhausted = DeliveryCommand("ADV-exhausted-r1", "ADV", 1, "maintenance", "maintenance", "wake", CommandState.PENDING, "now", "now", attempts=3).to_dict()
    service.store.data["commands"][exhausted["command_id"]] = exhausted
    assert service.discover_candidate("maintenance") is None
    service.store.data["commands"].clear()
    pending = DeliveryCommand("ADV-pending-r1", "ADV", 1, "maintenance", "maintenance", "wake", CommandState.PENDING, "now", "now").to_dict()
    service.store.data["commands"][pending["command_id"]] = pending
    assert service.discover_candidate("maintenance")["command_id"] == "ADV-pending-r1"


def test_dispatch_uses_controlled_insertion_and_ignores_broad_unrelated_controls() -> None:
    result = run_dispatch_scenario(dispatch_case())
    assert result["result"] == {"kind":"delivered", "note":"Expected user message proven."} and result["clicks"] == 1


def test_dispatch_fails_before_click_when_editor_does_not_accept_input() -> None:
    result = run_dispatch_scenario(dispatch_case(accepted=False))
    assert result["result"] == {"kind":"failed", "note":"Send control unavailable."} and result["clicks"] == 0


def test_dispatch_reports_rejected_insertion_before_click() -> None:
    result = run_dispatch_scenario(dispatch_case(rejectText=True))
    assert result["result"] == {"kind":"failed", "note":"Insertion rejected."} and result["clicks"] == 0


def test_dispatch_waits_for_a_delayed_send_control_and_delivery_proof() -> None:
    result = run_dispatch_scenario(dispatch_case(sendAfterTicks=3, deliveryAfterTicks=8))
    assert result["result"]["kind"] == "delivered" and result["clicks"] == 1 and result["ticks"] > 5


def test_dispatch_requires_a_new_matching_user_message_after_click() -> None:
    baseline_only = run_dispatch_scenario(dispatch_case(baseline=["Read the advisory."], deliveryAfterTicks=None))
    delivered = run_dispatch_scenario(dispatch_case(baseline=["Read the advisory."], deliveryAfterTicks=6))
    assert baseline_only["result"] == {"kind":"uncertain", "note":"Click attempted but user-message proof absent."} and baseline_only["clicks"] == 1
    assert delivered["result"] == {"kind":"delivered", "note":"Expected user message proven."} and delivered["clicks"] == 1


def test_dispatch_without_a_valid_send_control_is_preclick_failure() -> None:
    result = run_dispatch_scenario(dispatch_case(validSend=False))
    assert result["result"] == {"kind":"failed", "note":"Send control unavailable."} and result["clicks"] == 0


def test_injected_fallback_is_self_contained_and_matches_content_safety_gates() -> None:
    unavailable = dispatch_case(validSend=False)
    content = run_dispatch_scenario(unavailable)
    fallback = run_dispatch_scenario(unavailable, mode="fallback")
    delivered = run_dispatch_scenario(dispatch_case(deliveryAfterTicks=7), mode="fallback")
    assert fallback["result"] == content["result"] == {"kind":"failed", "note":"Send control unavailable."}
    assert delivered["result"]["kind"] == "delivered" and delivered["clicks"] == 1


def test_worker_reuses_an_exact_target_tab_without_creating_or_navigating() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", target)],
        "tabs":[ready_tab(17, target)], "commands":[command("ADV-exact", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in result["actions"] if action["kind"] in {"create", "update"}]
    assert [action for action in result["actions"] if action.get("path") == "/commands/ADV-exact/begin"]


def test_worker_creates_one_background_courier_then_claims_only_after_ready() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", target)],
        "tabs":[], "nextTabId":41, "commands":[command("ADV-create", "engineering")], "steps":[{"poll":True}],
    })
    created = [action for action in result["actions"] if action["kind"] == "create"]
    begins = [action for action in result["actions"] if action.get("path") == "/commands/ADV-create/begin"]
    ready_index = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/extension/readiness" and action["body"]["route_name"] == "engineering")
    begin_index = result["actions"].index(begins[0])
    assert len(created) == 1 and created[0]["tab"] == {"id":41, "url":target, "active":False}
    assert created[0]["commandStates"] == [{"command_id":"ADV-create", "state":"PENDING"}]
    assert result["storage"]["courierTabId"] == 41 and len(begins) == 1 and ready_index < begin_index


def test_worker_reuses_one_courier_tab_when_switching_routes() -> None:
    engineering = "https://chatgpt.com/c/engineering"
    maintenance = "https://chatgpt.com/c/maintenance"
    result = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", engineering), route("maintenance", maintenance)],
        "tabs":[], "nextTabId":50,
        "commands":[command("ADV-engineering", "engineering"), command("ADV-maintenance", "maintenance")],
        "steps":[{"poll":True}, {"poll":True}],
    })
    creates = [action for action in result["actions"] if action["kind"] == "create"]
    updates = [action for action in result["actions"] if action["kind"] == "update"]
    maintenance_ready = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/extension/readiness" and action["body"]["route_name"] == "maintenance")
    maintenance_begin = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/commands/ADV-maintenance/begin")
    assert len(creates) == 1 and len(updates) == 1
    assert updates[0] == {"kind":"update", "tabId":50, "properties":{"url":maintenance}}
    assert len(result["tabs"]) == 1 and maintenance_ready < maintenance_begin


def test_worker_discovers_unready_maintenance_then_navigates_and_claims_once() -> None:
    engineering = "https://chatgpt.com/c/engineering"
    maintenance = "https://chatgpt.com/c/maintenance"
    result = run_worker_scenario({
        "storage":{"courierTabId":53, "testArmed":False}, "routes":[route("engineering", engineering), route("maintenance", maintenance)],
        "tabs":[{"id":53, "url":engineering, "active":False}],
        "probes":{engineering:ready_tab(0, engineering)["probe"], maintenance:ready_tab(0, maintenance)["probe"]},
        "commands":[command("ADV-maintenance", "maintenance")], "steps":[{"poll":True}],
    })
    command_gets = [action["path"] for action in result["actions"] if action.get("path", "").startswith("/extension/commands/")]
    maintenance_ready = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/extension/readiness" and action["body"]["route_name"] == "maintenance")
    maintenance_begin = next(index for index, action in enumerate(result["actions"]) if action.get("path") == "/commands/ADV-maintenance/begin")
    assert command_gets == ["/extension/commands/engineering", "/extension/commands/maintenance"]
    assert {"kind":"update", "tabId":53, "properties":{"url":maintenance}} in result["actions"]
    assert maintenance_ready < maintenance_begin


def test_worker_claims_at_most_one_server_ordered_command_per_poll_cycle() -> None:
    engineering = "https://chatgpt.com/c/engineering"
    maintenance = "https://chatgpt.com/c/maintenance"
    result = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", engineering), route("maintenance", maintenance)],
        "tabs":[ready_tab(55, engineering)], "commands":[command("ADV-first", "engineering"), command("ADV-second", "maintenance")], "steps":[{"poll":True}],
    })
    begins = [action["path"] for action in result["actions"] if action.get("path", "").endswith("/begin")]
    assert begins == ["/commands/ADV-first/begin"] and result["commands"][1]["state"] == "PENDING"


def test_worker_replaces_a_stale_courier_tab_id_without_duplicates() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"courierTabId":999, "testArmed":False}, "routes":[route("engineering", target)],
        "tabs":[], "nextTabId":60, "commands":[command("ADV-stale", "engineering")], "steps":[{"poll":True}],
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
        "storage":{"courierTabId":70, "testArmed":False}, "routes":[route("engineering", target)],
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
        "storage":{"testArmed":False}, "routes":[route("engineering", target)],
        "tabs":[unrelated], "nextTabId":81, "commands":[command("ADV-unrelated", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in result["actions"] if action["kind"] == "update" and action["tabId"] == 80]
    assert result["tabs"] == [unrelated, {"id":81, "url":target, "active":False}]


def test_worker_keeps_test_routes_armed_but_allows_production() -> None:
    test_target = "https://chatgpt.com/c/test-route"
    blocked = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("slice_three_test-courier", test_target)],
        "tabs":[ready_tab(90, test_target)], "commands":[command("ADV-test", "slice_three_test-courier")], "steps":[{"poll":True}],
    })
    production_target = "https://chatgpt.com/c/production-route"
    allowed = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", production_target)],
        "tabs":[ready_tab(91, production_target)], "commands":[command("ADV-production", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in blocked["actions"] if action.get("path") == "/commands/ADV-test/begin"]
    assert len([action for action in allowed["actions"] if action.get("path") == "/commands/ADV-production/begin"]) == 1


def test_worker_does_not_reclaim_an_uncertain_delivery() -> None:
    target = "https://chatgpt.com/c/engineering"
    result = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", target)],
        "tabs":[ready_tab(99, target)], "commands":[command("ADV-uncertain", "engineering")], "delivery":{"kind":"uncertain", "note":"delivery not proven"}, "steps":[{"poll":True}, {"poll":True}],
    })
    begins = [action for action in result["actions"] if action.get("path") == "/commands/ADV-uncertain/begin"]
    assert len(begins) == 1 and result["commands"][0]["state"] == "UNCERTAIN"


def test_worker_emergency_stop_and_server_pause_block_all_claims() -> None:
    target = "https://chatgpt.com/c/engineering"
    emergency = run_worker_scenario({
        "storage":{"emergencyStop":True, "testArmed":False}, "routes":[route("engineering", target)],
        "tabs":[ready_tab(101, target)], "commands":[command("ADV-stop", "engineering")], "steps":[{"poll":True}],
    })
    paused = run_worker_scenario({
        "storage":{"testArmed":False}, "routes":[route("engineering", target)], "paused":True,
        "tabs":[ready_tab(102, target)], "commands":[command("ADV-pause", "engineering")], "steps":[{"poll":True}],
    })
    assert not [action for action in emergency["actions"] if action.get("path") == "/routes"]
    assert not [action for action in paused["actions"] if action.get("path") == "/commands/ADV-pause/begin"]


def test_popup_adds_a_route_without_replacing_existing_server_routes() -> None:
    engineering = "https://chatgpt.com/c/engineering"
    maintenance = "https://chatgpt.com/c/maintenance"
    result = run_popup_scenario({
        "routeName":"maintenance", "routes":[route("engineering", engineering)],
        "activeTab":{"id":1, "url":maintenance}, "steps":[{"register":True}],
    })
    posts = [action for action in result["actions"] if action["method"] == "POST" and action["path"] == "/routes"]
    assert [item["route_name"] for item in result["routes"]] == ["engineering", "maintenance"]
    assert posts == [{"method":"POST", "path":"/routes", "body":{"route_name":"maintenance", "target":"maintenance", "chatgpt_url":maintenance}}]
    assert result["confirms"] == [] and "routeName" not in result["storage"] and "routeUrl" not in result["storage"]


def test_popup_warns_only_for_a_same_name_route_overwrite() -> None:
    old = "https://chatgpt.com/c/engineering-old"
    replacement = "https://chatgpt.com/c/engineering-new"
    result = run_popup_scenario({
        "routeName":"engineering", "routes":[route("engineering", old)], "activeTab":{"id":2, "url":replacement}, "steps":[{"register":True}],
    })
    assert len(result["confirms"]) == 1 and "Overwrite engineering only?" in result["confirms"][0]
    assert result["routes"] == [{"route_name":"engineering", "target":"engineering", "chatgpt_url":replacement, "health":"AVAILABLE"}]


def test_exact_tab_readiness_and_test_arm_gate_dispatch(tmp_path: Path) -> None:
    write_source(tmp_path, [{"id": "ADV-302", "target": "slice_three_test"}])
    service = CourierService(RuntimeStore(tmp_path / "state.json"))
    service.register_route(Route("slice_three_test", "slice_three_test", "https://chatgpt.com/c/test", "now"))
    service.reconcile(advisories(tmp_path)[0])
    assert service.discover_candidate("slice_three_test")["command_id"] == "ADV-302-r1"
    not_ready = service.report_readiness("slice_three_test", "https://chatgpt.com/c/wrong", True, True, True, True, True)
    assert not_ready["state"] == "NOT_READY" and service.discover_candidate("slice_three_test")["command_id"] == "ADV-302-r1"
    assert service.begin_attempt("ADV-302-r1") is None
    ready_unarmed = service.report_readiness("slice_three_test", "https://chatgpt.com/c/test", True, True, True, True, False)
    assert ready_unarmed["state"] == "READY" and service.discover_candidate("slice_three_test")["command_id"] == "ADV-302-r1"
    assert service.begin_attempt("ADV-302-r1") is None
    service.report_readiness("slice_three_test", "https://chatgpt.com/c/test", True, True, True, True, True)
    assert service.discover_candidate("slice_three_test")["command_id"] == "ADV-302-r1"
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
    popup = (root / "popup.js").read_text(encoding="utf-8")
    assert "preflight" in worker and "/extension/readiness" in worker and "testArmed" in worker and "Registered tab is not open" in worker and "executeScript" in worker and "pageDispatch" in worker
    assert "VOICE_EMPTY" in content and "voiceSelectors" in content
    assert "requiresTestArm(selected.route.route_name) && !local.testArmed" in worker
    assert worker.count("/commands/${encodeURIComponent(selected.command.command_id)}/begin") == 1
    assert "courierTabId" in worker and "resolveCourierTab" in worker and "chrome.tabs.onRemoved" in worker
    assert "call('/routes')" in worker and "routeName:'', routeUrl:''" not in worker
    assert "other server routes were preserved" in popup and "Replace ${old.routeName}" not in popup
