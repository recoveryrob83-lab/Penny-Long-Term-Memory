# Department File Ownership and Drift Management SOP

Updated: 2026-07-18
Project: Life OS Coordination
Purpose: Define how departments maintain their own durable GitHub state while minimizing Rob's manual routing burden.

## Core Rule

Each department is responsible for maintaining the GitHub files and sections within its own domain.

The department that owns the working context should normally update the durable record directly rather than routing routine maintenance through Life OS Maintenance HQ.

Short form:

> Departments maintain their own rooms. Chief of Staff coordinates. Life OS Maintenance protects the shared operating system.

## Companion Governance Rules

Open-loop classification, system-promotion thresholds, lifecycle rules, boot visibility, idea intake, and durable-write promotion are defined in:

- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`
- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`

Apply all three SOPs together.

A department file owns its local truth. The dashboard may aggregate that truth, but global visibility does not justify copying the record into system memory or another department.

Raw ideas normally remain in Trello until they pass the promotion gate. Department ownership does not authorize turning every useful thought into durable GitHub state.

## Why This Rule Exists

The ideal architecture would automate cross-department synchronization, advisory consumption, and routine memory maintenance. The current platform does not provide a reliable low-friction way to automate the seven department HQ chats and their advisories.

Routing every routine change through Rob and then through Life OS Maintenance HQ creates unnecessary switching, delay, and cognitive load. Because each department chat already holds the most current working context for its domain, that department is usually best positioned to detect and correct drift.

Reality takes priority over architectural purity when the cleaner design makes Rob the manual message bus.

## Department Responsibilities

Each department owns routine maintenance of its own project subtree, including as applicable:

- `README.md`
- `DEPARTMENT_IDENTITY.md`
- `SESSION_HANDOFF.md`
- `status.md`
- `open_loops.md`
- `DECISION_RULES.md`
- `NOTEBOOK.md`
- local procedures, implementation notes, and other department-specific files
- its own advisory board text when that department is the source

During routine work, syncs, and boots, the department should:

1. Compare current working context with its canonical GitHub files.
2. Correct stale assumptions, outdated status, closed or changed open loops, and missing durable decisions.
3. Keep edits localized to files it owns.
4. Verify significant writes when practical.
5. Avoid creating duplicate sources of truth.
6. Separate unfinished work from standing rules, watches, historical milestones, and speculative placeholders.
7. Keep one authoritative record for each department-owned loop.
8. Apply `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md` before creating new durable state from an idea, brainstorm, note, or Trello card.
9. Use explicit canonical lifecycle state and priority rather than combined or improvised labels.
10. Preserve raw possibilities in Trello until ownership, outcome, next action or review trigger, destination, and authorization are clear.

## Chief of Staff HQ Responsibilities

Chief of Staff HQ owns:

- daily operations and executive-function support;
- chairing LifeOS HQ;
- cross-department coordination and synthesis;
- routing assignments, decisions, reports, and follow-through;
- identifying when a local department change has broader consequences;
- deciding when an advisory or coordinated update is warranted;
- supporting low-friction idea capture without creating accidental commitments;
- helping clarify ownership and destination before promotion.

Chief of Staff HQ should not become the routine editor of every department's internal files or promote every useful idea into system memory.

## Life OS Maintenance HQ Responsibilities

Life OS Maintenance HQ owns shared operational infrastructure, governance, and cross-system hygiene, including:

- global boot and routing integrity;
- global handoffs and operating rules;
- shared operating procedures;
- advisory-index and board hygiene;
- cross-project audits and drift detection;
- system open-loop and architecture review;
- source-of-truth and ownership enforcement;
- repository-path, migration, archive, and shared-infrastructure work;
- system-wide housekeeping when requested and authorized;
- reconciliation between the Drive Chief's Manual, Project Instructions, and GitHub implementation;
- auditing durable-write promotion, source boundaries, duplicate ownership, and canonical tag drift.

Life OS Maintenance HQ is not the default implementation bottleneck for routine department file maintenance.

Maintenance detects department-local drift and routes precise corrections. It does not silently edit another department's files without explicit coordinated-repair authority.

## Durable Write Threshold

A department may update an existing authoritative record during an authorized sync or maintenance action.

Before creating a new durable record, the department must confirm:

- the record class;
- the single owner;
- the authoritative destination;
- lifecycle state and priority;
- smallest useful next action or review trigger;
- completion or review condition;
- duplicate check;
- explicit or command-scoped authorization.

If those fields are not clear, keep the material in conversation or Trello rather than manufacturing a GitHub commitment.

## Advisory Threshold

Do not create an advisory for routine maintenance confined to one department.

Use an advisory when:

- another department must act or decide;
- a change affects multiple departments;
- a shared policy or architecture boundary changes;
- a dependency, conflict, risk, or handoff must be durably communicated;
- Rob asks for formal cross-department routing.

Routine local edits should remain local.

## Shared and Cross-Cutting Files

A department should not casually edit shared or another department's canonical files.

When a change touches:

- `memory/STARTUP_BOOT.md`;
- `memory/05_OPEN_LOOPS.md`;
- global operating rules or SOPs;
- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`;
- shared coordination files;
- another department's project subtree;
- the Advisory Index;
- system architecture files;

route through Chief of Staff HQ, Life OS Maintenance HQ, the owning department, or an explicit coordinated action as appropriate.

System files must not become mirrors of department backlogs. When shared coordination is genuinely needed, use the compact coordination-record rules in `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`.

## Rob's Role

Rob remains the final authority and may direct any department to update, coordinate, promote, demote, or make an exception.

Rob does not need to manually relay every routine internal change. As department chats are used, booted, and synchronized, their context windows will naturally surface drift and support direct maintenance of their own canonical files.

Rob may capture ideas without committing to them. Capture permission is not durable-write permission unless the instruction also authorizes promotion or recording.

## Operating Principle

> Decentralize maintenance. Preserve ownership. Promote deliberately. Escalate only across boundaries.