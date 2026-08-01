# Chief_of_Staff_HQ Session Handoff

Updated: 2026-08-01
Project: Chief_of_Staff_HQ / Daily Operations
Purpose: Current replacement-chat handoff for Rob's primary point of contact, personal-assistant headquarters, `LifeOS_HQ` chair, routing desk, and follow-through coordinator.

## Replacement-Chat Note

This handoff was refreshed because the current LifeOS HQ conversation completed a major V2 courier milestone and Rob chose to start a new chat before the conversation became unwieldy.

The replacement chat must reconstruct authority from the canonical Boot sequence and current project files. Conversation history and chat handbooks are orientation aids, not source truth.

## Role and Authority

`Chief_of_Staff_HQ` is Rob's default operational front door. It owns daily planning, practical coordination, executive-function support, report intake, cross-department synthesis, assignment routing, follow-through, advisory preparation, and authorized light connector execution.

`LifeOS_HQ` is the shared meeting room. It is not a department, backlog owner, or independent authority. Chief of Staff chairs it and routes real work to one owning department and one authoritative destination. Rob remains the final decision-maker.

Specialist judgment and durable state remain with the relevant department.

## Boot Instructions

1. Read `memory/STARTUP_BOOT.md` and every required universal-kernel file in the specified order.
2. Read this handoff.
3. Read `projects/main-assistant/DEPARTMENT_IDENTITY.md`.
4. Read `projects/main-assistant/README.md`, `status.md`, and `open_loops.md`.
5. Read `coordination/ADVISORY_INDEX.md` when advisory state or cross-department routing matters.
6. Re-read authoritative sources before making current-state claims that may have changed.
7. Keep Chief of Staff focused on coordination and follow-through rather than absorbing specialist ownership.

## Daily Operating Pattern

Apply `memory/06_DAILY_OPERATING_SOP.md` by default:

- choose one major action;
- add at most one low-friction support action when useful;
- treat travel, appointments, and unfamiliar routes as complete major tasks;
- prepare Penny-level work before asking Rob to act;
- keep due dates sparse and meaningful;
- judge success by completion and reduced friction, not task count.

## V2 Courier and Remote GitHub Source Milestone

The LifeOS V2 courier completed a successful cross-room production proof on 2026-08-01.

Verified transport behavior:

- the server supports multiple named routes;
- the extension discovers a pending command before route readiness, then navigates to the route and establishes readiness;
- `/begin` remains atomic and readiness-gated;
- exact URL, empty composer, content-script availability, send control, route health, pause, emergency-stop, and test-arm protections remain enforced;
- composer insertion, send-control selection, and delivery proof were hardened;
- post-click ambiguity becomes terminal `UNCERTAIN` rather than an automatic retry;
- one owned background courier tab may be created and later reused between routes;
- the newest Maintenance test command reached `DELIVERED`, and Maintenance visibly confirmed receipt.

Canonical evidence:

- `ADV-20260801-055` revision 1 remains immutable `UNCERTAIN` evidence with one attempt;
- revision 2 was delivered and acknowledged;
- Rob authorized closure;
- the advisory is closed on the Chief of Staff source board and in the Advisory Index.

The V2 advisory source now defaults to read-only `REMOTE_GITHUB` against `recoveryrob83-lab/Penny-Long-Term-Memory@main`.

Intended source behavior:

1. resolve `main` to one commit SHA;
2. fetch the Advisory Index and every referenced open-advisory board at that same SHA;
3. parse and reconcile only after the complete snapshot is available;
4. cache unchanged verified snapshots;
5. fail closed on GitHub, authentication, network, missing-file, malformed-index, or ambiguous-source failures;
6. quarantine isolated advisory-envelope errors without blocking valid advisories;
7. never run `git pull`, mutate Rob's working tree, or silently fall back to local files in production.

Live local validation reported `CURRENT` source state, a verified SHA, `ADV-20260728-054` as valid, and `ADV-20260726-053` quarantined because it lacks a V2 Courier Envelope.

Important publication discrepancy at handoff:

- the live local runtime includes the advisory-level quarantine repair;
- the current GitHub connector view of `main` still shows `0eeccc46df6980c62e29795e7f40c78a1d61a108` (`Read courier advisories from canonical GitHub snapshots`) as the latest code commit and does not yet show the quarantine repair commit;
- Engineering must publish and verify that local repair on `origin/main` before it is treated as durable repository truth.

## Local Resource Constraint and Courier Tab Use

Rob's PC cannot comfortably keep two active ChatGPT windows open during normal daytime work.

Current operating choice:

- Rob may close the courier-owned tab when automation is not running;
- scheduled nighttime automation may create or reuse one owned background tab;
- the extension must not hijack a composer containing text;
- tab reuse or post-delivery closure remains an Engineering implementation choice, provided it does not create tab sprawl or interfere with Rob's active chat.

## Command History Behavior

Current command persistence correctly preserves transport evidence, including delivered and uncertain revisions.

Engineering-owned follow-up remains:

- display commands newest first;
- keep active and uncertain records prominent;
- retain terminal evidence without leaving an indefinitely growing primary list;
- add a bounded history or retention policy that does not delete required evidence or alter dispatch order.

Dashboard display order must never become command-dispatch order.

## Source Systems and Boundaries

- GitHub: durable abstract state, handoffs, open loops, advisories, architecture, and validated history.
- Trello: raw intake, possibilities, and current attention.
- Todoist: commitments and reminders.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Drive: working documents and human-facing artifacts.
- Dashboard: visibility, diagnostics, and bounded controls, not source truth.
- Conversation: temporary reasoning and working context.

The account-linked financial connector remains isolated from `Chief_of_Staff_HQ`, `LifeOS_HQ`, and multi-connector operational chats. Route account-linked work to Finance-only context.

## Trello Flow Board

Canonical procedure: `coordination/TRELLO_FLOW_BOARD_SOP.md`.

- one card maximum in Now;
- three cards maximum in Next;
- Waiting contains blocked work only;
- Captured contains ideas, not promises;
- do not duplicate detailed truth across Trello, Todoist, GitHub, Calendar, Drive, or conversation.

## Current Advisory and Dependency State

Re-read `coordination/ADVISORY_INDEX.md` before making a freshness-sensitive claim.

At handoff:

- `ADV-20260801-055` is closed after successful revision-2 delivery and acknowledgement;
- `ADV-20260728-054` remains open and valid for Engineering;
- `ADV-20260726-053` remains an open Maintenance-owned source record but is non-dispatchable in V2 because its source text lacks a V2 Courier Envelope;
- the missing envelope is a source-owner issue, not authority to rewrite or promote the advisory from Chief of Staff;
- existing command records must not be reset, retried, deleted, or reclassified without explicit authority and evidence.

## Active Chief of Staff Open Loops

The authoritative queue is `projects/main-assistant/open_loops.md`.

Chief of Staff-owned active items remain:

1. Validate the friction-aware Daily Operating SOP through ordinary use.
2. Pilot lightweight expendable-item inventory beginning with transportation access and basic necessities.

Courier implementation, command-history policy, tab lifecycle, readiness-log deduplication, and publication of the quarantine patch are Engineering-owned external dependencies, not Chief of Staff implementation loops.

## Current Operating Watches

- Prevent `LifeOS_HQ` from becoming a department or competing backlog.
- Prevent report intake and coordination from silently transferring specialist ownership.
- Preserve one owner and one authoritative record for each real action.
- Treat `UNCERTAIN` transport as a hard stop, not permission to retry.
- Ensure remote-source failure remains fail-closed while isolated advisory parse errors remain quarantined and visible.
- Keep nighttime automation bounded and compatible with Rob's PC memory limits.
- Keep command history useful without deleting evidence.
- Preserve the current Office Leaks pause unless Rob explicitly resumes it.

## Next Actions for the Replacement Chat

1. Boot from canonical sources.
2. Confirm current `origin/main` and whether the quarantine repair has been published.
3. Read the current V2 `/status` source block before claiming remote sync health.
4. Verify the source is `REMOTE_GITHUB`, `CURRENT`, and pinned to a non-null commit SHA.
5. Preserve `ADV-20260726-053` as quarantined unless its source owner supplies a valid V2 envelope or otherwise resolves it.
6. Route command-history ordering, retention, courier-tab lifecycle, and readiness-event deduplication to Engineering when Rob chooses to continue refinement.
7. Continue ordinary Chief of Staff operations without turning the successful courier proof into unnecessary new infrastructure.
8. Keep durable updates small, owner-correct, and verified.

## Completion Standard

Chief of Staff is working correctly when Rob has a clear next action, avoidable friction is removed, department reports are synthesized without ownership drift, assignments reach one owner and one authoritative destination, automation evidence is truthful, stale wrappers close cleanly, and `LifeOS_HQ` does not create duplicate truth or administrative drag.
