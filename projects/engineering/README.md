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
- LifeOS Dashboard and Worker Operations architecture;
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
- A deterministic ingester validates the report, calculates the canonical checksum, updates existing runtime state, and requests report repair when needed without re-executing the work.
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

Engineering maintains its own project subtree during authorized maintenance and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, implementation packets, decision records, Engineering source-board advisory text, procedures, and Engineering-owned Worker result evidence.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner or explicit coordinated authorization.

Package E may pilot a Worker result outbox under Engineering-owned paths. It may not silently grant universal Worker write authority. Shared adoption requires Life OS Maintenance HQ review and explicit authorization by each owning department.

## Current Technical State

The LifeOS Dashboard is running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Department Inspection has been locally verified at 414 normalized records, zero findings, and zero warnings.

Package D is closed after implementing and validating the technical Worker registry, routing, transport, receiver, verification, duplicate-suppression, and synthetic pilot foundation.

Package E is active and authoritative at:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Current Package E evidence:

- Slice 2 dispatch-only transport is implemented and locally validated with 40 focused tests passing;
- `ADV-20260721-048` reached `engineering_worker` and the Worker completed independently;
- the courier failed to return the controlled browser tab to Engineering HQ after the successful wake;
- Slice 3 created the first bounded live immutable report artifact;
- report path: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`;
- creation commit: `fbe75f13bc1b3a2dd35815e0d145c25da8695e22`;
- blob SHA: `f218d63519d38352b8aee4a790ed20807b1bebee`;
- controlled outcome: `IMPLEMENT`;
- verification remains `pending`;
- Rob sees the successful package outbox in Worker Operations;
- deterministic ingestion and formal HQ signoff do not yet exist.

The existing ADV-048 run must not be resent. Its report is the first valid live target for Slice 4 ingestion.

## Current Decision Boundary

The next valid work is:

1. inspect the ADV-048 execution row and dispatch receipt;
2. repair exact return-to-source behavior without weakening dispatch safeguards or reopening duplicate-send risk;
3. add focused regression coverage;
4. implement Package E Slice 4 deterministic ingestion, checksum calculation, rejection evidence, report-repair wakes, and same-row runtime updates;
5. use the existing report artifact for first live ingestion;
6. leave formal Engineering HQ review and advisory closure pending until ingestion succeeds.

Later slices add owning-HQ verification, Rob validation, `READY_FOR_COS`, and a separately authorized read-only Chief of Staff scheduled-consumption task.

Cross-department rollout, scheduled-task activation, shared Worker-contract changes, new Worker authority, and advisory closure remain separate decisions.

## Composer Boundary

The general full-text composer investigation is paused and must not be reopened without demonstrated failure.

The Worker-only entrypoint preserves exact destination, hydration checks, empty-composer protection, explicit send, one-job locking, and stop-on-uncertainty safeguards. The return-to-source repair must remain bounded to the demonstrated post-send navigation defect and must not reintroduce repeated selection, character-range comparison, dual witnesses, focus hacks, alternate paste mechanisms, or broad timeout experiments without evidence.

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

Active department. Package D is closed. Package E has a successful live immutable outbox artifact, an open courier return-to-source defect, and no deterministic ingestion or formal HQ signoff yet. Slice 4 is next after the bounded browser-return repair.