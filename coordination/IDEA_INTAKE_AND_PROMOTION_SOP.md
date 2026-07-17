# Idea Intake and Promotion SOP

Updated: 2026-07-18
Project: Life OS Coordination
Purpose: Define how ideas enter Life OS, how Trello holds possibility and attention, when an idea earns durable promotion, and what every department must verify before writing new GitHub state.

## Core Principle

Capture is cheap. Promotion is earned.

Rob may generate, explore, and preserve as many ideas as useful without turning each idea into a commitment, open loop, project, or system obligation.

Short form:

> Capture freely. Clarify deliberately. Promote selectively. Own singularly.

## Source-System Roles

### Conversation

Conversation is the reasoning surface.

Use it to explore, challenge, combine, discard, and reshape ideas. A conversational idea is not durable state unless Rob authorizes capture or promotion.

### Trello

Trello is the intake, attention, and possibility layer.

Use it for:

- raw ideas;
- questions worth revisiting;
- possible projects;
- experiments not yet approved;
- opportunities;
- someday items;
- candidate work awaiting evaluation;
- promoted work that still needs an attention pointer.

A Trello card may preserve an idea without creating an obligation.

### GitHub

GitHub is durable abstract state.

Use it for:

- committed unfinished work;
- authoritative decisions;
- validated knowledge and experiment results;
- approved standing rules;
- operating watches;
- system architecture;
- historical milestones worth preserving.

GitHub is not the raw-idea inbox.

### Drive and Other Systems

- Drive holds working records, drafts, detailed documents, and artifacts.
- Todoist holds Rob-facing commitments and reminders.
- Calendar holds timed commitments.
- Gmail holds communication evidence.
- The dashboard is a read-only visibility and diagnostic layer.

Do not copy the same detailed truth into several systems merely for visibility.

## Idea Lifecycle

Use these logical stages. Trello list names may differ, but the meaning must remain stable.

1. **Captured:** The idea exists. No commitment is implied.
2. **Clarifying:** The idea is being defined, researched, or separated from adjacent ideas.
3. **Candidate:** The idea is clear enough for a promotion decision.
4. **Promoted:** The idea has an owner, authoritative destination, and accepted next action or review condition.
5. **Parked:** The idea is intentionally non-current and has a meaningful review or resume trigger.
6. **Rejected / Archived:** The idea will not be pursued under current assumptions.

Moving an idea forward requires new information. Repeated enthusiasm alone is not promotion evidence.

## Minimum Capture Standard

A raw Trello capture needs only:

- a clear enough title to recognize later;
- the source or context when useful;
- `stage/captured`.

Do not force priority, due date, owner, or project structure onto a raw idea.

Raw capture must remain friction-light. The system should not punish creativity with paperwork at the doorway.

## Canonical Trello Tag Vocabulary

Use one value from each relevant tag family. Do not invent synonyms when a canonical value fits.

### Stage

- `stage/captured`
- `stage/clarifying`
- `stage/candidate`
- `stage/promoted`
- `stage/parked`
- `stage/rejected`

### Type

- `type/idea`
- `type/project`
- `type/task`
- `type/experiment`
- `type/decision`
- `type/rule`
- `type/watch`
- `type/reference`

### Owner

- `owner/main`
- `owner/logistics`
- `owner/engineering`
- `owner/business`
- `owner/office-leaks`
- `owner/finance`
- `owner/wellness`
- `owner/system`
- `owner/project/<slug>`
- `owner/unassigned`

`owner/unassigned` is allowed during capture and clarification. It is not allowed at promotion.

### Horizon

- `horizon/now`
- `horizon/next`
- `horizon/later`
- `horizon/someday`

### Scope

- `scope/personal`
- `scope/department`
- `scope/cross-department`
- `scope/system`

### Context Tags

Optional context tags may describe a topic, campaign, product, person, or location. Limit them to the smallest useful set, normally no more than three.

Do not duplicate stage, owner, scope, horizon, or type as free-form context tags.

## Clarification Standard

Before an idea becomes a promotion candidate, clarify:

- What problem, opportunity, question, or outcome does it address?
- Why might it matter?
- Who is the likely owner?
- What would the smallest useful version look like?
- What time, money, energy, access, or dependency would it require?
- Does an equivalent idea, project, note, or open loop already exist?
- What would make it worth doing now rather than later?
- What event should trigger review if it remains parked?

Avoid mandatory numerical scoring unless repeated use proves that scoring improves decisions.

## Promotion Gate

An idea may enter GitHub only when all required questions have answers.

1. **Record class:** Is this committed work, a decision, evidence, a rule, a watch, or a milestone?
2. **Owner:** Which single department or project owns the authoritative record?
3. **Scope:** Is it personal, department-owned, cross-department, or truly system-level?
4. **Outcome:** What concrete result, decision, or preserved knowledge justifies durability?
5. **State:** What is its current lifecycle state?
6. **Priority:** What is its priority after commitment?
7. **Next action or trigger:** What happens next, or what event causes review or resumption?
8. **Completion or review condition:** How will Life OS know the record no longer belongs in its current state?
9. **Duplicate check:** Where is related authoritative state already stored?
10. **Authorization:** Has Rob or an authorized operating command approved the durable write or promotion?

If any required answer is missing, keep the item in Trello or ask one concise clarification. Do not manufacture certainty.

## Durable Write Authorization

A durable GitHub write is authorized when at least one of these is true:

- Rob explicitly asks to record, update, sync, promote, implement, or commit the change;
- Rob authorizes a defined housekeeping, audit, or synchronization scope;
- an accepted advisory or system coordination action explicitly requires the write;
- an authorized department sync corrects stale state within that department's owned files.

The following do not authorize durable promotion by themselves:

- brainstorming;
- enthusiasm;
- repeated mention;
- assistant recommendation;
- a raw Trello capture;
- a dashboard finding;
- broad usefulness;
- the possibility that an idea may matter later.

When authorization is ambiguous, remain read-only or capture in Trello rather than GitHub.

## Destination Rules

### Keep in Trello

Keep an item in Trello when it is speculative, unowned, unprioritized, exploratory, someday-oriented, or awaiting a real decision.

### Promote to a Department Open Loop

Promote to the owning department's `open_loops.md` when:

- future action is genuinely committed;
- one department owns completion;
- state and priority are explicit;
- a smallest useful next action is known;
- a completion or review condition exists.

Use the canonical table:

```markdown
| Status | Priority | Item | Next Action | Notes |
|---|---|---|---|---|
| Active | High | Example item | Perform the smallest useful next action | Include completion, review, dependency, or source context |
```

### Promote to a Notebook

Promote to a department notebook when the durable value is reasoning, evidence, a decision, validation, discovery, or historical context.

A notebook does not automatically create work.

Notebook records must include explicit metadata near the top when practical:

```text
Date: YYYY-MM-DD
Updated: YYYY-MM-DD
Department: <department>
Status: <canonical status>
Owner: <owner>
Record Type: <note, decision, experiment, validation, milestone>
Authority: <authoritative, summary, historical, derived>
```

Experiment notes may place an authoritative result status in a later result section, but a concise top-level status is preferred.

### Promote to a Rule or SOP

Promote to a standing rule or SOP when:

- the behavior is approved;
- it is expected to recur;
- it governs more than one isolated task;
- the authoritative location is clear;
- replacing the rule would require an intentional policy change.

Do not create an open loop merely to remember an enduring rule.

### Promote to System Memory

Promote to `memory/05_OPEN_LOOPS.md` only when the threshold in `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md` is met.

Shared visibility is not system ownership.

### Route Through an Advisory

Use an advisory when another department must act, decide, accept responsibility, or durably acknowledge a dependency.

Do not duplicate the same open loop into every affected department.

### Store the Working Artifact in Drive

When the durable GitHub record points to a detailed draft, ledger, design, spreadsheet, or document, keep the working artifact in Drive and store only the durable abstract state or pointer in GitHub.

## Canonical GitHub Vocabulary

### Lifecycle State

Use only:

- `Open`
- `Active`
- `Waiting`
- `Paused`
- `Blocked`
- `Completed`
- `Cancelled`

Do not use `Parked` as a GitHub lifecycle status. Durable parked work becomes `Paused` with `Low` priority and a review or resume trigger. Pure someday ideas remain in Trello.

### Priority

Use only:

- `Critical`
- `High`
- `Normal`
- `Low`
- `None`

Keep priority separate from lifecycle state. Do not use words such as `Priority` or `Urgent` as a status.

### Authority

Use:

- `Authoritative`
- `Summary`
- `Historical`
- `Derived`

A summary or dashboard representation must point back to the authoritative record rather than becoming a competing source.

## Department Write Contract

Before creating or materially expanding durable state, every department must:

1. Apply this promotion gate.
2. Search its own canonical files for an existing record.
3. Check relevant system or cross-department state only when routing requires it.
4. Select one authoritative destination.
5. Use explicit canonical state and priority.
6. Record the smallest useful next action or review trigger.
7. Avoid speculative placeholders.
8. Avoid duplicating another department's work for awareness.
9. Preserve evidence in a notebook rather than bloating an open-loop row.
10. Verify significant writes when practical.

Routine updates to an existing authoritative record do not require creating a new Trello idea card.

## Promoted Trello Cards

After promotion:

- add `stage/promoted`;
- replace `owner/unassigned` with the actual owner;
- add the authoritative GitHub path or Drive pointer;
- keep only the context needed for attention and flow;
- do not maintain a competing detailed backlog inside the card;
- archive or close the card when it no longer serves attention flow.

Trello remains the attention pointer. GitHub becomes the durable authority.

## Parking, Rejection, and De-Elevation

### Park

Park an idea when it is still potentially useful but not currently committed.

A parked card must name a review trigger such as:

- after a current project closes;
- when funding reaches a threshold;
- when a dependency becomes available;
- during the next quarterly review;
- when Rob explicitly reactivates it.

Avoid arbitrary due dates for someday ideas.

### Reject or Archive

Reject or archive when:

- the expected value is too low;
- it conflicts with current goals;
- the cost or risk is unacceptable;
- another existing solution is sufficient;
- the idea was useful exploration but does not require future attention.

Do not preserve rejected ideas in GitHub unless the rejection decision itself has durable strategic value.

### De-Elevate

Move committed work back to Trello or archive it when it is no longer committed and no durable dependency remains.

Preserve only historically useful decisions or evidence in GitHub. Do not leave zombie open loops behind.

## Review Rhythm

Review ideas intentionally, not continuously.

- Raw capture may happen at any time.
- Clarification should occur during planning, department review, or an intentional idea-processing session.
- Candidate promotion should occur when capacity, timing, and ownership can be evaluated.
- Parked ideas should be reviewed only at their stated trigger or a deliberate periodic review.
- Do not make every capture a daily obligation.

## Responsibility Map

### Rob

- remains final authority;
- may capture without commitment;
- approves promotion, exceptions, and major reprioritization;
- may designate an item system-level explicitly.

### Main Assistant

- supports low-friction capture and clarification;
- helps identify the likely owner and destination;
- prevents raw ideas from becoming accidental commitments;
- coordinates genuine cross-department promotion.

### Owning Department

- evaluates candidate ideas within its domain;
- applies the promotion gate;
- maintains the single authoritative durable record after promotion;
- updates, pauses, closes, or de-elevates the record as reality changes.

### Logistics

- maintains this shared governance;
- audits source boundaries, duplicate ownership, stale records, and tag drift;
- coordinates system-level promotion and demotion rules.

### Engineering

- maintains dashboard and parser support for the canonical structured vocabulary;
- adds automation only after the human workflow is stable and validated;
- does not auto-promote ideas or rewrite authority.

### Workers

- may capture or transform information under their contracts;
- may not promote raw material into department or system authority unless explicitly authorized.

## Anti-Patterns

Avoid:

- writing every exciting idea directly into `open_loops.md`;
- assigning fake urgency during capture;
- creating a project before an owner and next action exist;
- copying the same idea into several departments;
- using system memory as an executive idea dump;
- maintaining full details in both Trello and GitHub;
- turning notebook history into current work without a decision;
- leaving promoted cards without authoritative pointers;
- preserving rejected ideas as zombie commitments;
- automating promotion before the human rules are proven.

## Examples

### Raw Business Idea

“Tell a story about a business losing a $750 job because nobody followed up.”

Keep in Trello as `type/idea`, `owner/business`, and an appropriate horizon until Business decides on a concrete campaign or experiment.

### Approved Dashboard Fix

“Add a visible warning filter to Department Inspection.”

Once authorized, promote to Engineering-owned work with explicit next action and completion test. Preserve validation evidence in an Engineering notebook when useful.

### Connector Experiment

“Test whether a Google Drive write succeeds after cooldown.”

Promote to an Engineering experiment when the test protocol and authorization exist. Store the result in a notebook. Close the execution loop after verification.

### Shared Operating Rule

“All department open-loop tables separate status from priority.”

Store as a shared SOP or architecture rule. Do not copy it into seven department backlogs.

## Audit Checklist

For every proposed durable record, ask:

1. Is this still an idea, or has it become a commitment, decision, rule, watch, or evidence record?
2. Why is Trello no longer sufficient?
3. Who owns the authoritative record?
4. What exact destination should hold it?
5. What are its state, priority, next action, and completion or review condition?
6. Does an equivalent record already exist?
7. Does another department actually need to act or merely see it?
8. Is the write authorized?
9. What should remain in Trello after promotion?
10. What will remove or close this record later?

## Operating Principle

> Let ideas be abundant. Let commitments be deliberate. Let durable truth stay clean.
