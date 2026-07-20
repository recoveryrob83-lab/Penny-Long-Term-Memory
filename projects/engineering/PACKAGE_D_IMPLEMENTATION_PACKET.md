# Package D Implementation Packet

Updated: 2026-07-19
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal
Record Class: Engineering implementation packet

## Objective

Implement the smallest reliable technical runtime required by:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- `coordination/WORKER_EXECUTION_CONTRACT.md`;
- ADV-20260718-042;
- Rob's approved v1 routing and verification decisions.

Engineering owns the machinery. Life OS Maintenance owns the canonical governance contracts and profile convention. Department HQs own Worker profiles and authority.

## V1 Design Decisions

### Stable registry configuration

Each registered Worker has:

- `worker_id`;
- exact `chat_title`;
- `owning_department`;
- department-owned `profile_path`;
- `profile_version`;
- persistent specialization;
- `role: worker`;
- Engineering-owned `deployment_state`.

Allowed deployment states:

- `enabled`;
- `paused`;
- `retired`.

The registry does not duplicate the department profile's authority text.

### Runtime state

Runtime observation remains separate from stable configuration.

Worker route state contains:

- `worker_id`;
- route availability;
- last-seen time when available;
- pause reason when applicable.

Allowed route-availability values:

- `available`;
- `unavailable`;
- `ambiguous`;
- `unknown`.

Receiver revision state is keyed by both `worker_id` and `task_id`. One global revision counter per Worker is prohibited because it could suppress unrelated tasks.

### Execution envelope

The compact execution wrapper contains:

- `wrapper_id`;
- `run_id`;
- target `worker_id`;
- authoritative `task_id`;
- `task_revision`;
- `procedure_id`;
- `procedure_version`;
- `authorization_source`;
- `verification_mode`.

The envelope is a routing and validation wrapper, not a replacement copy of the advisory, profile, procedure, or source records.

### Idempotency

The v1 idempotency key is:

`worker_id + task_id + task_revision`

A retry may use a new `run_id`, but a new run ID does not create new authority or permit repeat execution of an already accepted revision.

### Exact-title routing

- zero exact title matches: fail closed;
- one exact enabled title match: continue;
- more than one exact title match: fail closed;
- paused or retired match: fail closed.

No fuzzy Worker-title routing is permitted.

### Composer witness

The Worker-only composer witness is:

- preserve exact destination, empty-composer, clipboard-restoration, explicit-send, and stop-on-uncertainty safeguards;
- after paste, copy the composer once;
- confirm the copied text contains the expected `wrapper_id`;
- otherwise fail closed.

Full-text equality, repeated composer selection, character-range comparison, and multiple write witnesses are not part of v1.

## Implementation Sequence

### Slice 1: Contracts and validation

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime.py`.

Provides:

- registry-entry validation;
- route-state and receiver-state contracts;
- compact execution-envelope validation;
- exact-title resolution;
- stale-revision and duplicate suppression checks;
- wrapper-ID composer witness helper.

### Slice 2: SQLite persistence

Status: Core persistence implemented and locally validated. Execution-history linkage is implemented and validated in Slice 4.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_store.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_store.py`.

Provides separate SQLite tables for:

- Worker registry configuration;
- Worker route state;
- receiver state keyed by `worker_id` plus `task_id`.

The store:

- keeps deployment and route availability separate;
- enforces unique Worker IDs, chat titles, and profile paths;
- requires a registered Worker before route or receiver state can be written;
- atomically accepts only newer task revisions;
- records the accepted `run_id` without allowing a retry ID to recreate authority;
- does not overload saved prompts or scheduled-job definitions with Worker authority.

### Slice 3: Registry service

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_service.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_service.py`.

Provides:

- registration of one already-authorized Worker entry;
- registry listing and stable-ID lookup;
- exact-title resolution;
- controlled `enabled`, `paused`, and `retired` deployment changes;
- route-state updates;
- fail-closed unknown-route behavior;
- envelope validation without mutation;
- validated atomic envelope acceptance.

No department profile is created or modified by the registry service.

### Validation evidence through Slice 3

The combined focused contract, persistence, and service suite contains 25 tests. Rob reported that the requested focused Worker-runtime tests and full dashboard suite passed in the local dashboard checkout before Slice 4 began.

### Slice 4: Execution-envelope integration

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_command_center.py`;
- `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`;
- `apps/lifeos-dashboard/tests/test_worker_command_center.py`.

Provides:

- a separate `WorkerCommandJob` and `WorkerExecutionResult` path without changing ordinary HQ jobs;
- compact rendered prompts containing one machine-readable execution wrapper line;
- exact registered Worker title transport;
- shared Command Center pause state and one-job lock;
- manual and scheduler-triggered execution methods for one already-authorized envelope;
- pre-transport registry, deployment, route, receiver-revision, and duplicate checks;
- successful-send suppression by `worker_id + task_id + task_revision`;
- bounded retry after failed transport because failed sends do not create successful idempotency evidence;
- nullable Worker metadata columns in the existing SQLite `execution_history` table;
- persisted wrapper, run, Worker, task, revision, procedure, authorization, idempotency, verification-mode, trigger, and future controlled-outcome fields;
- legacy HQ execution-history compatibility;
- a Worker-only automation entrypoint that copies the composer once after paste and checks only the expected wrapper marker.

Validation evidence:

- four focused Worker-runtime files passed with `36 passed`;
- the first full regression run reached `172 passed` with two pre-existing guidance-string assertion failures;
- Engineering repaired only those wording contracts: `Open Automation Logs` and `Nothing was sent`;
- both focused regression tests then passed;
- Rob reported the final full dashboard suite passed with `174 passed, 9 warnings in 173.76s`;
- no functional Slice 4 regression remained.

Current boundary:

- no Worker profile, registry entry, or real route is created by this slice;
- no Worker UI or dashboard controls are added;
- no recurring Worker authority schedule is introduced;
- `execute_scheduled` accepts one already-authorized execution-ready envelope from a scheduler caller;
- existing HQ destinations, prompts, schedules, and verification behavior remain unchanged.

### Slice 5: Receiver validation and outcomes

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_models.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`;
- `apps/lifeos-dashboard/tests/test_worker_receiver.py`.

Architecture:

- semantic preflight is separate from execution outcome finalization;
- a valid wrapper becomes `READY`, not `IMPLEMENT`;
- receiver acceptance consumes the task revision only after semantic validation succeeds;
- acceptance and revision consumption are atomic with the existing transport-history row;
- invalid preflight records either `REPORT_AND_HOLD` or `ELEVATE_FOR_APPROVAL` without consuming the revision;
- finalization records exactly one controlled outcome in the same `execution_history` row;
- transport success never becomes implementation success by implication.

Preflight validates:

- registered Worker ID, profile Worker ID, profile version, owning department, and target department;
- exact canonical procedure ID, version, task class, and checksum;
- exact caller-to-task-class authority;
- allowed and prohibited task classes;
- authorization class and approval references;
- parameter checksum, required fields, unknown fields, and parameter types;
- authoritative source references;
- requested read and write scopes;
- profile-approved and procedure-approved tools;
- exact verification mode;
- deployment, route, pause, stale-revision, and duplicate state;
- material transport text that changes scope, destination, permanence, permissions, or requested action.

Finalization validates:

- actual completion state;
- required evidence references;
- truthful external-action verification;
- actual read and write scopes against both assignment and profile authority;
- actual tools against the authorized assignment;
- `AUTOMATIC` machine-verifiable postconditions;
- newly discovered authority or approval requirements.

Controlled outcomes:

- `IMPLEMENT` only when bounded work completed and required evidence was recorded;
- `REPORT_AND_HOLD` for invalid authority, partial or failed work, missing evidence, unavailable verification, scope or tool expansion, stale delivery, or unresolved conflicts;
- `ELEVATE_FOR_APPROVAL` when Rob must authorize new authority, spending, connectors, cross-department scope, a material exception, or newly discovered approval-bearing work.

Persistence added to the existing execution-history row:

- profile version and owning department;
- task class and authorization class;
- procedure and parameter checksums;
- source references;
- requested and actual scopes;
- accepted timestamp and receiver reason;
- completion and verification states;
- evidence references;
- actual tools;
- external-action verification;
- final controlled outcome.

Validation evidence:

- the focused receiver suite passed with `22 passed`;
- Rob reported the complete dashboard regression suite passed with `196 passed, 9 warnings in 191.97s`;
- no Slice 5 functional regression remained.

Current boundary:

- normalized profile authority is supplied as an input to the receiver; no competing profile parser or authority source was invented;
- no department Worker profile or folder was created;
- no real Worker was registered or activated;
- no Worker UI or dashboard control was added;
- no recurring Worker authority schedule was created;
- no second run or outcome ledger was created.

### Slice 6: Verification views and wake suppression

Status: Implemented in source, pending Rob's focused and full local validation.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_verification.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_verification_runtime.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/__init__.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/tabs.js`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.js`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.css`;
- `apps/lifeos-dashboard/tests/test_worker_verification.py`;
- `apps/lifeos-dashboard/tests/test_worker_verification_runtime.py`;
- `apps/lifeos-dashboard/tests/test_automation_logs_ui.py`.

Architecture:

- the existing `execution_history` row remains the sole durable run, evidence, outcome, and verification record;
- no second queue table, queue service, or wake ledger is created;
- receiver machine-evidence state remains separate from Department HQ review state;
- verification state is exposed as `pending`, `verified`, or `rejected`;
- the existing Command Center status payload is enriched with a bounded Worker verification summary and records rather than adding another API family;
- Automation Logs remains read-only and now renders Worker identity, task revision, controlled outcome, verification mode, verification state, review route, wake target, and wake reason;
- an internal review method may mark `ROUTINE_BATCH` or `IMMEDIATE_HQ` implementation evidence `verified` or `rejected` in the same history row;
- `AUTOMATIC` verification may not be manually overridden and must come from the machine postcondition evidence;
- canonical `SOURCE_VERIFIED` or `CLOSED` state may be supplied by the authoritative caller to suppress further wakes without copying lifecycle truth into the run table.

Wake and queue mapping:

- `IMPLEMENT` plus verified `AUTOMATIC`: wake suppressed;
- `IMPLEMENT` plus unverified `AUTOMATIC`: fail-safe owning Department HQ wake;
- `IMPLEMENT` plus pending `ROUTINE_BATCH`: department review queue, no immediate desktop wake;
- verified `ROUTINE_BATCH`: queue removed and wake suppressed;
- pending `IMMEDIATE_HQ`: owning Department HQ wake;
- verified `IMMEDIATE_HQ`: repeat wake suppressed;
- `REPORT_AND_HOLD`: rejected verification state and owning Department HQ wake;
- `ELEVATE_FOR_APPROVAL`: rejected verification state and Chief of Staff HQ wake for Rob's decision;
- canonical `SOURCE_VERIFIED` or `CLOSED`: further wake suppressed.

Dashboard view:

- Worker outcome, pending, verified, rejected, and wake-required counters;
- Worker-verification and wake-routing filters;
- Worker and task facts inside the existing Automation Logs cards;
- searchable and copyable outcome, verification, queue, and wake evidence;
- no approval, review, send, or mutation controls.

Validation status:

- source and test files were read back from GitHub;
- the assistant container could not reach GitHub, so no repository-local test run was performed there;
- Rob's focused and complete local test runs remain the validation gate.

Current boundary:

- no real wake is emitted by Slice 6; it derives eligibility, target, and suppression only;
- no general Worker dashboard control surface is added;
- no Worker profile, real registry entry, or real route is created;
- no recurring Worker authority schedule is created;
- no canonical advisory lifecycle state is duplicated into SQLite;
- Slice 7 remains the synthetic end-to-end pilot.

### Slice 7: End-to-end pilot

Before activating a new real department Worker:

1. test one synthetic registry entry and fake route;
2. prove zero-match, duplicate-match, paused, stale-revision, and wrapper-mismatch failures;
3. prove one successful bounded run through persistent evidence;
4. verify no duplicate run occurs on retry;
5. only then activate one department-owned profile under the canonical contract.

## Out of Scope

This packet does not authorize:

- creating speculative Worker profiles or folders;
- migrating the grandfathered Raw Capture or Inventory packages;
- changing canonical governance contracts;
- fuzzy title matching;
- autonomous authority expansion;
- a new queue service;
- recurring Worker authority generation in v1;
- Package E;
- unrelated dashboard expansion;
- reopening the abandoned full-text composer-verification investigation.

## Completion Conditions

Package D reaches its first runtime milestone when:

- the registry and envelope schemas are persisted;
- one exact Worker route can be resolved safely;
- stale and duplicate revisions are suppressed;
- the wrapper ID is preserved through transport evidence;
- receiver validation returns one controlled outcome;
- focused and full repository tests pass;
- one synthetic end-to-end run is verified without activating a speculative real Worker.

## Next Action

Run the focused Slice 6 suite:

`python -m pytest -q tests\test_worker_verification.py tests\test_worker_verification_runtime.py tests\test_automation_logs_ui.py`

Then run the complete dashboard regression suite:

`python -m pytest -q tests`

If both pass, record Slice 6 as locally validated and begin Slice 7 with one synthetic registry entry and fake route. Do not activate a real Worker, create a real profile, emit a real wake, or add recurring Worker authority.