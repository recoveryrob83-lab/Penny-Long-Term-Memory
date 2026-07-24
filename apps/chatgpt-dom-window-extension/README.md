# LifeOS ChatGPT DOM Window

> Experimental: static validation is complete, but live Edge and ChatGPT DOM behavior must still be measured before this is treated as proven.

A local Microsoft Edge Manifest V3 extension that reduces the rendered size of explicitly enabled long ChatGPT conversations.

It removes older rendered conversation turns while keeping a configurable recent window. The authoritative conversation remains on ChatGPT and can be restored by disabling trimming and reloading.

## Safety model

- Disabled by default for every conversation.
- Settings are keyed to one exact `/c/<conversation-id>` URL.
- Canonical `*_Worker` rooms are protected because the LifeOS browser courier counts rendered conversation turns.
- Auto-trim runs only near the bottom of the conversation.
- Trimming pauses while ChatGPT is generating, while the conversation route is changing, or while selected/focused content would be affected.
- `Alt` + `Shift` + click pins or unpins an individual turn.
- Restore disables trimming for the conversation and reloads the full authoritative history.
- No network requests, remote code, analytics, or external services.

## Install in Microsoft Edge

1. Pull the repository changes.
2. Open `edge://extensions`.
3. Enable **Developer mode**.
4. Select **Load unpacked**.
5. Choose this directory:

   ```text
   apps/chatgpt-dom-window-extension
   ```

6. Pin **LifeOS ChatGPT DOM Window** to the Edge toolbar.
7. Open the long human conversation, click the extension, enable it for that conversation, and choose the rendered-turn window.

Do not force-enable it in a LifeOS Worker room. The extension blocks canonical Worker titles as a second safety layer.

## What it can and cannot reduce

Removing old rendered turn subtrees can reduce DOM nodes, layout objects, event-bound descendants, syntax-highlighted code blocks, and other renderer-side weight. It does not remove ChatGPT's server history, and it may not reclaim memory retained by the site's JavaScript application state, React references, or browser caches. Measure the result in Edge Task Manager before and after trimming.

## Files

- `manifest.json`: Edge Manifest V3 package definition.
- `src/core.js`: pure conversation-key, settings, protection, and trim-plan logic.
- `src/content.js`: opt-in trimming, route watching, mutation observation, pinning, and restore behavior.
- `src/content.css`: lightweight placeholder, pin, and toast styles.
- `popup/`: toolbar controls and statistics.
- `tests/core.test.js`: dependency-free Node tests for the pure trim logic.

## Validate

From this directory:

```powershell
node --test tests\core.test.js
node --check src\core.js
node --check src\content.js
node --check popup\popup.js
```

## Live smoke checklist

1. Confirm an ordinary saved conversation is detected and a canonical `*_Worker` room is Protected.
2. Record the ChatGPT renderer memory in Edge Task Manager.
3. Enable the extension for one long human conversation and begin with a 40-turn window.
4. Confirm old rendered turns disappear while scrolling, composing, and receiving a new response still work.
5. Record renderer memory again after Edge has had time to reclaim eligible resources.
6. Use **Restore full chat** and confirm the complete authoritative history returns after reload.
