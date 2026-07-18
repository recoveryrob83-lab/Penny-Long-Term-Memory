# Department Ownership and Dashboard Inspection

Date: 2026-07-17
Updated: 2026-07-18
Department: Engineering HQ
Status: MVP locally validated / source and parser cleanup verified / ordinary boot observation active

## Trigger

The LifeOS Dashboard exposed stale and duplicated operational state. `memory/05_OPEN_LOOPS.md` still listed Automation Command Center Phase 1 as a priority open loop even though Engineering had completed it and recorded the closure locally.

This revealed a structural problem rather than a display problem: global files were carrying department work that should remain authoritative only in the owning department.

## Decision Direction

Use need-to-know operational routing instead of universal duplication.

- Department `open_loops.md` files are authoritative for department-owned unfinished work.
- Global or system open loops are reserved for genuinely shared architecture, cross-department dependencies, multi-owner work, system-wide risks, or work with no single owner.
- Specialist departments should not boot with unrelated department backlogs.
- Cross-department awareness should arrive through advisories, explicit dependencies, routed handoffs, or Main/Logistics coordination.
- The dashboard may aggregate all department state for executive visibility without becoming another source of truth.

Example: dashboard and desktop-automation implementation help Life OS broadly, but the work is Engineering-owned. Wellness does not need the Engineering backlog unless pacing, recovery stability, burnout, sleep, or another Wellness dependency is actually involved.

## Approved Data Contract

Rob approved the Department Inspection data contract on 2026-07-18.

Canonical contract:

- `apps/lifeos-dashboard/DEPARTMENT_INSPECTION_DATA_CONTRACT.md`

Approved foundations:

1. one normalized record envelope;
2. seven department scopes plus System;
3. nine normalized record types;
4. separate lifecycle state and priority;
5. explicit source authority;
6. conservative parsing with confidence and warnings;
7. read-only duplicate and stale-state findings;
8. department files remain authoritative;
9. system files contain only genuinely system-owned work;
10. the dashboard remains an aggregation and diagnostic layer, not a mirrored ledger.

The contract intentionally preserves source ambiguity rather than allowing the inspector to hide inconsistent GitHub structure behind polished classification.

## Implemented MVP

Implementation head before tracking updates:

- `58538624c1bb138d7f8e8be85ac6c6f96be5dddf`

The read-only MVP includes:

- a normalized repository read model in `lifeos_dashboard/department_inspection.py`;
- seven canonical department scopes plus System;
- conservative parsing for Markdown open-loop tables and bullets;
- notebook, status, session-handoff, system-handoff, boot-log, and optional department-log inspection;
- separate lifecycle-state and priority normalization;
- visible legacy warnings when fields mix state and urgency;
- Work, Knowledge, Operations, and Findings categories;
- source paths, raw source fragments, authority, confidence, dates, and warnings;
- derived `state_priority_mixed`, `possible_duplicate`, and `stale_mirror` findings;
- GET `/api/department-inspection`;
- a Department Inspection tab between Overview and Automation;
- filters for department, category, record type, state, priority, date range, cross-department status, authority, warning status, search, and sorting;
- reload after the ordinary dashboard refresh completes its guarded GitHub synchronization;
- parser and endpoint test coverage.

The inspector does not edit, close, merge, reorder, promote, demote, or otherwise mutate GitHub records.

## Local Validation

Rob confirmed on 2026-07-18 that the Department Inspection tab works in the local Windows dashboard after guarded synchronization and server restart.

This validates the essential runtime path:

1. the dashboard pulled the implementation from GitHub;
2. the restarted FastAPI process loaded the new parser and endpoint;
3. the Department Inspection tab rendered in the intended position;
4. the live repository inspection loaded rather than the unavailable fallback state;
5. the existing Overview and Automation surfaces remained operational enough for normal use.

## First Live Audit Baseline

Rob observed:

- 458 normalized records;
- 4 findings;
- 101 records with warnings;
- a useful separation between Work, Operations, Knowledge, and Findings;
- a very large but legitimate notebook inventory;
- one `state_priority_mixed` finding;
- three `possible_duplicate` findings across Engineering / Logistics, Logistics / System, and Business / Wellness;
- a parser defect that removed underscores from file names displayed inside normalized summaries.

The baseline showed that the inventory was broad enough, but the first presentation and warning policy were too noisy for fast inspection.

## First Evidence-Based Tuning

Implemented after the live baseline:

- preserve underscores in file names and identifiers;
- remove routine `Priority not explicitly provided` warnings from bullet work items;
- normalize those bullet priorities to `unknown` while retaining medium confidence;
- require summary similarity before reporting cross-department duplicates when System is not involved;
- keep System mirrors and same-department duplicates eligible for findings;
- contain long record lists inside scrollable workbenches rather than extending the entire page;
- enrich Finding details with related title, state, authority, and source path instead of normalized IDs alone;
- add tests for underscore preservation, bullet-warning reduction, and unrelated cross-department title matches.

After restart, Rob observed:

- 459 normalized records;
- 4 findings;
- 15 records with warnings.

The warning reduction confirmed that routine missing-priority chatter had been removed without shrinking the underlying inventory.

## Confirmed Findings

The four remaining findings were inspected individually.

1. **Engineering state / priority mixing** was a true schema defect. The priority Engineering item used `Priority` as a Status value.
2. **Chat HQ observation** was duplicated in Engineering and Logistics while a system-level Seven Chat HQs operating watch already existed.
3. **Legacy Virtual Assistant folder** appeared across Logistics, Business, and System records even though repository-path disposition and reference migration belong to Logistics.
4. **Registry reference placeholders** in Business and Wellness were not real work. They were speculative reminders to accept a reference only if Logistics later assigned one. Engineering contained the same speculative placeholder in its parking lot.

## First Inspector-Guided Source Cleanup

Rob authorized the targeted cleanup on 2026-07-18.

Implemented changes:

- Engineering's Open table now separates `Status` and `Priority` columns.
- The inspector runtime reads explicit priority columns and preserves High, Normal, Low, Critical, None, and Unknown values; Medium normalizes to Normal under the approved contract.
- The broad Engineering and Logistics Chat HQ observation rows were removed; the system Seven Chat HQs operating watch remains authoritative.
- Logistics is now the sole open-loop owner for the Legacy Virtual Assistant folder disposition.
- Business open and parking mirrors for the Legacy VA folder were removed.
- System Waiting On and Parking Lot mirrors for the Legacy VA folder were removed.
- Speculative registry-reference placeholders were removed from Engineering, Business, and Wellness open-loop files.
- The cleanup history remains Engineering-owned rather than being copied into the global Recently Closed list.
- Test coverage now verifies that explicit priority remains separate from lifecycle state.

## Post-Cleanup Verification

After guarded synchronization and dashboard restart, Rob observed:

- 414 normalized records;
- 0 findings;
- 13 records with warnings.

Compared with the tuned pre-cleanup baseline of 459 / 4 / 15:

- 45 mirrored, duplicated, or low-value normalized records disappeared;
- all four confirmed structural findings disappeared naturally from source cleanup;
- warning volume fell slightly again without broad detector weakening;
- the remaining 13 warnings became a bounded review queue rather than evidence that the cleanup failed.

This was the first end-to-end proof that the inspector could expose structural defects, guide source cleanup, and verify the result without becoming a write-enabled source of truth.

## Warning Audit and Final Clean Verification

Rob used the new Warning Status filter to inspect the bounded queue.

The queue contained:

- ten notebook-status warnings;
- two Logistics rows using the legacy `Parked` lifecycle value;
- one warning that cleared when an Engineering tracking note gained an explicit recognized status.

The notebook audit exposed a real parser defect. Connector experiment notes could place an exact `Status: SUCCESS` field under a later `## Result` section, beyond the parser's bounded top-of-document metadata scan. The runtime policy now:

- honors an exact `Status:` field anywhere in a notebook;
- maps observed success and watched-validation statuses to `Completed`;
- maps observed deferred statuses to `Waiting`;
- maps observed raw and open statuses to `Open`;
- maps blocked statuses to `Blocked`;
- retains conservative fallback warnings for statuses not supported by evidence;
- includes regression coverage for the late-status Google Drive experiment.

The two Logistics records were valid paused work encoded with the legacy `Parked` value. Logistics now uses explicit `Status | Priority | Item | Next Action | Notes` columns, with both records set to `Paused | Low`.

After guarded synchronization, Python restart where required, and browser refresh, Rob confirmed:

- 414 normalized records;
- 0 findings;
- 0 warnings.

This final zero was achieved through confirmed source corrections and evidence-backed parser behavior, not by suppressing ambiguity or weakening detection.

## Implemented Operational Package

The ownership and routing architecture is now durable in:

- `coordination/OPEN_LOOP_OWNERSHIP_AND_VISIBILITY_SOP.md`;
- `coordination/DEPARTMENT_FILE_OWNERSHIP_SOP.md`;
- `coordination/IDEA_INTAKE_AND_PROMOTION_SOP.md`;
- `memory/03_OPERATIONAL_RULES.md`;
- `memory/STARTUP_BOOT.md`;
- `memory/05_OPEN_LOOPS.md`;
- department-local handoffs, status files, and open-loop files.

Implemented rules include:

1. department versus system open-loop ownership;
2. promotion and demotion thresholds for system-level loops;
3. role-routed boot context so specialists do not load unrelated global work;
4. advisory and dependency routing for work that crosses department boundaries;
5. lifecycle rules for creation, update, pause, closure, and reconciliation;
6. dashboard aggregation as a read-only visibility layer rather than a mirrored ledger;
7. stale-state detection and source cleanup through explicit human review;
8. Trello-first raw idea intake and deliberate durable-write promotion;
9. canonical tag families and structured GitHub lifecycle vocabulary;
10. separation between abundant ideas, committed work, durable evidence, and shared operating rules.

## Remaining Sequence

1. Observe ordinary specialist boots for evidence that the universal-kernel plus role-routed model works in practice.
2. Close the ownership system wrapper when ordinary use confirms stable routing.
3. Confirm the inspector remains read-only and introduces no new source-of-truth duplication.
4. Apply the new idea-intake and promotion rules in live Trello and department workflows, refining only from observed friction before automation.

Do not weaken finding detection merely to preserve a zero count. Future warnings should remain visible when they truthfully represent ambiguous source material.

## Product Lesson

The dashboard paid for itself by exposing duplicate state, unnecessary universal context, inconsistent lifecycle vocabulary, parser blind spots, over-engineering, and work that should remain local.

The deeper governance lesson is that Life OS needs promotion rules as much as storage locations. Trello can absorb abundant ideas without making them commitments. GitHub should receive only ideas that have become owned work, durable evidence, decisions, rules, watches, or milestones.

Treat that diagnostic and governance value as a core capability, not an accidental side effect.
