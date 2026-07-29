# Engineering_HQ Session Handoff

Updated: 2026-07-28
Project: Engineering_HQ
Purpose: Fresh-room handoff after Rob paused further repair of the current Worker orchestration system and redirected Engineering toward a deliberately simpler LifeOS Version Two.

## Metadata

- Project Owner: Rob
- Primary Chat: `Engineering_HQ`
- Current Phase: Active / LifeOS V2 Design / Simplification First / No Implementation Authorized
- Primary Systems: Google Drive working design documents, GitHub durable architecture and history, future `apps/lifeos_dashboardv2`, browser plugin, local LifeOS server, and dashboard
- Sensitivity Level: Moderate

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and the universal kernel.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Perform a separate read-only Sync before any GitHub implementation write.
7. Do not resume V1 patching, Worker-runtime repair, advisory review machinery, or transport debugging without a new explicit Rob decision.

## Current Decision

Rob concluded that the current LifeOS Worker and review architecture has become too brittle and over-engineered for a personal operating system. The accumulated send budgets, reset epochs, immutable review attempts, procedure gates, evidence ledgers, parallel lifecycle states, and layered runtime wrappers created excessive operator burden and too many failure points.

The current system is to be retired as legacy and preserved in GitHub history. It is not to be incrementally rescued into Version Two.

LifeOS Version Two will be designed with simplification as the primary objective.

## Version Two Trust Model

Rob authorizes. Chief of Staff routes. The owning department executes. GitHub records. The dashboard shows. The browser plugin transports.

Rob remains part of the operating model and may enter any department chat directly to inspect, correct, or complete work. The system should optimize for convenience, visibility, and easy recovery rather than attempting to prevent every possible human-correctable error.

Primary design rule:

> Automate the handoff, not the judgment.

## Version Two Core Flow

1. Rob tells Chief of Staff what needs to happen.
2. Chief of Staff creates or updates one advisory with one owning department.
3. The server detects the actionable advisory.
4. The browser plugin delivers one concise prompt to the registered department chat.
5. The department reads GitHub, performs the work, and updates the same advisory.
6. The server detects `COMPLETED`, `BLOCKED`, or `NEEDS_ROB`.
7. The browser plugin notifies Chief of Staff.
8. Chief of Staff reports to Rob, closes the work, or returns a dependency to Rob.

Multi-department work does not cascade automatically. It returns to Rob through Chief of Staff.

## Version Two Components

### Browser plugin

A narrow courier inside the browser. It registers routes, protects user text, inserts prompts, sends when authorized, reports basic transport state, and stops after three command-local attempts. It does not interpret advisories, read assistant response bodies, decide task success, or own workflow state.

### LifeOS server

The intermediary between GitHub, the browser plugin, and the dashboard. It watches advisories, creates delivery commands, tracks delivery state and up to three local attempts, watches advisory outcomes, and produces Chief of Staff notifications.

### Dashboard

Rob's forward-facing information and control center. It should clearly answer:

- What is happening?
- What is blocked?
- Who acts next?

It should expose simple pause, retry, mark-delivered, cancel, open-advisory, and open-chat controls without requiring Rob to inspect hidden runtime fields.

### GitHub

The durable operational truth and normal audit trail. One advisory carries the task, owner, scope, lifecycle state, outcome, blocker, and useful evidence links. Ordinary Git commits, diffs, and pull requests are sufficient for normal work.

## Simplified Safeguards

Retain:

- one authoritative advisory;
- one owner;
- registered browser routes;
- composer protection;
- one command ID;
- a maximum of three command-local attempts;
- no blind resend after uncertainty;
- simple work, delivery, and route states;
- normal Git history;
- tiered safeguards for genuinely consequential work;
- global pause;
- direct human override.

Remove from the normal path:

- universal send budgets and reset epochs;
- mandatory independent HQ review;
- immutable review-attempt chains;
- routine procedure-version gates;
- default blob SHA and checksum verification;
- separate evidence expectation and observation ledgers;
- automatic cross-department routing;
- multiple parallel business lifecycle state machines.

## Working Design Documents

The current noncanonical working documents are in Google Drive under `Life Organization/Chief Engineering Penny`:

- `Version Two Safeguards`
- `LifeOS Version Two System Design`

These documents are the current planning sources. They are not yet canonical GitHub implementation contracts.

Next design documents to produce:

1. Browser Plugin Design
2. LifeOS V2 Server Design
3. LifeOS V2 Dashboard Design

After Rob reviews and approves the complete design set, promote the approved documents into GitHub and prepare one comprehensive deliverables prompt for Codex Penny.

## Implementation Direction

- New implementation location: `apps/lifeos_dashboardv2`
- Current V1 dashboard and Worker orchestration code: preserve as archived legacy history
- Codex Penny: repository-wide implementation, tests, refactors, and reviewable delivery
- Engineering HQ: architecture, boundaries, acceptance criteria, protected behavior, and implementation prompt
- Rob: final architecture authority and real-browser acceptance testing

The intention is to do the thinking first and implementation second. Codex should build the approved system coherently in one bounded implementation effort rather than receive a chain of reactive patches.

## Current V1 Incident Context

The Maintenance Worker run `RUN-ADV-20260726-053-R1` and related ADV-053/ADV-054 repair history demonstrated both useful safeguards and the brittleness of the present architecture. The latest apparent runtime failure was actually stale Maintenance chat context after the wake succeeded. Do not continue adding V1 runtime patches from this handoff.

Preserve the incident and its Git history as design evidence. Any remaining V1 advisory lifecycle cleanup belongs to a separate explicit Rob decision and must not distract from V2 design.

## Next Valid Actions

1. Boot and Sync in the fresh Engineering HQ chat.
2. Review the two Drive working documents.
3. Discuss and refine the complete V2 process until Rob is satisfied.
4. Produce the browser plugin, server, and dashboard design documents.
5. Reconcile the design set for consistency and simplicity.
6. Promote only approved design decisions into GitHub.
7. Prepare one comprehensive Codex Penny implementation prompt for `apps/lifeos_dashboardv2`.

## Success Standard

A normal advisory travels from Chief of Staff to the owning department and back without Rob copying prompts, resetting machinery, interpreting hidden runtime conditions, or reading implementation details.

When something fails, the system presents one understandable blocker and one clear recovery action.

## Boundary

Rob decides. Engineering owns the machinery and technical architecture. Chief of Staff coordinates. Departments own their work and judgment. Version Two must reduce Rob's operational burden rather than merely pass more tests.
