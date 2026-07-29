const server = 'http://127.0.0.1:8765';
const call = async (path, options = {}) => { const r = await fetch(server + path, {headers:{'content-type':'application/json'}, ...options}); if (!r.ok) throw new Error(`${r.status}`); return r.json(); };
const state = () => chrome.storage.local.get({emergencyStop:false, routeName:'', routeUrl:'', testArmed:false});
async function heartbeat() { try { await call('/extension/heartbeat', {method:'POST', body:JSON.stringify({version:chrome.runtime.getManifest().version})}); } catch (_) {} }
async function reportReadiness(local, details = {}) { try { return await call('/extension/readiness', {method:'POST', body:JSON.stringify({route_name:local.routeName, url:details.url || '', content_script:!!details.content_script, composer_ready:!!details.composer_ready, composer_empty:!!details.composer_empty, send_control:!!details.send_control, test_armed:!!local.testArmed})}); } catch (_) { return null; } }
async function probe(local) {
  const tabs = await chrome.tabs.query({url:`${new URL(local.routeUrl).origin}/*`}); const tab = tabs.find((item) => item.url === local.routeUrl);
  if (!tab?.id) { await reportReadiness(local); return {ready:false, reason:'Registered tab is not open at its exact URL.'}; }
  try {
    let result;
    try { result = await chrome.tabs.sendMessage(tab.id, {type:'preflight'}); }
    catch (_) {
      try { await chrome.scripting.executeScript({target:{tabId:tab.id}, files:['content.js']}); result = await chrome.tabs.sendMessage(tab.id, {type:'preflight'}); }
      catch (error) { return {ready:false, reason:`Content-script recovery failed: ${String(error?.message || 'unknown browser error')}`}; }
    }
    const ready = result?.url === local.routeUrl && result.content_script && result.composer_ready && result.composer_empty && result.send_control;
    await reportReadiness(local, result || {});
    return {ready, tab, reason:ready ? 'Exact tab is ready.' : 'Composer or control is not ready.'};
  } catch (error) { await reportReadiness(local); return {ready:false, reason:`Content script is unavailable: ${String(error?.message || 'unknown browser error')}`}; }
}
async function poll() {
  const local = await state(); await heartbeat(); if (local.emergencyStop || !local.routeName || !local.routeUrl) return {ok:false, reason:'Route or emergency-stop state blocks dispatch.'};
  const probeResult = await probe(local); if (!probeResult.ready || !local.testArmed) return {ok:probeResult.ready, reason:probeResult.ready ? 'Exact tab ready; test arm remains off.' : probeResult.reason};
  let payload; try { payload = await call(`/extension/commands/${encodeURIComponent(local.routeName)}`); } catch (_) { return {ok:false, reason:'Local server is unavailable.'}; }
  const command = payload.command; if (payload.paused || !command) return {ok:true, reason:'No dispatch-eligible command.'};
  let begun; try { begun = await call(`/commands/${encodeURIComponent(command.command_id)}/begin`, {method:'POST'}); } catch (_) { return {ok:false, reason:'Server refused dispatch.'}; }
  let result;
  try { result = await chrome.tabs.sendMessage(probeResult.tab.id, {type:'dispatch', wake:begun.wake_payload, routeUrl:local.routeUrl}); }
  catch (_) { await call(`/commands/${encodeURIComponent(begun.command_id)}/fail`, {method:'POST', body:JSON.stringify({note:'Content script was unavailable before send.'})}).catch(()=>{}); return {ok:false, reason:'Content script disappeared before send.'}; }
  try {
    if (result.kind === 'delivered') await call(`/commands/${encodeURIComponent(begun.command_id)}/ack`, {method:'POST', body:JSON.stringify({note:'Expected user message appeared.'})});
    else if (result.kind === 'failed') await call(`/commands/${encodeURIComponent(begun.command_id)}/fail`, {method:'POST', body:JSON.stringify({note:result.note})});
    else await call(`/commands/${encodeURIComponent(begun.command_id)}/uncertain`, {method:'POST', body:JSON.stringify({note:result.note})});
  } catch (_) { await call(`/commands/${encodeURIComponent(begun.command_id)}/uncertain`, {method:'POST', body:JSON.stringify({note:'Transport became indeterminate after dispatch began.'})}).catch(()=>{}); }
  return {ok:true, reason:'Dispatch attempt reported.'};
}
chrome.alarms.create('lifeos-poll', {periodInMinutes:1}); chrome.alarms.onAlarm.addListener(poll); chrome.runtime.onStartup.addListener(poll); chrome.runtime.onInstalled.addListener(poll); chrome.runtime.onMessage.addListener((m, _s, reply) => { if (m.type === 'poll') { poll().then(reply); return true; } });
