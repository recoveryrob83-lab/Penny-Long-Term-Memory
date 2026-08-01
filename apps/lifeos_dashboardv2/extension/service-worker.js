const server = 'http://127.0.0.1:8765';
const chatgptOrigin = 'https://chatgpt.com';
const call = async (path, options = {}) => { const response = await fetch(server + path, {headers:{'content-type':'application/json'}, ...options}); if (!response.ok) throw new Error(`${response.status}`); return response.json(); };
const state = () => chrome.storage.local.get({emergencyStop:false, testArmed:false, courierTabId:null});
const normal = (text) => String(text || '').replace(/\r\n/g, '\n').trim();
const requiresTestArm = (routeName) => routeName.startsWith('slice_three_test');
const delay = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

function isChatgptUrl(url) { try { return new URL(url).origin === chatgptOrigin; } catch (_) { return false; } }
function readyProbe(result, routeUrl) { return result?.url === routeUrl && result.content_script && result.composer_ready && result.composer_empty && result.send_control; }
function availableRoute(route) { return route?.route_name && isChatgptUrl(route.chatgpt_url) && String(route.health || 'AVAILABLE').toUpperCase() === 'AVAILABLE'; }
async function heartbeat() { try { await call('/extension/heartbeat', {method:'POST', body:JSON.stringify({version:chrome.runtime.getManifest().version})}); } catch (_) {} }
async function reportReadiness(route, local, details = {}) { try { return await call('/extension/readiness', {method:'POST', body:JSON.stringify({route_name:route.route_name, url:details.url || '', content_script:!!details.content_script, composer_ready:!!details.composer_ready, composer_empty:!!details.composer_empty, send_control:!!details.send_control, test_armed:!!local.testArmed})}); } catch (_) { return null; } }

function pageProbe() {
  const composer = ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'].map((selector)=>document.querySelector(selector)).find(Boolean);
  const text = String(composer?.value ?? composer?.innerText ?? '').replace(/\r\n/g, '\n').trim();
  const send = ['button[data-testid="send-button"]', 'button[data-testid*="send" i]', 'button[aria-label="Send prompt"]', 'button[aria-label="Send message"]', 'button[aria-label*="Send" i]'].map((selector)=>document.querySelector(selector)).find(Boolean);
  const voice = ['button[data-testid*="voice"]', 'button[aria-label*="voice" i]'].map((selector)=>document.querySelector(selector)).find(Boolean);
  return {url:location.href, content_script:true, composer_ready:!!composer, composer_empty:!text, send_control:!!send || (!text && !!voice)};
}

async function direct(tabId, func, args = []) { const result = await chrome.scripting.executeScript({target:{tabId}, func, args}); return result[0]?.result; }
async function tabById(tabId) { if (!Number.isInteger(tabId)) return null; try { return await chrome.tabs.get(tabId); } catch (_) { return null; } }
async function probeTab(tabId) { try { return await chrome.tabs.sendMessage(tabId, {type:'preflight'}); } catch (_) { try { return await direct(tabId, pageProbe); } catch (_) { return null; } } }
async function clearCourierTab(tabId) { const current = await chrome.storage.local.get({courierTabId:null}); if (current.courierTabId === tabId) await chrome.storage.local.remove('courierTabId'); }
async function waitForExactUrl(tabId, routeUrl) { for (let attempt = 0; attempt < 20; attempt += 1) { const tab = await tabById(tabId); if (!tab) return null; if (tab.url === routeUrl) return tab; await delay(150); } return null; }
async function knownCourierTab(local) { if (!Number.isInteger(local.courierTabId)) return null; const tab = await tabById(local.courierTabId); if (!tab || !isChatgptUrl(tab.url)) { await clearCourierTab(local.courierTabId); return null; } return tab; }
async function exactTargetTab(routeUrl) { const tabs = await chrome.tabs.query({url:`${new URL(routeUrl).origin}/*`}); return tabs.find((tab) => tab.url === routeUrl) || null; }

async function resolveCourierTab(route, local) {
  const routeUrl = route.chatgpt_url;
  const courier = await knownCourierTab(local);
  const exact = await exactTargetTab(routeUrl);
  if (exact?.id) return {tab:exact, reason:'Reusing exact registered target tab.'};
  if (courier?.id) {
    const beforeNavigation = await probeTab(courier.id);
    if (!beforeNavigation || beforeNavigation.composer_empty !== true) return {tab:null, reason:'Courier tab contains text or could not prove its composer empty; navigation was refused.', details:beforeNavigation || {url:courier.url}};
    await chrome.tabs.update(courier.id, {url:routeUrl});
    const navigated = await waitForExactUrl(courier.id, routeUrl);
    return navigated ? {tab:navigated, reason:'Reused background courier tab at exact route.'} : {tab:null, reason:'Courier tab did not reach the exact registered URL.', details:{}};
  }
  const created = await chrome.tabs.create({url:routeUrl, active:false});
  if (!created?.id) return {tab:null, reason:'Courier tab could not be created.', details:{}};
  await chrome.storage.local.set({courierTabId:created.id});
  const navigated = await waitForExactUrl(created.id, routeUrl);
  return navigated ? {tab:navigated, reason:'Created background courier tab at exact route.'} : {tab:null, reason:'New courier tab did not reach the exact registered URL.', details:{}};
}

async function probe(route, local, tab) {
  if (!tab?.id || tab.url !== route.chatgpt_url) { await reportReadiness(route, local); return {ready:false, reason:'Registered tab is not open at its exact URL.'}; }
  const result = await probeTab(tab.id);
  const ready = readyProbe(result, route.chatgpt_url);
  await reportReadiness(route, local, result || {});
  return {ready, tab, reason:ready ? 'Exact tab is ready.' : 'Composer or control is not ready.'};
}

async function waitForReady(route, local, tab) {
  let result = {ready:false, tab, reason:'Composer or control is not ready.'};
  for (let attempt = 0; attempt < 20; attempt += 1) { result = await probe(route, local, tab); if (result.ready) return result; if (!await tabById(tab.id)) return {ready:false, reason:'Courier tab closed before readiness completed.'}; await delay(150); }
  return result;
}

async function selectEligibleRoute(routes) {
  for (const route of routes) {
    let payload;
    try { payload = await call(`/extension/commands/${encodeURIComponent(route.route_name)}`); } catch (_) { return {route:null, reason:'Local server is unavailable.'}; }
    if (payload.paused) return {route:null, reason:'Server dispatch is paused.'};
    if (payload.command) return {route, command:payload.command};
  }
  return {route:null, reason:'No dispatch-eligible command.'};
}

async function pageDispatch(wake, routeUrl) {
  const findComposer = () => ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'].map((selector)=>document.querySelector(selector)).find(Boolean);
  const findSend = () => ['button[data-testid="send-button"]', 'button[data-testid*="send" i]', 'button[aria-label="Send prompt"]', 'button[aria-label="Send message"]', 'button[aria-label*="Send" i]'].map((selector)=>document.querySelector(selector)).find((node)=>node && !node.disabled);
  const read = (node) => normal(node?.value ?? node?.innerText);
  const node = findComposer(); if (!node) return {kind:'failed', note:'Composer unavailable before send.'};
  if (read(node)) return {kind:'failed', note:'Composer contains unrelated text; preserved.'};
  if (location.href !== routeUrl) return {kind:'failed', note:'Route changed before send.'};
  if ('value' in node) { node.focus(); node.value = wake; node.dispatchEvent(new Event('input', {bubbles:true})); } else { node.focus(); document.execCommand('insertText', false, wake); node.dispatchEvent(new InputEvent('input', {bubbles:true, inputType:'insertText', data:wake})); }
  if (read(node) !== normal(wake)) return {kind:'failed', note:'Composer insertion verification failed.'};
  await delay(150);
  const button = findSend(); if (!button) return {kind:'failed', note:'Send control unavailable before send.'};
  button.click(); await delay(1200);
  const delivered = [...document.querySelectorAll('[data-message-author-role="user"]')].some((item)=>normal(item.innerText) === normal(wake));
  return delivered ? {kind:'delivered'} : {kind:'uncertain', note:'Send may have occurred but expected user message was not proven.'};
}

async function poll() {
  const local = await state();
  await heartbeat();
  if (local.emergencyStop) return {ok:false, reason:'Emergency stop blocks dispatch.'};
  let routePayload;
  try { routePayload = await call('/routes'); } catch (_) { return {ok:false, reason:'Local server is unavailable.'}; }
  const routes = (routePayload.items || []).filter(availableRoute);
  if (!routes.length) return {ok:false, reason:'No available registered routes.'};
  const selected = await selectEligibleRoute(routes);
  if (!selected.route) return {ok:true, reason:selected.reason};
  if (requiresTestArm(selected.route.route_name) && !local.testArmed) return {ok:true, reason:'Test route is ready but test arm remains off.'};
  const resolved = await resolveCourierTab(selected.route, local);
  if (!resolved.tab) { await reportReadiness(selected.route, local, resolved.details); return {ok:false, reason:resolved.reason}; }
  const probeResult = await waitForReady(selected.route, local, resolved.tab);
  if (!probeResult.ready) return {ok:false, reason:probeResult.reason};
  let begun; try { begun = await call(`/commands/${encodeURIComponent(selected.command.command_id)}/begin`, {method:'POST'}); } catch (_) { return {ok:false, reason:'Server refused dispatch.'}; }
  let result;
  try { result = await chrome.tabs.sendMessage(probeResult.tab.id, {type:'dispatch', wake:begun.wake_payload, routeUrl:selected.route.chatgpt_url}); }
  catch (_) { try { result = await direct(probeResult.tab.id, pageDispatch, [begun.wake_payload, selected.route.chatgpt_url]); } catch (_) { await call(`/commands/${encodeURIComponent(begun.command_id)}/fail`, {method:'POST', body:JSON.stringify({note:'Exact-tab script was unavailable before send.'})}).catch(()=>{}); return {ok:false, reason:'Exact-tab script disappeared before send.'}; } }
  try {
    if (result.kind === 'delivered') await call(`/commands/${encodeURIComponent(begun.command_id)}/ack`, {method:'POST', body:JSON.stringify({note:'Expected user message appeared.'})});
    else if (result.kind === 'failed') await call(`/commands/${encodeURIComponent(begun.command_id)}/fail`, {method:'POST', body:JSON.stringify({note:result.note})});
    else await call(`/commands/${encodeURIComponent(begun.command_id)}/uncertain`, {method:'POST', body:JSON.stringify({note:result.note})});
  } catch (_) { await call(`/commands/${encodeURIComponent(begun.command_id)}/uncertain`, {method:'POST', body:JSON.stringify({note:'Transport became indeterminate after dispatch began.'})}).catch(()=>{}); }
  return {ok:true, reason:'Dispatch attempt reported.'};
}

chrome.tabs.onRemoved.addListener((tabId) => { clearCourierTab(tabId).catch(() => {}); });
chrome.alarms.create('lifeos-poll', {periodInMinutes:1});
chrome.alarms.onAlarm.addListener(poll);
chrome.runtime.onStartup.addListener(poll);
chrome.runtime.onInstalled.addListener(poll);
chrome.runtime.onMessage.addListener((message, _sender, reply) => { if (message.type === 'poll') { poll().then(reply); return true; } });
