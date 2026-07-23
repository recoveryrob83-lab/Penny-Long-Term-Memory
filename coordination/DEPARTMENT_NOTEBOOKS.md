# Department Notebooks

Updated: 2026-07-18
Purpose: Standard LifeOS workflow for durable department reasoning, evidence, decisions, experiments, validation, discoveries, and historical context that should not be confused with raw idea intake or operational state.

## Status

Adopted as an optional LifeOS standard pattern.

## Core Boundary

Trello is the default intake layer for raw ideas, sparks, questions, possibilities, candidate projects, and someday material.

Department Notebooks are durable local knowledge records.

Short form:

> Trello catches the spark. A notebook preserves the fire that proved useful.

Apply:

- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`

before promoting an idea, conversation fragment, or Trello card into a department notebook.

## Purpose

Use Department Notebooks to preserve durable value such as:

- reasoning behind a decision;
- experiment plans and verified results;
- validation evidence;
- architectural interpretation;
- lessons from completed work;
- discoveries that may shape future decisions;
- historical context worth retaining;
- approved plans that need more context than an open-loop row;
- a durable explanation of why a rule, project, or implementation changed.

A notebook should answer why the material deserves durable memory.

Do not use a notebook merely because an idea is interesting or might matter someday. Keep that material in Trello until it passes the promotion gate.

## Not A Routing or Intake Surface

Department Notebooks are not:

- raw idea inboxes;
- Trello replacements;
- advisory boards;
- pending advisory boards;
- task lists;
- open-loop trackers;
- status ledgers;
- Drive working documents;
- Department Event Inbox entries;
- automatic sources of new commitments.

A notebook entry is not routed, acknowledged, scheduled, prioritized, or closed merely because it exists. Notebook material may be read during deliberate review or Hub synchronization without being promoted into operational state.

## Standard Locations

A department may maintain a local notebook hub at:

`projects/<department-folder>/NOTEBOOK.md`

A department may also maintain notebook leaves at:

`projects/<department-folder>/notebook/NOTE-YYYYMMDD-###-short-slug.md`

If a department uses notebook leaves, it should maintain a folder index at:

`projects/<department-folder>/notebook/README.md`

The folder index is a routing and discovery aid for notebook leaves. It is not an advisory board, task list, open-loop tracker, or competing source of operational truth.

Do not create empty notebook hubs or leaf indexes across every department by default. Create them when useful or when a department begins preserving promoted durable knowledge.

## Canonical Metadata

Notebook records should use explicit metadata near the top when practical:

```text
Date: YYYY-MM-DD
Updated: YYYY-MM-DD
Department: <Department Name>
Status: <Open, Active, Waiting, Paused, Blocked, Completed, or Cancelled>
Owner: <Owner>
Record Type: <Note, Decision, Experiment, Validation, Plan, or Milestone>
Authority: <Authoritative, Summary, Historical, or Derived>
```

Use the lifecycle and authority vocabulary in `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`.

Do not use free-form prose such as `Success`, `Raw / unprocessed`, `Parked`, or `Validated in production-like watched testing` as the primary lifecycle field. Preserve richer result language in the body while keeping the top-level status canonical.

An experiment may include a later result-specific `Status:` field when useful, but the document should still have a concise top-level lifecycle status whenever practical.

## Hub Format

Use this structure for `NOTEBOOK.md`:

```markdown
# <Department> Notebook

Updated: YYYY-MM-DD
Project: <Department Name>
Purpose: Durable reasoning, evidence, decisions, validation, discoveries, and historical context for this department.

## Notebook Rules

This is not a raw idea inbox, advisory board, task list, open-loop tracker, or source of current operational truth.
Raw ideas belong in Trello. Promote material here only when its durable knowledge value is clear.

## Notebook Leaves

Leaf notes, if used, live in `projects/<department-folder>/notebook/`.
Start with `projects/<department-folder>/notebook/README.md` before reading leaf notes.

## Notes

### NOTE-YYYYMMDD-001 — <Title>

- Date:
- Updated:
- Owner:
- Record Type:
- Authority:
- Status: Open / Active / Waiting / Paused / Blocked / Completed / Cancelled
- Source or promoted Trello pointer:
- Context Tags:

#### Summary

<one to three sentences>

#### Record

<reasoning, evidence, decision, validation, discovery, or historical context>

#### Operational Consequence

<none, or a pointer to the separately authorized open loop, advisory, rule, Drive artifact, or other authoritative record>
```

## Leaf Index Format

Use this structure for `projects/<department-folder>/notebook/README.md`:

```markdown
# <Department> Notebook Leaves

Updated: YYYY-MM-DD
Project: <Department Name>
Purpose: Routing index for durable notebook leaf records.

## Notebook Rules

Notebook leaves preserve promoted durable knowledge.
They are not raw idea captures, advisories, tasks, open loops, or operational source-of-truth records.

## Naming Convention

`NOTE-YYYYMMDD-###-short-slug.md`

## Leaf Index

| Note ID | Title | Status | Record Type | Authority | Topic / Context Tags | Path |
|---|---|---|---|---|---|---|
| NOTE-YYYYMMDD-001 | Example title | Completed | Validation | Authoritative | example | `projects/<department-folder>/notebook/NOTE-YYYYMMDD-001-example.md` |
```

## Leaf Note Format

Use this structure for individual notebook leaves:

```markdown
# NOTE-YYYYMMDD-### — <Title>

Date: YYYY-MM-DD
Updated: YYYY-MM-DD
Department: <Department Name>
Status: Open / Active / Waiting / Paused / Blocked / Completed / Cancelled
Owner: <Owner>
Record Type: Note / Decision / Experiment / Validation / Plan / Milestone
Authority: Authoritative / Summary / Historical / Derived

## Summary

<one to three sentences>

## Trigger or Source

<why this material was promoted into durable memory; include a Trello or source pointer when useful>

## Record

<main reasoning, evidence, decision, validation, discovery, or historical content>

## Operational Consequence

<none, or a pointer to a separately authorized open loop, advisory, rule, Drive artifact, or other authoritative record>
```

## Creation Gate

Before creating a notebook entry, confirm:

1. The material has durable reasoning, evidence, decision, validation, discovery, planning, or historical value.
2. Trello or conversation alone is no longer sufficient.
3. The owning department is clear.
4. An equivalent notebook or authoritative record does not already exist.
5. The status, owner, record type, and authority are explicit.
6. The write is authorized under `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`.
7. Any operational consequence will be recorded separately rather than smuggled into the notebook as an implicit task.

If these conditions are not met, keep the material in Trello or conversation.

## Review and Further Promotion

During deliberate review, notebook material may:

- remain durable knowledge with no operational consequence;
- inform a current decision;
- support an already-authorized open loop;
- be promoted into a Pending Advisory Board item;
- be promoted into a formal advisory;
- support creation of a Todoist commitment;
- point to a Drive working document;
- justify an update to a handoff, status file, open loop, rule, or SOP;
- become a historical or completed record;
- be archived when no longer useful.

Further promotion must be intentional and independently authorized. A notebook entry does not grant itself permission to become work.

## Relationship To Trello

Use Trello for:

- raw ideas;
- unowned possibilities;
- candidate projects;
- someday material;
- questions awaiting clarification;
- attention and flow.

Use a notebook when the durable knowledge itself is worth preserving.

When material is promoted from Trello:

- mark the card `stage/promoted`;
- add the notebook path;
- keep only the attention context needed in Trello;
- do not maintain two competing full records.

## Relationship To Pending Advisory Boards

Use a Pending Advisory Board only when a clarified and promoted item may become a future advisory, operating-rule proposal, architecture change, or cross-department coordination item.

The normal sequence is:

Trello capture → clarification → promotion decision → notebook or Pending Advisory Board when justified → formal advisory only after deliberate routing.

A notebook is not a mandatory stop for every advisory. Use the natural authoritative path.

## Review Cadence

Department Notebooks are checked when:

- Rob asks;
- a department is doing deliberate reflection, validation review, or cleanup;
- a department handoff says the notebook matters for current work;
- a notebook record may inform a specific current decision;
- `Chief_of_Staff_HQ` runs an explicit morning, nightly, sync, or notebook-review command.

Do not read full notebook history during ordinary boots or routine conversation.

For central `Chief_of_Staff_HQ` review:

- Morning sync reads entries from today and the previous calendar day.
- Nightly sync reads entries from the current calendar day.
- `/NBOOK` reads the current day's entries.
- `/NBOOK YYYY-MM-DD` reads one specified date.
- `/NBOOK YYYY-MM-DD..YYYY-MM-DD` reads an inclusive date range.
- `/NBOOK ALL` reads full notebook history only when Rob explicitly requests it.

When reading by date:

1. Search active department notebook hubs and notebook-leaf indexes.
2. Read only entries or leaves whose date matches the requested scope.
3. Treat the review as read-only unless Rob separately authorizes promotion or file changes.
4. Summarize cross-department implications for the Hub without converting every note into a task or open loop.
5. Prefer bounded context over exhaustive history.

## Scheduled Worker Guidance

When a scheduled sync Worker is explicitly asked to review notebook material, it should read the department's notebook index or hub first.

If notebook leaves exist, read `projects/<department-folder>/notebook/README.md` before opening individual leaf notes.

Scheduled Workers should remain read-only by default unless Rob explicitly authorizes writes.

Workers may capture raw ideas into their authorized Trello or intake destination, but they may not promote material into notebooks without explicit authorization.

## Design Principle

Preserve durable reasoning without turning every spark into architecture.

Keep raw possibility in Trello, operational truth in authoritative files, and validated knowledge in notebooks.

Read recent notebook context when coordination benefits, but do not carry the whole attic into every meeting.