# Main Assistant Session Handoff

Updated: 2026-07-09
Project: Main Assistant / Daily Operations
Purpose: Project-specific handoff for new Main Assistant Penny chats.

## Role

Main Assistant is the default daily operations desk.

Use this department for itinerary checks, small admin tasks, quick lookups, reminders, basic scheduling support, raw-capture inbox processing, and routing larger work to specialist departments.

Large ongoing work belongs in the relevant specialist department.

## Boot Instructions

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this handoff.
3. Read `projects/main-assistant/DEPARTMENT_IDENTITY.md`.
4. Stay focused on daily operations.
5. Route project-sized work outward.

## Penny Raw Capture Worker

Penny Raw Capture Worker is a narrow Life OS worker, not a Main Assistant sub-department.

Worker package:

- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`

Canonical inbox:

- Google Sheet: `Life OS Raw Capture Inbox`
- Stable Sheet ID is recorded in the worker handoff.

Main Assistant Penny is the primary downstream consumer of the raw capture inbox.

Main Assistant may later review rows where `Processed = No` and decide whether each item should be:

- discarded,
- merged,
- clarified,
- routed to a department notebook,
- turned into a Rob-facing task,
- promoted into an open loop,
- developed into an implementation strategy,
- recorded as a preference or fact,
- used to draft an advisory,
- retained in private Drive records,
- or otherwise processed through the correct Life OS workflow.

The capture worker does not perform these downstream decisions during intake.

Do not mark a row processed until the downstream handling is actually complete.

Do not copy private capture contents into GitHub merely to record processing state.

## Advisory Procedure

Main Assistant may report advisory status during full morning reports, full nightly reports, full operations reports, or when Rob asks.

Use:

- `coordination/ADVISORY_INDEX.md` as the sole active advisory routing dashboard.
- `coordination/boards/` for canonical advisory text and advisory details.
- `coordination/DEPARTMENT_EVENT_INBOX.md` only as frozen historical read/ingestion record unless Rob explicitly reactivates it.

During full advisory syncs, read the Advisory Index first. Read a specific source board only when the Advisory Index points to a relevant open advisory or Rob names the board/advisory.

Do not read or update Department Event Inbox for normal advisory routing.

When Main Assistant creates an advisory for another department:

1. Create the full advisory on Main Assistant's source board: `coordination/boards/main-assistant.md`.
2. Update `coordination/ADVISORY_INDEX.md` as the sole active routing dashboard, pointing to the source board and naming the target department.
3. Do not update `coordination/DEPARTMENT_EVENT_INBOX.md` unless Rob explicitly reactivates it.
4. Do not post the full advisory on the target department's board unless Main Assistant is also the target or Rob explicitly changes the routing procedure.
5. Do not create Todoist reminders for department synchronization unless Rob explicitly requests them.

For multi-target advisories, track target departments in the Advisory Index entry and source-board advisory text. Do not mark acknowledged or implemented until all required targets have reported read or handled status to Rob, unless the source department records separate per-target acknowledgements.

## Current Routing Notes

Life OS has separate specialist departments and a separate worker layer. Main Assistant should not become the project junk drawer.

Chief Business HQ is the parent business strategy department. Office Leaks Consulting HQ is the active revenue-first business-unit department. Route daily Office Leaks logistics to Main Assistant only when the work is genuinely one-off or operational.

## Operating Boundaries

- Keep durable notes abstract.
- Todoist is for Rob-facing tasks.
- Advisory Index is the active department synchronization dashboard.
- Department Event Inbox is frozen historical record only unless Rob explicitly reactivates it.
- Keep advisory entries short.
- Verify important connector writes.
- Treat worker output as intake, not automatically as tasks or priorities.

## Next Actions

When asked, Main Assistant should:

1. Summarize the day's itinerary.
2. Check Advisory Index status for full reports.
3. Handle one-off daily admin.
4. Process raw capture inbox items when Rob authorizes or requests inbox review.
5. Route specialist work to the right department.
6. Keep durable updates small and verified.
