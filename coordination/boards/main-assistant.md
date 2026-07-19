# Chief of Staff HQ Advisory Board

Updated: 2026-07-19
Purpose: Canonical advisory text sourced from Chief of Staff HQ, including formal advisories arising from LifeOS HQ meetings. The retained filesystem path remains `coordination/boards/main-assistant.md`.

## Open Advisories

### ADV-20260718-042 — Move automated prompt verification from composer transport to receiving Workers

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Engineering HQ
- Lifecycle State: OPEN
- Priority: HIGH
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department and Owner: Engineering HQ
- Record Class: Automation architecture implementation request
- Authorization Basis: Rob-approved bounded Engineering implementation
- Related Work: Package C migration, dashboard automation, prompt database, event-driven automation, and the canonical Worker contracts
- Completion Condition: The automation layer reliably delivers and logs a recognized envelope without exact semantic full-text equality; receiving Workers validate the canonical prompt, parameters, authority, ownership, and scope; the Worker returns `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`; Engineering provides current test or run-log evidence that duplicate execution and silent scope expansion are prevented.

#### Objective

Move semantic validation out of the composer transport and into the receiving Worker.

The automation layer is the courier. It verifies bounded delivery, correlation, and transport evidence. The receiving Worker verifies meaning, legitimacy, scope, ownership, authorization, and source-system boundaries under:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

#### Required Transport Behavior

Engineering should implement a small machine-readable envelope that includes at least:

```text
<<<LIFEOS_AUTOMATION>>>
run_id: RUN-YYYYMMDD-NNNN
prompt_id: DEPARTMENT_ACTION_ID
prompt_version: N
canonical_prompt_checksum: SHA256:...
source: CHIEF_OF_STAFF_HQ
target: ENGINEERING_HQ
authorization: READ_ONLY | BOUNDED_WRITE | APPROVAL_REQUIRED
advisory_id: ADV-YYYYMMDD-NNN
params_json: {...}
params_checksum: SHA256:...
<<<END_LIFEOS_AUTOMATION>>>
```

The transport must:

1. deliver one recognizable envelope to the intended destination;
2. require recognizable boundaries and minimum viable fields rather than exact full-text equality;
3. preserve one durable `run_id` across retries;
4. log source, target, prompt ID and version, authorization class, advisory or approval reference, parameters, checksums, delivery attempt, send action, observed composer state, retry count, and transport result;
5. prevent duplicate delivery for the same `run_id`;
6. avoid interpreting, editing, approving, silently truncating, or discarding requested work;
7. treat character counts and copied composer text as diagnostic evidence rather than the semantic gate.

#### Required Receiver Validation

The receiving Worker must:

1. recognize and parse the wrapper;
2. verify `prompt_id` and `prompt_version` against the canonical prompt database;
3. load the canonical prompt from the database when prompt-ID invocation is available;
4. normalize and verify prompt and parameter checksums;
5. validate parameters against the prompt schema;
6. confirm the source may request the task class;
7. confirm the target department owns the work;
8. confirm authorization, advisory or approval references, procedures, and source boundaries;
9. ignore harmless transport noise outside the recognized envelope while refusing text that changes scope, destination, permanence, permissions, or requested actions;
10. preserve `run_id`, advisory revision, Worker ID, and profile version in execution and reporting evidence.

#### Receiver Outcomes

- `IMPLEMENT`: wrapper, prompt, parameters, ownership, and authorization validate; execute only the bounded work and report evidence tied to `run_id`.
- `ELEVATE_FOR_APPROVAL`: the request is legitimate but requires new authority, judgment, conflict resolution, financial or privacy approval, or another decision not already granted.
- `REPORT_AND_HOLD`: prompt or checksum is unknown, parameters fail, ownership is wrong, authority is missing, the envelope is corrupted, scope conflicts with procedures, or unexpected instructions materially change the request.

#### Logging and Boundaries

The run log must preserve transport, validation, duplicate-suppression, Worker outcome, evidence, and final verification state.

Do not:

- make exact composer-text equality a release blocker;
- use minimum character count as semantic proof;
- let transport reinterpret work;
- let the wrapper bypass ownership, procedures, advisory approval, durable-write gates, or source-system boundaries;
- create a competing prompt source;
- close this advisory without current test or run-log evidence.

## Recently Acknowledged / Implemented Advisories

### ADV-20260719-043 — Create canonical LifeOS operational and Worker protocols

- Date: 2026-07-19
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Lifecycle State: CLOSED
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Acknowledged: 2026-07-19
- Implemented: 2026-07-19
- Source Verified: 2026-07-19
- Closed: 2026-07-19
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department and Owner: Life OS Maintenance HQ
- Record Class: Shared-governance implementation advisory

#### Final Outcome

Life OS Maintenance HQ implemented the canonical shared execution architecture and completed the required immediate HQ verification.

#### Files Created

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

#### Files Modified

- `memory/STARTUP_BOOT.md`
- `workers/WORKER_STANDARD.md`
- `workers/README.md`
- `coordination/boards/main-assistant.md`
- `coordination/ADVISORY_INDEX.md`

#### Exact Boot Changes

The existing ten-file universal kernel and its order were preserved.

After the universal kernel:

- every LifeOS HQ and Department HQ loads `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` before role-specific state;
- Department HQs retain their canonical local sequence and load routed dependencies only;
- Department HQs load the Worker contract only for Worker creation, authority review, holds, audits, approval, or immediate HQ verification;
- Workers use the same `memory/STARTUP_BOOT.md` entry point;
- Workers load the universal kernel, both shared protocols, the owning department identity, the exact department-owned profile, the authoritative advisory, task or schedule, and only required department records and procedures;
- Workers do not automatically load full department histories, notebooks, backlogs, unrelated open loops, or unrelated advisories.

#### Settled Architecture Preserved

The protocols codify:

- Rob's final authority;
- LifeOS HQ as shared strategic meeting room without a backlog;
- Chief of Staff HQ as daily operational front door, router, reporter, and follow-through coordinator;
- Department HQ ownership of specialist judgment, durable state, approvals, profiles, holds, and verification;
- Workers as bounded executors with no independent strategy or backlog;
- dashboard and automation as transport, visibility, diagnostic, and control layers without policy authority;
- one owner and one authoritative record;
- source-system boundaries;
- one-wake execution-ready routing;
- verification modes `AUTOMATIC`, `ROUTINE_BATCH`, and `IMMEDIATE_HQ`;
- lifecycle and priority separation;
- revision handling and duplicate suppression;
- hold, elevation, resume, wake-suppression, scheduled-procedure, and desktop-pause behavior;
- Worker outcomes `IMPLEMENT`, `REPORT_AND_HOLD`, and `ELEVATE_FOR_APPROVAL`;
- department-owned profile location `projects/<department>/workers/<profile>.md`;
- visible Worker-title and stable internal Worker-ID conventions;
- Worker self-edit and authority-ceiling prohibitions;
- durable Worker state in advisories, run records, logs, and permitted department records rather than competing Worker backlogs.

#### Conflict Reconciliation

The repository already contained two top-level pilot Worker packages and an older independent Worker boot standard.

Maintenance reconciled this without migrating or editing either pilot profile:

- `workers/WORKER_STANDARD.md` is now a compatibility pointer to canonical boot and the new Worker contract;
- `workers/README.md` is now a compatibility registry rather than an independent architecture source;
- the existing Raw Capture and Inventory pilots are grandfathered under their current bounded purposes;
- no additional top-level Worker package may be created by analogy;
- new Workers use department-owned profiles;
- pilot-local instructions are subordinate to the canonical shared protocols;
- migration, retirement, or relocation of either pilot requires separate owner review and authorization.

#### Read-Only Verification Evidence

Maintenance re-fetched and inspected:

- both canonical shared protocols;
- the unchanged ten-file universal-kernel order;
- the LifeOS HQ, Chief of Staff HQ, Maintenance HQ, specialist HQ, standalone-project, audit, and Worker branches;
- Worker outcomes, authority ceilings, profile location, naming, stable IDs, revision suppression, verification modes, pause behavior, holds, elevations, and source boundaries;
- both compatibility surfaces.

The inspection found one coherent canonical HQ branch, one coherent Worker branch, and no duplicate active authority model.

No specialist department strategy, handoff, status, open-loop file, Worker profile, dashboard code, automation code, or Engineering routing implementation was modified.

#### Remaining Implementation Dependencies

Engineering still owns:

- Worker routing registry implementation;
- exact-title lookup;
- zero-match and duplicate-match failure handling;
- stable-ID transport;
- receiver state;
- advisory revision deduplication;
- verification queues;
- wake suppression;
- technical rename and rollover procedures.

ADV-20260718-042 remains the active Engineering advisory for receiver-side semantic validation and related transport behavior. No duplicate Engineering advisory was created.

Specialist departments should create Worker profiles only when a real Worker is needed. No blanket profile-creation advisory is recommended.

### ADV-20260718-041 — Create a global Trello connector write SOP

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Lifecycle State: CLOSED
- Priority: HIGH
- Implemented: 2026-07-18
- Acknowledged: 2026-07-18
- Closed: 2026-07-18
- Durable Output: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`

Life OS Maintenance HQ extended the existing global Connector Reliability Operating Pattern with the Trello false-negative write protocol, live read-back, duplicate prevention, truthful reporting, and source-boundary protections.

### ADV-20260716-038 — Explore a read-mostly LifeOS desktop dashboard window

- Lifecycle State: CLOSED
- Acknowledged: 2026-07-16
- Closed: 2026-07-16

Engineering accepted the dashboard as a read-mostly window into authoritative systems and deferred implementation until Rob supplied further requirements.

### ADV-20260715-036 — Design prompts for seven LifeOS Department HQs

- Lifecycle State: CLOSED
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15

Rob confirmed all seven Department HQ chats were open and ready under the approved boundaries.

### ADV-20260715-035 — Standardize Rob's friction-aware daily operating pattern

- Lifecycle State: CLOSED
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15

Engineering verified that `memory/06_DAILY_OPERATING_SOP.md` is included in canonical boot.

### ADV-20260709-029 — Engineering request for dedicated rapid-capture Worker

- Lifecycle State: CLOSED
- Closed: 2026-07-09
- Implemented Through: ADV-20260709-030

Engineering defined the technology-independent Worker concept, and the earlier Life Logistics role implemented the original pilot package. Current Worker authority now lives in the July 19 canonical shared protocols.

## Board Rules

- Read `coordination/ADVISORY_INDEX.md` first.
- This retained path is the Chief of Staff HQ source board despite its legacy filename.
- LifeOS HQ formal advisories use Chief of Staff HQ as the source department.
- LifeOS HQ does not maintain a separate advisory board.
- Keep full actionable text for every open advisory and a bounded recent completed working set.
- Keep canonical advisory text here and routing state in the Advisory Index.
- Do not duplicate advisory text into target boards or department open loops merely for visibility.
- Use canonical lifecycle states and keep priority separate.
- Do not mark an advisory `IMPLEMENTED`, `SOURCE_VERIFIED`, or `CLOSED` without current evidence.
- Git history preserves the detailed text removed during compaction.