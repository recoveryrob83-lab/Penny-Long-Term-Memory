(() => {
  const CATEGORY_BY_TYPE = {
    work_item: "work",
    milestone: "work",
    note: "knowledge",
    decision: "knowledge",
    status: "operations",
    rule: "operations",
    watch: "operations",
    log: "operations",
    handoff: "operations",
  };

  const PRIORITY_ORDER = {
    critical: 0,
    high: 1,
    normal: 2,
    low: 3,
    none: 4,
    unknown: 5,
  };

  const byId = (id) => document.getElementById(id);
  const escape = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  let inspection = {
    records: [],
    findings: [],
    scopes: [],
    summary: {},
  };
  let loading = null;

  const scopeLabel = (department) => {
    const match = inspection.scopes.find((item) => item.id === department);
    return match?.label || department || "Unknown";
  };

  const recordCategory = (record) => (
    CATEGORY_BY_TYPE[record.record_type] || "operations"
  );

  const recordDate = (record) => (
    record.record_date
    || record.updated_at
    || record.closed_at
    || record.due_at
    || record.created_at
    || ""
  );

  const searchText = (record) => [
    record.title,
    record.summary,
    record.department,
    record.record_type,
    record.subtype,
    record.state,
    record.priority,
    record.owner,
    record.source_path,
    record.source_section,
    record.raw_text,
    ...(record.warnings || []),
  ].join(" ").toLowerCase();

  const filterState = () => ({
    department: byId("di-filter-department").value,
    category: byId("di-filter-category").value,
    recordType: byId("di-filter-type").value,
    state: byId("di-filter-state").value,
    priority: byId("di-filter-priority").value,
    dateFrom: byId("di-filter-date-from").value,
    dateTo: byId("di-filter-date-to").value,
    crossDepartment: byId("di-filter-cross").value,
    authority: byId("di-filter-authority").value,
    warningsOnly: byId("di-filter-warnings").checked,
    query: byId("di-filter-search").value.trim().toLowerCase(),
    sort: byId("di-filter-sort").value,
  });

  const matchesRecord = (record, filters) => {
    if (filters.category !== "all" && recordCategory(record) !== filters.category) {
      return false;
    }
    if (filters.department !== "all" && record.department !== filters.department) {
      return false;
    }
    if (filters.recordType !== "all" && record.record_type !== filters.recordType) {
      return false;
    }
    if (filters.state !== "all" && record.state !== filters.state) {
      return false;
    }
    if (filters.priority !== "all" && record.priority !== filters.priority) {
      return false;
    }
    if (
      filters.crossDepartment !== "all"
      && String(Boolean(record.cross_department)) !== filters.crossDepartment
    ) {
      return false;
    }
    if (
      filters.authority !== "all"
      && record.source_authority !== filters.authority
    ) {
      return false;
    }
    if (filters.warningsOnly && !(record.warnings || []).length) {
      return false;
    }

    const date = recordDate(record);
    if (filters.dateFrom && (!date || date < filters.dateFrom)) {
      return false;
    }
    if (filters.dateTo && (!date || date > filters.dateTo)) {
      return false;
    }
    if (filters.query && !searchText(record).includes(filters.query)) {
      return false;
    }
    return true;
  };

  const matchesFinding = (finding, filters) => {
    if (!["all", "findings"].includes(filters.category)) {
      return false;
    }
    if (
      filters.department !== "all"
      && !(finding.departments || []).includes(filters.department)
    ) {
      return false;
    }
    if (
      filters.recordType !== "all"
      || filters.state !== "all"
      || filters.priority !== "all"
      || filters.crossDepartment !== "all"
      || filters.authority !== "all"
      || filters.dateFrom
      || filters.dateTo
    ) {
      return false;
    }
    const text = [
      finding.anomaly_type,
      finding.severity,
      finding.summary,
      ...(finding.departments || []),
      ...(finding.records || []),
    ].join(" ").toLowerCase();
    return !filters.query || text.includes(filters.query);
  };

  const sortRecords = (records, mode) => [...records].sort((left, right) => {
    if (mode === "oldest") {
      return recordDate(left).localeCompare(recordDate(right));
    }
    if (mode === "department") {
      return scopeLabel(left.department).localeCompare(scopeLabel(right.department))
        || left.title.localeCompare(right.title);
    }
    if (mode === "priority") {
      return (PRIORITY_ORDER[left.priority] ?? 99)
        - (PRIORITY_ORDER[right.priority] ?? 99)
        || left.title.localeCompare(right.title);
    }
    return recordDate(right).localeCompare(recordDate(left));
  });

  const badge = (value, extraClass = "") => (
    `<span class="di-badge ${escape(extraClass)}">${escape(value)}</span>`
  );

  const recordCard = (record) => {
    const warnings = (record.warnings || []).map((warning) => (
      `<li>${escape(warning)}</li>`
    )).join("");
    const date = recordDate(record);
    const path = record.source_section
      ? `${record.source_path} · ${record.source_section}`
      : record.source_path;

    return `
      <article class="di-card" data-record-id="${escape(record.id)}">
        <div class="di-card-top">
          <div>
            <div class="di-kicker">
              ${escape(scopeLabel(record.department))} · ${escape(record.subtype)}
            </div>
            <div class="di-title">${escape(record.title)}</div>
          </div>
          <div class="di-badges">
            ${badge(record.state, `state-${record.state}`)}
            ${badge(record.priority, `priority-${record.priority}`)}
          </div>
        </div>
        <p class="di-summary">${escape(record.summary || "No summary available.")}</p>
        <div class="di-record-meta">
          <span>${escape(record.record_type)}</span>
          <span>${escape(record.source_authority)}</span>
          <span>${escape(record.parse_confidence)} confidence</span>
          ${date ? `<span>${escape(date)}</span>` : ""}
          ${(record.warnings || []).length
            ? `<span class="di-warning-count">${record.warnings.length} warning${record.warnings.length === 1 ? "" : "s"}</span>`
            : ""}
        </div>
        <div class="di-source-path">${escape(path)}</div>
        <details class="di-details">
          <summary>Inspect source record</summary>
          ${warnings ? `<ul class="di-warning-list">${warnings}</ul>` : ""}
          <pre>${escape(record.raw_text || "No raw source fragment available.")}</pre>
        </details>
      </article>
    `;
  };

  const findingCard = (finding) => `
    <article class="di-card di-finding-card severity-${escape(finding.severity)}">
      <div class="di-card-top">
        <div>
          <div class="di-kicker">
            ${escape((finding.departments || []).map(scopeLabel).join(" · ") || "System")}
          </div>
          <div class="di-title">${escape(finding.anomaly_type.replaceAll("_", " "))}</div>
        </div>
        <div class="di-badges">${badge(finding.severity, `severity-${finding.severity}`)}</div>
      </div>
      <p class="di-summary">${escape(finding.summary)}</p>
      <details class="di-details">
        <summary>Related normalized records</summary>
        <pre>${escape((finding.records || []).join("\n"))}</pre>
      </details>
    </article>
  `;

  const renderSection = (id, items, renderer, emptyMessage) => {
    const section = byId(`${id}-section`);
    const container = byId(id);
    byId(`${id}-count`).textContent = String(items.length);
    container.innerHTML = items.map(renderer).join("")
      || `<div class="di-empty">${escape(emptyMessage)}</div>`;
    section.hidden = items.length === 0;
  };

  const renderSummary = (visibleRecords, visibleFindings) => {
    const total = inspection.summary || {};
    byId("di-total-records").textContent = total.records ?? inspection.records.length;
    byId("di-total-findings").textContent = total.findings ?? inspection.findings.length;
    byId("di-total-warnings").textContent = total.warnings ?? 0;
    byId("di-visible-count").textContent = (
      `${visibleRecords.length} records · ${visibleFindings.length} findings visible`
    );
    byId("di-status").textContent = inspection.available ? "Live repository" : "Unavailable";
  };

  const render = () => {
    const filters = filterState();
    const records = sortRecords(
      inspection.records.filter((record) => matchesRecord(record, filters)),
      filters.sort,
    );
    const findings = inspection.findings.filter(
      (finding) => matchesFinding(finding, filters),
    );

    const work = records.filter((record) => recordCategory(record) === "work");
    const knowledge = records.filter(
      (record) => recordCategory(record) === "knowledge",
    );
    const operations = records.filter(
      (record) => recordCategory(record) === "operations",
    );

    renderSummary(records, findings);
    renderSection("di-work", work, recordCard, "No work records match these filters.");
    renderSection(
      "di-knowledge",
      knowledge,
      recordCard,
      "No knowledge records match these filters.",
    );
    renderSection(
      "di-operations",
      operations,
      recordCard,
      "No operations records match these filters.",
    );
    renderSection(
      "di-findings",
      findings,
      findingCard,
      "No findings match these filters.",
    );

    const noResults = !records.length && !findings.length;
    byId("di-no-results").hidden = !noResults;
  };

  const populateScopes = () => {
    const select = byId("di-filter-department");
    const current = select.value;
    select.innerHTML = [
      '<option value="all">All departments and System</option>',
      ...inspection.scopes.map((scope) => (
        `<option value="${escape(scope.id)}">${escape(scope.label)}</option>`
      )),
    ].join("");
    select.value = inspection.scopes.some((scope) => scope.id === current)
      ? current
      : "all";
  };

  const loadInspection = async () => {
    if (loading) return loading;
    byId("di-status").textContent = "Loading";
    byId("di-error").hidden = true;

    loading = fetch("/api/department-inspection", {cache: "no-store"})
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Department Inspection API returned ${response.status}.`);
        }
        return response.json();
      })
      .then((payload) => {
        inspection = payload;
        populateScopes();
        render();
      })
      .catch((error) => {
        console.error(error);
        byId("di-status").textContent = "Error";
        byId("di-error").textContent = error.message || "Inspection failed.";
        byId("di-error").hidden = false;
      })
      .finally(() => {
        loading = null;
      });
    return loading;
  };

  const resetFilters = () => {
    byId("di-filter-department").value = "all";
    byId("di-filter-category").value = "all";
    byId("di-filter-type").value = "all";
    byId("di-filter-state").value = "all";
    byId("di-filter-priority").value = "all";
    byId("di-filter-date-from").value = "";
    byId("di-filter-date-to").value = "";
    byId("di-filter-cross").value = "all";
    byId("di-filter-authority").value = "all";
    byId("di-filter-warnings").checked = false;
    byId("di-filter-search").value = "";
    byId("di-filter-sort").value = "newest";
    render();
  };

  [
    "di-filter-department",
    "di-filter-category",
    "di-filter-type",
    "di-filter-state",
    "di-filter-priority",
    "di-filter-date-from",
    "di-filter-date-to",
    "di-filter-cross",
    "di-filter-authority",
    "di-filter-warnings",
    "di-filter-search",
    "di-filter-sort",
  ].forEach((id) => {
    byId(id).addEventListener("input", render);
    byId(id).addEventListener("change", render);
  });

  byId("di-reset").addEventListener("click", resetFilters);
  document.querySelector('[data-tab-target="departments"]').addEventListener(
    "click",
    loadInspection,
  );
  window.addEventListener("lifeos:dashboard-refreshed", loadInspection);
})();
