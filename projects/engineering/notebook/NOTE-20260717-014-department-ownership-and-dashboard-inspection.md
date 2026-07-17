# Department Ownership and Dashboard Inspection

Date: 2026-07-17
Department: Engineering HQ
Status: High-priority next work package

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

## Required Operational Package

Before expanding the dashboard, formalize clean rules and procedures for:

1. department versus system open-loop ownership;
2. promotion and demotion thresholds for system-level loops;
3. role-routed boot context so specialists do not load unrelated global work;
4. advisory and dependency routing for work that crosses department boundaries;
5. lifecycle rules for creation, update, pause, closure, and reconciliation;
6. dashboard aggregation as a read-only visibility layer rather than a mirrored ledger;
7. stale-state detection and cleanup of existing duplicated global entries.

Likely durable output: an Open Loop Ownership and Visibility SOP plus targeted boot-routing updates and global-state reconciliation.

## Dashboard Requirement

Add a new tab between Overview and Automation for department-level inspection across all seven departments.

Working label: `Departments` or `Department Inspection`.

The tab should present separate categories for:

- department open loops;
- department notebooks;
- department logs and status records where useful;
- system-wide open loops as a clearly distinct category.

Filters and controls should include, where the source data supports them:

- department;
- status;
- priority;
- date or date range;
- newest or oldest order;
- notebook or record type;
- cross-department-only view;
- text search over titles and summaries.

The dashboard should show source paths and compact previews while preserving the department files as the only authoritative records.

## Implementation Sequence

1. Audit current global and department loop duplication.
2. Define and record ownership and routing rules.
3. Update boot behavior so specialist departments receive only relevant global context.
4. Reconcile stale global loops and handoff language.
5. Build the Department Inspection tab.
6. Validate filters against all seven departments and confirm no new source-of-truth duplication is introduced.

## Product Lesson

The dashboard is already paying for itself by exposing duplicate state, unnecessary universal context, over-engineering, and work that should remain local. Treat that diagnostic value as a core capability, not an accidental side effect.
