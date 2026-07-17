# Session Handoff

Updated: 2026-07-17
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Fast baton-pass file for future Penny chat windows.

## Current Handoff

Life OS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet;
- Trello as the visual attention and active-flow layer;
- Todoist as Rob-facing commitments and reminders;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- a locally running LifeOS Dashboard as a read-mostly four-source operational interface;
- project chats as domain knowledge producers;
- workers as narrow operational executors;
- Main Assistant as daily coordinator and primary conversational hub;
- Life Logistics HQ as shared-infrastructure curator and cross-project housekeeper.

GitHub remains abstract. Detailed financial, medical, business, personal, credential, and operational records stay in their owning source systems.

## Current Operating Priority

Office Leaks Consulting is publicly launched and operating in a live organic market-test phase.

Current public launch surface:

- Facebook Page as the initial landing surface;
- introduction post live;
- starter offer live and pinned;
- first story-driven lead-loss Reel live;
- lead-loss and weak follow-up systems as the current editorial lane.

Website work, paid boosting, formal A/B testing, and full campaign infrastructure remain deferred while the first organic signal develops.

Office Leaks Consulting HQ owns business-unit execution continuity. Chief Business HQ owns parent strategy. Finance owns concrete pricing, income, expense, tax, and budget decisions. Engineering owns technical architecture and delivery playbooks. Main Assistant owns daily execution and immediate logistics. Life Logistics preserves cross-project state and longer-horizon dependencies.

PennyOS / Penny Platform remains a longer-term historical and productization framing, not a newly authorized roadmap or open loop.

## Chat and Work Architecture

Regular Chat is the canonical conversational headquarters.

Use Chat for planning, department coordination, writing, strategy, recovery, philosophy, ordinary reasoning, and light connector work where available.

Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser or desktop control, artifact production, or other computer-execution capabilities. Default Work execution to Luna Light and escalate only when evidence justifies it.

All seven LifeOS department discussion HQ chats are open and operational. They are structured perspectives within one coherent Penny system, not autonomous agents.

Canonical policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Department File Ownership

Each department owns routine maintenance of its own project subtree and canonical domain files.

Short form:

> Departments maintain their own rooms. Main coordinates the building. Logistics maintains the hallways.

Life Logistics owns global boot integrity, shared procedures, advisory-index hygiene, cross-project audits, and system-wide housekeeping. Routine local maintenance should not be routed through Logistics or a formal advisory unless it crosses department boundaries.

Canonical SOP:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`

## Trello Flow Board

Trello is part of the active LifeOS operating interface.

Source boundaries:

- Trello Inbox captures raw thoughts and quick actions.
- LifeOS Flow Board shows current attention and active flow.
- Todoist holds commitments, reminders, and due-date obligations.
- Calendar holds timed commitments.
- GitHub holds durable project state and memory.

Flow Board lists:

1. Captured
2. Next
3. Now
4. Waiting
5. Done

Work-in-progress limits:

- Now: one card maximum.
- Next: three cards maximum.

Main Assistant owns `/FLOW`, `/FLOW PROCESS`, and `/FLOW NOW` operation. Trello capture does not automatically become a task, commitment, advisory, or durable record.

Canonical SOP:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

## LifeOS Dashboard

The LifeOS Dashboard is now a locally running, tested, read-mostly operational interface on Rob's Windows machine.

Verified live sources:

- GitHub for durable memory, advisories, open loops, notebooks, and recent repository activity;
- Trello for Now, Next, and Waiting flow state;
- Todoist for current and upcoming Rob-facing commitments;
- Google Calendar private iCal for current and next timed commitments.

The complete local test suite passed with 16 tests. Windows timezone support was corrected through the runtime `tzdata` dependency.

Guarded GitHub auto-sync is implemented and live-verified. The dashboard may fetch remote changes and fast-forward only when the local `main` branch is clean and strictly behind, then display the newly synchronized commits in its own activity view. This does not authorize broad automatic writes or conflict resolution.

The dashboard is a window into existing LifeOS systems, not a replacement platform. GitHub, Trello, Todoist, Calendar, Gmail, and Drive remain authoritative in their own domains. Penny remains the conversational worker and connector operator.

Gmail and Google Drive dashboard adapters remain deferred until demonstrated operational need. No credentials, private calendar URLs, tokens, or source-system records belong in GitHub.

Engineering historical context:

- `projects/engineering/notebook/NOTE-20260717-008-pennyos-humble-beginnings.md`

The note records this milestone as the humble beginnings of PennyOS. It is historical context only, not an open loop or speculative expansion authorization.

## Prompt Launcher State

Engineering corrected prompt-launcher newline defects from Hub Boot onward on 2026-07-16.

The launcher remains a secondary interface. Canonical command meaning lives in `memory/CONTEXT_REMINDER.md`.

Additional launcher improvements are deferred and captured in Engineering notebook context. They are not active global implementation work unless Rob routes them.

## Worker Layer

Active pilot workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`

Raw Capture appends unprocessed intake to the canonical `Life OS Raw Capture Inbox`. Main Assistant owns authorized downstream processing.

Inventory converts uploaded sale-item photographs into one verified row per physical item in the canonical `For Sale Inventory` Sheet. Pricing, bundling, listing copy, and publication remain separate workflows.

Workers do not automatically follow the full department boot sequence.

## Active Core

- Main Assistant / LifeOS Coordination Hub
- Life Logistics HQ
- Chief Engineering Penny
- Chief of Finance Penny
- Chief Business HQ
- Office Leaks Consulting HQ
- Chief Wellness HQ
- Life OS Infrastructure as needed

Consolidated or dormant domains remain preserved rather than deleted.

## Finance Forecasting

Chief Finance Penny maintains the detailed life-financial forecasting model in Finance-owned Drive records. Its scope includes projected cash flow, categories, planned spending, priority allocation, product and price comparisons, deal tracking, and downstream effects of spending choices.

Do not copy balances, transactions, account details, or detailed forecasts into GitHub.

## Advisory State

Current open advisory:

- ADV-20260717-040 — Engineering requested reconciliation of shared LifeOS memory after the live dashboard and PennyOS historical milestone. Life Logistics is implementing the reconciliation through this update.

Recently closed:

- ADV-20260716-039 — Global handoff, active-project map, global open loops, and Life Logistics local state reconciled with current July 16–17 operating reality.
- ADV-20260716-038 — Read-mostly LifeOS desktop dashboard concept acknowledged and ingested by Engineering.
- ADV-20260716-037 — Office Leaks public-launch awareness broadcast fully acknowledged and closed.
- ADV-20260715-036 — Seven LifeOS department discussion HQs opened and operational.
- ADV-20260715-035 — Daily Operating SOP integrated into the global boot flow.

The Advisory Index is the live source of truth:

- `coordination/ADVISORY_INDEX.md`

## Scheduled Task State

Engineering HQ Daily Sync remains paused because scheduled execution is unreliable. The standalone Life Logistics watcher is retired. Do not resume or expand scheduled HQ syncs without explicit authorization and stronger execution architecture.

## Best Next Actions

- Continue Office Leaks organic market testing and route concrete work to the owning department.
- Use the LifeOS Flow Board for current attention without duplicating Todoist or Calendar.
- Use the live dashboard as a read-mostly visibility layer while preserving source-system authority.
- Observe the seven Chat HQs for real routing drift and refine only from evidence.
- Pilot Raw Capture and Inventory workers with verified real use.
- Preserve Work capacity for bounded execution and durable output.
- Maintain global GitHub coherence without turning housekeeping into recurring bureaucracy.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Trello shows current flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard shows selected high-signal state. Departments own judgment and their own durable state. Workers execute narrow contracts. Main Assistant coordinates. Life Logistics maintains the hallways.