# Engineering HQ Session Handoff

Updated: 2026-07-19
Project: Engineering HQ
Purpose: Current handoff for technical architecture, Package D Worker-runtime implementation, desktop automation, connector reliability, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Worker Runtime and Receiver Validation
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center history, Engineering advisory board, Advisory Index, and other source systems only when explicitly required
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` when Package D is in scope.
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

## Highest-Priority Work Package

### Package D: Operations-Procedure and Worker-Runtime Implementation

Status: Active.

Canonical implementation packet:

- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`

Canonical governance and authorization references:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- ADV-20260718-042 on `coordination/boards/main-assistant.md`

Implemented slices:

1. Worker contracts and validation:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime.py`
   - `apps/lifeos-dashboard/tests/test_worker_runtime.py`
2. Worker registry, route, and task-scoped receiver persistence:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_store.py`
   - `apps/lifeos-dashboard/tests/test_worker_runtime_store.py`
3. Worker registry service:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_service.py`
   - `apps/lifeos-dashboard/tests/test_worker_runtime_service.py`
4. Worker Command Center execution path:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_command_center.py`
   - `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`
   - `apps/lifeos-dashboard/tests/test_worker_command_center.py`

Current source capabilities:

- stable Worker IDs and exact visible titles;
- department profile pointers with Engineering-owned deployment state kept outside profiles;
- `enabled`, `paused`, and `retired` deployment states;
- separate route availability;
- exact-title zero-match and duplicate-match failure;
- compact execution envelopes;
- task-scoped receiver revisions;
- idempotency by `worker_id + task_id + task_revision`;
- separate manual and scheduler-triggered Worker execution methods;
- shared Command Center pause and one-job lock;
- successful-send duplicate suppression while failed transport remains eligible for bounded retry;
- existing execution-history linkage for wrapper, run, Worker, task, revision, procedure, authorization, idempotency, verification mode, trigger, and future controlled outcome;
- one-copy Worker composer verification by expected `wrapper_id` only.

Validation state:

- Rob reported the Slice 1–3 focused tests and full dashboard suite passed locally.
- Slice 4 adds 11 focused tests and awaits Rob's focused and full local validation.
- No real Worker profile, registry entry, route, UI, or recurring Worker authority schedule has been created.

Next valid Engineering action:

1. run the four focused Worker-runtime test files;
2. run the full dashboard suite;
3. if both pass, begin Slice 5 receiver-side profile, authority, scope, parameter, verification-mode, and duplicate validation;
4. persist exactly one controlled outcome: `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL`;
5. keep Worker UI and real profile activation deferred until the synthetic pilot.

## Composer Boundary

The general full-text composer investigation is paused by Rob and must not be reopened without demonstrated failure.

The Worker-only path preserves exact destination, empty-composer, clipboard-restoration, explicit-send, one-job, and stop-on-uncertainty safeguards. After paste it copies once and checks only whether the expected `wrapper_id` is present.

Full-text equality, repeated selection, character-range comparison, multiple witnesses, alternate paste mechanisms, focus hacks, and broader timeout experiments are out of scope.

## Automation Command Center Boundary

The established HQ scheduler and attended automation remain operationally validated.

Slice 4 adds backend Worker execution only. It does not:

- change existing HQ destinations or prompt behavior;
- add Worker dashboard UI;
- create real Worker registry entries;
- create department profiles;
- create recurring Worker authority schedules;
- process receiver outcomes yet.

The scheduler adapter accepts one already-authorized execution-ready envelope. Correct recurring authority generation requires a separate approved model and is not inferred from ordinary recurrence.

## Advisory State

As of 2026-07-19:

- ADV-20260718-042 is OPEN and authoritative for receiver-side semantic validation and controlled Worker outcomes.
- ADV-20260719-043 is CLOSED after Life OS Maintenance created the canonical execution and Worker protocols.
- ADV-20260719-044 is OPEN on `coordination/boards/engineering.md`, targeted to Life OS Maintenance HQ for shared Worker filesystem, pointer, profile-state, handoff, watch, and architecture-history reconciliation.

Do not duplicate these advisories or create parallel open-loop wrappers.

## Other Active Tracks

- Monitor ADV-20260719-044 and observe corrected role-routed boots before closing the department-ownership wrapper.
- Observe four-source dashboard behavior during ordinary use.
- Continue Raw Capture and Inventory pilots only as grandfathered evidence sources.
- Align the Reliable Connector Execution Layer, operation ledger, and connector-health policy with the new envelope and evidence model.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Production Boundary

- ChatGPT Classic must be responsive for UI automation.
- Failed scheduled runs pause rather than retry blindly.
- Do not activate a speculative real Worker before the synthetic end-to-end pilot passes.
- Do not create recurring Worker authority schedules without an approved task-generation model.
- Do not begin Package E or unrelated automation expansion while Package D remains active.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Preserve unrelated content and source boundaries.
- Never commit secrets or private account data.
- Never claim local runtime success without Rob's confirmation.