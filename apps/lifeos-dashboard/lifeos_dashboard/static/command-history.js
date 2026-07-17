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
  main: "Main Assistant HQ",
  engineering: "Engineering HQ",
  logistics: "Logistics HQ",
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
