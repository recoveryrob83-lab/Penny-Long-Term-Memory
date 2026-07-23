# LifeOS Advisory Board Lifecycle Standard

Updated: 2026-07-10
Owner: Maintenance_HQ
Purpose: Keep advisory boards concise, accurate, boot-friendly, and auditable without losing durable history.

## Core Principle

> Live boards show current operational state. Git history and optional archives preserve older detail.

Advisory boards are operational routing ledgers first. They should answer quickly:

- What is open?
- What was recently completed?
- What rules govern this board?

They should not accumulate every completed advisory forever when that history makes the live board difficult to read or safely edit.

## Source-of-Truth Model

- `coordination/ADVISORY_INDEX.md` is the sole active advisory routing dashboard.
- The source department board under `coordination/boards/` is the canonical source for full open advisory text and source-department outcomes.
- Git commit history is the default historical archive for text removed during compaction.
- Optional files under `coordination/archive/` may preserve older advisory detail when convenient browsing is materially useful.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical record unless Rob explicitly reactivates it.
- Todoist and GitHub Issues are not advisory-state systems unless Rob explicitly changes the architecture.

## Board Categories

### Operational Boards

Operational boards are read frequently during boot, daily review, advisory synchronization, or cross-department coordination.

Current operational boards include:

- `coordination/boards/main-assistant.md`
- `coordination/boards/engineering.md`
- `coordination/boards/business.md`
- `coordination/boards/finance.md`
- `coordination/boards/office-leaks.md`
- a future `Maintenance_HQ` board, if one is created

Operational boards use the bounded recent-working-set rules in this standard.

### Low-Traffic / Historical Boards

Low-traffic boards belong to dormant departments, archived projects, or specialist areas with infrequent advisory activity.

They may retain more completed history when the board remains readable and safe to maintain.

Do not compact low-traffic boards merely for symmetry.

## Required Live-Board Structure

Operational boards should use:

```text
# <Department> Advisory Board

Updated: YYYY-MM-DD
Purpose: ...

## Open Advisories

<all currently open advisories in sufficient detail to act>

## Recently Acknowledged / Implemented Advisories

<bounded recent working set>

## Board Rule

<routing, source-of-truth, closure, and archive rules>
```

The live board should contain:

- every open advisory in enough detail for the target department to act,
- a limited recent set of completed advisories,
- implementation-report or durable-output paths when available,
- and the board operating rules.

## Recent Completed Working Set

Default for operational boards:

- keep the most recent 10 completed advisories, or
- keep completed advisories from the last 30 days,
- whichever produces the smaller practical working set.

`Maintenance_HQ` may adjust this threshold when actual use shows a better balance.

Do not remove a completed advisory from the live board while:

- implementation is still being verified,
- downstream departments still need the full text,
- it belongs to an unresolved multi-target chain,
- it is referenced by an active open loop,
- or its important outcome is not preserved elsewhere.

## Compaction Triggers

Review an operational board for compaction when one or more apply:

- the board exceeds roughly 250 to 300 lines,
- completed material materially outweighs open material,
- routine boot or review loads substantial irrelevant history,
- stale or conflicting statuses appear,
- connector-safe editing becomes difficult,
- the board no longer functions as a readable operational ledger,
- or Rob explicitly requests cleanup.

These are practical signals, not rigid law.

## Compaction Procedure

Before compacting:

1. Read `coordination/ADVISORY_INDEX.md`.
2. Read the full source board.
3. Verify the status of every advisory leaving the live working set.
4. Confirm no open advisory will be removed.
5. Confirm multi-target advisories are fully handled or separately tracked.
6. Confirm important outcomes exist in implementation reports, handoffs, open loops, standards, notebooks, or other durable files.
7. Fetch the current board and preserve it through Git commit history.

Then:

1. Keep every open advisory in full.
2. Keep the bounded recent completed working set.
3. Condense or remove older completed advisories.
4. Preserve prior full text through Git history.
5. Create a separate archive only when archive criteria are met.
6. Update the board date.
7. Verify the source board and Advisory Index agree.
8. Remove stale open loops that existed only for board synchronization.
9. Fetch the board after writing and verify the result.

## Archive Policy

Git history is the default archive.

Create a board-specific archive only when:

- humans need convenient in-repository browsing,
- an advisory contains durable decisions not preserved elsewhere,
- expected readers cannot reasonably use Git history,
- or the board volume justifies a yearly or quarterly archive.

Suggested optional paths:

```text
coordination/archive/engineering-advisories-2026.md
coordination/archive/business-advisories-2026.md
coordination/archive/finance-advisories-2026.md
```

Do not create empty archive files for every department.

Do not delete Git history.

## Closure Procedure

When an advisory is completed:

1. Confirm the target department reported acknowledgement or implementation.
2. Update the source-board status.
3. Move it from `Open Advisories` to `Recently Acknowledged / Implemented Advisories`.
4. Add acknowledgement, implementation, and closure dates when useful.
5. Add an implementation-report or durable-output path when one exists.
6. Update `coordination/ADVISORY_INDEX.md`.
7. Update open loops only when the underlying work changed.
8. Verify the source board and Advisory Index agree.
9. Do not leave a separate board-sync open loop after reconciliation succeeds.

## Board Editing Standard

Prefer small localized changes for routine status updates.

A deliberate full-file rewrite is acceptable when a board is structurally bloated or internally inconsistent, provided:

- the current file is fetched first,
- all open advisories are preserved,
- completed outcomes remain discoverable,
- Git history preserves the prior version,
- and the result is verified after writing.

Do not rebuild a board casually to change one line.

Do not leave known stale operational state merely to avoid a justified compaction.

## Ownership

- `Maintenance_HQ` owns this standard, board hygiene reviews, and compaction scheduling.
- Source departments own the accuracy of their advisory text and completion outcomes.
- Target departments report acknowledgement or implementation.
- `Engineering_HQ` may advise on file structure, connector safety, and auditability.
- Rob is final authority for archive deletion, major restructuring, exceptions, or reactivation of retired routing surfaces.

## Review Cadence

Review operational boards during:

- meaningful `Maintenance_HQ` housekeeping,
- morning or nightly sync when board size or inconsistency is apparent,
- advisory closure that requires a large write,
- or explicit cleanup requests.

Do not create a separate recurring bureaucracy solely to count lines.

## Privacy

Keep advisory boards abstract and non-sensitive.

Do not introduce personal, medical, financial-account, client-identifying, credential, tax, or other sensitive operational details during compaction or archival work.