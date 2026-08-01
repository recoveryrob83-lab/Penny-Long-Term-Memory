const composerSelectors = ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'];
const sendSelectors = ['button[data-testid="send-button"]', 'button[aria-label="Send prompt"]', 'button[aria-label="Send message"]'];
const voiceSelectors = ['button[data-testid*="voice"]', 'button[aria-label*="voice" i]'];
const normal = (text) => String(text || '').replace(/\r\n/g, '\n').trim();
const pause = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

function composer() { return composerSelectors.map((selector) => document.querySelector(selector)).find(Boolean); }
function visible(node) { return !!node && !node.disabled && node.getAttribute('aria-hidden') !== 'true' && node.getClientRects().length > 0; }
function getText(node) { return normal(node?.value ?? node?.innerText); }
function sameComposerContext(button, node) { const composerForm = node.closest?.('form'); const buttonForm = button.closest?.('form'); return !composerForm || !buttonForm || composerForm === buttonForm; }
function sendButton(node) { return sendSelectors.flatMap((selector) => [...document.querySelectorAll(selector)]).find((button) => visible(button) && sameComposerContext(button, node)) || null; }
function voiceControl() { return voiceSelectors.flatMap((selector) => [...document.querySelectorAll(selector)]).find(visible) || null; }
function inputEvent(text) { return typeof InputEvent === 'function' ? new InputEvent('input', {bubbles:true, inputType:'insertText', data:text}) : new Event('input', {bubbles:true}); }
function setText(node, text) {
  if ('value' in node) {
    const descriptor = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(node), 'value');
    if (descriptor?.set) descriptor.set.call(node, text); else node.value = text;
    node.focus(); node.dispatchEvent(inputEvent(text));
  } else {
    node.focus(); document.execCommand('insertText', false, text); node.dispatchEvent(inputEvent(text));
  }
}
function userMessages() { return [...document.querySelectorAll('[data-message-author-role="user"]')]; }
function newExpectedMessage(baseline, wake) { return userMessages().some((node) => !baseline.has(node) && normal(node.innerText) === normal(wake)); }
async function waitForSend(node, wake) { for (let attempt = 0; attempt < 20; attempt += 1) { if (getText(node) !== normal(wake)) return null; const button = sendButton(node); if (button) return button; await pause(100); } return null; }
async function waitForDelivery(baseline, wake) { for (let attempt = 0; attempt < 30; attempt += 1) { if (newExpectedMessage(baseline, wake)) return true; await pause(250); } return false; }

chrome.runtime.onMessage.addListener((message, _sender, reply) => {
  if (message.type === 'preflight') { const node = composer(); const empty = !getText(node); const send = sendButton(node); return reply({url:location.href, content_script:true, composer_ready:!!node, composer_empty:empty, send_control:!!send || (empty && !!voiceControl()), control_mode:send ? 'SEND' : (voiceControl() ? 'VOICE_EMPTY' : 'MISSING')}), true; }
  if (message.type === 'dispatch') { (async () => {
    const node = composer(); if (!node) return reply({kind:'failed', note:'Composer unavailable.'}), true;
    if (getText(node)) return reply({kind:'failed', note:'Composer contains unrelated text; preserved.'}), true;
    if (location.href !== message.routeUrl) return reply({kind:'failed', note:'Route changed before send.'}), true;
    setText(node, message.wake);
    const button = await waitForSend(node, message.wake);
    if (getText(node) !== normal(message.wake)) return reply({kind:'failed', note:'Insertion rejected.'}), true;
    if (!button) return reply({kind:'failed', note:'Send control unavailable.'}), true;
    if (location.href !== message.routeUrl) return reply({kind:'failed', note:'Route changed before send.'}), true;
    const baseline = new Set(userMessages());
    button.click();
    return reply(await waitForDelivery(baseline, message.wake) ? {kind:'delivered', note:'Expected user message proven.'} : {kind:'uncertain', note:'Click attempted but user-message proof absent.'}), true;
  })(); return true; }
  if (message.type === 'verify') return reply({delivered:newExpectedMessage(new Set(), message.wake)}), true;
});
