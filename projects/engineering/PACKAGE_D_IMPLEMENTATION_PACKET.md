# Package D Implementation Packet

Updated: 2026-07-19
Owner: Engineering HQ
Lifecycle State: Decision Gate
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

The envelope is a routing and validation wrapper, not a replacement copy of the advisory, profile, procedure, or source records. Its JSON representation is intentionally machine-readable so exact fields can be validated through transport and receiver acceptance.

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

### Receiver transport integrity

Receiver acceptance requires exactly one existing transport-history row for the envelope `run_id`.

That row must prove:

- `status = succeeded`;
- `mode = send`;
- `prompt_type = worker`;
- exact matching `wrapper_id`;
- exact matching Worker, task, revision, procedure, authorization source, idempotency key, and verification mode.

Transport success is not inferred from a run ID alone.

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

Provides separate SQLite tables for:

- Worker registry configuration;
- Worker route state;
- receiver state keyed by `worker_id` plus `task_id`.

The store keeps deployment and route availability separate, enforces unique identities and paths, requires registration before state writes, atomically accepts only newer task revisions, and does not overload saved prompts or schedules with Worker authority.

### Slice 3: Registry service

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/lifeos_dashboard/worker_runtime_service.py`;
- `apps/lifeos-dashboard/tests/test_worker_runtime_service.py`.

Provides:

- registration of one already-authorized Worker entry;
- registry listing and stable-ID lookup;
- exact-title resolution;
- controlled deployment-state changes;
- route-state updates;
- fail-closed unknown-route behavior;
- envelope validation without mutation;
- validated atomic envelope acceptance.

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
- two narrow guidance-string regressions were repaired;
- final full suite: `174 passed, 9 warnings in 173.76s`.

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

Preflight validates identity, department ownership, caller authority, procedure identity and checksum, task class, parameters, source references, requested scopes, approved tools, verification mode, deployment, route, pause, revision freshness, and material transport drift.

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
- machine-evidence state remains separate from Department HQ review state;
- verification state is exposed as `pending`, `verified`, or `rejected`;
- the existing Command Center status payload is enriched rather than creating another API family;
- Automation Logs remains read-only;
- `AUTOMATIC` verification cannot be manually overridden;
- canonical `SOURCE_VERIFIED` or `CLOSED` state may suppress further wakes without duplicating lifecycle truth into SQLite.

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

### Slice 7: Synthetic end-to-end pilot

Status: Implemented and locally validated.

Files:

- `apps/lifeos-dashboard/tests/test_worker_end_to_end_pilot.py`;
- transport-integrity hardening in `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver.py`;
- transport-integrity hardening in `apps/lifeos-dashboard/lifeos_dashboard/worker_receiver_store.py`;
- receiver regression coverage in `apps/lifeos-dashboard/tests/test_worker_receiver.py`.

Pilot construction:

- one synthetic Worker registry entry;
- one fake exact-title route;
- one synthetic authority profile;
- one synthetic canonical procedure;
- one synthetic task and execution envelope;
- one injected fake transport adapter;
- temporary SQLite databases and disposable fixtures only.

Pilot proof:

- zero exact-title match fails closed;
- duplicate exact-title match fails closed;
- paused deployment refuses before transport;
- unavailable route refuses before transport;
- missing wrapper witness fails transport and cannot consume a revision;
- corrupted successful transport metadata fails receiver validation;
- unauthorized scope records `REPORT_AND_HOLD` without consuming a revision;
- one successful transport becomes `READY`, then exactly one `IMPLEMENT` outcome with same-row evidence and verification review;
- pending routine work enters the review queue without an immediate wake;
- verified routine work leaves the queue and suppresses repeat wakes;
- retry with a new `run_id` cannot re-execute the accepted task revision;
- a second controlled outcome is refused;
- no synthetic state survives outside temporary test fixtures.

Validation evidence:

- focused pilot plus receiver regression suite: `32 passed`;
- full dashboard suite: `222 passed, 9 warnings in 238.78s`;
- no Slice 7 functional regression remained.

## Bounded Synthetic Desktop Transport Receipt

Status: Live validated by Rob on 2026-07-19.

Files:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`;
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`;
- existing verified transport entrypoint `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`.

Bounded construction:

- fixed visible title `Synthetic_Worker_Pilot` inside the `Life OS` project;
- disposable `synthetic_desktop_worker` identity inside the wrapper only;
- unique synthetic wrapper, run, and task IDs;
- explicit instruction forbidding file, connector, calendar, email, task, dashboard, external-system, or durable-record action;
- draft-only default;
- send requires both `--send` and `--confirm-send SYNTHETIC_SEND`;
- launcher creates no profile, registry entry, route record, schedule, wake, or durable authority.

Live evidence:

- exact target resolved: `Synthetic_Worker_Pilot, chat in project Life OS`;
- exact active document verified: `Life OS - Synthetic_Worker_Pilot`;
- stable enabled Group composer verified;
- wrapper `SYNTH-DESKTOP-WRAP-1784515664-0de7866901` pasted and copied once for marker verification;
- submission occurred only after explicit confirmation;
- terminal reported `Message submitted after explicit confirmation and clipboard verification.`;
- machine receipt reported `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- Worker returned the exact required acknowledgement: `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker authority was created.

The clean control run occurred after Rob removed an unrelated Business-oriented project source and refreshed ChatGPT Classic. The source anomaly remains captured in Trello for possible future investigation and is not duplicated here as a separate GitHub open loop.

## First Runtime Milestone Receipt

Package D reached its first backend runtime milestone on 2026-07-19 and subsequently validated the physical ChatGPT Classic transport seam.

Completion conditions satisfied:

- registry and envelope schemas are persisted;
- exact Worker routes resolve safely and fail closed on zero or duplicate matches;
- stale and duplicate revisions are suppressed;
- the wrapper ID is preserved through transport evidence;
- receiver acceptance verifies the complete successful-send transport row;
- receiver validation returns one controlled outcome;
- verification and wake decisions derive from the same durable history row;
- focused and full repository tests pass;
- one synthetic backend end-to-end run is verified without activating a speculative real Worker;
- one bounded live desktop wrapper traversed exact UI navigation, composer verification, explicit send, and exact semantic acknowledgement without creating durable authority.

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
- reopening the abandoned full-text composer investigation.

Backend and desktop transport success prove technical readiness. They do not create operational authority.

## Next Decision

Rob must separately decide one of these bounded paths:

1. stop at the validated backend-and-desktop milestone and gather evidence from existing grandfathered pilots;
2. select at most one candidate department-owned Worker for a separately authorized profile and activation review.

Before any real Worker write, establish:

- record class;
- one owner;
- authoritative department-owned profile path;
- lifecycle state and priority as separate fields;
- allowed task class;
- read and write scopes;
- approved tools;
- verification mode;
- smallest useful next action;
- completion, rejection, and review conditions;
- why GitHub is the correct system;
- the statement or standing rule authorizing the write.

No real profile, registry entry, route, wake, recurring authority schedule, or Package E work may proceed from this packet alone.