# Pending Advisory Boards

Updated: 2026-07-04
Purpose: Standard Life OS workflow for capturing possible advisories before they become formal cross-department coordination items.

## Status

Adopted as a Life OS standard pattern.

## Purpose

Pending Advisory Boards are local department staging notebooks.

They capture ideas that might later become formal advisories without immediately interrupting Rob or other departments.

Use them for:

- possible future advisories,
- architecture ideas,
- workflow improvements,
- design principles to consider,
- cross-department issues that need review before routing.

## Not A Communication Channel

Pending Advisory Boards are not formal advisory boards.

They do not update:

- `coordination/ADVISORY_INDEX.md`,
- `coordination/DEPARTMENT_EVENT_INBOX.md`,
- other department boards,
- Todoist.

Nothing on a pending board is considered routed, read, ingested, acknowledged, or closed.

## Standard Location

Each department may maintain a local pending board at:

`projects/<department-folder>/PENDING_ADVISORIES.md`

Examples:

- `projects/engineering/PENDING_ADVISORIES.md`
- `projects/business-development/PENDING_ADVISORIES.md`
- `projects/life-logistics-hq/PENDING_ADVISORIES.md`
- `projects/finance-benefits/PENDING_ADVISORIES.md`
- `projects/main-assistant/PENDING_ADVISORIES.md`

Create the file only when needed. Do not create empty pending boards everywhere just to satisfy the pattern.

## Standard Format

Use this structure:

```markdown
# Pending Advisories

Updated: YYYY-MM-DD
Project: <Department Name>
Purpose: Local staging area for possible future advisories.

## Operating Rule

This is a local staging notebook, not a routed advisory board.

Do not update the Advisory Index or Department Event Inbox for items here.

Promote items only during deliberate advisory review.

## Pending Items

### PA-YYYYMMDD-001 — <Short title>

- Date captured:
- Source:
- Possible target department(s):
- Priority guess:
- Status: Pending

#### Note

<Short abstract note.>

#### Promotion Criteria

<What would make this worth a formal advisory?>

## Promoted / Dismissed

- YYYY-MM-DD: <Item> — promoted to <ADV-ID> / dismissed because <brief reason>.
```

## Promotion Workflow

During nightly review, startup refresh, or deliberate advisory sync, Rob may ask a department to process its pending board.

The department should:

1. Review pending items.
2. Merge duplicates.
3. Group related ideas.
4. Dismiss items that no longer matter.
5. Promote only items that need cross-department routing.
6. Create formal advisories only after promotion.
7. Then update the Advisory Index and Department Event Inbox for promoted items only.

## Promotion Criteria

Promote a pending item into a formal advisory only when it needs one or more of the following:

- another department to read or act,
- a durable Life OS decision,
- a shared operating-rule change,
- cross-project coordination,
- a source-of-truth update,
- Rob-visible routing.

Do not promote simple notes, half-formed ideas, or local department reminders.

## Review Cadence

Pending boards are checked only when:

- Rob asks,
- a department is doing deliberate advisory review,
- Life Logistics HQ is doing housekeeping and the department handoff says its pending board matters,
- a pending item appears to be blocking current work.

Do not turn pending-board review into a default daily interruption.

## Design Principle

Capture should be easy.

Synchronization should be deliberate.

Formal advisories should represent reviewed coordination decisions, not every useful thought generated during conversation.