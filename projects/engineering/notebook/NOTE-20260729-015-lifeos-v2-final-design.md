# NOTE-20260729-015: LifeOS Version Two Final Design

- Date: 2026-07-29
- Owner: Engineering_HQ
- Record Type: Approved architecture / implementation contract
- Lifecycle State: Active
- Priority: High
- Authority: Rob-approved promotion from Engineering working design
- Implementation Target: `apps/lifeos_dashboardv2`

## Decision

LifeOS Version Two replaces the brittle Version One orchestration path with a simpler human-supervised courier architecture.

Primary rule:

> Automate the handoff, not the judgment.

Trust model:

> Rob authorizes. Chief of Staff issues the advisory. The target department or Worker executes. GitHub records. The dashboard shows. The browser extension transports.

Version One remains preserved as legacy evidence. This record does not authorize further V1 repair or compatibility layering.

## Core Flow

1. Rob authorizes work through `Chief_of_Staff_HQ`.
2. Chief of Staff creates or revises one authoritative advisory with one target.
3. The local LifeOS server reads the canonical Advisory Index and detects actionable revisions.
4. The server resolves the registered browser route and creates exactly one delivery command.
5. The browser extension protects existing composer text, inserts the exact wake, sends once, and reports transport state.
6. The target department or Worker reads GitHub, performs only the authorized work, and updates the same advisory.
7. The server detects `COMPLETED`, `BLOCKED`, or `NEEDS_ROB` and surfaces the outcome to Chief of Staff.
8. Cross-department dependencies return through Chief of Staff and Rob. They do not cascade automatically.

## Advisory Contract

Required fields:

- `advisory_id`
- `revision`
- `source_department`
- `target_department`
- `task_summary`
- `scope`
- `state`
- `outcome`
- `blocker`
- `updated_at`

V2 advisory states:

- `OPEN`
- `IN_PROGRESS`
- `BLOCKED`
- `NEEDS_ROB`
- `COMPLETED`
- `CLOSED`

Command identity is advisory ID plus revision, for example `ADV-055-r3`.

Rob and Chief of Staff determine whether a material change is a new revision or a new advisory. Reassign the same advisory only when the original work genuinely changes target. Create a new advisory for a distinct dependency, deliverable, or decision.

## Server Boundary

The local server:

- watches configured GitHub advisory sources;
- detects material revision, state, and outcome changes;
- resolves registered routes;
- creates one command per advisory revision;
- tracks transport state and command-local attempts;
- exposes APIs to the dashboard and extension;
- persists only the local transport state needed for safe restart;
- supports a single global pause state;
- resumes from current GitHub truth rather than replaying stale work.

The server does not:

- create task authority;
- interpret department judgment;
- maintain a competing advisory database;
- automatically cascade dependencies;
- infer completion from assistant prose;
- recreate V1 evidence bureaucracy.

Initial persistence is local JSON. SQLite may replace it only after demonstrated need.

## Browser Extension Boundary

Route registration:

1. Select an HQ or Worker route.
2. Open the intended ChatGPT conversation.
3. Register the current tab.
4. The extension reads the current URL.
5. A local confirmation displays the route and URL.

The extension:

- receives an exact command from the local server;
- verifies route and composer readiness;
- protects pre-existing composer text;
- inserts and sends the exact wake once;
- checks whether the expected user message appeared;
- reports `DELIVERED`, `FAILED`, or `UNCERTAIN`;
- stops after no more than three clearly pre-send attempts;
- respects global pause and a local emergency stop.

The extension must not read assistant response bodies, interpret advisories, determine task success, infer route identity from chat titles, route dependencies, or store durable advisory truth.

## Retry and Uncertainty

- Maximum three command-local attempts.
- Retry only clearly pre-send failures.
- If the expected user message appears, mark `DELIVERED`.
- If it is clearly absent and Send never occurred, a retry may occur.
- If the outcome is indeterminate, mark `UNCERTAIN` and stop.
- Never automatically replay an uncertain send.

## Pause and Resume

Global pause:

- stops new dispatches;
- does not rewrite advisory state;
- preserves confirmed delivered commands;
- ignores stale commands during pause;
- resumes from current GitHub truth;
- has no replay queue.

## Dashboard Boundary

The dashboard has three top-level sections:

1. Overview
2. Department Inspector
3. Automation

The dashboard is a read model, diagnostic surface, and bounded control surface. It is never a competing source of truth.

Approved controls:

- pause or resume;
- retry a clearly pre-send failure;
- cancel a pending delivery;
- open the advisory;
- open the target chat;
- change or re-register a route;
- refresh views.

Normal controls must not mark work complete, mark an advisory complete, infer success, reset advisory state, or replay uncertain sends.

## Implementation Slices

### Slice One: Server and Contracts

Build schemas, configuration, GitHub advisory reader, revision detection, route registry, command creation, persistence, pause behavior, APIs, logs, and tests.

Stop after the Slice One acceptance gate.

### Slice Two: Dashboard

Build the Automation surface first, then Department Inspector, then Overview connectors and presentation. Overview and Inspector remain read-only.

Stop after the Slice Two acceptance gate.

### Slice Three: Browser Extension

Build route registration, command retrieval, composer protection, send verification, delivery telemetry, pause behavior, and restart-safe uncertainty handling.

Stop after the Slice Three acceptance gate and real-browser testing.

## Internal Module Boundary

Recommended shape:

```text
apps/lifeos_dashboardv2/
  contracts/
  server/
  connectors/
  dashboard/
    overview/
    department_inspector/
    automation/
  extension/
  config/
  tests/
```

Overview consumes connector adapters. Automation consumes server APIs. Department Inspector consumes configured GitHub read models. The exact module names may change if a simpler coherent structure is found, but these boundaries must remain.

## Non-Goals

- no V1 rescue;
- no all-three-slices implementation in one mission;
- no automatic cross-department cascade;
- no response-body scraping;
- no generalized workflow engine;
- no multi-user SaaS architecture;
- no microservices or Kubernetes;
- no automatic record merging;
- no dashboard-owned work state;
- no speculative safeguards without observed need.

## Completion and Review Condition

This architecture remains active until Rob approves a revision or implementation evidence demonstrates a concrete conflict. Each production slice requires a separate Engineering review and Rob resume decision before the next slice begins.
