# Scheduled Tasks

Updated: 2026-07-03
Purpose: Communication layer for scheduled ChatGPT tasks that run outside the long-lived Penny department chats.

## Role

Scheduled tasks are not the same as department chats.

A scheduled task should boot from GitHub, perform a narrow job, then leave a memo here so the relevant Penny department can see what happened later.

## Core Files

- `TASK_INDEX.md`: list of scheduled tasks and their intended owner.
- `RUN_LOG.md`: short record of successful task runs.
- `ISSUE_LOG.md`: short record of failed, partial, blocked, or confusing runs.
- `templates/`: standard memo formats.
- `memos/`: department-specific inboxes.

## Operating Rule

Scheduled tasks should prefer read-only analysis at first.

If a task produces a useful output, it should write a short memo to the right department inbox when write access is available.

If writing fails, the task should report the output directly in its own task response and note the failure.

## Memo Rule

Memos should be short, dated, and operational.

Do not store sensitive details here.

Store task result, source pointers, routing, and next action only.

## Department Read Pattern

During boot or sync, a department may check its own memo inbox if Rob asks or if its handoff says scheduled task memos are relevant.

Main Assistant may check `scheduled-tasks/memos/main-assistant.md` for pre-generated daily brief or itinerary items.

Life Logistics HQ may check the index, run log, issue log, and any relevant memo inbox during system refresh or housekeeping.
