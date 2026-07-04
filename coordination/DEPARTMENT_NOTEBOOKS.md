# Department Notebooks

Updated: 2026-07-04
Purpose: Standard Life OS workflow for durable department-level idea capture that is not advisory, task, or operating-state material.

## Status

Adopted as an optional Life OS standard pattern.

## Purpose

Department Notebooks are durable local sketchpads.

They capture useful ideas, lessons, metaphors, patterns, sparks, and discussion fragments that are worth preserving but do not yet belong in a task list, advisory board, handoff, open loop, design-principles file, or Drive artifact.

## Not A Routing Surface

Department Notebooks are not:

- advisory boards,
- pending advisory boards,
- task lists,
- open-loop trackers,
- source-of-truth files,
- Drive working documents,
- Department Event Inbox entries.

A notebook entry is not routed, read, ingested, acknowledged, or closed.

## Standard Location

A department may maintain a local notebook at:

`projects/<department-folder>/NOTEBOOK.md`

Examples:

- `projects/engineering/NOTEBOOK.md`
- `projects/business-development/NOTEBOOK.md`
- `projects/main-assistant/NOTEBOOK.md`
- `projects/life-logistics-hq/NOTEBOOK.md`
- `projects/finance-benefits/NOTEBOOK.md`

Create the file only when useful. Do not create empty notebooks across all departments by default.

## Standard Format

Use this structure:

```markdown
# <Department> Notebook

Updated: YYYY-MM-DD
Project: <Department Name>
Purpose: Durable idea notebook for this department.

## Capture Rules

This is not an advisory board, task list, open-loop tracker, or source of operational truth.

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

## Review / Promotion

During periodic review, notebook items may be:

- left as notes,
- promoted to Pending Advisory Board items,
- promoted to formal advisories,
- converted into Todoist tasks,
- moved into Drive working docs,
- summarized into handoff/status/open-loop files,
- archived as no longer relevant.

Promotion should be intentional and should not happen automatically.

## Relationship To Pending Advisory Boards

Use a Department Notebook for broad idea preservation.

Use a Pending Advisory Board only when the item may become a future advisory, operating-rule proposal, architecture change, or cross-department coordination item.

Notebook first, Pending Advisory Board second, formal advisory only after deliberate promotion.

## Review Cadence

Department Notebooks are checked only when:

- Rob asks,
- a department is doing deliberate reflection or cleanup,
- a department handoff says the notebook matters for current work,
- a notebook item may inform a specific current decision.

Do not turn notebook review into a default daily interruption.

## Design Principle

Capture useful ideas without forcing action.

Preserve long-term memory without over-routing.

Keep operational source-of-truth files clean.