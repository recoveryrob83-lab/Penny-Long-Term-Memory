# Engineering_HQ

Updated: 2026-07-23

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
- technical Worker routing, transport, logging, duplicate suppression, result ingestion, evidence, and reliability;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

Engineering owns the machinery. It does not own canonical shared Worker governance, department-specific Worker authority, another department's records, source-owner advisory lifecycle, or domain judgment.

## Canonical Naming Boundary

`memory/HQ_NAMING_STANDARD.md` is the canonical naming source.

Current exact ChatGPT room titles are:

- `LifeOS_HQ`
- `Maintenance_HQ`
- `Engineering_HQ`
- `Business_HQ`
- `Office_Leaks_HQ`
- `Finance_HQ`
- `Chief_of_Staff_HQ`
- `Wellness_HQ`
- current Worker: `Engineering_Worker`

`Maintenance_HQ` owns the shared textual standard. `Engineering_HQ` owns implementation of those titles in Engineering-controlled code, browser routing, runtime configuration, current route mappings, prompt launchers, tests, and bounded active-state migrations.

Display-name changes do not authorize filesystem-path renames, Worker-ID changes, destination-key changes, historical-row rewrites, immutable-evidence rewrites, or checksum changes.

## Canonical Worker Model

A LifeOS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, procedures, authority, holds, verification, and domain judgment.
- GitHub holds canonical profiles, procedures, task state, decisions, and immutable result and review evidence.
- SQLite runtime state remains the sole operational ledger.
- The Worker registry row holds stable identity, the exact private ChatGPT conversation URL, and a monotonic route revision.
- Browser dispatch uses the registered exact URL and fails closed if it is missing or invalid.
- The browser courier wakes an authorized Worker or owning HQ, proves one correlated submission, returns immediately, and never waits for completion.
- The Worker performs bounded work and writes one immutable schema-valid report attempt under exact narrow reporting authority.
- A deterministic ingester validates the report, calculates the canonical checksum, updates the existing runtime row, and requests report repair when needed without re-executing the work.
- Department HQ reviews report integrity, authority compliance, evidence, and the actual work where possible.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Signed HQ or Rob results become consumption-ready.
- A separately authorized scheduled watcher may report meaningful signed changes.
- The Worker courier never wakes `Chief_of_Staff_HQ`.
- Source owners retain advisory lifecycle and closure authority.

Python, browser automation, SQLite, and the dashboard provide routing, safety, logging, duplicate suppression, ingestion, verification mechanics, and visibility. They are not the Worker and do not replace Department HQ judgment.

A GitHub Worker result outbox is immutable evidence, not a competing runtime ledger.

## Direct URL Routing Contract

The registered exact conversation URL is the authoritative browser locator for a Worker.

- Sidebar discovery is not part of normal Worker dispatch.
- Sidebar visibility after navigation is not route identity.
- A missing or invalid registered URL blocks dispatch before any send.
- One existing Worker row remains authoritative; fresh-chat rollover does not create a second Worker identity.
- Route changes increment `route_revision`.
- A changed route is placed on `unknown` hold with `last_seen_at` cleared.
- Real advisory execution requires route availability to be exactly `available`.
- A zero-authority canary promotes only the exact unchanged witnessed revision.
- Private exact conversation URLs remain in ignored local runtime state and are not copied into GitHub memory files.

## Guarded Dashboard Route Rollover

The Worker Operations dashboard can capture a replacement Worker conversation directly from the local CDP browser target list without requiring manual URL pasting.

Capture fails closed unless:

- automation is paused;
- the shared execution lock is free;
- the operator explicitly confirms capture;
- the expected route revision still matches the authoritative row;
- exactly one ChatGPT conversation target is open;
- the browser target title matches the selected Worker's exact title;
- the captured URL is not already owned by another Worker.

A successful changed capture updates one existing registry row, increments the revision, and holds the route until the existing synthetic zero-authority canary succeeds.

Starting the dashboard alone does not authorize route capture, route rollover, real Worker dispatch, schedules, or unattended local orchestrator sends.

## Not This Department

- Business strategy, branding, market research, monetization, or customer discovery: `Business_HQ` or `Office_Leaks_HQ`.
- Finance, benefits, budget, bills, subscriptions, or cost approval: `Finance_HQ`.
- Daily one-off scheduling, ordinary coordination, executive-function support, or quick administration: `Chief_of_Staff_HQ`.
- Shared global boot integrity, advisory-index hygiene, cross-project audits, migrations, canonical Worker governance, and system-wide housekeeping: `Maintenance_HQ`.
- Recovery, pacing, health, or sustainability judgment: `Wellness_HQ`.

## Department File Ownership

Engineering maintains its own project subtree during authorized maintenance and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, implementation packets, decision records, Engineering source-board advisory text, procedures, and Engineering-owned Worker result evidence.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner or explicit coordinated authorization.

Package E proved a Worker result outbox only under Engineering-owned paths. It did not grant universal Worker write authority. Shared adoption requires `Maintenance_HQ` review and explicit authorization by each owning department.

## Current Technical State

Package D and Package E are closed.

The completed runtime repair chain is:

1. **Canonical title rollover and courier verifier repair**
   - PR #9
   - Merge: `f8cc341e17cb68492c5f66339382b753bd1612ab`
   - Canonical underscore titles implemented in Engineering executable surfaces and active title-bearing state.
   - Post-navigation identity uses the already resolved exact URL plus room witnesses instead of requiring persistent sidebar visibility.

2. **Authoritative direct Worker URL routing**
   - PR #10
   - Merge: `b859c3c72e8b82f876b9ebf72d2961f4eb33ecbd`
   - Existing Worker registry row stores the exact URL and route revision.
   - Direct dispatch fails closed without the registered URL.
   - Production `engineering_worker` route revision `1` was verified by a live zero-authority canary and promoted to `available`.

3. **Guarded dashboard route capture and rollover**
   - PR #11
   - Merge: `2587b540e24ca09036c1f0094187c69c2b363c63`
   - Dashboard capture, revision guards, wrong-room refusal, duplicate ownership refusal, verification holds, and canary-only promotion are implemented.
   - Final consolidated regression gate: `80 passed`.
   - No production route rollover occurred during implementation.

## Current Production Worker State

- Worker ID: `engineering_worker`
- Chat title: `Engineering_Worker`
- Deployment state: `enabled`
- Route revision: `1`
- Route availability: `available`
- Registry identity rows: one
- Private exact URL: local runtime state only

## Current Dashboard State

The LifeOS Dashboard code is merged to `main` and ready for local launch or restart.

Expected endpoint:

```text
http://127.0.0.1:8765
```

The current fresh `Engineering_HQ` chat completed canonical Boot and a separate read-only Sync. The remaining post-merge smoke check is:

- confirm local `main` is clean and contains merge `2587b540e24ca09036c1f0094187c69c2b363c63` or later;
- start or confirm the dashboard process;
- inspect `/api/health`;
- inspect Worker Operations;
- confirm one `engineering_worker` row at route revision `1` with availability `available`;
- confirm guarded route controls render;
- do not capture or mutate the route without an actual replacement Worker room and explicit Rob authorization.

## Current Decision Boundary

Completed routing repairs must not remain open merely for visibility and must not be recreated as new work.

Future Engineering work must come from:

- `projects/engineering/open_loops.md`;
- a demonstrated defect with bounded repair authority;
- or a new explicit Rob instruction.

Cross-department result-outbox adoption, universal Worker write authority, optional human-readable envelope work, broader unattended packaging, new recurring tasks, connectors, spending, and public actions remain separate decisions.

`ADV-20260723-052` is closed after Rob confirmed the watcher destination test passed. `ADV-20260718-042` is closed by its Chief of Staff source owner after implementation and source verification. Slow rollout remains an operational pacing decision, not unfinished Engineering work.

## Browser and Automation Boundary

- Operate only against exact canonical ChatGPT URLs.
- Use the registered exact Worker URL as the authoritative locator.
- Do not require selected-room sidebar visibility after exact URL navigation.
- Require stable history hydration, exact room identity, an empty composer, and no active generation.
- Prove a new marker-bearing user turn, increased turn count, and an empty composer before calling a send confirmed.
- Never blind-retry a confirmed or uncertain submission.
- Ingest existing immutable HQ evidence before attempting another HQ wake.
- Use atomic one-shot claims to suppress concurrent or uncertain repeat wakes.
- Fail closed on unrecognized post-submit states and require human inspection.
- Do not scrape assistant responses in the dispatch-only courier.
- Do not let automation decide HQ or Rob judgment.
- Do not let courier, dashboard, watcher, or evidence receipts close source advisories automatically.

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

Active department. Package D and Package E are closed. Canonical runtime titles, direct Worker URL routing, and guarded dashboard route management are complete. Fresh-room Boot and Sync are complete; the read-only post-merge dashboard smoke check remains pending before continuing from the remaining open loops.
