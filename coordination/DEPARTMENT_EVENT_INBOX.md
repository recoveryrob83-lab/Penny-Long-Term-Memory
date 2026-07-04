# Department Event Inbox

Updated: 2026-07-04
Purpose: Lightweight Life OS register for advisory and synchronization events between Penny departments.

## Operating Rule

This file tracks abstract department-to-department sync events.

It is not a user task list.

Todoist owns Rob-facing action items. This file owns system synchronization state.

Keep entries short and non-sensitive.

## Status Values

- New: event exists but has not been routed or read.
- Routed: Rob or a department has routed the event to the target.
- Read: target department has reported read.
- Ingested: target department has updated local context, handoffs, logs, or routing where needed.
- Partial: some target departments have read/ingested, but at least one target is still pending.
- Acknowledged: source advisory or event has been acknowledged.
- Closed: no further sync action is needed.

## Advisory Watcher v0.1 Procedure

A scheduled ChatGPT task may be used as a lightweight Advisory Watcher.

The watcher is a reporting layer only. It is not the source of truth.

Source of truth remains:

- `coordination/ADVISORY_INDEX.md` for advisory dashboard state.
- `coordination/DEPARTMENT_EVENT_INBOX.md` for department read and ingestion state.
- Department advisory boards for advisory details.

Note: standalone Advisory Watcher is no longer the preferred scheduled-task slot usage. Its reporting logic is folded into daily HQ sync workers.

## Daily HQ Sync Note

Daily HQ sync workers are the current preferred scheduled-task experiment for core HQs.

Engineering HQ Daily Sync is the first pilot, scheduled for 6:00 AM America/Chicago.

Daily sync workers should read boot/handoff/advisory context, consume advisories addressed to their department, and report meaningful updates. They should not modify systems unless Rob explicitly authorizes that behavior.

## Design Principles Note

Life OS design principles live in:

- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

No new platform enters Life OS until it solves a measured problem that cannot be cleanly solved by an existing component.

## Pending Advisory Board Note

Pending Advisory Board standard lives in:

- `coordination/PENDING_ADVISORY_BOARDS.md`

Pending boards are local department staging notebooks, not routed advisory channels.

## Event Register

| Event ID | Date | Source | Target(s) | Priority | Status | Subject | Source Pointer | Notes |
|---|---|---|---|---|---|---|---|---|
| ADV-20260704-004 | 2026-07-04 | Chief Engineering Penny | Life Logistics HQ | High | Closed | Department Pending Advisory Boards | `coordination/boards/engineering.md` | Life Logistics adopted Pending Advisory Boards as a standard pattern and created the procedure file. |
| ADV-20260704-003 | 2026-07-04 | Chief Engineering Penny | Chief Engineering Penny | High | New | Engineering sync completed and connector reliability next work | `coordination/boards/engineering.md` | Self-addressed advisory for next Engineering continuation packet. |
| ADV-20260704-002 | 2026-07-04 | Chief Business HQ | Chief Engineering Penny | High | Ingested | Drive connector reliability is a major Penny product risk | `coordination/boards/business.md` | Engineering ingested advisory and created Reliable Connector Execution Layer as first concrete research track. |
| ADV-20260704-001 | 2026-07-04 | Chief Business HQ | Life Logistics HQ | High | Closed | Business HQ research, Drive architecture, and reboot-state update needed | `coordination/boards/business.md` | Life Logistics re-consumed during daily boot; Business Drive architecture resolved as Chief Business HQ > Business Development. |
| ADV-20260703-011 | 2026-07-03 | Job Search HQ | Life Logistics HQ | Medium | Closed | Local job-search location design rule | `coordination/boards/job-search.md` | Life Logistics ingested rule; Job Search handoff and README updated with commute-aware local search rule. |
| ADV-20260703-010 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | Medium | Closed | Life OS design principle for new platforms | `coordination/boards/engineering.md` | Design-principles file created; Kanban/project-management tools deferred until measured pipeline-state pain appears. |
| ADV-20260703-009 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | High | Ingested | Scheduled HQ sync system experiment | `coordination/boards/engineering.md` | Life Logistics HQ ingested advisory; daily HQ sync pilot architecture recorded. |
| ADV-20260703-008 | 2026-07-03 | Recovery HQ | Life Logistics HQ / Main Assistant | Medium | Closed | Recovery Meeting Notes Workdesk created | `coordination/boards/recovery.md` | Life Logistics HQ and Main Assistant both consumed advisory; acknowledgement complete. |
| ADV-20260703-004 | 2026-07-03 | Chief Business HQ | Life Logistics HQ / Main Assistant | High | Closed | Frequent logistics updates needed for Penny platform research | `coordination/boards/business.md` | Life Logistics HQ and Main Assistant both consumed advisory; acknowledgement complete. |
| ADV-20260703-007 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ / Routed Departments | High | Closed | Scheduled advisory watcher and inbox procedure | `coordination/boards/engineering.md` | Procedure rollout completed across active HQs. No further routing needed. |
| ADV-20260703-006 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | High | Ingested | Engineering HQ online, Drive scaffold created, and event inbox need identified | `coordination/boards/engineering.md` | Life Logistics HQ read the advisory and created this event inbox as the first implementation. |
| ADV-20260703-002 | 2026-07-03 | Chief Wellness HQ | Life Logistics HQ | Medium | Closed | Wellness Admin reference update | `coordination/boards/wellness.md` | Advisory board exists; Life Logistics handled Wellness Admin reference update. |
| ADV-20260703-001 | 2026-07-03 | Recovery HQ | Recovery Logistics / Main Assistant / All Departments | Medium | Acknowledged | Daily Meditation workbench creation | `coordination/boards/recovery.md` | Recovery board and Advisory Index show acknowledged; Morning Meditation is a Recovery workbench, not a separate department. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260704-004 | Life Logistics HQ | Read | Ingested | Pending Advisory Board standard adopted. |
| ADV-20260704-003 | Chief Engineering Penny | Unread | Pending | Self-addressed advisory for next Engineering continuation packet. |
| ADV-20260704-002 | Chief Engineering Penny | Read | Ingested | Engineering status, handoff, and open loops updated; Reliable Connector Execution Layer research track created. |
| ADV-20260704-001 | Life Logistics HQ | Read | Ingested | Re-consumed during 2026-07-04 daily boot; Business Drive architecture resolved. |
| ADV-20260703-011 | Life Logistics HQ | Read | Ingested | Job Search handoff/README updated with commute-aware local search rule. |
| ADV-20260703-010 | Life Logistics HQ | Read | Ingested | Design-principles file created and platform-adoption principle recorded. |
| ADV-20260703-009 | Life Logistics HQ | Read | Ingested | Daily HQ sync pilot architecture recorded; observe Engineering HQ Daily Sync before additional rollout. |
| ADV-20260703-008 | Life Logistics HQ | Read | Ingested | Recovery Meeting Notes Workdesk recognized as a Recovery workbench/resource update. |
| ADV-20260703-008 | Main Assistant | Read | Ingested | Main Assistant consumed advisory and should route meeting-note capture or summary work to Recovery Meeting Notes Workdesk unless Rob asks otherwise. |
| ADV-20260703-004 | Life Logistics HQ | Read | Ingested | Life Logistics HQ will monitor Business HQ routing, structure, and cross-department cleanliness during active Penny Platform research. |
| ADV-20260703-004 | Main Assistant | Read | Ingested | Main Assistant should route relevant one-off business support to Chief Business HQ unless Rob says otherwise. |

## Notes

Use this inbox when a department creates an advisory or synchronization event that another department needs to ingest.

The Advisory Index remains the official advisory dashboard.

This inbox is the working notification/register layer for department read and ingestion state.