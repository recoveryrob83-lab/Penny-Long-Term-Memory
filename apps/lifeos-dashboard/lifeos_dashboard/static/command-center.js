const commandCenter = {
  destination: document.getElementById("cc-destination"),
  promptType: document.getElementById("cc-prompt-type"),
  promptWrap: document.getElementById("cc-prompt-wrap"),
  promptSelect: document.getElementById("cc-prompt-select"),
  customPrompt: document.getElementById("cc-custom-prompt"),
  canonicalControls: document.getElementById("cc-canonical-controls"),
  duplicateButton: document.getElementById("cc-duplicate-prompt"),
  saveControls: document.getElementById("cc-save-controls"),
  saveName: document.getElementById("cc-save-name"),
  saveButton: document.getElementById("cc-save-prompt"),
  updateButton: document.getElementById("cc-update-prompt"),
  deleteButton: document.getElementById("cc-delete-prompt"),
  confirmWrap: document.getElementById("cc-confirm-wrap"),
  confirmSend: document.getElementById("cc-confirm-send"),
  runButton: document.getElementById("cc-run"),
  pauseButton: document.getElementById("cc-pause"),
  summary: document.getElementById("cc-summary"),
  status: document.getElementById("cc-status"),
  history: document.getElementById("cc-history"),
};

const canonicalPrompts = [
  {key: "boot", label: "Boot"},
];

let savedPrompts = [];
let canonicalRequestToken = 0;
let lastPromptType = commandCenter.promptType.value;
let selectedCanonicalKey = "boot";
let selectedSavedPromptId = "";
let customDraft = {name: "", prompt: ""};

const ccEscape = (value) => String(value ?? "")
  .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;").replaceAll("'", "&#039;");

const selectedSavedPrompt = () => savedPrompts.find(
  (item) => String(item.id) === selectedSavedPromptId
);

const activePromptText = () => commandCenter.customPrompt.value;

const rememberCustomDraft = () => {
  if (commandCenter.promptType.value !== "custom") return;
  customDraft = {
    name: commandCenter.saveName.value,
    prompt: commandCenter.customPrompt.value,
  };
};

const capturePromptSelection = (source = commandCenter.promptType.value) => {
  if (source === "canonical") {
    selectedCanonicalKey = commandCenter.promptSelect.value || "boot";
  } else if (source === "saved") {
    selectedSavedPromptId = commandCenter.promptSelect.value;
  }
};

const renderPromptSelector = () => {
  const type = commandCenter.promptType.value;
  commandCenter.promptWrap.hidden = type === "custom";

  if (type === "canonical") {
    commandCenter.promptSelect.innerHTML = canonicalPrompts.map((item) =>
      `<option value="${ccEscape(item.key)}">${ccEscape(item.label)}</option>`
    ).join("");
    if (!canonicalPrompts.some((item) => item.key === selectedCanonicalKey)) {
      selectedCanonicalKey = canonicalPrompts[0]?.key || "";
    }
    commandCenter.promptSelect.value = selectedCanonicalKey;
    return;
  }

  if (type === "saved") {
    commandCenter.promptSelect.innerHTML = '<option value="">Choose a saved prompt</option>' + savedPrompts.map((item) =>
      `<option value="${ccEscape(item.id)}">${ccEscape(item.name)}</option>`
    ).join("");
    if (!savedPrompts.some((item) => String(item.id) === selectedSavedPromptId)) {
      selectedSavedPromptId = "";
    }
    commandCenter.promptSelect.value = selectedSavedPromptId;
  }
};

const loadCanonicalPrompt = async () => {
  if (selectedCanonicalKey !== "boot") {
    throw new Error("That canonical prompt is not available yet.");
  }
  const token = ++canonicalRequestToken;
  commandCenter.saveName.value = "Loading canonical prompt...";
  commandCenter.customPrompt.value = "Loading prompt text...";
  const response = await fetch(
    `/api/command-center/canonical-prompt/${encodeURIComponent(commandCenter.destination.value)}`,
    {cache: "no-store"},
  );
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Canonical prompt preview failed.");
  if (token !== canonicalRequestToken || commandCenter.promptType.value !== "canonical") return;
  commandCenter.saveName.value = data.name || "Canonical boot prompt";
  commandCenter.customPrompt.value = data.prompt || "";
};

const syncPromptDetails = async () => {
  const type = commandCenter.promptType.value;
  const selected = selectedSavedPrompt();

  commandCenter.canonicalControls.hidden = type !== "canonical";
  commandCenter.saveControls.hidden = type === "canonical";
  commandCenter.saveButton.hidden = type !== "custom";
  commandCenter.updateButton.hidden = type !== "saved" || !selected;
  commandCenter.deleteButton.hidden = type !== "saved" || !selected;
  commandCenter.saveName.readOnly = type === "canonical" || (type === "saved" && !selected);
  commandCenter.customPrompt.readOnly = type === "canonical" || (type === "saved" && !selected);

  if (type === "canonical") {
    try {
      await loadCanonicalPrompt();
    } catch (error) {
      commandCenter.saveName.value = "Canonical boot prompt";
      commandCenter.customPrompt.value = "";
      commandCenter.summary.textContent = error.message;
    }
  } else if (type === "saved") {
    canonicalRequestToken += 1;
    commandCenter.saveName.value = selected?.name || "";
    commandCenter.customPrompt.value = selected?.prompt || "";
  } else {
    canonicalRequestToken += 1;
    commandCenter.saveName.readOnly = false;
    commandCenter.customPrompt.readOnly = false;
  }
};

const updateCommandCenterForm = async () => {
  const type = commandCenter.promptType.value;
  const send = commandCenter.confirmSend.checked;
  await syncPromptDetails();
  const canonicalLabel = canonicalPrompts.find((item) => item.key === selectedCanonicalKey)?.label || "Canonical";
  const promptLabel = type === "canonical"
    ? `${canonicalLabel} canonical prompt`
    : type === "saved"
      ? "saved prompt"
      : "new custom prompt";
  const action = send ? "send live" : "place as a verified draft";
  const label = commandCenter.destination.selectedOptions[0]?.textContent || "destination";
  commandCenter.summary.textContent = `${action[0].toUpperCase()}${action.slice(1)} the ${promptLabel} in ${label}.`;
};

const setSavedPrompts = (items = []) => {
  savedPrompts = items;
  if (!savedPrompts.some((item) => String(item.id) === selectedSavedPromptId)) {
    selectedSavedPromptId = "";
  }
  renderPromptSelector();
};

const renderCommandCenter = async (data) => {
  commandCenter.status.textContent = data.paused ? "Paused" : data.running ? "Running" : "Ready";
  commandCenter.status.className = `mode-badge ${data.paused ? "cc-paused" : data.running ? "cc-running" : "cc-ready"}`;
  commandCenter.pauseButton.textContent = data.paused ? "Resume automation" : "Pause automation";
  commandCenter.runButton.disabled = Boolean(data.paused || data.running);
  setSavedPrompts(data.saved_prompts || []);
  const history = data.history || [];
  commandCenter.history.innerHTML = history.map((item) => {
    const when = item.finished_at ? new Date(item.finished_at * 1000).toLocaleString() : "";
    const detail = item.stderr?.trim() || item.stdout?.trim() || item.reason;
    return `<div class="cc-history-item">
      <div class="list-item-header"><strong>${ccEscape(item.destination)}</strong><span class="badge">${ccEscape(item.status)}</span></div>
      <p class="item-meta">${ccEscape(item.mode)} · ${ccEscape(item.prompt_type)} · ${ccEscape(when)}</p>
      <p class="item-meta">${ccEscape(detail)}</p>
    </div>`;
  }).join("") || '<div class="cc-history-item">No automation runs recorded yet.</div>';
  await updateCommandCenterForm();
};

const loadCommandCenter = async () => {
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Command Center returned ${response.status}.`);
  await renderCommandCenter(await response.json());
};

commandCenter.promptType.addEventListener("change", async () => {
  capturePromptSelection(lastPromptType);
  if (lastPromptType === "custom") {
    customDraft = {
      name: commandCenter.saveName.value,
      prompt: commandCenter.customPrompt.value,
    };
  }
  const nextType = commandCenter.promptType.value;
  lastPromptType = nextType;
  renderPromptSelector();
  if (nextType === "custom") {
    commandCenter.saveName.value = customDraft.name;
    commandCenter.customPrompt.value = customDraft.prompt;
  }
  await updateCommandCenterForm();
});

commandCenter.promptSelect.addEventListener("change", async () => {
  capturePromptSelection();
  await updateCommandCenterForm();
});
commandCenter.destination.addEventListener("change", updateCommandCenterForm);
commandCenter.confirmSend.addEventListener("change", updateCommandCenterForm);
commandCenter.saveName.addEventListener("input", rememberCustomDraft);
commandCenter.customPrompt.addEventListener("input", rememberCustomDraft);

commandCenter.duplicateButton.addEventListener("click", async () => {
  if (commandCenter.promptType.value !== "canonical") return;
  const originalName = commandCenter.saveName.value.trim() || "Canonical boot prompt";
  const originalPrompt = commandCenter.customPrompt.value;
  if (!originalPrompt.trim()) {
    commandCenter.summary.textContent = "Canonical prompt text is not loaded yet.";
    return;
  }
  canonicalRequestToken += 1;
  customDraft = {
    name: `${originalName} copy`,
    prompt: originalPrompt,
  };
  commandCenter.promptType.value = "custom";
  lastPromptType = "custom";
  renderPromptSelector();
  commandCenter.saveName.value = customDraft.name;
  commandCenter.customPrompt.value = customDraft.prompt;
  await updateCommandCenterForm();
  commandCenter.summary.textContent = "Editable copy created. Rename it, adjust the prompt if needed, then save it as a new prompt.";
  commandCenter.saveName.focus();
  commandCenter.saveName.select();
});

commandCenter.saveButton.addEventListener("click", async () => {
  const name = commandCenter.saveName.value.trim();
  const prompt = commandCenter.customPrompt.value.trim();
  if (!name || !prompt) {
    commandCenter.summary.textContent = "Enter both a prompt name and prompt text before saving.";
    return;
  }
  const response = await fetch("/api/command-center/prompts", {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, prompt}),
  });
  const data = await response.json();
  if (!response.ok) {
    commandCenter.summary.textContent = data.detail || "Saved prompt failed.";
    return;
  }
  await renderCommandCenter(data);
  const saved = savedPrompts.find((item) => item.name === name);
  if (saved) {
    commandCenter.promptType.value = "saved";
    lastPromptType = "saved";
    selectedSavedPromptId = String(saved.id);
    renderPromptSelector();
    await updateCommandCenterForm();
  }
  commandCenter.summary.textContent = `Saved prompt: ${name}`;
});

commandCenter.updateButton.addEventListener("click", async () => {
  const selected = selectedSavedPrompt();
  const name = commandCenter.saveName.value.trim();
  const prompt = commandCenter.customPrompt.value.trim();
  if (!selected) {
    commandCenter.summary.textContent = "Choose a saved prompt before saving changes.";
    return;
  }
  if (!name || !prompt) {
    commandCenter.summary.textContent = "Prompt name and text cannot be empty.";
    return;
  }
  const response = await fetch(`/api/command-center/prompts/${selected.id}`, {
    method: "PUT", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, prompt}),
  });
  const data = await response.json();
  if (!response.ok) {
    commandCenter.summary.textContent = data.detail || "Update failed.";
    return;
  }
  selectedSavedPromptId = String(selected.id);
  await renderCommandCenter(data);
  renderPromptSelector();
  await updateCommandCenterForm();
  commandCenter.summary.textContent = `Updated saved prompt: ${name}`;
});

commandCenter.deleteButton.addEventListener("click", async () => {
  const selected = selectedSavedPrompt();
  if (!selected) return;
  const response = await fetch(`/api/command-center/prompts/${selected.id}`, {method: "DELETE"});
  const data = await response.json();
  if (!response.ok) {
    commandCenter.summary.textContent = data.detail || "Delete failed.";
    return;
  }
  selectedSavedPromptId = "";
  await renderCommandCenter(data);
  commandCenter.summary.textContent = `Deleted saved prompt: ${selected.name}`;
});

commandCenter.pauseButton.addEventListener("click", async () => {
  commandCenter.pauseButton.disabled = true;
  try {
    const current = await (await fetch("/api/command-center", {cache: "no-store"})).json();
    const response = await fetch("/api/command-center/pause", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({paused: !current.paused}),
    });
    if (!response.ok) throw new Error(`Pause control returned ${response.status}.`);
    await renderCommandCenter(await response.json());
  } catch (error) {
    commandCenter.summary.textContent = error.message;
  } finally {
    commandCenter.pauseButton.disabled = false;
  }
});

commandCenter.runButton.addEventListener("click", async () => {
  const type = commandCenter.promptType.value;
  const custom = type !== "canonical";
  const send = commandCenter.confirmSend.checked;
  const prompt = activePromptText();
  if (custom && !prompt.trim()) {
    commandCenter.summary.textContent = type === "saved" ? "Choose a saved prompt." : "Custom prompt cannot be empty.";
    return;
  }
  commandCenter.runButton.disabled = true;
  commandCenter.runButton.textContent = "Running...";
  try {
    const response = await fetch("/api/command-center/run", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        destination: commandCenter.destination.value,
        prompt_type: custom ? "custom" : "canonical",
        custom_prompt: prompt,
        mode: send ? "send" : "draft",
        confirm_send: send,
      }),
    });
    const result = await response.json();
    commandCenter.summary.textContent = result.reason || result.detail || "Automation finished.";
  } catch (error) {
    commandCenter.summary.textContent = error.message;
  } finally {
    commandCenter.runButton.textContent = "Run now";
    await loadCommandCenter().catch(() => {});
  }
});

renderPromptSelector();
updateCommandCenterForm();
loadCommandCenter().catch((error) => { commandCenter.summary.textContent = error.message; });