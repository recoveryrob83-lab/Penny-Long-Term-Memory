(function exposeCore(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.ChatGPTDomTrimmerCore = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function buildCore() {
  "use strict";

  const MIN_KEEP_TURNS = 10;
  const MAX_KEEP_TURNS = 200;
  const DEFAULT_KEEP_TURNS = 40;

  function conversationKeyFromUrl(value) {
    try {
      const url = new URL(value);
      if (url.protocol !== "https:" || url.hostname !== "chatgpt.com") return null;
      const match = url.pathname.match(/(?:^|\/)c\/([^/?#]+)/);
      return match ? `c:${match[1]}` : null;
    } catch {
      return null;
    }
  }

  function clampKeepTurns(value) {
    const parsed = Number.parseInt(String(value), 10);
    if (!Number.isFinite(parsed)) return DEFAULT_KEEP_TURNS;
    return Math.min(MAX_KEEP_TURNS, Math.max(MIN_KEEP_TURNS, parsed));
  }

  function normalizeConversationConfig(value) {
    const input = value && typeof value === "object" ? value : {};
    return {
      enabled: input.enabled === true,
      autoTrim: input.autoTrim !== false,
      keepTurns: clampKeepTurns(input.keepTurns),
      pinnedTurnIds: Array.isArray(input.pinnedTurnIds)
        ? [...new Set(input.pinnedTurnIds.filter((item) => typeof item === "string" && item))]
        : [],
    };
  }

  function buildTrimPlan(turns, keepTurns, pinnedTurnIds) {
    const normalizedKeep = clampKeepTurns(keepTurns);
    const pinned = new Set(pinnedTurnIds || []);
    const cutoff = Math.max(0, turns.length - normalizedKeep);
    const remove = [];
    const keep = [];

    turns.forEach((turn, index) => {
      const isRecent = index >= cutoff;
      const isPinned = pinned.has(turn.id);
      if (!isRecent && !isPinned && turn.protected !== true) remove.push(turn);
      else keep.push(turn);
    });

    return {
      remove,
      keep,
      cutoff,
      keepTurns: normalizedKeep,
      pinnedCount: keep.filter((turn) => pinned.has(turn.id)).length,
    };
  }

  function workerTitleLooksProtected(value) {
    const title = String(value || "").trim();
    return /(?:^|\s|[-|])\w+_Worker(?:\s|$|[-|])/i.test(title)
      || /\bWorker\s*-\s*ChatGPT\b/i.test(title);
  }

  return {
    DEFAULT_KEEP_TURNS,
    MAX_KEEP_TURNS,
    MIN_KEEP_TURNS,
    buildTrimPlan,
    clampKeepTurns,
    conversationKeyFromUrl,
    normalizeConversationConfig,
    workerTitleLooksProtected,
  };
});
