(() => {
  "use strict";

  const ui = {
    state: document.getElementById("state"),
    summary: document.getElementById("summary"),
    warning: document.getElementById("warning"),
    enabled: document.getElementById("enabled"),
    keepTurns: document.getElementById("keep-turns"),
    autoTrim: document.getElementById("auto-trim"),
    visibleTurns: document.getElementById("visible-turns"),
    trimmedTurns: document.getElementById("trimmed-turns"),
    trimmedElements: document.getElementById("trimmed-elements"),
    pinnedTurns: document.getElementById("pinned-turns"),
    trimNow: document.getElementById("trim-now"),
    restore: document.getElementById("restore"),
    message: document.getElementById("message"),
  };

  let activeTabId = null;
  let status = null;
  let busy = false;

  function tabsQuery(query) {
    return new Promise((resolve) => chrome.tabs.query(query, resolve));
  }

  function sendMessage(message) {
    return new Promise((resolve, reject) => {
      chrome.tabs.sendMessage(activeTabId, message, (response) => {
        const error = chrome.runtime.lastError;
        if (error) reject(new Error(error.message));
        else resolve(response);
      });
    });
  }

  function setMessage(message, tone = "") {
    ui.message.textContent = message;
    ui.message.className = `message ${tone}`.trim();
  }

  function setBusy(value) {
    busy = value;
    render();
  }

  function render() {
    const supported = Boolean(status?.supportedConversation);
    const protectedWorker = Boolean(status?.workerProtected);
    const enabled = Boolean(status?.config?.enabled);
    const locked = busy || !supported || protectedWorker;

    ui.state.textContent = protectedWorker
      ? "Protected"
      : !supported
        ? "Unavailable"
        : enabled
          ? "Active"
          : "Off";
    ui.state.className = `badge ${protectedWorker ? "warn" : supported ? "good" : "bad"}`;
    ui.summary.textContent = protectedWorker
      ? "This Worker conversation is protected because LifeOS transport counts rendered turns."
      : supported
        ? "Settings apply only to this exact saved conversation."
        : "Open a saved ChatGPT conversation, then reopen this extension.";

    ui.warning.hidden = !protectedWorker;
    ui.warning.textContent = protectedWorker
      ? "DOM trimming is intentionally blocked here. Enable it only in ordinary human conversations."
      : "";

    ui.enabled.checked = enabled;
    ui.enabled.disabled = locked;
    ui.keepTurns.value = String(status?.config?.keepTurns || 40);
    ui.keepTurns.disabled = busy || !supported || protectedWorker;
    ui.autoTrim.checked = status?.config?.autoTrim !== false;
    ui.autoTrim.disabled = busy || !supported || protectedWorker;
    ui.trimNow.disabled = locked || !enabled || status?.generating;
    ui.restore.disabled = busy || !supported || (!enabled && !(status?.stats?.trimmedTurns > 0));

    ui.visibleTurns.textContent = String(status?.stats?.visibleTurns || 0);
    ui.trimmedTurns.textContent = String(status?.stats?.trimmedTurns || 0);
    ui.trimmedElements.textContent = Number(status?.stats?.trimmedElements || 0).toLocaleString();
    ui.pinnedTurns.textContent = String(status?.config?.pinnedTurnIds?.length || 0);
  }

  async function refreshStatus() {
    const tabs = await tabsQuery({active: true, currentWindow: true});
    activeTabId = tabs[0]?.id;
    if (!activeTabId) throw new Error("No active Edge tab was found.");
    const response = await sendMessage({type: "GET_STATUS"});
    if (!response?.ok) throw new Error(response?.error || "ChatGPT DOM Window is unavailable on this page.");
    status = response;
    render();
  }

  async function setConfig(patch) {
    setBusy(true);
    try {
      const response = await sendMessage({type: "SET_CONFIG", config: patch});
      if (!response?.ok) throw new Error(response?.error || "Could not save this conversation's settings.");
      status = response;
      setMessage("Conversation settings saved.", "good");
    } catch (error) {
      setMessage(error.message, "bad");
    } finally {
      setBusy(false);
    }
  }

  ui.enabled.addEventListener("change", () => setConfig({enabled: ui.enabled.checked}));
  ui.keepTurns.addEventListener("change", () => setConfig({keepTurns: Number(ui.keepTurns.value)}));
  ui.autoTrim.addEventListener("change", () => setConfig({autoTrim: ui.autoTrim.checked}));

  ui.trimNow.addEventListener("click", async () => {
    setBusy(true);
    setMessage("Trimming older rendered turns…");
    try {
      const response = await sendMessage({type: "TRIM_NOW"});
      if (!response?.ok) throw new Error(response?.error || "Trim failed.");
      status = response;
      const removed = response.stats?.lastTrimmedTurns || 0;
      setMessage(
        removed ? `Removed ${removed} older rendered turns.` : "Nothing needed trimming.",
        "good",
      );
    } catch (error) {
      setMessage(error.message, "bad");
    } finally {
      setBusy(false);
    }
  });

  ui.restore.addEventListener("click", async () => {
    setBusy(true);
    setMessage("Reloading the full authoritative conversation…");
    try {
      const response = await sendMessage({type: "RESTORE_FULL"});
      if (!response?.ok) throw new Error(response?.error || "Restore failed.");
      window.close();
    } catch (error) {
      setMessage(error.message, "bad");
      setBusy(false);
    }
  });

  refreshStatus().catch((error) => {
    status = null;
    ui.state.textContent = "Unavailable";
    ui.state.className = "badge bad";
    ui.summary.textContent = "Open chatgpt.com in a saved conversation, then reopen this extension.";
    setMessage(error.message, "bad");
    render();
  });
})();
