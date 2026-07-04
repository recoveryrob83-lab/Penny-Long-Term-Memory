# Scheduled Task Index

Updated: 2026-07-03
Purpose: Dashboard of scheduled tasks, owners, cadence, and memo targets.

## Task Table

| Task ID | Status | Owner / Role | Cadence | Purpose | Memo Target | Notes |
|---|---|---|---|---|---|---|
| ST-20260703-002 | Active Pilot | Chief Engineering Penny | Daily at 6:00 AM America/Chicago | Engineering HQ daily sync: boot Engineering context, read GitHub handoffs/advisories, consume Engineering-targeted advisories, and report meaningful updates | TBD / Engineering HQ chat response | First daily HQ sync pilot. Should not modify systems unless Rob explicitly authorizes. |
| ST-20260703-001 | Retired | Life Logistics HQ | One-time / superseded | Original scheduler capability test / standalone watcher concept | `scheduled-tasks/memos/life-logistics-hq.md` | Superseded by daily HQ sync model. |

## Status Meanings

- Proposed Test: not yet proven.
- Active Pilot: currently being tested.
- Active: expected to run on schedule.
- Paused: intentionally stopped.
- Retired: no longer used.
- Failed: needs repair before reuse.

## Owner Rule

The owner is the department identity the scheduled task should boot as.

The memo target is where the task should leave its result for the long-lived department chat to read later, if memo writing proves useful.

## Scheduled Sync Guardrail

Scheduled sync tasks should prefer read-only analysis and reporting.

They should not modify GitHub, Google Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.