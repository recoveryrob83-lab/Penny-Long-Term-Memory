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

No Business, Finance, Wellness, or Office Leaks Worker title or ID is canonical. `Business_HQ`, `Finance_HQ`, and `Wellness_HQ` do not request Workers at present. Office Leaks remains paused.

`Maintenance_HQ` owns the shared textual standard. `Engineering_HQ` owns implementation of titles and stable IDs in Engineering-controlled code, browser routing, runtime configuration, route mappings, tests, and bounded active-state migrations.

Display-name changes do not authorize filesystem-path renames, Worker-ID changes, destination-key changes, historical-row rewrites, immutable-evidence rewrites, or checksum changes.

## Canonical Worker Model

A LifeOS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, procedures, authority, holds, verification, retirement, and domain judgment.
- GitHub holds canonical profiles, procedures, decisions, and immutable result and review evidence.
- SQLite runtime state is the sole operational ledger for registry, route, dispatch, result, review, pause, send-budget, and deployment state.
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

## Lean Worker Adoption Rule

The production Worker portfolio is intentionally limited to `Engineering_Worker` and `Maintenance_Worker`.

A department does not receive a Worker because a technical path exists or because another department has one. New adoption requires:

- a recurring, standardized workload;
- a measurable bottleneck or reliability problem;
- an explicit request from the owning department;
- a narrow task class and authority boundary;
- shared-contract and governance review;
- one canonical profile, stable ID, exact title, result path, review procedure, route, canary, and separate activation decision.

Current owner decisions:

- `Business_HQ`: continue bounded one-off research assignments; reconsider only a narrow Market Evidence Worker after standardized research creates a measurable bottleneck.
- `Finance_HQ`: no Worker requested at present.
- `Wellness_HQ`: no Worker requested at present.
- `Office_Leaks_HQ`: business and Worker rollout paused.

These decisions close the initial expansion phase. They do not prohibit later reconsideration after the trigger exists.

## Activation and Readiness Boundary

The activation-readiness service recomputes technical prerequisites from canonical profile and procedure files plus read-only SQLite state.

- Findings use `PASS`, `HOLD`, and `NOT_APPLICABLE`.
- Overall technical state is `READY_FOR_AUTHORITY_REVIEW` or `HOLD`.
- Every report returns `activation_authorized: false`.
- Technical readiness does not create a profile, route, registry row, schedule, permission, assignment, or activation authority.
- Owning-department authority, Maintenance governance review, and Rob approval remain separate gates wherever required.
- Explicit human activation is a separate authority event and does not turn the readiness report into an activation ledger.

## Guarded Registration and Routing

Worker Operations can register an approved canonical Worker profile and capture the exact active ChatGPT room without copying the private URL into GitHub.

Registration requires exact agreement among profile path, Worker ID, canonical title, owner, project, profile version, specialization, and role. It also requires automation paused, no running job, the shared lock free, and explicit operator confirmation.

A successful registration creates one route-less row and one `unknown` route hold. It creates no assignment, execution row, schedule, route, activation, or authority.

Route capture requires an unchanged expected revision, exactly one intended target, an exact title match, and a URL not owned by another Worker. A successful capture updates the existing row, increments the revision, and keeps the route held until the zero-authority canary succeeds.

Starting the dashboard alone authorizes none of these actions.

## Composer Safety

Current merged behavior:

- requires stable room hydration, exact route identity, one visible composer, and no active generation;
- reuses only the current run-linked draft;
- preserves unrelated, malformed, and unproven text;
- clears an older canonical LifeOS wrapper only when its `wrapper_id` and `run_id` are proven together in one submitted user turn;
- verifies the proven stale composer is empty before inserting a new prompt;
- proves a new correlated user turn and an empty composer before confirming a send;
- never blind-retries confirmed or uncertain submissions.

PR #21, `Clear proven stale Worker composer residue`, was squash-merged to `main` as `620ef84c57cbb87123bbca30e43faffda1e71032` after the branch was refreshed against current `main` and Rob reported the focused tests, affected regressions, and Ruff green. Rob then confirmed ordinary post-merge dashboard health. The separately authorized Maintenance repository audit should provide the next natural live observation of composer cleanup and full-chain behavior without replaying the completed canary.

## Completed Technical State

- Package D: registry, receiver, transport, verification, and bounded pilot mechanics.
- Package E: immutable result outbox, deterministic ingestion, repair, HQ review, Rob validation, consumption, and duplicate suppression.
- Package F Wave 0A: canonical naming, exact URL routing, guarded route capture, zero-authority canary, and browser recovery.
- Package F Wave 0B: owning-HQ destination resolution, persisted shared safety pause, global send budget, and read-only activation readiness.
- PR #19: approved Maintenance profile, result procedure, HQ review procedure, review-path bridge, and tests.
- PR #20: guarded Worker registration and canary targeting for the sole routed Worker awaiting verification.
- PR #21: evidence-backed stale composer-residue cleanup with unrelated-text preservation and no prior-send retry.
- PR #21 deployment follow-through: current `main` pulled, dashboard restarted, and ordinary health confirmed by Rob.
- Maintenance Worker registration, exact route revision 1, successful canary, route availability, and active deployment are user-reported complete.
- Initial Worker expansion review: closed with Engineering and Maintenance active, and Business, Finance, and Wellness declining rollout for now.

Key recent merge commits:

- PR #15: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`
- PR #16: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`
- PR #17: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`
- PR #18: `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`
- PR #19: `28a7a4fc40317d043dbe9983747475f85d37742a`
- PR #20: `e91783dd9705df4a090eae2b4414adead6dafcf4`
- PR #21: `620ef84c57cbb87123bbca30e43faffda1e71032`

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
- Deployment state: active and live
- Assigned work: none

### Deferred Department Workers

- Business, Finance, and Wellness: no current Worker request.
- No title, ID, profile, room, registry row, route, canary, activation, schedule, or assignment is authorized.
- Reconsideration belongs to the owning department after a recurring standardized bottleneck is demonstrated.

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

Maintenance-owned Worker artifacts remain owned by `Maintenance_HQ`; Engineering owns only the routing and runtime machinery around them. Business, Finance, and Wellness retain authority over any future Worker purpose and adoption decision.

## Current Decision Boundary

1. Define the Maintenance repository-audit assignment as the next full-system Worker test.
2. Establish exact scope, authoritative sources, allowed writes, exclusions, authorization source, immutable result path, completion condition, and `IMMEDIATE_HQ` review before dispatch.
3. Use the authorized audit to observe composer cleanup, dispatch evidence, return-to-source behavior, result creation, ingestion, HQ review, and Rob validation where required.
4. Keep the Worker portfolio lean until an owning department demonstrates a recurring standardized bottleneck and explicitly requests evaluation.
5. Keep Office Leaks paused.

The completed rollout and healthy deployment do not authorize the audit's execution wrapper, task record, result path, or broad cross-department writes by themselves.

Future Engineering work must come from `projects/engineering/open_loops.md`, a demonstrated defect with bounded repair authority, or a new explicit Rob instruction.

## Browser and Automation Boundary

- Operate only against exact canonical ChatGPT URLs.
- Use the registered exact Worker URL as the authoritative locator.
- Require stable history hydration, exact room identity, a safe composer state, and no active generation.
- Preserve unrelated, malformed, and unproven composer text.
- Clear only evidence-backed stale canonical LifeOS wrapper residue.
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

Active department. Packages D and E are closed. Package F Waves 0A and 0B are complete. The initial Worker expansion phase is closed with a lean portfolio of `Engineering_Worker` and `Maintenance_Worker`. The Maintenance Worker is active and live with no assignment. Business, Finance, and Wellness do not request Workers at present. PR #21 is merged and ordinary post-merge dashboard health is confirmed. Office Leaks is paused. The separately bounded Maintenance repository audit is the selected next full-system test and requires exact assignment authority before dispatch.