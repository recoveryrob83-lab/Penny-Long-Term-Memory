# Life OS Operating Rules

Updated: 2026-07-06
Source: Google Drive `11_OPERATIONAL_RULES.md`

## Purpose

This document stores durable operating rules for Rob's Life OS / Life Logistics HQ system.

These rules govern how Strategy Penny, Implementation Penny, connectors, source-of-truth files, advisories, decision rules, role drift checks, pending advisory boards, department notebooks, department events, scheduled sync workers, design principles, publication standards, and operational context should be handled.

## Source of Truth Rules

- GitHub is the preferred durable source for long-term memory, boot files, handoffs, operating rules, active projects, and open loops.
- Google Drive remains the operational workspace for Docs, Sheets, checkbook tracking, generated files, job-search working documents, and human-readable artifacts.
- Todoist is the Rob-facing action queue.
- Google Calendar is the timed commitments queue.
- Gmail is communication evidence.
- `coordination/ADVISORY_INDEX.md` is the sole active advisory routing dashboard.
- `coordination/boards/` contains formal department advisory boards and canonical advisory text.
- `coordination/DEPARTMENT_EVENT_INBOX.md` is a frozen historical synchronization/read/ingestion register, not an active advisory routing surface unless Rob explicitly reactivates it.
- `coordination/DECISION_RULES_REGISTRY.md` is the central registry for reusable decision rules.
- `coordination/PENDING_ADVISORY_BOARDS.md` is the standard procedure for local pending-advisory staging.
- `coordination/DEPARTMENT_NOTEBOOKS.md` is the standard procedure for optional local department notebooks.
- `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` is the standard for authoritative homes and publication copies.
- `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` is the operating pattern for connector-heavy work and fallback workflows.
- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md` is the durable home for Life OS design principles.

Do not assume information is true merely because it appears in chat memory. Prefer verified connector results, GitHub files, Drive files, Gmail messages, Calendar events, and Todoist tasks.

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

Formal Life OS advisories must be posted to the proper advisory routing files:

1. The source department board under `coordination/boards/`.
2. `coordination/ADVISORY_INDEX.md`.

Do not update `coordination/DEPARTMENT_EVENT_INBOX.md` for normal advisory routing.

GitHub Issues are not a Life OS advisory surface unless Rob explicitly changes the architecture later.

Do not create, track, route, or close formal Life OS advisories through GitHub Issues.

The Advisory Index is the official dashboard for formal advisory state. It should answer:

- Which advisories are open?
- Where are they located?
- Who is the target department?

Target departments read advisory details directly from the source department board.

Department Event Inbox is retained as historical record only. It should not be treated as the active read/ingestion ledger unless Rob explicitly reactivates it.

Todoist should not be used as the source of truth for department synchronization state.

For multi-target advisories, track target departments in the Advisory Index entry and source-board advisory text. Do not mark a multi-target advisory implemented until all required target departments have reported handled status to Rob or the source board records separate per-target acknowledgement.

## Source-of-Truth and Publication Rule

Standard procedure lives at:

- `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md`

Core principle: choose the natural authoritative home first. Then make every other copy clearly secondary.

Short form: source in GitHub, publish to Drive, with exceptions when another system is the natural authoritative home.

This is not GitHub-for-everything. It is a one-authoritative-home rule.

## Design Principles Rule

Life OS design principles live in:

- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md`

Design principles are stable architecture guardrails, not implementation details.

Current platform-adoption principle: no new platform enters the Life OS architecture until it solves a measured problem that cannot be cleanly solved by an existing component.

Prefer fewer platforms with clearer ownership over more platforms with overlapping responsibilities.

## Pending Advisory Board Rules

Pending Advisory Boards are local department staging notebooks, not routed advisory channels.

Standard procedure lives at:

- `coordination/PENDING_ADVISORY_BOARDS.md`

A department may create a local pending board at:

- `projects/<department-folder>/PENDING_ADVISORIES.md`

Create a pending board only when needed. Do not create empty pending boards across every department by default.

Pending items do not update the Advisory Index, Department Event Inbox, Todoist, or other department boards.

Promote pending items into formal advisories only during deliberate review and only when cross-department routing or a durable shared decision is needed.

## Department Notebook Rules

Department Notebooks are optional local sketchpads for durable idea capture.

Standard procedure lives at:

- `coordination/DEPARTMENT_NOTEBOOKS.md`

A department may create a local notebook at:

- `projects/<department-folder>/NOTEBOOK.md`

Create a notebook only when useful. Do not create empty notebooks across every department by default.

Notebook entries do not update the Advisory Index, Department Event Inbox, Todoist, open loops, or other department boards.

Use notebooks for ideas worth preserving that are not yet tasks, advisories, open loops, handoff state, design principles, or Drive artifacts.

## Scheduled HQ Sync Rules

Daily HQ sync workers are the preferred scheduled-task experiment for core HQs.

The standalone Advisory Watcher is no longer the preferred scheduled-task slot usage; its useful reporting logic is folded into daily HQ sync prompts.

Scheduled HQ sync workers should boot into the correct department identity, read current boot/handoff/advisory/decision-rule context, consume advisories addressed to that department, report meaningful updates, and avoid modifying systems unless Rob explicitly authorizes that behavior.

Engineering HQ Daily Sync is the first pilot. Observe results before rolling out additional daily sync workers.

## Connector Truthfulness Rules

Never fabricate connector results.

Distinguish clearly between connector unavailable, schema undiscovered, permission denied, operation failed, and operation succeeded.

Before beginning multi-document or production edits, verify that connector invocation is currently available.

If connector invocation fails or becomes unstable, do not fight the environment. Report the blocker and bootstrap a fresh Implementation Penny session if needed.

## GitHub Editing Rule

GitHub memory files should be edited as Markdown text.

When updating an existing file:
1. Fetch the file first.
2. Preserve existing content unless intentionally replacing it.
3. Commit with a clear message.
4. When possible, verify by fetching the file after the commit.

Prefer short, dated entries for ongoing logs.

## Logging and Housekeeping Rule

Use housekeeping updates only when meaningful state changes occur.

Update Session Handoff after meaningful Life OS work.

Update Open Loops when open loops are created, closed, clarified, or changed.

Update Boot Log or Captain's Log for durable architecture changes, major workflow lessons, important new root files, or significant technical lessons.