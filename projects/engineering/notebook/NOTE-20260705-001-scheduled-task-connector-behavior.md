# NOTE-20260705-001 — Scheduled Task Connector Behavior

Date: 2026-07-05
Department: Chief Engineering Penny
Status: Active observation / early experiment results
Topic: Scheduled tasks, connector invocation, and execution-context behavior

## Summary

Rob reported new evidence that scheduled tasks can invoke connectors when the connector mention is manually included in the scheduled task prompt. This revises the earlier working assumption that scheduled tasks could not use connectors.

The failure mode from the earlier test appears to have been prompt construction rather than an inherent scheduled-task connector limitation.

## Observations So Far

### ST-001 — Gmail connector scheduled-task test

Result: PASS, per Rob's report.

Observed behavior:
- Rob manually created a scheduled task prompt containing a connector invocation.
- The scheduled task successfully used Gmail.
- The task did not create a new chat in that test.

Preliminary finding:
- Scheduled tasks can invoke at least some connectors when the connector reference is included correctly in the scheduled prompt.
- Gmail is confirmed working in one manual scheduled-task test.

### Earlier assistant-created scheduled task test

Result: Failed to invoke connector as intended, per prior observation.

Preliminary finding:
- When the assistant created the scheduled task with a connector tag, the tag did not translate through as an active connector invocation.
- This suggests connector invocation may depend on how the scheduled-task prompt is authored or serialized.
- The difference between manually creating a task and assistant-created task needs further testing.

### ST-002 — GitHub connector scheduled-task test

Status: Scheduled / pending at time of this note.

Task title: Engineering Notebook Check

Prompt purpose:
- Invoke `@GitHub`.
- Check repository `recoveryrob83-lab/Penny-Long-Term-Memory`.
- Read `projects/engineering/notebook/`.
- Identify and report the most recent Engineering notebook entry.
- Do not modify GitHub.

Scheduled timing:
- One-time run, approximately 10 minutes after creation on 2026-07-05.

Open question:
- Whether assistant-created scheduled tasks can successfully preserve and activate the `@GitHub` connector reference.

## Execution Context Observation

Rob observed that the successful Gmail scheduled-task test did not create a new chat.

This revises the execution-context model. Scheduled task execution context should not be treated as deterministic.

Possible behaviors now include:
1. Scheduled task creates a new chat.
2. Scheduled task runs in an existing scheduled-task thread or current task context.
3. Behavior may vary by platform, prompt construction, recurrence type, connector used, or OpenAI implementation details.

## Engineering Interpretation

The robust Life OS design should not depend on whether a scheduled task creates a new chat.

Instead, scheduled workers should be designed as context-agnostic workers:
- identify their role,
- bootstrap from durable memory,
- perform the assigned task,
- report results clearly,
- write only when explicitly authorized by the prompt,
- and avoid assuming prior conversation state.

Working architectural rule:

> Every scheduled worker must assume it is starting from an unknown execution context.

## Impact on Life OS Architecture

This finding reopens the possibility of scheduled HQ workers.

Potential use case:
- A daily Life Logistics scheduled worker invokes GitHub,
- reads `coordination/ADVISORY_INDEX.md` and `coordination/DEPARTMENT_EVENT_INBOX.md`,
- reports open advisories by target department,
- and only writes if explicitly authorized.

This could reduce Rob's manual burden by changing the workflow from:

`Manually boot every HQ to check advisories`

into:

`Run centralized advisory scan, then wake only departments with open routed items.`

## Current Connector Compatibility Matrix

| Connector | Scheduled Task Result | Evidence Level | Notes |
|---|---:|---:|---|
| Gmail | PASS | One manual test | Rob reported scheduled task successfully used Gmail. |
| GitHub | Pending | Test scheduled | Assistant-created task includes `@GitHub`; awaiting result. |
| Todoist | Unknown | Not tested | Needs scheduled-task connector test. |
| Google Calendar | Unknown | Not tested | Needs scheduled-task connector test. |
| Google Drive | Unknown | Not tested | Needs scheduled-task connector test. |
| Google Contacts | Unknown | Not tested | Needs scheduled-task connector test. |

## Risks and Caveats

- Do not generalize Gmail success to all connectors.
- Do not assume assistant-created scheduled tasks serialize connector references the same way manually-created tasks do.
- Do not assume new-chat behavior or same-thread behavior.
- Do not allow scheduled workers to perform production writes until read-only connector reliability is characterized.
- Treat this as early evidence, not a finalized standard.

## Recommended Next Tests

### ST-002
Test assistant-created scheduled task with `@GitHub` read-only repository lookup.

### ST-003
Test manually-created scheduled task with `@GitHub` read-only repository lookup.

### ST-004
Test assistant-created scheduled task with `@Todoist` read-only task lookup.

### ST-005
Test manually-created scheduled task with `@Todoist` read-only task lookup.

### ST-100 Series
Characterize scheduled-task execution environment:
- new chat vs existing thread,
- manual task vs assistant-created task,
- one-time vs recurring task,
- connector vs no connector,
- short prompt vs longer boot prompt.

## Provisional Design Rule

> Scheduled tasks may be viable as connector-capable cron workers, but each worker must be stateless, read-only by default, and bootstrapped from durable memory until connector and execution-context behavior are better characterized.
