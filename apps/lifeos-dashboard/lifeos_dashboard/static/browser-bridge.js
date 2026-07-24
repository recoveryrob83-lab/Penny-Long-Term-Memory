const browserBridgeUi = {
  button: document.getElementById("wo-reconnect-browser"),
  state: document.getElementById("wo-browser-state"),
  detail: document.getElementById("wo-browser-detail"),
  refresh: document.getElementById("wo-refresh"),
};

if (browserBridgeUi.button) {
  let bridgeBusy = false;
  let lastOperations = null;

  function renderBridgeControl(data) {
    lastOperations = data;
    const available = Boolean(data?.browser?.available);
    const blocked = Boolean(data?.running || bridgeBusy);
    browserBridgeUi.button.disabled = available || blocked;
    browserBridgeUi.button.textContent = bridgeBusy
      ? "Starting Edge..."
      : available
        ? "Bridge ready"
        : "Reconnect bridge";
    browserBridgeUi.button.title = available
      ? "The loopback CDP bridge is already available."
      : blocked
        ? "Another local automation action is currently running."
        : "Launch the dedicated Edge CDP profile and verify the loopback bridge.";
  }

  async function loadBridgeState({quiet = false} = {}) {
    if (!quiet) browserBridgeUi.button.disabled = true;
    try {
      const response = await fetch("/api/worker-operations", {cache: "no-store"});
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || `Worker Operations returned ${response.status}.`);
      }
      renderBridgeControl(data);
    } catch (error) {
      browserBridgeUi.button.disabled = true;
      browserBridgeUi.button.textContent = "Bridge unavailable";
      browserBridgeUi.detail.textContent = error.message;
    }
  }

  browserBridgeUi.button.addEventListener("click", async () => {
    if (bridgeBusy || lastOperations?.browser?.available || lastOperations?.running) return;
    bridgeBusy = true;
    renderBridgeControl(lastOperations || {});
    browserBridgeUi.state.textContent = "Starting";
    browserBridgeUi.state.className = "worker-health-warn";
    browserBridgeUi.detail.textContent = "Launching the dedicated Edge profile and verifying loopback CDP...";
    try {
      const response = await fetch("/api/worker-operations/browser/reconnect", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({confirm_launch: true, timeout_seconds: 20}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Browser bridge reconnect failed.");
      renderBridgeControl(data.operations || {});
      browserBridgeUi.state.textContent = "Ready";
      browserBridgeUi.state.className = "worker-health-good";
      browserBridgeUi.detail.textContent = data.reason || "Browser bridge verified.";
      browserBridgeUi.refresh?.click();
    } catch (error) {
      browserBridgeUi.state.textContent = "Offline";
      browserBridgeUi.state.className = "worker-health-bad";
      browserBridgeUi.detail.textContent = error.message;
      await loadBridgeState({quiet: true});
    } finally {
      bridgeBusy = false;
      renderBridgeControl(lastOperations || {});
    }
  });

  loadBridgeState();
  window.setInterval(() => {
    if (!bridgeBusy && !document.hidden) loadBridgeState({quiet: true});
  }, 5000);
}
