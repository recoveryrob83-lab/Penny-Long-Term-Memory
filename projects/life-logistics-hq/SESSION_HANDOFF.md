# Life Logistics HQ Session Handoff

Updated: 2026-07-04
Project: Life Logistics HQ / Chief of Staff Penny
Purpose: Project-specific handoff for the Life Logistics HQ coordination chat.

## Metadata

- Project Owner: Rob
- Primary Chat: Life Logistics HQ
- Current Phase: Active / Cross-Project Coordination
- Primary Systems: GitHub, Google Drive, Todoist, Calendar, Gmail, Contacts, Advisory Boards, Pending Advisory Boards, Department Notebooks, Department Event Inbox, Scheduled Task Notes, RPR/user-mediated files
- Sensitivity Level: Moderate
- GitHub Rule: Keep GitHub abstract and organized.

## Department Identity

Read:

`projects/life-logistics-hq/DEPARTMENT_IDENTITY.md`

Life Logistics HQ is Rob's Chief of Staff Penny for the Life OS.

## Current System State

Life OS includes:

- GitHub durable memory map.
- Google Drive working records cabinet.
- Todoist Rob-facing action queue.
- Calendar timed commitments.
- Gmail communication evidence.
- Department advisory boards.
- Pending Advisory Board standard.
- Department Notebook standard.
- Source-of-Truth and Publication Standard.
- Advisory Index.
- Department Event Inbox.
- Daily HQ sync pilot model.
- Life OS design-principles file.
- Reliable Connector Execution Layer as the first concrete Engineering research track.

## Current Architecture Standards

- Pending Advisory Boards: `coordination/PENDING_ADVISORY_BOARDS.md`
- Department Notebooks: `coordination/DEPARTMENT_NOTEBOOKS.md`
- Source-of-Truth and Publication Standard: `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`
- Design Principles: `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

Source/publication rule: choose the natural authoritative home first, then make every other copy clearly secondary.

Short form: source in GitHub, publish to Drive, with exceptions when another system is the natural authoritative home.

## Current Drive Architecture Decisions

Business Drive architecture is resolved:

- Life Organization > Chief Business HQ
- Under that: Business Development

Business Development should be treated as a subfolder under Chief Business HQ, not a separate top-level business root.

## Objectives

- Maintain Life OS structure.
- Keep GitHub coherent and abstract.
- Coordinate project handoffs and department identities.
- Maintain global open loops and project map.
- Run startup refreshes and nightly housekeeping when Rob asks.
- Read, route, and track advisory-board items when appropriate.
- Maintain Department Event Inbox state for cross-department read/ingestion tracking.
- Maintain the Pending Advisory Board standard.
- Maintain the Department Notebook standard.
- Maintain the source-of-truth and publication standard.
- Track scheduled-task architecture findings at an abstract level.
- Protect role clarity between Main Assistant, Life Logistics HQ, and specialist departments.

## Advisory Workflow

Source-of-truth files:

- `coordination/ADVISORY_INDEX.md` is the advisory dashboard.
- `coordination/DEPARTMENT_EVENT_INBOX.md` is the department synchronization/read/ingestion register.
- `coordination/boards/` contains department advisory details.
- `coordination/PENDING_ADVISORY_BOARDS.md` contains the standard pending-board workflow.
- `coordination/DEPARTMENT_NOTEBOOKS.md` contains the standard department-notebook workflow.
- `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` contains the ownership/publication workflow.

When Life Logistics HQ creates or consumes an advisory:

1. Read the relevant board.
2. Update the central Advisory Index when status changes.
3. Update the Department Event Inbox entry.
4. Track target department read/ingestion status.
5. Do not acknowledge multi-target advisories until all target departments have reported read/handled status, unless the source department records separate per-target acknowledgements.
6. Do not create Todoist reminders for department synchronization unless Rob explicitly requests them.

Todoist is Rob's personal task system. Department Event Inbox is the system synchronization register.

## Local Capture Workflows

Pending Advisory Boards are local department staging notebooks, not routed advisory channels.

Department Notebooks are optional local sketchpads for durable idea capture.

Create local pending boards or notebooks only when useful. Do not create empty files across all departments by default.

## Scheduled HQ Sync Model

Daily HQ sync workers are now the preferred scheduled-task experiment over a standalone Advisory Watcher.

Engineering HQ Daily Sync is the first pilot.

Scheduled sync workers should read, consume advisories, and report. They should not modify GitHub, Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.

## Current Major Open Loops For Life Logistics

- Observe Engineering HQ Daily Sync pilot before rolling out additional daily sync workers.
- Keep Reliable Connector Execution Layer visible as the first concrete Engineering research track.
- Continue advisory and event-inbox hygiene.
- Retry Life Logistics `status.md` creation later only if useful; previous creation attempts were blocked by connector safety checks.

## Source Systems

- GitHub: durable memory map, handoffs, project state, advisory structure, pending advisory standard, department notebook standard, source/publication standard, Department Event Inbox, scheduled-task notes, design principles, Captain's Log.
- Google Drive: working records and detailed artifacts.
- Todoist: Rob-facing action queue.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Contacts: people lookup.
- RPR/user-mediated files: reliable path for structured or brittle records.

## Connector / Safety Notes

- Prefer small, verifiable updates.
- Fetch before editing GitHub files.
- Verify important edits when possible.
- Use abstract language in GitHub.
- Use RPR when structured records need reliable handling.
- Avoid repeated retries after connector safety blocks.
- Treat connector failures as observed behavior, not assumed mechanism.

## Decision Log

- Life Logistics HQ and Main Assistant are separate roles.
- Main Assistant is the daily operations desk.
- Life Logistics HQ is the Chief of Staff and system curator.
- Department Event Inbox owns system synchronization state. Todoist owns Rob-facing actions.
- Design principles govern whether new platforms enter Life OS.
- Business Drive architecture: `Life Organization > Chief Business HQ > Business Development`.
- Pending Advisory Boards are local staging notebooks, not routed advisory channels.
- Department Notebooks are optional local sketchpads, not routing or source-of-truth systems.
- Source-of-truth rule: choose the natural authoritative home first; every other copy is secondary.

## Immediate Next Actions

1. Continue using Life Logistics HQ for cross-project coordination and advisory workflow cleanup.
2. Use Main Assistant for daily operations.
3. Use specialist chats for focused work.
4. Observe Engineering HQ Daily Sync pilot before adding more daily sync workers.

## Notes for Next Penny

This chat is Life Logistics HQ, not Main Assistant. Protect role clarity. Route daily admin to Main Assistant and specialist project work to the right department. Keep GitHub tidy and abstract. Use the Advisory Index plus Department Event Inbox for advisory sync state.