# Department Ownership and Dashboard Inspection

Date: 2026-07-17
Updated: 2026-07-18
Department: Engineering HQ
Status: Approved / implementation-ready

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

## Required Operational Package

Formalize clean rules and procedures for:

1. department versus system open-loop ownership;
2. promotion and demotion thresholds for system-level loops;
3. role-routed boot context so specialists do not load unrelated global work;
4. advisory and dependency routing for work that crosses department boundaries;
5. lifecycle rules for creation, update, pause, closure, and reconciliation;
6. dashboard aggregation as a read-only visibility layer rather than a mirrored ledger;
7. stale-state detection and cleanup of existing duplicated global entries.

Likely durable output: an Open Loop Ownership and Visibility SOP plus targeted boot-routing updates and global-state reconciliation.

## Dashboard Requirement

Add a new tab between Overview and Automation for department-level inspection across all seven departments plus System.

Working label: `Departments` or `Department Inspection`.

The tab should present four primary categories:

- Work;
- Knowledge;
- Operations;
- Findings.

Version 1 filters:

- department;
- category;
- record type;
- lifecycle state;
- priority;
- date or date range;
- cross-department status;
- source authority;
- warnings only;
- text search;
- newest, oldest, department, or priority sorting.

The dashboard should show source paths, compact previews, raw text when requested, confidence, and warnings while preserving the department files as the only authoritative records.

## Implementation Sequence

1. Implement the normalized record model and conservative parsers against the approved contract.
2. Build a read-only Department Inspection tab between Overview and Automation.
3. Load all seven department scopes plus System from canonical source families.
4. Expose Work, Knowledge, Operations, and Findings views with approved filters.
5. Validate classifications and anomaly findings against existing GitHub inconsistencies.
6. Use the inspector to audit and clean duplicated or misplaced GitHub state.
7. Formalize the Open Loop Ownership and Visibility SOP and role-routed boot changes using evidence from the inspector.
8. Confirm no new source-of-truth duplication is introduced.

## Product Lesson

The dashboard is already paying for itself by exposing duplicate state, unnecessary universal context, over-engineering, and work that should remain local. Treat that diagnostic value as a core capability, not an accidental side effect.
