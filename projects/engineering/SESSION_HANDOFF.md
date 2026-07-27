# Engineering_HQ Session Handoff

Updated: 2026-07-26
Project: Engineering_HQ
Purpose: Fresh-room handoff after the core Worker platform and initial cross-department rollout were closed with an intentionally lean production portfolio, the Maintenance Worker remained active and idle, PR #21 merged the composer-residue repair, local deployment health remained to be confirmed, and a future repository-audit assignment remained separate and unauthorized until explicitly defined.

## Metadata

- Project Owner: Rob
- Primary Chat: `Engineering_HQ`
- Current Phase: Active / Core Worker Platform Complete / Lean Worker Portfolio / Maintenance Worker Active and Idle / PR #21 Merged / Local Deployment Health Pending / Repository Audit Assignment Pending Separate Authorization / Office Leaks Paused
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center runtime state, ChatGPT Department and Worker rooms, Engineering advisory board, Advisory Index, local Edge CDP bridge, and the GitHub-only Life OS Change Watch
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, private ChatGPT conversation URLs, or sensitive implementation details in LifeOS memory files or Worker result artifacts.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `memory/HQ_NAMING_STANDARD.md` before touching title-bearing code, runtime state, prompt launchers, route mappings, or tests.
7. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` when Worker dispatch, immutable result ingestion, HQ review, Rob validation, consumption, or browser courier behavior is in scope.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker authority, reporting, verification, activation prerequisites, or execution behavior is in scope.
9. Read the exact owning department's Worker profile and review procedure before linking, validating, or dispatching that Worker.
10. Perform a separate read-only Sync before any implementation write.
11. Keep connector, database, browser, and dashboard work small, explicit, fail-closed, and verifiable.

## Handbook Context

The Engineering handbook is available through Project Sources as a noncanonical context mirror. It may restore ordinary room identity and stable boundaries without a full Boot, but it does not replace GitHub or authorize writes. Fetch live canonical files before consequential actions, runtime claims, route changes, or package decisions.

## Department Role

`Engineering_HQ` owns technical architecture, software planning, repository strategy, automation design, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering owns technical Worker infrastructure: exact routing, transport, logging, duplicate suppression, immutable result ingestion, report repair, verification mechanics, runtime evidence, activation-prerequisite reporting, tests, and reliability safeguards.

Engineering does not own shared Worker governance, another department's Worker purpose or authority, source-owner lifecycle, business strategy, or domain judgment.

Route AI systems business strategy to `Business_HQ`, paused Office Leaks matters to `Office_Leaks_HQ`, cost-bearing choices to `Finance_HQ`, ordinary coordination to `Chief_of_Staff_HQ`, shared governance and memory hygiene to `Maintenance_HQ`, and wellbeing judgment to `Wellness_HQ`.

## Completed Architecture

### Package D

Lifecycle State: CLOSED

Established Worker registry, route, browser transport, semantic receiver, duplicate suppression, verification mechanics, and bounded pilot foundations.

### Package E

Lifecycle State: CLOSED
Closed: 2026-07-23
Canonical closeout: `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Proved the Engineering-only chain for dispatch, immutable result evidence, deterministic ingestion, report repair, owning-HQ review, Rob validation when required, consumption readiness, watcher reporting, and duplicate suppression.

### Package F Wave 0A

Lifecycle State: COMPLETE
Completed: 2026-07-23

Established canonical room and Worker naming, exact registered Worker URL routing, route revisions, guarded route capture, zero-authority canary behavior, and browser-bridge recovery.

### Package F Wave 0B

Lifecycle State: COMPLETE
Completed: 2026-07-25

Completed slices:

- PR #15, merge `83c309f651de0354982fcd6cbb68f9cf3251d6a3`: cross-department owning-HQ destination resolution.
- PR #16, merge `3bf20ca231b3b5fbb1c315b24881e46939b3b508`: persisted shared safety-pause triggers.
- PR #17, merge `e1d297f1a2517490b3fb2a37298689c6db25bfb0`: conservative global send budget.
- PR #18, merge `4a00c4908cfd71a2b2ebfe41c084b68a5d2907e5`: read-only contract-derived activation gate.

Rob confirmed the post-merge dashboard smoke passed.

### Initial Department Worker Expansion

Lifecycle State: CLOSED / LEAN PORTFOLIO ADOPTED
Closed: 2026-07-26

The production Worker portfolio remains intentionally limited to:

- `Engineering_Worker` / `engineering_worker`
- `Maintenance_Worker` / `maintenance_worker`

Owner decisions:

- `Business_HQ` does not request a Worker. Research continues through bounded one-off assignments. Reconsider only a narrow Market Evidence Worker after recurring standardized research creates a measurable bottleneck.
- `Finance_HQ` does not request a Worker at present.
- `Wellness_HQ` does not request a Worker at present.
- `Office_Leaks_HQ` remains paused.

No Business, Finance, Wellness, or Office Leaks Worker profile, title, stable ID, room, registry row, route, canary, activation, schedule, or assignment is authorized. Further adoption requires a demonstrated recurring standardized bottleneck and a new explicit request from the owning department.

## Maintenance Worker Rollout

Lifecycle State: ACTIVE / LIVE / NO ASSIGNMENTS

Canonical GitHub work:

- PR #19 merged as `28a7a4fc40317d043dbe9983747475f85d37742a`.
- PR #20 merged as `e91783dd9705df4a090eae2b4414adead6dafcf4`.
- Profile: `projects/life-logistics-hq/workers/maintenance_worker.md`.
- Result procedure: `projects/life-logistics-hq/procedures/maintenance_worker_result_submission.md`.
- HQ review procedure: `projects/life-logistics-hq/procedures/maintenance_hq_worker_review_receipt.md`.

Rob reports the following live local state:

- one registered `maintenance_worker` row;
- exact title `Maintenance_Worker`;
- exact private route captured at revision 1;
- zero-authority browser canary succeeded;
- courier returned to Engineering;
- route availability became `available`;
- the Worker is active and live;
- no work has been assigned.

Activation is complete and is separate from assignment authority. It does not create a task, schedule, unattended execution, broader connector permission, source-record repair authority, spending, or cross-department authority. A first real Maintenance assignment requires one separately exact bounded task, sources, read scope, allowed write scope, immutable result path, authorization source, and `IMMEDIATE_HQ` review.

The activation-readiness service remains read-only and continues to report `activation_authorized: false`. Rob's explicit activation is a separate authority event and does not turn the readiness report into a deployment ledger.

## Composer Residue Repair

Lifecycle State: MERGED TO `main` / LOCAL DEPLOYMENT HEALTH PENDING

After the successful Maintenance canary, ChatGPT restored the submitted synthetic prompt in the Maintenance composer. Rob manually deleted it. The send itself remained confirmed and the route remained valid.

PR #21, `Clear proven stale Worker composer residue`, was refreshed against current `main` and squash-merged as `620ef84c57cbb87123bbca30e43faffda1e71032` after Rob reported the focused tests, affected regressions, and Ruff green.

The merged repair:

- parses only a canonical `LIFEOS_EXECUTION_WRAPPER=` first line containing valid JSON and nonempty `wrapper_id` and `run_id`;
- clears an older LifeOS composer draft only when both identifiers are proven together in one submitted user turn in the same Worker conversation;
- reuses the current run-linked draft;
- preserves unrelated, malformed, and unproven text;
- verifies the proven stale composer is empty before inserting a new prompt;
- does not retry the prior send or weaken new-turn correlation and stop-on-uncertainty behavior.

GitHub exposed no workflow run for the merge. Rob's local validation is the current test evidence. Pull current `main`, restart the dashboard, and confirm ordinary health before treating deployment follow-through as complete. The next separately authorized Worker dispatch should provide natural live evidence of cleanup behavior; do not rerun the completed Maintenance canary merely to manufacture evidence.

## Current Production Worker State

### Engineering Worker

- Worker ID: `engineering_worker`
- Exact chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Route availability: `available`
- One authoritative registry row exists.
- Private exact URL remains only in ignored local SQLite state.

### Maintenance Worker

- Worker ID: `maintenance_worker`
- Exact chat title: `Maintenance_Worker`
- Canonical profile and procedures: present on `main`
- Registry and route linkage: user-reported complete
- Route revision: user-reported `1`
- Route availability: user-reported `available`
- Zero-authority canary: user-reported successful
- Deployment state: active and live
- First real assignment: none

### Deferred Department Workers

- Business, Finance, and Wellness have declined Worker rollout for now.
- Reconsideration belongs to the owning department after a recurring standardized bottleneck is demonstrated.
- No canonical Worker artifacts or runtime state should be created by analogy.

### Office Leaks

- Business state: paused by Rob.
- Office Leaks Worker rollout: paused.
- Existing Office Leaks files remain owned by `Office_Leaks_HQ` and must not become competing truth for the AI systems business.

## Next Valid Actions

1. Pull current `main`, restart the dashboard, and confirm ordinary health after PR #21.
2. Keep the active Maintenance Worker idle until a separately authorized first assignment exists.
3. Define the planned repository-audit assignment separately after this closeout. Establish the exact task, authoritative sources, read scope, allowed writes, exclusions, authorization source, immutable result path, completion condition, and `IMMEDIATE_HQ` review before dispatch.
4. Use that or another separately authorized Worker run to observe the full Worker-to-HQ evidence chain and composer cleanup behavior without rerunning the completed canary.
5. Keep the production Worker portfolio lean until an owning department demonstrates a recurring standardized bottleneck and explicitly requests evaluation.
6. Keep Office Leaks work paused.

The repository-audit statement in this handoff is planning context, not an assignment or write authority.

## Validation Standard

- Fetch current files before editing.
- Use current SHAs or equivalent concurrency guards.
- Preserve unrelated content and historical evidence.
- Prefer the smallest useful change.
- Read back every significant write.
- Do not claim route availability, a canary pass, dispatch, external action, or verification without current evidence or explicit Rob report.
- No meaningful change means no write.

## Advisory State

Open Engineering advisories: None.

`ADV-20260718-042`, `ADV-20260719-044`, and `ADV-20260723-052` are closed and must not be recreated as active work.

## Production Boundary

- Browser automation acts only on exact canonical URLs.
- Registered exact Worker URLs, not sidebar visibility, are authoritative route locators.
- Each stable Worker ID has one authoritative registry row.
- Route changes increment the route revision and remain held until a zero-authority canary passes.
- The persisted shared safety pause is the only circuit-breaker state and requires explicit human resume.
- The send budget is one manually reset epoch shared by Worker and owning-HQ wake attempts; elapsed time never refills it.
- Reset does not Resume, erase evidence, or authorize a send.
- The activation validator reports prerequisites only and always sets `activation_authorized: false`; explicit human activation is separate.
- `READY_FOR_AUTHORITY_REVIEW` is not activation approval or assignment authority.
- Confirmed or uncertain submissions are not retried blindly.
- PR #21 permits only proven stale LifeOS residue to be cleared; unrelated composer text remains protected.
- Immutable Git evidence outranks stale local transport state.
- Worker reports remain evidence until deterministic ingestion.
- `IMMEDIATE_HQ` work never auto-verifies.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Courier, ingester, dashboard, watcher, HQ receipt, and Rob receipt do not auto-close source work.
- The Worker courier does not wake `Chief_of_Staff_HQ` under the current contract.
- The current production portfolio is `Engineering_Worker` and `Maintenance_Worker` only.
- New Workers, connectors, recurring tasks, spending, cross-department authority, broader durable-write authority, public actions, or real Maintenance assignments require separate approval.

## Boundary

Rob decides. Department HQs own their Workers and judgment. `Maintenance_HQ` owns shared governance. `Engineering_HQ` owns the machinery. Source owners close their own records.