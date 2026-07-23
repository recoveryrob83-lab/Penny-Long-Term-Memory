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

Maintenance_HQ owns the shared textual standard. Engineering_HQ owns implementation of those titles in Engineering-controlled code, browser routing, runtime configuration, current route mappings, prompt launchers, tests, and bounded active-state migrations. Display-name changes do not authorize filesystem-path renames, worker-ID changes, destination-key changes, historical-row rewrites, immutable-evidence rewrites, or checksum changes.

## Canonical Worker Model

A LifeOS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, procedures, authority, holds, verification, and domain judgment.
- GitHub holds canonical profiles, procedures, task state, decisions, and immutable result and review evidence.
- SQLite `execution_history` remains the sole operational runtime ledger.
- The browser courier wakes an authorized Worker or owning HQ, proves one correlated submission, returns immediately, and never waits for completion.
- The Worker performs bounded work and writes one immutable schema-valid report attempt under exact narrow reporting authority.
- A deterministic ingester validates the report, calculates the canonical checksum, updates the existing runtime row, and requests report repair when needed without re-executing the work.
- Department HQ reviews report integrity, authority compliance, evidence, and the actual work where possible.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Signed HQ or Rob results become consumption-ready.
- A separately authorized scheduled watcher may report meaningful signed changes.
- The courier never wakes `Chief_of_Staff_HQ`.
- Source owners retain advisory lifecycle and closure authority.

Python, browser automation, SQLite, and the dashboard provide routing, safety, logging, duplicate suppression, ingestion, verification mechanics, and visibility. They are not the Worker and do not replace Department HQ judgment.

A GitHub Worker result outbox is immutable evidence, not a competing runtime ledger.

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

The LifeOS Dashboard is running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Department Inspection has been locally verified at 414 normalized records, zero findings, and zero warnings.

Package D is closed after implementing and validating the technical Worker registry, routing, transport, receiver, verification, duplicate-suppression, and synthetic pilot foundation.

Package E is closed and authoritative at:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Package E completed and live-validated the Engineering-only chain for:

- dispatch-only Worker wakes;
- exact URL, hydration, identity, composer, generation, and new-turn submission witnesses;
- immediate courier release and source-room return;
- immutable schema-valid Worker reports;
- deterministic checksum and same-row result ingestion;
- rejection and correction-only report-repair mechanics;
- owning-HQ wakes and immutable HQ review receipts;
- explicit Rob-validation receipts when HQ cannot inspect decisive evidence;
- signed consumption-ready states;
- scheduled watcher reporting under separate authorization;
- duplicate execution, result, and HQ-wake suppression;
- source-owner advisory lifecycle separation.

Final live evidence includes:

- `ADV-20260721-048`: immutable Worker report plus `Engineering_HQ` `VERIFIED` receipt, consumption-ready without Rob validation;
- `ADV-20260722-049`: `ROB_VALIDATION_REQUIRED` HQ receipt followed by Rob's immutable `VERIFIED` receipt;
- `ADV-20260723-051`: Worker report, HQ wake, immutable `VERIFIED` review, `HQ_VERIFIED` runtime reconciliation, and live duplicate-wake suppression after repair.

The scheduled watcher machinery is separately authorized under `Chief_of_Staff_HQ`. `ADV-20260723-052` remains open solely to verify that its report lands in the existing Chief of Staff conversation without creating a new chat or triggering work.

## Current Transition

Maintenance_HQ completed the repository-wide current-text naming repair and preserved executable Engineering surfaces, browser selectors, runtime registries, SQLite data, tests, historical evidence, immutable Worker artifacts, and stable filesystem paths for a separate Engineering repair.

Rob authorized the next Engineering slice after a fresh-room boot and sync:

1. update Engineering-owned code, configuration, route mappings, prompt launchers, dashboard labels, tests, and active title-bearing local state to the canonical underscore titles;
2. use exact old-to-new mappings rather than broad replacement;
3. preserve historical execution rows, immutable reports and receipts, worker IDs, destination keys, run IDs, wrapper IDs, checksums, and stable paths;
4. verify all eight HQ rooms and `Engineering_Worker` in draft or zero-authority mode before resuming broader rollout.

The browser bridge was successfully re-established after an Edge restart through a CDP-enabled Edge session at `http://127.0.0.1:9222`.

A zero-authority courier self-test then exposed a specific verifier defect. The courier resolved the exact `Engineering_Worker` URL and loaded the Worker conversation, but ChatGPT refreshed and collapsed the project sidebar behind `Show more`. The redundant post-navigation identity verifier waited for the hidden sidebar anchor and failed closed before filling the composer or sending. Nothing was sent and no runtime row was created.

The repair must keep pre-navigation sidebar URL resolution, then use the already verified exact URL plus loaded-room, history, composer, and generation witnesses after navigation. Sidebar visibility is navigation furniture, not authoritative post-navigation identity.

## Current Decision Boundary

Package E slices and advisories must not be recreated as active work.

Future Engineering work must come from:

- `projects/engineering/open_loops.md`;
- a demonstrated defect with bounded repair authority;
- or a new explicit Rob instruction.

Cross-department result-outbox adoption, universal Worker write authority, optional human-readable envelope work, broader unattended packaging, new recurring tasks, connectors, spending, and public actions remain separate decisions.

`ADV-20260718-042` remains open under `coordination/boards/main-assistant.md` and is not closed by Package E.

## Browser and Automation Boundary

- Operate only against exact canonical ChatGPT URLs.
- Use sidebar links to resolve exact destinations when needed, but do not require a selected room's sidebar anchor to remain visible after exact URL navigation.
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

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, private user data, or sensitive implementation details in LifeOS GitHub memory or Worker result artifacts.

Use ignored local environment files or the appropriate secure source system for operational credentials.

## Boot Files

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`

## Current Status

Active department. Package D and Package E are closed. Maintenance_HQ completed the textual naming repair. The next fresh Engineering_HQ chat must boot and sync before executing the bounded exact-title implementation rollover and courier post-navigation verifier repair. The watcher destination test remains pending under `ADV-20260723-052`.
