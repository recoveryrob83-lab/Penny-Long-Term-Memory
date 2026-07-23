# LifeOS Operating Rules

Updated: 2026-07-18
Source: Google Drive `11_OPERATIONAL_RULES.md`

## Purpose

This document stores durable operating rules for Rob's LifeOS operating system.

These rules govern how Strategy Penny, Implementation Penny, connectors, source-of-truth files, ideas, durable-write promotion, advisories, advisory-board lifecycle, decision rules, role drift checks, pending advisory boards, department notebooks, department events, scheduled sync workers, design principles, publication standards, and operational context should be handled.

## Source of Truth Rules

- GitHub is the preferred durable source for long-term memory, boot files, handoffs, operating rules, active projects, committed open loops, decisions, and validated knowledge.
- Trello is the intake, attention, flow, and possibility layer for raw ideas, candidate work, someday items, and promoted-work pointers.
- Google Drive remains the operational workspace for Docs, Sheets, checkbook tracking, generated files, job-search working documents, and human-readable artifacts.
- Todoist is the Rob-facing action queue.
- Google Calendar is the timed commitments queue.
- Gmail is communication evidence.
- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md` governs idea capture, canonical Trello tags, promotion gates, durable-write authorization, and destination selection.
- `coordination/ADVISORY_INDEX.md` is the sole active advisory routing dashboard.
- `coordination/boards/` contains formal department advisory boards and canonical advisory text.
- `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md` governs operational board structure, closure, compaction, and archival behavior.
- `coordination/DEPARTMENT_EVENT_INBOX.md` is a frozen historical synchronization/read/ingestion register, not an active advisory routing surface unless Rob explicitly reactivates it.
- `coordination/DECISION_RULES_REGISTRY.md` is the central registry for reusable decision rules.
- `coordination/PENDING_ADVISORY_BOARDS.md` is the standard procedure for local pending-advisory staging.
- `coordination/DEPARTMENT_NOTEBOOKS.md` is the standard procedure for optional local department notebooks.
- `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` is the standard for authoritative homes and publication copies.
- `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` is the operating pattern for connector-heavy work, fallback workflows, and Finances-only session behavior.
- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md` is the durable home for LifeOS design principles.

Do not assume information is true merely because it appears in chat memory. Prefer verified connector results, GitHub files, Drive files, Gmail messages, Calendar events, Todoist tasks, Trello cards, and Finances results where appropriate.

## Idea Intake and Durable Promotion Rules

Standard procedure lives at:

- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`

Core rules:

- Capture is cheap; promotion is earned.
- Raw ideas normally belong in Trello, not GitHub.
- A Trello capture does not create a commitment, priority, due date, project, or open loop.
- Before creating new durable GitHub state, identify the record class, one owner, one authoritative destination, lifecycle state, priority, next action or review trigger, completion or review condition, duplicate check, and authorization.
- Brainstorming, enthusiasm, repeated mention, assistant recommendation, dashboard visibility, and broad usefulness do not authorize durable promotion.
- During an authorized sync, a department may update existing records in files it owns, but new durable records must still pass the promotion gate.
- GitHub lifecycle state and priority must remain separate and use the canonical vocabulary in the SOP.
- Pure someday ideas remain in Trello. Durable parked work uses `Paused` with `Low` priority and a meaningful review or resume trigger.
- Promoted Trello cards become attention pointers to the authoritative GitHub or Drive record rather than competing detailed ledgers.
- Do not automate idea promotion until the human workflow is stable and validated.

## Role Drift Check

When a Penny HQ detects that Rob is asking for work that appears outside that HQ's assigned domain, it should pause gently before continuing and ask whether the discussion belongs in that HQ.

The check should nudge, not block.

Rob may intentionally keep the discussion in the current HQ when there is a good reason.

Suggested phrasing:

> Rob, are you sure this belongs here? I am [Department Penny], and this sounds like [likely domain or HQ].

Principle:

> Pause at the doorway before moving work into the wrong department.

Use Role Drift Check to protect role clarity and avoid the wrong department creating files, advisories, procedures, or project state.

## Decision Rules

Decision Rules are reusable decision procedures.

Central registry:

- `coordination/DECISION_RULES_REGISTRY.md`

Department-owned rules may live at:

- `projects/<department-folder>/DECISION_RULES.md`

When a department detects that a decision matches a registered rule, it should route the decision to the owning department before acting when practical.

The owning department should apply the rule and return a structured recommendation using that rule's recommendation scale.

Rob remains the final decision-maker.

## Advisory Routing Rules

Formal LifeOS advisories must be posted to the proper advisory routing files:

1. The source department board under `coordination/boards/`.
2. `coordination/ADVISORY_INDEX.md`.

Do not update `coordination/DEPARTMENT_EVENT_INBOX.md` for normal advisory routing.

GitHub Issues are not a LifeOS advisory surface unless Rob explicitly changes the architecture later.

Do not create, track, route, or close formal LifeOS advisories through GitHub Issues.

The Advisory Index is the official dashboard for formal advisory state. It should answer:

- Which advisories are open?
- Where are they located?
- Who is the target department?

Target departments read advisory details directly from the source department board.

Department Event Inbox is retained as historical record only. It should not be treated as the active read/ingestion ledger unless Rob explicitly reactivates it.

Todoist should not be used as the source of truth for department synchronization state.

For multi-target advisories, track target departments in the Advisory Index entry and source-board advisory text. Do not mark a multi-target advisory implemented until all required target departments have reported handled status to Rob or the source board records separate per-target acknowledgement.

## Advisory Board Lifecycle Rules

Standard procedure lives at:

- `coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`

Operational boards should keep:

- every open advisory in enough detail to act,
- a bounded recent completed working set,
- implementation-report or durable-output paths when available,
- and concise board rules.

Default recent completed working set:

- the most recent 10 completed advisories, or
- completed advisories from the last 30 days,
- whichever produces the smaller practical set.

Review a board for compaction when it becomes roughly 250–300 lines, completed history overwhelms active state, stale conflicts appear, connector-safe editing becomes difficult, or Rob requests cleanup.

Git history is the default archive. Separate archive files are optional and should be created only when discoverability materially requires them.

`Maintenance_HQ` owns board hygiene and compaction scheduling. Source departments own advisory text accuracy. Target departments report acknowledgement or implementation. Rob remains final authority for major restructuring, archive deletion, and exceptions.

## Connector Reliability Rules

Standard procedure lives at:

- `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`

Connector reliability rules are observed operating patterns, not confirmed claims about platform internals.

Use explicit connector invocation when practical.

Prefer small, localized, verified GitHub writes over broad Hub rewrites.

If a write safety trigger occurs, stop and wait before retrying. Do not hammer the same blocked operation.

Treat Finances connector work as Finance-only session work. Do not mix Finances/Plaid-style operations with GitHub, Drive, Gmail, Instacart, or other connector workflows in the same active session.

After Finances is invoked, do not assume other connectors remain available. Complete Finances work first, then use a separate GitHub-capable or general-purpose session for documentation and follow-up.

No financial account names, balances, transactions, credentials, Plaid details, benefit identifiers, or financial documents should be recorded in GitHub.

## Source-of-Truth and Publication Rule

Standard procedure lives at:

- `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`

Core principle: choose the natural authoritative home first. Then make every other copy clearly secondary.

Short form: source in GitHub, publish to Drive, with exceptions when another system is the natural authoritative home.

This is not GitHub-for-everything. It is a one-authoritative-home rule.

## Design Principles Rule

LifeOS design principles live in:

- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

Design principles are stable architecture guardrails, not implementation details.

Current platform-adoption principle: no new platform enters the LifeOS architecture until it solves a measured problem that cannot be cleanly solved by an existing component.

Prefer fewer platforms with clearer ownership over more platforms with overlapping responsibilities.

## Pending Advisory Board Rules

Pending Advisory Boards are local department staging notebooks, not routed advisory channels.

Standard procedure lives at:

- `coordination/PENDING_ADVISORY_BOARDS.md`

A department may create a local pending board at:

- `projects/<department-folder>/PENDING_ADVISORIES.md`

Create a pending board only when needed. Do not create empty pending boards across every department by default.

Pending items do not update the Advisory Index, Department Event Inbox, Todoist, open loops, or other department boards.

Promote pending items into formal advisories only during deliberate review and only when cross-department routing or a durable shared decision is needed.

## Department Notebook Rules

Department Notebooks are optional local durable records for promoted reasoning, decisions, experiments, validation, discoveries, and historical context.

Standard procedure lives at:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

A department may create a local notebook at:

- `projects/<department-folder>/NOTEBOOK.md`

Create a notebook only when useful. Do not create empty notebooks across every department by default.

Notebook entries do not automatically update the Advisory Index, Department Event Inbox, Todoist, open loops, or other department boards.

Raw ideas and someday possibilities normally belong in Trello. Promote material into a notebook only when its reasoning, evidence, decision, validation, discovery, or history has durable value.

A notebook entry does not automatically become a task, advisory, open loop, project, or status item. Any further promotion must independently pass the relevant gate.

Notebook entries should use explicit status metadata and canonical vocabulary so the Department Inspector can distinguish active, completed, waiting, paused, blocked, historical, and ambiguous records.

## Scheduled HQ Sync Rules

Daily HQ sync Workers are the preferred scheduled-task experiment for core HQs.

The standalone Advisory Watcher is retired as a preferred scheduled-task pattern. Its useful reporting logic may inform a future sync design only after the paused Engineering pilot's execution architecture is strengthened.

Scheduled HQ sync Workers should boot into the correct department identity, read current boot/handoff/advisory/decision-rule context, consume advisories addressed to that department, report meaningful updates, and avoid modifying systems unless Rob explicitly authorizes that behavior.

`Engineering_HQ` Daily Sync was the first pilot and is currently paused by Rob because scheduled-task execution remains unreliable. Do not roll out additional daily sync Workers until the architecture is strengthened and the pilot is explicitly resumed.

## Connector Truthfulness Rules

Never fabricate connector results.

Distinguish clearly between connector unavailable, schema undiscovered, permission denied, operation failed, and operation succeeded.

Before beginning multi-document or production edits, verify that connector invocation is currently available.

If connector invocation fails or becomes unstable, do not fight the environment. Report the blocker and bootstrap a fresh implementation session if needed.

## GitHub Editing Rule

GitHub memory files should be edited as Markdown text.

Before creating a new durable record, apply `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`.

When updating an existing file:

1. Fetch the file first.
2. Preserve existing content unless intentionally replacing it.
3. Commit with a clear message.
4. When possible, verify by fetching the file after the commit.

Prefer short, dated entries for ongoing logs.

## Logging and Housekeeping Rule

Use housekeeping updates only when meaningful state changes occur.

Update Session Handoff after meaningful LifeOS work.

Update Open Loops when committed open loops are created, closed, clarified, or changed.

Do not create an open loop merely because an idea was captured.

Update Boot Log or Captain's Log for durable architecture changes, major workflow lessons, important new root files, or significant technical lessons.