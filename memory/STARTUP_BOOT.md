# Startup Boot

Updated: 2026-07-19
Project: LifeOS / Maintenance_HQ / Penny Long-Term Memory
Purpose: Canonical startup and routing procedure for fresh Penny chats, `LifeOS_HQ`, Department HQs, projects, and Workers.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

## Boot Principle

Use one universal operating kernel, then branch by operating role and load only the context required by the named room, department, project, or Worker.

Do not make every specialist read the global handoff, all active projects, all system loops, migration state, unrelated department backlogs, or full department history.

Short form:

> Shared rules are universal. Execution rules are shared. Operational state is role-routed.

Boot loads context. Sync compares context with authoritative state. Boot does not authorize maintenance, and Sync is read-only by default.

When both are requested, complete Boot first, then perform a separate read-only Sync report.

## Step 1: Identify the Boot Target

Before reading beyond the universal kernel, determine whether Rob is booting:

- `LifeOS_HQ`, the shared strategic meeting room;
- `Chief_of_Staff_HQ`;
- `Maintenance_HQ`;
- another Department HQ;
- a standalone project;
- a bounded Worker;
- an explicit system audit or architecture review.

When Rob names a room, department, project, or Worker, use that route. Do not broaden the boot merely because additional files are available.

Legacy display names are interpreted through:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `memory/HQ_NAMING_STANDARD.md`

Filesystem paths remain unchanged unless a separate migration is authorized.

## Step 2: Universal Operating Kernel

`LifeOS_HQ`, Department HQs, standalone projects, and explicit system-review chats read these files in this exact order:

1. `memory/STARTUP_BOOT.md`
2. `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`
3. `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
4. `memory/00_START_HERE.md`
5. `memory/CONTEXT_REMINDER.md`
6. `memory/03_OPERATIONAL_RULES.md`
7. `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
8. `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
9. `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`
10. `memory/06_DAILY_OPERATING_SOP.md`

The order above is canonical and unchanged.

ChatGPT Project Instructions are Layer Zero and may already be active before boot. The GitHub copy is the versioned canonical deployment source used to verify, audit, and reconcile the deployed Project Settings text.

The Hub Operating Contract defines the current authority map, official role names, legacy-name translation, Hub action transfer, and reporting structure.

The universal kernel defines command meaning, safety, source boundaries, file ownership, open-loop ownership, Chat versus Work usage, and the default daily operating standard.

The following are not universal kernel files:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/02_BOOT_LOG.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- `MIGRATION_PLAN.md`
- `MIRROR_STATUS.md`

Load them only under the role-routed rules below.

## Step 3: Shared Execution Protocol

After the universal kernel, every `LifeOS_HQ` and Department HQ reads:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`

This shared protocol defines:

- organizational topology;
- strategic, operational, Department HQ, and Worker boundaries;
- source-system boundaries;
- advisory continuity;
- lifecycle and priority separation;
- verification modes;
- wake eligibility and suppression;
- hold, elevation, and resume behavior;
- scheduled-procedure and desktop-pause rules;
- reporting and execution ownership.

Do not copy this protocol into department subtrees.

A Worker reads both shared protocols under the Worker branch below.

## Step 4: Role-Routed Context

### LifeOS_HQ

`LifeOS_HQ` is the shared strategic meeting room. It is not a department and has no independent project subtree or backlog.

After the universal kernel and shared execution protocol, read:

1. `memory/01_SESSION_HANDOFF.md`
2. `memory/04_ACTIVE_PROJECTS.md`
3. `memory/05_OPEN_LOOPS.md`
4. `coordination/ADVISORY_INDEX.md` when advisory state, routing, or a cross-department decision is relevant

Read department files only when current coordination, a named dependency, a routed assignment, or the meeting topic requires them.

Inside the Hub:

- `[MAIN]` is `Chief_of_Staff_HQ` speaking as chair;
- department tags provide domain judgment and recommendations;
- Rob remains final authority;
- the Hub itself does not become the owner of work;
- real actions transfer to one owning department and one authoritative destination;
- Hub-originated formal advisories use `coordination/boards/main-assistant.md` as the retained `Chief_of_Staff_HQ` source-board path.

Do not read all department notebooks or backlogs merely because a Hub meeting is broad.

### Chief_of_Staff_HQ

After the universal kernel and shared execution protocol, read:

1. `projects/main-assistant/SESSION_HANDOFF.md`
2. `projects/main-assistant/DEPARTMENT_IDENTITY.md`
3. `projects/main-assistant/README.md`
4. `projects/main-assistant/status.md`
5. `projects/main-assistant/open_loops.md`

Read these shared files when coordinating broad daily operations, receiving department reports, routing assignments, preparing a Hub report, or supporting a system decision:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

Read `memory/02_BOOT_LOG.md` only when recent boot-history changes, migration history, or recreated-chat recovery makes it relevant.

`Chief_of_Staff_HQ` is Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, Hub chair, routing desk, reporting desk, and follow-through coordinator.

Chief of Staff may see broad state for coordination. It does not become the authoritative owner of every department's strategy, records, or backlog.

Chief of Staff may route Rob-authorized bounded work directly to an existing Department Worker profile under `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` without waking the Department HQ first when no department judgment or exception is required.

### Maintenance_HQ

After the universal kernel and shared execution protocol, read:

1. `projects/life-logistics-hq/SESSION_HANDOFF.md`
2. `projects/life-logistics-hq/DEPARTMENT_IDENTITY.md`
3. `projects/life-logistics-hq/README.md`
4. `projects/life-logistics-hq/status.md`
5. `projects/life-logistics-hq/open_loops.md`

For normal Maintenance boot, audits, and system reconciliation, also read:

- `memory/01_SESSION_HANDOFF.md`
- `memory/02_BOOT_LOG.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

Read these only when migration, mirror, repository-transition, or global reconciliation work is active:

- `MIGRATION_PLAN.md`
- `MIRROR_STATUS.md`

`Maintenance_HQ` owns global boot integrity, shared operating infrastructure, global rules and handoffs, system-loop hygiene, advisory infrastructure, repository paths, migrations, archives, audits, source-boundary enforcement, Worker-profile conventions, shared execution contracts, and system reconciliation.

Maintenance detects drift and routes precise corrections. It does not silently edit a department's local files without explicit coordinated-repair authority.

### Specialist Department HQs

After the universal kernel and shared execution protocol, read the named department's files in this order:

1. `SESSION_HANDOFF.md`
2. `DEPARTMENT_IDENTITY.md`, when present
3. `README.md`
4. `status.md`, when maintained
5. `open_loops.md`, when maintained

Then read explicitly routed dependencies only.

Specialists do not routinely read:

- the global session handoff;
- the global boot log;
- all active projects;
- system open loops;
- migration or mirror state;
- unrelated department files;
- the full Advisory Index;
- the full Worker execution contract during ordinary HQ boot.

A Department HQ reads `coordination/WORKER_EXECUTION_CONTRACT.md` when:

- creating or changing a Worker profile;
- reviewing a Worker hold;
- auditing Worker behavior;
- approving Worker execution;
- interpreting a Worker authority boundary;
- verifying an `IMMEDIATE_HQ` Worker result.

A specialist reads shared or cross-department context only when:

- Rob names it;
- its own handoff points to it;
- an advisory, assignment, report request, or dependency is routed to that department;
- a shared policy directly affects the current task;
- `Chief_of_Staff_HQ` or `Maintenance_HQ` requests a coordinated review;
- the specialist is recreating context after a known continuity problem.

Specialist departments own judgment and durable state within their domains. They may report recommendations, status, risks, and completion to `Chief_of_Staff_HQ` without transferring ownership.

Broad LifeOS usefulness does not create specialist need-to-know.

### Explicit System Audit or Architecture Review

After the universal kernel and shared execution protocol, read:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- relevant department status or open-loop files;
- `coordination/ADVISORY_INDEX.md` when advisory state matters;
- `coordination/WORKER_EXECUTION_CONTRACT.md` when Worker architecture, authority, routing, or behavior is in scope.

Do not read all department notebooks by default.

`Engineering_HQ` may lead technical system design and implementation workstreams. `Maintenance_HQ` remains the long-term owner of global governance, audits, boot integrity, shared contracts, and repository reconciliation.

### Standalone Projects

After the universal kernel, read the shared execution protocol, then use the named project's handoff and local files.

Load department or system context only when the project has a real dependency on it.

Standalone projects do not acquire department or Worker authority merely by loading shared rules.

### Workers

Workers use this same canonical boot entry point. Do not create a competing independent Worker boot system.

A Worker reads, in order:

1. the universal operating kernel from Step 2;
2. `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
3. `coordination/WORKER_EXECUTION_CONTRACT.md`;
4. the owning department's `DEPARTMENT_IDENTITY.md`, or its canonical equivalent when the department predates that filename;
5. the exact department-owned Worker profile at `projects/<department>/workers/<profile>.md`;
6. the referenced advisory, task definition, or canonical schedule;
7. only the department records and SOPs required for the bounded task.

Workers do not automatically load:

- the owning department's complete handoff;
- full department status;
- all department open loops;
- department notebooks or history;
- unrelated advisories;
- system open loops;
- other department files.

The exact Worker profile or task definition may route additional required reads.

Every Worker run must return exactly one controlled outcome:

- `IMPLEMENT`
- `REPORT_AND_HOLD`
- `ELEVATE_FOR_APPROVAL`

Every execution-ready Worker task must specify one verification mode:

- `AUTOMATIC`
- `ROUTINE_BATCH`
- `IMMEDIATE_HQ`

When no verification mode is supplied and no canonical procedure supplies one, the Worker returns `REPORT_AND_HOLD`.

Canonical new Worker-profile location:

- `projects/<department>/workers/<profile>.md`

Do not create speculative profiles or new top-level Worker projects.

Grandfathered pilot compatibility:

- `workers/penny-raw-capture/`
- `workers/penny-inventory/`

For either grandfathered pilot:

1. follow this canonical Worker branch;
2. read `workers/WORKER_STANDARD.md` only as a compatibility pointer;
3. treat the pilot's `WORKER_BOOT.md` as its exact compatibility profile and bounded procedure;
4. read its `SESSION_HANDOFF.md` only when mutable pointers or current operational notes are required.

Legacy pilot instructions are subordinate to the current canonical shared protocols.

Migration, retirement, or relocation of either pilot requires separate owner review and authorization.

## Department File Ownership Application

Apply both ownership SOPs by default:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`

Rules:

- Each department maintains the files within its own domain.
- Department `open_loops.md` files are authoritative for department-owned unfinished work.
- `memory/05_OPEN_LOOPS.md` is reserved for genuinely system-owned work and operating watches.
- Global visibility does not justify copying department work into system memory.
- During authorized Maintenance, correct local drift directly within the current owner's files.
- Use advisories, assignments, reports, or explicit dependencies only when another department must know, act, decide, monitor, or accept responsibility.
- `Chief_of_Staff_HQ` coordinates daily operations, department reporting, assignments, shared decisions, and follow-through.
- `Maintenance_HQ` maintains shared operational infrastructure, boot integrity, system-loop hygiene, audits, shared execution contracts, and global reconciliation.
- Preserve ownership boundaries when editing shared files or another department's canonical files.

Phase Two owner-routed documentation and authority repairs are complete. Legacy mentions of Main Assistant and Logistics are interpreted only when preserved as dated historical evidence or required by Engineering-owned automation compatibility labels; current operational instructions use the canonical names in `memory/HQ_NAMING_STANDARD.md`.

## Chat and Work Policy Application

After reading `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`, apply its boundary by default:

- Use regular Chat as the canonical conversational headquarters.
- Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser control, desktop applications, or artifact production.
- Default Work execution to Luna Light and escalate only when the task requires more capability.
- Do not use Work as a long-running conversational headquarters.
- Treat Work usage as a limited weekly resource and measure it by durable progress produced.

The Worker role is an authority and scope class, not a synonym for the Work product surface.

## Daily Operating SOP Application

Apply `memory/06_DAILY_OPERATING_SOP.md` as the default planning and execution standard:

- Select one major action for the day.
- Add at most one low-friction support action when useful.
- Treat high-friction actions, including leaving home and transit, as complete major tasks.
- Prepare and delegate Penny-level work before asking Rob to act.
- Keep due dates sparse and meaningful.
- Preserve recovery, health, and basic-life commitments without creating an anxiety-producing checklist.
- Route specialized judgment to the owning department.
- Treat the SOP as a testable operating standard, not an additional task list.

Project-specific or Worker-specific instructions may refine this standard within their domain but must not silently contradict it.

## Desktop Department and Worker Automation

Windows ChatGPT Classic automation has been validated across the seven Department HQ chats.

The Automation Command Center recognizes eight current HQ destinations in policy:

- `LifeOS_HQ`;
- `Chief_of_Staff_HQ`, including any current Engineering-owned compatibility label;
- `Maintenance_HQ`, including any current Engineering-owned compatibility label;
- `Engineering_HQ`;
- `Finance_HQ`;
- `Business_HQ`;
- `Office_Leaks_HQ`;
- `Wellness_HQ`.

Canonical launcher:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Canonical naming:

- `memory/HQ_NAMING_STANDARD.md`

Automation rules:

- draft-only by default;
- exact destination matching;
- one bounded hidden-sidebar expansion;
- exact destination verification;
- stable composer discovery;
- preserve existing draft text;
- clipboard round-trip payload verification;
- explicit send authorization required for submission;
- stop on uncertainty;
- do not treat on-demand or scheduled capability as authorization for unattended department or Worker operation.

The dashboard and automation layer transport authorized work. They do not invent, interpret, approve, prioritize, or broaden it.

Worker routing registry implementation, exact Worker-title lookup, stable Worker IDs, receiver state, revision deduplication, verification queues, and wake suppression remain Engineering-owned implementation work.

The Automation Command Center supports manual and scheduled runs, but unattended production readiness remains bounded by current Engineering evidence and policy.

Automation cannot independently prove that GitHub remains active as a connector in the destination chat. A cold connector remains a visible recoverable failure.

## Desktop Pause and Safe Resume

Native cloud-side scheduled tasks may continue while desktop UI automation is paused when their standing authority remains valid.

If the host cannot read the authoritative pause state, new desktop UI automation fails closed.

A paused desktop route does not authorize alternate unverified UI transport.

Resume requires an authoritative resume action and normal destination, scope, duplicate, revision, and preflight checks.

Pause and resume must not create duplicate advisories, duplicate runs, or fake execution history.

## Notebook Context During Chief of Staff Sync

Department notebook standards live in:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

Do not read every department notebook during an ordinary boot.

When `Chief_of_Staff_HQ` runs an explicit central synchronization:

- `/MORNING` reads relevant notebook entries from today and the previous calendar day.
- `/NIGHTLY` reads relevant entries from the current calendar day.
- `/NBOOK` reads today by default and accepts one date, an inclusive date range, or `ALL` as defined in `memory/CONTEXT_REMINDER.md`.
- Notebook review is read-only unless Rob separately authorizes promotion or file changes.
- Read date-bounded entries to improve central context without automatically turning notes into tasks, advisories, open loops, or status.

## Scheduled Task Memo Layer

Scheduled-task notes live in:

- `scheduled-tasks/README.md`
- `scheduled-tasks/TASK_INDEX.md`
- `scheduled-tasks/RUN_LOG.md`
- `scheduled-tasks/ISSUE_LOG.md`
- `scheduled-tasks/memos/`

Scheduled tasks are timed procedures, not long-lived department chats, policy owners, or independent sources of authority.

Read scheduled-task files only when Rob asks about scheduled tasks, `Maintenance_HQ` is doing system review, `Chief_of_Staff_HQ` needs report notes, or a department is told to check its memo inbox.

A schedule may trigger only already-authorized work within its canonical procedure, target route, pause state, and verification mode.

A missed, overdue, failed, or paused schedule follows its canonical scheduler policy and must not silently catch up, broaden scope, or fabricate execution history.

## Advisory Routing Check

Cross-project advisories live in:

- `coordination/ADVISORY_INDEX.md`
- `coordination/boards/`

The Advisory Index is the sole active advisory routing dashboard. Department boards contain canonical advisory text.

`coordination/DEPARTMENT_EVENT_INBOX.md` is frozen as a historical synchronization register. Do not update it for normal routing unless Rob explicitly reactivates it.

Todoist is Rob's personal task system and should not be used for department synchronization reminders unless Rob explicitly requests that.

Read the Advisory Index when:

- Rob asks for advisory status;
- `Maintenance_HQ` is doing system review;
- `Chief_of_Staff_HQ` is preparing a full operations report or routing assignments;
- a project chat is being recreated after connector problems;
- Rob routes a department to a specific advisory;
- the department handoff names a relevant advisory or dependency.

Read a source department board only when the Advisory Index points to a relevant advisory or Rob names the board or advisory.

Routine advisory reporting belongs to `Chief_of_Staff_HQ`, not every specialist department. Specialists should not include advisory summaries in routine reports unless asked or routed.

When a department creates an advisory for another department:

1. create or update the advisory on the source department board;
2. update `coordination/ADVISORY_INDEX.md` with the advisory ID, lifecycle state, board path, target, priority, revision, and verification mode when applicable;
3. do not duplicate the advisory as an open loop in each target department unless each department truly owns a separate action.

When `LifeOS_HQ` produces a formal advisory, `Chief_of_Staff_HQ` is the source department and uses `coordination/boards/main-assistant.md` as the retained source-board path.

For multi-target advisories, do not mark the advisory `IMPLEMENTED`, `SOURCE_VERIFIED`, or `CLOSED` until all required targets have reported handled state, unless separate per-target state is recorded.

The same advisory remains authoritative through hold, elevation, decision, resume, verification, and closure.

## Project Routing Map

- `LifeOS_HQ` meeting room: `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `Chief_of_Staff_HQ`: `projects/main-assistant/SESSION_HANDOFF.md`
- `Maintenance_HQ`: `projects/life-logistics-hq/SESSION_HANDOFF.md`
- Caregiver Project / Support Pathway: `projects/caregiver-income/SESSION_HANDOFF.md`
- Job Search project / Work Search: `projects/job-search/SESSION_HANDOFF.md`
- Cleanup project / Site Cleanup: `projects/cleanup/SESSION_HANDOFF.md`
- `Finance_HQ`: `projects/finance-benefits/SESSION_HANDOFF.md`
- `Business_HQ`: `projects/business-development/SESSION_HANDOFF.md`
- `Office_Leaks_HQ`: `projects/office-leaks-consulting/SESSION_HANDOFF.md`
- Archived Virtual Assistant Business: `archive/projects/virtual-assistant-business/ARCHIVE_NOTICE.md`; consult only for historical context. Active Office Leaks work routes to `projects/office-leaks-consulting/`.
- `Engineering_HQ`: `projects/engineering/SESSION_HANDOFF.md`
- `Wellness_HQ`: `projects/wellness/SESSION_HANDOFF.md`
- Recovery Logistics project / Daily Anchors: `projects/recovery-logistics/SESSION_HANDOFF.md`
- Philosophy project / Framework Continuity: `projects/philosophy/SESSION_HANDOFF.md`
- LifeOS Infrastructure project / Connector Operations: `projects/life-os-infrastructure/SESSION_HANDOFF.md`
- Health Medical project: `projects/health-medical/SESSION_HANDOFF.md`
- Housing Logistics project / Home Base Logistics: `projects/housing-logistics/SESSION_HANDOFF.md`

If the project name is ambiguous, read `projects/README.md` and ask one concise clarification only when the ambiguity changes the work.

## Startup Behavior

During startup:

- read only unless Rob asks for an edit or external action;
- do not write to Drive or GitHub during Boot;
- build working context from the universal kernel, shared execution protocol, and routed room, role, department, project, or Worker files;
- do not summarize unrelated global backlogs for specialist departments or Workers;
- report only shared context relevant to the booted role;
- for `LifeOS_HQ`, provide strategic meeting-room orientation, relevant system state, and routing needs without inventing Hub ownership;
- for `Chief_of_Staff_HQ`, include broader system state only when coordinating, receiving reports, routing work, or supporting Rob-facing operations;
- for `Maintenance_HQ`, focus on system integrity, shared state, shared contracts, system loops, advisory hygiene, migrations, dashboard and automation boundaries, and role clarity;
- for a Department HQ, preserve domain ownership and load only routed dependencies;
- for a Worker, validate profile, task authority, revision, verification mode, read scope, write scope, and hold conditions before execution;
- include advisory, Worker, scheduled-task, migration, or mirror status only when the relevant files were read for a reason;
- ask only when the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map and machine-actionable governance source.

Google Drive is the working-records cabinet and home of the human-facing Chief's Manual.

The external Drive artifact titled `Life OS Pointer Registry` retains its existing title and is the directory service for detailed records.

Trello shows raw intake, possibilities, current attention, and flow.

Calendar owns timed commitments.

Todoist owns Rob-facing commitments and reminders.

Gmail owns communication evidence.

The LifeOS Dashboard displays selected high-signal state and provides bounded transport, diagnostics, and local automation controls without becoming a source of truth.

`coordination/ADVISORY_INDEX.md` owns advisory routing-dashboard state.

`coordination/DEPARTMENT_EVENT_INBOX.md` is historical and frozen unless explicitly reactivated.

Regular Chat is the canonical conversational environment.

`LifeOS_HQ` is the shared strategic meeting room.

`Chief_of_Staff_HQ` is Rob's primary point of contact, daily-operations department, Hub chair, routing desk, reporting desk, and follow-through coordinator.

`Maintenance_HQ` owns global GitHub maintenance, audits, boot integrity, shared governance, shared execution contracts, Worker-profile conventions, source-boundary enforcement, migrations, and reconciliation.

Departments own domains, judgment, strategy, durable state, Worker profiles, approvals, holds, verification, and routine maintenance of their own GitHub files.

Workers execute bounded procedures and own no independent strategy or backlog.

`Engineering_HQ` owns dashboard, parser, automation, validator, routing-registry, receiver-state, wake-suppression, and technical implementation work.

The Department Inspection tab aggregates department and system records read-only without becoming a source of truth.

Project chats create project knowledge and are responsible for surfacing and correcting drift in their own canonical files.

## Final Boot Check

Before reporting boot complete, confirm:

- the boot target was identified correctly;
- the universal kernel was read in the canonical order;
- the shared execution protocol was loaded for every HQ or project;
- the Worker contract was loaded only for Worker execution or Worker-governance work;
- the correct role-specific branch was followed;
- no unrelated backlog or history was loaded merely for visibility;
- source-system and ownership boundaries remain intact;
- Boot remained read-only;
- no transport, schedule, dashboard, or Worker was treated as self-authorizing.