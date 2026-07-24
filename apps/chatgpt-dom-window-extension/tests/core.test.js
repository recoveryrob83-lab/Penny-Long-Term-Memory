const test = require("node:test");
const assert = require("node:assert/strict");

const Core = require("../src/core.js");

test("extracts stable ChatGPT conversation keys", () => {
  assert.equal(
    Core.conversationKeyFromUrl("https://chatgpt.com/c/abc-123?model=gpt-5"),
    "c:abc-123",
  );
  assert.equal(
    Core.conversationKeyFromUrl("https://chatgpt.com/g/gizmo/c/xyz"),
    "c:xyz",
  );
  assert.equal(Core.conversationKeyFromUrl("https://chatgpt.com/"), null);
  assert.equal(Core.conversationKeyFromUrl("https://example.com/c/abc"), null);
});

test("normalizes bounded per-conversation settings", () => {
  assert.deepEqual(Core.normalizeConversationConfig(null), {
    enabled: false,
    autoTrim: true,
    keepTurns: 40,
    pinnedTurnIds: [],
  });
  assert.deepEqual(Core.normalizeConversationConfig({
    enabled: true,
    autoTrim: false,
    keepTurns: 2,
    pinnedTurnIds: ["a", "a", "", 4, "b"],
  }), {
    enabled: true,
    autoTrim: false,
    keepTurns: 10,
    pinnedTurnIds: ["a", "b"],
  });
});

test("keeps the recent window and pinned old turns", () => {
  const turns = Array.from({length: 8}, (_, index) => ({id: `turn-${index}`}));
  const plan = Core.buildTrimPlan(turns, 10, ["turn-1"]);
  assert.equal(plan.remove.length, 0, "minimum keep window prevents tiny destructive plans");

  const longTurns = Array.from({length: 30}, (_, index) => ({id: `turn-${index}`}));
  const longPlan = Core.buildTrimPlan(longTurns, 10, ["turn-2", "turn-7"]);
  assert.deepEqual(longPlan.remove.map((turn) => turn.id), [
    "turn-0", "turn-1", "turn-3", "turn-4", "turn-5", "turn-6", "turn-8", "turn-9",
    "turn-10", "turn-11", "turn-12", "turn-13", "turn-14", "turn-15", "turn-16",
    "turn-17", "turn-18", "turn-19",
  ]);
  assert.equal(longPlan.keep.length, 12);
  assert.equal(longPlan.pinnedCount, 2);
});

test("preserves temporarily protected turns", () => {
  const turns = Array.from({length: 20}, (_, index) => ({
    id: `turn-${index}`,
    protected: index === 3,
  }));
  const plan = Core.buildTrimPlan(turns, 10, []);
  assert.equal(plan.remove.some((turn) => turn.id === "turn-3"), false);
});

test("recognizes canonical Worker room titles", () => {
  assert.equal(Core.workerTitleLooksProtected("Engineering_Worker - ChatGPT"), true);
  assert.equal(Core.workerTitleLooksProtected("LifeOS Planning - ChatGPT"), false);
});
