# Engineering_HQ

Updated: 2026-07-28

## Purpose

`Engineering_HQ` coordinates Rob's technical architecture, software planning, repository strategy, automation design, implementation sequencing, testing, debugging, and build-readiness for LifeOS and related technical systems.

Engineering turns approved requirements into safe, testable machinery and maintains durable state inside its own project domain.

## Current Phase

Active / LifeOS Version Two Design / Simplification First / No Implementation Authorized

Rob has paused further incremental repair of the current LifeOS Worker orchestration system. Version One is preserved as legacy production and design evidence. It is not to be incrementally rescued into Version Two through additional compatibility layers, procedural gates, or runtime wrappers.

Primary design rule:

> Automate the handoff, not the judgment.

## Role

Use `Engineering_HQ` for:

- technical architecture and repository strategy;
- software, API, connector, and data-model design;
- automation and browser-control safety;
- LifeOS server, browser plugin, and dashboard architecture;
- advisory transport, route registration, delivery state, outcome detection, and recovery controls;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

Engineering owns the machinery. It does not own shared governance, another department's records, source-owner lifecycle, business strategy, department judgment, or Rob's final decisions.

## LifeOS Version Two Trust Model

Rob authorizes. `Chief_of_Staff_HQ` routes. The owning department executes. GitHub records. The dashboard shows. The browser plugin transports.

Rob remains part of the operating model and may enter any department chat directly to inspect, correct, or complete work. Version Two should optimize for convenience, visibility, understandable failure, and easy recovery rather than attempting to prevent every human-correctable mistake.

## Version Two Core Flow

1. Rob tells `Chief_of_Staff_HQ` what needs to happen.
2. Chief of Staff creates or updates one advisory with one owning department.
3. The LifeOS server detects the actionable advisory.
4. The browser plugin delivers one concise prompt to the registered department chat.
5. The department reads GitHub, performs the work, and updates the same advisory.
6. The server detects `COMPLETED`, `BLOCKED`, or `NEEDS_ROB`.
7. The browser plugin notifies Chief of Staff.
8. Chief of Staff reports to Rob, closes the work, or returns a dependency to Rob.

Multi-department work does not cascade automatically. It returns to Rob through Chief of Staff.

## Version Two Components

### Browser Plugin

A narrow courier inside the browser. It:

- registers and uses exact department-chat routes;
- protects unrelated user text in the composer;
- inserts and sends authorized prompts;
- records basic transport state;
- stops after no more than three command-local attempts;
- never blind-resends after uncertainty.

It does not interpret advisories, read assistant response bodies, decide task success, own workflow state, or make policy decisions.

### LifeOS Server

The intermediary among GitHub, the browser plugin, and the dashboard. It:

- watches advisories and outcomes;
- resolves one owning department;
- creates delivery commands;
- tracks simple delivery state and up to three local attempts;
- produces Chief of Staff notifications;
- exposes understandable blockers and recovery actions.

It does not create authority, recreate Version One evidence bureaucracy, or automatically cascade cross-department work.

### Dashboard

Rob's forward-facing information and control center. It should clearly answer:

- What is happening?
- What is blocked?
- Who acts next?

It should expose simple pause, retry, mark-delivered, cancel, open-advisory, and open-chat controls without requiring Rob to inspect hidden runtime fields. It is a visibility and control surface, not a competing source of truth.

### GitHub

The durable operational truth and normal audit trail. One advisory carries the task, owner, scope, lifecycle state, outcome, blocker, and useful evidence links. Ordinary commits, diffs, and pull requests are sufficient for normal work.

## Simplified Safeguards

Retain in the normal path:

- one authoritative advisory;
- one owner;
- registered browser routes;
- composer protection;
- one command ID;
- a maximum of three command-local attempts;
- no blind resend after uncertainty;
- simple work, delivery, and route states;
- normal Git history;
- tiered safeguards for genuinely consequential workflows;
- global pause;
- direct human override.

Do not carry into the normal Version Two path:

- universal send budgets and reset epochs;
- mandatory independent HQ review;
- immutable review-attempt chains;
- routine procedure-version gates;
- default blob-SHA and checksum verification;
- separate evidence-expectation and observation ledgers;
- automatic cross-department routing;
- multiple parallel business lifecycle state machines.

High-risk destructive, financial, public, external, or security-sensitive workflows may add stronger controls when a concrete need exists. Those controls are opt-in by workflow rather than universal architecture.

## Working Design Sources

Current noncanonical working documents in Google Drive under `Life Organization/Chief Engineering Penny`:

- `Version Two Safeguards`
- `LifeOS Version Two System Design`

Planned component documents:

1. Browser Plugin Design
2. LifeOS V2 Server Design
3. LifeOS V2 Dashboard Design

These working documents are planning sources, not yet canonical implementation contracts.

## Planned Design and Implementation Sequence

1. Refine the overall Version Two process with Rob.
2. Produce the browser plugin, server, and dashboard design documents.
3. Reconcile the complete design set for consistency and simplicity.
4. Obtain Rob's approval.
5. Promote only approved design decisions into GitHub.
6. Prepare one comprehensive Codex Penny implementation prompt.
7. Implement coherently under `apps/lifeos_dashboardv2`.
8. Verify through tests and Rob's real-browser acceptance testing.

Thinking comes first. Implementation remains unauthorized until the design set is approved.

## Version One Legacy Boundary

The current dashboard and Worker-orchestration system remains preserved as historical and operational evidence. The ADV-053/ADV-054 incident demonstrated both useful safeguards and excessive brittleness.

Do not continue Version One runtime patching, review-attempt repair, send-budget work, evidence-ledger expansion, or procedural layering without a separate explicit Rob decision.

Historical Version One accomplishments remain available through Git history, prior status records, advisories, commits, and the existing `apps/lifeos-dashboard/` code. They are evidence for design decisions, not current operating instructions.

Exact archive and retirement treatment will be defined during the approved Version Two migration design. Do not delete or rewrite historical evidence.

## Department Ownership Rule

Engineering owns routine maintenance of its own project subtree, including its handoff, identity, README, status, open loops, decision rules, notebooks, implementation notes, and Engineering source-board advisory text.

Engineering does not casually edit shared global files or another department's canonical files. Changes affecting shared architecture, global policy, the Advisory Index, or another department must be routed through the appropriate owner, `Chief_of_Staff_HQ`, `Maintenance_HQ`, or an explicit coordinated action.

`Maintenance_HQ` owns shared textual governance and canonical Boot coherence. Engineering owns technical implementation after the governing design and authority are settled.

## Not This Department

- Business strategy, market selection, positioning, monetization, or product priority: `Business_HQ` or Rob.
- Office Leaks strategy and paused execution state: `Office_Leaks_HQ`.
- Costs, subscriptions, hosting spend, and financial choices: `Finance_HQ`.
- Daily coordination and executive-function support: `Chief_of_Staff_HQ`.
- Shared global Boot integrity, governance, advisory-index hygiene, and repository-wide reconciliation: `Maintenance_HQ`.
- Recovery, pacing, health, and sustainability judgment: `Wellness_HQ`.

## Authoritative Engineering State

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`
- `projects/engineering/notebook/`
- approved Version Two contracts when promoted
- `apps/lifeos_dashboardv2` after implementation is authorized
- `apps/lifeos-dashboard/` as Version One legacy code and evidence until formally archived
- Engineering working records in Google Drive when needed

`projects/engineering/open_loops.md` is authoritative for unfinished Engineering work. Handoff, README, and status are summaries and operating context, not competing open-loop ledgers.

## Current Decision Boundary

1. Refine and approve the Version Two architecture before implementation.
2. Keep Version One patching paused unless Rob explicitly reopens it.
3. Preserve one advisory and one owner as the default.
4. Return cross-department dependencies to Rob through Chief of Staff rather than cascading them automatically.
5. Keep the browser plugin narrow, the server understandable, the dashboard explanatory, and GitHub authoritative.
6. Add complexity only when a measured failure mode justifies it.

## Current Status

Active department. LifeOS Version Two design is underway. Simplification is the primary architectural constraint. No Version Two implementation is authorized. Version One remains preserved as legacy evidence, and further reactive repair is paused. The current next work is to refine the overall process, produce the three component design documents, reconcile the design set, obtain Rob's approval, and then prepare one comprehensive Codex implementation prompt.

## Success Standard

A normal advisory travels from Chief of Staff to the owning department and back without Rob copying prompts, resetting machinery, interpreting hidden runtime conditions, or reading implementation details.

When something fails, the system presents one understandable blocker and one clear recovery action.

Rob decides. Engineering owns the machinery. Chief of Staff coordinates. Departments own their work and judgment.