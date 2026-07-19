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

Status: Core persistence implemented and locally validated. Execution-history linkage is implemented in Slice 4.

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

Status: Backend implementation complete in source, pending Rob's focused and full local validation.

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

Current boundary:

- no Worker profile, registry entry, or real route is created by this slice;
- no Worker UI or dashboard controls are added;
- no recurring Worker authority schedule is introduced;
- `execute_scheduled` accepts one already-authorized execution-ready envelope from a scheduler caller;
- receiver acceptance and canonical Worker outcomes remain Slice 5;
- `controlled_outcome` remains null until a receiver result is processed;
- existing HQ destinations, prompts, schedules, and verification behavior remain unchanged.

### Slice 5: Receiver validation and outcomes

Validate at the receiving Worker boundary:

- correct Worker ID;
- current profile version;
- allowed task class;
- permitted read and write scope;
- required parameters and source references;
- verification mode;
- pause and duplicate state.

The Worker returns exactly one canonical outcome:

- `IMPLEMENT`;
- `REPORT_AND_HOLD`;
- `ELEVATE_FOR_APPROVAL`.

### Slice 6: Verification views

Reuse existing SQLite execution history and Automation Logs where practical.

A separate queue service is not required for v1. A filtered persisted verification state is sufficient:

- `pending`;
- `verified`;
- `rejected`.

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

Run:

`python -m pytest -q tests/test_worker_runtime.py tests/test_worker_runtime_store.py tests/test_worker_runtime_service.py tests/test_worker_command_center.py`

Then run:

`python -m pytest -q`

If both pass, begin Slice 5 by implementing receiver-side profile and authorization validation plus the three controlled outcomes, while keeping Worker UI and real profile activation deferred.