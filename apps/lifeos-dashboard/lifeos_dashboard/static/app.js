const byId = (id) => document.getElementById(id);

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const showToast = (message) => {
  const toast = byId("toast");
  toast.textContent = message;
  toast.classList.add("visible");
  window.setTimeout(() => toast.classList.remove("visible"), 1800);
};

const renderSources = (sources = []) => {
  byId("source-strip").innerHTML = sources.map((source) => `
    <div class="source-chip ${escapeHtml(source.state)}">
      <strong>${escapeHtml(source.name)}</strong>
      <span>${escapeHtml(source.state)} · ${escapeHtml(source.freshness)}</span>
    </div>
  `).join("");
};

const renderToday = (today = {}) => {
  byId("today-date").textContent = today.date_label || "";
  const event = today.next_event || {};
  byId("next-event").innerHTML = `
    <span class="event-time">Next event · ${escapeHtml(event.time || "No time")}</span>
    <div class="event-title">${escapeHtml(event.title || "No upcoming event")}</div>
    <div class="event-location">${escapeHtml(event.location || "")}</div>
  `;

  byId("commitment-list").innerHTML = (today.commitments || []).map((item) => `
    <div class="list-item">
      <div class="list-item-header">
        <span class="item-title">${escapeHtml(item.title)}</span>
        <span class="badge">${escapeHtml(item.state)}</span>
      </div>
      <p class="item-meta">${escapeHtml(item.source)}</p>
    </div>
  `).join("") || '<div class="list-item">No commitments loaded.</div>';
};

const renderFlow = (flow = {}) => {
  const now = flow.now || {};
  byId("now-card").innerHTML = `
    <span class="now-label">${escapeHtml(now.status || "Now")}</span>
    <div class="now-title">${escapeHtml(now.title || "No active Now card")}</div>
    <div class="now-lane">${escapeHtml(now.lane || "")}</div>
  `;

  byId("next-list").innerHTML = (flow.next || []).map((item) => `
    <div class="list-item">
      <div class="item-title">${escapeHtml(item.title)}</div>
      <p class="item-meta">${escapeHtml(item.lane)}</p>
    </div>
  `).join("") || '<div class="list-item">No Next cards loaded.</div>';

  byId("waiting-list").innerHTML = (flow.waiting || []).map((item) => `
    <div class="list-item">
      <div class="item-title">${escapeHtml(item.title)}</div>
      <p class="item-meta">${escapeHtml(item.reason)}</p>
    </div>
  `).join("") || '<div class="list-item">Nothing waiting.</div>';
};

const renderAttention = (attention = {}) => {
  byId("gmail-signals").innerHTML = (attention.gmail || []).map((signal) => `
    <div class="signal-card">
      <span class="signal-number">${escapeHtml(signal.count)}</span>
      <div class="signal-label">${escapeHtml(signal.label)}</div>
      <p class="signal-detail">${escapeHtml(signal.detail)}</p>
    </div>
  `).join("") || '<div class="signal-card">No attention signals loaded.</div>';

  byId("drive-list").innerHTML = (attention.drive || []).map((file) => `
    <div class="list-item">
      <div class="list-item-header">
        <span class="item-title">${escapeHtml(file.title)}</span>
        <span class="badge">${escapeHtml(file.status)}</span>
      </div>
      <p class="item-meta">${escapeHtml(file.kind)}</p>
    </div>
  `).join("") || '<div class="list-item">No Drive shortcuts loaded.</div>';
};

const compactList = (items = [], emptyMessage = "Nothing loaded.") => items.map((item) => `
  <div class="list-item">
    <div class="item-title">${escapeHtml(item.title)}</div>
    <p class="item-meta">${escapeHtml(item.detail)}</p>
  </div>
`).join("") || `<div class="list-item">${escapeHtml(emptyMessage)}</div>`;

const renderGitHub = (github = {}) => {
  const advisories = github.open_advisories || [];
  const openLoops = github.open_loops || [];
  const recentActivity = github.recent_activity || [];

  byId("github-repo-meta").textContent = github.repository
    ? `${github.repository} · ${github.head || "unknown"}`
    : "Sample placeholder";

  const facts = [
    {label: "Branch", value: github.branch || "Not connected"},
    {label: "Working tree", value: github.working_tree || "Unknown"},
    {label: "Open advisories", value: advisories.length},
    {label: "Priority loops", value: openLoops.length},
  ];

  byId("github-facts").innerHTML = facts.map((fact) => `
    <div class="github-fact">
      <span>${escapeHtml(fact.label)}</span>
      <strong>${escapeHtml(fact.value)}</strong>
    </div>
  `).join("");

  byId("github-advisories").innerHTML = compactList(
    advisories,
    "No open advisories. The routing board is clear."
  );
  byId("github-open-loops").innerHTML = compactList(
    openLoops,
    "No priority open loops found."
  );
  byId("github-activity").innerHTML = compactList(
    recentActivity,
    "No recent durable commits found."
  );
};

const renderNotebooks = (notebooks = []) => {
  byId("notebook-list").innerHTML = notebooks.map((note) => `
    <article class="notebook-item">
      <div class="notebook-header">
        <div>
          <div class="notebook-department">${escapeHtml(note.department)}</div>
          <div class="notebook-title">${escapeHtml(note.title)}</div>
        </div>
        <div class="notebook-date">${escapeHtml(note.date)}</div>
      </div>
      <p class="notebook-summary">${escapeHtml(note.summary)}</p>
      <span class="badge">${escapeHtml(note.status)}</span>
    </article>
  `).join("") || '<div class="notebook-item">No recent notebook activity loaded.</div>';
};

const copyPrompt = async (prompt, label) => {
  try {
    await navigator.clipboard.writeText(prompt);
    showToast(`Copied: ${label}`);
  } catch (error) {
    console.error(error);
    showToast("Clipboard access failed. Select and copy the prompt manually.");
  }
};

const renderCommands = (commands = []) => {
  const container = byId("command-list");
  container.innerHTML = commands.map((command, index) => `
    <article class="command-item">
      <div class="command-header">
        <div class="command-title">${escapeHtml(command.label)}</div>
        <button class="copy-button" type="button" data-command-index="${index}">Copy</button>
      </div>
      <div class="command-preview">${escapeHtml(command.prompt)}</div>
    </article>
  `).join("") || '<div class="command-item">No commands loaded.</div>';

  container.querySelectorAll("[data-command-index]").forEach((button) => {
    const index = Number(button.dataset.commandIndex);
    const command = commands[index];
    button.addEventListener("click", () => copyPrompt(command.prompt, command.label));
  });
};

const renderDashboard = (data) => {
  const meta = data.meta || {};
  byId("dashboard-title").textContent = meta.title || "LifeOS Dashboard";
  byId("dashboard-subtitle").textContent = meta.subtitle || "Current LifeOS state";
  byId("mode-badge").textContent = `${meta.mode || "unknown"} mode`;
  byId("snapshot-state").textContent = `Snapshot: ${meta.status || "unknown"}`;

  const servedAt = meta.served_at ? new Date(meta.served_at) : new Date();
  byId("last-refreshed").textContent = `Refreshed ${servedAt.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  })}`;

  renderSources(data.sources);
  renderToday(data.today);
  renderFlow(data.flow);
  renderAttention(data.attention);
  renderGitHub(data.github);
  renderNotebooks(data.notebooks);
  renderCommands(data.commands);
};

const showLoadError = (error) => {
  console.error(error);
  byId("dashboard-subtitle").textContent = "The dashboard could not load its current snapshot.";
  byId("source-strip").innerHTML = `
    <div class="error-message">
      ${escapeHtml(error.message || "Unknown dashboard error")}
    </div>
  `;
  byId("snapshot-state").textContent = "Snapshot unavailable";
};

const loadDashboard = async () => {
  const button = byId("refresh-button");
  button.disabled = true;
  button.textContent = "Refreshing...";

  try {
    const response = await fetch("/api/dashboard", {cache: "no-store"});
    if (!response.ok) {
      throw new Error(`Dashboard API returned ${response.status}.`);
    }
    renderDashboard(await response.json());
  } catch (error) {
    showLoadError(error);
  } finally {
    button.disabled = false;
    button.textContent = "Refresh view";
  }
};

byId("refresh-button").addEventListener("click", loadDashboard);
loadDashboard();
