(() => {
  const style = document.createElement("style");
  style.textContent = `
    .di-record-list {
      max-height: min(76vh, 920px);
      overflow-y: auto;
      overscroll-behavior: contain;
      padding-right: 6px;
      scrollbar-gutter: stable;
    }

    .di-record-list::-webkit-scrollbar {
      width: 10px;
    }

    .di-record-list::-webkit-scrollbar-thumb {
      border: 2px solid transparent;
      border-radius: 999px;
      background: rgba(141, 212, 255, 0.28);
      background-clip: padding-box;
    }

    .di-related-record {
      display: block;
      margin-bottom: 10px;
      white-space: pre-wrap;
    }

    #di-filter-warnings {
      display: none;
    }
  `;
  document.head.appendChild(style);

  let recordMapPromise = null;

  const loadRecordMap = () => {
    if (!recordMapPromise) {
      recordMapPromise = fetch("/api/department-inspection", {cache: "no-store"})
        .then((response) => {
          if (!response.ok) throw new Error(`Inspection API returned ${response.status}.`);
          return response.json();
        })
        .then((payload) => new Map(
          (payload.records || []).map((record) => [record.id, record]),
        ))
        .catch((error) => {
          console.error("Unable to enrich Department Inspection findings.", error);
          return new Map();
        });
    }
    return recordMapPromise;
  };

  const labelByDepartment = {
    "main-assistant": "Chief_of_Staff_HQ",
    logistics: "Maintenance_HQ",
    engineering: "Engineering_HQ",
    business: "Business_HQ",
    "office-leaks": "Office_Leaks_HQ",
    finance: "Finance_HQ",
    wellness: "Wellness_HQ",
    system: "System",
  };

  const enhanceFindingDetails = async () => {
    const map = await loadRecordMap();
    document.querySelectorAll("#di-findings details pre:not([data-enriched])").forEach((pre) => {
      const ids = pre.textContent.split("\n").map((value) => value.trim()).filter(Boolean);
      const lines = ids.map((id) => {
        const record = map.get(id);
        if (!record) return id;
        const department = labelByDepartment[record.department] || record.department;
        const source = record.source_section
          ? `${record.source_path} · ${record.source_section}`
          : record.source_path;
        return `${department} · ${record.title}\n${record.state} · ${record.source_authority}\n${source}`;
      });
      pre.textContent = lines.join("\n\n");
      pre.dataset.enriched = "true";
    });
  };

  const warningCheckbox = document.getElementById("di-filter-warnings");
  const warningLabel = warningCheckbox?.closest("label");
  const filterGrid = document.querySelector(".di-filter-grid");
  let warningSelect = null;

  const visibleCards = (container) => Array.from(
    container?.querySelectorAll(":scope > .di-card") || [],
  ).filter((card) => !card.hidden);

  const applyWarningStatus = () => {
    if (!warningSelect) return;
    const mode = warningSelect.value;

    ["di-work", "di-knowledge", "di-operations"].forEach((id) => {
      const container = document.getElementById(id);
      const section = document.getElementById(`${id}-section`);
      const count = document.getElementById(`${id}-count`);

      Array.from(container?.querySelectorAll(":scope > .di-card") || []).forEach((card) => {
        const hasWarning = Boolean(card.querySelector(".di-warning-count"));
        card.hidden = mode === "without" && hasWarning;
      });

      const visible = visibleCards(container).length;
      if (count) count.textContent = String(visible);
      if (section) section.hidden = visible === 0;
    });

    const findingsSection = document.getElementById("di-findings-section");
    if (findingsSection && mode !== "all") findingsSection.hidden = true;

    const visibleRecords = ["di-work", "di-knowledge", "di-operations"]
      .reduce((total, id) => total + visibleCards(document.getElementById(id)).length, 0);
    const visibleFindings = mode === "all"
      ? visibleCards(document.getElementById("di-findings")).length
      : 0;

    const visibleCount = document.getElementById("di-visible-count");
    if (visibleCount) {
      visibleCount.textContent = `${visibleRecords} records · ${visibleFindings} findings visible`;
    }

    const noResults = document.getElementById("di-no-results");
    if (noResults) noResults.hidden = visibleRecords + visibleFindings > 0;
  };

  if (warningCheckbox && warningLabel && filterGrid) {
    warningSelect = document.createElement("select");
    warningSelect.id = "di-filter-warning-status";
    warningSelect.innerHTML = [
      '<option value="all">All records</option>',
      '<option value="with">With warnings</option>',
      '<option value="without">Without warnings</option>',
    ].join("");

    warningLabel.className = "di-filter-field";
    warningLabel.replaceChildren(
      document.createTextNode("Warning status"),
      warningSelect,
      warningCheckbox,
    );

    const searchField = filterGrid.querySelector(".di-filter-wide");
    filterGrid.insertBefore(warningLabel, searchField || null);

    warningSelect.addEventListener("change", () => {
      warningCheckbox.checked = warningSelect.value === "with";
      warningCheckbox.dispatchEvent(new Event("change", {bubbles: true}));
      requestAnimationFrame(applyWarningStatus);
    });

    document.getElementById("di-reset")?.addEventListener("click", () => {
      warningSelect.value = "all";
      warningCheckbox.checked = false;
      requestAnimationFrame(applyWarningStatus);
    });
  }

  const findings = document.getElementById("di-findings");
  if (findings) {
    new MutationObserver(enhanceFindingDetails).observe(findings, {
      childList: true,
      subtree: true,
    });
  }

  const recordLists = document.querySelector(".di-category-stack");
  if (recordLists) {
    new MutationObserver(() => requestAnimationFrame(applyWarningStatus)).observe(
      recordLists,
      {childList: true, subtree: true},
    );
  }

  document.querySelector('[data-tab-target="departments"]')?.addEventListener(
    "click",
    () => {
      enhanceFindingDetails();
      requestAnimationFrame(applyWarningStatus);
    },
  );
  window.addEventListener("lifeos:dashboard-refreshed", () => {
    recordMapPromise = null;
    enhanceFindingDetails();
    requestAnimationFrame(applyWarningStatus);
  });
})();
