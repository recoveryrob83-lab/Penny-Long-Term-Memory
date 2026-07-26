# Engineering_HQ Status

Updated: 2026-07-26

## Current Phase

Active / Core Worker Platform Complete / Lean Worker Portfolio / Maintenance Worker Active and Idle / PR #21 Merged / Local Deployment Health Pending / Office Leaks Paused / Repository Audit Assignment Pending Separate Authorization

## Department Scope

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering owns Worker machinery: exact routing, stable IDs, browser transport, route revisions, duplicate suppression, immutable result ingestion, report repair, runtime evidence, activation-prerequisite reporting, verification mechanics, tests, and reliability safeguards.

Engineering does not own shared governance, another department's Worker authority, source-owner lifecycle, business strategy, or domain judgment.

## Source Boundaries

- GitHub holds durable architecture, profiles, procedures, packages, decisions, advisories, and immutable Worker evidence.
- `projects/engineering/open_loops.md` is authoritative for unfinished Engineering work.
- SQLite Command Center state is the sole operational ledger for Worker registry, routes, dispatch, results, review, pause, send-budget, and deployment state.
- Private ChatGPT conversation URLs remain only in ignored local runtime state.
- Dashboard views provide visibility and transport, not independent truth or closure authority.
- Department HQs own their Worker purpose, authority, holds, verification, and retirement.
- `Maintenance_HQ` owns shared Worker governance.

Never store secrets, credentials, tokens, private account details, medical details, private user data, private ChatGPT conversation URLs, or sensitive implementation details in GitHub memory or Worker result artifacts.

## Completed Architecture

- Package D: CLOSED. Worker registry, routing, browser transport, receiver, duplicate suppression, verification, and bounded pilot foundations.
- Package E: CLOSED on 2026-07-23. Immutable result evidence, deterministic ingestion, repair, HQ review, Rob validation, consumption readiness, watcher reporting, and duplicate suppression.
- Package F Wave 0A: COMPLETE on 2026-07-23. Canonical naming, exact URL routing, route revisions, guarded route capture, zero-authority canary behavior, and browser recovery.
- Package F Wave 0B: COMPLETE on 2026-07-25. Owning-HQ destination resolution, persisted shared safety pause, global send budget, and read-only activation readiness.
- Initial cross-department Worker rollout: COMPLETE on 2026-07-26 with an intentionally lean production portfolio.

Key merges:

- PR #15: `83c309f651de0354982fcd6cbb68f9cf3251d6a3`
- PR #16: `3bf20ca231b3b5fbb1c315b24881e46939b3b508`
- PR #17: `e1d297f1a2517490b3fb2a37298689c6db25bfb0`
- PR #18: `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`
- PR #19: `28a7a4fc40317d043dbe9983747475f85d37742a`
- PR #20: `e91783dd9705df4a090eae2b4414adead6dafcf4`
- PR #21: `620ef84c57cbb87123bbca30e43faffda1e71032`

## Maintenance Worker

Lifecycle State: ACTIVE / LIVE / NO ASSIGNMENTS

Canonical files:

- `projects/life-logistics-hq/workers/maintenance_worker.md`
- `projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md`
- `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md`

Rob reports:

- one registered `maintenance_worker` row;
- exact title `Maintenance_Worker`;
- route revision `1`;
- successful zero-authority browser round trip;
- successful return to Engineering;
- route availability `available`;
- Worker deployment state active and live;
- no work assigned.

Activation is complete and is recorded separately from assignment authority. It does not create a task, schedule, unattended execution, broader connector permission, source-record repair authority, spending, or cross-department authority. The first real assignment still requires one separately exact bounded task, required source references and scopes, authorization source, immutable result path, and `IMMEDIATE_HQ` verification.

## Composer Residue Repair

Lifecycle State: MERGED TO `main` / LOCAL DEPLOYMENT HEALTH PENDING

During the Maintenance canary, ChatGPT restored the already-submitted prompt in the Worker composer after transport had confirmed the user turn and returned to Engineering. Rob manually removed it.

PR #21, `Clear proven stale Worker composer residue`, was squash-merged to `main` as `620ef84c57cbb87123bbca30e43faffda1e71032` after the branch was refreshed to current `main` and Rob reported all focused tests, affected regressions, and Ruff green.

The merged repair:

- recognizes only a canonical `LIFEOS_EXECUTION_WRAPPER=` first line containing valid JSON and nonempty `wrapper_id` and `run_id`;
- requires both IDs to occur together in one submitted user turn in that same Worker conversation before clearing residue;
- preserves unrelated, malformed, and unproven composer text;
- verifies the proven stale composer is empty before inserting the next prompt;
- does not retry the prior send or weaken the existing correlated-turn and stop-on-uncertainty gates.

No GitHub workflow runs were attached to the merge. Rob's local validation is the current test evidence. The next deployment step is to pull `main`, restart the dashboard, and confirm ordinary health. Live composer-cleanup evidence should come from a later separately authorized Worker dispatch rather than rerunning the completed Maintenance canary.

## Worker Portfolio

### Engineering Worker

- ID: `engineering_worker`
- Title: `Engineering_Worker`
- Route revision: `1`
- Availability: `available`
- Activation state: existing enabled production Worker

### Maintenance Worker

- ID: `maintenance_worker`
- Title: `Maintenance_Worker`
- Profile and procedures: on `main`
- Registry, route revision 1, canary, return to Engineering, and availability `available`: user-reported complete
- Deployment state: active and live
- Assigned work: none

### Deferred Department Workers

- `Business_HQ`: no Worker requested. Continue bounded one-off research assignments. Reconsider only a narrow Market Evidence Worker after recurring standardized research creates a measurable bottleneck.
- `Finance_HQ`: no Worker requested at present. Continue bounded one-off assignments and reconsider only after a recurring standardized workload creates a measurable bottleneck.
- `Wellness_HQ`: no Worker requested at present. Continue bounded one-off assignments and reconsider only after a recurring standardized workload creates a measurable bottleneck.
- No title, stable ID, profile, room, registry row, route, canary, activation, schedule, or assignment is authorized for these departments.

### Office Leaks

- Business state: paused by Rob
- Worker rollout: paused
- Existing records remain owned by `Office_Leaks_HQ` and must not become competing truth for the AI systems business

## Current Work

1. Pull current `main`, restart the dashboard, and confirm ordinary health after PR #21.
2. Keep the active Maintenance Worker idle until a separately authorized first assignment exists.
3. Define the future repository-audit assignment separately, including exact scope, authorization source, allowed writes, immutable result path, and `IMMEDIATE_HQ` review. This closeout does not assign it.
4. Use that or another separately authorized Worker dispatch to observe the full execution chain and composer cleanup behavior without rerunning the completed canary.
5. Keep the production Worker portfolio lean unless an owning department demonstrates a recurring standardized bottleneck and requests evaluation.
6. Keep Office Leaks paused.

## Advisory State

Open Engineering advisories: None.

`ADV-20260718-042`, `ADV-20260719-044`, and `ADV-20260723-052` are closed and must not be recreated as active work.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- One authoritative registry row exists per stable Worker ID.
- Route changes require a revision increment, initial hold, and zero-authority canary.
- The persisted shared safety pause is the only circuit breaker and requires explicit human resume.
- The shared send budget is one manually reset epoch; elapsed time never refills it and Reset does not Resume.
- The activation validator always reports `activation_authorized: false`; explicit human activation is a separate authority event and does not make the validator an activation ledger.
- Confirmed or uncertain sends are never blind-retried.
- PR #21 permits only proven stale LifeOS residue to be cleared; unrelated drafts remain protected.
- Immutable Git evidence outranks stale local transport state.
- `IMMEDIATE_HQ` work never auto-verifies.
- Courier, dashboard, ingester, watcher, HQ receipt, and Rob receipt do not close source work automatically.
- The Worker courier does not wake `Chief_of_Staff_HQ` under the current contract.
- The current production Worker portfolio is `Engineering_Worker` plus `Maintenance_Worker`; additional Workers require a demonstrated bottleneck, owner request, shared-contract review, and separate authorization.
- Recurring tasks, connectors, spending, public actions, broader authority, and real Maintenance assignments require separate owner review and authorization.

## Boundary

`Engineering_HQ` owns the machinery. Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. Source owners close their own records.