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
| ADV-20260703-007 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | High | Ingested | Scheduled advisory watcher and inbox procedure | `coordination/boards/engineering.md` | Life Logistics HQ read and ingested the advisory; watcher procedure added here. |
| ADV-20260703-006 | 2026-07-03 | Chief Engineering Penny | Life Logistics HQ | High | Ingested | Engineering HQ online, Drive scaffold created, and event inbox need identified | `coordination/boards/engineering.md` | Life Logistics HQ read the advisory and created this event inbox as the first implementation. |

## Department Read Tracking

| Event ID | Department | Read Status | Ingest Status | Notes |
|---|---|---|---|---|
| ADV-20260703-007 | Life Logistics HQ | Read | Ingested | Advisory watcher v0.1 procedure added to this file. |
| ADV-20260703-006 | Life Logistics HQ | Read | Ingested | Engineering advisory read and Life OS memory updated. |

## Notes

Use this inbox when a department creates an advisory or synchronization event that another department needs to ingest.

The Advisory Index remains the official advisory dashboard.

This inbox is the working notification/register layer for department read and ingestion state.