# Department File Ownership and Drift Management SOP

Updated: 2026-07-15
Project: Life OS Coordination
Purpose: Define how departments maintain their own durable GitHub state while minimizing Rob's manual routing burden.

## Core Rule

Each department is responsible for maintaining the GitHub files and sections within its own domain.

The department that owns the working context should normally update the durable record directly rather than routing routine maintenance through Life Logistics HQ.

Short form:

> Departments maintain their own rooms. Main coordinates the building. Logistics maintains the hallways.

## Why This Rule Exists

The ideal architecture would automate cross-department synchronization, advisory consumption, and routine memory maintenance. The current platform does not provide a reliable low-friction way to automate seven department chats and their advisories.

Routing every routine change through Rob and then through Logistics creates unnecessary switching, delay, and cognitive load. Because each department chat already holds the most current working context for its domain, that department is usually best positioned to detect and correct drift.

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

## Main Assistant Responsibilities

Main Assistant owns:

- cross-department coordination
- routing and synthesis
- shared policies and system-level decisions
- identifying when a local department change has broader consequences
- deciding when an advisory or coordinated update is warranted

Main should not become the routine editor of every department's internal files.

## Life Logistics Responsibilities

Life Logistics HQ owns shared operational infrastructure and cross-system hygiene, including:

- global boot and routing integrity
- shared operating procedures
- advisory index hygiene
- cross-project audits
- shared open-loop and architecture review
- detecting conflicts between departments
- system-wide housekeeping when requested

Logistics is not the default implementation bottleneck for routine department file maintenance.

## Advisory Threshold

Do not create an advisory for routine maintenance confined to one department.

Use an advisory when:

- another department must act or decide
- a change affects multiple departments
- a shared policy or architecture boundary changes
- a dependency, conflict, risk, or handoff must be durably communicated
- Rob asks for formal cross-department routing

Routine local edits should remain local.

## Shared and Cross-Cutting Files

A department should not casually edit shared or another department's canonical files.

When a change touches:

- `memory/STARTUP_BOOT.md`
- global operating rules or SOPs
- shared coordination files
- another department's project subtree
- the Advisory Index
- system architecture files

route through Main Assistant, Life Logistics, the owning department, or an explicit coordinated action as appropriate.

## Rob's Role

Rob remains the final authority and may direct any department to update, coordinate, or make an exception.

Rob does not need to manually relay every routine internal change. As department chats are used, booted, and synchronized, their context windows will naturally surface drift and support direct maintenance of their own canonical files.

## Operating Principle

> Decentralize maintenance. Preserve ownership. Escalate only across boundaries.
