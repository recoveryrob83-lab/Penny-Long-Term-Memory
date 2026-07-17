# Startup Boot

Updated: 2026-07-18
Project: Life OS / Logistics HQ / Penny Long-Term Memory
Purpose: Canonical startup and routing procedure for fresh Penny chats, departments, projects, and workers.

## Repository

Open:

`recoveryrob83-lab/Penny-Long-Term-Memory`

## Boot Principle

Use a small universal operating kernel, then load only the context required by the named role or project.

Do not make every specialist read the global handoff, all active projects, all system loops, migration state, or unrelated department backlogs.

Short form:

> Shared rules are universal. Operational state is role-routed.

## Step 1: Identify the Boot Target

Before reading beyond the universal kernel, determine whether Rob is booting:

- Main Assistant HQ;
- Logistics HQ;
- one of the specialist departments;
- a standalone project;
- a narrow worker;
- a general LifeOS coordination or system-review chat.

When Rob names a department, project, or worker, use that route. Do not broaden the boot merely because additional files are available.

## Step 2: Universal Operating Kernel

Departments, projects, Main Assistant, Logistics, and general LifeOS coordination read these files in order:

1. `memory/STARTUP_BOOT.md`
2. `memory/00_START_HERE.md`
3. `memory/CONTEXT_REMINDER.md`
4. `memory/03_OPERATIONAL_RULES.md`
5. `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
6. `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
7. `projects/life-os-infrastructure/CHAT_WORK_EXECUTION_POLICY.md`
8. `memory/06_DAILY_OPERATING_SOP.md`

The universal kernel defines identity, command meaning, safety, source boundaries, file ownership, open-loop ownership, Chat versus Work usage, and the default daily operating standard.

The following are no longer universal boot files:

- `memory/01_SESSION_HANDOFF.md`
- `memory/02_BOOT_LOG.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- `MIGRATION_PLAN.md`
- `MIRROR_STATUS.md`

Read them only under the role-routed rules below.

## Step 3: Role-Routed Shared Context

### Main Assistant HQ

After the universal kernel, read:

1. `projects/main-assistant/SESSION_HANDOFF.md`
2. `projects/main-assistant/DEPARTMENT_IDENTITY.md`
3. `projects/main-assistant/README.md`
4. `projects/main-assistant/status.md`
5. `projects/main-assistant/open_loops.md`

Read these shared files when coordinating broad daily operations, cross-department synthesis, a hub report, or a system decision:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

Read `memory/02_BOOT_LOG.md` only when recent boot-history changes, migration history, or a recreated chat makes it relevant.

Main Assistant may see broad state for coordination. It does not become the authoritative owner of each department's backlog.

### Logistics HQ

After the universal kernel, read:

1. `projects/life-logistics-hq/SESSION_HANDOFF.md`
2. `projects/life-logistics-hq/DEPARTMENT_IDENTITY.md`
3. `projects/life-logistics-hq/README.md`
4. `projects/life-logistics-hq/status.md`
5. `projects/life-logistics-hq/open_loops.md`

For normal Logistics boot and system maintenance, also read:

- `memory/01_SESSION_HANDOFF.md`
- `memory/02_BOOT_LOG.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

Read these only when migration, mirror, repository-transition, or global reconciliation work is active:

- `MIGRATION_PLAN.md`
- `MIRROR_STATUS.md`

Logistics owns global boot integrity, shared infrastructure, system-loop hygiene, migrations, repository-path disposition, cross-project audits, and system reconciliation.

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
- an advisory or dependency is routed to that department;
- a shared policy directly affects the current task;
- Main Assistant or Logistics requests a coordinated review;
- the specialist is recreating context after a known continuity problem.

Broad LifeOS usefulness does not create specialist need-to-know.

### General LifeOS Coordination or System Review

For an explicit cross-department audit, architecture review, or system report, read:

- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`
- relevant department status or open-loop files;
- `coordination/ADVISORY_INDEX.md` when advisory state matters.

Do not read all department notebooks by default.

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
- During routine syncs, correct local drift directly when authorized.
- Use advisories or explicit dependencies only when another department must know, act, decide, monitor, or accept responsibility.
- Main Assistant coordinates shared policy and cross-department decisions.
- Logistics maintains shared operational infrastructure, boot integrity, system-loop hygiene, and cross-project audits.
- Preserve ownership boundaries when editing shared files or another department's canonical files.

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

Windows ChatGPT Classic department automation is operational across all seven HQs.

Canonical launcher:

- `apps/lifeos-dashboard/automation/draft_department_boot.py`

Canonical naming:

- `memory/HQ_NAMING_STANDARD.md`

Automation rules:

- draft-only by default;
- exact HQ matching;
- one bounded hidden-sidebar expansion;
- exact destination verification;
- stable Group composer discovery;
- preserve existing draft text;
- clipboard round-trip payload verification;
- explicit `--send` authorization required for submission;
- stop on uncertainty;
- do not treat on-demand automation as authorization for unattended scheduled boots.

The automation cannot independently prove that GitHub remains active as a connector in the destination chat. A cold connector remains a visible recoverable soft failure.

## Notebook Context During Hub Sync

Department notebook standards live in:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

Do not read every department notebook during an ordinary boot.

When Main Assistant runs an explicit hub synchronization:

- `/MORNING` reads notebook entries from today and the previous calendar day.
- `/NIGHTLY` reads notebook entries from the current calendar day.
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

Read scheduled-task files only when Rob asks about scheduled tasks, Logistics is doing system review, Main Assistant needs morning-report notes, or a department is told to check its memo inbox.

Engineering HQ Daily Sync remains paused. Validated on-demand desktop automation does not reactivate unattended scheduled execution.

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
- Logistics is doing system review;
- Main Assistant is preparing a full operations report;
- a project chat is being recreated after connector problems;
- Rob routes a department to a specific advisory;
- the department handoff names a relevant advisory or dependency.

Read a source department board only when the Advisory Index points to a relevant advisory or Rob names the board or advisory.

Routine advisory reporting belongs to Main Assistant, not every specialist department. Specialists should not include advisory summaries in routine reports unless asked.

When a department creates an advisory for another department:

1. Create the advisory on the source department board.
2. Update `coordination/ADVISORY_INDEX.md` with the advisory ID, status, board path, and targets.
3. Do not duplicate the advisory as an open loop in each target department unless each department truly owns a separate action.

For multi-target advisories, do not mark fully acknowledged or implemented until all required targets have reported handled status, unless separate per-target status is recorded.

## Project Routing Map

- Logistics HQ: `projects/life-logistics-hq/SESSION_HANDOFF.md`
- Main Assistant HQ: `projects/main-assistant/SESSION_HANDOFF.md`
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

- Read only unless Rob asks for an edit or external action.
- Do not write to Drive or GitHub during boot.
- Build working context from the universal kernel plus the routed role or project files.
- Do not summarize unrelated global backlogs for specialist departments.
- Report only shared context that is relevant to the booted role.
- For Main Assistant, include broader system state only when coordinating or reporting across departments.
- For Logistics, focus on system integrity, shared state, system loops, advisory hygiene, migrations, dashboard and automation boundaries, and role clarity.
- Include advisory, worker, scheduled-task, migration, or mirror status only when the relevant files were read for a reason.
- Ask only when the next action is genuinely ambiguous.

## System Architecture

GitHub is the durable memory map.

Google Drive is the working-records cabinet.

The Life OS Pointer Registry in Drive is the directory service for detailed records.

Trello shows current attention and flow.

Calendar owns timed commitments.

Todoist owns Rob-facing commitments and reminders.

Gmail owns communication evidence.

The LifeOS Dashboard displays selected high-signal state from authoritative systems and provides local automation controls.

`coordination/ADVISORY_INDEX.md` owns advisory dashboard state.

`coordination/DEPARTMENT_EVENT_INBOX.md` is historical and frozen unless explicitly reactivated.

Regular Chat is the canonical conversational headquarters.

Work is the bounded execution environment for local computer and heavy implementation tasks.

Departments own domains, judgment, strategy, durable state, and routine maintenance of their own GitHub files.

Main Assistant coordinates daily operations, cross-department policy, and shared decisions.

Logistics maintains shared operational infrastructure, global hygiene, system-loop integrity, migrations, and cross-project audits.

Engineering owns dashboard and desktop-automation implementation.

The Department Inspection tab aggregates department and system records read-only without becoming a source of truth.

Workers execute narrow procedures under stable contracts.

Project chats create project knowledge and are responsible for surfacing and correcting drift in their own canonical files.
