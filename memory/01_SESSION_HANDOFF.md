# Session Handoff

Updated: 2026-07-15
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet;
- Todoist as Rob-facing task management;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- project chats as domain knowledge producers;
- workers as narrow operational executors;
- Main Assistant as daily coordinator and primary conversational hub;
- Life Logistics HQ as shared-infrastructure curator and cross-project housekeeper.

The immediate business priority is Office Leaks Consulting, a revenue-first business-unit HQ under Chief Business HQ focused on service-business systems consulting, local office leak cleanup, workflow organization, documentation, process cleanup, and trust-based delivery for local service businesses.

Office Leaks grew out of the former Virtual Assistant Business project. The legacy folder remains historical redirect context:

- Active HQ: `projects/office-leaks-consulting/`
- Legacy context: `projects/virtual-assistant-business/`

PennyOS / Penny Platform is paused, not abandoned. It remains a longer-term productization path informed by Life OS operations and Office Leaks market learning.

## Chat HQ Operating Architecture

As of 2026-07-15, all seven LifeOS department discussion HQ chats are open and ready, while the Main Assistant hub is the primary conversational front door.

These HQs are regular ChatGPT discussion rooms for:

- planning and natural conversation;
- GitHub boot and synchronization;
- research and technical or strategic discussion;
- advisories and cross-department routing;
- substantial authorized connector-backed work where the current Chat surface supports it;
- maintaining useful domain context without consuming unnecessary Work capacity.

They are not autonomous agents and do not independently share hidden state. They are structured departmental perspectives within one coherent Penny system.

Observed Chat/Work boundary as of 2026-07-15:

- Repeated Sol 5.6 Medium and High reasoning, GitHub reads/writes, and extensive Google Drive spreadsheet work in general Chat did not move the weekly Work usage meter during the observed period.
- Work usage appears tied to the separate Work/Task execution environment rather than ordinary Chat model strength.
- Treat this as a strong field observation, not a permanent claim about undocumented platform internals.
- Use the strongest Chat model justified by the reasoning task.
- Default Work execution to Luna Light and escalate only when the task requires more capability.

Work mode remains reserved for:

- substantial code writing or testing;
- local repository operations;
- large local file edits;
- test-suite execution;
- packaging applications;
- browser or desktop automation;
- complex artifact generation;
- long-running implementation tasks.

Main Assistant owns overall coordination and final synthesis. Departments own specialized judgment and durable domain state. Workers execute narrow procedures. Rob remains final authority for consequential, destructive, financial, or externally visible actions.

Engineering should observe the live HQ system for routing friction, duplicated authority, stale boot assumptions, connector limitations, and unnecessary model usage. Refine only from real evidence.

## Department File Ownership and Drift

Each department now owns routine maintenance of its own GitHub project subtree and canonical domain files.

During routine boots and syncs, departments should compare current working context with GitHub and directly correct stale status, handoffs, open loops, decisions, and local procedures.

Do not route routine local maintenance through Life Logistics or formal advisories. Use advisories for cross-department dependencies, decisions, risks, conflicts, or required action.

Main coordinates shared policy and cross-department changes. Life Logistics maintains global boot integrity, shared procedures, advisory-index hygiene, cross-project audits, and system-wide housekeeping.

Canonical SOP:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`

## Current Active Core

- Main Assistant / LifeOS Coordination Hub
- Life Logistics HQ
- Chief Engineering Penny
- Chief of Finance Penny
- Chief Business HQ
- Office Leaks Consulting HQ
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

Raw Capture mission:

> Capture first. Organize later.

It appends raw intake to the canonical Google Sheet `Life OS Raw Capture Inbox`. Main Assistant owns later processing of rows where `Processed = No`.

Inventory mission:

> See the item. Record the item. Verify the row.

It converts sale-item photographs uploaded directly into chat into one verified row per physical item in the canonical Google Sheet `For Sale Inventory`.

Inventory does not automatically price, bundle, group, write listings, publish Marketplace posts, or make sale-strategy decisions.

Workers load the shared worker standard and their worker-specific boot contract. They do not automatically follow the full department boot sequence.

## Consolidated / Dormant Departments

- Work Search is consolidated into Main Assistant for current lightweight logistics and reminders.
- Support Pathway is consolidated into Main Assistant for current lightweight research and logistics.
- Daily Anchors / Recovery Logistics is dormant until Rob reactivates it.
- Philosophy HQ is dormant until Rob reactivates it.

Preserve project history. Do not delete department files without explicit authorization.

## Current Durable Architecture

- Canonical startup: `memory/STARTUP_BOOT.md`
- Context shortcuts and hub commands: `memory/CONTEXT_REMINDER.md`
- Daily Operating SOP: `memory/06_DAILY_OPERATING_SOP.md`
- Department File Ownership SOP: `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- Chat/Work Execution Policy: `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`
- Active Projects: `memory/04_ACTIVE_PROJECTS.md`
- Open Loops: `memory/05_OPEN_LOOPS.md`
- Worker registry: `workers/README.md`
- Shared worker standard: `workers/WORKER_STANDARD.md`
- Advisory dashboard: `coordination/ADVISORY_INDEX.md`
- Advisory details: `coordination/boards/`
- Advisory Board Lifecycle Standard: `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`
- Decision Rules Registry: `coordination/DECISION_RULES_REGISTRY.md`
- Pending Advisory Boards standard: `coordination/PENDING_ADVISORY_BOARDS.md`
- Department Notebooks standard: `coordination/DEPARTMENT_NOTEBOOKS.md`
- Source-of-Truth and Publication Standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`
- Connector Reliability Operating Pattern: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`
- Design Principles: `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`
- Local prompt-launcher database: `engineering/classroom/prompt_launcher/prompt_library.json`

`coordination/DEPARTMENT_EVENT_INBOX.md` is frozen historical state and must not be updated for normal advisory routing.

## Daily Operating Standard

Every department boot inherits `memory/06_DAILY_OPERATING_SOP.md` through the canonical global boot sequence.

Default pattern:

- choose one major action;
- add at most one low-friction support action when useful;
- treat leaving home and transit as a complete major task;
- prepare and delegate Penny-level work before asking Rob to act;
- keep due dates sparse and meaningful;
- preserve recovery, health, and basic-life commitments without creating another anxiety-producing checklist;
- route specialized judgment to the owning department.

The SOP is a testable operating standard, not a rigid task list.

Current real-world evidence: Rob attended a recovery meeting despite significant pre-departure activation friction and reported that the bus ride became pleasant once movement began. Preserve the working rule that friction predicts activation difficulty, not necessarily a poor outcome.

## Finance Forecasting System

Chief Finance Penny created a substantial Google Sheets life-financial forecasting model.

Its working scope includes:

- projected cash flow rather than only historical transactions;
- category tracking;
- planned spending and priority allocation;
- product and price comparisons;
- deal tracking;
- downstream impact of present spending choices.

Detailed financial records, balances, transactions, and forecasts remain in Finance-owned Google Drive files and must not be copied into GitHub. GitHub may retain only abstract operational context and pointers.

Immediate transportation pressure is easing through expected recovery-community support and paid cleanup work with friends. Final projected spending should wait until actual incoming amounts are known.

## Active Shortcut Set

The current response and operations shortcut vocabulary lives in `memory/CONTEXT_REMINDER.md`.

It includes:

- response controls such as `/HUMAN`, `/ELI10`, `/DEEPER`, `/NOYES`, `/GIVE3`, `/TABLE`, `/TIGHTEN`, `/FLOOD`, `/STEPS`, and `/REDPEN`;
- boot, advisory, and synchronization commands;
- connector-specific Drive, Calendar, Gmail, Todoist, itinerary, morning, nightly, capture, and open-loop commands;
- hub coordination commands including `/HUB`, `/SYNC`, `/ROLES`, `/DECIDE`, `/DEPENDENCIES`, `/RIPPLE`, `/MINUTES`, `/WATCH`, `/DRIFT`, `/ROUTE`, `/ESCALATE`, `/BROADCAST`, `/CLOSELOOP`, and `/UPDATEGITHUB`;
- department tags for Main, Logistics, Engineering, Finance, Business, and Wellness perspectives.

The context file is canonical. Prompt launcher JSON is a secondary interface and must not silently redefine command meaning.

## Advisory State

As of 2026-07-15, the Advisory Index contains no open advisories.

Recently closed:

- ADV-20260715-036 — Seven LifeOS department discussion HQ chats opened and confirmed ready; Chat/Work separation and operating boundaries are active.
- ADV-20260715-035 — Daily Operating SOP integrated into the global boot path.
- ADV-20260714-034 — Expanded connector-tagged shortcut vocabulary synchronized.
- ADV-20260713-033 — Core boot and advisory shortcut rollout synchronized.
- ADV-20260710-032 — Penny Inventory Worker package implemented and canonical resource verified.
- ADV-20260710-031 — Advisory Board Lifecycle Standard implemented.
- ADV-20260709-030 — Formal worker layer and Raw Capture Worker implemented.

The Advisory Index is the sole active routing dashboard. Source boards contain canonical advisory text. Git history is the default archive for compacted completed detail.

## Office Leaks Operating Philosophy

Office Leaks Consulting is a practical, trust-based systems consulting lane for small local service businesses.

Core philosophy:

- Respect the people. Fix the process.
- Good people deserve good systems.
- The tool is not the product. The habit is the product.
- No shame. No blame. Fix the system.

Engineering delivery architecture:

- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Drive: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Finance working-record pointer:

- `projects/finance-benefits/OFFICE_LEAKS_FINANCE_POINTERS.md`

Keep GitHub abstract. Pricing, startup costs, revenue tracking, taxes, and detailed financial models belong in Finance-owned working records.

## Best Next Actions

- Use the Main Assistant hub as the primary conversational front door.
- Use department HQs for sustained specialist work and direct maintenance of their own GitHub state.
- Use general Chat for substantial reasoning and connector-backed work where available.
- Reserve Work for bounded local execution and default to Luna Light unless more capability is justified.
- Use the Finance forecasting model once actual incoming funds and priorities are known.
- Pilot Penny Raw Capture Worker with real intake and verified writes.
- Pilot Penny Inventory Worker with 2–3 real uploaded sale-item photographs.
- Keep pricing, grouping, listing copy, and publication separate from inventory capture.
- Continue Office Leaks positioning, offers, outreach, and delivery-method work.
- Continue Engineering's Reliable Connector Execution Layer and operation-ledger design.
- Keep Engineering HQ Daily Sync paused pending stronger scheduled-execution architecture and explicit authorization.
- Maintain advisory-board hygiene without turning cleanup into recurring bureaucracy.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Calendar owns time. Todoist owns Rob-facing actions. Gmail owns communications. Departments own judgment and their own durable state. Workers execute narrow contracts. Main Assistant coordinates. Life Logistics curates shared infrastructure and cross-project memory.

Use RPR when reliable structured-file editing matters more than connector automation.