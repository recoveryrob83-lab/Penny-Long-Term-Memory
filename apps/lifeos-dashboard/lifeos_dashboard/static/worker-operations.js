const workerOps = {
  status: document.getElementById("wo-status"),
  refresh: document.getElementById("wo-refresh"),
  browserState: document.getElementById("wo-browser-state"),
  browserDetail: document.getElementById("wo-browser-detail"),
  gateState: document.getElementById("wo-gate-state"),
  advisoryCount: document.getElementById("wo-advisory-count"),
  reviewCount: document.getElementById("wo-review-count"),
  advisorySelect: document.getElementById("wo-advisory-select"),
  advisoryDetail: document.getElementById("wo-advisory-detail"),
  selectedPriority: document.getElementById("wo-selected-priority"),
  confirmSend: document.getElementById("wo-confirm-send"),
  confirmSelfTest: document.getElementById("wo-confirm-self-test"),
  run: document.getElementById("wo-run"),
  selfTest: document.getElementById("wo-self-test"),
  pause: document.getElementById("wo-pause"),
  runState: document.getElementById("wo-run-state"),
  legacyDetail: document.getElementById("wo-legacy-detail"),
  workerCount: document.getElementById("wo-worker-count"),
  workers: document.getElementById("wo-workers"),
  reviewMeta: document.getElementById("wo-review-meta"),
  reviews: document.getElementById("wo-reviews"),
  historyCount: document.getElementById("wo-history-count"),
  history: document.getElementById("wo-history"),
};

if (workerOps.status) {
  let workerOpsData = null;
  let selectedAdvisoryId = "";
  let workerOpsBusy = false;
  const openHistoryRunIds = new Set();

  const woEscape = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const woDate = (timestamp) => {
    if (!timestamp) return "Unknown time";
    return new Date(Number(timestamp) * 1000).toLocaleString();
  };

  const woBadgeClass = (value) => {
    const clean = String(value || "unknown").toLowerCase();
    if (["succeeded", "verified", "available", "implement", "ready", "dispatch_submitted"].includes(clean)) {
      return "worker-badge-good";
    }
    if (["failed", "rejected", "unavailable", "report_and_hold"].includes(clean)) {
      return "worker-badge-bad";
    }
    if (["pending", "running", "ambiguous", "elevate_for_approval", "result_pending"].includes(clean)) {
      return "worker-badge-warn";
    }
    return "worker-badge-neutral";
  };

  const selectedAdvisory = () => (workerOpsData?.advisories || []).find(
    (item) => item.advisory_id === selectedAdvisoryId,
  );

  function setRunMessage(message, tone = "neutral") {
    workerOps.runState.textContent = message;
    workerOps.runState.dataset.tone = tone;
  }

  function renderHealth(data) {
    const browser = data.browser || {};
    workerOps.browserState.textContent = browser.available ? "Ready" : "Offline";
    workerOps.browserState.className = browser.available ? "worker-health-good" : "worker-health-bad";
    workerOps.browserDetail.textContent = browser.available
      ? browser.browser || "CDP available"
      : browser.reason || "CDP unavailable";

    const gateLabel = data.paused ? "Paused" : data.running ? "Running" : "Ready";
    workerOps.gateState.textContent = gateLabel;
    workerOps.gateState.className = data.paused
      ? "worker-health-bad"
      : data.running
        ? "worker-health-warn"
        : "worker-health-good";
    workerOps.status.textContent = gateLabel;
    workerOps.status.className = `mode-badge ${data.paused ? "wo-paused" : data.running ? "wo-running" : "wo-ready"}`;
    workerOps.pause.textContent = data.paused ? "Resume automation" : "Pause automation";
    workerOps.advisoryCount.textContent = String((data.advisories || []).length);
    workerOps.reviewCount.textContent = String(Number(data.verification?.summary?.pending || 0));
  }

  function renderAdvisories(data) {
    const advisories = data.advisories || [];
    if (!advisories.some((item) => item.advisory_id === selectedAdvisoryId)) {
      selectedAdvisoryId = advisories[0]?.advisory_id || "";
    }
    workerOps.advisorySelect.innerHTML = advisories.length
      ? advisories.map((item) => (
        `<option value="${woEscape(item.advisory_id)}">${woEscape(item.advisory_id)} · ${woEscape(item.title || item.task_class)}</option>`
      )).join("")
      : '<option value="">No execution-ready Worker advisories</option>';
    workerOps.advisorySelect.value = selectedAdvisoryId;

    const advisory = selectedAdvisory();
    if (!advisory) {
      workerOps.selectedPriority.textContent = "No selection";
      workerOps.advisoryDetail.innerHTML = `<p>${woEscape(data.advisory_error || "No execution-ready Worker advisory is currently indexed.")}</p>`;
      return;
    }
    workerOps.selectedPriority.textContent = advisory.priority || "NORMAL";
    workerOps.advisoryDetail.innerHTML = `
      <div class="worker-advisory-title"><strong>${woEscape(advisory.title || advisory.advisory_id)}</strong><span class="worker-pill">Revision ${woEscape(advisory.revision)}</span></div>
      <dl class="worker-advisory-grid">
        <div><dt>Worker</dt><dd>${woEscape(advisory.worker_id)}</dd></div>
        <div><dt>Owner</dt><dd>${woEscape(advisory.target_department)}</dd></div>
        <div><dt>Task class</dt><dd>${woEscape(advisory.task_class)}</dd></div>
        <div><dt>Authority</dt><dd>${woEscape(advisory.authorization_class)}</dd></div>
        <div><dt>Procedure</dt><dd>${woEscape(advisory.procedure_id)} v${woEscape(advisory.procedure_version)}</dd></div>
        <div><dt>Verification</dt><dd>${woEscape(advisory.verification_mode)}</dd></div>
      </dl>
      <p class="worker-source-note">Source: ${woEscape(advisory.board_path)} · Run: ${woEscape(advisory.run_id)}</p>`;
  }

  function renderWorkers(data) {
    const workers = data.workers || [];
    workerOps.workerCount.textContent = `${workers.length} registered`;
    workerOps.workers.innerHTML = workers.map((item) => {
      const route = item.route || {};
      return `<article class="worker-card">
        <div class="worker-card-header"><strong>${woEscape(item.chat_title)}</strong><span class="worker-badge ${woBadgeClass(route.availability)}">${woEscape(route.availability || "unknown")}</span></div>
        <p>${woEscape(item.worker_id)} · ${woEscape(item.owning_department)}</p>
        <p class="worker-card-meta">Profile v${woEscape(item.profile_version)} · deployment ${woEscape(item.deployment_state)}</p>
        ${route.pause_reason ? `<p class="worker-card-warning">${woEscape(route.pause_reason)}</p>` : ""}
      </article>`;
    }).join("") || '<p class="worker-empty">No registered Workers are visible in the local runtime.</p>';
  }

  function renderReviews(data) {
    const records = (data.verification?.records || []).filter(
      (item) => item.verification_state === "pending" || item.wake_required,
    );
    workerOps.reviewMeta.textContent = `${records.length} need attention`;
    workerOps.reviews.innerHTML = records.map((item) => {
      const canReview = item.controlled_outcome === "IMPLEMENT" && item.verification_state === "pending";
      return `<article class="worker-card worker-review-card" data-run-id="${woEscape(item.run_id)}">
        <div class="worker-card-header"><strong>${woEscape(item.task_id)} · r${woEscape(item.task_revision)}</strong><span class="worker-badge ${woBadgeClass(item.verification_state)}">${woEscape(item.verification_state)}</span></div>
        <p>${woEscape(item.worker_id)} reported ${woEscape(item.controlled_outcome)}</p>
        <p class="worker-card-meta">${woEscape(item.verification_mode)} · ${woEscape(item.wake_reason || item.receiver_reason)}</p>
        ${canReview ? '<label class="worker-review-reason">Review reason<input type="text" data-review-reason placeholder="What evidence did HQ verify?"></label><div class="worker-review-actions"><button type="button" data-review-state="verified">Verify</button><button type="button" data-review-state="rejected">Reject</button></div>' : ""}
      </article>`;
    }).join("") || '<p class="worker-empty">No Worker runs currently require HQ review.</p>';
  }

  function captureOpenHistoryRuns() {
    workerOps.history.querySelectorAll(".worker-history-item[data-run-id] details[open]").forEach((details) => {
      const item = details.closest(".worker-history-item[data-run-id]");
      if (item?.dataset.runId) openHistoryRunIds.add(item.dataset.runId);
    });
  }

  function renderHistory(data) {
    captureOpenHistoryRuns();
    const rows = data.history || [];
    const visibleRunIds = new Set(rows.map((item) => String(item.run_id || "")));
    for (const runId of [...openHistoryRunIds]) {
      if (!visibleRunIds.has(runId)) openHistoryRunIds.delete(runId);
    }
    workerOps.historyCount.textContent = `${rows.length} runs shown`;
    workerOps.history.innerHTML = rows.map((item) => {
      const runId = String(item.run_id || "");
      const dispatch = item.dispatch_state || (item.assistant_turn_id ? "LEGACY_RESPONSE_CAPTURED" : "Not submitted");
      const resultState = item.controlled_outcome || item.worker_reported_outcome || (dispatch === "DISPATCH_SUBMITTED" ? "RESULT_PENDING" : "Not available");
      const detail = item.stdout || item.stderr || item.reason || "No additional run detail recorded.";
      const detailsOpen = openHistoryRunIds.has(runId) ? " open" : "";
      return `<article class="worker-history-item" data-run-id="${woEscape(runId)}">
        <div class="worker-card-header"><strong>${woEscape(item.task_id || item.run_id)}</strong><span class="worker-badge ${woBadgeClass(item.status)}">${woEscape(item.status)}</span></div>
        <div class="worker-history-meta"><span>${woEscape(item.worker_id)}</span><span>r${woEscape(item.task_revision)}</span><span>${woEscape(woDate(item.finished_at))}</span></div>
        <div class="worker-history-outcomes"><span>Dispatch: <b>${woEscape(dispatch)}</b></span><span>Result: <b>${woEscape(resultState)}</b></span></div>
        <details${detailsOpen}><summary>Run evidence</summary><p><b>Run:</b> ${woEscape(item.run_id)}</p><p><b>Wrapper:</b> ${woEscape(item.wrapper_id)}</p><p><b>User turn:</b> ${woEscape(item.user_turn_id || "Not recorded")}</p><p><b>Returned to HQ:</b> ${item.returned_to_source ? "yes" : "not verified"}</p><pre>${woEscape(detail)}</pre></details>
      </article>`;
    }).join("") || '<p class="worker-empty">No Worker execution rows have been recorded.</p>';
  }

  function renderLegacy(data) {
    const legacy = data.legacy || {};
    workerOps.legacyDetail.textContent = (
      `The old prompt-and-schedule UI is retired from view. Its backend remains available for rollback. `
      + `Scheduler running: ${legacy.scheduler_running ? "yes" : "no"}; `
      + `saved prompts: ${legacy.saved_prompts || 0}; scheduled jobs: ${legacy.scheduled_jobs || 0}.`
    );
  }

  function updateRunAvailability() {
    const advisory = selectedAdvisory();
    const browserReady = Boolean(workerOpsData?.browser?.available);
    const blocked = Boolean(workerOpsData?.paused || workerOpsData?.running || workerOpsBusy);
    workerOps.run.disabled = !advisory || !browserReady || blocked || !workerOps.confirmSend.checked;
    workerOps.selfTest.disabled = !browserReady || blocked || !workerOps.confirmSelfTest.checked;
  }

  function renderWorkerOperations(data) {
    workerOpsData = data;
    renderHealth(data);
    renderAdvisories(data);
    renderWorkers(data);
    renderReviews(data);
    renderHistory(data);
    renderLegacy(data);
    updateRunAvailability();
  }

  async function loadWorkerOperations({quiet = false} = {}) {
    if (!quiet) workerOps.refresh.disabled = true;
    try {
      const response = await fetch("/api/worker-operations", {cache: "no-store"});
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || `Worker Operations returned ${response.status}.`);
      renderWorkerOperations(data);
    } catch (error) {
      workerOps.status.textContent = "Unavailable";
      workerOps.status.className = "mode-badge wo-paused";
      setRunMessage(error.message, "bad");
    } finally {
      workerOps.refresh.disabled = false;
    }
  }

  workerOps.advisorySelect.addEventListener("change", () => {
    selectedAdvisoryId = workerOps.advisorySelect.value;
    workerOps.confirmSend.checked = false;
    renderAdvisories(workerOpsData || {});
    updateRunAvailability();
  });
  workerOps.confirmSend.addEventListener("change", updateRunAvailability);
  workerOps.confirmSelfTest.addEventListener("change", updateRunAvailability);
  workerOps.refresh.addEventListener("click", () => loadWorkerOperations());
  workerOps.history.addEventListener("toggle", (event) => {
    const details = event.target.closest("details");
    const item = details?.closest(".worker-history-item[data-run-id]");
    const runId = item?.dataset.runId;
    if (!details || !runId) return;
    if (details.open) openHistoryRunIds.add(runId);
    else openHistoryRunIds.delete(runId);
  }, true);

  workerOps.pause.addEventListener("click", async () => {
    workerOps.pause.disabled = true;
    try {
      const response = await fetch("/api/command-center/pause", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({paused: !Boolean(workerOpsData?.paused)}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Pause control failed.");
      await loadWorkerOperations();
    } catch (error) {
      setRunMessage(error.message, "bad");
    } finally {
      workerOps.pause.disabled = false;
    }
  });

  workerOps.run.addEventListener("click", async () => {
    const advisory = selectedAdvisory();
    if (!advisory || !workerOps.confirmSend.checked) return;
    workerOpsBusy = true;
    updateRunAvailability();
    workerOps.run.textContent = "Dispatching...";
    setRunMessage(`Waking ${advisory.worker_id} for ${advisory.advisory_id} revision ${advisory.revision}. Leave the ChatGPT tab untouched until the courier returns.`, "warn");
    try {
      const response = await fetch("/api/worker-operations/run", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({advisory_id: advisory.advisory_id, confirm_send: true, timeout_seconds: 600}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Worker dispatch failed.");
      const result = data.result || {};
      setRunMessage(result.reason || `Dispatch ${data.run_id} completed.`, result.status === "succeeded" ? "good" : "bad");
      workerOps.confirmSend.checked = false;
      renderWorkerOperations(data.status || await (await fetch("/api/worker-operations")).json());
    } catch (error) {
      setRunMessage(error.message, "bad");
      await loadWorkerOperations({quiet: true});
    } finally {
      workerOpsBusy = false;
      workerOps.run.textContent = "Run selected advisory";
      updateRunAvailability();
    }
  });

  workerOps.selfTest.addEventListener("click", async () => {
    if (!workerOps.confirmSelfTest.checked) return;
    workerOpsBusy = true;
    updateRunAvailability();
    workerOps.selfTest.textContent = "Testing courier...";
    setRunMessage("Sending one zero-authority wake. Leave the ChatGPT tab untouched until the courier returns.", "warn");
    try {
      const response = await fetch("/api/worker-operations/self-test", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({confirm_send: true, timeout_seconds: 300}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Courier self-test failed.");
      const receipt = data.receipt || {};
      const turn = receipt.user_turn_id || "an unnumbered user turn";
      const zeroAuthority = receipt.durable_authority_created === false
        ? "No durable authority was created."
        : "Durable-authority status was not verified.";
      const returned = receipt.returned_to_source ? "Returned to HQ successfully." : "HQ return was not verified.";
      setRunMessage(`Courier self-test succeeded. Wake submitted at ${turn}. ${returned} ${zeroAuthority}`, receipt.returned_to_source ? "good" : "warn");
      workerOps.confirmSelfTest.checked = false;
      renderWorkerOperations(data.operations);
    } catch (error) {
      setRunMessage(error.message, "bad");
      await loadWorkerOperations({quiet: true});
    } finally {
      workerOpsBusy = false;
      workerOps.selfTest.textContent = "Test courier";
      updateRunAvailability();
    }
  });

  workerOps.reviews.addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-review-state]");
    if (!button) return;
    const card = button.closest("[data-run-id]");
    const reasonInput = card?.querySelector("[data-review-reason]");
    const reason = reasonInput?.value.trim() || "";
    if (!reason) {
      reasonInput?.focus();
      return;
    }
    button.disabled = true;
    try {
      const response = await fetch("/api/worker-operations/review", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({run_id: card.dataset.runId, state: button.dataset.reviewState, actor: "Engineering HQ", reason}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "HQ review failed.");
      renderWorkerOperations(data.status);
      setRunMessage(`HQ review recorded for ${card.dataset.runId}.`, "good");
    } catch (error) {
      setRunMessage(error.message, "bad");
      button.disabled = false;
    }
  });

  loadWorkerOperations();
  window.setInterval(() => {
    if (!workerOpsBusy && !document.hidden) loadWorkerOperations({quiet: true});
  }, 8000);
}
