# Department Ownership and Dashboard Inspection

Date: 2026-07-17
Updated: 2026-07-18
Department: Engineering HQ
Status: MVP locally validated / first live-audit tuning awaiting restart confirmation

## Trigger

The LifeOS Dashboard exposed stale and duplicated operational state. `memory/05_OPEN_LOOPS.md` still listed Automation Command Center Phase 1 as a priority open loop even though Engineering had completed it and recorded the closure locally.

This revealed a structural problem rather than a display problem: global files are carrying department work that should remain authoritative only in the owning department.

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
- filters for department, category, record type, state, priority, date range, cross-department status, authority, warnings, search, and sorting;
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

The baseline showed that the inventory is broad enough, but the first presentation and warning policy are too noisy for fast inspection.

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

This tuning remains read-only and does not alter the source Markdown.

## Required Operational Package

Using inspector evidence, formalize clean rules and procedures for:

1. department versus system open-loop ownership;
2. promotion and demotion thresholds for system-level loops;
3. role-routed boot context so specialists do not load unrelated global work;
4. advisory and dependency routing for work that crosses department boundaries;
5. lifecycle rules for creation, update, pause, closure, and reconciliation;
6. dashboard aggregation as a read-only visibility layer rather than a mirrored ledger;
7. stale-state detection and cleanup of existing duplicated global entries.

Likely durable output: an Open Loop Ownership and Visibility SOP plus targeted boot-routing updates and global-state reconciliation.

## Remaining Sequence

1. Pull and restart the dashboard to validate the first live-audit tuning.
2. Compare new warning and finding counts with the baseline.
3. Review the enriched Findings details and decide which records are genuinely duplicated or misplaced.
4. Correct further parser or filter behavior only where evidence warrants it.
5. Use the inspector to audit and clean duplicated, stale, or misplaced GitHub state.
6. Formalize the Open Loop Ownership and Visibility SOP and role-routed boot changes using evidence from the inspector.
7. Reconcile system and department files under the new rules.
8. Confirm the inspector remains read-only and introduces no new source-of-truth duplication.

## Product Lesson

The dashboard is already paying for itself by exposing duplicate state, unnecessary universal context, over-engineering, and work that should remain local. Treat that diagnostic value as a core capability, not an accidental side effect.
