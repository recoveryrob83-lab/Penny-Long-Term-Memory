# Scheduled Tasks

Updated: 2026-07-03
Purpose: Architecture notes for ChatGPT scheduled tasks used by Life OS.

## Role

Scheduled tasks are experimental Life OS sync workers.

The current preferred model is daily HQ sync for core departments, not many small standalone watcher services.

## Current Understanding

Scheduled-task slots appear scarce, so they should be treated as premium Life OS infrastructure.

The standalone Advisory Watcher concept has been retired as preferred slot usage. Its useful behavior is folded into daily HQ sync prompts.

## Core Daily Sync Candidates

Likely core sync slots:

1. Life Logistics HQ Sync
2. Main Assistant Sync
3. Chief Finance Sync
4. Chief Business Sync
5. Chief Engineering Sync

## Active Pilot

`Engineering HQ Daily Sync` is the first pilot.

Cadence: daily at 6:00 AM America/Chicago.

Purpose: test whether a scheduled sync can preserve department identity, read GitHub boot/handoff/advisory context, consume Engineering-targeted advisories, and report useful updates without unwanted writes.

## Operating Rule

Scheduled sync workers should prefer read-only analysis and reporting.

They should not modify GitHub, Google Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.

They should report only when there are meaningful updates, advisories requiring routing, documentation changes to recommend, or issues needing action.

## Core Files

- `TASK_INDEX.md`: list of scheduled tasks and their intended owner.
- `RUN_LOG.md`: short record of successful task runs.
- `ISSUE_LOG.md`: short record of failed, partial, blocked, or confusing runs.
- `templates/`: standard memo formats.
- `memos/`: department-specific inboxes, if memo writing proves useful.

## Memo Rule

Memos should be short, dated, and operational.

Do not store sensitive details here.

Store task result, source pointers, routing, and next action only.

## Department Read Pattern

During boot or sync, a department may check its own memo inbox if Rob asks or if its handoff says scheduled task memos are relevant.

Life Logistics HQ may check the index, run log, issue log, and relevant memo inboxes during system refresh or housekeeping.