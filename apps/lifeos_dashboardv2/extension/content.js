const selectors = ['#prompt-textarea', 'textarea[data-id="root"]', '[contenteditable="true"][role="textbox"]'];
const sendSelectors = ['button[data-testid="send-button"]', 'button[aria-label="Send prompt"]'];
const normal = (text) => String(text || '').replace(/\r\n/g, '\n').trim();
function composer() { return selectors.map((s) => document.querySelector(s)).find(Boolean); }
function sendButton() { return sendSelectors.map((s) => document.querySelector(s)).find((node) => node && !node.disabled); }
function getText(node) { return normal(node?.value ?? node?.innerText); }
function setText(node, text) { if ('value' in node) { node.focus(); node.value = text; node.dispatchEvent(new Event('input', {bubbles: true})); } else { node.focus(); document.execCommand('insertText', false, text); node.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: text})); } }
function userMessageExists(text) { return [...document.querySelectorAll('[data-message-author-role="user"]')].some((node) => normal(node.innerText) === normal(text)); }
chrome.runtime.onMessage.addListener((message, _sender, reply) => {
  if (message.type === 'preflight') { const node = composer(); return reply({url:location.href, content_script:true, composer_ready:!!node, composer_empty:!getText(node), send_ready:!!sendButton()}), true; }
  if (message.type === 'dispatch') {
    const node = composer(); if (!node) return reply({kind:'failed', note:'Composer unavailable before send.'}), true;
    if (getText(node)) return reply({kind:'failed', note:'Composer contains unrelated text; preserved.'}), true;
    if (location.href !== message.routeUrl) return reply({kind:'failed', note:'Route changed before send.'}), true;
    setText(node, message.wake); if (getText(node) !== normal(message.wake)) return reply({kind:'failed', note:'Composer insertion verification failed.'}), true;
    const button = sendButton(); if (!button) return reply({kind:'failed', note:'Send control unavailable before send.'}), true;
    button.click();
    setTimeout(() => reply(userMessageExists(message.wake) ? {kind:'delivered'} : {kind:'uncertain', note:'Send may have occurred but expected user message was not proven.'}), 1200);
    return true;
  }
  if (message.type === 'verify') return reply({delivered: userMessageExists(message.wake)}), true;
});
