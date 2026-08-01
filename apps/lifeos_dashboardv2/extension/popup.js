const server = 'http://127.0.0.1:8765';
const $ = (selector) => document.querySelector(selector);
const chatgptConversation = (url) => { try { const parsed = new URL(url); return parsed.origin === 'https://chatgpt.com' && parsed.pathname.includes('/c/'); } catch (_) { return false; } };
const request = async (path, options = {}) => { const response = await fetch(server + path, {headers:{'content-type':'application/json'}, ...options}); if (!response.ok) throw new Error(`${response.status}`); return response.json(); };

async function routes() { const payload = await request('/routes'); return payload.items || []; }
async function courierStatus() {
  const local = await chrome.storage.local.get({courierTabId:null});
  if (!Number.isInteger(local.courierTabId)) return 'No extension-owned courier tab.';
  try { const tab = await chrome.tabs.get(local.courierTabId); return `Courier tab #${tab.id}: ${tab.url}`; } catch (_) { return 'Courier tab reference is stale; it will be replaced when needed.'; }
}
function showRoutes(items) { $('#routes').textContent = items.length ? items.map((route) => `${route.route_name} -> ${route.chatgpt_url} (${route.health || 'AVAILABLE'})`).join('\n') : 'No server-registered routes.'; }
async function render(message = '') {
  const local = await chrome.storage.local.get({emergencyStop:false, testArmed:false});
  $('#arm').textContent = `Arm test dispatch: ${local.testArmed ? 'on' : 'off'}`;
  $('#routes').textContent = 'Loading server routes...';
  try { showRoutes(await routes()); $('#courier').textContent = await courierStatus(); $('#status').textContent = local.emergencyStop ? 'Emergency stop active.' : (message || 'Server registry is canonical; current tab is used only when registering a route.'); }
  catch (_) { $('#routes').textContent = 'Server routes unavailable.'; $('#courier').textContent = 'Courier tab status unavailable.'; $('#status').textContent = 'Local server is unavailable; no dispatch will be claimed.'; }
}

$('#register').onclick = async () => {
  const routeName = $('#route').value.trim();
  const [tab] = await chrome.tabs.query({active:true, currentWindow:true});
  if (!routeName || !chatgptConversation(tab?.url)) { $('#status').textContent = 'Choose a route label and an exact ChatGPT conversation URL.'; return; }
  let existing;
  try { existing = (await routes()).find((route) => route.route_name === routeName); } catch (_) { $('#status').textContent = 'Local server is unavailable; route was not registered.'; return; }
  if (existing && existing.chatgpt_url !== tab.url && !confirm(`Overwrite ${routeName} only?\n${existing.chatgpt_url}\nwith\n${tab.url}`)) return;
  try { await request('/routes', {method:'POST', body:JSON.stringify({route_name:routeName, target:routeName, chatgpt_url:tab.url})}); await render(`Registered ${routeName}; other server routes were preserved.`); }
  catch (_) { $('#status').textContent = 'Local server rejected route registration.'; }
};
$('#poll').onclick = async () => { try { const result = await chrome.runtime.sendMessage({type:'poll'}); $('#status').textContent = result.reason; } catch (_) { $('#status').textContent = 'Courier service worker is unavailable.'; } };
$('#arm').onclick = async () => { const local = await chrome.storage.local.get({testArmed:false}); await chrome.storage.local.set({testArmed:!local.testArmed}); render(); };
$('#stop').onclick = async () => { const local = await chrome.storage.local.get({emergencyStop:false}); await chrome.storage.local.set({emergencyStop:!local.emergencyStop}); render(); };
render();
