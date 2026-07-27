# System Session Handoff

Updated: 2026-07-27
Project: LifeOS / Maintenance_HQ / Penny Long-Term Memory
Purpose: System-level baton pass for `LifeOS_HQ`, `Chief_of_Staff_HQ`, `Maintenance_HQ`, and explicit cross-department coordination. This file is not a mirror of department backlogs, live advisories, runtime state, or the full Worker contract.

## Current System State

LifeOS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet, home of the human-facing Chief's Manual, and editable handbook library;
- Project Sources as noncanonical project-context mirrors, including one role-neutral global handbook and explicitly intended-room handbook mirrors;
- Trello as the raw-intake, visual-attention, and active-flow layer;
- Todoist as Rob-facing commitments and reminders;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- a locally running LifeOS Dashboard with Overview, Department Inspection, Automation, and Worker Operations surfaces;
- one central meeting room plus seven Department HQ chats;
- validated Windows desktop automation for bounded exact-destination transport;
- a dashboard-integrated Automation Command Center with persistent history, scheduled procedures, shared safety pause, conservative send budget, activation-prerequisite reporting, and safety reporting;
- one canonical HQ and Worker boot entry point at `memory/STARTUP_BOOT.md`;
- one canonical execution protocol at `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- one canonical Worker authority contract at `coordination/WORKER_EXECUTION_CONTRACT.md`;
- Workers as narrow operational executors owned by one department;
- `Chief_of_Staff_HQ` as Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, Hub chair, routing desk, reporting desk, and follow-through coordinator;
- `Maintenance_HQ` as global GitHub maintainer, boot owner, shared-contract owner, governance auditor, migration owner, publication-mirror steward, and reconciliation authority;
- `Engineering_HQ` as technical architecture, routing-registry, transport, receiver-state, dashboard, automation, and implementation owner;
- two current production Workers: `Engineering_Worker` and `Maintenance_Worker`;
- one active Rob-approved Maintenance assignment: `ADV-20260726-053` revision 1 / `RUN-ADV-20260726-053-R1`, pending immutable result submission and `IMMEDIATE_HQ` review.

GitHub remains abstract. Detailed financial, medical, business, personal, credential, customer, and operational records stay in their natural source systems.

## Official Eight-Room Architecture

LifeOS uses eight top-level rooms:

1. `LifeOS_HQ`, the shared meeting room;
2. `Chief_of_Staff_HQ`;
3. `Maintenance_HQ`;
4. `Engineering_HQ`;
5. `Finance_HQ`;
6. `Business_HQ`;
7. `Office_Leaks_HQ`;
8. `Wellness_HQ`.

`LifeOS_HQ` is not a department and does not own an independent backlog.

`Chief_of_Staff_HQ` chairs the Hub, receives department reports, routes assignments, integrates recommendations, supports daily life, and checks follow-through.

Departments retain ownership of their domain judgment, durable records, Worker authority, Worker profiles, holds, verification, and retirement.

`Maintenance_HQ` owns global GitHub maintenance, governance, boot integrity, source boundaries, audits, migrations, shared procedures, profile conventions, shared execution contracts, Project Source publication discipline, and reconciliation.

`Engineering_HQ` owns technical routing and transport implementation, including the Worker routing registry, exact-title lookup, stable-ID transport, receiver state, advisory-revision deduplication, immutable result ingestion, verification queues, wake suppression, dashboard code, automation code, databases, tests, and technical rollover mechanisms.

Canonical authority and naming:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `memory/HQ_NAMING_STANDARD.md`

## Ownership and Boot Architecture

Current operating rules:

- department `open_loops.md` files are authoritative for department-owned unfinished work;
- `memory/05_OPEN_LOOPS.md` contains genuinely system-owned work and operating watches only;
- the universal operating kernel loads shared rules, including Project Instructions and the Hub Operating Contract;
- every `LifeOS_HQ` and Department HQ then loads `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` before role-specific state;
- `LifeOS_HQ` reads broad shared coordination state without becoming an owner;
- `Chief_of_Staff_HQ` reads broader state when coordinating daily operations, assignments, department reports, scheduled reporting, or system decisions;
- `Chief_of_Staff_HQ` may route Rob-authorized execution-ready work directly to an existing Department Worker when no department judgment or exception is required;
- `Maintenance_HQ` reads broad system state for audits, global maintenance, migrations, boot integrity, shared-contract maintenance, publication reconciliation, and source-boundary enforcement;
- specialist departments load their own files plus only relevant advisories, assignments, dependencies, shared policies, or routed context;
- a Worker loads the universal kernel, both shared protocols, the owning department identity, the exact Worker profile, the authoritative advisory, task definition, or schedule, and only the records required for the bounded task;
- Workers do not automatically load full department histories, notebooks, backlogs, or unrelated open loops;
- the Department Inspection surface aggregates department and system records read-only without becoming a source of truth.

Canonical shared rules:

- `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`
- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `memory/STARTUP_BOOT.md`
- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`

Short form:

> The Hub is the table. `Chief_of_Staff_HQ` coordinates. Departments judge and own. Workers execute. `Maintenance_HQ` protects the contracts. `Engineering_HQ` builds the machinery. Rob decides.

## July 23-27 Naming, Publication, and Worker Reconciliation

Completed outcomes:

- current system spelling is `LifeOS`;
- current top-level room titles use exact underscore names;
- current production Worker titles are `Engineering_Worker` and `Maintenance_Worker`;
- future Worker titles follow `<Department_Name>_Worker` only after owner-approved rollout;
- all seven Department HQ boot file sets were aligned and verified during the 2026-07-23 naming repair;
- stable filesystem paths, historical evidence, immutable Worker artifacts, receipts, checksums, IDs, URLs, and accurate quotations were preserved;
- Engineering completed the separately authorized canonical runtime-title rollover, direct URL routing, guarded route capture, browser bridge recovery, and Package F Wave 0B safety kernel;
- `ADV-20260723-052` closed after the read-only watcher reported in the existing `Chief_of_Staff_HQ` conversation without creating a new chat or triggering work;
- the shared ChatGPT Project publication reconciliation closed on 2026-07-25 after current project context showed canonical underscore instructions, retrieved the stable global handbook, exposed the eight intended-room handbooks, and showed no numbered competing global handbook copy;
- the production Worker portfolio remained intentionally lean after Business, Finance, and Wellness declined current Worker rollout and Office Leaks remained paused;
- `Maintenance_Worker` was registered, route-verified, activated by Rob, and remained idle until the exact first assignment was authorized;
- Engineering posted `ADV-20260726-053` revision 1 under direct Rob authority for one coordinated repository audit and repair;
- `Maintenance_Worker` accepted only that exact revision and run, with one-run cross-department current-text authority and `IMMEDIATE_HQ` verification.

Project Source handbooks remain generated, noncanonical context mirrors. The global handbook is role-neutral. Each room handbook carries an explicit intended-room statement and grants no authority merely because it is visible to another room.

## Shared Execution and Worker Architecture

The canonical architecture established on 2026-07-19 remains active:

- shared execution governance lives in `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- the universal Worker authority ceiling lives in `coordination/WORKER_EXECUTION_CONTRACT.md`;
- `memory/STARTUP_BOOT.md` is the single canonical HQ and Worker entry point;
- new Worker profiles live at `projects/<department>/workers/<profile>.md` and are created only when the owning Department HQ activates a real Worker;
- department profiles define stable identity and authority, not deployment or runtime state;
- the root Raw Capture and Inventory packages remain grandfathered compatibility pilots;
- the normal execution-ready path targets the owning Department Worker directly and should usually require one event-driven wake;
- verification modes, wake suppression, holds, elevations, resume signals, revision handling, immutable evidence, and duplicate suppression are shared rules rather than department copies.

Package D, Package E, Package F Wave 0A, and Package F Wave 0B Engineering implementation are complete. Their validated machinery does not create cross-department adoption authority, new Workers, or automatic advisory closure.

The Wave 0B activation-prerequisite report is read-only and always reports `activation_authorized: false`. Technical readiness remains separate from owning-department authority, Maintenance shared-governance review, and Rob approval where the Worker contract requires it.

The current Maintenance run is authorized only by `ADV-20260726-053` revision 1 and approval reference `ROB-DIRECT-COORDINATED-REPAIR-20260726`. It creates no recurring schedule, unattended execution, new connector, spending, public action, destructive authority, standing cross-department authority, or future assignment.

## Department Inspection Evidence

The read-only Department Inspection MVP remains locally validated at:

- 414 normalized records;
- zero findings;
- zero warnings.

This confirms parser-visible structural cleanliness at the time of validation. It does not replace semantic governance audits. Inspector findings remain audit prompts, not automatic verdicts.

## Dashboard, Automation, and Scheduler Boundaries

The dashboard is a visibility, transport, diagnostic, and bounded-control layer, not a replacement source of truth or policy owner.

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Guarded GitHub sync may fast-forward only when local `main` is clean and strictly behind. It does not resolve conflicts, discard work, rebase, reset, or authorize broad automatic writes.

The Automation Command Center supports exact destinations, protected canonical prompts, persistent run history, bounded schedules, immutable result ingestion, HQ and Rob verification receipts, shared safety pause, conservative send budgeting, read-only activation-prerequisite reporting, and duplicate-suppression controls.

Scheduler production reliability has live evidence, but fully unattended Windows production remains unapproved unless current Engineering evidence and Rob's explicit authorization establish the exact production scope.

`Engineering_HQ Daily Sync` remains paused by deliberate operating choice until Rob explicitly resumes it.

The hourly `Chief_of_Staff_HQ` advisory watcher remains an active read-only pilot. Its destination test passed, `ADV-20260723-052` is closed, and the watcher creates no work, authority, or advisory lifecycle changes.

Deployment state, route availability, pause state, exact-title resolution, stable-ID transport, receiver state, verification queues, one-shot wake claims, and technical rollover belong to the Engineering-owned routing registry and runtime. Department-owned Worker profiles define stable identity and authority only.

## Chat and Work Architecture

Regular Chat is the canonical conversational environment.

`LifeOS_HQ` is the shared meeting room. `Chief_of_Staff_HQ` is the normal daily point of contact.

Use Chat for planning, department coordination, writing, strategy, recovery, philosophy, ordinary reasoning, GitHub synchronization, and light connector work where available.

Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser or desktop control, artifact production, or other computer-execution capabilities.

Canonical policy:

- `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`

## Trello Flow Boundary

Trello Inbox captures raw thoughts and quick actions.

LifeOS Flow Board shows current attention and active flow.

Todoist holds commitments, reminders, and due-date obligations.

Calendar holds timed commitments.

GitHub holds durable project state and memory.

`Chief_of_Staff_HQ` owns `/FLOW`, `/FLOW PROCESS`, and `/FLOW NOW` operation.

Canonical SOP:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

## Advisory State

`coordination/ADVISORY_INDEX.md` is the live source of truth for open advisory routing. Do not cache a static advisory list in this handoff.

Current routed work at this handoff:

- `ADV-20260726-053` — OPEN — source board `coordination/boards/engineering.md` — target `maintenance_worker` / `Maintenance_HQ` — verification `IMMEDIATE_HQ`.

Department Event Inbox remains frozen as historical context unless Rob explicitly reactivates it.

`LifeOS_HQ` formal advisories use `Chief_of_Staff_HQ` as the source department and `coordination/boards/main-assistant.md` as the retained source-board path. Department-originated advisories remain on their source department boards.

`ADV-20260718-042` and `ADV-20260723-052` are closed. Do not recreate them as active implementation or validation work.

## Active Core Rooms

- `LifeOS_HQ`, meeting room
- `Chief_of_Staff_HQ`
- `Maintenance_HQ`
- `Engineering_HQ`
- `Finance_HQ`
- `Business_HQ`
- `Office_Leaks_HQ`
- `Wellness_HQ`

LifeOS Infrastructure remains a shared project area used as needed, not an additional top-level department chat.

Consolidated or dormant domains remain preserved rather than deleted.

## Source Boundaries

- GitHub: durable abstract state, architecture, ownership, pointers, contracts, profiles, and auditable changes.
- Drive: Chief's Manual, working documents, detailed records, editable handbook documents, and human-facing artifacts.
- Project Sources: noncanonical project context, including the role-neutral global handbook and explicitly intended-room handbook mirrors; no handbook grants authority or replaces live GitHub state.
- Trello: raw intake, current attention, and flow.
- Todoist: Rob-facing commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Dashboard and automation logs: transport, diagnostics, and run evidence.
- Department files: authoritative department state.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.

## Best Next System Actions

1. Complete only `ADV-20260726-053` revision 1 within its exact authority, create the immutable result, and stop for `Maintenance_HQ` review.
2. Keep the source advisory and Advisory Index unchanged during Worker execution.
3. Let Department HQs create or change Worker profiles only under their own authority and the canonical Worker contract.
4. Keep technical readiness separate from owning-department authority, Maintenance governance review, and Rob approval.
5. Preserve the two grandfathered pilots under compatibility rules and migrate or retire them only through separate owner review and authorization.
6. Preserve one stable global handbook and one explicitly intended-room handbook per room without numbered competing copies or authority drift.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet and editable handbook library. Project Sources publish noncanonical context. Trello catches possibility and shows flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard transports and observes without governing. The Hub deliberates. `Chief_of_Staff_HQ` coordinates. Departments judge and own. Workers execute. `Maintenance_HQ` protects the contracts. `Engineering_HQ` builds the machinery. Rob decides.