const commandCenter = {
  destination: document.getElementById("cc-destination"),
  promptType: document.getElementById("cc-prompt-type"),
  customPrompt: document.getElementById("cc-custom-prompt"),
  mode: document.getElementById("cc-mode"),
  confirmWrap: document.getElementById("cc-confirm-wrap"),
  confirmSend: document.getElementById("cc-confirm-send"),
  runButton: document.getElementById("cc-run"),
  pauseButton: document.getElementById("cc-pause"),
  summary: document.getElementById("cc-summary"),
  status: document.getElementById("cc-status"),
  history: document.getElementById("cc-history"),
};

const ccEscape = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const updateCommandCenterForm = () => {
  const custom = commandCenter.promptType.value === "custom";
  const send = commandCenter.mode.value === "send";
  commandCenter.customPrompt.hidden = !custom;
  commandCenter.confirmWrap.hidden = !send;
  if (!send) commandCenter.confirmSend.checked = false;
  const promptLabel = custom ? "custom prompt" : "canonical boot prompt";
  const action = send ? "send" : "place as a verified draft";
  const label = commandCenter.destination.selectedOptions[0]?.textContent || "destination";
  commandCenter.summary.textContent = `${action[0].toUpperCase()}${action.slice(1)} the ${promptLabel} in ${label}.`;
};

const renderCommandCenter = (data) => {
  commandCenter.status.textContent = data.paused
    ? "Paused"
    : data.running
      ? "Running"
      : "Ready";
  commandCenter.status.className = `mode-badge ${data.paused ? "cc-paused" : data.running ? "cc-running" : "cc-ready"}`;
  commandCenter.pauseButton.textContent = data.paused ? "Resume automation" : "Pause automation";
  commandCenter.runButton.disabled = Boolean(data.paused || data.running);
  const history = data.history || [];
  commandCenter.history.innerHTML = history.map((item) => `
    <div class="cc-history-item">
      <div class="list-item-header">
        <strong>${ccEscape(item.destination)}</strong>
        <span class="badge">${ccEscape(item.status)}</span>
      </div>
      <p class="item-meta">${ccEscape(item.mode)} · ${ccEscape(item.prompt_type)} · ${ccEscape(item.reason)}</p>
    </div>
  `).join("") || '<div class="cc-history-item">No automation runs recorded yet.</div>';
};

const loadCommandCenter = async () => {
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Command Center returned ${response.status}.`);
  renderCommandCenter(await response.json());
};

commandCenter.promptType.addEventListener("change", updateCommandCenterForm);
commandCenter.mode.addEventListener("change", updateCommandCenterForm);
commandCenter.destination.addEventListener("change", updateCommandCenterForm);

commandCenter.pauseButton.addEventListener("click", async () => {
  commandCenter.pauseButton.disabled = true;
  try {
    const current = await (await fetch("/api/command-center", {cache: "no-store"})).json();
    const response = await fetch("/api/command-center/pause", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({paused: !current.paused}),
    });
    if (!response.ok) throw new Error(`Pause control returned ${response.status}.`);
    renderCommandCenter(await response.json());
  } catch (error) {
    commandCenter.summary.textContent = error.message;
  } finally {
    commandCenter.pauseButton.disabled = false;
  }
});

commandCenter.runButton.addEventListener("click", async () => {
  const custom = commandCenter.promptType.value === "custom";
  const send = commandCenter.mode.value === "send";
  if (custom && !commandCenter.customPrompt.value.trim()) {
    commandCenter.summary.textContent = "Custom prompt cannot be empty.";
    return;
  }
  if (send && !commandCenter.confirmSend.checked) {
    commandCenter.summary.textContent = "Send mode requires the confirmation checkbox.";
    return;
  }
  commandCenter.runButton.disabled = true;
  commandCenter.runButton.textContent = "Running...";
  try {
    const response = await fetch("/api/command-center/run", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        destination: commandCenter.destination.value,
        prompt_type: commandCenter.promptType.value,
        custom_prompt: commandCenter.customPrompt.value,
        mode: commandCenter.mode.value,
        confirm_send: commandCenter.confirmSend.checked,
      }),
    });
    const result = await response.json();
    commandCenter.summary.textContent = result.reason || result.detail || "Automation finished.";
    await loadCommandCenter();
  } catch (error) {
    commandCenter.summary.textContent = error.message;
  } finally {
    commandCenter.runButton.textContent = "Run now";
    await loadCommandCenter().catch(() => {});
  }
});

updateCommandCenterForm();
loadCommandCenter().catch((error) => {
  commandCenter.summary.textContent = error.message;
});
