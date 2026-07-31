const server = 'http://127.0.0.1:8765';
const call = async (path, options = {}) => { const r = await fetch(server + path, {headers:{'content-type':'application/json'}, ...options}); if (!r.ok) throw new Error(`${r.status}`); return r.json(); };
const state = () => chrome.storage.local.get({emergencyStop:false, routeName:'', routeUrl:'', testArmed:false});
const normal = (text) => String(text || '').replace(/\r\n/g, '\n').trim();
const requiresTestArm = (routeName) => routeName.startsWith('slice_three_test');
async function heartbeat() { try { await call('/extension/heartbeat', {method:'POST', body:JSON.stringify({version:chrome.runtime.getManifest().version})}); } catch (_) {} }
async function reportReadiness(local, details = {}) { try { return await call('/extension/readiness', {method:'POST', body:JSON.stringify({route_name:local.routeName, url:details.url || '', content_script:!!details.content_script, composer_ready:!!details.composer_ready, composer_empty:!!details.composer_empty, send_control:!!details.send_control, test_armed:!!local.testArmed})}); } catch (_) { return null; } }
function pageProbe() {
  const composer = ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'].map((s)=>document.querySelector(s)).find(Boolean);
  const text = String(composer?.value ?? composer?.innerText ?? '').replace(/\r\n/g, '\n').trim();
  const send = ['button[data-testid="send-button"]', 'button[data-testid*="send" i]', 'button[aria-label="Send prompt"]', 'button[aria-label="Send message"]', 'button[aria-label*="Send" i]'].map((s)=>document.querySelector(s)).find(Boolean);
  const voice = ['button[data-testid*="voice"]', 'button[aria-label*="voice" i]'].map((s)=>document.querySelector(s)).find(Boolean);
  return {url:location.href, content_script:true, composer_ready:!!composer, composer_empty:!text, send_control:!!send || (!text && !!voice)};
}
async function direct(tabId, func, args = []) { const result = await chrome.scripting.executeScript({target:{tabId}, func, args}); return result[0]?.result; }
async function probe(local) {
  const tabs = await chrome.tabs.query({url:`${new URL(local.routeUrl).origin}/*`}); const tab = tabs.find((item) => item.url === local.routeUrl);
  if (!tab?.id) { await reportReadiness(local); return {ready:false, reason:'Registered tab is not open at its exact URL.'}; }
  try {
    let result;
    try { result = await chrome.tabs.sendMessage(tab.id, {type:'preflight'}); }
    catch (_) { result = await direct(tab.id, pageProbe); }
    const ready = result?.url === local.routeUrl && result.content_script && result.composer_ready && result.composer_empty && result.send_control;
    await reportReadiness(local, result || {});
    return {ready, tab, reason:ready ? 'Exact tab is ready.' : 'Composer or control is not ready.'};
  } catch (error) { await reportReadiness(local); return {ready:false, reason:`Exact-tab script probe failed: ${String(error?.message || 'unknown browser error')}`}; }
}
async function pageDispatch(wake, routeUrl) {
  const normal = (text) => String(text || '').replace(/\r\n/g, '\n').trim();
  const findComposer = () => ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'].map((s)=>document.querySelector(s)).find(Boolean);
  const findSend = () => ['button[data-testid="send-button"]', 'button[data-testid*="send" i]', 'button[aria-label="Send prompt"]', 'button[aria-label="Send message"]', 'button[aria-label*="Send" i]'].map((s)=>document.querySelector(s)).find((node)=>node && !node.disabled);
  const read = (node) => normal(node?.value ?? node?.innerText);
  const node = findComposer(); if (!node) return {kind:'failed', note:'Composer unavailable before send.'};
  if (read(node)) return {kind:'failed', note:'Composer contains unrelated text; preserved.'};
  if (location.href !== routeUrl) return {kind:'failed', note:'Route changed before send.'};
  if ('value' in node) { node.focus(); node.value = wake; node.dispatchEvent(new Event('input', {bubbles:true})); } else { node.focus(); document.execCommand('insertText', false, wake); node.dispatchEvent(new InputEvent('input', {bubbles:true, inputType:'insertText', data:wake})); }
  if (read(node) !== normal(wake)) return {kind:'failed', note:'Composer insertion verification failed.'};
  await new Promise((resolve)=>setTimeout(resolve, 150));
  const button = findSend(); if (!button) return {kind:'failed', note:'Send control unavailable before send.'};
  button.click(); await new Promise((resolve)=>setTimeout(resolve, 1200));
  const delivered = [...document.querySelectorAll('[data-message-author-role="user"]')].some((item)=>normal(item.innerText) === normal(wake));
  return delivered ? {kind:'delivered'} : {kind:'uncertain', note:'Send may have occurred but expected user message was not proven.'};
}
async function poll() {
  const local = await state(); await heartbeat(); if (local.emergencyStop || !local.routeName || !local.routeUrl) return {ok:false, reason:'Route or emergency-stop state blocks dispatch.'};
  const probeResult = await probe(local); if (!probeResult.ready || (requiresTestArm(local.routeName) && !local.testArmed)) return {ok:probeResult.ready, reason:probeResult.ready ? 'Exact tab ready; test arm remains off.' : probeResult.reason};
  let payload; try { payload = await call(`/extension/commands/${encodeURIComponent(local.routeName)}`); } catch (_) { return {ok:false, reason:'Local server is unavailable.'}; }
  const command = payload.command; if (payload.paused || !command) return {ok:true, reason:'No dispatch-eligible command.'};
  let begun; try { begun = await call(`/commands/${encodeURIComponent(command.command_id)}/begin`, {method:'POST'}); } catch (_) { return {ok:false, reason:'Server refused dispatch.'}; }
  let result;
  try { result = await chrome.tabs.sendMessage(probeResult.tab.id, {type:'dispatch', wake:begun.wake_payload, routeUrl:local.routeUrl}); }
  catch (_) { try { result = await direct(probeResult.tab.id, pageDispatch, [begun.wake_payload, local.routeUrl]); } catch (_) { await call(`/commands/${encodeURIComponent(begun.command_id)}/fail`, {method:'POST', body:JSON.stringify({note:'Exact-tab script was unavailable before send.'})}).catch(()=>{}); return {ok:false, reason:'Exact-tab script disappeared before send.'}; } }
  try {
    if (result.kind === 'delivered') await call(`/commands/${encodeURIComponent(begun.command_id)}/ack`, {method:'POST', body:JSON.stringify({note:'Expected user message appeared.'})});
    else if (result.kind === 'failed') await call(`/commands/${encodeURIComponent(begun.command_id)}/fail`, {method:'POST', body:JSON.stringify({note:result.note})});
    else await call(`/commands/${encodeURIComponent(begun.command_id)}/uncertain`, {method:'POST', body:JSON.stringify({note:result.note})});
  } catch (_) { await call(`/commands/${encodeURIComponent(begun.command_id)}/uncertain`, {method:'POST', body:JSON.stringify({note:'Transport became indeterminate after dispatch began.'})}).catch(()=>{}); }
  return {ok:true, reason:'Dispatch attempt reported.'};
}
chrome.alarms.create('lifeos-poll', {periodInMinutes:1}); chrome.alarms.onAlarm.addListener(poll); chrome.runtime.onStartup.addListener(poll); chrome.runtime.onInstalled.addListener(poll); chrome.runtime.onMessage.addListener((m, _s, reply) => { if (m.type === 'poll') { poll().then(reply); return true; } });
