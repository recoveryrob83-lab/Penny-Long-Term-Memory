# Engineering Advisory Board

Updated: 2026-07-06
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

### ADV-20260706-020 — Adopt Finances-only session rule

- Date: 2026-07-06
- From: Chief Engineering Penny
- To: Life Logistics HQ / Life OS Infrastructure
- Priority: High
- Status: Acknowledged / Implemented
- Related Project(s): Life OS, Finance HQ, Finances connector, connector reliability, session isolation
- Source Location: Engineering HQ chat / connector sandbox report
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ / Life OS Infrastructure

#### Summary

Engineering consumed ADV-20260706-019 from Finance and reviewed Rob's connector sandbox report.

Current evidence supports treating Finances as a special high-sensitivity connector that may isolate or narrow the active connector environment during a financial session.

#### Outcome

Life Logistics adopted the Finances-only session rule as an observed operating pattern, not a confirmed claim about platform internals.

Updated files include:

- `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`
- `memory/03_OPERATIONAL_RULES.md`
- `projects/finance-benefits/SESSION_HANDOFF.md`

Adopted rule:

Finances connector work should occur in a dedicated Finance-only chat/session. Do not mix Finances/Plaid-style operations with GitHub, Drive, Gmail, Instacart, or other connector workflows in the same active session. After Finances is invoked, do not assume other connectors remain available.

No financial account names, balances, transactions, credentials, Plaid details, benefit identifiers, or financial documents should be recorded in GitHub.

### ADV-20260706-018 — Simplify the Life OS Advisory Routing System

- Date: 2026-07-06
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Acknowledged / Implemented
- Related Project(s): Life OS, advisory routing, connector reliability, scheduled workers, operating standards
- Source Location: Engineering HQ chat / Rob handoff
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ

#### Summary

Engineering recommended reviewing the current advisory routing architecture because the prior system required duplicate writes to source board, Advisory Index, and Department Event Inbox.

#### Outcome

Life Logistics accepted the recommendation and simplified advisory routing.

New active routing architecture:

- Source department board: canonical advisory text.
- Advisory Index: sole active routing dashboard.

Department Event Inbox is now frozen as a historical synchronization/read/ingestion register and should not be updated for normal advisory routing unless Rob explicitly reactivates it.

Updated files include:

- `memory/03_OPERATIONAL_RULES.md`
- `memory/STARTUP_BOOT.md`
- `coordination/README.md`
- `coordination/template.md`
- `coordination/ADVISORY_INDEX.md`
- `coordination/DEPARTMENT_EVENT_INBOX.md`

Decision: use fewer connector writes and reduce advisory routing fragility.

### ADV-20260706-017 — Adopt connector reliability operating pattern from Gemini/Drive tests

- Date: 2026-07-06
- From: Chief Engineering Penny
- To: Life Logistics HQ / Life OS Infrastructure
- Priority: High
- Status: Acknowledged / Implemented
- Related Project(s): Life OS, Reliable Connector Execution Layer, Google Drive workflows, Gemini worker evaluation, scheduled workers, boot reliability
- Source Location: Engineering HQ chat
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ / Life OS Infrastructure

#### Summary

Engineering and Rob completed a small but useful connector-reliability test sequence involving Gemini, Google Drive, GitHub, and explicit connector invocation.

#### Outcome

Life Logistics created `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` as the durable operating note for explicit connector invocation, small verified writes, waiting after safety triggers, Gemini-as-optional-Drive-artifact-generator, and verification of generated artifacts.

Decision: Gemini is an optional fallback or companion for selected Google Workspace artifact generation, not a default Life OS dependency and not a complete in-place Drive record maintainer.

### ADV-20260705-015 — Globalize department notebook leaf routing/index standard

- Date: 2026-07-05
- From: Chief Engineering Penny
- To: Life Logistics HQ / Life OS Infrastructure
- Priority: High
- Status: Acknowledged / Implemented
- Related Project(s): Life OS, Department Notebooks, notebook leaf files, scheduled-task sync workers, discoverability
- Source Location: Engineering consumption of ADV-20260705-014
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ / Life OS Infrastructure

#### Summary

Engineering consumed ADV-20260705-014, created `projects/engineering/notebook/README.md`, updated `projects/engineering/NOTEBOOK.md`, and recommended globalizing the notebook leaf/index pattern.

#### Outcome

Life Logistics updated `coordination/DEPARTMENT_NOTEBOOKS.md` to adopt notebook leaf folders, `notebook/README.md` leaf indexes, leaf-note naming/format guidance, and scheduled-worker guidance to read notebook indexes before leaf notes when notebook review is requested.

Decision: do not create empty notebook indexes across every department by default. Create them when useful or when a department begins using notebook leaves.

### ADV-20260704-013 — Tighten advisory posting board rules

- Date: 2026-07-04
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Acknowledged / Ingested
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ

Life Logistics clarified that advisories live on the source department's board and target department is routed through Index/Event Inbox.

### ADV-20260704-012 — Connector safety-trigger avoidance rules needed

- Date: 2026-07-04
- From: Life Logistics HQ
- To: Chief Engineering Penny
- Priority: High
- Status: Acknowledged / Ingested
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Chief Engineering Penny

Engineering will incorporate connector safety-trigger avoidance into the Reliable Connector Execution Layer.