# Department Notebooks

Updated: 2026-07-05
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

## Standard Locations

A department may maintain a local notebook hub at:

`projects/<department-folder>/NOTEBOOK.md`

A department may also maintain notebook leaves at:

`projects/<department-folder>/notebook/NOTE-YYYYMMDD-###-short-slug.md`

If a department uses notebook leaves, it should maintain a folder index at:

`projects/<department-folder>/notebook/README.md`

The folder index is a routing/discovery aid for notebook leaves. It is not an advisory board, task list, open-loop tracker, or source-of-truth file.

Do not create empty notebook hubs or leaf indexes across every department by default. Create them when useful or when a department begins using notebook leaves.

## Hub Format

Use this structure for `NOTEBOOK.md`:

```markdown
# <Department> Notebook

Updated: YYYY-MM-DD
Project: <Department Name>
Purpose: Durable idea notebook for this department.

## Capture Rules

This is not an advisory board, task list, open-loop tracker, or source of operational truth.

Use it for durable ideas worth preserving.

## Notebook Leaves

Leaf notes, if used, live in `projects/<department-folder>/notebook/`.

Start with `projects/<department-folder>/notebook/README.md` before reading leaf notes.

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

## Leaf Index Format

Use this structure for `projects/<department-folder>/notebook/README.md`:

```markdown
# <Department> Notebook Leaves

Updated: YYYY-MM-DD
Project: <Department Name>
Purpose: Routing index for notebook leaf notes.

## Capture Rules

Notebook leaves are durable idea notes.

They are not advisories, tasks, open loops, source-of-truth files, or Department Event Inbox items.

## Naming Convention

`NOTE-YYYYMMDD-###-short-slug.md`

## Leaf Index

| Note ID | Title | Status | Topic / Tags | Path |
|---|---|---|---|---|
| NOTE-YYYYMMDD-001 | Example title | Active / Revisited / Promoted / Archived | example | `projects/<department-folder>/notebook/NOTE-YYYYMMDD-001-example.md` |
```

## Leaf Note Format

Use this structure for individual notebook leaves:

```markdown
# NOTE-YYYYMMDD-### — <Title>

Date: YYYY-MM-DD
Department: <Department Name>
Status: Active observation / Revisited / Promoted / Archived
Topic: <short topic>

## Summary

<one to three sentences>

## Note

<main content>

## Possible Future Use

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

## Scheduled Worker Guidance

When a scheduled sync worker is explicitly asked to review notebook material, it should read the department's notebook index or hub first.

If notebook leaves exist, read `projects/<department-folder>/notebook/README.md` before opening individual leaf notes.

Scheduled workers should remain read-only by default unless Rob explicitly authorizes writes.

## Design Principle

Capture useful ideas without forcing action.

Preserve long-term memory without over-routing.

Keep operational source-of-truth files clean.