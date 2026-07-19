# Engineering HQ

Updated: 2026-07-19

## Purpose

Engineering HQ coordinates Rob's technical architecture, software planning, repository strategy, automation design, implementation planning, testing, and build-readiness for Life OS and related technical systems.

Engineering turns approved requirements into safe, testable technical systems and maintains durable state inside its own project domain.

## Role

Use Engineering HQ for:

- technical architecture and repository strategy;
- software, API, connector, and data-model design;
- automation and desktop-control safety;
- LifeOS Dashboard and Automation Command Center architecture;
- prompt systems and command interfaces;
- technical Worker routing, receiver validation, runtime enforcement, and reliability;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

## Current Operating Tracks

- Package D Worker-runtime implementation under the canonical shared execution and Worker contracts.
- Worker registry, stable IDs, exact-title routing, deployment and route state, task-scoped receiver revisions, and idempotency.
- Separate Worker Command Center execution with persistent envelope evidence.
- Receiver-side semantic and authorization validation under ADV-20260718-042.
- Desktop department automation maintenance under exact-navigation and stop-on-uncertainty rules.
- LifeOS Dashboard observation and source-health behavior.
- Reliable Connector Execution Layer, operation-ledger, verification, and retry policy design.
- Grandfathered Raw Capture and Inventory Worker evidence.
- Office Leaks delivery architecture as concrete requirements mature.

## Not This Department

- Business strategy, branding, market research, monetization, or customer discovery: Business HQ or Office Leaks HQ.
- Finance, benefits, budget, bills, subscriptions, or cost approval: Finance HQ.
- Daily one-off scheduling, ordinary coordination, executive-function support, or quick administration: Chief of Staff HQ.
- Shared global boot integrity, advisory-index hygiene, cross-project audits, migrations, canonical Worker governance, and system-wide housekeeping: Life OS Maintenance HQ.
- Recovery, pacing, health, or sustainability judgment: Wellness HQ.

## Department File Ownership

Engineering maintains its own project subtree during routine boots, syncs, and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, decision rules, implementation notes, and Engineering source-board advisory text.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner or explicit coordinated authorization.

## Current Technical State

The LifeOS Dashboard is locally running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Guarded GitHub synchronization permits only clean, strictly-behind fast-forward updates. Department Inspection has been locally verified at 414 normalized records, zero findings, and zero warnings.

The established Automation Command Center supports eight exact HQ destinations, canonical, saved, and custom prompts, persistent schedules and run history, validated pause-on-failure and restart policy, Scheduler Ledger synchronization, and bounded cleanup controls.

The canonical shared architecture lives in:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

Package D has implemented four backend slices:

1. Worker contracts and validation.
2. SQLite registry, route, and task-scoped receiver persistence.
3. Registry service and exact-title resolution.
4. Separate Worker Command Center transport and execution-history integration.

Current Worker-runtime capabilities include:

- stable `worker_id` and exact `chat_title`;
- department-owned profile pointers with Engineering-owned deployment state outside profiles;
- `enabled`, `paused`, and `retired` deployment states;
- separate route availability;
- compact execution envelopes;
- task-scoped receiver revision state;
- idempotency by `worker_id + task_id + task_revision`;
- exact-title zero-match and duplicate-match failure;
- shared Command Center pause and one-job locking;
- manual and scheduler-triggered methods for one authorized envelope;
- successful-send duplicate suppression and bounded retry after failed transport;
- existing SQLite execution-history metadata for wrapper, run, Worker, task, revision, procedure, authorization, idempotency, verification mode, trigger, and future outcome;
- Worker-only post-paste verification by one copied-text check for the expected `wrapper_id`.

Rob reported the Slice 1–3 focused tests and full dashboard suite passed locally. Slice 4 adds 11 focused tests and awaits focused plus full local validation.

No real Worker profile, route, registry entry, Worker UI, or recurring Worker authority schedule has been created.

ADV-20260718-042 remains authoritative for receiver-side semantic validation. ADV-20260719-044 remains open to Life OS Maintenance HQ for shared Worker filesystem and continuity repairs.

## Composer Boundary

The old full-text composer investigation is closed as an active engineering path.

The Worker-only entrypoint preserves exact destination, empty-composer, clipboard restoration, explicit send, and stop-on-uncertainty safeguards. After paste it copies once and checks only whether the expected wrapper ID is present.

Do not reopen repeated selection, character-range comparison, multiple witnesses, focus hacks, alternate paste mechanisms, or broad timeout experiments without demonstrated failure.

## Security Rule

Never store secrets, credentials, tokens, API keys, private calendar URLs, financial account details, medical details, private user data, or sensitive implementation details in Life OS GitHub memory.

Use ignored local environment files or the appropriate secure source system for operational credentials.

## Boot Files

- `projects/engineering/SESSION_HANDOFF.md`
- `projects/engineering/DEPARTMENT_IDENTITY.md`
- `projects/engineering/README.md`
- `projects/engineering/status.md`
- `projects/engineering/open_loops.md`

## Current Status

Active department. Current gate: run the four focused Worker-runtime test files and the full dashboard suite. If both pass, begin Slice 5 receiver-side profile, authority, scope, parameter, duplicate, and controlled-outcome validation. Keep Worker UI, real profile activation, recurring Worker authority generation, Package E, and unrelated expansion deferred.