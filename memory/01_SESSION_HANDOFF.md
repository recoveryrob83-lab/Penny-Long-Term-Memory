# System Session Handoff

Updated: 2026-07-19
Project: LifeOS / Maintenance_HQ / Penny Long-Term Memory
Purpose: System-level baton pass for `LifeOS_HQ`, `Chief_of_Staff_HQ`, `Maintenance_HQ`, and explicit cross-department coordination. This file is not a mirror of department backlogs or the full Worker contract.

## Current System State

LifeOS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet and home of the human-facing Chief's Manual;
- Trello as the raw-intake, visual-attention, and active-flow layer;
- Todoist as Rob-facing commitments and reminders;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- a locally running LifeOS Dashboard with Overview, Department Inspection, and Automation tabs;
- one central meeting room plus seven Department HQ chats;
- validated Windows desktop automation for drafting or explicitly sending prompts to exact LifeOS destinations;
- an operational dashboard-integrated Automation Command Center with manual and scheduled runs, persistent history, and safety reporting;
- one canonical HQ and Worker boot entry point at `memory/STARTUP_BOOT.md`;
- one canonical execution protocol at `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- one canonical Worker authority contract at `coordination/WORKER_EXECUTION_CONTRACT.md`;
- Workers as narrow operational executors owned by one department;
- `Chief_of_Staff_HQ` as Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, Hub chair, routing desk, and follow-through coordinator;
- `Maintenance_HQ` as global GitHub maintainer, boot owner, shared-contract owner, governance auditor, migration owner, and reconciliation authority;
- `Engineering_HQ` as technical architecture, routing-registry, transport, receiver-state, and implementation owner.

GitHub remains abstract. Detailed financial, medical, business, personal, credential, and operational records stay in their owning source systems.

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

Departments retain ownership of their domain judgment, durable records, Worker authority, Worker profiles, holds, and verification.

`Maintenance_HQ` owns global GitHub maintenance, governance, boot integrity, source boundaries, audits, migrations, shared procedures, profile conventions, shared execution contracts, and reconciliation.

`Engineering_HQ` owns technical routing and transport implementation, including the Worker routing registry, exact-title lookup, stable-ID transport, receiver state, advisory-revision deduplication, verification queues, wake suppression, and technical rename or rollover mechanisms.

Canonical authority and naming:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `memory/HQ_NAMING_STANDARD.md`

## Ownership and Boot Architecture

Current operating rules:

- department `open_loops.md` files are authoritative for department-owned unfinished work;
- `memory/05_OPEN_LOOPS.md` is the System Open Loops file and does not mirror department backlogs;
- the universal operating kernel loads shared rules, including the Project Instructions and Hub Operating Contract;
- every `LifeOS_HQ` and Department HQ then loads `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` before role-specific state;
- `LifeOS_HQ` reads broad shared coordination state without becoming an owner;
- `Chief_of_Staff_HQ` reads broader state when coordinating daily operations, assignments, department reports, or system decisions;
- `Chief_of_Staff_HQ` may route Rob-authorized execution-ready work directly to an existing Department Worker when no department judgment or exception is required;
- `Maintenance_HQ` reads broad system state for audits, global maintenance, migrations, boot integrity, shared-contract maintenance, and reconciliation;
- specialist departments load their own files plus only relevant advisories, assignments, dependencies, shared policies, or routed context;
- a Worker loads the universal kernel, both shared protocols, the owning department identity, the exact Worker profile, the authoritative advisory, task definition, or schedule, and only the records required for the bounded task;
- Workers do not automatically load full department histories, notebooks, backlogs, or unrelated open loops;
- the Department Inspection tab aggregates seven departments plus System read-only without becoming a source of truth.

Canonical rules:

- `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`
- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `memory/STARTUP_BOOT.md`
- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`

Short form:

> The Hub is the table. `Chief_of_Staff_HQ` coordinates. Departments judge and own. Workers execute. `Maintenance_HQ` protects the contracts. `Engineering_HQ` builds the routing machinery. Rob decides.

## Governance Alignment

The dated entries below preserve the role names used when Rob adopted the transition on 2026-07-18. They are historical evidence; current names are defined by `memory/HQ_NAMING_STANDARD.md`.

- Main Assistant's official role name is now `Chief of Staff HQ`;
- Logistics' official role name is now `Life OS Maintenance HQ`;
- `LifeOS HQ` is a meeting room rather than an independent department or authority;
- Chief of Staff HQ is the primary point of contact and receives department reports;
- actions produced in the Hub transfer to the correct department and authoritative destination;
- Hub-originated formal advisories use the retained Chief of Staff source-board path `coordination/boards/main-assistant.md` plus the Advisory Index;
- existing project paths remain unchanged during the naming transition.

Phase One updated the constitutional and shared-system layer. Phase Two owner-routed naming, authority, ownership, and pointer repairs are complete across the seven current Department HQs. The post-implementation residual documentation drift was reconciled on 2026-07-18.

On 2026-07-19, ADV-20260719-043 established the canonical shared execution and Worker architecture:

- shared execution governance lives in `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- the universal Worker authority ceiling lives in `coordination/WORKER_EXECUTION_CONTRACT.md`;
- `memory/STARTUP_BOOT.md` remains the single canonical HQ and Worker entry point;
- new Worker profiles live at `projects/<department>/workers/<profile>.md` and are created only when the owning Department HQ activates a real Worker;
- the two root packages under `workers/` remain grandfathered compatibility pilots rather than the model for new Workers;
- the normal execution-ready path targets the owning Department Worker directly and should usually require one event-driven wake;
- verification modes, wake suppression, holds, elevations, resume signals, revision handling, and duplicate suppression are shared rules rather than department copies.

The deployed ChatGPT LifeOS Project Settings copy was verified on 2026-07-18 against the paste-ready section of `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`. No additional manual replacement is pending. Future reconciliation opens only when a demonstrated difference appears.

## Department Inspection Evidence

The read-only Department Inspection MVP is locally validated.

Evidence progression:

- 458 normalized records / 4 findings / 101 warnings;
- 459 / 4 / 15 after evidence-based parser and presentation tuning;
- 414 / 0 / 13 after source cleanup;
- 414 / 0 / 0 after warning audit, notebook-status parser correction, explicit Logistics status normalization, and Rob's live local verification.

The zero-warning result confirms parser-visible structural cleanliness. It does not replace semantic governance audits. Use inspector findings as audit prompts, not automatic verdicts.

## Dashboard and Automation Boundaries

The dashboard is a visibility, transport, diagnostic, and bounded-control layer, not a replacement source of truth or policy owner.

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Guarded GitHub auto-sync may fast-forward only when local `main` is clean and strictly behind. It does not resolve conflicts, discard work, rebase, reset, or authorize broad automatic writes.

The Automation Command Center supports exact destinations, protected canonical prompts, saved and custom prompts, draft or explicitly confirmed send mode, one-time/daily/weekly schedules, separate Scheduled Jobs and Run History, and structured failure reporting.

Scheduling is operational but not yet production-ready for fully unattended Windows use. Engineering owns remaining technical evidence and implementation.

`Engineering_HQ` Daily Sync remains paused until Rob explicitly resumes it under an approved architecture.

Deployment state, route availability, pause state, active or retired routing, exact-title resolution, stable-ID transport, receiver state, verification queues, and wake suppression belong to the Engineering-owned routing registry and runtime. Department-owned Worker profiles define stable identity and authority only.

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

## Worker Layer

Canonical architecture:

- shared execution protocol: `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- Worker authority contract: `coordination/WORKER_EXECUTION_CONTRACT.md`;
- canonical boot branch: `memory/STARTUP_BOOT.md`;
- new department-owned profile location: `projects/<department>/workers/<profile>.md`.

A Department HQ owns each Worker's purpose, allowed task classes, stable identity, authority, profile, holds, verification, and retirement. `Chief_of_Staff_HQ` may route Rob-authorized bounded work into an existing profile without taking ownership of specialist judgment. `Maintenance_HQ` owns the shared contracts, profile convention, boot coherence, and source-boundary protection. `Engineering_HQ` owns routing and runtime implementation.

Grandfathered compatibility pilots:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`;
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`.

`workers/README.md` and `workers/WORKER_STANDARD.md` are compatibility surfaces only. No new top-level Worker package may be created by analogy.

Workers do not inherit department or system backlogs unless the exact profile or task routes a required read. Worker durable state belongs in the authoritative advisory or task definition, run record, automation logs, permitted department records, and the department profile for stable identity and authority only.

## Advisory State

`coordination/ADVISORY_INDEX.md` is the live source of truth for open advisory routing. Do not cache a static advisory list in this handoff.

Department Event Inbox remains frozen as historical context unless Rob explicitly reactivates it.

`LifeOS_HQ` formal advisories use `Chief_of_Staff_HQ` as the source department and `coordination/boards/main-assistant.md` as the retained source-board path. Department-originated advisories remain on their source department boards.

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
- Drive: Chief's Manual, working documents, detailed records, and human-facing artifacts.
- Trello: raw intake, current attention, and flow.
- Todoist: Rob-facing commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Dashboard and automation logs: transport, diagnostics, and run evidence.
- Department files: authoritative department state.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.

## Best Next System Actions

1. Preserve the canonical shared protocols and single HQ/Worker boot branch through ordinary audits.
2. Let Engineering complete the active receiver-side validation and routing-runtime work under ADV-20260718-042 without moving deployment state into department profiles.
3. Let specialist departments create Worker profiles only when a real Worker is activated and operational evidence justifies it.
4. Observe the two grandfathered pilots under the compatibility rules and migrate or retire them only through separate owner review and authorization.
5. Refresh the Department Inspector after meaningful source changes and inspect demonstrated findings individually.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Trello catches possibility and shows flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard transports and observes without governing. The Hub deliberates. `Chief_of_Staff_HQ` coordinates. Departments judge and own. Workers execute. `Maintenance_HQ` protects the contracts. `Engineering_HQ` builds the machinery. Rob decides.