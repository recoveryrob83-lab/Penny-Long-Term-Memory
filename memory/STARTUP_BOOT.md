# Startup Boot

Updated: 2026-07-18
Project: Life OS / Life OS Maintenance HQ / Penny Long-Term Memory
Purpose: Canonical startup and routing procedure for fresh Penny chats, LifeOS HQ, departments, projects, and workers.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

## Boot Principle

Use a small universal operating kernel, then load only the context required by the named room, role, department, project, or worker.

Do not make every specialist read the global handoff, all active projects, all system loops, migration state, or unrelated department backlogs.

Short form:

> Shared rules are universal. Operational state is role-routed.

Boot loads context. Sync compares context with authoritative state. Boot does not authorize maintenance, and Sync is read-only by default.

When both are requested, complete Boot first, then perform a separate read-only Sync report.

## Step 1: Identify the Boot Target

Before reading beyond the universal kernel, determine whether Rob is booting:

- `LifeOS HQ`, the central meeting room;
- `Chief of Staff HQ`;
- `Life OS Maintenance HQ`;
- one of the specialist departments;
- a standalone project;
- a narrow worker;
- an explicit system audit or architecture review.

When Rob names a room, department, project, or worker, use that route. Do not broaden the boot merely because additional files are available.

Legacy display names are interpreted through:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `memory/HQ_NAMING_STANDARD.md`

Filesystem paths remain unchanged unless a separate migration is authorized.

## Step 2: Universal Operating Kernel

LifeOS HQ, departments, projects, Chief of Staff, Life OS Maintenance, and explicit system-review chats read these files in order:

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

ChatGPT Project Instructions are Layer Zero and may already be active before boot. The GitHub copy is the versioned canonical deployment source used to verify, audit, and reconcile the deployed Project Settings text.

The Hub Operating Contract defines the current authority map, official role names, legacy-name translation, Hub action transfer, and reporting structure.

The universal kernel defines command meaning, safety, source boundaries, file ownership, open-loop ownership, Chat versus Work usage, and the default daily operating standard.

The following are not universal boot files:

- `memory/01_SESSION_HANDOFF.md`
- `memory/02_BOOT_LOG.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- `MIGRATION_PLAN.md`
- `MIRROR_STATUS.md`

Read them only under the role-routed rules below.

## Step 3: Role-Routed Shared Context

### LifeOS HQ

LifeOS HQ is the shared meeting room. It is not a department and has no independent project subtree or backlog.

After the universal kernel, read:

1. `memory/01_SESSION_HANDOFF.md`
2. `memory/04_ACTIVE_PROJECTS.md`
3. `memory/05_OPEN_LOOPS.md`
4. `coordination/ADVISORY_INDEX.md` when advisory state, routing, or a cross-department decision is relevant

Read department files only when current coordination, a named dependency, a routed assignment, or the meeting topic requires them.

Inside the Hub:

- `[MAIN]` is Chief of Staff speaking as chair;
- department tags provide domain judgment and recommendations;
- Rob remains final authority;
- the Hub itself does not become the owner of work;
- real actions are transferred to one owning department and one authoritative destination;
- Hub-originated formal advisories use `coordination/boards/main-assistant.md` as the retained Chief of Staff source-board path.

Do not read all department notebooks or backlogs merely because a Hub meeting is broad.

### Chief of Staff HQ

After the universal kernel, read:

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

Chief of Staff HQ is Rob's primary point of contact, personal-assistant headquarters, daily-operations desk, Hub chair, routing desk, and follow-through coordinator.

Chief of Staff may see broad state for coordination. It does not become the authoritative owner of every department's strategy, records, or backlog.

### Life OS Maintenance HQ

After the universal kernel, read:

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

Life OS Maintenance HQ owns global boot integrity, shared operating infrastructure, global rules and handoffs, system-loop hygiene, advisory infrastructure, repository paths, migrations, archives, audits, source-boundary enforcement, and system reconciliation.

Maintenance detects drift and routes precise corrections. It does not silently edit a department's local files without explicit coordinated-repair authority.

### Specialist Departments

After the universal kernel, read the named department's files in this order:

1. `SESSION_HANDOFF.md`
2. `DEPARTMENT_IDENTITY.md`, when present
3. `README.md`
4. `status.md`, when maintained
5. `open_loops.md`, when maintained

Specialists do not routinely read:

- the global session handoff;
- the global boot log;
- all active projects;
- system open loops;
- migration or mirror state;
- unrelated department files;
- the full Advisory Index.

A specialist reads shared or cross-department context only when:

- Rob names it;
- its own handoff points to it;
- an advisory, assignment, report request, or dependency is routed to that department;
- a shared policy directly affects the current task;
- Chief of Staff or Life OS Maintenance requests a coordinated review;
- the specialist is recreating context after a known continuity problem.

Specialist departments own judgment and durable state within their domains. They may report recommendations, status, risks, and completion to Chief of Staff HQ without transferring ownership.

Broad LifeOS usefulness does not create specialist need-to-know.

### Explicit System Audit or Architecture Review

For an explicit cross-department audit, architecture review, or system report, read:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- relevant department status or open-loop files;
- `coordination/ADVISORY_INDEX.md` when advisory state matters.

Do not read all department notebooks by default.

Engineering may lead technical system design and implementation workstreams. Life OS Maintenance remains the long-term owner of global governance, audits, boot integrity, and repository reconciliation.

### Standalone Projects

Use the named project's handoff and local files after the universal kernel. Load department or system context only when the project has a real dependency on it.

### Workers

Workers do not follow the universal department boot unless their contract explicitly says so.

Worker boot order:

1. `workers/WORKER_STANDARD.md`
2. the worker's `WORKER_BOOT.md`
3. the worker's `SESSION_HANDOFF.md` only when mutable resource pointers or current operational notes are needed

Workers are narrow executors, not departments, HQs, or general LifeOS coordinators.

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
- Chief of Staff coordinates daily operations, department reporting, assignments, shared decisions, and follow-through.
- Life OS Maintenance maintains shared operational infrastructure, boot integrity, system-loop hygiene, audits, and global reconciliation.
- Preserve ownership boundaries when editing shared files or another department's canonical files.

Legacy mentions of Main Assistant and Logistics in files not yet updated are interpreted as Chief of Staff HQ and Life OS Maintenance HQ under the Hub Operating Contract.

## Chat and Work Policy Application

After reading `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`, apply its boundary by default:

- Use regular Chat as the canonical conversational headquarters.
- Use Chat for planning, department coordination, ordinary reasoning, GitHub synchronization, and light connector work where available.
- Use Work only for bounded execution requiring local files, terminal access, coding, testing, browser control, desktop applications, or artifact production.
- Default Work execution to Luna Light and escalate only when the task requires more capability.
- Do not use Work as a long-running conversational headquarters.
- Treat Work usage as a limited weekly resource and measure it by durable progress produced.

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

Project-specific instructions may refine this standard within their domain but must not silently contradict it.

## Desktop Department Automation

Windows ChatGPT Classic automation has been validated across the seven department HQ chats.

The Automation Command Center recognizes eight exact destinations:

- LifeOS HQ;
- Chief of Staff HQ through the current `Main Assistant HQ` automation label until Engineering updates it;
- Life OS Maintenance HQ through the current `Logistics HQ` automation label until Engineering updates it;
- Engineering HQ;
- Finance HQ;
- Business HQ;
- Office Leaks HQ;
- Wellness HQ.

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
- do not treat on-demand or scheduled capability as authorization for unattended department operation.

The Automation Command Center supports manual and scheduled runs, but unattended production readiness remains incomplete. Engineering HQ Daily Sync remains paused until Rob explicitly resumes it after restart, overdue-run, recurrence, recovery, and preflight boundaries are safe enough.

Automation cannot independently prove that GitHub remains active as a connector in the destination chat. A cold connector remains a visible recoverable failure.

## Notebook Context During Chief of Staff Sync

Department notebook standards live in:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

Do not read every department notebook during an ordinary boot.

When Chief of Staff runs an explicit central synchronization:

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

Scheduled tasks are not long-lived department chats. Treat them as experimental timed prompts unless later proven stable.

Read scheduled-task files only when Rob asks about scheduled tasks, Life OS Maintenance is doing system review, Chief of Staff needs report notes, or a department is told to check its memo inbox.

Engineering HQ Daily Sync remains paused. Existing scheduling capability does not reactivate it.

## Worker Layer

Life OS workers live under:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`
- `workers/<worker-name>/`

Current worker routing:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Raw Capture Worker resource handoff: `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`
- Penny Inventory Worker resource handoff: `workers/penny-inventory/SESSION_HANDOFF.md`

If Rob names a worker, use the worker boot instead of treating it as a project department.

## Advisory Routing Check

Cross-project advisories live in:

- `coordination/ADVISORY_INDEX.md`
- `coordination/boards/`

The Advisory Index is the sole active advisory routing dashboard. Department boards contain canonical advisory text.

`coordination/DEPARTMENT_EVENT_INBOX.md` is frozen as a historical synchronization register. Do not update it for normal routing unless Rob explicitly reactivates it.

Todoist is Rob's personal task system and should not be used for department synchronization reminders unless Rob explicitly requests that.

Read the Advisory Index when:

- Rob asks for advisory status;
- Life OS Maintenance is doing system review;
- Chief of Staff is preparing a full operations report or routing assignments;
- a project chat is being recreated after connector problems;
- Rob routes a department to a specific advisory;
- the department handoff names a relevant advisory or dependency.

Read a source department board only when the Advisory Index points to a relevant advisory or Rob names the board or advisory.

Routine advisory reporting belongs to Chief of Staff, not every specialist department. Specialists should not include advisory summaries in routine reports unless asked or routed.

When a department creates an advisory for another department:

1. create the advisory on the source department board;
2. update `coordination/ADVISORY_INDEX.md` with the advisory ID, status, board path, and targets;
3. do not duplicate the advisory as an open loop in each target department unless each department truly owns a separate action.

When LifeOS HQ produces a formal advisory, Chief of Staff HQ is the source department and uses `coordination/boards/main-assistant.md` as the retained source-board path.

For multi-target advisories, do not mark fully acknowledged or implemented until all required targets have reported handled status, unless separate per-target status is recorded.

## Project Routing Map

- LifeOS HQ meeting room: `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- Chief of Staff HQ: `projects/main-assistant/SESSION_HANDOFF.md`
- Life OS Maintenance HQ: `projects/life-logistics-hq/SESSION_HANDOFF.md`
- Caregiver Project HQ / Support Pathway: `projects/caregiver-income/SESSION_HANDOFF.md`
- Job Search HQ / Work Search: `projects/job-search/SESSION_HANDOFF.md`
- Cleanup Project HQ / Site Cleanup: `projects/cleanup/SESSION_HANDOFF.md`
- Finance HQ: `projects/finance-benefits/SESSION_HANDOFF.md`
- Business HQ: `projects/business-development/SESSION_HANDOFF.md`
- Office Leaks HQ: `projects/office-leaks-consulting/SESSION_HANDOFF.md`
- Legacy Virtual Assistant Business: `projects/virtual-assistant-business/SESSION_HANDOFF.md` redirects to Office Leaks and is historical only.
- Engineering HQ: `projects/engineering/SESSION_HANDOFF.md`
- Wellness HQ: `projects/wellness/SESSION_HANDOFF.md`
- Recovery Logistics / Daily Anchors: `projects/recovery-logistics/SESSION_HANDOFF.md`
- Philosophy HQ / Framework Continuity: `projects/philosophy/SESSION_HANDOFF.md`
- Life OS Infrastructure / Connector Operations: `projects/life-os-infrastructure/SESSION_HANDOFF.md`
- Health Medical HQ: `projects/health-medical/SESSION_HANDOFF.md`
- Housing Logistics HQ / Home Base Logistics: `projects/housing-logistics/SESSION_HANDOFF.md`

If the project name is ambiguous, read `projects/README.md` and ask one concise clarification only when the ambiguity changes the work.

## Startup Behavior

During startup:

- read only unless Rob asks for an edit or external action;
- do not write to Drive or GitHub during Boot;
- build working context from the universal kernel plus the routed room, role, department, or project files;
- do not summarize unrelated global backlogs for specialist departments;
- report only shared context relevant to the booted role;
- for LifeOS HQ, provide meeting-room orientation, relevant system state, and routing needs without inventing Hub ownership;
- for Chief of Staff, include broader system state only when coordinating, receiving reports, or routing work;
- for Life OS Maintenance, focus on system integrity, shared state, system loops, advisory hygiene, migrations, dashboard and automation boundaries, and role clarity;
- include advisory, worker, scheduled-task, migration, or mirror status only when the relevant files were read for a reason;
- ask only when the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map.

Google Drive is the working-records cabinet and home of the human-facing Chief's Manual.

The Life OS Pointer Registry in Drive is the directory service for detailed records.

Trello shows raw intake, current attention, and flow.

Calendar owns timed commitments.

Todoist owns Rob-facing commitments and reminders.

Gmail owns communication evidence.

The LifeOS Dashboard displays selected high-signal state from authoritative systems and provides bounded local automation controls.

`coordination/ADVISORY_INDEX.md` owns advisory dashboard state.

`coordination/DEPARTMENT_EVENT_INBOX.md` is historical and frozen unless explicitly reactivated.

Regular Chat is the canonical conversational environment.

LifeOS HQ is the shared meeting room.

Chief of Staff HQ is Rob's primary point of contact, daily-operations department, Hub chair, routing desk, and follow-through coordinator.

Life OS Maintenance HQ owns global GitHub maintenance, audits, boot integrity, shared governance, source-boundary enforcement, migrations, and reconciliation.

Departments own domains, judgment, strategy, durable state, and routine maintenance of their own GitHub files.

Engineering owns dashboard, parser, automation, validator, and technical implementation work.

The Department Inspection tab aggregates department and system records read-only without becoming a source of truth.

Workers execute narrow procedures under stable contracts.

Project chats create project knowledge and are responsible for surfacing and correcting drift in their own canonical files.