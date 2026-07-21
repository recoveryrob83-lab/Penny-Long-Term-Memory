# Engineering HQ

Updated: 2026-07-21

## Purpose

Engineering HQ coordinates Rob's technical architecture, software planning, repository strategy, automation design, implementation sequencing, testing, debugging, and build-readiness for Life OS and related technical systems.

Engineering turns approved requirements into safe, testable machinery and maintains durable state inside its own project domain.

## Role

Use Engineering HQ for:

- technical architecture and repository strategy;
- software, API, connector, and data-model design;
- automation and desktop-control safety;
- LifeOS Dashboard and Automation Command Center architecture;
- prompt systems and command interfaces;
- technical Worker routing, transport, logging, duplicate suppression, result ingestion, evidence, and reliability;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

Engineering owns the machinery. It does not own canonical shared Worker governance, department-specific Worker authority, another department's records, source-owner advisory lifecycle, or domain judgment.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, procedures, authority, holds, verification, and domain judgment.
- GitHub holds canonical profiles, procedures, task state, and immutable result and review evidence.
- SQLite `execution_history` remains the sole operational runtime ledger.
- The browser courier wakes an authorized Worker or owning HQ, proves submission, returns immediately, and never waits for completion.
- The Worker performs bounded work and writes one immutable schema-valid report attempt under exact narrow reporting authority.
- A deterministic ingester validates the report, updates existing runtime state, and requests report repair when needed without re-executing the work.
- Department HQ reviews report integrity, authority compliance, evidence, and the actual work where possible.
- Work unavailable to HQ inspection requires explicit Rob validation.
- Signed HQ or Rob results become available for later scheduled Chief of Staff consumption.
- The courier never wakes Chief of Staff.
- Source owners retain advisory lifecycle and closure authority.

Python, browser automation, SQLite, and the dashboard provide routing, safety, logging, duplicate suppression, ingestion, verification mechanics, and visibility. They are not the Worker and do not replace Department HQ judgment.

A GitHub Worker result outbox is immutable evidence, not a competing runtime ledger.

## Not This Department

- Business strategy, branding, market research, monetization, or customer discovery: Business HQ or Office Leaks HQ.
- Finance, benefits, budget, bills, subscriptions, or cost approval: Finance HQ.
- Daily one-off scheduling, ordinary coordination, executive-function support, or quick administration: Chief of Staff HQ.
- Shared global boot integrity, advisory-index hygiene, cross-project audits, migrations, canonical Worker governance, and system-wide housekeeping: Life OS Maintenance HQ.
- Recovery, pacing, health, or sustainability judgment: Wellness HQ.

## Department File Ownership

Engineering maintains its own project subtree during authorized maintenance and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, implementation packets, decision records, and Engineering source-board advisory text.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner or explicit coordinated authorization.

Package E may pilot a Worker result outbox under Engineering-owned paths. It may not silently grant universal Worker write authority. Shared adoption requires Life OS Maintenance HQ review and explicit authorization by each owning department.

## Current Technical State

The LifeOS Dashboard is locally running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Department Inspection has been locally verified at 414 normalized records, zero findings, and zero warnings.

Canonical shared architecture lives in:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

Package D is closed after implementing and validating the technical Worker registry, routing, transport, receiver, verification, duplicate-suppression, and synthetic pilot foundation.

Package E is active and authoritative at:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

The initial Package E one-tab courier and Worker Operations cockpit are an implemented transitional foundation. Live pilots demonstrated exact destination routing, hydration protection, and zero-authority transport, but also exposed the architectural cost of waiting for Worker responses in the browser.

The production direction is now:

1. dispatch-only courier wake;
2. immediate return and browser-gate release;
3. immutable Worker result artifact;
4. deterministic ingestion and report repair;
5. owning-HQ wake and verification receipt;
6. Rob validation when HQ cannot independently inspect the work;
7. signed result ready for later Chief of Staff consumption.

The current courier still contains response-waiting and assistant-response capture from the superseded round-trip design. It is transitional and must be refactored before further real Package E proof.

## Current Decision Boundary

The next valid implementation is Package E Slice 2: convert the one-tab courier into dispatch-only transport that proves the correlated user turn, records `DISPATCH_SUBMITTED`, returns immediately, and frees the courier while the Worker executes independently.

Later slices add an Engineering-only result-outbox pilot, deterministic ingester and report repair, owning-HQ verification, Rob validation, and a separately authorized read-only Chief of Staff scheduled-consumption task.

Cross-department rollout, scheduled-task activation, shared Worker-contract changes, new Worker authority, and advisory closure remain separate decisions.

## Composer Boundary

The general full-text composer investigation is paused and must not be reopened without demonstrated failure.

The Worker-only entrypoint preserves exact destination, hydration checks, empty-composer protection, explicit send, one-job locking, and stop-on-uncertainty safeguards. The dispatch-only redesign must not reintroduce repeated selection, character-range comparison, dual witnesses, focus hacks, alternate paste mechanisms, or broad timeout experiments without evidence.

## Security Rule

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, private user data, or sensitive implementation details in Life OS GitHub memory or Worker result artifacts.

Use ignored local environment files or the appropriate secure source system for operational credentials.

## Boot Files

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`

## Current Status

Active department. Package D is closed. Package E has been reshaped around nonblocking dispatch, immutable result evidence, deterministic ingestion and repair, Department HQ verification, explicit Rob validation where necessary, and later scheduled Chief of Staff consumption. The next implementation action is the dispatch-only courier conversion.