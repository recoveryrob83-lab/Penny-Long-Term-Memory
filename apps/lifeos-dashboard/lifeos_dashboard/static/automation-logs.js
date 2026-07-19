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
  sort: document.getElementById("automation-log-filter-sort"),
  search: document.getElementById("automation-log-filter-search"),
  refresh: document.getElementById("automation-log-refresh"),
  expand: document.getElementById("automation-log-expand"),
};

if (!ui.list) return;

const destinationLabels = {
  hub: "LifeOS HQ",
  main: "Chief of Staff HQ",
  engineering: "Engineering HQ",
  logistics: "Life OS Maintenance HQ",
  business: "Business HQ",
  "office-leaks": "Office Leaks HQ",
  finance: "Finance HQ",
  wellness: "Wellness HQ",
};

let history = [];
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

function eventTime(entry) {
  return Number(entry.finished_at || entry.started_at || 0);
}

function duration(entry, context) {
  const explicit = Number(context.duration_seconds);
  if (Number.isFinite(explicit)) return explicit;
  return Math.max(0, Number(entry.finished_at || 0) - Number(entry.started_at || 0));
}

function combinedLog(entry) {
  const context = runContext(entry);
  const lines = [
    `record_id=${entry.id ?? "unknown"}`,
    `run_id=${context.run_id || "unknown"}`,
    `status=${entry.status || "unknown"}`,
    `destination=${entry.destination || "unknown"}`,
    `mode=${entry.mode || "unknown"}`,
    `prompt_type=${entry.prompt_type || "unknown"}`,
    `exit_code=${entry.exit_code ?? "none"}`,
    `started_at=${entry.started_at ?? "unknown"}`,
    `finished_at=${entry.finished_at ?? "unknown"}`,
    `reason=${entry.reason || ""}`,
    "",
    "===== STDOUT =====",
    entry.stdout || "<empty>",
    "",
    "===== STDERR =====",
    entry.stderr || "<empty>",
  ];
  return lines.join("\n");
}

function filteredHistory() {
  const result = ui.result.value;
  const destination = ui.destination.value;
  const trigger = ui.trigger.value;
  const query = ui.search.value.trim().toLocaleLowerCase();
  const direction = ui.sort.value === "oldest" ? 1 : -1;

  return history
    .filter((entry) => result === "all" || entry.status === result)
    .filter((entry) => destination === "all" || entry.destination === destination)
    .filter((entry) => {
      if (trigger === "all") return true;
      return String(runContext(entry).trigger || "unknown") === trigger;
    })
    .filter((entry) => !query || combinedLog(entry).toLocaleLowerCase().includes(query))
    .sort((left, right) => direction * (eventTime(left) - eventTime(right)));
}

function fact(label, value) {
  return `<div class="automation-log-fact"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function render() {
  const rows = filteredHistory();
  ui.count.textContent = `${rows.length} of ${history.length} runs`;
  ui.expand.textContent = expandAll ? "Collapse all" : "Expand all";

  ui.list.innerHTML = rows.map((entry, index) => {
    const context = runContext(entry);
    const events = backendEvents(entry);
    const timestamp = eventTime(entry)
      ? new Date(eventTime(entry) * 1000).toLocaleString()
      : "Time unavailable";
    const department = destinationLabels[entry.destination] || entry.destination || "Unknown";
    const runId = context.run_id || `legacy-record-${entry.id ?? index}`;
    const trigger = context.trigger || "legacy";
    const schedule = context.schedule_name
      ? `${context.schedule_name} (#${context.schedule_id ?? "?"})`
      : "Not scheduled";
    const promptFingerprint = context.prompt_length == null
      ? "Canonical / protected"
      : `${context.prompt_length} chars · ${context.prompt_sha256 || "hash unavailable"}`;
    const backendSummary = events.length
      ? events.map((event) => event.event || "event").join(" → ")
      : "No structured backend events (legacy run)";
    const open = expandAll ? " open" : "";

    return `<details class="automation-log-entry" data-log-index="${index}"${open}>
      <summary>
        <div class="automation-log-title">
          <strong>${escapeHtml(department)} · ${escapeHtml(entry.status || "unknown")}</strong>
          <span>${escapeHtml(timestamp)} · ${escapeHtml(trigger)} · ${escapeHtml(entry.mode || "unknown")} · ${escapeHtml(runId)}</span>
        </div>
        <span class="badge">${escapeHtml(entry.exit_code == null ? "no exit code" : `exit ${entry.exit_code}`)}</span>
      </summary>
      <div class="automation-log-body">
        <div class="automation-log-facts">
          ${fact("Record", entry.id ?? "legacy")}
          ${fact("Run ID", runId)}
          ${fact("Trigger", trigger)}
          ${fact("Schedule", schedule)}
          ${fact("Duration", `${duration(entry, context).toFixed(3)}s`)}
          ${fact("Timeout", context.timeout_seconds ? `${context.timeout_seconds}s` : "Unknown")}
          ${fact("Prompt", promptFingerprint)}
          ${fact("Streams", `${String(entry.stdout || "").length} stdout · ${String(entry.stderr || "").length} stderr chars`)}
        </div>
        <p class="automation-log-reason">${escapeHtml(entry.reason || "No reason recorded.")}</p>
        <div class="automation-log-fact"><span>Backend event path</span><strong>${escapeHtml(backendSummary)}</strong></div>
        <details class="automation-log-stream" open>
          <summary>Complete stdout (${String(entry.stdout || "").length} characters)</summary>
          <pre>${escapeHtml(entry.stdout || "<empty>")}</pre>
        </details>
        <details class="automation-log-stream"${entry.stderr ? " open" : ""}>
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
  history = data.history || [];
  ui.state.textContent = data.running ? "Run active" : "Ready";
  render();
}

[ui.result, ui.destination, ui.trigger, ui.sort].forEach((control) => {
  control.addEventListener("change", render);
});
ui.search.addEventListener("input", render);
ui.refresh.addEventListener("click", () => {
  loadLogs(true).catch((error) => {
    ui.state.textContent = "Error";
    ui.list.innerHTML = `<div class="automation-log-empty">${escapeHtml(error.message)}</div>`;
  });
});
ui.expand.addEventListener("click", () => {
  expandAll = !expandAll;
  render();
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
