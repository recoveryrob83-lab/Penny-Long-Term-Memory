# Engineering HQ Session Handoff

Updated: 2026-07-19
Project: Engineering HQ
Purpose: Current handoff for technical architecture, Package D Worker-runtime implementation, desktop automation, connector reliability, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Backend and Desktop Milestone Complete and Worker Activation Decision Gate
- Primary Systems: GitHub, local LifeOS Dashboard, SQLite Command Center history, Engineering advisory board, Advisory Index, and other source systems only when explicitly required
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` when Package D or Worker activation is in scope.
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

Status: Backend and physical desktop transport milestone complete. Slices 1–7 are implemented and locally validated, and one bounded synthetic wrapper passed through ChatGPT Classic with exact acknowledgement. The next valid action is a separate activation decision, not automatic Worker deployment.

Canonical implementation packet:

- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`

Canonical governance and authorization references:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- ADV-20260718-042 on `coordination/boards/main-assistant.md`

Implemented and locally validated slices:

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
5. Worker receiver validation and controlled outcomes:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_models.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`
   - `apps/lifeos-dashboard/tests/test_worker_receiver.py`
6. Worker verification views and wake suppression:
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_verification.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/worker_verification_runtime.py`
   - `apps/lifeos-dashboard/lifeos_dashboard/static/tabs.js`
   - `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.js`
   - `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.css`
   - `apps/lifeos-dashboard/tests/test_worker_verification.py`
   - `apps/lifeos-dashboard/tests/test_worker_verification_runtime.py`
   - `apps/lifeos-dashboard/tests/test_automation_logs_ui.py`
7. Synthetic end-to-end pilot:
   - `apps/lifeos-dashboard/tests/test_worker_end_to_end_pilot.py`
   - exact transport-history validation in `worker_receiver.py` and `worker_receiver_store.py`

Bounded desktop validation:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`
- existing exact-title Worker transport in `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`

Current capabilities:

- stable Worker IDs and exact visible titles;
- department profile pointers with Engineering-owned deployment state kept outside profiles;
- `enabled`, `paused`, and `retired` deployment states;
- separate route availability;
- exact-title zero-match and duplicate-match failure;
- compact JSON execution envelopes;
- task-scoped receiver revisions;
- idempotency by `worker_id + task_id + task_revision`;
- separate manual and scheduler-triggered Worker execution methods;
- shared Command Center pause and one-job lock;
- successful-send duplicate suppression while failed transport remains eligible for bounded retry;
- existing execution-history linkage for wrapper, run, Worker, task, revision, procedure, authorization, idempotency, verification mode, trigger, receiver evidence, controlled outcome, and verification review;
- one-copy Worker composer verification by expected `wrapper_id` only;
- receiver acceptance requiring exactly one successful Worker send with exact matching transport-envelope metadata;
- semantic receiver validation for profile identity/version, owning department, exact calling authority, procedure/version/checksum, parameters, sources, scopes, tools, verification mode, pause state, and revision freshness;
- atomic receiver acceptance only after transport and semantic validation both succeed;
- evidence-backed finalization with exactly one `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL` outcome;
- derived `pending`, `verified`, and `rejected` verification states without a second queue ledger;
- queue eligibility, wake targeting, and wake suppression derived from the same execution-history row;
- read-only Automation Logs counters, filters, Worker facts, and wake evidence;
- no real wake emission or dashboard mutation controls;
- a disposable synthetic integration harness proving the backend pipeline without durable real-world authority;
- a successful bounded live wrapper proving exact ChatGPT Classic navigation, stable composer verification, explicit send, receipt generation, and exact acknowledgement.

Validation state:

- the four focused Worker-runtime files passed with `36 passed`;
- the first Slice 4 full suite reached `172 passed` with two guidance-string assertion failures;
- Engineering repaired only the `Open Automation Logs` and `Nothing was sent` wording contracts;
- both focused regressions passed;
- the Slice 4 full suite passed with `174 passed, 9 warnings in 173.76s`;
- the focused Slice 5 receiver suite passed with `22 passed`;
- the Slice 5 full suite passed with `196 passed, 9 warnings in 191.97s`;
- the focused Slice 6 verification/runtime/Automation Logs suite passed with `20 passed`;
- the Slice 6 full suite passed with `212 passed, 9 warnings in 198.41s`;
- the focused Slice 7 end-to-end pilot and receiver suite passed with `32 passed`;
- Rob reported the complete dashboard suite passed with `222 passed, 9 warnings in 238.78s`;
- Slices 1–7 are locally validated with no remaining functional regression;
- Rob reported live desktop receipt `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- the synthetic Worker returned exact acknowledgement `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker profile, registry entry, route, wake, UI mutation control, or recurring Worker authority schedule has been created.

Synthetic proof:

- zero and duplicate exact-title resolution fail closed;
- paused deployment and unavailable route refuse before transport;
- missing wrapper witness fails transport and cannot consume authority;
- corrupted persisted transport metadata fails receiver validation;
- unauthorized scope records `REPORT_AND_HOLD` without revision consumption;
- one successful backend run traverses transport, `READY`, `IMPLEMENT`, evidence persistence, routine verification review, and wake suppression in one row;
- retry with a new `run_id` cannot re-execute the accepted revision;
- a second controlled outcome is refused;
- temporary databases and fixtures isolate backend synthetic state;
- the live desktop wrapper traversed exact UI transport and semantic acknowledgement without durable authority.

Next valid Engineering action:

1. stop at the validated backend-and-desktop milestone and gather evidence from the grandfathered pilots; or
2. select at most one candidate department-owned Worker for a separately authorized profile and activation review;
3. do not create a real Worker profile, registry entry, route, wake, or schedule without separate authorization from Rob and the owning department;
4. if a real candidate is considered, establish its record class, owner, authoritative profile path, lifecycle state, priority, task class, scopes, verification mode, review condition, and why GitHub is correct before any durable write;
5. keep recurring Worker authority generation and Package E deferred.

## Composer Boundary

The general full-text composer investigation is paused by Rob and must not be reopened without demonstrated failure.

The Worker-only path preserves exact destination, empty-composer, clipboard-restoration, explicit-send, one-job, and stop-on-uncertainty safeguards. After paste it copies once and checks only whether the expected `wrapper_id` is present.

Full-text equality, repeated selection, character-range comparison, multiple witnesses, alternate paste mechanisms, focus hacks, and broader timeout experiments are out of scope.

## Automation Command Center Boundary

The established HQ scheduler and attended automation remain operationally validated. The separate Worker backend, receiver, verification, synthetic integration, and bounded desktop transport paths are validated.

Package D does not:

- change existing HQ destinations or prompt behavior;
- add general Worker execution controls;
- create real Worker registry entries;
- create department profiles;
- create recurring Worker authority schedules;
- create a second run, outcome, queue, wake, or verification ledger;
- emit a real wake;
- authorize a real Worker merely because tests or a synthetic desktop transport passed.

The scheduler adapter accepts one already-authorized execution-ready envelope. Correct recurring authority generation requires a separate approved model and is not inferred from ordinary recurrence.

Any real profile and activation remain department-owned durable decisions.

## Advisory State

As of 2026-07-19:

- ADV-20260718-042 is OPEN and authoritative for receiver-side semantic validation and controlled Worker outcomes. Engineering implementation and local tests now exist; source verification and lifecycle changes remain with the advisory owner.
- ADV-20260719-043 is CLOSED after Life OS Maintenance created the canonical execution and Worker protocols.
- ADV-20260719-044 is OPEN on `coordination/boards/engineering.md`, targeted to Life OS Maintenance HQ for shared Worker filesystem, pointer, profile-state, handoff, watch, and architecture-history reconciliation.

Do not duplicate these advisories or create parallel open-loop wrappers.

## Other Active Tracks

- Monitor ADV-20260719-044 and observe corrected role-routed boots before closing the department-ownership wrapper.
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

## Safety and Truthfulness

- Prefer small, verifiable operations.
- Fetch before editing and verify after writing.
- Preserve unrelated content and source boundaries.
- Never commit secrets or private account data.
- Never claim local runtime success without Rob's confirmation.