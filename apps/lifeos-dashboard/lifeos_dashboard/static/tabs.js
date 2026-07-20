const ensureAutomationLogsSurface = () => {
  const navigation = document.querySelector(".dashboard-tabs");
  const footer = document.querySelector(".footer");
  if (!navigation || !footer) return;

  if (!navigation.querySelector('[data-tab-target="automation-logs"]')) {
    const button = document.createElement("button");
    button.className = "dashboard-tab";
    button.type = "button";
    button.setAttribute("role", "tab");
    button.setAttribute("aria-selected", "false");
    button.dataset.tabTarget = "automation-logs";
    button.textContent = "Automation Logs";
    navigation.appendChild(button);
  }

  if (!document.querySelector('[data-tab-panel="automation-logs"]')) {
    const panel = document.createElement("section");
    panel.className = "tab-page automation-logs-page";
    panel.dataset.tabPanel = "automation-logs";
    panel.setAttribute("role", "tabpanel");
    panel.hidden = true;
    panel.innerHTML = `
      <main class="dashboard-grid">
        <section class="panel automation-logs-panel" aria-labelledby="automation-logs-heading">
          <div class="section-heading">
            <div>
              <p class="eyebrow">COMPLETE EXECUTION EVIDENCE</p>
              <h2 id="automation-logs-heading">Automation Logs</h2>
            </div>
            <div class="cc-list-meta">
              <span id="automation-log-state" class="mode-badge">Loading</span>
              <span id="automation-log-count" class="panel-meta"></span>
            </div>
          </div>
          <p class="item-meta">Full run metadata, backend event path, stdout, and stderr from the authoritative Command Center execution history. Worker verification and wake routing are derived from the same run rows. Prompt bodies and environment secrets are not copied into diagnostic metadata.</p>
          <div class="automation-verification-summary" aria-label="Worker verification summary">
            <div class="automation-verification-card"><span>Worker outcomes</span><strong id="automation-worker-total">0</strong></div>
            <div class="automation-verification-card"><span>Pending review</span><strong id="automation-worker-pending">0</strong></div>
            <div class="automation-verification-card"><span>Verified</span><strong id="automation-worker-verified">0</strong></div>
            <div class="automation-verification-card"><span>Rejected / held</span><strong id="automation-worker-rejected">0</strong></div>
            <div class="automation-verification-card"><span>Wake required</span><strong id="automation-worker-wakes">0</strong></div>
          </div>
          <div class="automation-log-toolbar" aria-label="Automation log filters">
            <label class="cc-filter-field">Result<select id="automation-log-filter-result"><option value="all">All results</option><option value="succeeded">Succeeded</option><option value="failed">Failed</option><option value="refused">Refused</option></select></label>
            <label class="cc-filter-field">Department<select id="automation-log-filter-destination"><option value="all">All departments</option><option value="hub">LifeOS HQ</option><option value="main">Chief of Staff HQ</option><option value="engineering">Engineering HQ</option><option value="logistics">Life OS Maintenance HQ</option><option value="business">Business HQ</option><option value="office-leaks">Office Leaks HQ</option><option value="finance">Finance HQ</option><option value="wellness">Wellness HQ</option></select></label>
            <label class="cc-filter-field">Trigger<select id="automation-log-filter-trigger"><option value="all">Manual and scheduled</option><option value="manual">Manual</option><option value="scheduled">Scheduled</option><option value="unknown">Legacy / unstructured</option></select></label>
            <label class="cc-filter-field">Worker verification<select id="automation-log-filter-worker-state"><option value="all">All runs</option><option value="not-worker">Non-Worker runs</option><option value="pending">Pending</option><option value="verified">Verified</option><option value="rejected">Rejected / held</option></select></label>
            <label class="cc-filter-field">Wake routing<select id="automation-log-filter-wake"><option value="all">All wake states</option><option value="required">Wake required</option><option value="queued">Routine queue</option><option value="suppressed">Wake suppressed</option></select></label>
            <label class="cc-filter-field">Order<select id="automation-log-filter-sort"><option value="newest">Newest first</option><option value="oldest">Oldest first</option></select></label>
            <label class="cc-filter-field">Search<input id="automation-log-filter-search" type="search" placeholder="Stages, errors, run ID, Worker, outcome..."></label>
            <div class="automation-log-actions">
              <button id="automation-log-refresh" class="primary-button" type="button">Refresh logs</button>
              <button id="automation-log-expand" class="copy-button" type="button">Expand all</button>
            </div>
          </div>
          <div id="automation-log-list" class="automation-log-list" aria-live="polite"></div>
        </section>
      </main>`;
    footer.before(panel);
  }

  if (!document.querySelector('link[href="/static/automation-logs.css"]')) {
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = "/static/automation-logs.css";
    document.head.appendChild(stylesheet);
  }

  if (!document.querySelector('script[src="/static/automation-logs.js"]')) {
    const script = document.createElement("script");
    script.src = "/static/automation-logs.js";
    script.defer = true;
    document.head.appendChild(script);
  }
};

ensureAutomationLogsSurface();

const tabButtons = Array.from(document.querySelectorAll("[data-tab-target]"));
const tabPanels = Array.from(document.querySelectorAll("[data-tab-panel]"));

const activateTab = (target) => {
  tabButtons.forEach((button) => {
    const active = button.dataset.tabTarget === target;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
    button.tabIndex = active ? 0 : -1;
  });

  tabPanels.forEach((panel) => {
    const active = panel.dataset.tabPanel === target;
    panel.hidden = !active;
  });

  window.localStorage.setItem("lifeos-active-tab", target);
};

tabButtons.forEach((button, index) => {
  button.addEventListener("click", () => activateTab(button.dataset.tabTarget));
  button.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight"].includes(event.key)) return;
    event.preventDefault();
    const direction = event.key === "ArrowRight" ? 1 : -1;
    const next = (index + direction + tabButtons.length) % tabButtons.length;
    tabButtons[next].focus();
    activateTab(tabButtons[next].dataset.tabTarget);
  });
});

const remembered = window.localStorage.getItem("lifeos-active-tab");
const initial = tabButtons.some((button) => button.dataset.tabTarget === remembered)
  ? remembered
  : "overview";
activateTab(initial);

const inspectionTuning = document.createElement("script");
inspectionTuning.src = "/static/department-inspection-tuning.js";
inspectionTuning.defer = true;
document.head.appendChild(inspectionTuning);
