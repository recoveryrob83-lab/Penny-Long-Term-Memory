(() => {
const CONTEXT_PREFIX = "LIFEOS_RUN_CONTEXT=";
const BACKEND_PREFIX = "LIFEOS_BACKEND=";
const ui = {
  panel: document.querySelector('[data-tab-panel="automation-logs"]'),
  list: document.getElementById("automation-log-list"),
  count: document.getElementById("automation-log-count"),
  state: document.getElementById("automation-log-state"),
  result: document.getElementById("automation-log-filter-result"),
  destination: document.getElementById("automation-log-filter-destination"),
  trigger: document.getElementById("automation-log-filter-trigger"),
  workerState: document.getElementById("automation-log-filter-worker-state"),
  wake: document.getElementById("automation-log-filter-wake"),
  sort: document.getElementById("automation-log-filter-sort"),
  search: document.getElementById("automation-log-filter-search"),
  refresh: document.getElementById("automation-log-refresh"),
  expand: document.getElementById("automation-log-expand"),
  workerTotal: document.getElementById("automation-worker-total"),
  workerPending: document.getElementById("automation-worker-pending"),
  workerVerified: document.getElementById("automation-worker-verified"),
  workerRejected: document.getElementById("automation-worker-rejected"),
  workerWakes: document.getElementById("automation-worker-wakes"),
};

if (!ui.list) return;

const destinationLabels = {
  hub: "LifeOS_HQ",
  main: "Chief_of_Staff_HQ",
  engineering: "Engineering_HQ",
  logistics: "Maintenance_HQ",
  business: "Business_HQ",
  "office-leaks": "Office_Leaks_HQ",
  finance: "Finance_HQ",
  wellness: "Wellness_HQ",
};

const departmentKeys = {
  "main-assistant": "main",
  engineering: "engineering",
  "life-logistics-hq": "logistics",
  "business-development": "business",
  "office-leaks-consulting": "office-leaks",
  finance: "finance",
  wellness: "wellness",
};

let history = [];
let verificationRecords = [];
let verificationSummary = {};
let verificationByHistoryId = new Map();
let historySignature = "";
let requestToken = 0;
let expandAll = false;

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

function parsePrefixedJson(text, prefix) {
  const values = [];
  String(text || "").split(/\r?\n/).forEach((line) => {
    if (!line.startsWith(prefix)) return;
    try {
      values.push(JSON.parse(line.slice(prefix.length)));
    } catch (_) {
      values.push({event: "unparsed", raw: line.slice(prefix.length)});
    }
  });
  return values;
}

function runContext(entry) {
  return parsePrefixedJson(entry.stdout, CONTEXT_PREFIX)[0] || {};
}

function backendEvents(entry) {
  return parsePrefixedJson(entry.stdout, BACKEND_PREFIX);
}

function workerRecord(entry) {
  return verificationByHistoryId.get(Number(entry.id)) || null;
}

function eventTime(entry) {
  return Number(entry.finished_at || entry.started_at || 0);
}

function duration(entry, context) {
  const explicit = Number(context.duration_seconds);
  if (Number.isFinite(explicit)) return explicit;
  return Math.max(0, Number(entry.finished_at || 0) - Number(entry.started_at || 0));
}

function runId(entry, context, worker) {
  return worker?.run_id || context.run_id || `legacy-record-${entry.id ?? "unknown"}`;
}

function effectiveDestination(entry, worker) {
  if (!worker) return entry.destination || "unknown";
  return departmentKeys[worker.owning_department] || worker.owning_department;
}

function combinedLog(entry) {
  const context = runContext(entry);
  const worker = workerRecord(entry);
  const lines = [
    `record_id=${entry.id ?? "unknown"}`,
    `run_id=${runId(entry, context, worker)}`,
    `status=${entry.status || "unknown"}`,
    `destination=${entry.destination || "unknown"}`,
    `mode=${entry.mode || "unknown"}`,
    `prompt_type=${entry.prompt_type || "unknown"}`,
    `exit_code=${entry.exit_code ?? "none"}`,
    `started_at=${entry.started_at ?? "unknown"}`,
    `finished_at=${entry.finished_at ?? "unknown"}`,
    `reason=${entry.reason || ""}`,
  ];
  if (worker) {
    lines.push(
      `worker_id=${worker.worker_id}`,
      `task_id=${worker.task_id}`,
      `task_revision=${worker.task_revision}`,
      `owning_department=${worker.owning_department}`,
      `controlled_outcome=${worker.controlled_outcome}`,
      `verification_mode=${worker.verification_mode}`,
      `verification_state=${worker.verification_state}`,
      `review_route=${worker.review_route}`,
      `wake_disposition=${worker.wake_disposition}`,
      `wake_target=${worker.wake_target || "none"}`,
      `wake_reason=${worker.wake_reason || ""}`,
    );
  }
  lines.push(
    "",
    "===== STDOUT =====",
    entry.stdout || "<empty>",
    "",
    "===== STDERR =====",
    entry.stderr || "<empty>",
  );
  return lines.join("\n");
}

function filteredHistory() {
  const result = ui.result.value;
  const destination = ui.destination.value;
  const trigger = ui.trigger.value;
  const workerState = ui.workerState.value;
  const wake = ui.wake.value;
  const query = ui.search.value.trim().toLocaleLowerCase();
  const direction = ui.sort.value === "oldest" ? 1 : -1;

  return history
    .filter((entry) => result === "all" || entry.status === result)
    .filter((entry) => {
      if (destination === "all") return true;
      return effectiveDestination(entry, workerRecord(entry)) === destination;
    })
    .filter((entry) => {
      if (trigger === "all") return true;
      const worker = workerRecord(entry);
      const observed = String(runContext(entry).trigger || (worker ? "unknown" : "unknown"));
      return observed === trigger;
    })
    .filter((entry) => {
      if (workerState === "all") return true;
      const worker = workerRecord(entry);
      if (workerState === "not-worker") return !worker;
      return worker?.verification_state === workerState;
    })
    .filter((entry) => {
      if (wake === "all") return true;
      const worker = workerRecord(entry);
      if (!worker) return false;
      if (wake === "required") return Boolean(worker.wake_required);
      if (wake === "queued") return Boolean(worker.queue_eligible);
      return !worker.wake_required;
    })
    .filter((entry) => !query || combinedLog(entry).toLocaleLowerCase().includes(query))
    .sort((left, right) => direction * (eventTime(left) - eventTime(right)));
}

function fact(label, value) {
  return `<div class="automation-log-fact"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function captureDetailState() {
  const state = new Map();
  ui.list.querySelectorAll("details[data-detail-key]").forEach((details) => {
    state.set(details.getAttribute("data-detail-key"), details.open);
  });
  return state;
}

function detailOpen(previous, key, defaultValue, override) {
  if (typeof override === "boolean") return override;
  if (expandAll) return true;
  return previous.has(key) ? previous.get(key) : defaultValue;
}

function renderVerificationSummary() {
  ui.workerTotal.textContent = verificationSummary.total ?? 0;
  ui.workerPending.textContent = verificationSummary.pending ?? 0;
  ui.workerVerified.textContent = verificationSummary.verified ?? 0;
  ui.workerRejected.textContent = verificationSummary.rejected ?? 0;
  ui.workerWakes.textContent = verificationSummary.wake_required ?? 0;
}

function workerFacts(worker) {
  if (!worker) return "";
  const wake = worker.wake_required
    ? `${worker.wake_disposition} → ${worker.wake_target || "unresolved"}`
    : worker.queue_eligible
      ? "Routine queue · no immediate wake"
      : "Suppressed";
  return [
    fact("Worker", worker.worker_id),
    fact("Task", `${worker.task_id} · rev ${worker.task_revision}`),
    fact("Outcome", worker.controlled_outcome),
    fact("Verification", `${worker.verification_state} · ${worker.verification_mode}`),
    fact("Review route", worker.review_route),
    fact("Wake", wake),
  ].join("");
}

function render(openOverride = null) {
  const rows = filteredHistory();
  const previousDetails = captureDetailState();
  ui.count.textContent = `${rows.length} of ${history.length} runs`;
  ui.expand.textContent = expandAll ? "Collapse all" : "Expand all";
  renderVerificationSummary();

  ui.list.innerHTML = rows.map((entry, index) => {
    const context = runContext(entry);
    const worker = workerRecord(entry);
    const events = backendEvents(entry);
    const timestamp = eventTime(entry)
      ? new Date(eventTime(entry) * 1000).toLocaleString()
      : "Time unavailable";
    const destinationKey = effectiveDestination(entry, worker);
    const department = worker?.owning_department
      || destinationLabels[destinationKey]
      || entry.destination
      || "Unknown";
    const identity = runId(entry, context, worker);
    const trigger = context.trigger || (worker ? "worker" : "legacy");
    const schedule = context.schedule_name
      ? `${context.schedule_name} (#${context.schedule_id ?? "?"})`
      : "Not scheduled";
    const promptFingerprint = context.prompt_length == null
      ? worker ? "Worker wrapper / protected" : "Canonical / protected"
      : `${context.prompt_length} chars · ${context.prompt_sha256 || "hash unavailable"}`;
    const backendSummary = events.length
      ? events.map((event) => event.event || "event").join(" → ")
      : "No structured backend events (legacy or Worker transport run)";
    const runKey = `run:${identity}`;
    const stdoutKey = `${runKey}:stdout`;
    const stderrKey = `${runKey}:stderr`;
    const open = detailOpen(previousDetails, runKey, false, openOverride) ? " open" : "";
    const stdoutOpen = detailOpen(previousDetails, stdoutKey, true, openOverride) ? " open" : "";
    const stderrOpen = detailOpen(previousDetails, stderrKey, Boolean(entry.stderr), openOverride)
      ? " open"
      : "";
    const badge = worker
      ? `${worker.controlled_outcome} · ${worker.verification_state}`
      : entry.exit_code == null ? "no exit code" : `exit ${entry.exit_code}`;

    return `<details class="automation-log-entry" data-log-index="${index}" data-detail-key="${escapeHtml(runKey)}"${open}>
      <summary>
        <div class="automation-log-title">
          <strong>${escapeHtml(department)} · ${escapeHtml(entry.status || "unknown")}</strong>
          <span>${escapeHtml(timestamp)} · ${escapeHtml(trigger)} · ${escapeHtml(entry.mode || "unknown")} · ${escapeHtml(identity)}</span>
        </div>
        <span class="badge">${escapeHtml(badge)}</span>
      </summary>
      <div class="automation-log-body">
        <div class="automation-log-facts">
          ${fact("Record", entry.id ?? "legacy")}
          ${fact("Run ID", identity)}
          ${fact("Trigger", trigger)}
          ${fact("Schedule", schedule)}
          ${fact("Duration", `${duration(entry, context).toFixed(3)}s`)}
          ${fact("Timeout", context.timeout_seconds ? `${context.timeout_seconds}s` : "Unknown")}
          ${fact("Prompt", promptFingerprint)}
          ${fact("Streams", `${String(entry.stdout || "").length} stdout · ${String(entry.stderr || "").length} stderr chars`)}
          ${workerFacts(worker)}
        </div>
        <p class="automation-log-reason">${escapeHtml(worker?.receiver_reason || entry.reason || "No reason recorded.")}</p>
        ${worker ? `<div class="automation-log-wake"><span>Wake decision</span><strong>${escapeHtml(worker.wake_reason || "No wake reason recorded.")}</strong></div>` : ""}
        <div class="automation-log-fact"><span>Backend event path</span><strong>${escapeHtml(backendSummary)}</strong></div>
        <details class="automation-log-stream" data-detail-key="${escapeHtml(stdoutKey)}"${stdoutOpen}>
          <summary>Complete stdout (${String(entry.stdout || "").length} characters)</summary>
          <pre>${escapeHtml(entry.stdout || "<empty>")}</pre>
        </details>
        <details class="automation-log-stream" data-detail-key="${escapeHtml(stderrKey)}"${stderrOpen}>
          <summary>Complete stderr (${String(entry.stderr || "").length} characters)</summary>
          <pre>${escapeHtml(entry.stderr || "<empty>")}</pre>
        </details>
        <div class="automation-log-copy-row">
          <button class="copy-button" type="button" data-copy-log="${index}">Copy complete run log</button>
        </div>
      </div>
    </details>`;
  }).join("") || '<div class="automation-log-empty">No automation runs match these filters.</div>';
}

async function writeClipboard(value) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return;
  }
  const textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
}

async function loadLogs(showLoading = false) {
  const token = ++requestToken;
  if (showLoading) ui.state.textContent = "Loading";
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Automation logs returned ${response.status}.`);
  const data = await response.json();
  if (token !== requestToken) return;
  const nextHistory = data.history || [];
  const workerVerification = data.worker_verification || {summary: {}, records: []};
  const nextVerificationRecords = workerVerification.records || [];
  const nextSignature = JSON.stringify({
    history: nextHistory,
    verification: workerVerification,
  });
  const changed = nextSignature !== historySignature;
  history = nextHistory;
  verificationRecords = nextVerificationRecords;
  verificationSummary = workerVerification.summary || {};
  verificationByHistoryId = new Map(
    verificationRecords.map((record) => [Number(record.history_id), record]),
  );
  historySignature = nextSignature;
  ui.state.textContent = data.running ? "Run active" : "Ready";
  if (changed || showLoading) render();
}

[ui.result, ui.destination, ui.trigger, ui.workerState, ui.wake, ui.sort].forEach((control) => {
  control.addEventListener("change", () => render());
});
ui.search.addEventListener("input", () => render());
ui.refresh.addEventListener("click", () => {
  loadLogs(true).catch((error) => {
    ui.state.textContent = "Error";
    ui.list.innerHTML = `<div class="automation-log-empty">${escapeHtml(error.message)}</div>`;
  });
});
ui.expand.addEventListener("click", () => {
  expandAll = !expandAll;
  render(expandAll);
});
ui.list.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy-log]");
  if (!button) return;
  const entry = filteredHistory()[Number(button.dataset.copyLog)];
  if (!entry) return;
  const original = button.textContent;
  try {
    await writeClipboard(combinedLog(entry));
    button.textContent = "Copied";
  } catch (_) {
    button.textContent = "Copy failed";
  }
  setTimeout(() => { button.textContent = original; }, 1400);
});

loadLogs(true).catch((error) => {
  ui.state.textContent = "Error";
  ui.list.innerHTML = `<div class="automation-log-empty">${escapeHtml(error.message)}</div>`;
});
setInterval(() => {
  if (!ui.panel?.hidden) loadLogs(false).catch(() => {});
}, 5000);
})();
