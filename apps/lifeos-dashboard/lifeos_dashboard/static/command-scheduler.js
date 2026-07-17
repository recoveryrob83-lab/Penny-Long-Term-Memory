(() => {
const ui = {
  promptType: document.getElementById("cc-prompt-type"),
  promptSelect: document.getElementById("cc-prompt-select"),
  destination: document.getElementById("cc-destination"),
  promptName: document.getElementById("cc-save-name"),
  promptText: document.getElementById("cc-custom-prompt"),
  destinationWarning: document.getElementById("cc-destination-warning"),
  confirmDestination: document.getElementById("cc-confirm-destination"),
  confirmSend: document.getElementById("cc-confirm-send"),
  name: document.getElementById("cc-schedule-name"),
  cadence: document.getElementById("cc-schedule-cadence"),
  date: document.getElementById("cc-schedule-date"),
  dateLabel: document.getElementById("cc-schedule-date-label"),
  time: document.getElementById("cc-schedule-time"),
  weekdays: document.getElementById("cc-weekdays"),
  summary: document.getElementById("cc-schedule-summary"),
  saveButton: document.getElementById("cc-save-schedule"),
  cancelEditButton: document.getElementById("cc-cancel-schedule-edit"),
  list: document.getElementById("cc-schedules"),
  status: document.getElementById("cc-scheduler-status"),
};

let state = {saved_prompts: [], scheduled_jobs: []};
let editingId = null;
let editingSnapshot = null;

const escapeHtml = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");
const wait = (ms = 40) => new Promise((resolve) => setTimeout(resolve, ms));
const localDate = (date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
const localTime = (date) => `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;

function initializeTime() {
  if (ui.date.value && ui.time.value) return;
  const candidate = new Date(Date.now() + 10 * 60 * 1000);
  candidate.setSeconds(0, 0);
  ui.date.value = localDate(candidate);
  ui.time.value = localTime(candidate);
}

function checkedWeekdays() {
  return Array.from(ui.weekdays.querySelectorAll('input[type="checkbox"]:checked')).map((item) => Number(item.value));
}

function setCheckedWeekdays(days = []) {
  const selected = new Set(days.map(Number));
  ui.weekdays.querySelectorAll('input[type="checkbox"]').forEach((item) => {
    item.checked = selected.has(Number(item.value));
  });
}

function selectedSavedPrompt() {
  if (ui.promptType.value !== "saved") return null;
  return state.saved_prompts.find((item) => String(item.id) === ui.promptSelect.value) || null;
}

function destinationKeyForLabel(label) {
  return Array.from(ui.destination.options).find((item) => item.textContent.trim() === label.trim())?.value || null;
}

function visibleWarningDefault() {
  if (!ui.destinationWarning || ui.destinationWarning.hidden) return null;
  const text = document.getElementById("cc-destination-warning-text")?.textContent || "";
  const match = text.match(/created for (.*?), but it will run in/i);
  return match ? destinationKeyForLabel(match[1]) : null;
}

function resolveDefaultDestination() {
  if (ui.promptType.value === "canonical") return null;
  if (editingSnapshot && editingId !== null) return editingSnapshot.default_destination || ui.destination.value;
  if (ui.promptType.value === "saved") return selectedSavedPrompt()?.default_destination || ui.destination.value;
  return visibleWarningDefault() || ui.destination.value;
}

function updateSummary() {
  const name = ui.name.value.trim() || "This prompt";
  if (!ui.date.value || !ui.time.value) {
    ui.summary.textContent = "Choose a date and time to create a timed run.";
    return;
  }
  const cadence = ui.cadence.value;
  const repeat = cadence === "once" ? `once on ${ui.date.value}` : cadence === "daily" ? `daily beginning ${ui.date.value}` : `weekly beginning ${ui.date.value}`;
  const action = ui.confirmSend.checked ? "send live" : "place a verified draft";
  const destination = ui.destination.selectedOptions[0]?.textContent || "the destination";
  ui.summary.textContent = `${name} will ${action} in ${destination} ${repeat} at ${ui.time.value} CT.`;
}

function updateCadenceUi() {
  ui.weekdays.hidden = ui.cadence.value !== "weekly";
  ui.dateLabel.textContent = ui.cadence.value === "once" ? "Run date" : "Start date";
  updateSummary();
}

function scheduleState(schedule) {
  if (schedule.enabled) return "Active";
  if (schedule.cadence === "once" && schedule.last_status === "succeeded") return "Completed";
  if (schedule.cadence === "once" && ["failed", "refused"].includes(schedule.last_status)) return "Failed";
  return "Paused";
}

function scheduleSortKey(schedule) {
  if (schedule.enabled && schedule.next_run_at) return [0, Number(schedule.next_run_at)];
  const recent = Number(schedule.last_run_at || schedule.updated_at || schedule.created_at || 0);
  return [1, -recent];
}

function sortedSchedules() {
  return [...(state.scheduled_jobs || [])].sort((a, b) => {
    const left = scheduleSortKey(a);
    const right = scheduleSortKey(b);
    return left[0] - right[0] || left[1] - right[1] || Number(b.id) - Number(a.id);
  });
}

function description(schedule) {
  const next = schedule.next_run_at ? new Date(Number(schedule.next_run_at) * 1000).toLocaleString() : "No future run";
  const cadence = schedule.cadence === "once" ? "Once" : schedule.cadence === "daily" ? "Daily" : `Weekly (${(schedule.weekdays || []).map((day) => ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day]).join(", ")})`;
  return `${cadence} at ${schedule.schedule_time} · Next: ${next}`;
}

function render() {
  ui.status.textContent = state.scheduler_running ? "Scheduler running" : "Scheduler stopped";
  ui.list.innerHTML = sortedSchedules().map((schedule) => {
    const last = schedule.last_run_at
      ? `Last: ${new Date(Number(schedule.last_run_at) * 1000).toLocaleString()} · ${schedule.last_status || "unknown"}`
      : "Not run yet";
    return `<article class="cc-history-item cc-schedule-item" data-schedule-id="${escapeHtml(schedule.id)}">
      <div class="list-item-header"><strong>${escapeHtml(schedule.name)}</strong><span class="badge">${escapeHtml(scheduleState(schedule))}</span></div>
      <p class="item-meta">${escapeHtml(schedule.destination)} · ${escapeHtml(schedule.mode)} · ${escapeHtml(description(schedule))}</p>
      <p class="item-meta">${escapeHtml(last)}</p>
      ${schedule.last_reason ? `<p class="item-meta">${escapeHtml(schedule.last_reason)}</p>` : ""}
      <div class="cc-mini-actions">
        <button class="copy-button" type="button" data-schedule-action="edit">Edit</button>
        <button class="copy-button" type="button" data-schedule-action="toggle">${schedule.enabled ? "Pause" : "Resume"}</button>
        <button class="cc-danger-button" type="button" data-schedule-action="delete">Delete</button>
      </div>
    </article>`;
  }).join("") || '<div class="cc-history-item">No timed runs scheduled yet.</div>';
}

async function loadStatus() {
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Scheduler status returned ${response.status}.`);
  state = await response.json();
  render();
}

function collectPayload() {
  const source = ui.promptType.value;
  const custom = source !== "canonical";
  const prompt = ui.promptText.value.trim();
  if (custom && !prompt) throw new Error(source === "saved" ? "Choose a saved prompt before scheduling." : "Custom prompt cannot be empty.");
  if (!ui.name.value.trim()) throw new Error("Enter a schedule name.");
  if (!ui.date.value || !ui.time.value) throw new Error("Choose both a schedule date and time.");
  const weekdays = checkedWeekdays();
  if (ui.cadence.value === "weekly" && weekdays.length === 0) throw new Error("Choose at least one weekday.");
  const mismatchVisible = ui.destinationWarning && !ui.destinationWarning.hidden;
  if (mismatchVisible && !ui.confirmDestination.checked) throw new Error("Choose the one-time destination confirmation or make the selected destination the default before scheduling.");
  const saved = selectedSavedPrompt();
  return {
    name: ui.name.value.trim(),
    destination: ui.destination.value,
    prompt_type: custom ? "custom" : "canonical",
    custom_prompt: custom ? prompt : "",
    mode: ui.confirmSend.checked ? "send" : "draft",
    confirm_send: ui.confirmSend.checked,
    default_destination: resolveDefaultDestination(),
    confirm_destination: mismatchVisible ? ui.confirmDestination.checked : false,
    source_type: source,
    source_prompt_id: source === "saved" && saved ? Number(saved.id) : null,
    cadence: ui.cadence.value,
    schedule_date: ui.date.value,
    schedule_time: ui.time.value,
    weekdays,
    timezone: "America/Chicago",
    enabled: editingSnapshot ? Boolean(editingSnapshot.enabled) : true,
  };
}

function resetEditor() {
  editingId = null;
  editingSnapshot = null;
  ui.saveButton.textContent = "Create schedule";
  ui.cancelEditButton.hidden = true;
  ui.name.value = "";
  ui.cadence.value = "once";
  setCheckedWeekdays([]);
  initializeTime();
  updateCadenceUi();
}

async function loadIntoEditor(schedule) {
  editingId = Number(schedule.id);
  editingSnapshot = {...schedule};
  ui.name.value = schedule.name || "";
  ui.cadence.value = schedule.cadence || "once";
  ui.date.value = schedule.schedule_date || "";
  ui.time.value = schedule.schedule_time || "";
  setCheckedWeekdays(schedule.weekdays || []);
  updateCadenceUi();
  ui.saveButton.textContent = "Save schedule changes";
  ui.cancelEditButton.hidden = false;
  const savedExists = schedule.source_type === "saved" && state.saved_prompts.some((item) => Number(item.id) === Number(schedule.source_prompt_id));
  const source = schedule.source_type === "canonical" ? "canonical" : savedExists ? "saved" : "custom";
  ui.promptType.value = source;
  ui.promptType.dispatchEvent(new Event("change"));
  await wait(80);
  if (source === "saved") {
    ui.promptSelect.value = String(schedule.source_prompt_id);
    ui.promptSelect.dispatchEvent(new Event("change"));
    await wait(80);
  } else if (source === "custom") {
    ui.promptName.value = schedule.name || "Scheduled prompt";
    ui.promptText.value = schedule.custom_prompt || "";
    ui.promptName.dispatchEvent(new Event("input"));
    ui.promptText.dispatchEvent(new Event("input"));
  }
  ui.destination.value = schedule.destination;
  ui.destination.dispatchEvent(new Event("change"));
  await wait(80);
  ui.confirmSend.checked = schedule.mode === "send";
  ui.confirmSend.dispatchEvent(new Event("change"));
  ui.confirmDestination.checked = Boolean(schedule.confirm_destination);
  updateSummary();
  ui.name.focus();
}

[ui.date, ui.time, ui.destination, ui.confirmSend, ui.confirmDestination].forEach((item) => item.addEventListener("change", updateSummary));
ui.cadence.addEventListener("change", updateCadenceUi);
ui.name.addEventListener("input", updateSummary);
ui.weekdays.addEventListener("change", updateSummary);

ui.saveButton.addEventListener("click", async () => {
  ui.saveButton.disabled = true;
  try {
    const payload = collectPayload();
    const url = editingId === null ? "/api/command-center/schedules" : `/api/command-center/schedules/${editingId}`;
    const response = await fetch(url, {
      method: editingId === null ? "POST" : "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Schedule save failed.");
    state = data;
    render();
    const message = editingId === null ? "Timed run created." : "Timed run updated.";
    resetEditor();
    ui.summary.textContent = message;
  } catch (error) {
    ui.summary.textContent = error.message;
  } finally {
    ui.saveButton.disabled = false;
  }
});

ui.cancelEditButton.addEventListener("click", () => {
  resetEditor();
  ui.summary.textContent = "Schedule edit canceled.";
});

ui.list.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-schedule-action]");
  if (!button) return;
  const scheduleId = Number(button.closest("[data-schedule-id]")?.dataset.scheduleId);
  const schedule = (state.scheduled_jobs || []).find((item) => Number(item.id) === scheduleId);
  if (!schedule) return;
  const action = button.dataset.scheduleAction;
  button.disabled = true;
  try {
    if (action === "edit") {
      await loadIntoEditor(schedule);
      return;
    }
    const response = action === "delete"
      ? await fetch(`/api/command-center/schedules/${scheduleId}`, {method: "DELETE"})
      : await fetch(`/api/command-center/schedules/${scheduleId}/enabled`, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({enabled: !schedule.enabled}),
        });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Schedule action failed.");
    state = data;
    render();
    ui.summary.textContent = action === "delete" ? `Deleted timed run: ${schedule.name}` : `${schedule.name} ${schedule.enabled ? "paused" : "resumed"}.`;
    if (editingId === scheduleId && action === "delete") resetEditor();
  } catch (error) {
    ui.summary.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

initializeTime();
updateCadenceUi();
loadStatus().catch((error) => { ui.summary.textContent = error.message; });
setInterval(() => loadStatus().catch(() => {}), 15000);
})();
