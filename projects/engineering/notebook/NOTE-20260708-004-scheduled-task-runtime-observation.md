# NOTE-20260708-004 — Scheduled Task Runtime Observation

Date: 2026-07-08
Project: Chief Engineering Penny / Engineering HQ
Related Projects: Life OS, Wellness HQ, scheduled task workers, Prompt Library / Command Launcher
Status: Active observation / platform behavior note

## Context

Rob ran a scheduled task in the Wellness HQ chat because Wellness is not heavily used yet. The task was a simple boot-and-sync test.

Observed behavior:

- The scheduled task appeared in the same chat window rather than opening a new chat.
- The task successfully invoked the GitHub connector during that run.
- Wellness HQ then produced a diagnostic explaining that scheduled tasks appear to send the stored prompt back into a ChatGPT run, where the model then decides how to satisfy it.

This suggests scheduled tasks may be better understood as scheduled prompt injections or scheduled prompt runners, not guaranteed independent autonomous worker chats.

## Working Interpretation

Scheduled tasks are useful, but should not yet be treated as reliable autonomous sync agents.

They may:

- Continue inside the originating conversation.
- Sometimes invoke connectors successfully.
- Sometimes answer from context if tool access is unavailable or the model decides not to invoke tools.
- Behave differently depending on execution context, connector availability, conversation binding, and prompt wording.

## Engineering Implication

Future scheduled-task prompts should be self-verifying.

A scheduled boot/sync task should not merely say "boot and sync." It should explicitly require live source-system access and explicit reporting of what was read.

Recommended prompt language:

> You must attempt a live GitHub read before reporting success. Do not answer from memory. If GitHub is unavailable, report that clearly. Include the file paths successfully read and distinguish live connector access from remembered context.

This protects Life OS from false-positive sync reports.

## Reliability Classification

Current classification:

- Scheduled tasks: experimental scheduled prompt runners.
- Not yet reliable autonomous agents.
- Useful for prompts, reminders, and light self-checks.
- Require verification language for any connector-dependent task.

## Possible Test Matrix

Future Engineering can test:

1. Same chat vs new chat behavior.
2. Prompt with explicit `@GitHub` vs no explicit connector mention.
3. Read-only boot vs advisory check.
4. Whether file paths and live-read citations are included.
5. Whether the task reports connector unavailable when blocked.
6. Whether the task modifies anything without explicit permission.
7. Whether connector access differs by department chat.
8. Whether long-running chats behave differently from fresh chats.

## Relationship to Prompt Library / Command Launcher

This supports the Prompt Library / Command Launcher idea.

If scheduled tasks remain inconsistent, a local desktop prompt launcher may be more reliable for many Life OS operations because Rob can intentionally trigger the command in the correct chat and verify connector behavior immediately.

Manual command launching and scheduled prompt running should be treated as complementary paths:

- Prompt launcher: user-triggered, immediate, more observable.
- Scheduled task: time-triggered, useful but requires self-verification.

## Design Rule Candidate

Do not trust scheduled task success unless the task reports the live source reads or connector unavailability explicitly.

## Closing Note

This is a small operational discovery, but it clarifies the automation layer. Life OS automation should evolve from observed runtime behavior, not assumptions about how scheduled workers ought to behave.
