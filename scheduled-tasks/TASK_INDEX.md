# Scheduled Task Index

Updated: 2026-07-03
Purpose: Dashboard of scheduled tasks, owners, cadence, and memo targets.

## Task Table

| Task ID | Status | Owner / Role | Cadence | Purpose | Memo Target | Notes |
|---|---|---|---|---|---|---|
| ST-20260703-001 | Proposed Test | Life Logistics HQ | One-time test | Test scheduled task boot, GitHub read access, memo writing, and handoff behavior | `scheduled-tasks/memos/life-logistics-hq.md` | First scheduler capability test |

## Status Meanings

- Proposed Test: not yet proven.
- Active: expected to run on schedule.
- Paused: intentionally stopped.
- Retired: no longer used.
- Failed: needs repair before reuse.

## Owner Rule

The owner is the department identity the scheduled task should boot as.

The memo target is where the task should leave its result for the long-lived department chat to read later.
