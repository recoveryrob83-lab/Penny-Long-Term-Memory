(() => {
const commandScheduler = {
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

let schedulerStatus = {saved_prompts: [], scheduled_jobs: []};
let editingScheduleId = null;
let editingScheduleSnapshot = null;

const schedulerEscape = (value) => String(value ?? "")
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const waitForUi = (milliseconds = 40) => new Promise((resolve) => setTimeout(resolve, milliseconds));

const toLocalDateValue = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};

const toLocalTimeValue = (date) =>
  `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;

const initializeScheduleTime = () => {
  if (commandScheduler.date.value && commandScheduler.time.value) return;
  const candidate = new Date(Date.now() + 10 * 60 * 1000);
  candidate.setSeconds(0, 0);
  commandScheduler.date.value = toLocalDateValue(candidate);
  commandScheduler.time.value = toLocalTimeValue(candidate);
};

const checkedWeekdays = () => Array.from(
  commandScheduler.weekdays.querySelectorAll('input[type="checkbox"]:checked')
).map((input) => Number(input.value));

const setCheckedWeekdays = (days = []) => {
  const selected = new Set(days.map(Number));
  commandScheduler.weekdays.querySelectorAll('input[type="checkbox"]').forEach((input) => {
    input.checked = selected.has(Number(input.value));
  });
};

const destinationKeyForLabel = (label) => {
  const option = Array.from(commandScheduler.destination.options).find(
    (item) => item.textContent.trim() === label.trim()
  );
  return option?.value || null;
};

const selectedSavedPrompt = () => {
  if (commandScheduler.promptType.value !== "saved") return null;
  return schedulerStatus.saved_prompts.find(
    (item) => String(item.id) === commandScheduler.promptSelect.value
  ) || null;
};

const visibleWarningDefault = () => {
  if (!commandScheduler.destinationWarning || commandScheduler.destinationWarning.hidden) return null;
  const text = document.getElementById("cc-destination-warning-text")?.textContent || "";
  const match = text.match(/created for (.*?), but it will run in/i);
  return match ? destinationKeyForLabel(match[1]) : null;
};

const resolveDefaultDestination = () => {
  const source = commandScheduler.promptType.value;
  if (source === "canonical") return null;
  if (editingScheduleSnapshot && editingScheduleId !== null) {
    return editingScheduleSnapshot.default_destination || commandScheduler.destination.value;
  }
  if (source === "saved") {
    return selectedSavedPrompt()?.default_destination || commandScheduler.destination.value;
  }
  return visibleWarningDefault() || commandScheduler.destination.value;
};

const updateCadenceUi = () => {
  const weekly = commandScheduler.cadence.value === "weekly";
  commandScheduler.weekdays.hidden = !weekly;
  commandScheduler.dateLabel.textContent = commandScheduler.cadence.value === "once"
    ? "Run date"
    : "Start date";
  updateScheduleSummary();
};

const scheduleDescription = (schedule) => {
  const localNext = schedule.next_run_at
    ? new Date(Number(schedule.next_run_at) * 1000).toLocaleString()
    : "No future run";
  const cadence = String(schedule.cadence || "");
  const cadenceLabel = cadence === "once"
    ? "Once"
    : cadence === "daily"
      ? "Daily"
      : `Weekly (${(schedule.weekdays || []).map((day) => ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day]).join(", ")})`;
  return `${cadenceLabel} at ${schedule.schedule_time} · Next: ${localNext}`;
};

const updateScheduleSummary = () => {
  const name = commandScheduler.name.value.trim() || "This prompt";
  const date = commandScheduler.date.value;
  const time = commandScheduler.time.value;
  if (!date || !time) {
    commandScheduler.summary.textContent = "Choose a date and time to create a timed run.";
    return;
  }
  const cadence = commandScheduler.cadence.value;
  const repeat = cadence === "once"
    ? `once on ${date}`
    : cadence === "daily"
      ? `daily beginning ${date}`
      : `weekly beginning ${date}`;
  const action = commandScheduler.confirmSend.checked ? "send live" : "place a verified draft";
  const destination = commandScheduler.destination.selectedOptions[0]?.textContent || "the destination";
  commandScheduler.summary.textContent = `${name} will ${action} in ${destination} ${repeat} at ${time} CT.`;
};

const renderSchedules = () => {
  const schedules = schedulerStatus.scheduled_jobs || [];
  commandScheduler.status.textContent = schedulerStatus.scheduler_running
    ? "Scheduler running"
    : "Scheduler stopped";
  commandScheduler.list.innerHTML = schedules.map((schedule) => {
    const state = schedule.enabled ? "Active" : schedule.last_status === "succeeded" && schedule.cadence === "once" ? "Completed" : "Paused";
    const last = schedule.last_run_at
      ? `Last: ${new Date(Number(schedule.last_run_at) * 1000).toLocaleString()} · ${schedule.last_status || "unknown"}`
      : "Not run yet";
    return `<article class="cc-history-item cc-schedule-item" data-schedule-id="${schedulerEscape(schedule.id)}">
      <div class="list-item-header"><strong>${schedulerEscape(schedule.name)}</strong><span class="badge">${schedulerEscape(state)}</span></div>
      <p class="item-meta">${schedulerEscape(schedule.destination)} · ${schedulerEscape(schedule.mode)} · ${schedulerEscape(scheduleDescription(schedule))}</p>
      <p class="item-meta">${schedulerEscape(last)}</p>
      ${schedule.last_reason ? `<p class="item-meta">${schedulerEscape(schedule.last_reason)}</p>` : ""}
      <div class="cc-mini-actions">
        <button class="copy-button" type="button" data-schedule-action="edit">Edit</button>
        <button class="copy-button" type="button" data-schedule-action="toggle">${schedule.enabled ? "Pause" : "Resume"}</button>
        <button class="cc-danger-button" type="button" data-schedule-action="delete">Delete</button>
      </div>
    </article>`;
  }).join("") || '<div class="cc-history-item">No timed runs scheduled yet.</div>';
};

const loadSchedulerStatus = async () => {
  const response = await fetch("/api/command-center", {cache: "no-store"});
  if (!response.ok) throw new Error(`Scheduler status returned ${response.status}.`);
  schedulerStatus = await response.json();
  renderSchedules();
};

const collectSchedulePayload = () => {
  const source = commandScheduler.promptType.value;
  const custom = source !== "canonical";
  const prompt = commandScheduler.promptText.value.trim();
  if (custom && !prompt) {
    throw new Error(source === "saved" ? "Choose a saved prompt before scheduling." : "Custom prompt cannot be empty.");
  }
  if (!commandScheduler.name.value.trim()) throw new Error("Enter a schedule name.");
  if (!commandScheduler.date.value || !commandScheduler.time.value) {
    throw new Error("Choose both a schedule date and time.");
  }
  const weekdays = checkedWeekdays();
  if (commandScheduler.cadence.value === "weekly" && weekdays.length === 0) {
    throw new Error("Choose at least one weekday.");
  }
  const mismatchVisible = commandScheduler.destinationWarning && !commandScheduler.destinationWarning.hidden;
  if (mismatchVisible && !commandScheduler.confirmDestination.checked) {
    throw new Error("Choose the one-time destination confirmation or make the selected destination the default before scheduling.");
  }
  const saved = selectedSavedPrompt();
  return {
    name: commandScheduler.name.value.trim(),
    destination: commandScheduler.destination.value,
    prompt_type: custom ? "custom" : "canonical",
    custom_prompt: custom ? prompt : "",
    mode: commandScheduler.confirmSend.checked ? "send" : "draft",
    confirm_send: commandScheduler.confirmSend.checked,
    default_destination: resolveDefaultDestination(),
    confirm_destination: mismatchVisible ? commandScheduler.confirmDestination.checked : false,
    source_type: source,
    source_prompt_id: source === "saved" && saved ? Number(saved.id) : null,
    cadence: commandScheduler.cadence.value,
    schedule_date: commandScheduler.date.value,
    schedule_time: commandScheduler.time.value,
    weekdays,
    timezone: "America/Chicago",
    enabled: editingScheduleSnapshot ? Boolean(editingScheduleSnapshot.enabled) : true,
  };
};

const resetScheduleEditor = () => {
  editingScheduleId = null;
  editingScheduleSnapshot = null;
  commandScheduler.saveButton.textContent = "Create schedule";
  commandScheduler.cancelEditButton.hidden = true;
  commandScheduler.name.value = "";
  commandScheduler.cadence.value = "once";
  setCheckedWeekdays([]);
  initializeScheduleTime();
  updateCadenceUi();
};

const loadScheduleIntoEditor = async (schedule) => {
  editingScheduleId = Number(schedule.id);
  editingScheduleSnapshot = {...schedule};
  commandScheduler.name.value = schedule.name || "";
  commandScheduler.cadence.value = schedule.cadence || "once";
  commandScheduler.date.value = schedule.schedule_date || "";
  commandScheduler.time.value = schedule.schedule_time || "";
  setCheckedWeekdays(schedule.weekdays || []);
  updateCadenceUi();
  commandScheduler.saveButton.textContent = "Save schedule changes";
  commandScheduler.cancelEditButton.hidden = false;

  const savedStillExists = schedule.source_type === "saved" && schedulerStatus.saved_prompts.some(
    (item) => Number(item.id) === Number(schedule.source_prompt_id)
  );
  const source = schedule.source_type === "canonical"
    ? "canonical"
    : savedStillExists ? "saved" : "custom";
  commandScheduler.promptType.value = source;
  commandScheduler.promptType.dispatchEvent(new Event("change"));
  await waitForUi(80);

  if (source === "saved") {
    commandScheduler.promptSelect.value = String(schedule.source_prompt_id);
    commandScheduler.promptSelect.dispatchEvent(new Event("change"));
    await waitForUi(80);
  } else if (source === "custom") {
    commandScheduler.promptName.value = schedule.name || "Scheduled prompt";
    commandScheduler.promptText.value = schedule.custom_prompt || "";
    commandScheduler.promptName.dispatchEvent(new Event("input"));
    commandScheduler.promptText.dispatchEvent(new Event("input"));
  }

  commandScheduler.destination.value = schedule.destination;
  commandScheduler.destination.dispatchEvent(new Event("change"));
  await waitForUi(80);
  commandScheduler.confirmSend.checked = schedule.mode === "send";
  commandScheduler.confirmSend.dispatchEvent(new Event("change"));
  commandScheduler.confirmDestination.checked = Boolean(schedule.confirm_destination);
  updateScheduleSummary();
  commandScheduler.name.focus();
};

commandScheduler.cadence.addEventListener("change", updateCadenceUi);
commandScheduler.date.addEventListener("change", updateScheduleSummary);
commandScheduler.time.addEventListener("change", updateScheduleSummary);
commandScheduler.name.addEventListener("input", updateScheduleSummary);
commandScheduler.weekdays.addEventListener("change", updateScheduleSummary);
commandScheduler.destination.addEventListener("change", updateScheduleSummary);
commandScheduler.confirmSend.addEventListener("change", updateScheduleSummary);
commandScheduler.confirmDestination.addEventListener("change", updateScheduleSummary);

commandScheduler.saveButton.addEventListener("click", async () => {
  commandScheduler.saveButton.disabled = true;
  try {
    const payload = collectSchedulePayload();
    const url = editingScheduleId === null
      ? "/api/command-center/schedules"
      : `/api/command-center/schedules/${editingScheduleId}`;
    const response = await fetch(url, {
      method: editingScheduleId === null ? "POST" : "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Schedule save failed.");
    schedulerStatus = data;
    renderSchedules();
    const message = editingScheduleId === null ? "Timed run created." : "Timed run updated.";
    resetScheduleEditor();
    commandScheduler.summary.textContent = message;
  } catch (error) {
    commandScheduler.summary.textContent = error.message;
  } finally {
    commandScheduler.saveButton.disabled = false;
  }
});

commandScheduler.cancelEditButton.addEventListener("click", () => {
  resetScheduleEditor();
  commandScheduler.summary.textContent = "Schedule edit canceled.";
});

commandScheduler.list.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-schedule-action]");
  if (!button) return;
  const item = button.closest("[data-schedule-id]");
  const scheduleId = Number(item?.dataset.scheduleId);
  const schedule = (schedulerStatus.scheduled_jobs || []).find((entry) => Number(entry.id) === scheduleId);
  if (!schedule) return;
  const action = button.dataset.scheduleAction;
  button.disabled = true;
  try {
    if (action === "edit") {
      await loadScheduleIntoEditor(schedule);
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
    schedulerStatus = data;
    renderSchedules();
    commandScheduler.summary.textContent = action === "delete"
      ? `Deleted timed run: ${schedule.name}`
      : `${schedule.name} ${schedule.enabled ? "paused" : "resumed"}.`;
    if (editingScheduleId === scheduleId && action === "delete") resetScheduleEditor();
  } catch (error) {
    commandScheduler.summary.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

initializeScheduleTime();
updateCadenceUi();
loadSchedulerStatus().catch((error) => {
  commandScheduler.summary.textContent = error.message;
});
setInterval(() => loadSchedulerStatus().catch(() => {}), 15000);
})();
