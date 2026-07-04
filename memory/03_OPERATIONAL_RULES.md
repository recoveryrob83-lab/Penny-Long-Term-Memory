# Life OS Operating Rules

Updated: 2026-07-04
Source: Google Drive `11_OPERATIONAL_RULES.md`

## Purpose

This document stores durable operating rules for Rob's Life OS / Life Logistics HQ system.

These rules govern how Strategy Penny, Implementation Penny, connectors, source-of-truth files, advisories, pending advisory boards, department notebooks, department events, scheduled sync workers, design principles, publication standards, and operational context should be handled.

## Source of Truth Rules

As of the GitHub migration work on 2026-07-02:

- GitHub is being promoted to the preferred durable source for long-term memory, boot files, handoffs, operating rules, active projects, and open loops.
- Google Drive remains the operational workspace for Docs, Sheets, checkbook tracking, generated files, job-search working documents, and other human-readable artifacts.
- Todoist is the Rob-facing action queue.
- Google Calendar is the timed commitments queue.
- Gmail is communication evidence.
- `coordination/ADVISORY_INDEX.md` is the advisory dashboard.
- `coordination/DEPARTMENT_EVENT_INBOX.md` is the department synchronization/read/ingestion register.
- `coordination/PENDING_ADVISORY_BOARDS.md` is the standard procedure for local pending-advisory staging.
- `coordination/DEPARTMENT_NOTEBOOKS.md` is the standard procedure for optional local department notebooks.
- `coordination/SOURCE_OF_TRUTH_AND_PUBLICATION_STANDARD.md` is the standard for authoritative homes and publication copies.
- `projects/life-os-infrastructure/DESIGN_PRINCIPLES.md` is the durable home for Life OS design principles.

Do not assume information is true merely because it appears in chat memory. Prefer verified connector results, GitHub files, Drive files, Gmail messages, Calendar events, and Todoist tasks.

Label unverified facts clearly.

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

## Advisory and Department Event Rules

Advisory boards live under `coordination/boards/`.

The Advisory Index is the official dashboard for advisory state.

The Department Event Inbox is the working notification/register layer for department read and ingestion state.

Todoist should not be used as the source of truth for department synchronization state.

For multi-target advisories, do not mark acknowledged or implemented until all targeted departments have reported read/handled status to Rob, unless the source department records separate per-target acknowledgements.

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

Scheduled HQ sync workers should:

- Boot into the correct department identity.
- Read current boot, handoff, Advisory Index, and Department Event Inbox context.
- Consume advisories addressed to that department.
- Report meaningful updates, routing needs, documentation recommendations, or issues.
- Avoid modifying GitHub, Google Drive, Todoist, Calendar, Gmail, or other systems unless Rob explicitly authorizes that behavior.

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