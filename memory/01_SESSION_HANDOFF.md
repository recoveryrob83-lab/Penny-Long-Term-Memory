# System Session Handoff

Updated: 2026-07-18
Project: Life OS / Logistics HQ / Penny Long-Term Memory
Purpose: System-level baton pass for Main Assistant, Logistics, and explicit cross-department coordination. This file is not a mirror of department backlogs.

## Current System State

Life OS is operational with:

- GitHub as the durable memory and architecture map;
- Google Drive as the working-records cabinet;
- Trello as the visual attention and active-flow layer;
- Todoist as Rob-facing commitments and reminders;
- Calendar as the timed-commitment layer;
- Gmail as communication evidence;
- a locally running LifeOS Dashboard with Overview, Department Inspection, and Automation tabs;
- seven operational department HQ chats;
- validated Windows desktop automation for drafting or explicitly sending prompts to exact LifeOS destinations;
- an operational dashboard-integrated Automation Command Center with manual and scheduled runs, persistent history, and safety reporting;
- workers as narrow operational executors;
- Main Assistant as daily coordinator and primary conversational hub;
- Logistics as shared-infrastructure curator, boot maintainer, migration owner, and cross-project auditor.

GitHub remains abstract. Detailed financial, medical, business, personal, credential, and operational records stay in their owning source systems.

## Ownership and Boot Architecture

Implemented on 2026-07-18:

- department `open_loops.md` files are authoritative for department-owned unfinished work;
- `memory/05_OPEN_LOOPS.md` is now the System Open Loops file and no longer mirrors department backlogs;
- a small universal operating kernel replaced universal loading of the global handoff, boot log, active projects, system loops, migration plan, and mirror status;
- Main Assistant and Logistics receive broader shared context according to role;
- specialist departments load their own files plus only explicitly relevant advisories, dependencies, shared policies, or routed context;
- the Department Inspection tab aggregates all seven departments plus System read-only without becoming a source of truth.

Canonical rules:

- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`
- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `memory/STARTUP_BOOT.md`
- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`

Short form:

> Shared rules are universal. Operational state is role-routed. Visibility is not ownership.

## Current System Coordination

One active system coordination package remains:

- Department ownership and role-routed boot reconciliation.
- Lead: Engineering HQ.
- Coordination: Logistics HQ and Main Assistant HQ.
- Canonical record: `projects/engineering/notebook/NOTE-20260717-014-department-ownership-and-dashboard-inspection.md`.

Remaining system work:

1. refresh and restart the local dashboard after the latest parser and source changes;
2. verify that confirmed duplicate findings disappear and warning counts remain useful;
3. inspect any remaining findings individually;
4. reconcile any additional global summaries or boot assumptions exposed by the inspector;
5. close the system coordination wrapper when ownership and routing remain stable in ordinary use.

Detailed department work belongs in each department's handoff, status, and open-loop files.

## Department Inspection Evidence

The read-only Department Inspection MVP is locally validated.

First live baseline:

- 458 normalized records;
- 4 findings;
- 101 records with warnings.

After evidence-based parser and presentation tuning:

- 459 normalized records;
- 4 findings;
- 15 records with warnings.

The remaining findings exposed:

- one Engineering state/priority schema defect;
- a broad Chat HQ watch duplicated across Engineering, Logistics, and System;
- Legacy Virtual Assistant folder disposition mirrored across Logistics, Business, and System;
- speculative registry-reference placeholders in several departments.

Targeted cleanup completed:

- Engineering now separates lifecycle state from priority;
- the system Chat HQ watch remains while department mirrors were removed;
- Logistics solely owns Legacy Virtual Assistant folder disposition;
- Business and System Legacy VA mirrors were removed;
- speculative registry-reference placeholders were removed;
- explicit priority-column parsing and test coverage were added.

Local restart verification is still pending because the running Python process must load the parser change.

## Dashboard and Automation Boundaries

The dashboard is a visibility and local-control layer, not a replacement source of truth.

Verified live sources:

- GitHub;
- Trello;
- Todoist;
- Google Calendar private iCal.

Guarded GitHub auto-sync may fast-forward only when local `main` is clean and strictly behind. It does not resolve conflicts, discard work, rebase, reset, or authorize broad automatic writes.

The Automation Command Center supports exact destinations, protected canonical prompts, saved and custom prompts, draft or explicitly confirmed send mode, one-time/daily/weekly schedules, separate Scheduled Jobs and Run History, and structured failure reporting.

Scheduling is operational but not yet production-ready for fully unattended Windows use. Remaining technical evidence and implementation belong to Engineering, including restart/overdue behavior, repeated recurrence, collapsed-project recovery, scheduler preflight, missed-run policy, and possible Windows startup or service packaging.

Engineering HQ Daily Sync remains paused until Rob explicitly resumes it after the unattended-operation boundary is safe enough.

## Chat and Work Architecture

Regular Chat is the canonical conversational headquarters.

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

Main Assistant owns `/FLOW`, `/FLOW PROCESS`, and `/FLOW NOW` operation.

Canonical SOP:

- `coordination/TRELLO_FLOW_BOARD_SOP.md`

## Worker Layer

Active pilot workers:

- Penny Raw Capture Worker: `workers/penny-raw-capture/WORKER_BOOT.md`
- Penny Inventory Worker: `workers/penny-inventory/WORKER_BOOT.md`

Main Assistant owns authorized downstream processing. Engineering owns worker architecture and reliability guidance. Logistics owns durable worker routing and pointer hygiene.

Workers do not inherit department or system backlogs unless their contract explicitly requires a pointer.

## Advisory State

Current open advisories:

- None.

The Advisory Index is the live source of truth:

- `coordination/ADVISORY_INDEX.md`

Department Event Inbox remains frozen as historical context unless Rob explicitly reactivates it.

## Active Core

- Main Assistant HQ
- Logistics HQ
- Engineering HQ
- Finance HQ
- Business HQ
- Office Leaks HQ
- Wellness HQ
- Life OS Infrastructure as needed

Consolidated or dormant domains remain preserved rather than deleted.

## Source Boundaries

- GitHub: durable abstract state, architecture, ownership, pointers, and auditable changes.
- Drive: working documents, detailed records, and human-facing artifacts.
- Trello: current attention and flow.
- Todoist: Rob-facing commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Dashboard: read-only aggregation plus bounded local automation controls.
- Department files: authoritative department state.
- `memory/05_OPEN_LOOPS.md`: genuinely system-owned work and operating watches only.

## Best Next System Actions

- Verify the post-cleanup Department Inspection counts after the desktop connection and local dashboard process are available.
- Use remaining findings as audit prompts rather than automatic verdicts.
- Let departments maintain their own state during ordinary work.
- Let Main Assistant coordinate broad decisions without becoming the editor of every department backlog.
- Let Logistics maintain boot integrity, system-loop hygiene, migrations, and cross-project audits.
- Keep system records compact and close the current ownership-reconciliation wrapper once ordinary use proves the routing stable.

## Guiding Principle

GitHub is the map. Drive is the filing cabinet. Trello shows current flow. Calendar owns time. Todoist owns commitments and reminders. Gmail owns communications. The dashboard sees broadly without owning broadly. Departments own their work. Main coordinates. Logistics maintains the hallways.
