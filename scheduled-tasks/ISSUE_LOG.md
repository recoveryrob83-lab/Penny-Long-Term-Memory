# Scheduled Task Issue Log

Updated: 2026-07-05
Purpose: Short record of scheduled task runs that failed, partially completed, or behaved unexpectedly.

## Issue Log

| Issue ID | Date / Time | Task ID | Owner | Problem | Impact | Next Action |
|---|---|---|---|---|---|---|
| ISSUE-20260705-001 | 2026-07-05 | Scheduled connector tests | Life OS / Engineering | Execution context varied across tests; one run stayed in place, another opened a new chat. Earlier assistant-created connector prompt did not invoke connector as intended. | Scheduled workers cannot assume chat identity or prior context. | Keep workers stateless, read-only by default, and bootstrapped from durable memory. |

## Rule

Use this file for scheduler failures, connector failures, missing access, partial runs, unexpected new-chat behavior, or memo-write problems.

Keep details short and operational.