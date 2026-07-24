const workerRouteUi = {
  panel: document.getElementById("wo-route-management"),
  worker: document.getElementById("wo-route-worker"),
  revision: document.getElementById("wo-route-revision"),
  url: document.getElementById("wo-route-url"),
  state: document.getElementById("wo-route-state"),
  detail: document.getElementById("wo-route-detail"),
  confirm: document.getElementById("wo-confirm-route-capture"),
  capture: document.getElementById("wo-capture-route"),
  message: document.getElementById("wo-route-message"),
};

if (workerRouteUi.panel) {
  let routeOperations = null;
  let routeBusy = false;
  let selectedWorkerId = "";

  const routeEscape = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const currentWorker = () => (routeOperations?.workers || []).find(
    (item) => item.worker_id === selectedWorkerId,
  );

  function setRouteMessage(message, tone = "neutral") {
    workerRouteUi.message.textContent = message;
    workerRouteUi.message.dataset.tone = tone;
  }

  function updateRouteAvailability() {
    const worker = currentWorker();
    const browserReady = Boolean(routeOperations?.browser?.available);
    const paused = Boolean(routeOperations?.paused);
    const blocked = Boolean(routeOperations?.running || routeBusy);
    workerRouteUi.capture.disabled = (
      !worker
      || !browserReady
      || !paused
      || blocked
      || !workerRouteUi.confirm.checked
    );
  }

  function renderRouteManagement(data) {
    routeOperations = data;
    const workers = data.workers || [];
    if (!workers.some((item) => item.worker_id === selectedWorkerId)) {
      selectedWorkerId = workers[0]?.worker_id || "";
    }
    workerRouteUi.worker.innerHTML = workers.length
      ? workers.map((item) => (
        `<option value="${routeEscape(item.worker_id)}">${routeEscape(item.chat_title)} · ${routeEscape(item.worker_id)}</option>`
      )).join("")
      : '<option value="">No registered Workers</option>';
    workerRouteUi.worker.value = selectedWorkerId;

    const worker = currentWorker();
    const route = worker?.route || {};
    workerRouteUi.revision.textContent = worker
      ? `Revision ${worker.route_revision || 0}`
      : "No route";
    workerRouteUi.state.textContent = route.availability || "unknown";
    workerRouteUi.state.className = `worker-badge ${[
      "available",
    ].includes(String(route.availability || "").toLowerCase())
      ? "worker-badge-good"
      : ["unavailable"].includes(String(route.availability || "").toLowerCase())
        ? "worker-badge-bad"
        : "worker-badge-warn"}`;
    workerRouteUi.url.innerHTML = worker?.conversation_url
      ? `<code>${routeEscape(worker.conversation_url)}</code>`
      : "No exact conversation URL is registered.";

    const guidance = [];
    guidance.push(data.paused
      ? "Automation is paused for a guarded route write."
      : "Pause automation before capturing a different route.");
    guidance.push(data.browser?.available
      ? "Browser bridge is ready. Keep exactly one ChatGPT conversation tab open."
      : "Browser bridge is offline.");
    if (route.pause_reason) guidance.push(route.pause_reason);
    workerRouteUi.detail.textContent = guidance.join(" ");
    updateRouteAvailability();
  }

  async function loadRouteOperations({quiet = false} = {}) {
    if (!quiet) workerRouteUi.capture.disabled = true;
    try {
      const response = await fetch("/api/worker-operations", {cache: "no-store"});
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || `Worker Operations returned ${response.status}.`);
      renderRouteManagement(data);
    } catch (error) {
      setRouteMessage(error.message, "bad");
    } finally {
      updateRouteAvailability();
    }
  }

  workerRouteUi.worker.addEventListener("change", () => {
    selectedWorkerId = workerRouteUi.worker.value;
    workerRouteUi.confirm.checked = false;
    renderRouteManagement(routeOperations || {});
  });

  workerRouteUi.confirm.addEventListener("change", updateRouteAvailability);

  workerRouteUi.capture.addEventListener("click", async () => {
    const worker = currentWorker();
    if (!worker || !workerRouteUi.confirm.checked) return;
    routeBusy = true;
    updateRouteAvailability();
    workerRouteUi.capture.textContent = "Capturing route...";
    setRouteMessage(
      `Capturing the sole open ChatGPT conversation for ${worker.chat_title}.`,
      "warn",
    );
    try {
      const response = await fetch("/api/worker-operations/routes/capture", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          worker_id: worker.worker_id,
          expected_route_revision: Number(worker.route_revision || 0),
          confirm_capture: true,
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Worker route capture failed.");
      workerRouteUi.confirm.checked = false;
      renderRouteManagement(data.operations || routeOperations || {});
      setRouteMessage(
        data.changed
          ? `${data.message} Resume automation, then run the zero-authority courier test.`
          : data.message,
        data.changed ? "warn" : "good",
      );
      document.getElementById("wo-refresh")?.click();
    } catch (error) {
      setRouteMessage(error.message, "bad");
      await loadRouteOperations({quiet: true});
    } finally {
      routeBusy = false;
      workerRouteUi.capture.textContent = "Capture active chat as route";
      updateRouteAvailability();
    }
  });

  document.getElementById("wo-pause")?.addEventListener("click", () => {
    window.setTimeout(() => loadRouteOperations({quiet: true}), 350);
  });
  document.getElementById("wo-self-test")?.addEventListener("click", () => {
    window.setTimeout(() => loadRouteOperations({quiet: true}), 1200);
  });

  loadRouteOperations();
  window.setInterval(() => {
    if (!routeBusy && !document.hidden) loadRouteOperations({quiet: true});
  }, 8000);
}
