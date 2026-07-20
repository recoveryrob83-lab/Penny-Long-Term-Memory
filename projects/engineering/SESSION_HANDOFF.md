# Engineering HQ Session Handoff

Updated: 2026-07-19
Project: Engineering HQ
Purpose: Current handoff for technical architecture, Package D Worker-runtime implementation, desktop automation, connector reliability, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Backend and Desktop Milestone Complete / ADV-042 Receiver-Ingress Gap Identified / Next Implementation-Goal Decision Pending
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center history, Engineering advisory board, Advisory Index when needed, and other source systems only when explicitly required
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` when Package D, ADV-20260718-042, or Worker activation is in scope.
7. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker routing, authority, or execution behavior is in scope.
8. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
9. Read current Engineering notebook records only when directly referenced by active work.
10. Keep connector work small, explicit, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, prompt systems, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own the canonical shared Worker contract, global boot coherence, profile convention, or department-specific Worker authority. Life OS Maintenance HQ owns those governance surfaces. Departments own their Worker profiles and authority. Engineering owns the technical registry, transport, validation, receiver state, duplicate suppression, verification mechanics, runtime evidence, tests, and reliability required to enforce the approved architecture.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared governance and global memory hygiene to Life OS Maintenance HQ, and wellbeing or sustainability judgment to Wellness HQ.

## Chat and Work Model

Use regular Chat for architecture, planning, GitHub synchronization, prompt work, debugging analysis, advisories, and bounded connector updates.

Use Work for substantial coding, local terminal work, full test execution, desktop control, packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without current evidence.

## Primary Current Work Package

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Active
Priority: Normal

Status: Backend and physical desktop transport milestone complete. Slices 1–7 are implemented and locally validated, and one bounded synthetic wrapper passed through ChatGPT Classic with exact acknowledgement. ADV-20260718-042 remains open because a read-only Engineering verification identified a receiver-ingress integration gap and a missing joined physical end-to-end proof.

Canonical implementation packet:

- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`

Canonical governance and authorization references:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- ADV-20260718-042 on `coordination/boards/main-assistant.md`

Implemented slices:

1. Worker contracts and validation.
2. Worker registry, route, and task-scoped receiver persistence.
3. Worker registry service.
4. Separate Worker Command Center execution path.
5. Receiver semantic validation and controlled outcomes.
6. Verification views, queue derivation, and wake suppression.
7. Disposable synthetic end-to-end backend pilot with transport-integrity hardening.

Bounded desktop validation:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`
- exact-title Worker transport in `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`

Current capabilities:

- stable Worker IDs and exact visible titles;
- department profile pointers with Engineering-owned deployment state outside profiles;
- separate route availability;
- compact JSON execution envelopes;
- task-scoped receiver revisions and idempotency;
- shared Command Center pause and one-job lock;
- successful-send duplicate suppression with bounded retry after failed transport;
- one-copy Worker composer verification by expected `wrapper_id`;
- receiver acceptance requiring one exact successful Worker transport row;
- semantic validation for profile identity, ownership, caller authority, procedure and parameter checksums, source references, scopes, tools, verification mode, and revision freshness;
- atomic receiver acceptance after transport and semantic validation;
- exactly one evidence-backed `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL` outcome;
- same-row verification review, queue derivation, wake targeting, and wake suppression;
- read-only Automation Logs visibility;
- no real wake emission or Worker mutation controls.

Validation state:

- focused Slice 7 and receiver suite: `32 passed`;
- complete dashboard regression suite reported by Rob: `222 passed, 9 warnings in 238.78s`;
- live desktop receipt reported `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- exact acknowledgement: `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker profile, registry entry, route, wake, UI mutation control, or recurring Worker authority schedule was created.

## ADV-042 Verification Finding

Engineering completed a separate read-only verification against ADV-20260718-042.

Substantial implementation is present, including transport metadata validation, semantic preflight, checksum and schema validation, ownership and scope enforcement, duplicate suppression, controlled outcomes, evidence persistence, and verification review.

Two closure gaps remain:

1. Production receiver ingress and canonical resolution: the runtime does not yet demonstrate a path that parses transported wrapper evidence and independently resolves the authoritative Worker profile, canonical procedure, and task source before constructing `ReceiverAssignment`.
2. Joined physical end-to-end proof: the backend pilot uses injected transport, while the physical desktop pilot intentionally stops after transport and acknowledgement. One bounded proof has not yet joined physical transport to receiver acceptance, outcome, evidence, and verification.

Recommended implementation order, subject to Rob's decision:

1. receiver ingress and canonical resolution;
2. human-readable display-only envelope summary;
3. source-owner verification of ADV-042 and Package D closure review;
4. only then consider one separately authorized real Worker activation.

This recommendation is not itself activation authority or a selected implementation goal.

## Planned Production Readability Follow-up

Before the first real Worker activation, preserve the compact JSON envelope as the sole authoritative machine representation and add a generated human-readable summary beside it.

The summary must:

- derive every displayed field from the same `ExecutionEnvelope` object used to render JSON;
- show Worker, task and revision, procedure and version, authorization source, verification mode, wrapper ID, run ID, and bounded instruction in plain language;
- remain display-only and non-authoritative;
- have no independent edit path, parser, persistence record, or lifecycle state;
- be covered by focused field-parity tests.

## Composer Boundary

The general full-text composer investigation is paused by Rob and must not be reopened without demonstrated failure.

The Worker-only path preserves exact destination, empty-composer protection, clipboard restoration, explicit send, one-job locking, and stop-on-uncertainty safeguards. After paste it copies once and checks only whether the expected `wrapper_id` is present.

Full-text equality, repeated selection, character-range comparison, multiple witnesses, alternate paste mechanisms, focus hacks, and broader timeout experiments are out of scope.

## Advisory State

As of 2026-07-19:

- ADV-20260718-042 is OPEN and authoritative for receiver-side semantic validation and controlled Worker outcomes. Engineering implementation is substantial, but source verification and lifecycle changes remain with the advisory owner after the identified gaps are resolved.
- ADV-20260719-043 is CLOSED after Life OS Maintenance created the canonical execution and Worker protocols.
- ADV-20260719-044 is CLOSED, implemented, and source verified after Life OS Maintenance reconciled shared Worker filesystem, pointer, profile-state, handoff, watch, and architecture-history drift.

Do not duplicate these advisories or create parallel open-loop wrappers.

## Other Active Tracks

- Observe corrected role-routed specialist boots and inspect demonstrated defects. Do not continue monitoring ADV-20260719-044 implementation.
- Observe four-source dashboard behavior during ordinary use.
- Continue Raw Capture and Inventory pilots only as grandfathered evidence sources.
- Align the Reliable Connector Execution Layer, operation ledger, and connector-health policy with the validated envelope, evidence, controlled-outcome, verification-state, wake-suppression, transport-integrity, and desktop-receipt model.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Production Boundary

- ChatGPT Classic must be responsive for UI automation.
- Failed scheduled runs pause rather than retry blindly.
- Package D backend and desktop validation do not authorize a real Worker, profile, route, wake, recurring authority schedule, or Package E.
- Any real activation requires a separate bounded decision and source-owned profile authority.
- Do not create recurring Worker authority schedules without an approved task-generation model.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Next Valid Action

Have Rob select one bounded next implementation goal. Engineering recommends receiver ingress and canonical resolution before envelope readability or real Worker activation, but no implementation is authorized merely by this handoff.