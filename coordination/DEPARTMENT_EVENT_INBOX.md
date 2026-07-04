# Department Event Inbox

Updated: 2026-07-03
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

The watcher should:

1. Check `coordination/ADVISORY_INDEX.md` and `coordination/DEPARTMENT_EVENT_INBOX.md` on a recurring cadence.
2. Identify open advisories or unread department inbox items.
3. Generate a concise report for Rob only when routing is needed.
4. Include copy-paste-ready routing messages Rob can paste into target HQ chats.
5. Avoid modifying GitHub unless Rob later explicitly approves that behavior.

Suggested watcher prompt:

```text
Check the Life OS GitHub advisory system. Read coordination/ADVISORY_INDEX.md and coordination/DEPARTMENT_EVENT_INBOX.md. If there are open advisories or unread department event items, report only the items needing routing. For each item, include the target department, advisory/event ID, board/path, priority, and a copy-paste-ready message Rob can paste into the target HQ chat. Do not modify GitHub. If nothing needs routing, say that no advisory routing is needed.
```

## Event Register

| Event ID | Date | Source | Target(s) | Priority | Status | Subject | Source Pointer | Notes |
|---|---|---|---|---|---|---|---|---|
| ADV-20260703-008 | 2026-07-03 | Recovery HQ | Life Logistics HQ / Main Assistant | Medium | Closed | Recovery Meeting Notes Workdesk created | `coordination/boards/recovery.md` | Life Logistics HQ and Main Assistant both consumed advisory; acknowledgement complete. |
| ADV-20260703-004 | 2026-07-03 | Chief Business HQ | Life Logistics HQ / Main Assistant | High | Closed | Frequent logistics updates needed for Penny platform research | `coordination/boards/business.md` | Life Logistics HQ and Main Assistant both consumed advisory; acknowledgement complete. |
| ADV-20260703-007 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ / Routed Departments | High | Closed | Scheduled advisory watcher and inbox procedure | `coordination/boards/engineering.md` | Procedure rollout completed across active HQs. No further routing needed. |
| ADV-20260703-006 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | High | Ingested | Engineering HQ online, Drive scaffold created, and event inbox need identified | `coordination/boards/engineering.md` | Life Logistics HQ read the advisory and created this event inbox as the first implementation. |
| ADV-20260703-002 | 2026-07-03 | Chief Wellness HQ | Life Logistics HQ | Medium | Closed | Wellness Admin reference update | `coordination/boards/wellness.md` | Advisory board exists; Life Logistics HQ handled folder reference update. |
| ADV-20260703-001 | 2026-07-03 | Recovery HQ | Recovery Logistics / Main Assistant / All Departments | Medium | Acknowledged | Daily Meditation workbench creation | `coordination/boards/recovery.md` | Recovery board and Advisory Index show acknowledged; Morning Meditation is a Recovery workbench, not a separate department. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260703-008 | Life Logistics HQ | Read | Ingested | Recovery Meeting Notes Workdesk recognized as a Recovery workbench/resource update. |
| ADV-20260703-008 | Main Assistant | Read | Ingested | Main Assistant consumed advisory and should route meeting-note capture or summary work to Recovery Meeting Notes Workdesk unless Rob asks otherwise. |
| ADV-20260703-004 | Life Logistics HQ | Read | Ingested | Life Logistics HQ will monitor Business HQ routing, structure, and cross-department cleanliness during active Penny Platform research. |
| ADV-20260703-004 | Main Assistant | Read | Ingested | Main Assistant consumed advisory and should route relevant one-off business support to Chief Business HQ unless Rob says otherwise. |
| ADV-20260703-007 | Life Logistics HQ | Read | Ingested | Advisory watcher v0.1 procedure added to this file. |
| ADV-20260703-007 | Chief Wellness HQ | Read | Ingested | Chief Wellness HQ updated handoff, identity, README, status, and open loops for the advisory board + Advisory Index + Department Event Inbox workflow. |
| ADV-20260703-007 | Caregiver Project HQ | Read | Ingested | Caregiver Project HQ updated README, department identity, and advisory board for Advisory Index + Department Event Inbox workflow. |
| ADV-20260703-007 | Recovery HQ | Read | Ingested | Recovery HQ updated handoff, department identity, and README for Advisory Index + Department Event Inbox workflow. |
| ADV-20260703-007 | Philosophy HQ | Read | Ingested | Philosophy HQ updated handoff, department identity, README, status, open loops, and advisory board note for Advisory Index + Department Event Inbox workflow. |
| ADV-20260703-006 | Life Logistics HQ | Read | Ingested | Engineering advisory read and Life OS memory updated. |
| ADV-20260703-002 | Life Logistics HQ | Read | Ingested | Life Logistics HQ handled Wellness Admin reference update. |
| ADV-20260703-002 | Chief Wellness HQ | Read | Ingested | Chief Wellness HQ created Wellness board and updated local advisory workflow references. |
| ADV-20260703-001 | Recovery HQ | Read | Ingested | Recovery HQ created, acknowledged, and locally ingested Morning Meditation as a Recovery workbench. |

## Notes

Use this inbox when a department creates an advisory or synchronization event that another department needs to ingest.

The Advisory Index remains the official advisory dashboard.

This inbox is the working notification/register layer for department read and ingestion state.