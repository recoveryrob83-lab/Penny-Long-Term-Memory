# Department Event Inbox

Updated: 2026-07-04
Purpose: Lightweight Life OS register for advisory and synchronization events between Penny departments.

## Operating Rule

This file tracks abstract department-to-department sync events.

It is not a user task list.

Todoist owns Rob-facing action items. This file owns system synchronization state.

Keep entries short and non-sensitive.

## Source of Truth

- Advisory dashboard: `coordination/ADVISORY_INDEX.md`
- Advisory details: `coordination/boards/`
- Pending advisory standard: `coordination/PENDING_ADVISORY_BOARDS.md`
- Department notebook standard: `coordination/DEPARTMENT_NOTEBOOKS.md`

Pending boards and notebooks are local capture surfaces, not routed advisory channels.

## Current Open / Pending Events

| Event ID | Source | Target(s) | Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260704-003 | Chief Engineering Penny | Chief Engineering Penny | New | Engineering sync completed and connector reliability next work | Self-addressed advisory for next Engineering continuation packet. |

## Recent Closed / Ingested Events

| Event ID | Source | Target(s) | Status | Subject | Notes |
|---|---|---|---|---|---|
| ADV-20260704-005 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Notebooks for long-term idea capture | Life Logistics adopted optional Department Notebooks as a standard pattern and created the procedure file. |
| ADV-20260704-004 | Chief Engineering Penny | Life Logistics HQ | Closed | Department Pending Advisory Boards | Life Logistics adopted Pending Advisory Boards as a standard pattern and created the procedure file. |
| ADV-20260704-002 | Chief Business HQ | Chief Engineering Penny | Ingested | Drive connector reliability is a major Penny product risk | Engineering created Reliable Connector Execution Layer as first concrete research track. |
| ADV-20260704-001 | Chief Business HQ | Life Logistics HQ | Closed | Business HQ research, Drive architecture, and reboot-state update needed | Life Logistics ingested; Business Drive architecture resolved as Chief Business HQ > Business Development. |
| ADV-20260703-011 | Job Search HQ | Life Logistics HQ | Closed | Local job-search location design rule | Life Logistics ingested commute-aware job-search rule. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260704-005 | Life Logistics HQ | Read | Ingested | Department Notebook standard adopted. |
| ADV-20260704-004 | Life Logistics HQ | Read | Ingested | Pending Advisory Board standard adopted. |
| ADV-20260704-003 | Chief Engineering Penny | Unread | Pending | Self-addressed advisory for next Engineering continuation packet. |
| ADV-20260704-002 | Chief Engineering Penny | Read | Ingested | Reliable Connector Execution Layer research track created. |
| ADV-20260704-001 | Life Logistics HQ | Read | Ingested | Business Drive architecture resolved. |

## Notes

Historical advisory state is preserved in repository history and department boards.

Use this inbox for active synchronization/read/ingestion state, not as a permanent transcript.