# Session Handoff

Updated: 2026-07-10
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with GitHub as durable memory map, Drive as working records cabinet, Todoist as Rob-facing action queue, Calendar as timed commitments, Gmail as communication evidence, project chats as knowledge producers, workers as narrow operational executors, and Life Logistics HQ as cross-project curator.

The immediate Life OS business priority is Office Leaks Consulting: a revenue-first business-unit HQ under Chief Business HQ focused on service-business systems consulting, local office leak cleanup, workflow organization, documentation, process cleanup, and trust-based delivery for local service businesses.

Office Leaks grew out of the former Virtual Assistant Business worker project but is no longer merely a generic VA concept. It now has its own HQ folder:

- `projects/office-leaks-consulting/`

Legacy VA folder:

- `projects/virtual-assistant-business/` now exists as historical/redirect context unless Rob later authorizes archival cleanup.

PennyOS / Penny Platform is paused, not abandoned. It remains a longer-term platform/productization path and may be informed by Office Leaks service work and market learning.

## Current Active Core

- Life Logistics HQ
- Main Assistant / Daily Operations
- Chief of Finance Penny
- Chief Business HQ
- Office Leaks Consulting HQ
- Chief Engineering Penny
- Chief Wellness HQ
- Life OS Infrastructure as needed

## Worker Layer

Life OS now has a formal worker layer separate from departments and HQs.

Worker root:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`

First worker:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Mutable pointer / operational handoff: `workers/penny-raw-capture/SESSION_HANDOFF.md`

Worker mission:

> Capture first. Organize later.

The Penny Raw Capture Worker appends Rob's raw ideas, reminders, observations, facts, questions, resources, contacts, and other intake to the canonical Google Sheet `Life OS Raw Capture Inbox`.

Main Assistant Penny is the downstream owner for later processing of rows where `Processed = No`.

Workers do not automatically read the full department boot. They load the shared worker standard, their worker-specific boot contract, and their handoff only when mutable pointers or current operational notes are needed.

## Consolidated / Dormant Departments

- Work Search is consolidated into Main Assistant for current lightweight logistics and reminders.
- Support Pathway is consolidated into Main Assistant for current lightweight research and logistics.
- Daily Anchors / Recovery Logistics is dormant until Rob reactivates it.
- Philosophy HQ is dormant until Rob reactivates it.

Preserve project history. Do not delete department files.

## Current Durable Architecture

- Active Projects is the authoritative current project map: `memory/04_ACTIVE_PROJECTS.md`.
- Open Loops tracks current unfinished work: `memory/05_OPEN_LOOPS.md`.
- Worker registry: `workers/README.md`.
- Shared worker standard: `workers/WORKER_STANDARD.md`.
- Advisory dashboard: `coordination/ADVISORY_INDEX.md`.
- Advisory details: `coordination/boards/`.
- Department Event Inbox: `coordination/DEPARTMENT_EVENT_INBOX.md` is frozen historical record only.
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`.
- Pending Advisory Boards standard: `coordination/PENDING_ADVISORY_BOARDS.md`.
- Department Notebooks standard: `coordination/DEPARTMENT_NOTEBOOKS.md`.
- Source-of-Truth and Publication Standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`.
- Connector Reliability Operating Pattern: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`.
- Design Principles: `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`.

## Current Advisory Rule

Advisories live on the source department's board.

The target department is named inside the advisory and routed through the Advisory Index.

The Advisory Index is the sole active routing dashboard. It should show open advisory ID, source board path, and target department.

Do not update Department Event Inbox for normal advisory routing unless Rob explicitly reactivates it.

Template language uses `Posted Board` and `Target Department` rather than ambiguous `Target Board` language.

## Current Decision Rules

Decision Rules are reusable decision procedures.

Central registry:

- `coordination/DECISION_RULES_REGISTRY.md`

Active first rule:

- DR-FIN-20260704-001 — Discretionary Purchase Pause Rule, owned by Chief of Finance Penny.

## Current Open Advisory State

No open advisories are currently listed in the Advisory Index.

Recently implemented / acknowledged:

- ADV-20260709-030 — Implemented by Life Logistics; formal worker layer, worker standard, Penny Raw Capture Worker package, canonical Sheet pointer, and boot routing created.
- ADV-20260709-029 — Closed / Implemented Through ADV-20260709-030; Engineering completed the architecture and Life Logistics implemented the resulting worker package. No separate work remains.
- 2026-07-09: Office Leaks Consulting elevated to business-unit HQ under Chief Business HQ.
- ADV-20260708-028 — Implemented by Life Logistics; Office Leaks finance working records synced across Life OS.
- ADV-20260708-027 — Implemented by Life Logistics; Engineering Office Leaks architecture updates synced across Life OS.
- ADV-20260708-026 — Closed / Fully Acknowledged; Office Leaks operating philosophy reviewed by all target departments.
- ADV-20260707-025 — Acknowledged by Engineering; delivery playbook request for bite-sized local service office cleanup offers.
- ADV-20260707-024 — Business HQ parent-state refreshed for VA Business priority.
- ADV-20260707-023 — Finance state refreshed for Virtual Assistant income stream.
- ADV-20260707-021 — Virtual Assistant Business scaffold created as Business HQ sub-project.

## Office Leaks Operating Philosophy

Office Leaks Consulting is a practical, trust-based systems consulting lane for small local service businesses.

Core philosophy:

- Respect the people. Fix the process.
- Good people deserve good systems.
- The tool is not the product. The habit is the product.
- No shame. No blame. Fix the system.

Life Logistics should keep Office Leaks visible as an active income-stream candidate with possible near-term real-world logistics: discovery visits, transportation, follow-up reminders, outreach loops, document organization, and conversion of plans into calendar/task actions when Rob authorizes.

## Office Leaks Architecture / Finance Pointers

Office Leaks HQ:

- `projects/office-leaks-consulting/`

Engineering delivery architecture:

- Human-system delivery layer note: `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Related Drive doc: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Finance working-record pointer:

- `projects/finance-benefits/OFFICE_LEAKS_FINANCE_POINTERS.md`

Keep GitHub abstract. Detailed financial models, pricing notes, startup costs, revenue tracking, and tax set-aside planning live in Drive through the Finance pointer file.

## Best Next Actions

- For Penny Raw Capture Worker: begin pilot use and confirm append/verification behavior in actual capture requests.
- For Main Assistant: process raw inbox rows only when Rob authorizes or requests review.
- For Office Leaks Consulting HQ: develop local-service-business positioning, offers, lead-leak materials, proposal/portfolio packet, outreach path, and repeatable delivery method.
- For Business: guide parent strategy and decide later whether Office Leaks should remain a Business HQ department or grow into a separate top-level business division.
- For Engineering: continue delivery-playbook architecture and worker reliability support as needed.
- For Finance: use the Office Leaks finance working records for pricing, startup costs, tool decisions, revenue tracking, and tax set-aside planning once concrete.
- For Main Assistant: support daily execution, reminders, scheduling, outreach loops, lightweight logistics, and authorized raw-inbox processing.
- For Life Logistics: keep advisory routing, worker routing, and Office Leaks logistics visible and clean.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Calendar owns time. Todoist owns Rob-facing actions. Gmail owns communications. Workers execute narrow contracts. Captain's Log records meaningful operational sessions.

Use RPR when reliable structured-file editing matters more than connector automation.
