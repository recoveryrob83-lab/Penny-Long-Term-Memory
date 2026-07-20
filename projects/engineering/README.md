# Engineering HQ

Updated: 2026-07-20

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
- technical Worker routing, transport, logging, duplicate suppression, evidence, and reliability;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

Engineering owns the machinery. It does not own canonical shared Worker governance, department-specific Worker authority, another department's records, or the Worker’s domain judgment.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

- The Department HQ owns the Worker profile, procedures, authority, and domain judgment.
- GitHub holds the canonical profile, procedures, task state, and durable evidence.
- The Worker chat reads those sources, validates the bounded assignment, performs authorized work, and returns one controlled outcome with evidence.
- Department HQ reviews the result and retains ownership.
- Python, desktop automation, SQLite, and the dashboard provide courier, routing, safety, logging, duplicate-suppression, and visibility infrastructure.

Python is not the Worker. Machine-side validation may provide defense in depth, but it does not replace the ChatGPT Worker’s operational source reading, judgment, refusal behavior, or Department HQ review.

## Not This Department

- Business strategy, branding, market research, monetization, or customer discovery: Business HQ or Office Leaks HQ.
- Finance, benefits, budget, bills, subscriptions, or cost approval: Finance HQ.
- Daily one-off scheduling, ordinary coordination, executive-function support, or quick administration: Chief of Staff HQ.
- Shared global boot integrity, advisory-index hygiene, cross-project audits, migrations, canonical Worker governance, and system-wide housekeeping: Life OS Maintenance HQ.
- Recovery, pacing, health, or sustainability judgment: Wellness HQ.

## Department File Ownership

Engineering maintains its own project subtree during authorized maintenance and implementation work. This includes its handoff, identity, README, status, open loops, notebooks, implementation packets, decision records, and Engineering source-board advisory text.

Shared global files, other departments' canonical files, the Advisory Index, and cross-department governance changes require the appropriate owner or explicit coordinated authorization.

## Current Technical State

The LifeOS Dashboard is locally running on Rob's Windows machine with live read-only GitHub, Trello, Todoist, and Google Calendar data. Department Inspection has been locally verified at 414 normalized records, zero findings, and zero warnings.

The established Automation Command Center supports eight exact HQ destinations, canonical, saved, and custom prompts, persistent schedules and run history, validated pause-on-failure and restart policy, Scheduler Ledger synchronization, and bounded cleanup controls.

Canonical shared architecture lives in:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

Package D has implemented and locally validated seven technical slices:

1. Worker contracts and validation.
2. SQLite Worker registry, route state, and task-scoped receiver persistence.
3. Registry service and exact-title resolution.
4. Separate Worker Command Center transport and execution-history integration.
5. Receiver semantic validation and controlled outcomes.
6. Verification views, queue derivation, and wake suppression.
7. Disposable synthetic end-to-end backend pilot with transport-integrity hardening.

A separate bounded synthetic desktop pilot passed exact ChatGPT Classic navigation, wrapper-marker verification, explicit submission, receipt generation, and exact acknowledgement without creating durable authority.

Validation evidence recorded in the Package D packet includes a focused Slice 7 and receiver suite of 32 passing tests, a complete dashboard regression suite of 222 passing tests with 9 warnings, and a successful bounded desktop receipt with `durable_authority_created: false`.

No real Worker profile, registry entry, route, wake, Worker control surface, or recurring Worker authority schedule has been created.

## Current Decision Boundary

ADV-20260718-042 states that the automation layer is the courier and the receiving Worker validates canonical prompt or procedure, parameters, authority, ownership, scope, and source boundaries.

For Life OS, that receiving Worker is the specialized ChatGPT Worker room. The earlier Engineering recommendation for a mandatory Python receiver-ingress and canonical-resolution service overinterpreted the machine-runtime layer and is withdrawn as a presumed next requirement.

The next implementation goal remains unselected. Engineering’s current recommendation is:

1. define the operational Worker execution procedure and canonical GitHub source-resolution contract;
2. run one bounded ChatGPT Worker pilot;
3. verify controlled outcomes, refusal of unauthorized expansion, duplicate suppression, evidence, and Department HQ review;
4. add deeper Python source resolution only if the pilot demonstrates a concrete need.

The human-readable envelope summary remains a separate small production-readability follow-up before the first real Worker activation.

ADV-20260719-044 is closed, implemented, and source verified. Engineering no longer monitors Maintenance implementation of that advisory.

## Composer Boundary

The general full-text composer investigation is paused and must not be reopened without demonstrated failure.

The Worker-only entrypoint preserves exact destination, empty-composer protection, clipboard restoration, explicit send, one-job locking, and stop-on-uncertainty safeguards. After paste it copies once and checks only whether the expected wrapper ID is present.

Do not resume repeated selection, character-range comparison, multiple witnesses, focus hacks, alternate paste mechanisms, or broad timeout experiments without demonstrated failure.

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

Active department. Package D's technical backend and desktop milestone is complete. ADV-042 remains open pending bounded operational ChatGPT Worker evidence and source-owner review. Rob's next implementation-goal decision is pending. Real Worker activation, recurring Worker authority generation, Package E, and unrelated expansion remain deferred.