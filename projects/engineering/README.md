# Engineering_HQ

Updated: 2026-08-01

## Purpose

`Engineering_HQ` owns Rob's technical architecture, software planning, repository strategy, automation design, implementation sequencing, testing, debugging, runtime diagnostics, and build-readiness for LifeOS and related systems.

Engineering turns approved requirements into safe, understandable, testable machinery and maintains durable state inside its own project domain.

## Current Phase

Active / LifeOS V2 Operational Core / Bounded Reliability Refinement

LifeOS V2 is no longer only a design effort. The core outbound courier and canonical GitHub advisory source have been implemented and tested in production conditions.

Primary design rule remains:

> Automate the handoff, not the judgment.

## Role

Use `Engineering_HQ` for:

- technical architecture and repository strategy;
- software, API, connector, and data-model design;
- LifeOS server, browser extension, and dashboard implementation;
- advisory parsing, route registration, command reconciliation, and transport state;
- browser-control safety and composer protection;
- canonical GitHub snapshot ingestion and source-health reporting;
- tests, debugging, failure recovery, and technical evidence;
- Engineering-owned handoff, status, open-loop, notebook, and implementation maintenance.

Engineering owns the machinery. It does not own shared governance, another department's source records, advisory lifecycle authority, business strategy, department judgment, or Rob's final decisions.

## LifeOS V2 Trust Model

Rob authorizes. `Chief_of_Staff_HQ` routes. The owning department executes. GitHub records. The dashboard shows. The browser extension transports.

Rob remains part of the operating model and may inspect, correct, or complete work directly. V2 favors convenience, visibility, understandable failure, and easy recovery over universal procedural armor.

## Proven Outbound Courier

The production courier has demonstrated:

- multiple canonical server-registered routes;
- exact registered ChatGPT conversation URLs;
- one owned background courier tab that may be created and reused;
- refusal to navigate or overwrite when the composer is not provably empty;
- command discovery before route readiness;
- readiness-gated atomic `/begin`;
- production routes without test arm and test routes with test arm;
- hardened composer insertion and narrow send-control selection;
- bounded proof of a newly rendered exact user message;
- terminal `UNCERTAIN` after unresolved post-click transport;
- no blind retry after uncertainty;
- server-side `DELIVERED` acknowledgement after proof.

The first Maintenance route test preserved revision 1 as `UNCERTAIN`, delivered revision 2 successfully, received visible Maintenance acknowledgement, and closed under Rob's authority.

Transport proves delivery, not task authority, task completion, or source ownership.

## Canonical GitHub Advisory Source

Production defaults to `REMOTE_GITHUB` for:

- repository: `recoveryrob83-lab/Penny-Long-Term-Memory`
- branch: `main`

The source synchronizer:

1. resolves the branch to one immutable commit SHA;
2. fetches the Advisory Index at that SHA;
3. fetches every referenced open-advisory board at the same SHA;
4. reconciles only after the required snapshot is available;
5. caches unchanged verified snapshots;
6. exposes source mode, state, verified SHA, timestamps, and errors;
7. never mutates Rob's local working tree or silently falls back to local files.

`LOCAL_DEVELOPMENT` is explicit and test-oriented.

Fatal source-integrity failures remain fail-closed. Isolated advisory-envelope defects should be quarantined, visible, and non-dispatchable without blocking valid advisories.

## Durable Publication Boundary

The core remote synchronizer is durable on `main` at commit:

- `0eeccc46df6980c62e29795e7f40c78a1d61a108`

A later local repair successfully quarantines `ADV-20260726-053`, which lacks a V2 Courier Envelope, while accepting valid advisories. Current GitHub `main` still shows the earlier fatal whole-snapshot parse behavior.

Until the quarantine repair is committed, pushed, and read back, it is local implementation state rather than durable repository truth.

Do not rewrite the Maintenance-owned advisory merely to satisfy the parser.

## Runtime Components

### Browser Extension

The extension is a narrow courier. It:

- reads canonical routes from the server;
- owns at most one tracked background courier tab;
- protects composer text;
- navigates to exact routes;
- probes readiness;
- performs one bounded send effect;
- reports transport evidence.

It does not interpret advisory policy, read assistant response bodies, decide work success, or own advisory lifecycle.

### LifeOS Server

The server mediates among GitHub, the extension, persistence, and dashboard. It:

- obtains commit-pinned advisory snapshots;
- parses V2 Courier Envelopes;
- reconciles commands;
- exposes canonical routes;
- separates command discovery from dispatch authorization;
- atomically claims commands;
- records delivery state and source provenance;
- fails closed when source truth cannot be verified.

### Dashboard

The dashboard is Rob's visibility and bounded-control surface. It should clearly answer:

- What is happening?
- What is blocked?
- Who acts next?
- Is canonical GitHub source healthy?

It is not a competing source of truth.

### GitHub

GitHub is durable operational truth and normal audit history. Advisory source records remain owned by their source departments. Engineering owns code and technical evidence, not advisory lifecycle.

## Local Resource Constraint

Rob's PC cannot comfortably keep multiple active ChatGPT windows open during ordinary work.

The courier tab may be closed when automation is idle. Nighttime automation may create or reuse one owned background tab. Engineering must avoid tab sprawl and must never navigate away from a composer containing text.

## Remaining Reliability Work

Current Engineering work includes:

- publish and verify the advisory-quarantine repair;
- display command records newest first without changing dispatch selection;
- retain active and uncertain evidence prominently while bounding old terminal history;
- settle and test courier-tab reuse versus post-delivery closure around Rob's resource limit;
- deduplicate or rate-limit repeated identical readiness telemetry;
- continue return-path and nighttime-automation work only from explicit scope and evidence.

## Version One Boundary

The previous dashboard and Worker-orchestration system remains preserved as legacy evidence under `apps/lifeos-dashboard/` and Git history.

Do not reintroduce universal send budgets, reset epochs, mandatory review chains, parallel evidence ledgers, or automatic cross-department cascades into the normal V2 path without a measured failure mode and explicit authorization.

## Department Ownership Rule

Engineering maintains its own project subtree and implementation code.

Engineering does not casually edit shared global files or another department's canonical files. Shared architecture, governance, advisory-index changes, or another department's records require the correct owner or explicit coordinated authority.

`Maintenance_HQ` owns shared textual governance and repository-wide coherence. Engineering owns technical implementation and technical enforcement.

## Authoritative Engineering State

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`
- `projects/engineering/notebook/`
- `apps/lifeos_dashboardv2`
- `apps/lifeos-dashboard/` as V1 legacy evidence

`projects/engineering/open_loops.md` is authoritative for unfinished Engineering work. Handoff, README, and status summarize current context rather than creating parallel backlogs.

## Success Standard

A valid advisory committed to canonical GitHub becomes discoverable without Rob manually pulling the repository, reaches exactly one registered department conversation, never overwrites user text, never blind-retries uncertainty, records understandable state, and presents one clear recovery action when something fails.

Rob decides. Engineering owns the machinery. Chief of Staff coordinates. Departments own their work and judgment. GitHub records durable truth.