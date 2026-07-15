# Session Handoff

Updated: 2026-07-15
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

Life OS has a formal worker layer separate from departments and HQs.

Worker root:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`

Active pilot workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Raw Capture Worker handoff: `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`
- Penny Inventory Worker handoff: `workers/penny-inventory/SESSION_HANDOFF.md`

Penny Raw Capture Worker mission:

> Capture first. Organize later.

It appends raw intake to the canonical Google Sheet `Life OS Raw Capture Inbox`. Main Assistant owns later processing of rows where `Processed = No`.

Penny Inventory Worker mission:

> See the item. Record the item. Verify the row.

It converts sale-item photographs uploaded directly into chat into one verified row per item in the canonical Google Sheet `For Sale Inventory`.

The Inventory Worker does not automatically price, bundle, group, write listings, publish Marketplace posts, or make sale-strategy decisions.

Workers do not automatically read the full department boot. They load the shared worker standard, their worker-specific boot contract, and their handoff only when mutable pointers or current operational notes are needed.

## Consolidated / Dormant Departments

- Work Search is consolidated into Main Assistant for current lightweight logistics and reminders.
- Support Pathway is consolidated into Main Assistant for current lightweight research and logistics.
- Daily Anchors / Recovery Logistics is dormant until Rob reactivates it.
- Philosophy HQ is dormant until Rob reactivates it.

Preserve project history. Do not delete department files.

## Current Durable Architecture

- Active Projects: `memory/04_ACTIVE_PROJECTS.md`.
- Open Loops: `memory/05_OPEN_LOOPS.md`.
- Worker registry: `workers/README.md`.
- Shared worker standard: `workers/WORKER_STANDARD.md`.
- Advisory dashboard: `coordination/ADVISORY_INDEX.md`.
- Advisory details: `coordination/boards/`.
- Advisory Board Lifecycle Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`.
- Initial high-use board review: `coordination/ADVISORY_BOARD_REVIEW_2026-07-10.md`.
- Department Event Inbox: `coordination/DEPARTMENT_EVENT_INBOX.md` is frozen historical record only.
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`.
- Pending Advisory Boards standard: `coordination/PENDING_ADVISORY_BOARDS.md`.
- Department Notebooks standard: `coordination/DEPARTMENT_NOTEBOOKS.md`.
- Source-of-Truth and Publication Standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`.
- Connector Reliability Operating Pattern: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`.
- Context Reminder and response shortcuts: `memory/CONTEXT_REMINDER.md`.
- Local prompt-launcher database: `engineering/classroom/prompt_launcher/prompt_library.json`.
- Design Principles: `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`.

## Active Shortcut Set

The current response/operations shortcut set is defined in `memory/CONTEXT_REMINDER.md` and includes response-style commands, `/BOOT`, advisory commands, `/ITINERARY`, `/TODOIST`, `/MORNING`, `/NIGHTLY`, `/OPENLOOPS`, `/CAPTURE`, `/DRIVE`, `/CALENDAR`, and `/GMAIL`.

Connector-specific shortcuts deliberately include `@GitHub`, `@Todoist`, `@Google Calendar`, `@Google Drive`, or `@Gmail` so the intended connector is active in the launched chat.

## Current Advisory Rule

Advisories live on the source department's board.

The target department is named inside the advisory and routed through the Advisory Index.

The Advisory Index is the sole active routing dashboard.

Operational boards follow `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md` and keep all open advisories plus a bounded recent completed working set.

Git history is the default archive for completed advisory text removed during justified compaction.

Do not update Department Event Inbox for normal advisory routing unless Rob explicitly reactivates it.

## Current Decision Rules

Decision Rules are reusable decision procedures.

Central registry:

- `coordination/DECISION_RULES_REGISTRY.md`

Active first rule:

- DR-FIN-20260704-001 — Discretionary Purchase Pause Rule, owned by Chief of Finance Penny.

## Current Open Advisory State

As of 2026-07-15, the Advisory Index contains one open Engineering advisory:

- ADV-20260715-036 — Open; Engineering prompt package for seven LifeOS discussion HQs.

Recently implemented / acknowledged:

- ADV-20260715-035 — Implemented / Acknowledged / Closed; Engineering verified and integrated the friction-aware Daily Operating SOP into the global boot flow.

Recently implemented / acknowledged:

- ADV-20260714-034 — Implemented / Acknowledged / Closed; expanded connector-tagged shortcut set ingested, canonical vocabulary preserved in `memory/CONTEXT_REMINDER.md`, and no duplicate definitions found.
- ADV-20260713-033 — Implemented / Acknowledged / Closed; Life Logistics ingested the `/BOOT`, `/ADVISE`, `/ADVISORY`, and `/SYNCADVISORY` shortcut rollout.
- ADV-20260710-032 — Implemented / Acknowledged / Closed; Penny Inventory Worker package created, canonical resource verified, and worker routing updated.
- ADV-20260710-031 — Implemented / Closed; Advisory Board Lifecycle Standard created, high-use boards reviewed, and Engineering board compacted.
- ADV-20260709-030 — Implemented by Life Logistics; formal worker layer, worker standard, Penny Raw Capture Worker package, canonical Sheet pointer, and boot routing created.
- ADV-20260709-029 — Closed / Implemented Through ADV-20260709-030; no separate work remains.
- 2026-07-09: Office Leaks Consulting elevated to business-unit HQ under Chief Business HQ.
- ADV-20260708-028 — Implemented by Life Logistics; Office Leaks finance working records synced across Life OS.
- ADV-20260708-027 — Implemented by Life Logistics; Engineering Office Leaks architecture updates synced across Life OS.
- ADV-20260708-026 — Closed / Fully Acknowledged; Office Leaks operating philosophy reviewed by all target departments.

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

- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Drive doc: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Finance working-record pointer:

- `projects/finance-benefits/OFFICE_LEAKS_FINANCE_POINTERS.md`

Keep GitHub abstract. Detailed financial models, pricing notes, startup costs, revenue tracking, and tax set-aside planning live in Drive through the Finance pointer file.

## Best Next Actions

- Pilot Penny Raw Capture Worker with real intake and verified writes.
- Pilot Penny Inventory Worker with real uploaded sale-item photographs and verified one-row-per-item writes.
- Keep pricing, grouping, listing copy, and publication separate from inventory capture.
- Process raw inbox rows only when Rob authorizes or requests review.
- Continue Office Leaks positioning, offers, outreach, and delivery-method work.
- Maintain advisory-board hygiene without turning compaction into recurring bureaucracy.
- Keep the Engineering HQ Daily Sync paused pending additional scheduling/execution architecture.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Calendar owns time. Todoist owns Rob-facing actions. Gmail owns communications. Workers execute narrow contracts. Captain's Log records meaningful operational sessions.

Use RPR when reliable structured-file editing matters more than connector automation.
