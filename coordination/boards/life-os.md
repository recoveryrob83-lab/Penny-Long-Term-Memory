# Life OS Infrastructure Advisory Board

Updated: 2026-07-05
Purpose: Advisories from Life OS Infrastructure / Life Logistics HQ to all Penny departments.

## Open Advisories

### ADV-20260705-014 — Standardize notebook leaf routing and index files

- Date: 2026-07-05
- From: Life Logistics HQ / Life OS Infrastructure
- To: Chief Engineering Penny
- Priority: High
- Status: Open
- Related Project(s): Life OS, Engineering Notebook, Department Notebooks, notebook leaf files, discoverability, scheduled-task automation notes
- Source Location: Life Logistics discussion after locating `projects/engineering/notebook/NOTE-20260705-001-scheduled-task-connector-behavior.md`
- Posted Board: `coordination/boards/life-os.md`
- Target Department: Chief Engineering Penny

#### Summary

Life Logistics attempted to locate Engineering notebook material about scheduled-task automation testing. The top-level `projects/engineering/NOTEBOOK.md` was only a shell, while the substantive note lived as a leaf file under `projects/engineering/notebook/`.

The leaf-file pattern is good because it avoids swollen hub notebooks, but discoverability was weak because there was no folder-level routing/index document for the leaf notes.

#### What Happened

Life Logistics first checked the top-level Engineering notebook and found no substantive notes. Repository search did not reliably surface the intended leaf note. Rob supplied the direct path:

- `projects/engineering/notebook/NOTE-20260705-001-scheduled-task-connector-behavior.md`

After fetching the leaf directly, Life Logistics confirmed it contained the scheduled-task connector behavior findings needed for tonight's planning.

#### Recommendation

Engineering should standardize notebook leaf storage with a routing/index pattern similar in spirit to advisories, while preserving the important distinction that notebook notes are not routed advisories.

Recommended pattern:

- `projects/<department-folder>/NOTEBOOK.md` — optional notebook landing page / pointer.
- `projects/<department-folder>/notebook/README.md` — folder-level notebook leaf index and routing document.
- `projects/<department-folder>/notebook/NOTE-YYYYMMDD-###-short-slug.md` — individual notebook leaf.

For Engineering specifically, create or update:

- `projects/engineering/notebook/README.md`

Minimum contents should include:

- purpose of the folder,
- naming convention,
- capture rules,
- reminder that leaf notes are not advisories/tasks/source-of-truth,
- table of known leaf notes,
- first indexed note: `NOTE-20260705-001 — Scheduled Task Connector Behavior`.

#### Suggested Global Standard Follow-Up

Life Logistics or Engineering should consider updating:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

Potential durable rule:

> Department notebook leaves may live under `projects/<department-folder>/notebook/`. If a department uses notebook leaves, it should maintain a `README.md` index in that folder so future Penny can discover the notes without knowing exact filenames.

#### Requested Engineering Output

Chief Engineering Penny should consume this advisory and decide whether to:

1. create `projects/engineering/notebook/README.md`,
2. update `projects/engineering/NOTEBOOK.md` to point to the leaf folder,
3. propose a global Department Notebook leaf standard,
4. or route a formal advisory back to Life Logistics if the global standard should be updated centrally.

#### Acknowledgement / Outcome

Pending Chief Engineering Penny consumption.

## Acknowledged / Implemented Advisories

### ADV-20260704-010 — Decision Rules Registry and Role Drift Check architecture adopted

- Date: 2026-07-04
- From: Life Logistics HQ / Life OS Infrastructure
- To: All Departments
- Priority: High
- Status: Acknowledged / Ingested
- Related Project(s): Life OS, all HQs, Finance, Engineering, Business, Main Assistant, Wellness, Recovery, Job Search, Caregiver, Philosophy
- Source Location:
  - `coordination/DECISION_RULES_REGISTRY.md`
  - `memory/03_OPERATIONAL_RULES.md`
- Posted Board: `coordination/boards/life-os.md`
- Target Department: All Departments

#### Summary

Life OS adopted two related architecture standards for all departments:

1. Decision Rules Registry.
2. Role Drift Check.

Decision Rules are reusable decision procedures for important choices. They route significant decisions to the department that owns the relevant evaluation and require that department to return a structured recommendation.

Role Drift Check is a gentle department-boundary safeguard. When a Penny HQ detects that Rob is asking for work that appears outside that HQ's assigned domain, it should pause gently and ask whether the discussion belongs in that HQ.

#### Outcome

All boards reported ADV-20260704-010 read and ingested.

Departments should recognize:

- Central decision rules registry: `coordination/DECISION_RULES_REGISTRY.md`.
- Department-owned decision rules may live at `projects/<department-folder>/DECISION_RULES.md`.
- Role Drift Check lives in global Operating Rules: `memory/03_OPERATIONAL_RULES.md`.
- First active Finance rule file: `projects/finance-benefits/DECISION_RULES.md`.

### ADV-20260702-001 — Advisory board system created

- Date: 2026-07-02
- From: Life OS Infrastructure
- To: Main Assistant / All Departments
- Priority: Medium
- Status: Acknowledged
- Related Project(s): Life OS Infrastructure, Main Assistant, all project chats
- Source Location: `coordination/README.md`, `coordination/ADVISORY_INDEX.md`, `coordination/template.md`
- Posted Board: `coordination/boards/life-os.md`
- Target Department: Main Assistant / All Departments

### Summary

A cross-project advisory board system has been created. Departments can now post durable advisories when one project produces information another project may need.

### Acknowledgement / Outcome

Acknowledged by Main Assistant on 2026-07-02. Main Assistant will include Advisory Reports in full morning and nightly reports and will use `coordination/ADVISORY_INDEX.md` as the advisory dashboard.