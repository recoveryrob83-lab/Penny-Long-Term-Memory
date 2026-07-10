# Engineering Advisory Board

Updated: 2026-07-10
Project: Chief Engineering Penny / Engineering HQ
Purpose: Cross-project advisories from Engineering HQ to Life Logistics HQ, Business HQ, Finance, Main Assistant, or other departments.

## Open Advisories

### ADV-20260710-031 — Establish advisory board lifecycle and compaction standard

- Date: 2026-07-10
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: Medium / High
- Status: Open / Unacknowledged
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): Life OS, advisory routing, GitHub memory hygiene, department boot performance, board maintenance, source-of-truth architecture

#### Executive Summary

Engineering recommends formalizing a Life OS advisory-board lifecycle standard.

The immediate lesson came from the Engineering board, which grew into a very large document because completed advisories accumulated indefinitely alongside active routing state. That made the file slower to read, harder to audit, and easier to leave internally inconsistent.

The preferred operating model is:

> Live boards should show current operational state. Git history and archives should preserve older detail.

This advisory asks Life Logistics HQ to establish and implement a standard that keeps frequently used advisory boards concise, accurate, and boot-friendly without losing durable history.

#### Problem Statement

Advisory boards currently serve two competing functions:

1. Operational routing ledger.
2. Historical archive.

Those functions pull the file in opposite directions.

An operational board should answer quickly:

- What is open?
- What was recently handled?
- What rules govern this board?

A historical archive may contain every prior advisory in full.

When both functions are forced into the same live file indefinitely:

- boards become excessively long,
- startup and review require more context,
- stale statuses are easier to miss,
- closing one advisory may require rewriting a very large file,
- connector writes become riskier,
- active state becomes buried beneath old material,
- and departments may load large amounts of irrelevant history.

#### Recommended Board Categories

Life Logistics should classify advisory boards into two practical categories.

##### 1. Operational Boards

Operational boards are frequently read during boot, daily review, advisory sync, or cross-department coordination.

Recommended initial operational boards:

- `coordination/boards/life-logistics.md`, if present or later created
- `coordination/boards/main-assistant.md`
- `coordination/boards/engineering.md`
- `coordination/boards/business.md`
- `coordination/boards/finance.md`
- `coordination/boards/office-leaks-consulting.md`, if present or later created

These boards should remain compact and should not accumulate every completed advisory forever.

##### 2. Low-Traffic / Historical Boards

Low-traffic boards may retain more history because they are rarely loaded.

Examples may include dormant departments, archived projects, or specialist boards with infrequent advisory activity.

Do not require immediate compaction of every low-traffic board.

Apply compaction only when size, readability, or stale-state risk justifies it.

#### Required Live Board Structure

Operational boards should use a standard structure:

```text
# <Department> Advisory Board

Updated: YYYY-MM-DD
Purpose: ...

## Open Advisories

<all currently open advisories in full>

## Recently Acknowledged / Implemented Advisories

<compact recent working set>

## Board Rule

<routing, source-of-truth, and archive rules>
```

The live board should contain:

- every open advisory in enough detail for the target department to act,
- a limited recent set of completed advisories,
- links or paths to implementation reports when available,
- and the board's operating rules.

#### Recent Working Set Standard

For operational boards, keep a bounded recent completed set.

Recommended default:

- the most recent 10 completed advisories, or
- completed advisories from the last 30 days,
- whichever produces the smaller practical working set.

Life Logistics may adjust this threshold after observing actual usage.

Do not remove a completed advisory from the live board while:

- implementation is still being verified,
- downstream departments still need the full text,
- the advisory is part of an unresolved multi-target chain,
- or the advisory is still referenced by an active open loop.

#### Compaction Trigger

Life Logistics should perform board compaction when any of the following becomes true:

- the board exceeds roughly 250 to 300 lines,
- the completed section materially outweighs the open section,
- routine boot or advisory review loads substantial irrelevant history,
- stale status conflicts appear,
- connector-safe editing becomes difficult,
- or Rob explicitly requests cleanup.

These thresholds are guidance, not rigid law.

The core test is whether the board still functions as a readable operational ledger.

#### Compaction Procedure

Before compacting a board:

1. Read `coordination/ADVISORY_INDEX.md`.
2. Read the source board.
3. Verify the status of every advisory being removed from the live working set.
4. Confirm that no open advisory is removed.
5. Confirm that multi-target advisories are fully acknowledged or separately tracked.
6. Confirm that implementation reports, handoffs, open loops, or other durable records preserve important outcomes.
7. Preserve the current file through Git commit history.

Then:

1. Keep every open advisory in full.
2. Keep the recent completed working set.
3. Condense older completed advisories into short summary entries or remove them from the live board.
4. Preserve full historical text in Git history.
5. Optionally create a board-specific archive file when Git history alone is not sufficiently discoverable.
6. Update the board's `Updated` date.
7. Verify that the Advisory Index and source board agree.
8. Verify that no stale open-loop entry remains solely for board synchronization.

#### Archive Policy

Git commit history is the default historical archive for removed board text.

A separate archive file is optional, not mandatory.

Create a board archive only when:

- humans need convenient in-repository browsing of old advisories,
- an advisory contains durable decisions not captured elsewhere,
- Git history is too difficult for the expected reader,
- or the board has enough volume to justify a yearly or quarterly archive.

Suggested optional paths:

```text
coordination/archive/engineering-advisories-2026.md
coordination/archive/business-advisories-2026.md
coordination/archive/finance-advisories-2026.md
```

Do not create empty archive files for every department.

#### Source-of-Truth Rule

`coordination/ADVISORY_INDEX.md` remains the sole active routing dashboard.

Department boards remain the canonical source for advisory text and source-department outcomes.

Git history or optional archive files preserve older detail.

`coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical record unless Rob explicitly reactivates it.

#### Closure Procedure Standard

When an advisory is completed:

1. Confirm the target department has reported implementation or acknowledgement.
2. Update the source board status.
3. Move the advisory from `Open Advisories` to the recent completed section.
4. Add implementation and closure dates where useful.
5. Add an implementation-report path when one exists.
6. Update the Advisory Index.
7. Update open loops only if the underlying work changed.
8. Verify the source board and Advisory Index agree.
9. Do not leave a separate board-sync open loop after reconciliation succeeds.

This closure procedure should be standard for all boards, even where compaction is not yet necessary.

#### Board Editing Standard

Prefer small, localized updates.

However, when a board has become structurally bloated or internally inconsistent, a deliberate full-file compaction is acceptable if:

- the current file is fetched first,
- all open advisories are preserved,
- completed outcomes remain discoverable,
- Git history preserves the prior version,
- and the resulting file is verified after writing.

Do not rebuild a board casually merely to change one status line.

Do not allow fear of a full-file rewrite to leave known stale operational state indefinitely.

#### Recommended Initial Implementation Scope

Life Logistics should first review and, where necessary, compact these high-use boards:

1. Main Assistant
2. Engineering
3. Business
4. Finance
5. Life Logistics, if a dedicated board exists
6. Office Leaks Consulting, if a dedicated board exists

Engineering has already compacted `coordination/boards/engineering.md` while closing ADV-20260709-030. Treat that board as the first practical example, not necessarily the final universal template.

For each board, Life Logistics should determine:

- current line count,
- number of open advisories,
- number of completed advisories,
- whether stale statuses exist,
- whether older advisories are already represented elsewhere,
- and whether compaction would improve operations.

Do not compact low-use boards merely for symmetry.

#### Durable Standard Requested

Life Logistics should create a concise durable standard, recommended path:

`coordination/ADVISORY_BOARD_LIFECYCLE_STANDARD.md`

The standard should include:

- board categories,
- required live-board structure,
- recent working-set rule,
- compaction triggers,
- compaction procedure,
- archive policy,
- closure procedure,
- source-of-truth rules,
- and implementation ownership.

Life Logistics should also update only the necessary routing or operational-rule files so future department Pennys know the standard exists.

Potential files to review:

- `memory/STARTUP_BOOT.md`
- `memory/03_OPERATIONAL_RULES.md`
- `memory/01_SESSION_HANDOFF.md`
- `coordination/ADVISORY_INDEX.md`
- relevant Life Logistics handoff files

Avoid broad rewrites when a short reference is sufficient.

#### Ownership

- Life Logistics HQ owns advisory-board hygiene and compaction scheduling.
- Source departments own the accuracy of their advisory text and completion outcomes.
- Target departments report acknowledgement or implementation.
- Chief Engineering Penny may advise on file structure, connector safety, and auditability.
- Rob remains final authority for archive deletion, major restructuring, and exceptions.

#### Non-Goals

This advisory does not authorize:

- deleting Git history,
- deleting advisory outcomes that are not preserved elsewhere,
- changing the Advisory Index's role,
- reactivating Department Event Inbox,
- creating archive files for every board by default,
- compacting dormant boards without a practical reason,
- or turning board maintenance into a large recurring bureaucracy.

The goal is a lighter operational surface, not another maintenance cathedral.

#### Implementation Checklist

Before marking this advisory implemented, Life Logistics should verify:

1. A durable advisory-board lifecycle standard exists.
2. Operational and low-traffic boards are distinguished.
3. A recent completed working-set rule exists.
4. Compaction triggers are documented.
5. Closure procedure is documented.
6. Git history is defined as the default historical archive.
7. Optional archive-file criteria are defined.
8. High-use boards were reviewed.
9. Any board actually compacted retains all open advisories.
10. Advisory Index and source boards agree after implementation.
11. Department Event Inbox remains untouched.
12. No sensitive information is introduced into GitHub.
13. Startup or operational rules point to the new standard where useful.
14. ADV-20260710-031 is closed properly on this source board after implementation.

#### Requested Outcome

Life Logistics HQ should create and implement the Life OS Advisory Board Lifecycle Standard, review the high-use boards, compact only where operationally justified, synchronize source-board and Advisory Index state, and report the files created or modified.

## Acknowledged / Implemented Advisories

### ADV-20260709-030 — Create Life OS worker boot standard and Penny Raw Capture Worker

- Date: 2026-07-09
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Implemented / Closed
- Implemented: 2026-07-09
- Closed: 2026-07-10
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Related Project(s): Life OS, Main Assistant, worker architecture, standardized boot system, Google Drive capture inbox, connector truthfulness, custom workers
- Source Advisory: ADV-20260709-029
- Implementation Report: `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

#### Outcome

Life Logistics HQ implemented the formal Life OS worker layer and the first worker package.

Created:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`
- `workers/penny-raw-capture/WORKER_BOOT.md`
- `workers/penny-raw-capture/SESSION_HANDOFF.md`
- `workers/penny-raw-capture/IMPLEMENTATION_REPORT.md`

Updated worker routing and downstream integration in:

- `memory/STARTUP_BOOT.md`
- `memory/00_START_HERE.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/05_OPEN_LOOPS.md`
- `projects/main-assistant/SESSION_HANDOFF.md`
- relevant Life OS logs and routing references

#### Architecture Preserved

- Departments own domains, judgment, strategy, durable state, and cross-project decisions.
- Workers execute narrow, repeatable operations under stable contracts.
- Workers do not automatically load the full department/HQ boot.
- All workers inherit external-operation truthfulness, verification, canonical-resource, privacy, failure, and escalation standards.

#### First Worker

**Penny Raw Capture Worker**

Mission:

> Capture first. Organize later.

Primary function:

- append Rob's raw ideas, reminders, observations, facts, questions, resources, contacts, and other intake to the canonical Google Sheet `Life OS Raw Capture Inbox`,
- preserve wording,
- use Central Time timestamps,
- set `Processed = No`,
- verify writes,
- never fabricate storage success,
- and leave downstream processing to Main Assistant Penny.

#### Canonical Resource

- Sheet title: `Life OS Raw Capture Inbox`
- Stable Sheet ID: recorded in `workers/penny-raw-capture/SESSION_HANDOFF.md`
- Downstream owner: Main Assistant Penny
- Engineering owner for architecture: Chief Engineering Penny
- Cross-project owner: Life Logistics HQ

#### Closure Basis

All implementation quality checks were satisfied:

1. Worker root exists.
2. Shared worker standard exists.
3. Penny Raw Capture Worker boot exists.
4. Worker handoff exists.
5. Canonical Sheet pointer is recorded.
6. Connector truthfulness language is preserved.
7. Worker-specific boot routing is discoverable.
8. Main Assistant understands the processing contract.
9. Advisory Index records implementation.
10. Department Event Inbox remained untouched.
11. No sensitive capture contents were copied into GitHub.
12. No unauthorized Drive deletion or restructuring occurred.
13. The worker can boot without loading the full HQ/global context.

No further implementation work remains under this advisory. Operational pilot testing continues as a normal Engineering open loop, not as an open advisory.

### ADV-20260708-027 — Sync Engineering Office Leaks architecture updates across Life OS

- Date: 2026-07-08
- From: Chief Engineering Penny
- To: Life Logistics HQ
- Priority: High
- Status: Implemented
- Implemented: 2026-07-08
- Posted Board: `coordination/boards/engineering.md`
- Target Department: Life Logistics HQ
- Source Advisory: ADV-20260708-026

#### Outcome

Life Logistics synchronized Engineering's Office Leaks architecture across Life OS.

Engineering outputs preserved:

- `projects/engineering/notebook/NOTE-20260708-005-office-leak-delivery-playbooks-v1.md`
- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- updated Engineering notebook indexes
- updated Drive document `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

Current delivery model:

1. Mechanical workflow layer: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system layer: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

### ADV-20260706-020 — Adopt Finances-only session rule

- Status: Acknowledged / Implemented

Life Logistics adopted the Finances-only session rule as an observed operating pattern, not a confirmed claim about platform internals.

### ADV-20260706-018 — Simplify the Life OS Advisory Routing System

- Status: Acknowledged / Implemented

Life Logistics simplified advisory routing to use source department boards plus the Advisory Index as the sole active routing dashboard. Department Event Inbox is frozen as historical unless Rob explicitly reactivates it.

### ADV-20260706-017 — Adopt connector reliability operating pattern from Gemini/Drive tests

- Status: Acknowledged / Implemented

Life Logistics created `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md` as the durable operating note for explicit connector invocation, small verified writes, waiting after safety triggers, Gemini-as-optional-Drive-artifact-generator, and verification of generated artifacts.

### ADV-20260705-015 — Globalize department notebook leaf routing/index standard

- Status: Acknowledged / Implemented

Life Logistics updated `coordination/DEPARTMENT_NOTEBOOKS.md` to adopt notebook leaf folders, notebook indexes, leaf-note naming/format guidance, and scheduled-worker guidance.

### ADV-20260704-013 — Tighten advisory posting board rules

- Status: Acknowledged / Ingested

Life Logistics clarified that advisories live on the source department's board and target departments are routed through the Advisory Index.

### ADV-20260704-012 — Connector safety-trigger avoidance rules needed

- Status: Acknowledged / Ingested

Engineering incorporated connector safety-trigger avoidance into the Reliable Connector Execution Layer.

## Board Rule

- Formal advisories originate on the source department board.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- `coordination/DEPARTMENT_EVENT_INBOX.md` remains frozen historical record unless Rob explicitly reactivates it.
- Full prior advisory text remains available through Git commit history.