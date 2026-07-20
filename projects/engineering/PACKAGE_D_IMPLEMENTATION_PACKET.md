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

Engineering owns the machinery. Life OS Maintenance HQ owns canonical shared governance contracts and the profile convention. Department HQs own Worker profiles and authority.

Package D is not complete merely because backend components and desktop transport work independently. Closure requires a production receiver-ingress path, authoritative source resolution, joined bounded evidence, and source-owner verification of ADV-20260718-042.

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

The envelope is a routing and validation wrapper, not a replacement copy of the advisory, profile, procedure, or source records. Its JSON representation is the sole authoritative machine transport representation.

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

- preserve exact destination, empty-composer protection, clipboard restoration, explicit send, and stop-on-uncertainty safeguards;
- after paste, copy the composer once;
- confirm the copied text contains the expected `wrapper_id`;
- otherwise fail closed.

Full-text equality, repeated composer selection, character-range comparison, and multiple write witnesses are not part of v1.

### Receiver transport integrity

Receiver acceptance requires exactly one existing transport-history row for the envelope `run_id`.

That row must prove:

- `status = succeeded`;
- `mode = send`;
- `prompt_type = worker`;
- exact matching `wrapper_id`;
- exact matching Worker, task, revision, procedure, authorization source, idempotency key, and verification mode.

Transport success is not inferred from a run ID alone.

### One durable execution record

The existing `execution_history` row remains the sole durable transport, receiver, outcome, evidence, and verification record.

Package D must not create a second:

- execution ledger;
- controlled-outcome ledger;
- verification ledger;
- queue ledger;
- wake ledger.

Views and wake decisions derive from the same row.

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

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_store.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_store.py`.

Provides separate SQLite tables for Worker registry configuration, route state, and receiver state keyed by `worker_id` plus `task_id`.

The store keeps deployment and route availability separate, enforces unique identities and paths, requires registration before state writes, and atomically accepts only newer task revisions.

### Slice 3: Registry service

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_service.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_service.py`.

Provides registration of one already-authorized Worker entry, registry lookup, exact-title resolution, controlled deployment changes, route updates, fail-closed unknown-route behavior, envelope validation without mutation, and atomic envelope acceptance.

No department profile is created or modified by the registry service.

### Slice 4: Execution-envelope integration

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_command_center.py`;
- `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`;
- `apps/lifeos-dashboard/tests/test_worker_command_center.py`.

Provides:

- separate Worker Command Center jobs and results without changing ordinary HQ jobs;
- compact machine-readable wrapper prompts;
- exact registered-title transport;
- shared pause state and one-job lock;
- manual and scheduler-triggered execution for one already-authorized envelope;
- successful-send suppression by idempotency key;
- bounded retry after failed transport;
- nullable Worker metadata in the existing `execution_history` table;
- legacy HQ history compatibility;
- Worker-only one-copy wrapper-marker verification.

Validation evidence:

- focused Worker-runtime suite: `36 passed`;
- final full suite after two narrow wording repairs: `174 passed, 9 warnings in 173.76s`.

### Slice 5: Receiver validation and controlled outcomes

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_models.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`;
- `apps/lifeos-dashboard/tests/test_worker_receiver.py`.

Architecture:

- semantic preflight is separate from execution outcome finalization;
- a valid wrapper becomes `READY`, not `IMPLEMENT`;
- receiver acceptance consumes the task revision only after transport and semantic validation succeed;
- acceptance and revision consumption are atomic with the existing transport-history row;
- invalid preflight records `REPORT_AND_HOLD` or `ELEVATE_FOR_APPROVAL` without consuming the revision;
- finalization records exactly one controlled outcome in the same row;
- transport success never becomes implementation success by implication.

Preflight validates identity, department ownership, caller authority, procedure identity and checksum, task class, parameters, source references, requested scopes, approved tools, verification mode, deployment, route, pause, revision freshness, and caller-reported material transport drift.

Finalization validates completion, evidence, external-action truthfulness, actual scopes and tools, machine postconditions, and newly discovered approval needs.

Controlled outcomes:

- `IMPLEMENT`;
- `REPORT_AND_HOLD`;
- `ELEVATE_FOR_APPROVAL`.

Validation evidence:

- focused receiver suite: `22 passed`;
- full suite: `196 passed, 9 warnings in 191.97s`.

### Slice 6: Verification views and wake suppression

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_verification.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_verification_runtime.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/tabs.js`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.js`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/automation-logs.css`;
- related focused tests.

Architecture:

- the existing `execution_history` row remains the sole durable run, evidence, outcome, and verification record;
- machine-evidence state remains separate from Department HQ review state;
- verification state is exposed as `pending`, `verified`, or `rejected`;
- the existing Command Center status payload is enriched rather than creating another API family;
- Automation Logs remains read-only;
- `AUTOMATIC` verification cannot be manually overridden;
- canonical source lifecycle state may suppress further wakes without duplicating lifecycle truth into SQLite.

Wake and queue mapping:

- verified `AUTOMATIC`: wake suppressed;
- unverified `AUTOMATIC`: owning Department HQ wake;
- pending `ROUTINE_BATCH`: department review queue, no immediate wake;
- verified `ROUTINE_BATCH`: queue removed and wake suppressed;
- pending `IMMEDIATE_HQ`: owning Department HQ wake;
- verified `IMMEDIATE_HQ`: repeat wake suppressed;
- `REPORT_AND_HOLD`: owning Department HQ wake;
- `ELEVATE_FOR_APPROVAL`: Chief of Staff HQ wake for Rob's decision.

Validation evidence:

- focused verification/runtime/Automation Logs suite: `20 passed`;
- full suite: `212 passed, 9 warnings in 198.41s`.

### Slice 7: Synthetic end-to-end backend pilot

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/tests/test_worker_end_to_end_pilot.py`;
- transport-integrity hardening in `worker_receiver.py` and `worker_receiver_store.py`;
- receiver regression coverage in `test_worker_receiver.py`.

Pilot construction:

- one synthetic Worker registry entry;
- one fake exact-title route;
- one synthetic authority profile;
- one synthetic canonical procedure;
- one synthetic task and execution envelope;
- one injected fake transport adapter;
- temporary SQLite databases and disposable fixtures only.

Pilot proof:

- zero and duplicate exact-title matches fail closed;
- paused deployment and unavailable route refuse before transport;
- missing wrapper witness fails transport and cannot consume a revision;
- corrupted successful transport metadata fails receiver validation;
- unauthorized scope records `REPORT_AND_HOLD` without consuming a revision;
- one successful transport becomes `READY`, then exactly one `IMPLEMENT` with same-row evidence and verification review;
- pending routine work enters the review queue without an immediate wake;
- verified routine work leaves the queue and suppresses repeat wakes;
- retry with a new `run_id` cannot re-execute the accepted task revision;
- a second controlled outcome is refused;
- no synthetic state survives outside temporary fixtures.

Validation evidence:

- focused pilot plus receiver regression suite: `32 passed`;
- full dashboard suite: `222 passed, 9 warnings in 238.78s`;
- no Slice 7 functional regression remained.

## Bounded Synthetic Desktop Transport Receipt

Status: Live validated by Rob on 2026-07-19.

Files:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`;
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`;
- `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`.

Bounded construction:

- fixed visible title `Synthetic_Worker_Pilot` inside the `Life OS` project;
- disposable `synthetic_desktop_worker` identity inside the wrapper only;
- unique synthetic wrapper, run, and task IDs;
- explicit instruction forbidding file, connector, calendar, email, task, dashboard, external-system, or durable-record action;
- draft-only default;
- send requires explicit synthetic confirmation;
- launcher creates no profile, registry entry, route record, schedule, wake, or durable authority.

Live evidence:

- exact target resolved and active document verified;
- stable Group composer verified;
- wrapper `SYNTH-DESKTOP-WRAP-1784515664-0de7866901` pasted and copied once for marker verification;
- submission occurred only after explicit confirmation;
- machine receipt reported `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- Worker returned exact acknowledgement `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker authority was created.

## ADV-20260718-042 Verification Review

Status: Read-only Engineering review complete. Advisory remains OPEN under its source owner.

Implemented evidence satisfies the component-level requirements for:

- recognizable machine-readable wrapper transport;
- persisted envelope identity and checksums;
- exact successful-send transport validation;
- profile, ownership, caller, task-class, procedure, parameter, scope, tool, and verification-mode enforcement;
- duplicate and stale-revision suppression;
- controlled outcomes;
- same-row evidence and verification review.

Two closure gaps remain.

### Gap 1: Receiver ingress and canonical resolution

The current receiver service validates supplied `ReceiverAssignment`, `WorkerAuthorityProfile`, and `CanonicalProcedureSpec` objects. The production path does not yet demonstrate that it:

1. parses transported or persisted wrapper evidence;
2. resolves the registered Worker;
3. loads the department-owned authoritative profile;
4. resolves the canonical procedure by ID and version;
5. resolves the authoritative task or advisory source and parameters;
6. constructs `ReceiverAssignment` internally;
7. derives material transport drift instead of trusting a caller-supplied Boolean;
8. invokes the existing semantic receiver only after those resolutions succeed.

The ingress layer must resolve authority but never invent or duplicate it.

### Gap 2: Joined physical end-to-end proof

The backend pilot validates the complete receiver and verification pipeline using injected transport. The physical desktop pilot validates actual ChatGPT Classic transport and acknowledgement but intentionally performs no receiver acceptance or controlled outcome.

Package D still needs one bounded, non-authoritative proof connecting:

physical transport -> persisted transport evidence -> authoritative resolution -> receiver acceptance -> one controlled outcome -> evidence persistence -> verification review.

## Planned Human-Readable Envelope Follow-up

Before the first real Worker activation, add a display-only human-readable summary beside the canonical compact JSON envelope.

The summary must:

- derive every field from the same `ExecutionEnvelope` object;
- show Worker, task and revision, procedure and version, authorization source, verification mode, wrapper ID, run ID, and bounded instruction;
- remain non-authoritative;
- have no independent edit path, parser, persistence record, or lifecycle state;
- be covered by parity tests.

The summary does not replace or parse back into authority.

## Current Boundary

Package D does not authorize:

- a real Worker profile or folder;
- a real registry entry or route;
- a real desktop wake;
- a recurring Worker authority schedule;
- a general Worker dashboard control surface;
- a second run, outcome, queue, wake, or verification ledger;
- Package E;
- autonomous authority expansion;
- migration of grandfathered Worker packages;
- reopening the paused general full-text composer investigation.

Backend and desktop transport success prove substantial technical readiness. They do not create operational authority or complete the receiver-ingress seam.

## Next Decision

Rob must separately select one bounded next implementation goal.

Engineering recommendation:

1. receiver ingress and canonical resolution;
2. joined bounded end-to-end validation;
3. human-readable envelope summary, either as a small follow-up after ingress or immediately before the first real activation;
4. source-owner verification and closure review for ADV-20260718-042;
5. only then consider at most one department-owned Worker for separately authorized profile and activation review.

Before any real Worker write, establish:

- record class;
- one owner;
- authoritative department-owned profile path;
- canonical lifecycle state and separate priority;
- allowed task class;
- read and write scopes;
- approved tools;
- verification mode;
- smallest useful next action;
- completion, rejection, and review conditions;
- why GitHub is the correct system;
- the statement or standing rule authorizing the write.

No real profile, registry entry, route, wake, recurring authority schedule, Package E work, or next implementation slice may proceed from this packet alone.