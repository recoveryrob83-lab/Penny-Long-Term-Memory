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

const workerRegistrationUi = {
  panel: document.getElementById("wo-worker-registration"),
  profile: document.getElementById("wo-registration-profile"),
  confirm: document.getElementById("wo-confirm-registration"),
  register: document.getElementById("wo-register-worker"),
  message: document.getElementById("wo-registration-message"),
};

if (workerRouteUi.panel && workerRegistrationUi.panel) {
  let routeOperations = null;
  let registrationStatus = null;
  let routeBusy = false;
  let registrationBusy = false;
  let selectedWorkerId = "";
  let selectedProfilePath = "";

  const routeEscape = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const currentWorker = () => (routeOperations?.workers || []).find(
    (item) => item.worker_id === selectedWorkerId,
  );

  const currentProfile = () => (registrationStatus?.candidates || []).find(
    (item) => item.profile_path === selectedProfilePath,
  );

  function setRouteMessage(message, tone = "neutral") {
    workerRouteUi.message.textContent = message;
    workerRouteUi.message.dataset.tone = tone;
  }

  function setRegistrationMessage(message, tone = "neutral") {
    workerRegistrationUi.message.textContent = message;
    workerRegistrationUi.message.dataset.tone = tone;
  }

  function updateRouteAvailability() {
    const worker = currentWorker();
    const browserReady = Boolean(routeOperations?.browser?.available);
    const paused = Boolean(routeOperations?.paused);
    const blocked = Boolean(routeOperations?.running || routeBusy || registrationBusy);
    workerRouteUi.capture.disabled = (
      !worker
      || !browserReady
      || !paused
      || blocked
      || !workerRouteUi.confirm.checked
    );
  }

  function updateRegistrationAvailability() {
    const profile = currentProfile();
    const paused = Boolean(registrationStatus?.paused);
    const blocked = Boolean(
      registrationStatus?.running || registrationBusy || routeBusy
    );
    workerRegistrationUi.register.disabled = (
      !profile
      || !paused
      || blocked
      || !workerRegistrationUi.confirm.checked
    );
  }

  function renderRegistration(data) {
    registrationStatus = data;
    const candidates = data.candidates || [];
    if (!candidates.some((item) => item.profile_path === selectedProfilePath)) {
      selectedProfilePath = candidates[0]?.profile_path || "";
    }
    workerRegistrationUi.profile.innerHTML = candidates.length
      ? candidates.map((item) => (
        `<option value="${routeEscape(item.profile_path)}">${routeEscape(item.chat_title)} · ${routeEscape(item.worker_id)}</option>`
      )).join("")
      : '<option value="">No canonical unregistered profiles</option>';
    workerRegistrationUi.profile.value = selectedProfilePath;

    if (!candidates.length && (data.errors || []).length) {
      setRegistrationMessage(
        `Profile discovery held: ${data.errors[0].reason}`,
        "bad",
      );
    } else if (!candidates.length) {
      setRegistrationMessage("Every canonical profile is already registered.", "good");
    } else if (!data.paused) {
      setRegistrationMessage(
        "Pause automation before registering the selected canonical identity.",
        "warn",
      );
    } else {
      setRegistrationMessage(
        "Ready to create one route-less registry row at revision 0.",
        "neutral",
      );
    }
    updateRegistrationAvailability();
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

  async function loadRegistration({quiet = false} = {}) {
    if (!quiet) workerRegistrationUi.register.disabled = true;
    try {
      const response = await fetch(
        "/api/worker-operations/registration",
        {cache: "no-store"},
      );
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || `Worker registration returned ${response.status}.`);
      renderRegistration(data);
    } catch (error) {
      setRegistrationMessage(error.message, "bad");
    } finally {
      updateRegistrationAvailability();
    }
  }

  workerRegistrationUi.profile.addEventListener("change", () => {
    selectedProfilePath = workerRegistrationUi.profile.value;
    workerRegistrationUi.confirm.checked = false;
    updateRegistrationAvailability();
  });

  workerRegistrationUi.confirm.addEventListener(
    "change",
    updateRegistrationAvailability,
  );

  workerRegistrationUi.register.addEventListener("click", async () => {
    const profile = currentProfile();
    if (!profile || !workerRegistrationUi.confirm.checked) return;
    registrationBusy = true;
    updateRegistrationAvailability();
    updateRouteAvailability();
    workerRegistrationUi.register.textContent = "Registering Worker...";
    setRegistrationMessage(
      `Registering ${profile.chat_title} from ${profile.profile_path}.`,
      "warn",
    );
    try {
      const response = await fetch("/api/worker-operations/registration", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          profile_path: profile.profile_path,
          confirm_registration: true,
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Worker registration failed.");
      selectedWorkerId = data.worker?.worker_id || selectedWorkerId;
      workerRegistrationUi.confirm.checked = false;
      renderRegistration(data.registration || registrationStatus || {});
      renderRouteManagement(data.operations || routeOperations || {});
      setRegistrationMessage(
        `${data.message} Registration created no route and no activation authority.`,
        data.changed ? "good" : "neutral",
      );
      setRouteMessage(
        `Select ${data.worker?.chat_title || "the new Worker"}, keep its exact chat open, and capture the route while automation remains paused.`,
        "warn",
      );
      document.getElementById("wo-refresh")?.click();
    } catch (error) {
      setRegistrationMessage(error.message, "bad");
      await Promise.all([
        loadRegistration({quiet: true}),
        loadRouteOperations({quiet: true}),
      ]);
    } finally {
      registrationBusy = false;
      workerRegistrationUi.register.textContent = "Register approved Worker";
      updateRegistrationAvailability();
      updateRouteAvailability();
    }
  });

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
    updateRegistrationAvailability();
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
          ? `${data.message} Resume automation, then run the zero-authority courier test supported for that Worker.`
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
      updateRegistrationAvailability();
    }
  });

  document.getElementById("wo-pause")?.addEventListener("click", () => {
    window.setTimeout(() => {
      loadRouteOperations({quiet: true});
      loadRegistration({quiet: true});
    }, 350);
  });
  document.getElementById("wo-refresh")?.addEventListener("click", () => {
    loadRegistration({quiet: true});
  });
  document.getElementById("wo-self-test")?.addEventListener("click", () => {
    window.setTimeout(() => loadRouteOperations({quiet: true}), 1200);
  });

  loadRouteOperations();
  loadRegistration();
  window.setInterval(() => {
    if (!routeBusy && !registrationBusy && !document.hidden) {
      loadRouteOperations({quiet: true});
      loadRegistration({quiet: true});
    }
  }, 8000);
}
