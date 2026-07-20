# Package D Implementation Packet

Updated: 2026-07-20
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal
Record Class: Engineering implementation packet

## Objective

Implement the smallest reliable combination of operational procedure and technical infrastructure required by:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
- `coordination/WORKER_EXECUTION_CONTRACT.md`;
- ADV-20260718-042;
- Rob's approved v1 routing and verification decisions.

Engineering owns the machinery. Life OS Maintenance HQ owns canonical shared governance contracts and the profile convention. Department HQs own Worker profiles, procedures, authority, and domain judgment.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The operational chain is:

1. a Department HQ or approved calling source authorizes one bounded assignment;
2. technical infrastructure transports a recognizable envelope to the exact Worker chat and records delivery evidence;
3. the Worker reads its department-owned profile and the named canonical procedure, prompt, task, advisory, or source record from GitHub;
4. the Worker validates identity, version, parameters, caller authority, ownership, scope, tools, procedures, and source boundaries;
5. the Worker performs only authorized work or refuses and reports the reason;
6. the Worker returns exactly one controlled outcome with run-linked evidence;
7. the owning Department HQ reviews the result and retains domain ownership.

Python, desktop automation, SQLite, and the dashboard are courier, routing, safety, duplicate-suppression, evidence, and visibility infrastructure. They are not the Worker.

Machine validation may provide useful defense in depth. It must not replace or silently assume the Worker’s operational source reading, judgment, refusal behavior, or Department HQ review.

## ADV-20260718-042 Interpretation

The advisory explicitly separates transport from receiver responsibility.

### Automation-layer responsibility

The automation layer must:

- deliver one recognizable bounded envelope to the intended destination;
- preserve correlation and transport evidence;
- log source, target, prompt or procedure identity, version, authorization reference, parameters, checksums, attempts, send action, retry count, and result;
- prevent duplicate delivery or execution under the approved idempotency model;
- avoid interpreting, editing, approving, truncating, or broadening the requested work;
- treat composer text and character counts as diagnostics rather than semantic proof.

### Receiving-Worker responsibility

The specialized ChatGPT Worker must:

- recognize and parse the envelope;
- resolve the named canonical prompt or procedure and its version from GitHub;
- load its department-owned profile and relevant authoritative task or advisory source;
- validate parameters and checksums where applicable;
- confirm that the caller may request the task class;
- confirm that the owning department owns the work;
- confirm authorization, approvals, procedures, and source-system boundaries;
- ignore harmless transport noise while refusing changes to scope, destination, permanence, permissions, or requested actions;
- preserve run, task or advisory, Worker, and profile identifiers in evidence;
- return `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`.

The earlier Engineering conclusion that Package D required a new autonomous Python receiver-ingress and canonical-resolution service overinterpreted the technical runtime. That is not currently a required closure condition.

## V1 Technical Design Decisions

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

Allowed route values:

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

The envelope is a routing and validation wrapper, not a replacement copy of the profile, procedure, advisory, task, or source record. Its JSON representation is the authoritative machine transport representation.

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

### Transport-history integrity

The technical receiver model requires exactly one existing successful transport-history row for the envelope `run_id` before backend acceptance.

That row must prove:

- `status = succeeded`;
- `mode = send`;
- `prompt_type = worker`;
- exact matching `wrapper_id`;
- exact matching Worker, task, revision, procedure, authorization source, idempotency key, and verification mode.

Transport success is not inferred from a run ID alone.

### One durable execution record

The existing `execution_history` row remains the sole durable transport, outcome, evidence, and verification record for the technical runtime.

Package D must not create a second:

- execution ledger;
- controlled-outcome ledger;
- verification ledger;
- queue ledger;
- wake ledger.

Views and wake decisions derive from the same row.

## Implemented Technical Slices

### Slice 1: Contracts and validation

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime.py`.

Provides registry-entry validation, route and receiver contracts, compact envelope validation, exact-title resolution, stale-revision and duplicate checks, and the wrapper-ID composer witness helper.

### Slice 2: SQLite persistence

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_store.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_store.py`.

Provides separate registry, route, and task-scoped receiver state while preserving stable authority outside the runtime database.

### Slice 3: Registry service

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_service.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_service.py`.

Provides registration of one already-authorized Worker entry, registry lookup, exact-title resolution, controlled deployment changes, route updates, fail-closed unknown-route behavior, envelope validation, and atomic revision acceptance.

No department profile is created or modified by the registry service.

### Slice 4: Execution-envelope integration

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_command_center.py`;
- `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`;
- `apps/lifeos-dashboard/tests/test_worker_command_center.py`.

Provides separate Worker jobs and results, compact wrapper transport, exact registered-title delivery, shared pause and one-job locking, manual and scheduler-triggered transport for one already-authorized envelope, successful-send suppression, bounded retry after failed transport, execution-history metadata, and one-copy wrapper-marker verification.

Validation evidence:

- focused Worker-runtime suite: `36 passed`;
- final full suite after two narrow wording repairs: `174 passed, 9 warnings in 173.76s`.

### Slice 5: Receiver validation and controlled outcomes

Status: Implemented and locally validated as technical infrastructure and a testable semantic contract.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_models.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`;
- `apps/lifeos-dashboard/tests/test_worker_receiver.py`.

Provides semantic preflight, atomic revision acceptance, transport-history matching, procedure and parameter checks, scope and tool enforcement, evidence-backed finalization, and exactly one controlled outcome.

The Python receiver models the required validation semantics and provides defense in depth. It is not itself the specialized ChatGPT Worker and does not establish that every canonical source must be independently resolved by Python before Worker operation.

Validation evidence:

- focused receiver suite: `22 passed`;
- full suite: `196 passed, 9 warnings in 191.97s`.

### Slice 6: Verification views and wake suppression

Status: Implemented and locally validated.

Files include:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_verification.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_verification_runtime.py`;
- Automation Logs frontend files;
- related focused tests.

Provides same-row verification state, separate machine-evidence and Department HQ review semantics, derived queues and wake decisions, read-only Automation Logs visibility, and no competing ledger.

Validation evidence:

- focused verification/runtime/Automation Logs suite: `20 passed`;
- full suite: `212 passed, 9 warnings in 198.41s`.

### Slice 7: Synthetic end-to-end backend pilot

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/tests/test_worker_end_to_end_pilot.py`;
- transport-integrity hardening in `worker_receiver.py` and `worker_receiver_store.py`;
- receiver regression coverage.

The disposable backend pilot proved exact-title failure behavior, pause and route refusal, missing-witness failure, corrupted-history rejection, unauthorized-scope hold, one successful `READY` to `IMPLEMENT` flow, verification review, duplicate suppression, second-outcome refusal, and temporary-only test state.

Validation evidence:

- focused pilot plus receiver regression suite: `32 passed`;
- full dashboard suite: `222 passed, 9 warnings in 238.78s`.

## Bounded Synthetic Desktop Transport Receipt

Status: Live validated by Rob on 2026-07-19.

Files:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`;
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`;
- `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`.

Live evidence:

- exact target and active document verified;
- stable Group composer verified;
- wrapper `SYNTH-DESKTOP-WRAP-1784515664-0de7866901` pasted and copied once for marker verification;
- submission occurred only after explicit confirmation;
- receipt reported `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- Worker returned exact acknowledgement `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker authority was created.

## Remaining Operational Validation

ADV-20260718-042 remains OPEN under its source owner.

The technical component evidence is substantial. The remaining useful proof is one bounded operational ChatGPT Worker flow demonstrating that the receiving Worker itself:

1. recognizes the envelope;
2. reads its department-owned profile from GitHub;
3. resolves the named canonical prompt or procedure and authoritative task or advisory source;
4. validates version, parameters, caller authority, ownership, scope, tools, procedures, and source boundaries;
5. refuses unknown, corrupted, unauthorized, ownership-conflicted, or scope-expanding work;
6. returns exactly one `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD` outcome;
7. reports evidence tied to the run, Worker, profile, task or advisory, and procedure;
8. permits Department HQ and run-history verification;
9. preserves duplicate suppression and prevents silent scope expansion.

This proof may use a synthetic or narrowly department-owned case. It must not create broad Worker authority merely to demonstrate the procedure.

## Operational Worker Procedure Requirements

Before the pilot, define one bounded procedure covering:

- envelope recognition and minimum required fields;
- exact GitHub profile and procedure source paths;
- canonical source-loading order;
- checksum or version validation where applicable;
- caller and task-class authorization checks;
- department ownership checks;
- allowed read and write scopes;
- approved tools and connector boundaries;
- durable-write gate handling;
- refusal and escalation conditions;
- duplicate and stale-revision handling;
- controlled outcome format;
- evidence and verification report format;
- Department HQ review and closure condition.

The procedure should point to canonical records rather than copying their full content into another source.

## Optional Python Hardening

A Python canonical source resolver or deeper automated ingress layer is deferred.

It should be considered only if a bounded operational pilot demonstrates a concrete need, such as:

- repeated failure to load the correct canonical source;
- unsafe ambiguity between versions or profile paths;
- inability to prevent duplicate execution with existing controls;
- unacceptable risk of scope expansion;
- a volume or reliability threshold that makes operational validation brittle;
- a requirement for fully unattended execution that Rob separately authorizes.

Any such implementation must remain infrastructure. It must not acquire domain ownership, invent authority, duplicate canonical truth, or replace Department HQ judgment.

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
- reopening the paused general full-text composer investigation;
- turning Python infrastructure into an autonomous department worker.

Technical success proves infrastructure readiness. It does not create operational authority.

## Next Decision

Rob must separately select one bounded next implementation goal.

Engineering recommendation:

1. define the operational Worker execution procedure and canonical GitHub source-resolution contract;
2. conduct one bounded synthetic or narrowly department-owned ChatGPT Worker pilot;
3. present the evidence for source-owner verification and closure review of ADV-20260718-042;
4. add the human-readable envelope summary before the first real Worker activation;
5. add deeper Python source-resolution enforcement only after demonstrated need;
6. only then consider at most one department-owned Worker for separately authorized profile and activation review.

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

No real profile, registry entry, route, wake, recurring authority schedule, Package E work, optional Python hardening, or next implementation slice may proceed from this packet alone.