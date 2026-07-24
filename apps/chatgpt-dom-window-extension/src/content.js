(() => {
  "use strict";

  const Core = globalThis.ChatGPTDomTrimmerCore;
  if (!Core) return;

  const STORAGE_KEY = "conversationConfigs";
  const PRIMARY_TURN_SELECTOR = '[data-testid^="conversation-turn-"]';
  const FALLBACK_MESSAGE_SELECTOR = "[data-message-author-role]";
  const PROMPT_SELECTOR = "#prompt-textarea";
  const STOP_SELECTOR = 'button[data-testid="stop-button"]';
  const PLACEHOLDER_ID = "lifeos-dom-window-placeholder";
  const ROUTE_STABLE_MS = 1600;
  const AUTO_TRIM_DEBOUNCE_MS = 1200;
  const NEAR_BOTTOM_PX = 1400;

  let activeConversationKey = Core.conversationKeyFromUrl(location.href);
  let routeChangedAt = Date.now();
  let config = Core.normalizeConversationConfig(null);
  let trimTimer = null;
  let routeTimer = null;
  let observer = null;
  let trimmedTurnIds = new Set();
  let stats = freshStats();

  function freshStats() {
    return {
      trimmedTurns: 0,
      trimmedElements: 0,
      lastTrimmedTurns: 0,
      lastTrimmedElements: 0,
      visibleTurns: 0,
      lastTrimmedAt: null,
    };
  }

  function storageGet(key) {
    return new Promise((resolve) => chrome.storage.local.get(key, resolve));
  }

  function storageSet(value) {
    return new Promise((resolve) => chrome.storage.local.set(value, resolve));
  }

  async function readAllConfigs() {
    const result = await storageGet(STORAGE_KEY);
    const value = result?.[STORAGE_KEY];
    return value && typeof value === "object" ? value : {};
  }

  async function loadConfig() {
    activeConversationKey = Core.conversationKeyFromUrl(location.href);
    if (!activeConversationKey) {
      config = Core.normalizeConversationConfig(null);
      return config;
    }
    const configs = await readAllConfigs();
    config = Core.normalizeConversationConfig(configs[activeConversationKey]);
    applyPinnedClasses();
    return config;
  }

  async function saveConfig(nextConfig) {
    if (!activeConversationKey) throw new Error("Open a saved ChatGPT conversation first.");
    const configs = await readAllConfigs();
    config = Core.normalizeConversationConfig(nextConfig);
    configs[activeConversationKey] = config;
    await storageSet({[STORAGE_KEY]: configs});
    applyPinnedClasses();
    return config;
  }

  function currentTitle() {
    const heading = document.querySelector("main h1, main h2, header h1, header h2");
    return `${document.title} ${heading?.textContent || ""}`.trim();
  }

  function isWorkerProtected() {
    return Core.workerTitleLooksProtected(currentTitle());
  }

  function isGenerating() {
    const stop = document.querySelector(STOP_SELECTOR);
    return Boolean(stop && stop.getClientRects().length);
  }

  function composerReady() {
    const prompt = document.querySelector(PROMPT_SELECTOR);
    return Boolean(prompt && prompt.getClientRects().length);
  }

  function stableRoute() {
    return Date.now() - routeChangedAt >= ROUTE_STABLE_MS;
  }

  function getTurnElements() {
    const primary = [...document.querySelectorAll(PRIMARY_TURN_SELECTOR)];
    if (primary.length) return primary;

    const seen = new Set();
    const fallback = [];
    for (const message of document.querySelectorAll(FALLBACK_MESSAGE_SELECTOR)) {
      const turn = message.closest("article") || message.parentElement;
      if (turn && !seen.has(turn)) {
        seen.add(turn);
        fallback.push(turn);
      }
    }
    return fallback;
  }

  function turnId(element, index) {
    const testId = element.getAttribute("data-testid");
    if (testId) return testId;
    const role = element.querySelector(FALLBACK_MESSAGE_SELECTOR)?.getAttribute("data-message-author-role") || "turn";
    const text = (element.textContent || "").trim().slice(0, 120);
    return `fallback:${index}:${role}:${simpleHash(text)}`;
  }

  function simpleHash(value) {
    let hash = 2166136261;
    for (let index = 0; index < value.length; index += 1) {
      hash ^= value.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(36);
  }

  function selectionTouches(element) {
    const selection = document.getSelection();
    if (!selection || selection.rangeCount === 0 || selection.isCollapsed) return false;
    const range = selection.getRangeAt(0);
    return element.contains(range.commonAncestorContainer) || range.intersectsNode(element);
  }

  function turnRecords() {
    const pinned = new Set(config.pinnedTurnIds);
    const active = document.activeElement;
    return getTurnElements().map((element, index) => {
      const id = turnId(element, index);
      return {
        element,
        id,
        protected: pinned.has(id)
          || Boolean(active && element.contains(active))
          || selectionTouches(element),
      };
    });
  }

  function findScrollContainer(element) {
    let current = element?.parentElement;
    while (current && current !== document.body) {
      const style = getComputedStyle(current);
      const scrollable = /(auto|scroll|overlay)/.test(style.overflowY)
        && current.scrollHeight > current.clientHeight + 16;
      if (scrollable) return current;
      current = current.parentElement;
    }
    return document.scrollingElement || document.documentElement;
  }

  function distanceFromBottom(scroller) {
    if (!scroller) return Number.POSITIVE_INFINITY;
    if (scroller === document.scrollingElement || scroller === document.documentElement) {
      const root = document.scrollingElement || document.documentElement;
      return root.scrollHeight - root.scrollTop - root.clientHeight;
    }
    return scroller.scrollHeight - scroller.scrollTop - scroller.clientHeight;
  }

  function isNearBottom(turns) {
    const last = turns.at(-1)?.element;
    return distanceFromBottom(findScrollContainer(last)) <= NEAR_BOTTOM_PX;
  }

  function countElements(element) {
    return 1 + element.querySelectorAll("*").length;
  }

  function removePlaceholder() {
    document.getElementById(PLACEHOLDER_ID)?.remove();
  }

  function ensurePlaceholder(anchor) {
    if (!anchor?.parentNode) return;
    let placeholder = document.getElementById(PLACEHOLDER_ID);
    if (!placeholder) {
      placeholder = document.createElement("section");
      placeholder.id = PLACEHOLDER_ID;
      placeholder.className = "lifeos-dom-window-placeholder";
      placeholder.innerHTML = `
        <strong data-lifeos-trim-summary></strong>
        <span data-lifeos-trim-detail></span>
        <div class="lifeos-dom-window-placeholder-actions">
          <button type="button" data-lifeos-trim-action="restore">Restore full chat</button>
          <button type="button" data-lifeos-trim-action="trim">Trim again</button>
        </div>`;
      placeholder.addEventListener("click", async (event) => {
        const button = event.target.closest("button[data-lifeos-trim-action]");
        if (!button) return;
        if (button.dataset.lifeosTrimAction === "restore") await restoreFullChat();
        if (button.dataset.lifeosTrimAction === "trim") await trimNow({manual: true});
      });
    }

    if (placeholder.nextElementSibling !== anchor) {
      anchor.parentNode.insertBefore(placeholder, anchor);
    }
    placeholder.querySelector("[data-lifeos-trim-summary]").textContent =
      `${stats.trimmedTurns} earlier turns removed from the rendered page`;
    placeholder.querySelector("[data-lifeos-trim-detail]").textContent =
      `Approximately ${stats.trimmedElements.toLocaleString()} DOM elements released. Reload restores the authoritative conversation.`;
  }

  function applyPinnedClasses() {
    const pinned = new Set(config.pinnedTurnIds);
    getTurnElements().forEach((element, index) => {
      element.classList.toggle("lifeos-dom-window-pinned", pinned.has(turnId(element, index)));
    });
  }

  function toast(message) {
    document.querySelector(".lifeos-dom-window-toast")?.remove();
    const node = document.createElement("div");
    node.className = "lifeos-dom-window-toast";
    node.textContent = message;
    document.documentElement.appendChild(node);
    window.setTimeout(() => node.remove(), 2400);
  }

  async function togglePinForTurn(element) {
    if (!activeConversationKey || isWorkerProtected()) return;
    const turns = getTurnElements();
    const index = turns.indexOf(element);
    if (index < 0) return;
    const id = turnId(element, index);
    const pinned = new Set(config.pinnedTurnIds);
    if (pinned.has(id)) {
      pinned.delete(id);
      toast("Turn unpinned. It may be trimmed later.");
    } else {
      pinned.add(id);
      toast("Turn pinned. It will be preserved when older turns are trimmed.");
    }
    await saveConfig({...config, pinnedTurnIds: [...pinned]});
  }

  async function trimNow({manual = false} = {}) {
    await loadConfig();
    if (!activeConversationKey || !config.enabled) return statusPayload("disabled");
    if (isWorkerProtected()) return statusPayload("worker-protected");
    if (!stableRoute() || !composerReady() || isGenerating()) {
      return statusPayload("busy");
    }

    const turns = turnRecords();
    stats.visibleTurns = turns.length;
    if (!manual && !isNearBottom(turns)) return statusPayload("reading-history");

    const plan = Core.buildTrimPlan(turns, config.keepTurns, config.pinnedTurnIds);
    if (!plan.remove.length) {
      if (stats.trimmedTurns && plan.keep[0]?.element) ensurePlaceholder(plan.keep[0].element);
      return statusPayload("nothing-to-trim");
    }

    const anchor = plan.keep[0]?.element;
    if (!anchor) return statusPayload("no-anchor");
    const scroller = findScrollContainer(anchor);
    const anchorTopBefore = anchor.getBoundingClientRect().top;
    let removedElements = 0;
    let newTurnCount = 0;

    for (const turn of plan.remove) {
      removedElements += countElements(turn.element);
      if (!trimmedTurnIds.has(turn.id)) {
        trimmedTurnIds.add(turn.id);
        newTurnCount += 1;
      }
      turn.element.remove();
    }

    ensurePlaceholder(anchor);
    const anchorTopAfter = anchor.getBoundingClientRect().top;
    const delta = anchorTopAfter - anchorTopBefore;
    if (Number.isFinite(delta) && Math.abs(delta) > 1) {
      if (scroller === document.scrollingElement || scroller === document.documentElement) {
        window.scrollBy(0, delta);
      } else {
        scroller.scrollTop += delta;
      }
    }

    stats.trimmedTurns += newTurnCount;
    stats.trimmedElements += removedElements;
    stats.lastTrimmedTurns = plan.remove.length;
    stats.lastTrimmedElements = removedElements;
    stats.visibleTurns = getTurnElements().length;
    stats.lastTrimmedAt = Date.now();
    ensurePlaceholder(anchor);
    return statusPayload("trimmed");
  }

  async function restoreFullChat() {
    if (activeConversationKey) {
      await saveConfig({...config, enabled: false});
    }
    removePlaceholder();
    location.reload();
  }

  function scheduleTrim(delay = AUTO_TRIM_DEBOUNCE_MS) {
    window.clearTimeout(trimTimer);
    if (!config.enabled || !config.autoTrim) return;
    trimTimer = window.setTimeout(() => trimNow({manual: false}), delay);
  }

  function statusPayload(reason = "ready") {
    const turns = getTurnElements();
    return {
      ok: true,
      reason,
      conversationKey: activeConversationKey,
      supportedConversation: Boolean(activeConversationKey),
      workerProtected: isWorkerProtected(),
      generating: isGenerating(),
      config,
      stats: {...stats, visibleTurns: turns.length},
      title: currentTitle(),
    };
  }

  async function handleRouteChange() {
    const nextKey = Core.conversationKeyFromUrl(location.href);
    if (nextKey === activeConversationKey) return;
    activeConversationKey = nextKey;
    routeChangedAt = Date.now();
    trimmedTurnIds = new Set();
    stats = freshStats();
    removePlaceholder();
    await loadConfig();
    scheduleTrim(ROUTE_STABLE_MS + 250);
  }

  function startRouteWatcher() {
    let previousHref = location.href;
    routeTimer = window.setInterval(() => {
      if (location.href !== previousHref) {
        previousHref = location.href;
        handleRouteChange();
      }
    }, 500);
  }

  function startObserver() {
    observer?.disconnect();
    observer = new MutationObserver((mutations) => {
      if (!config.enabled || !config.autoTrim) return;
      if (mutations.some((mutation) => mutation.addedNodes.length || mutation.removedNodes.length)) {
        scheduleTrim();
      }
    });
    observer.observe(document.documentElement, {childList: true, subtree: true});
  }

  document.addEventListener("click", (event) => {
    if (!event.altKey || !event.shiftKey) return;
    const turn = event.target.closest(PRIMARY_TURN_SELECTOR);
    if (!turn) return;
    event.preventDefault();
    event.stopPropagation();
    togglePinForTurn(turn);
  }, true);

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    void sender;
    (async () => {
      switch (message?.type) {
        case "GET_STATUS":
          await loadConfig();
          return statusPayload();
        case "SET_CONFIG": {
          await loadConfig();
          if (isWorkerProtected() && message.config?.enabled === true) {
            throw new Error("Worker conversations are protected because LifeOS transport counts rendered turns.");
          }
          await saveConfig({...config, ...message.config});
          if (config.enabled) scheduleTrim(50);
          else removePlaceholder();
          return statusPayload("config-saved");
        }
        case "TRIM_NOW":
          return trimNow({manual: true});
        case "RESTORE_FULL":
          await restoreFullChat();
          return {ok: true, reason: "reloading"};
        default:
          throw new Error("Unknown DOM Window command.");
      }
    })().then(sendResponse).catch((error) => sendResponse({ok: false, error: error.message}));
    return true;
  });

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== "local" || !changes[STORAGE_KEY]) return;
    loadConfig().then(() => scheduleTrim(50));
  });

  loadConfig().then(() => {
    startObserver();
    startRouteWatcher();
    scheduleTrim(ROUTE_STABLE_MS + 250);
  });

  window.addEventListener("beforeunload", () => {
    observer?.disconnect();
    window.clearInterval(routeTimer);
    window.clearTimeout(trimTimer);
  }, {once: true});
})();
