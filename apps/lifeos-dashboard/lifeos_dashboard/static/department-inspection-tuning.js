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
    "main-assistant": "Main Assistant HQ",
    logistics: "Logistics HQ",
    engineering: "Engineering HQ",
    business: "Business HQ",
    "office-leaks": "Office Leaks HQ",
    finance: "Finance HQ",
    wellness: "Wellness HQ",
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

  const findings = document.getElementById("di-findings");
  if (findings) {
    new MutationObserver(enhanceFindingDetails).observe(findings, {
      childList: true,
      subtree: true,
    });
  }

  document.querySelector('[data-tab-target="departments"]')?.addEventListener(
    "click",
    enhanceFindingDetails,
  );
  window.addEventListener("lifeos:dashboard-refreshed", () => {
    recordMapPromise = null;
    enhanceFindingDetails();
  });
})();
