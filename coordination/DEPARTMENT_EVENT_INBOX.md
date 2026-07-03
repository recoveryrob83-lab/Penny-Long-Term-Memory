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
- Acknowledged: source advisory or event has been acknowledged.
- Closed: no further sync action is needed.

## Event Register

| Event ID | Date | Source | Target(s) | Priority | Status | Subject | Source Pointer | Notes |
|---|---|---|---|---|---|---|---|---|
| ADV-20260703-006 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | High | Ingested | Engineering HQ online, Drive scaffold created, and event inbox need identified | `coordination/boards/engineering.md` | Life Logistics HQ read the advisory and created this event inbox as the first implementation. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260703-006 | Life Logistics HQ | Read | Ingested | Engineering advisory read and Life OS memory updated. |

## Notes

Use this inbox when a department creates an advisory or synchronization event that another department needs to ingest.

The Advisory Index remains the official advisory dashboard.

This inbox is the working notification/register layer for department read and ingestion state.