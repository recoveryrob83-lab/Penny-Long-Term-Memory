(() => {
const ui = {
  list: document.getElementById("cc-history"),
  count: document.getElementById("cc-history-count"),
  status: document.getElementById("cc-history-filter-status"),
  destination: document.getElementById("cc-history-filter-destination"),
  mode: document.getElementById("cc-history-filter-mode"),
  sort: document.getElementById("cc-history-filter-sort"),
};

if (!ui.list) return;

let history = [];
let requestToken = 0;
let reloadTimer = null;

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

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

function eventTime(entry) {
  return Number(entry.finished_at || entry.started_at || 0);
}

function filteredHistory() {
  const status = ui.status.value;
  const destination = ui.destination.value;
  const mode = ui.mode.value;
  const direction = ui.sort.value === "oldest" ? 1 : -1;

  return history
    .filter((entry) => status === "all" || entry.status === status)
    .filter((entry) => destination === "all" || entry.destination === destination)
    .filter((entry) => mode === "all" || entry.mode === mode)
    .sort((left, right) => direction * (eventTime(left) - eventTime(right)));
}

function render() {
  const rows = filteredHistory();
  ui.count.textContent = `${rows.length} of ${history.length} runs`;
  observer.disconnect();
  ui.list.innerHTML = rows.map((entry) => {
    const timestamp = eventTime(entry)
      ? new Date(eventTime(entry) * 1000).toLocaleString()
      : "Time unavailable";
    const reason = entry.reason || entry.stderr?.trim() || entry.stdout?.trim() || "No result detail recorded.";
    const department = destinationLabels[entry.destination] || entry.destination || "Unknown destination";
    const promptType = entry.prompt_type === "canonical" ? "canonical" : "custom";
    return `<article class="cc-history-item">
      <div class="list-item-header"><strong>${escapeHtml(department)}</strong><span class="badge">${escapeHtml(entry.status || "unknown")}</span></div>
      <p class="item-meta">${escapeHtml(entry.mode || "unknown")} · ${escapeHtml(promptType)} · ${escapeHtml(timestamp)}</p>
      <p class="item-meta">${escapeHtml(reason)}</p>
    </article>`;
  }).join("") || '<div class="cc-history-item">No run-history entries match these filters.</div>';
  observer.observe(ui.list, {childList: true});
}

async function loadHistory() {
  const token = ++requestToken;
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Run history returned ${response.status}.`);
  const data = await response.json();
  if (token !== requestToken) return;
  history = data.history || [];
  render();
}

function scheduleReload() {
  clearTimeout(reloadTimer);
  reloadTimer = setTimeout(() => loadHistory().catch(() => {}), 50);
}

const observer = new MutationObserver(scheduleReload);
observer.observe(ui.list, {childList: true});

[ui.status, ui.destination, ui.mode, ui.sort].forEach((control) => {
  control.addEventListener("change", render);
});

loadHistory().catch((error) => {
  ui.list.innerHTML = `<div class="cc-history-item">${escapeHtml(error.message)}</div>`;
});
setInterval(() => loadHistory().catch(() => {}), 15000);
})();

(() => {
const DEBUG_CADENCE = "debug_5m";
const COMPLETION_MARKER = "Debug recurrence test completed after two attempts.";
const cadence = document.getElementById("cc-schedule-cadence");
const cadenceFilter = document.getElementById("cc-schedule-filter-cadence");
const confirmSend = document.getElementById("cc-confirm-send");
const scheduleName = document.getElementById("cc-schedule-name");
const scheduleDate = document.getElementById("cc-schedule-date");
const scheduleTime = document.getElementById("cc-schedule-time");
const destination = document.getElementById("cc-destination");
const summary = document.getElementById("cc-schedule-summary");
const scheduleList = document.getElementById("cc-schedules");
const scheduleCount = document.getElementById("cc-schedule-count");
const schedulerStatus = document.getElementById("cc-scheduler-status");
const stateFilter = document.getElementById("cc-schedule-filter-state");
const saveButton = document.getElementById("cc-save-schedule");
const cancelButton = document.getElementById("cc-cancel-schedule-edit");

if (
  !cadence
  || !cadenceFilter
  || !confirmSend
  || !summary
  || !scheduleList
  || !scheduleCount
  || !schedulerStatus
  || !stateFilter
) return;

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

function ensureOption(select, value, label) {
  if (Array.from(select.options).some((option) => option.value === value)) return;
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label;
  select.appendChild(option);
}

ensureOption(cadence, DEBUG_CADENCE, "Debug: every 5 minutes (2 drafts)");
ensureOption(cadenceFilter, DEBUG_CADENCE, "Debug: every 5 minutes");

function debugSelected() {
  return cadence.value === DEBUG_CADENCE;
}

function syncDebugControls() {
  const isDebug = debugSelected();
  if (isDebug) {
    confirmSend.checked = false;
    confirmSend.disabled = true;
    confirmSend.closest("label")?.setAttribute(
      "title",
      "Five-minute recurrence tests are always draft-only and stop after two attempts."
    );
    const name = scheduleName?.value.trim() || "This prompt";
    const target = destination?.selectedOptions[0]?.textContent || "the destination";
    if (scheduleDate?.value && scheduleTime?.value) {
      summary.textContent = `${name} will place a verified draft in ${target} every 5 minutes beginning ${scheduleDate.value} at ${scheduleTime.value} CT, then stop after 2 attempts.`;
    }
    return;
  }
  confirmSend.disabled = false;
  confirmSend.closest("label")?.removeAttribute("title");
}

function syncLedgerStatus(data) {
  const scheduler = data.scheduler_running ? "Scheduler running" : "Scheduler stopped";
  const ledger = data.schedule_ledger || {};
  let ledgerLabel = "Ledger off";
  if (ledger.configured) {
    ledgerLabel = ledger.state === "error"
      ? "Ledger error"
      : ledger.state === "synced"
        ? "Ledger synced"
        : "Ledger ready";
  }
  schedulerStatus.textContent = `${scheduler} · ${ledgerLabel}`;
  schedulerStatus.title = ledger.last_error || ledger.spreadsheet_url || "";
}

function hideCompletedFromUpcoming(completed) {
  return completed && ["scheduled", "paused"].includes(stateFilter.value);
}

let decorating = false;
let listObserver;

async function decorateDebugSchedules() {
  if (decorating) return;
  decorating = true;
  listObserver.disconnect();
  try {
    const response = await fetch("/api/command-center", {cache: "no-store"});
    if (!response.ok) return;
    const data = await response.json();
    syncLedgerStatus(data);
    (data.scheduled_jobs || [])
      .filter((schedule) => schedule.cadence === DEBUG_CADENCE)
      .forEach((schedule) => {
        const article = scheduleList.querySelector(`[data-schedule-id="${schedule.id}"]`);
        if (!article) return;
        const completed = String(schedule.last_reason || "").includes(COMPLETION_MARKER);
        if (hideCompletedFromUpcoming(completed)) {
          article.remove();
          return;
        }
        const metas = article.querySelectorAll("p.item-meta");
        const department = destinationLabels[schedule.destination] || schedule.destination;
        const next = schedule.next_run_at
          ? new Date(Number(schedule.next_run_at) * 1000).toLocaleString()
          : "No future run";
        if (metas[0]) {
          metas[0].textContent = `${department} · draft · Debug every 5 minutes (2 attempts max) · Next: ${next}`;
        }
        const badge = article.querySelector(".badge");
        if (badge) {
          badge.textContent = completed
            ? "Completed"
            : schedule.enabled
              ? schedule.last_run_at
                ? "Active · 1/2"
                : "Active · 0/2"
              : "Paused";
        }
        const toggle = article.querySelector('[data-schedule-action="toggle"]');
        if (toggle && completed) {
          toggle.textContent = "Completed";
          toggle.disabled = true;
        }
      });

    const visibleDefinitions = scheduleList.querySelectorAll("[data-schedule-id]").length;
    scheduleCount.textContent = `${visibleDefinitions} of ${(data.scheduled_jobs || []).length} definitions`;
    if (visibleDefinitions === 0 && ["scheduled", "paused"].includes(stateFilter.value)) {
      scheduleList.innerHTML = '<div class="cc-history-item">No upcoming scheduled jobs match these filters.</div>';
    }
  } catch (_) {
    // The primary scheduler UI remains authoritative when decoration cannot load.
  } finally {
    listObserver.observe(scheduleList, {childList: true});
    decorating = false;
  }
}

listObserver = new MutationObserver(() => {
  decorateDebugSchedules().catch(() => {});
});
listObserver.observe(scheduleList, {childList: true});

cadence.addEventListener("change", () => setTimeout(syncDebugControls, 0));
confirmSend.addEventListener("change", () => {
  if (debugSelected()) setTimeout(syncDebugControls, 0);
});
[scheduleDate, scheduleTime, destination].forEach((control) => {
  control?.addEventListener("change", () => setTimeout(syncDebugControls, 0));
});
scheduleName?.addEventListener("input", () => setTimeout(syncDebugControls, 0));
scheduleList.addEventListener("click", (event) => {
  if (event.target.closest('[data-schedule-action="edit"]')) {
    setTimeout(syncDebugControls, 250);
  }
});
saveButton?.addEventListener("click", () => setTimeout(syncDebugControls, 150));
cancelButton?.addEventListener("click", () => setTimeout(syncDebugControls, 100));

syncDebugControls();
setTimeout(() => decorateDebugSchedules().catch(() => {}), 100);
})();

(() => {
const COMPLETION_MARKER = "Debug recurrence test completed after two attempts.";
const scheduleList = document.getElementById("cc-schedules");
const scheduleCount = document.getElementById("cc-schedule-count");
const summary = document.getElementById("cc-schedule-summary");
const listMeta = scheduleCount?.closest(".cc-list-meta");

if (!scheduleList || !scheduleCount || !summary || !listMeta) return;

const button = document.createElement("button");
button.id = "cc-clear-completed";
button.className = "cc-danger-button";
button.type = "button";
button.hidden = true;
listMeta.appendChild(button);

let completedSchedules = [];
let refreshing = false;

function isCompleted(schedule) {
  if (schedule.enabled || schedule.next_run_at) return false;
  if (schedule.cadence === "once" && schedule.last_status === "succeeded") return true;
  return String(schedule.last_reason || "").includes(COMPLETION_MARKER);
}

async function refreshCompleted() {
  if (refreshing || button.disabled) return;
  refreshing = true;
  try {
    const response = await fetch("/api/command-center", {cache: "no-store"});
    if (!response.ok) return;
    const data = await response.json();
    completedSchedules = (data.scheduled_jobs || []).filter(isCompleted);
    button.hidden = completedSchedules.length === 0;
    button.textContent = `Clear completed (${completedSchedules.length})`;
    button.title = "Delete completed schedule definitions from the dashboard and Scheduler Ledger. Run history is preserved.";
  } finally {
    refreshing = false;
  }
}

button.addEventListener("click", async () => {
  await refreshCompleted();
  if (completedSchedules.length === 0) return;
  const confirmed = window.confirm(
    `Delete ${completedSchedules.length} completed schedule definition${completedSchedules.length === 1 ? "" : "s"}? `
    + "Their matching Scheduler Ledger rows will also be cleared. Run history will be preserved."
  );
  if (!confirmed) return;

  button.disabled = true;
  let deleted = 0;
  try {
    for (const schedule of completedSchedules) {
      const response = await fetch(`/api/command-center/schedules/${schedule.id}`, {method: "DELETE"});
      if (!response.ok) {
        throw new Error(
          `Cleanup stopped after ${deleted} deletion${deleted === 1 ? "" : "s"}. `
          + "The next Sheet row was not confirmed cleared, so its local schedule definition was kept."
        );
      }
      deleted += 1;
      scheduleList.querySelector(`[data-schedule-id="${schedule.id}"]`)?.remove();
    }
    summary.textContent = `Cleared ${deleted} completed schedule definition${deleted === 1 ? "" : "s"} from the dashboard and Scheduler Ledger. Run history was preserved.`;
  } catch (error) {
    summary.textContent = error.message;
  } finally {
    button.disabled = false;
    completedSchedules = [];
    await refreshCompleted();
  }
});

setTimeout(() => refreshCompleted().catch(() => {}), 250);
setInterval(() => refreshCompleted().catch(() => {}), 15000);
})();
