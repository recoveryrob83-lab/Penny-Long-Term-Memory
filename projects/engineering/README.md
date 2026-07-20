# Engineering HQ

Updated: 2026-07-19

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
- technical Worker routing, receiver validation, runtime enforcement, evidence, and reliability;
- testing, debugging, implementation sequencing, feasibility review, and build-ready packets;
- Engineering-owned durable-memory maintenance.

Engineering owns the machinery. It does not own canonical shared Worker governance, department-specific Worker authority, or another department's records.

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

Package D has implemented and locally validated seven slices:

1. Worker contracts and validation.
2. SQLite Worker registry, route state, and task-scoped receiver persistence.
3. Registry service and exact-title resolution.
4. Separate Worker Command Center transport and execution-history integration.
5. Receiver semantic validation and controlled outcomes.
6. Verification views, queue derivation, and wake suppression.
7. Disposable synthetic end-to-end backend pilot with transport-integrity hardening.

A separate bounded synthetic desktop pilot also passed exact ChatGPT Classic navigation, wrapper-marker verification, explicit submission, receipt generation, and exact acknowledgement without creating durable authority.

Current Worker-runtime capabilities include:

- stable Worker IDs and exact visible titles;
- department-owned profile pointers with Engineering-owned deployment state kept outside profiles;
- separate deployment and route-availability state;
- compact machine-readable execution envelopes;
- task-scoped receiver revision state and idempotency;
- exact-title zero-match and duplicate-match failure;
- shared Command Center pause and one-job locking;
- manual and scheduler-triggered transport for one already-authorized envelope;
- successful-send duplicate suppression with bounded retry after failed transport;
- exact successful-transport metadata validation before receiver acceptance;
- semantic checks for profile identity, ownership, caller authority, procedure identity and checksum, parameters, sources, scopes, tools, verification mode, and revision freshness;
- exactly one controlled outcome: `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL`;
- same-row evidence, Department HQ review, verification state, queue derivation, and wake suppression;
- read-only Automation Logs visibility without a second ledger.

Validation evidence currently recorded in the Package D packet includes a focused Slice 7 and receiver suite of 32 passing tests and a complete dashboard regression suite of 222 passing tests with 9 warnings. The live desktop pilot reported `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`.

No real Worker profile, registry entry, route, wake, Worker control surface, or recurring Worker authority schedule has been created.

## Current Decision Boundary

ADV-20260718-042 remains open and authoritative for receiver-side semantic validation and controlled outcomes. A read-only Engineering verification found the implementation substantially complete but identified two remaining closure gaps:

1. a production receiver-ingress path that parses transported evidence and independently resolves the authoritative Worker profile, canonical procedure, and task source instead of receiving preconstructed authoritative objects from its caller;
2. one joined bounded proof connecting physical desktop transport to receiver acceptance, controlled outcome, evidence, and verification.

Rob has not yet selected the next implementation slice. Receiver ingress and canonical resolution is the leading Engineering recommendation, while the human-readable envelope summary remains a separate smaller production-readability follow-up.

ADV-20260719-044 is closed, implemented, and source verified. Engineering no longer monitors Maintenance implementation of that advisory. The remaining department-ownership action is ordinary observation of corrected role-routed boots and demonstrated defects.

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

Active department. Package D's backend and desktop milestone is complete, ADV-042 remains open pending receiver-ingress integration and joined validation, and Rob's next bounded implementation-goal decision is pending. Real Worker activation, recurring Worker authority generation, Package E, and unrelated expansion remain deferred.