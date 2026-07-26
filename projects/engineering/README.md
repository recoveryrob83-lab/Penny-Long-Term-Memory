# Engineering_HQ

Updated: 2026-07-26

## Purpose

`Engineering_HQ` coordinates Rob's technical architecture, software planning, repository strategy, automation design, implementation sequencing, testing, debugging, and build-readiness for LifeOS and related technical systems.

Engineering turns approved requirements into safe, testable machinery and maintains durable state inside its own project domain.

## Role

Use `Engineering_HQ` for:

- technical architecture and repository strategy;
- software, API, connector, and data-model design;
- automation and desktop-control safety;
- LifeOS Dashboard and Worker Operations architecture;
- prompt systems and command interfaces;
- Worker routing, transport, logging, duplicate suppression, result ingestion, verification, and reliability;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

Engineering owns the machinery. It does not own shared Worker governance, department-specific Worker authority, another department's records, source-owner lifecycle, business strategy, or domain judgment.

## Canonical Naming Boundary

`memory/HQ_NAMING_STANDARD.md` is the canonical naming source.

Current canonical Worker titles and IDs are:

- `Engineering_Worker` / `engineering_worker`
- `Maintenance_Worker` / `maintenance_worker`

No Business Worker title or ID is canonical yet. `Business_HQ` is only the likely next owner after Rob's shift toward an AI systems business for solo developers and small teams.

`Maintenance_HQ` owns the shared textual standard. `Engineering_HQ` owns implementation of titles and stable IDs in Engineering-controlled code, browser routing, runtime configuration, route mappings, tests, and bounded active-state migrations.

Display-name changes do not authorize filesystem-path renames, Worker-ID changes, destination-key changes, historical-row rewrites, immutable-evidence rewrites, or checksum changes.

## Canonical Worker Model

A LifeOS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, procedures, authority, holds, verification, retirement, and domain judgment.
- GitHub holds canonical profiles, procedures, decisions, and immutable result and review evidence.
- SQLite runtime state is the sole operational ledger for registry, route, dispatch, result, review, pause, and send-budget state.
- Each Worker has one stable ID and one authoritative registry row.
- Browser dispatch uses the registered exact private conversation URL and fails closed if it is missing or invalid.
- Route changes increment the revision and remain held until the unchanged route passes a zero-authority canary.
- The browser courier proves one correlated submission, returns immediately, and never waits for completion.
- The Worker performs only bounded, already-authorized work.
- A deterministic ingester validates immutable result evidence and updates the existing runtime row.
- Department HQ reviews authority compliance, evidence, and the actual work where possible.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Source owners retain lifecycle and closure authority.
- The Worker courier does not wake `Chief_of_Staff_HQ` under the current contract.

Python, browser automation, SQLite, and the dashboard provide machinery and visibility. They are not the Worker and do not replace Department HQ judgment.

## Activation and Readiness Boundary

The activation-readiness service recomputes technical prerequisites from canonical profile and procedure files plus read-only SQLite state.

- Findings use `PASS`, `HOLD`, and `NOT_APPLICABLE`.
- Overall technical state is `READY_FOR_AUTHORITY_REVIEW` or `HOLD`.
- Every report returns `activation_authorized: false`.
- Technical readiness does not create a profile, route, registry row, schedule, permission, assignment, or activation authority.
- Owning-department authority, Maintenance governance review, and Rob approval remain separate gates wherever required.

## Guarded Registration and Routing

Worker Operations can register an approved canonical Worker profile and capture the exact active ChatGPT room without copying the private URL into GitHub.

Registration requires exact agreement among profile path, Worker ID, canonical title, owner, project, profile version, specialization, and role. It also requires automation paused, no running job, the shared lock free, and explicit operator confirmation.

A successful registration creates one route-less row and one `unknown` route hold. It creates no assignment, execution row, schedule, route, activation, or authority.

Route capture requires an unchanged expected revision, exactly one intended target, an exact title match, and a URL not owned by another Worker. A successful capture updates the existing row, increments the revision, and keeps the route held until the zero-authority canary succeeds.

Starting the dashboard alone authorizes none of these actions.

## Composer Safety

Current merged behavior:

- requires stable room hydration, exact route identity, one visible composer, and no active generation;
- reuses only the exact current run-linked draft;
- preserves unrelated text;
- proves a new correlated user turn and an empty composer before confirming a send;
- never blind-retries confirmed or uncertain submissions.

Draft PR #21 adds evidence-backed stale-residue cleanup. After merge, an older canonical LifeOS wrapper may be cleared only when its `wrapper_id` and `run_id` already occur together in one submitted user turn. Malformed, unrelated, or unproven text remains untouched.

## Completed Technical State

- Package D: registry, receiver, transport, verification, and bounded pilot mechanics.
- Package E: immutable result outbox, deterministic ingestion, repair, HQ review, Rob validation, consumption, and duplicate suppression.
- Package F Wave 0A: canonical naming, exact URL routing, guarded route capture, zero-authority canary, and browser recovery.
- Package F Wave 0B: owning-HQ destination resolution, persisted shared safety pause, global send budget, and read-only activation readiness.
- PR #19: approved Maintenance profile, result procedure, HQ review procedure, review-path bridge, and tests.
- PR #20: guarded Worker registration and canary targeting for the sole routed Worker awaiting verification.

Key recent merge commits:

- PR #15: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`
- PR #16: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`
- PR #17: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`
- PR #18: `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`
- PR #19: `28a7a4fc40317d043dbe9983747475f85d37742a`
- PR #20: `e91783dd9705df4a090eae2b4414adead6dafcf4`

## Current Worker State

### Engineering Worker

- ID: `engineering_worker`
- Title: `Engineering_Worker`
- Route revision: `1`
- Availability: `available`

### Maintenance Worker

- ID: `maintenance_worker`
- Title: `Maintenance_Worker`
- Profile and procedures: on `main`
- Registry, route revision 1, canary, return to Engineering, and availability `available`: user-reported complete
- Activation and first real assignment authority: absent

### Business Worker Candidate

- Likely owner: `Business_HQ`
- Strategic focus: AI systems services for solo developers and small teams
- Profile, procedures, stable ID, exact title, room, registry, route, canary, activation, schedule, and assignment: not defined or authorized

### Office Leaks

- Business and Worker rollout: paused by Rob
- Existing Office Leaks records remain owned by `Office_Leaks_HQ`

## Not This Department

- AI systems business strategy, market research, monetization, customer discovery, or Business Worker purpose: `Business_HQ`.
- Paused Office Leaks strategy and records: `Office_Leaks_HQ`.
- Cost approval and financial choices: `Finance_HQ`.
- Daily coordination and executive-function support: `Chief_of_Staff_HQ`.
- Shared global Boot integrity, canonical Worker governance, and repository-wide hygiene: `Maintenance_HQ`.
- Recovery, pacing, health, and sustainability judgment: `Wellness_HQ`.

## Department File Ownership

Engineering maintains its own project subtree during authorized maintenance and implementation work. Shared global files, another department's canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner or explicit coordinated authorization.

Maintenance-owned Worker artifacts remain owned by `Maintenance_HQ`; Engineering owns only the routing and runtime machinery around them. Business owns any future Business Worker purpose and authority.

## Current Decision Boundary

1. Review and merge PR #21 only under explicit merge authority.
2. Inspect Maintenance activation readiness before any real assignment.
3. Observe the next separately authorized dispatch for composer cleanup behavior.
4. Keep Office Leaks paused.
5. Wait for `Business_HQ` and Rob to define a Business Worker contract before Engineering creates machinery around it.

Business candidacy is not approval. Do not create a profile, title, ID, room, registry row, route, schedule, activation, or assignment by analogy with Maintenance.

Future Engineering work must come from `projects/engineering/open_loops.md`, a demonstrated defect with bounded repair authority, or a new explicit Rob instruction.

## Browser and Automation Boundary

- Operate only against exact canonical ChatGPT URLs.
- Use the registered exact Worker URL as the authoritative locator.
- Require stable history hydration, exact room identity, a safe composer state, and no active generation.
- Prove a new marker-bearing user turn and an empty composer before calling a send confirmed.
- Never blind-retry a confirmed or uncertain submission.
- Ingest existing immutable evidence before attempting another HQ wake.
- Use atomic one-shot claims to suppress repeat wakes.
- Fail closed on unrecognized post-submit states.
- Do not let automation decide HQ or Rob judgment.
- Do not let courier, dashboard, watcher, or evidence receipts close source work automatically.

## Security Rule

Never store secrets, credentials, tokens, API keys, private calendar URLs, private ChatGPT conversation URLs, financial account details, medical details, private user data, or sensitive implementation details in LifeOS GitHub memory or Worker result artifacts.

Use ignored local environment files or the appropriate secure source system for operational credentials and private runtime locators.

## Boot Files

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`

## Current Status

Active department. Packages D and E are closed. Package F Waves 0A and 0B are complete. Maintenance registration, route revision 1, and the zero-authority canary are user-reported complete; activation is not authorized. PR #21 is validated but unmerged. Office Leaks is paused. Business is the likely next Worker-owning department, pending an explicit Business-owned contract and Rob authorization.
