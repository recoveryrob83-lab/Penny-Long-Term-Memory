(() => {
  const panel = document.querySelector('[data-tab-panel="automation-logs"]');
  const logPanel = panel?.querySelector(".automation-logs-panel");
  if (!panel || !logPanel) return;

  if (!document.querySelector('link[href="/static/latest-run-report.css"]')) {
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = "/static/latest-run-report.css";
    document.head.appendChild(stylesheet);
  }

  let root = document.getElementById("automation-latest-run");
  if (!root) {
    root = document.createElement("details");
    root.id = "automation-latest-run";
    root.className = "automation-latest-run";
    root.open = true;
    root.innerHTML = `
      <summary>
        <div class="latest-run-heading">
          <span class="latest-run-kicker">CURRENT OR LATEST WORKER EXECUTION</span>
          <strong>Latest Run Report</strong>
          <span id="latest-run-summary">Waiting for Worker execution history.</span>
        </div>
        <span id="latest-run-state" class="latest-run-state" data-tone="neutral">Loading</span>
      </summary>
      <div class="latest-run-body">
        <div id="latest-run-facts" class="latest-run-facts"></div>
        <p id="latest-run-reason" class="latest-run-reason">No run reason is available yet.</p>
        <div class="latest-run-actions">
          <button id="latest-run-filter-logs" class="copy-button" type="button">Filter full logs to this run</button>
        </div>
        <section class="latest-run-section" aria-labelledby="latest-run-lifecycle-heading">
          <div class="latest-run-section-heading">
            <h3 id="latest-run-lifecycle-heading">Durable lifecycle</h3>
            <span>Derived from the authoritative execution row</span>
          </div>
          <div id="latest-run-lifecycle" class="latest-run-timeline"></div>
        </section>
        <section class="latest-run-section" aria-labelledby="latest-run-attempts-heading">
          <div class="latest-run-section-heading">
            <h3 id="latest-run-attempts-heading">Attempt history</h3>
            <span>Meaningful orchestrator events for this run only</span>
          </div>
          <div id="latest-run-attempts" class="latest-run-timeline"></div>
        </section>
      </div>`;
    const verificationSummary = logPanel.querySelector(".automation-verification-summary");
    logPanel.insertBefore(root, verificationSummary || logPanel.firstChild);
  }

  const ui = {
    summary: document.getElementById("latest-run-summary"),
    state: document.getElementById("latest-run-state"),
    facts: document.getElementById("latest-run-facts"),
    reason: document.getElementById("latest-run-reason"),
    lifecycle: document.getElementById("latest-run-lifecycle"),
    attempts: document.getElementById("latest-run-attempts"),
    filter: document.getElementById("latest-run-filter-logs"),
  };

  let requestToken = 0;
  let reportSignature = "";
  let selectedRunId = "";

  const escapeHtml = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const displayTime = (timestamp) => {
    const value = Number(timestamp || 0);
    return value ? new Date(value * 1000).toLocaleString() : "Time unavailable";
  };

  const rowTime = (row) => Math.max(
    ...[
      "rob_validation_ingested_at",
      "hq_review_ingested_at",
      "hq_wake_sent_at",
      "repair_dispatched_at",
      "report_validated_at",
      "report_ingested_at",
      "finished_at",
      "started_at",
    ].map((key) => Number(row?.[key] || 0)),
  );

  const toneFor = (value) => {
    const clean = String(value || "").toUpperCase();
    if (/(FAILED|ERROR|STOPPED|REJECTED)/.test(clean)) return "bad";
    if (/(REPAIR|PENDING|REQUIRED|HOLD|RUNNING|CLAIMED)/.test(clean)) return "warn";
    if (/(SUCCEEDED|VALIDATED|SUBMITTED|VERIFIED|READY|COMPLETED)/.test(clean)) return "good";
    return "neutral";
  };

  const fact = (label, value) => `
    <div class="latest-run-fact">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value || "Not recorded")}</strong>
    </div>`;

  const stage = (label, state, detail, timestamp = null) => ({
    label,
    state: state || "Not recorded",
    detail: detail || "No additional reason was recorded.",
    timestamp,
  });

  function durableStages(row) {
    const stages = [];
    if (row.dispatch_state || row.status) {
      const transport = [
        row.user_turn_id ? `User turn ${row.user_turn_id}` : null,
        row.returned_to_source ? "Returned to source" : null,
      ].filter(Boolean).join(" · ");
      stages.push(stage(
        "Worker dispatch",
        row.dispatch_state || row.status,
        transport || row.reason,
        row.finished_at,
      ));
    }
    if (row.result_state || row.worker_reported_outcome || row.controlled_outcome) {
      stages.push(stage(
        "Worker result",
        row.result_state || row.worker_reported_outcome || row.controlled_outcome,
        row.receiver_reason || row.failure_reason || row.reason,
        row.report_validated_at || row.report_ingested_at,
      ));
    }
    if (row.repair_state || row.repair_dispatch_state) {
      const repairState = [row.repair_state, row.repair_dispatch_state].filter(Boolean).join(" · ");
      stages.push(stage(
        "Report repair",
        repairState,
        row.repair_reason || row.repair_dispatch_reason || row.receiver_reason,
        row.repair_dispatched_at,
      ));
    }
    if (row.hq_wake_state) {
      const wakeEvidence = [
        row.hq_wake_target,
        row.hq_wake_user_turn_id ? `User turn ${row.hq_wake_user_turn_id}` : null,
        row.hq_wake_returned_to_source ? "Returned to source" : null,
      ].filter(Boolean).join(" · ");
      stages.push(stage(
        "Owning-HQ wake",
        row.hq_wake_state,
        wakeEvidence || row.reason,
        row.hq_wake_sent_at,
      ));
    }
    if (row.hq_review_state) {
      stages.push(stage(
        "Owning-HQ review",
        row.hq_review_state,
        row.hq_review_reason,
        row.hq_review_ingested_at,
      ));
    }
    if (row.rob_validation_state || row.requires_rob_validation) {
      stages.push(stage(
        "Rob validation",
        row.rob_validation_state || "REQUIRED",
        row.rob_validation_reason || "Rob validation remains required.",
        row.rob_validation_ingested_at,
      ));
    }
    if (row.hq_review_state || row.rob_validation_state || row.ready_for_consumption != null) {
      stages.push(stage(
        "Consumption readiness",
        row.ready_for_consumption ? "READY" : "HELD",
        row.ready_for_consumption
          ? "The run is ready for its authorized consumer."
          : "The run is not ready for consumption.",
        row.hq_review_ingested_at || row.rob_validation_ingested_at,
      ));
    }
    return stages;
  }

  function renderTimeline(target, items, emptyMessage) {
    target.innerHTML = items.length
      ? items.map((item) => `
        <article class="latest-run-stage" data-tone="${toneFor(item.state)}">
          <div class="latest-run-stage-marker" aria-hidden="true"></div>
          <div class="latest-run-stage-content">
            <div class="latest-run-stage-title">
              <strong>${escapeHtml(item.label)}</strong>
              <span class="latest-run-stage-state" data-tone="${toneFor(item.state)}">${escapeHtml(item.state)}</span>
            </div>
            <p>${escapeHtml(item.detail)}</p>
            ${item.timestamp ? `<time>${escapeHtml(displayTime(item.timestamp))}</time>` : ""}
          </div>
        </article>`).join("")
      : `<div class="latest-run-empty">${escapeHtml(emptyMessage)}</div>`;
  }

  function commandCenterFallback(commandCenter) {
    const history = commandCenter.history || [];
    const records = commandCenter.worker_verification?.records || [];
    return records.map((record) => {
      const execution = history.find((item) => Number(item.id) === Number(record.history_id)) || {};
      return {...execution, ...record};
    });
  }

  function latestRow(commandCenter, workerOperations) {
    const rows = workerOperations.history?.length
      ? workerOperations.history
      : commandCenterFallback(commandCenter);
    const runEvents = (workerOperations.orchestrator?.events || [])
      .filter((event) => String(event.run_id || "").trim())
      .sort((left, right) => Number(right.occurred_at || 0) - Number(left.occurred_at || 0));
    const eventRunId = String(runEvents[0]?.run_id || "");
    if (eventRunId) {
      const eventRow = rows.find((row) => String(row.run_id || "") === eventRunId);
      if (eventRow) return eventRow;
    }
    return [...rows].sort((left, right) => rowTime(right) - rowTime(left))[0] || null;
  }

  function attemptHistory(workerOperations, runId) {
    return (workerOperations.orchestrator?.events || [])
      .filter((event) => String(event.run_id || "") === runId)
      .sort((left, right) => Number(left.occurred_at || 0) - Number(right.occurred_at || 0))
      .map((event) => stage(
        String(event.action || "Orchestrator action").replaceAll("_", " "),
        event.status || "unknown",
        event.detail || "No event reason was recorded.",
        event.occurred_at,
      ));
  }

  function reportReason(row, attempts) {
    return row.hq_review_reason
      || row.rob_validation_reason
      || row.receiver_reason
      || row.failure_reason
      || attempts.at(-1)?.detail
      || row.reason
      || "No run reason is available yet.";
  }

  function render(commandCenter, workerOperations) {
    const row = latestRow(commandCenter, workerOperations);
    if (!row) {
      selectedRunId = "";
      ui.summary.textContent = "No Worker execution has been recorded yet.";
      ui.state.textContent = "No run";
      ui.state.dataset.tone = "neutral";
      ui.facts.innerHTML = "";
      ui.reason.textContent = "The existing Automation Logs remain available below.";
      renderTimeline(ui.lifecycle, [], "No durable lifecycle is available.");
      renderTimeline(ui.attempts, [], "No orchestrator attempts are available.");
      ui.filter.disabled = true;
      return;
    }

    selectedRunId = String(row.run_id || "");
    const attempts = attemptHistory(workerOperations, selectedRunId);
    const lifecycle = durableStages(row);
    const state = row.result_state || row.hq_review_state || row.status || "UNKNOWN";
    const current = /(PENDING|RUNNING|VALIDATED|SUBMITTED|REQUIRED|HOLD)/.test(String(state).toUpperCase());
    const updatedAt = Math.max(rowTime(row), ...attempts.map((item) => Number(item.timestamp || 0)));
    const budget = workerOperations.send_budget || {};

    ui.summary.textContent = `${current ? "Current" : "Latest"} · ${selectedRunId} · updated ${displayTime(updatedAt)}`;
    ui.state.textContent = state;
    ui.state.dataset.tone = toneFor(state);
    ui.facts.innerHTML = [
      fact("Run ID", selectedRunId),
      fact("Worker", row.worker_id),
      fact("Owner", row.owning_department),
      fact("Task", row.task_id || row.advisory_id),
      fact("Result state", row.result_state || row.status),
      fact("HQ review", row.hq_review_state || "Not reached"),
      fact("Send budget", budget.limit ? `${budget.used || 0} / ${budget.limit}` : "Unavailable"),
      fact("Last meaningful update", displayTime(updatedAt)),
    ].join("");
    ui.reason.textContent = reportReason(row, attempts);
    renderTimeline(ui.lifecycle, lifecycle, "No durable lifecycle stages were recorded.");
    renderTimeline(
      ui.attempts,
      attempts,
      "No per-cycle orchestrator events are retained for this run. The durable lifecycle above remains authoritative.",
    );
    ui.filter.disabled = !selectedRunId;
  }

  async function loadLatestRun() {
    const token = ++requestToken;
    const commandResponse = await fetch("/api/command-center", {cache: "no-store"});
    if (!commandResponse.ok) {
      throw new Error(`Command Center returned ${commandResponse.status}.`);
    }
    const commandCenter = await commandResponse.json();
    let workerOperations = {};
    try {
      const workerResponse = await fetch("/api/worker-operations", {cache: "no-store"});
      const payload = await workerResponse.json();
      if (workerResponse.ok) workerOperations = payload;
    } catch (_) {
      workerOperations = {};
    }
    if (token !== requestToken) return;
    const nextSignature = JSON.stringify({
      history: commandCenter.history || [],
      verification: commandCenter.worker_verification || {},
      workerHistory: workerOperations.history || [],
      orchestrator: workerOperations.orchestrator || {},
      sendBudget: workerOperations.send_budget || {},
    });
    if (nextSignature === reportSignature) return;
    reportSignature = nextSignature;
    render(commandCenter, workerOperations);
  }

  ui.filter.addEventListener("click", () => {
    if (!selectedRunId) return;
    const search = document.getElementById("automation-log-filter-search");
    const list = document.getElementById("automation-log-list");
    if (!search) return;
    search.value = selectedRunId;
    search.dispatchEvent(new Event("input", {bubbles: true}));
    list?.scrollIntoView({behavior: "smooth", block: "start"});
  });

  document.getElementById("automation-log-refresh")?.addEventListener("click", () => {
    reportSignature = "";
    loadLatestRun().catch((error) => {
      ui.reason.textContent = error.message;
      ui.state.textContent = "Error";
      ui.state.dataset.tone = "bad";
    });
  });

  loadLatestRun().catch((error) => {
    ui.reason.textContent = error.message;
    ui.state.textContent = "Error";
    ui.state.dataset.tone = "bad";
  });
  setInterval(() => {
    if (!panel.hidden) loadLatestRun().catch(() => {});
  }, 5000);
})();
