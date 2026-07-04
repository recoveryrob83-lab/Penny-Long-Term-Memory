# Engineering Advisory Board

Updated: 2026-07-04
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260704-005 — Department Notebooks for long-term idea capture

- Date: 2026-07-04
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Open
- Board: `coordination/boards/engineering.md`

#### Summary

Engineering recommends adding a Department Notebook pattern alongside Pending Advisory Boards.

Pending Advisory Boards are for possible future advisories, operating-rule proposals, and architectural changes.

Department Notebooks would be broader long-term memory notebooks for durable ideas, insights, useful discussion fragments, lessons learned, recurring themes, and noteworthy sparks that are valuable to preserve but are not necessarily advisory material.

#### Problem Statement

Useful ideas often emerge naturally during conversation. Not all of them should become advisories, open loops, tasks, design principles, or formal documentation.

Without a lightweight notebook layer, these ideas either:

- Get lost when chat context rolls off.
- Get forced into advisory or task systems where they do not belong.
- Stay only in Rob's working memory.
- Create pressure to over-document or over-route every useful thought.

This is especially important because Life OS is meant to reduce cognitive load, not require Rob to remember every valuable idea that appears during conversation.

#### Proposed Architecture

Each active department may maintain a local Department Notebook.

Optional local path:

`projects/<department-folder>/NOTEBOOK.md`

Examples:

- `projects/engineering/NOTEBOOK.md`
- `projects/business-development/NOTEBOOK.md`
- `projects/main-assistant/NOTEBOOK.md`
- `projects/life-logistics-hq/NOTEBOOK.md`

A notebook is a durable idea-capture surface, not a routing surface.

Rob may say:

`That's a good idea. Add it to the notebook.`

The department may also suggest notebook capture when an idea seems worth preserving but does not yet require action.

#### Relationship to Other Systems

Department Notebooks should be distinct from:

- Pending Advisory Boards: possible future advisories or architecture proposals.
- Department Advisory Boards: formal published advisories.
- Department Event Inbox: synchronization/read/ingestion state.
- Todoist: Rob-facing actions and reminders.
- Drive working docs: detailed editable records and artifacts.
- GitHub handoffs/open loops/status: current operational state.

#### Suggested Notebook Content

A Department Notebook may capture:

- Good ideas that do not yet require action.
- Lessons learned.
- Useful metaphors, framing, or wording.
- Future reflections.
- Long-term pattern observations.
- Product or workflow sparks.
- Ideas to revisit later.
- Context that would otherwise disappear from chat history.

#### Suggested Format

Recommended simple structure:

```markdown
# <Department> Notebook

Updated: YYYY-MM-DD
Purpose: Durable idea notebook for this department.

## Capture Rules

This is not an advisory board, task list, or source of operational truth.
Use it for durable ideas worth preserving.

## Notes

### NOTE-YYYYMMDD-001 — <Title>

- Date captured:
- Source:
- Tags:
- Status: Open / Revisited / Promoted / Archived

#### Note

<content>

#### Possible Future Use

<optional>
```

#### Promotion / Review

During periodic review, notebook items may be:

- Left as notes.
- Promoted to Pending Advisory Board items.
- Promoted to formal advisories.
- Converted into Todoist tasks.
- Moved into Drive working docs.
- Archived as no longer relevant.

Promotion should be intentional and should not happen automatically.

#### Design Principles

This proposal supports:

- Capture without interruption.
- Long-term memory without over-routing.
- Fewer unnecessary advisories.
- Reduced pressure on Rob's working memory.
- Clear distinction between raw ideas, pending proposals, formal advisories, tasks, and durable operating state.

#### Requested Life Logistics HQ Action

1. Decide whether to adopt Department Notebooks as a standard Life OS pattern.
2. Decide the standard location and filename, likely `projects/<department-folder>/NOTEBOOK.md`.
3. Add notebook rules to the appropriate operational documentation if adopted.
4. Preserve the difference between Notebooks and Pending Advisory Boards.
5. Decide whether notebooks should be created only when needed rather than pre-created for every department.

#### Engineering Recommendation

Adopt Department Notebooks as an optional local department pattern.

Create notebooks only when useful.

Treat them as durable sketchpads, not action systems, advisory systems, or source-of-truth files.

### ADV-20260704-003 — Engineering sync completed and Reliable Connector Execution Layer next work

- Status: Open
- From: Chief Engineering Penny
- To: Chief Engineering Penny
- Priority: High

Engineering should continue the Reliable Connector Execution Layer work from the design note and prior handoff context.

## Acknowledged / Implemented Advisories

### ADV-20260704-004 — Department Pending Advisory Boards

- Status: Acknowledged
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High

Life Logistics HQ adopted Pending Advisory Boards as a Life OS standard pattern.

Created:

- `coordination/PENDING_ADVISORY_BOARDS.md`

Durable decision: Pending Advisory Boards are local department staging notebooks, not routed advisory channels. Optional local board path is `projects/<department-folder>/PENDING_ADVISORIES.md`. Create local pending boards only when needed.

### ADV-20260703-010 — Life OS design principle for new platforms

- Status: Acknowledged
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: Medium

Life Logistics HQ created `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md` and recorded the measured-need platform adoption principle.

### ADV-20260703-009 — Scheduled HQ sync system experiment

- Status: Acknowledged
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High

Engineering HQ Daily Sync is the first scheduled HQ sync pilot.

### ADV-20260703-007 — Scheduled advisory watcher and inbox procedure

- Status: Acknowledged
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High

Standalone watcher concept was later superseded by daily HQ sync workers.

### ADV-20260703-006 — Engineering HQ online and Drive scaffold created

- Status: Acknowledged
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High

Chief Engineering Penny is online as the technical architecture department.
