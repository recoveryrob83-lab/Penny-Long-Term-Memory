# Scheduled Task Index

Updated: 2026-07-23
Purpose: Dashboard of scheduled procedures, owners, cadence, destination, and current lifecycle state.

## Task Table

| Task ID | Status | Owner / Role | Cadence | Purpose | Result Destination | Notes |
|---|---|---|---|---|---|---|
| ST-20260723-003 | Active Pilot | `Chief_of_Staff_HQ` | Hourly | Read-only advisory watcher: report meaningful signed advisory changes and follow-through needs without creating or executing work | Existing `Chief_of_Staff_HQ` conversation | Destination behavior is under bounded validation through `ADV-20260723-052`. Read and report only. No Worker dispatch, HQ wake, new chat, connector write, advisory closure, or follow-on work is authorized. |
| ST-20260703-002 | Paused | `Engineering_HQ` | Formerly daily at 6:00 AM America/Chicago | Department daily sync: boot Engineering context, read GitHub handoffs and advisories, consume Engineering-targeted context, and report meaningful updates | Existing `Engineering_HQ` conversation or the procedure's verified result path | Paused by Rob on 2026-07-11. Scheduler reliability has since been validated, but this task remains paused by deliberate operating choice. Resume only through explicit Rob authorization. Do not catch up missed runs. |
| ST-20260703-001 | Retired | Life Logistics HQ | One-time / superseded | Original scheduler capability test and standalone watcher experiment | `scheduled-tasks/memos/life-logistics-hq.md` | Historical owner label retained. Superseded by later department-sync and bounded watcher patterns. |

## Status Meanings

- **Proposed Test:** Defined for review but not authorized to run.
- **Active Pilot:** Authorized bounded procedure currently being validated.
- **Active:** Expected to run under stable standing authority.
- **Paused:** Intentionally stopped; elapsed time does not authorize resume.
- **Retired:** No longer used.
- **Failed:** Requires repair or explicit disposition before reuse.

## Owner Rule

The owner is the department identity responsible for the procedure's purpose, destination, report interpretation, and pause or retirement decision.

The scheduled platform transports timing. It does not own the procedure or create authority.

## Destination Rule

The result destination must be explicit.

A procedure that requires an existing HQ conversation must not create a new chat merely because the scheduled runtime can do so. A memo path, chat destination, advisory, or runtime record is a result surface, not a competing source of truth.

## Scheduled Procedure Guardrail

Scheduled procedures should prefer read-only analysis and reporting.

They must not modify GitHub, Google Drive, Todoist, Calendar, Gmail, Trello, or another system unless the exact canonical procedure and Rob's authority explicitly permit the write.

Missed, overdue, failed, or paused runs must not silently catch up, broaden scope, fabricate execution history, or retry uncertain external actions blindly.

## Historical Naming Rule

Current active and paused task rows use canonical names from `memory/HQ_NAMING_STANDARD.md`.

Retired rows and immutable run or issue evidence may retain historically accurate names, paths, identifiers, and wording.
