# Open Loop Ownership and Visibility SOP

Updated: 2026-07-18
Project: Life OS Coordination
Purpose: Define where unfinished work belongs, when it becomes system-level, how cross-department visibility works, and how the dashboard aggregates state without creating duplicate truth.

## Core Principle

Visibility is not ownership.

A record may be useful to every department and still belong to only one department. The LifeOS Dashboard may aggregate all department and system records for Rob without copying those records into global memory.

Short form:

> One owner, one authoritative record, many permitted viewers.

## Record Classes

Do not use `open loop` as a catch-all label.

- **Open loop:** unfinished action that requires future work.
- **Active work:** an open loop currently being worked.
- **Waiting item:** unfinished work blocked by an external event, person, decision, or dependency.
- **Paused item:** intentionally stopped work with a clear resume trigger.
- **Parking-lot item:** a deliberately deferred possibility that is not current work and has a concrete review trigger.
- **Standing rule:** an enduring operating constraint. It is not unfinished work.
- **Operating watch:** a condition being observed. It becomes work only when its trigger occurs.
- **Milestone / closed item:** historical evidence that work finished or a decision was completed.
- **Notebook record:** context, reasoning, validation, or discovery. A note does not automatically become a task.

If a sentence only says “remember this rule,” “watch this condition,” “accept a reference someday,” or “this happened,” it does not belong in an open-work section.

## Authoritative Location

Department-owned unfinished work belongs in the owning department's `open_loops.md`.

Examples:

- dashboard parser implementation belongs to Engineering HQ;
- repository-path migration and archive disposition belong to Life OS Maintenance HQ;
- pricing decisions belong to Finance HQ or Business HQ according to the decision being made;
- wellness routines belong to Wellness HQ;
- Office Leaks execution belongs to Office Leaks HQ.

The authoritative department record may be summarized in its `status.md` or `SESSION_HANDOFF.md`, but those summaries must not become competing open-loop ledgers.

`memory/05_OPEN_LOOPS.md` is the system-level open-loop and operating-watch file. It is not a mirror of every department backlog.

## Department-Owned by Default

A work item remains department-owned when one department can:

- decide the next action;
- perform or coordinate the work;
- determine completion;
- maintain the authoritative context;
- route any narrow dependency through an advisory or explicit handoff.

Broad usefulness, executive interest, historical importance, or visibility across Life OS do not make a department item system-owned.

A dashboard feature may help all of Life OS while its implementation remains Engineering-owned.

## System-Level Promotion Threshold

Promote work into `memory/05_OPEN_LOOPS.md` only when at least one of these is true:

1. No single department can own completion.
2. Two or more departments must each take substantive action or make a decision.
3. A shared policy, boot rule, source boundary, or architecture contract is changing.
4. The work represents a system-wide blocker, risk, outage, or integrity problem.
5. Chief of Staff HQ or Life OS Maintenance HQ must actively coordinate multiple owners through completion.
6. Rob explicitly designates the work as system-level.

Mere mentions, awareness, downstream benefit, or a possible future dependency are not enough.

## System Coordination Records

When one department still owns execution but system coordination is necessary:

- keep the detailed authoritative record in the department;
- create only a compact system coordination record;
- name the lead department;
- name the departments that must act or decide;
- link or point to the authoritative department path;
- describe only the system-level dependency or coordination outcome;
- do not copy the department's full next action and notes.

A system coordination record is a coordination envelope, not a duplicate task card.

## Promotion and Demotion

### Promote

Before promoting a department item to system level:

1. Confirm the system-level threshold is met.
2. Identify the lead owner or state that the work has no single owner.
3. Preserve one authoritative detailed record.
4. Add only the minimum system coordination context.
5. Route required department action through advisories, dependencies, or handoffs.

### Demote

Demote a system item when:

- one department can now own completion;
- cross-department action is finished;
- the remaining work is only local implementation;
- the item has become a standing rule, watch, or historical milestone;
- the system record merely repeats a department record.

On demotion:

1. preserve or create the authoritative department record;
2. remove the system open-loop mirror;
3. retain a system closure note only when the system coordination outcome itself is historically important;
4. do not copy the local completion history into global Recently Closed by default.

## Lifecycle Rules

### Create

Create an open loop only when all of these are known:

- owner or lead;
- current state;
- smallest useful next action;
- reason the work remains unfinished;
- completion or review condition.

Do not create speculative placeholders for events that have not occurred.

### Update

Update the authoritative record when:

- state changes;
- the next action changes materially;
- ownership changes;
- a dependency appears or clears;
- completion evidence arrives.

Summaries and handoffs should point back to the authoritative record rather than silently diverging.

### Pause or Wait

Use `Waiting` when progress depends on an external event or input.

Use `Paused` when Life OS intentionally stops the work.

Use a parking lot only when the item is genuinely non-current and has a meaningful resume or review trigger.

### Close

When work completes:

1. remove it from the active section;
2. add a concise dated closure record when the evidence is worth preserving;
3. keep detailed validation in the department notebook when appropriate;
4. remove stale system coordination wrappers;
5. do not preserve duplicate closures in multiple ledgers merely for visibility.

### Reconcile

During a department sync or system audit:

- compare open work with status and handoff summaries;
- identify closed work still listed as open;
- identify the same item at department and system levels;
- separate rules and watches from unfinished work;
- remove speculative placeholders;
- preserve historical notes without promoting them back into current work.

## Cross-Department Routing

Use an advisory, explicit dependency, routed handoff, or Chief of Staff / Life OS Maintenance coordination when another department must know, act, decide, monitor, or accept responsibility.

Do not duplicate an open loop into another department merely to create awareness.

A department may reference another department's item in notes or status when needed, but the reference should identify:

- the owning department;
- the required local dependency or decision;
- the authoritative source path;
- the trigger for further action.

## Dashboard Visibility Contract

The Department Inspection tab is a read-only aggregation and diagnostic layer.

It may:

- read department and system sources;
- normalize state and priority;
- filter, sort, and search;
- show raw source paths and fragments;
- flag possible duplicates, stale mirrors, mixed fields, and ambiguous parsing;
- expose all department records to Rob for executive visibility.

It must not:

- become an authoritative work ledger;
- write classifications back automatically;
- merge or close records automatically;
- promote department work to system level;
- create advisories or dependencies without explicit authorization;
- hide source ambiguity behind confident-looking output.

Inspector findings are audit prompts, not automatic verdicts. Review the related source records before editing GitHub.

## Boot Visibility Rules

Every HQ receives a small universal operating kernel. After that, context is role-routed.

### Specialist Departments

Specialists read:

- the universal kernel;
- their own handoff, identity, README, status, and open loops;
- only advisories, dependencies, system decisions, or shared policies that are relevant to their current work.

Specialists do not routinely load the global handoff, all active projects, all system loops, migration state, or unrelated department backlogs.

### Chief of Staff HQ

Chief of Staff HQ may read broader shared state when coordinating daily operations, system decisions, cross-department synthesis, department reports, assignments, or a full Hub report.

### Life OS Maintenance HQ

Life OS Maintenance HQ reads broad system state when maintaining boot integrity, shared governance, advisory hygiene, cross-project audits, migrations, source boundaries, or global reconciliation.

### Workers

Workers follow their worker boot contract and do not inherit department or system backlogs unless their contract explicitly requires a pointer.

## Responsibility Map

### Owning Department

- maintains the authoritative department record;
- updates state and next action;
- closes completed work;
- routes real cross-department dependencies;
- avoids speculative and duplicated entries.

### Chief of Staff HQ

- coordinates daily operations, cross-department decisions, reports, assignments, and follow-through;
- identifies when a system coordination record is warranted;
- does not become the routine editor or owner of every department backlog.

### Life OS Maintenance HQ

- maintains global boot and system-loop integrity;
- maintains shared governance and source-boundary rules;
- audits ownership collisions and stale mirrors;
- owns repository-path, migration, archive, and shared-infrastructure work;
- removes system records that no longer meet the promotion threshold;
- routes department-local corrections rather than silently taking over local files.

### Engineering HQ

- maintains the read-only inspector and normalization contract;
- corrects parser defects from observed evidence;
- does not use the inspector to silently rewrite source ownership.

### Rob

- remains final authority;
- may assign, promote, demote, close, or make exceptions explicitly.

## Anti-Patterns

Avoid:

- copying every department priority into global open loops;
- keeping the same task open in multiple departments;
- storing a standing rule as unfinished work;
- keeping “someday, if assigned” placeholders;
- creating a global mirror merely because Rob should be able to see the item;
- using a system closure list as a duplicate history of department completions;
- treating a similar title as proof of duplication without reading the sources;
- letting handoff summaries silently become more authoritative than the owning file.

## Audit Checklist

For each suspected duplicate, ask:

1. What concrete outcome remains unfinished?
2. Which department can determine completion?
3. Must another department actually act or decide?
4. Is the system record coordinating work or merely repeating it?
5. Is this really a rule, watch, note, milestone, or speculative placeholder?
6. Which single record should remain authoritative?
7. What references or advisories are needed after duplicates are removed?

## Operating Principle

> Aggregate broadly. Route deliberately. Own singularly. Reconcile ruthlessly.