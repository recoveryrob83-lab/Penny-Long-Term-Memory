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
  destinationWarning: document.getElementById("cc-destination-warning"),
  destinationWarningText: document.getElementById("cc-destination-warning-text"),
  confirmDestination: document.getElementById("cc-confirm-destination"),
  confirmDestinationText: document.getElementById("cc-confirm-destination-text"),
  makeDestinationDefault: document.getElementById("cc-make-destination-default"),
  confirmSend: document.getElementById("cc-confirm-send"),
  runButton: document.getElementById("cc-run"),
  pauseButton: document.getElementById("cc-pause"),
  summary: document.getElementById("cc-summary"),
  status: document.getElementById("cc-status"),
  history: document.getElementById("cc-history"),
};

const fallbackCanonicalPrompts = [{
  key: "boot",
  label: "Boot",
  category: "Boot / Sync",
  description: "Load the canonical operating kernel and role-routed department context.",
  scope: "department",
  read_only: true,
}];

let canonicalPrompts = [...fallbackCanonicalPrompts];
let savedPrompts = [];
let canonicalRequestToken = 0;
let lastPromptType = commandCenter.promptType.value;
let selectedCanonicalKey = "boot";
let selectedSavedPromptId = "";
let customDraft = {
  name: "",
  prompt: "",
  defaultDestination: null,
  originType: null,
  originPromptKey: null,
};

const ccEscape = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const selectedSavedPrompt = () => savedPrompts.find(
  (item) => String(item.id) === selectedSavedPromptId,
);

const destinationLabel = (key) => {
  const option = Array.from(commandCenter.destination.options).find(
    (item) => item.value === key,
  );
  return option?.textContent || key || "the original destination";
};

const metadataDefaultDestination = (item) => (
  item?.default_destination || item?.defaultDestination || null
);
const metadataOriginType = (item) => item?.origin_type || item?.originType || null;
const metadataOriginPromptKey = (item) => (
  item?.origin_prompt_key || item?.originPromptKey || null
);

const activePromptMetadata = () => {
  const type = commandCenter.promptType.value;
  if (type === "saved") return selectedSavedPrompt();
  if (type === "custom") return customDraft;
  return null;
};

const destinationMismatch = () => {
  if (commandCenter.promptType.value === "canonical") return false;
  const original = metadataDefaultDestination(activePromptMetadata());
  return Boolean(original && original !== commandCenter.destination.value);
};

const resetDestinationConfirmation = () => {
  commandCenter.confirmDestination.checked = false;
};

const rememberCustomDraft = () => {
  if (commandCenter.promptType.value !== "custom") return;
  customDraft = {
    ...customDraft,
    name: commandCenter.saveName.value,
    prompt: commandCenter.customPrompt.value,
  };
};

const capturePromptSelection = (type = commandCenter.promptType.value) => {
  if (type === "canonical") {
    selectedCanonicalKey = commandCenter.promptSelect.value || "boot";
  } else if (type === "saved") {
    selectedSavedPromptId = commandCenter.promptSelect.value;
  }
};

function setCanonicalPrompts(items = []) {
  const valid = Array.isArray(items)
    ? items.filter((item) => item && item.key && item.label)
    : [];
  canonicalPrompts = valid.length ? valid : [...fallbackCanonicalPrompts];
  if (!canonicalPrompts.some((item) => item.key === selectedCanonicalKey)) {
    selectedCanonicalKey = canonicalPrompts[0]?.key || "boot";
  }
  renderPromptSelector();
}

function renderPromptSelector() {
  const type = commandCenter.promptType.value;
  commandCenter.promptWrap.hidden = type === "custom";
  if (type === "canonical") {
    commandCenter.promptSelect.innerHTML = canonicalPrompts.map(
      (item) => `<option value="${ccEscape(item.key)}">${ccEscape(item.label)}</option>`,
    ).join("");
    if (!canonicalPrompts.some((item) => item.key === selectedCanonicalKey)) {
      selectedCanonicalKey = canonicalPrompts[0]?.key || "";
    }
    commandCenter.promptSelect.value = selectedCanonicalKey;
    return;
  }
  if (type === "saved") {
    commandCenter.promptSelect.innerHTML = '<option value="">Choose a saved prompt</option>'
      + savedPrompts.map(
        (item) => `<option value="${ccEscape(item.id)}">${ccEscape(item.name)}</option>`,
      ).join("");
    if (!savedPrompts.some((item) => String(item.id) === selectedSavedPromptId)) {
      selectedSavedPromptId = "";
    }
    commandCenter.promptSelect.value = selectedSavedPromptId;
  }
}

function applySavedDefaultDestination() {
  const defaultDestination = metadataDefaultDestination(selectedSavedPrompt());
  if (!defaultDestination) return;
  if (Array.from(commandCenter.destination.options).some(
    (item) => item.value === defaultDestination,
  )) {
    commandCenter.destination.value = defaultDestination;
  }
}

async function loadCanonicalPrompt() {
  const token = ++canonicalRequestToken;
  commandCenter.saveName.value = "Loading canonical prompt...";
  commandCenter.customPrompt.value = "Loading prompt text...";
  const destinationToken = `${commandCenter.destination.value}~${selectedCanonicalKey}`;
  const response = await fetch(
    `/api/command-center/canonical-prompt/${encodeURIComponent(destinationToken)}`,
    {cache: "no-store"},
  );
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Canonical prompt preview failed.");
  if (token !== canonicalRequestToken || commandCenter.promptType.value !== "canonical") {
    return;
  }
  commandCenter.saveName.value = data.name || "Canonical prompt";
  commandCenter.customPrompt.value = data.prompt || "";
}

async function syncPromptDetails() {
  const type = commandCenter.promptType.value;
  const saved = selectedSavedPrompt();
  commandCenter.canonicalControls.hidden = type !== "canonical";
  commandCenter.saveControls.hidden = type === "canonical";
  commandCenter.saveButton.hidden = type !== "custom";
  commandCenter.updateButton.hidden = type !== "saved" || !saved;
  commandCenter.deleteButton.hidden = type !== "saved" || !saved;
  commandCenter.saveName.readOnly = type === "canonical" || (type === "saved" && !saved);
  commandCenter.customPrompt.readOnly = type === "canonical" || (type === "saved" && !saved);

  if (type === "canonical") {
    try {
      await loadCanonicalPrompt();
    } catch (error) {
      const definition = canonicalPrompts.find((item) => item.key === selectedCanonicalKey);
      commandCenter.saveName.value = definition?.label || "Canonical prompt";
      commandCenter.customPrompt.value = "";
      commandCenter.summary.textContent = error.message;
    }
    return;
  }

  canonicalRequestToken += 1;
  if (type === "saved") {
    commandCenter.saveName.value = saved?.name || "";
    commandCenter.customPrompt.value = saved?.prompt || "";
  } else {
    commandCenter.saveName.readOnly = false;
    commandCenter.customPrompt.readOnly = false;
  }
}

function renderDestinationWarning() {
  const type = commandCenter.promptType.value;
  const metadata = activePromptMetadata();
  const original = metadataDefaultDestination(metadata);
  const mismatch = type !== "canonical" && destinationMismatch();
  commandCenter.destinationWarning.hidden = !mismatch;
  if (!mismatch) {
    resetDestinationConfirmation();
    return;
  }
  const originalLabel = destinationLabel(original);
  const selectedLabel = destinationLabel(commandCenter.destination.value);
  commandCenter.destinationWarningText.textContent = (
    `This prompt was created for ${originalLabel}, but it will run in ${selectedLabel}. `
    + "Review the prompt text before continuing."
  );
  commandCenter.confirmDestinationText.textContent = (
    `Use ${selectedLabel} for this run only. I reviewed the prompt and intend to send it there.`
  );
  commandCenter.makeDestinationDefault.textContent = type === "saved"
    ? `Make ${selectedLabel} the saved default`
    : `Use ${selectedLabel} as this prompt's default`;
}

async function updateCommandCenterForm({syncPrompt = true} = {}) {
  const type = commandCenter.promptType.value;
  const send = commandCenter.confirmSend.checked;
  if (syncPrompt) await syncPromptDetails();
  renderDestinationWarning();
  const definition = canonicalPrompts.find((item) => item.key === selectedCanonicalKey);
  const canonicalLabel = definition?.label || "Canonical";
  const promptLabel = type === "canonical"
    ? `${canonicalLabel} canonical prompt`
    : type === "saved"
      ? "saved prompt"
      : "new custom prompt";
  const action = send ? "send live" : "place as a verified draft";
  const destination = commandCenter.destination.selectedOptions[0]?.textContent || "destination";
  commandCenter.summary.textContent = (
    `${action[0].toUpperCase()}${action.slice(1)} the ${promptLabel} in ${destination}.`
  );
}

function setSavedPrompts(items = []) {
  savedPrompts = items;
  if (!savedPrompts.some((item) => String(item.id) === selectedSavedPromptId)) {
    selectedSavedPromptId = "";
  }
  renderPromptSelector();
}

function renderHistory(items = []) {
  commandCenter.history.innerHTML = items.map((item) => {
    const finished = item.finished_at
      ? new Date(item.finished_at * 1000).toLocaleString()
      : "";
    const detail = item.stderr?.trim() || item.stdout?.trim() || item.reason;
    return `<div class="cc-history-item">
      <div class="list-item-header"><strong>${ccEscape(item.destination)}</strong><span class="badge">${ccEscape(item.status)}</span></div>
      <p class="item-meta">${ccEscape(item.mode)} · ${ccEscape(item.prompt_type)} · ${ccEscape(finished)}</p>
      <p class="item-meta">${ccEscape(detail)}</p>
    </div>`;
  }).join("") || '<div class="cc-history-item">No automation runs recorded yet.</div>';
}

async function renderCommandCenter(data) {
  commandCenter.status.textContent = data.paused ? "Paused" : data.running ? "Running" : "Ready";
  commandCenter.status.className = `mode-badge ${data.paused ? "cc-paused" : data.running ? "cc-running" : "cc-ready"}`;
  commandCenter.pauseButton.textContent = data.paused ? "Resume automation" : "Pause automation";
  commandCenter.runButton.disabled = Boolean(data.paused || data.running);
  setCanonicalPrompts(data.canonical_prompts || []);
  setSavedPrompts(data.saved_prompts || []);
  renderHistory(data.history || []);
  await updateCommandCenterForm();
}

async function loadCommandCenter() {
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Command Center returned ${response.status}.`);
  await renderCommandCenter(await response.json());
}

commandCenter.promptType.addEventListener("change", async () => {
  capturePromptSelection(lastPromptType);
  if (lastPromptType === "custom") rememberCustomDraft();
  resetDestinationConfirmation();
  const type = commandCenter.promptType.value;
  lastPromptType = type;
  renderPromptSelector();
  if (type === "custom") {
    commandCenter.saveName.value = customDraft.name;
    commandCenter.customPrompt.value = customDraft.prompt;
  } else if (type === "saved") {
    applySavedDefaultDestination();
  }
  await updateCommandCenterForm();
});

commandCenter.promptSelect.addEventListener("change", async () => {
  capturePromptSelection();
  resetDestinationConfirmation();
  if (commandCenter.promptType.value === "saved") applySavedDefaultDestination();
  await updateCommandCenterForm();
});

commandCenter.destination.addEventListener("change", async () => {
  resetDestinationConfirmation();
  await updateCommandCenterForm({
    syncPrompt: commandCenter.promptType.value === "canonical",
  });
});

commandCenter.confirmDestination.addEventListener(
  "change",
  () => updateCommandCenterForm({syncPrompt: false}),
);
commandCenter.confirmSend.addEventListener(
  "change",
  () => updateCommandCenterForm({syncPrompt: false}),
);
commandCenter.saveName.addEventListener("input", rememberCustomDraft);
commandCenter.customPrompt.addEventListener("input", rememberCustomDraft);

commandCenter.duplicateButton.addEventListener("click", async () => {
  if (commandCenter.promptType.value !== "canonical") return;
  const name = commandCenter.saveName.value.trim() || "Canonical prompt";
  const prompt = commandCenter.customPrompt.value;
  if (!prompt.trim()) {
    commandCenter.summary.textContent = "Canonical prompt text is not loaded yet.";
    return;
  }
  canonicalRequestToken += 1;
  customDraft = {
    name: `${name} copy`,
    prompt,
    defaultDestination: commandCenter.destination.value,
    originType: "canonical",
    originPromptKey: selectedCanonicalKey,
  };
  commandCenter.promptType.value = "custom";
  lastPromptType = "custom";
  resetDestinationConfirmation();
  renderPromptSelector();
  commandCenter.saveName.value = customDraft.name;
  commandCenter.customPrompt.value = customDraft.prompt;
  await updateCommandCenterForm();
  commandCenter.summary.textContent = (
    "Editable copy created. Rename it, adjust the prompt if needed, then save it as a new prompt."
  );
  commandCenter.saveName.focus();
  commandCenter.saveName.select();
});

commandCenter.makeDestinationDefault.addEventListener("click", async () => {
  if (!destinationMismatch()) return;
  const key = commandCenter.destination.value;
  const label = destinationLabel(key);
  const type = commandCenter.promptType.value;
  if (type === "custom") {
    customDraft = {...customDraft, defaultDestination: key};
    resetDestinationConfirmation();
    renderDestinationWarning();
    commandCenter.summary.textContent = `Default destination set to ${label}. Save the prompt to keep this setting.`;
    return;
  }
  const saved = selectedSavedPrompt();
  if (type !== "saved" || !saved) return;
  const currentName = commandCenter.saveName.value;
  const currentPrompt = commandCenter.customPrompt.value;
  commandCenter.makeDestinationDefault.disabled = true;
  try {
    const response = await fetch(`/api/command-center/prompts/${saved.id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: saved.name,
        prompt: saved.prompt,
        default_destination: key,
        origin_type: metadataOriginType(saved),
        origin_prompt_key: metadataOriginPromptKey(saved),
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      commandCenter.summary.textContent = data.detail || "Default destination update failed.";
      return;
    }
    setSavedPrompts(data.saved_prompts || []);
    commandCenter.saveName.value = currentName;
    commandCenter.customPrompt.value = currentPrompt;
    resetDestinationConfirmation();
    renderDestinationWarning();
    commandCenter.summary.textContent = `Default destination updated to ${label}.`;
  } catch (error) {
    commandCenter.summary.textContent = error.message;
  } finally {
    commandCenter.makeDestinationDefault.disabled = false;
  }
});

commandCenter.saveButton.addEventListener("click", async () => {
  const name = commandCenter.saveName.value.trim();
  const prompt = commandCenter.customPrompt.value.trim();
  if (!name || !prompt) {
    commandCenter.summary.textContent = "Enter both a prompt name and prompt text before saving.";
    return;
  }
  const defaultDestination = metadataDefaultDestination(customDraft)
    || commandCenter.destination.value;
  const response = await fetch("/api/command-center/prompts", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name,
      prompt,
      default_destination: defaultDestination,
      origin_type: metadataOriginType(customDraft),
      origin_prompt_key: metadataOriginPromptKey(customDraft),
    }),
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
    applySavedDefaultDestination();
    resetDestinationConfirmation();
    await updateCommandCenterForm();
  }
  commandCenter.summary.textContent = `Saved prompt: ${name}`;
});

commandCenter.updateButton.addEventListener("click", async () => {
  const saved = selectedSavedPrompt();
  const name = commandCenter.saveName.value.trim();
  const prompt = commandCenter.customPrompt.value.trim();
  if (!saved) {
    commandCenter.summary.textContent = "Choose a saved prompt before saving changes.";
    return;
  }
  if (!name || !prompt) {
    commandCenter.summary.textContent = "Prompt name and text cannot be empty.";
    return;
  }
  const response = await fetch(`/api/command-center/prompts/${saved.id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name,
      prompt,
      default_destination: metadataDefaultDestination(saved),
      origin_type: metadataOriginType(saved),
      origin_prompt_key: metadataOriginPromptKey(saved),
    }),
  });
  const data = await response.json();
  if (response.ok) {
    selectedSavedPromptId = String(saved.id);
    await renderCommandCenter(data);
    renderPromptSelector();
    await updateCommandCenterForm();
    commandCenter.summary.textContent = `Updated saved prompt: ${name}`;
  } else {
    commandCenter.summary.textContent = data.detail || "Update failed.";
  }
});

commandCenter.deleteButton.addEventListener("click", async () => {
  const saved = selectedSavedPrompt();
  if (!saved) return;
  const response = await fetch(`/api/command-center/prompts/${saved.id}`, {method: "DELETE"});
  const data = await response.json();
  if (response.ok) {
    selectedSavedPromptId = "";
    resetDestinationConfirmation();
    await renderCommandCenter(data);
    commandCenter.summary.textContent = `Deleted saved prompt: ${saved.name}`;
  } else {
    commandCenter.summary.textContent = data.detail || "Delete failed.";
  }
});

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
  const prompt = commandCenter.customPrompt.value;
  if (custom && !prompt.trim()) {
    commandCenter.summary.textContent = type === "saved"
      ? "Choose a saved prompt."
      : "Custom prompt cannot be empty.";
    return;
  }
  if (!custom && !prompt.trim()) {
    commandCenter.summary.textContent = "Canonical prompt text is not loaded yet.";
    return;
  }
  if (destinationMismatch() && !commandCenter.confirmDestination.checked) {
    const label = destinationLabel(commandCenter.destination.value);
    commandCenter.summary.textContent = (
      `Choose whether to use ${label} once or make it the new default before running.`
    );
    commandCenter.confirmDestination.focus();
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
        prompt_type: custom ? "custom" : "canonical",
        custom_prompt: prompt,
        mode: send ? "send" : "draft",
        confirm_send: send,
        default_destination: metadataDefaultDestination(activePromptMetadata()),
        confirm_destination: commandCenter.confirmDestination.checked,
      }),
    });
    const data = await response.json();
    commandCenter.summary.textContent = data.reason || data.detail || "Automation finished.";
  } catch (error) {
    commandCenter.summary.textContent = error.message;
  } finally {
    commandCenter.runButton.textContent = "Run now";
    await loadCommandCenter().catch(() => {});
  }
});

renderPromptSelector();
updateCommandCenterForm();
loadCommandCenter().catch((error) => {
  commandCenter.summary.textContent = error.message;
});
