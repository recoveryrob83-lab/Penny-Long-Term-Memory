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

The future minimal composer write witness is:

- copy composer text once;
- confirm the copied text contains the expected `wrapper_id`;
- send only when normal destination, empty-composer, and explicit-send safeguards also pass;
- otherwise fail closed.

Full-text equality, repeated composer selection, character-range comparison, and multiple write witnesses are not part of v1.

## Implementation Sequence

### Slice 1: Contracts and validation

Status: Implemented in source, pending full repository validation.

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

Focused isolated evidence: 11 tests passed. The full repository suite was not run because the active execution container could not clone GitHub. Rob's local dashboard environment remains the required source for the complete test pass.

### Slice 2: SQLite persistence

Add small durable tables or equivalent migrations for:

- Worker registry configuration;
- Worker route state;
- receiver state keyed by `worker_id` plus `task_id`;
- wrapper, run, and idempotency evidence associated with execution history.

Do not overload saved prompts or scheduled-job definitions with Worker authority.

### Slice 3: Registry service

Add service methods for:

- listing registered Workers;
- registering or updating one authorized Worker entry;
- pausing and retiring routes;
- exact-title and stable-ID resolution;
- duplicate-title detection;
- profile-path and version validation.

No department profile is created or modified by the registry service.

### Slice 4: Execution-envelope integration

Integrate envelopes into manual and scheduled Command Center execution without removing existing HQ destinations.

Required behavior:

- preserve one `wrapper_id` and `run_id` per attempt;
- preserve the authoritative task and revision;
- validate authorization and target identity before transport;
- suppress stale and duplicate revisions;
- fail closed on missing, ambiguous, paused, retired, or unauthorized routes.

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

Run the new focused tests in Rob's local dashboard checkout, then implement Slice 2 by extending `CommandCenterStore` with minimal Worker registry, route-state, and task-scoped receiver-state persistence.