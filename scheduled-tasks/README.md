# Scheduled Tasks

Updated: 2026-07-23
Purpose: Architecture, authority, and continuity notes for ChatGPT scheduled procedures used by LifeOS.

## Role

Scheduled tasks are timed procedures. They are not long-lived department chats, policy owners, independent authorities, or competing sources of truth.

A schedule may trigger only already-authorized work within its canonical procedure, target route, pause state, duplicate controls, and verification boundary.

## Current Operating Model

Scheduled-task slots are limited operational infrastructure and should be used only when repeated delivery or condition checking produces demonstrated value.

Current patterns include:

- department sync procedures, when separately authorized;
- narrow read-only watchers, when their owner, destination, cadence, report condition, and non-action boundary are explicit;
- one-time bounded tests used to validate scheduling behavior.

Do not assume that every department needs a scheduled sync or watcher.

## Current Pilot State

### Engineering_HQ Daily Sync

`Engineering_HQ Daily Sync` was the first department-sync pilot.

- State: Paused by Rob.
- Former cadence: daily at 6:00 AM America/Chicago.
- Current interpretation: scheduler production reliability has been validated, but this specific unattended task remains paused by deliberate operating choice.
- Resume condition: Rob explicitly authorizes resume under the current architecture.
- No missed run should silently catch up.

### Chief_of_Staff_HQ Advisory Watcher

A separately authorized hourly read-only advisory watcher is currently associated with `Chief_of_Staff_HQ`.

- Purpose: report meaningful signed advisory changes and follow-through needs in the existing `Chief_of_Staff_HQ` conversation.
- Current validation: destination behavior is being tested through `ADV-20260723-052`.
- Authority ceiling: read and report only.
- It may not close advisories, create work, dispatch Workers, create chats, modify connectors, change priority, or broaden authority.

The watcher is not a replacement for the Advisory Index or source boards.

## Operating Rules

Scheduled procedures should:

- boot or load the correct bounded context;
- remain read-only unless exact standing authority permits a write;
- report only meaningful changes, exceptions, or requested summaries;
- suppress duplicate processing;
- preserve one owner and one authoritative record;
- fail closed when route, identity, scope, pause state, or authority is uncertain;
- distinguish no-change runs from failures;
- avoid creating a new chat when an existing authorized destination is required.

They should not modify GitHub, Google Drive, Todoist, Calendar, Gmail, Trello, or another system unless the exact canonical procedure and Rob's authority permit that action.

## Missed, Failed, and Paused Runs

A missed, overdue, failed, or paused schedule follows its canonical scheduler policy.

Do not:

- silently catch up every missed occurrence;
- fabricate execution history;
- broaden scope because a run is late;
- treat elapsed time as resume authority;
- retry an uncertain external action blindly.

## Core Files

- `TASK_INDEX.md`: current scheduled-task map, ownership, cadence, destination, and state.
- `RUN_LOG.md`: short historical record of successful task runs.
- `ISSUE_LOG.md`: short historical record of failed, partial, blocked, or confusing runs.
- `templates/`: standard memo formats.
- `memos/`: department-specific result inboxes when the canonical procedure uses them.

## Historical Evidence Rule

Run and issue logs may retain names and labels that were accurate when the event occurred. Current task rows and current instructions use the canonical names in `memory/HQ_NAMING_STANDARD.md`.

## Memo Rule

Memos should be short, dated, abstract, and operational.

Store only:

- task result;
- source pointers;
- routing outcome;
- verification state;
- smallest next action or review trigger.

Do not store sensitive details or create a competing work ledger.

## Department Read Pattern

A department may check its own scheduled-task memo inbox when Rob asks, its handoff requires it, or a current procedure routes a result there.

`Maintenance_HQ` may inspect the index, logs, and relevant memos during system review, reconciliation, scheduler governance, or authorized housekeeping. `Engineering_HQ` owns scheduler and automation implementation. `Chief_of_Staff_HQ` owns Rob-facing operational reporting and watcher destination behavior.
