# Package E Implementation Packet

Updated: 2026-07-21
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal
Record Class: Engineering implementation packet

## Title

**Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption**

## Authorization Basis

Rob explicitly authorized the Automation Command Center UI rebuild on 2026-07-20, designated the resulting work as Package E after Package D closeout, and on 2026-07-21 directed Engineering HQ to reshape Package E around a standardized Worker work log, nonblocking courier dispatch, Department HQ validation, and scheduled Chief of Staff consumption.

This packet authorizes only the bounded Engineering-owned technical architecture and implementation work described here. It does not by itself:

- grant a Worker new durable-write authority;
- change another department's Worker profile or procedure;
- change shared Worker governance;
- create cross-department authority;
- activate unattended schedules;
- delegate Department HQ judgment;
- delegate Rob-only validation;
- authorize Chief of Staff to close source-owned advisories;
- create automatic advisory acknowledgement, verification, implementation, or closure.

Cross-department rollout requires the proper owning department and any necessary Life OS Maintenance HQ shared-contract work.

## Why the Architecture Changed

The first Package E response-bridge pilot exposed two different browser-coupling failures:

1. the browser could reach a Worker conversation before its history finished hydrating, allowing a send attempt against a partially loaded room;
2. after a successful submission, the courier could remain occupied waiting for a legitimate long-running Worker response and then lose confidence during post-send capture.

The pilot also exposed a reporting-contract defect: a generated template represented `profile_version` as a quoted placeholder, leading the Worker to emit a string where the receiver required an integer.

These failures demonstrate that browser transport, Worker execution, result reporting, receiver validation, Department HQ review, and Chief of Staff consumption must be separate stages.

The courier must not wait for work to finish, interpret chat prose, revisit Worker rooms to scrape responses, validate work, or wake Chief of Staff.

## Objective

Complete a nonblocking operational chain from one already-authorized canonical assignment to a signed Department HQ result that is available for later Chief of Staff consumption without requiring Rob to manually carry prompts, reports, or evidence between rooms.

The intended chain is:

1. one canonical advisory, task, or approved source authorizes a bounded assignment;
2. Worker Operations resolves the exact execution-ready revision;
3. the browser courier wakes the exact Worker, proves submission, records dispatch evidence, returns to the source HQ, and becomes immediately available for another wake;
4. the Worker performs the authorized work independently of browser automation;
5. the Worker creates one immutable schema-valid result attempt in its deterministic GitHub result folder;
6. a local result ingester discovers the report, validates its path, schema, identity, assignment, authority, scopes, tools, evidence, and revision, then updates the existing SQLite runtime state;
7. when a report is invalid, the ingester records a bounded rejection and queues a report-repair wake that authorizes correction of the report only, not re-execution or scope expansion;
8. when a report is valid, the courier wakes the owning Department HQ and immediately returns;
9. the Department HQ reviews report integrity, authority compliance, and the work itself where independent verification is possible;
10. when HQ cannot independently verify the work, it records that limitation and routes a Rob-validation requirement;
11. a signed HQ or Rob validation receipt makes the result ready for Chief of Staff consumption;
12. a separately authorized scheduled Chief of Staff task periodically reads only consumption-ready results and reports meaningful items without receiving courier wakes or changing source advisory lifecycle automatically.

## Canonical Architecture

### One owner and one operational ledger

- Engineering HQ owns the technical machinery and this implementation packet.
- Department HQs own Worker profiles, procedures, authority, domain judgment, holds, and verification.
- Source owners own advisory lifecycle and closure.
- Rob remains final authority and validates work that cannot be independently checked by the owning HQ.
- SQLite `execution_history` remains the sole operational runtime ledger for assignment, dispatch, report state, repair state, receiver outcome, HQ review, and Rob-validation state.
- GitHub remains authoritative for packages, profiles, procedures, advisories, tasks, decisions, and immutable evidence artifacts.
- The Worker result outbox is an evidence surface and audit trail, not a competing runtime queue or lifecycle ledger.
- Dashboard views remain interfaces over GitHub and SQLite state, not independent truth.

No second execution, response, outcome, wake, queue, verification, or consumption ledger may be created.

### Courier boundary

The courier has exactly two short transport roles:

1. wake a Worker with one already-authorized assignment;
2. wake the owning Department HQ when the ingester has a schema-valid report ready for review.

For either wake, the courier may:

- operate only against canonical exact ChatGPT conversation URLs;
- borrow the one controlled ChatGPT tab after preflight;
- require the exact room to finish hydrating before preparing the composer;
- require an empty composer and no active generation;
- preserve the source URL;
- send one bounded correlated wake;
- prove the correlated user turn exists;
- return to the exact source URL;
- disconnect and release the shared execution gate immediately.

The courier must not:

- wait for Worker or HQ completion;
- capture or interpret assistant responses;
- validate a Worker report;
- inspect work evidence;
- decide whether a report is accepted;
- wake Chief of Staff directly;
- broaden, approve, prioritize, or close work;
- act on arbitrary browser tabs;
- blind-retry after uncertain submission.

### Deterministic Worker result outbox

The Engineering pilot uses this deterministic evidence path:

`projects/<department>/worker-results/<worker_id>/<run_id>/`

Immutable attempt files use zero-padded sequence numbers:

- `report-001.json`
- `rejection-001.json`
- `report-002.json`
- `hq-review-001.json`
- `rob-validation-001.json`, only when Rob validation is required

Rules:

- a Worker creates a new report attempt and never overwrites an earlier artifact;
- the path department, Worker ID, and run ID must match the canonical assignment;
- every artifact uses a versioned strict schema;
- unknown fields, missing fields, wrong types, mismatched identities, stale revisions, conflicting attempts, unauthorized scopes, or unverifiable claims fail closed;
- commit SHA, blob SHA, path, and report checksum become evidence references on the existing runtime state;
- raw secrets, credentials, private data, detailed medical data, or other prohibited content must never enter the outbox;
- report files do not change advisory lifecycle or constitute HQ verification.

### Narrow report-write authority

Writing a result file is execution reporting, but it is still a durable GitHub write.

Before a Worker may use the outbox, its owning Department HQ must explicitly authorize a narrow create-only reporting scope that:

- applies only to the Worker's own deterministic result folder;
- applies only to the current authorized `run_id`;
- permits new immutable report attempts only;
- prohibits overwrites and deletion;
- prohibits edits to advisories, status, open loops, procedures, profiles, implementation files, or unrelated evidence;
- does not convert a read-only task into general write authority;
- does not authorize re-execution, scope expansion, or lifecycle change.

Package E may pilot this authority with `engineering_worker` inside Engineering-owned paths. Shared adoption requires Life OS Maintenance HQ review of the universal contract and explicit owning-department profile or procedure updates. Engineering must not silently grant every Worker standing GitHub write authority.

### Result ingester boundary

The local result ingester is deterministic technical machinery. It may:

- poll or watch the approved GitHub outbox location;
- discover new immutable artifacts;
- verify exact path identity, schema version, field types, run identity, Worker identity, task revision, procedure, authorization source, verification mode, scopes, tools, evidence, and checksums;
- compare the report against canonical GitHub assignment sources and existing SQLite runtime state;
- update report and receiver fields on the existing `execution_history` runtime state;
- write a bounded machine rejection artifact when a report is invalid;
- queue a repair wake or HQ-review wake under the rules below;
- suppress duplicates and stale attempts.

The ingester must not:

- reinterpret free-form Worker prose;
- silently repair malformed reports;
- invent missing evidence;
- re-execute work;
- select new work or priorities;
- change source advisory lifecycle;
- approve HQ verification;
- wake Chief of Staff;
- create a competing runtime ledger.

### Report-repair loop

When a report fails deterministic validation, the ingester records a rejection artifact containing:

- run ID and Worker ID;
- rejected report attempt;
- exact validation error codes;
- expected field types or values;
- observed values when safe to preserve;
- allowed action: submit a corrected report only;
- `work_reexecution_authorized: false`;
- `scope_expansion_authorized: false`;
- next report attempt number;
- escalation condition.

The courier may then wake the same Worker with a bounded report-repair request.

A repair wake:

- uses the same canonical run and assignment;
- does not create new task authority;
- does not authorize repeated work;
- permits only a new immutable report attempt;
- stops and routes to the owning HQ after the configured repair-attempt ceiling or any authority conflict.

The exact repair-attempt ceiling is an implementation parameter. Initial live validation must use a conservative bounded value and fail closed.

### Department HQ review

A schema-valid Worker report triggers an owning-HQ review wake according to the assignment's verification mode.

For `IMMEDIATE_HQ`, the courier wakes the owning HQ promptly.

For `ROUTINE_BATCH`, the report enters the existing department review queue without an immediate wake unless a hold, conflict, or time-sensitive condition justifies one.

For `AUTOMATIC`, machine verification is permitted only when the authoritative procedure defines an explicit deterministic postcondition. Automatic advisory closure remains prohibited unless separately and explicitly authorized by the source owner and shared contract.

The owning Department HQ reviews:

1. report integrity and correlation;
2. authority and scope compliance;
3. evidence sufficiency;
4. the actual work where independent inspection is possible;
5. unresolved uncertainty, holds, or approval requirements.

HQ writes one immutable review receipt with one review state:

- `VERIFIED`
- `REJECTED`
- `REPAIR_REQUIRED`
- `ROB_VALIDATION_REQUIRED`

HQ review does not close the source advisory automatically.

### Rob-validation path

When the work cannot be independently verified by the owning HQ, the HQ review receipt must state:

- report integrity result;
- authority-compliance result;
- what evidence was checked;
- why direct work verification is unavailable;
- the exact observation or decision Rob must provide.

The result is not ready for ordinary Chief of Staff consumption until Rob records `VERIFIED` or `REJECTED`, unless the result itself is an urgent hold or elevation that Chief of Staff must coordinate.

Rob validation is preserved as an immutable receipt linked to the same run.

### Chief of Staff consumption boundary

The courier never wakes Chief of Staff.

A separately authorized ChatGPT scheduled task may periodically inspect only results that have reached a consumption-ready state, including:

- HQ-verified completion;
- Rob-verified completion;
- HQ-confirmed `REPORT_AND_HOLD`;
- HQ-confirmed `ELEVATE_FOR_APPROVAL`;
- verification rejection requiring coordination;
- stale or unresolved review conditions that meet a defined reporting threshold.

The Chief of Staff task may:

- synthesize meaningful changes for Rob;
- identify the owning department and source owner;
- identify decisions, holds, or follow-through needs;
- state when an advisory appears ready for source-owner review.

It must not:

- consume raw unvalidated Worker reports as truth;
- replace Department HQ review;
- wake Workers or Department HQs through the courier;
- create new authority;
- close source advisories automatically;
- write durable consumption state without separate bounded authority and a proven deduplication design.

The first Chief of Staff scheduled-task pilot is read-only and manual-first. Its cadence, deduplication method, and activation require separate explicit authorization after the Engineering end-to-end chain passes.

## Runtime State Model

The following are technical runtime states, not advisory lifecycle states:

1. `AUTHORIZED`
2. `DISPATCH_PENDING`
3. `DISPATCH_SUBMITTED`
4. `RESULT_PENDING`
5. `REPORT_DISCOVERED`
6. `REPORT_REJECTED`
7. `REPORT_REPAIR_PENDING`
8. `REPORT_VALIDATED`
9. `HQ_REVIEW_PENDING`
10. `HQ_VERIFIED`
11. `HQ_REJECTED`
12. `ROB_VALIDATION_REQUIRED`
13. `ROB_VERIFIED`
14. `ROB_REJECTED`
15. `READY_FOR_COS`
16. `HELD`
17. `ELEVATED_FOR_APPROVAL`

These states remain in the existing SQLite runtime model. GitHub artifacts provide immutable evidence but do not independently drive lifecycle without ingester validation.

## Implemented Foundation: Existing Worker Operations and Courier

Lifecycle State: Implemented foundation / Transitional architecture

Implemented components include:

- `apps/lifeos-dashboard/automation/chatgpt_worker_browser_roundtrip.py`;
- `apps/lifeos-dashboard/automation/run_synthetic_worker_browser_pilot.py`;
- `apps/lifeos-dashboard/automation/run_synthetic_worker_browser_pilot.cmd`;
- `apps/lifeos-dashboard/automation/validate_and_run_worker_operations.cmd`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_operations.py`;
- Worker Operations API routes and dashboard surface;
- exact destination and hydration checks;
- shared pause and one-job execution gate;
- canonical advisory discovery;
- existing SQLite execution history and HQ review views;
- focused browser, backend, application, and UI tests.

The existing browser implementation still contains response-waiting and response-capture behavior from the superseded round-trip design. It is transitional and must not be treated as the final Package E architecture.

`ADV-20260720-047` revision 2 is preserved as architecture-discovery evidence:

- the Worker received and completed the bounded assignment;
- the courier stopped after submission uncertainty while waiting for response capture;
- the Worker produced a strong human-readable evidence report;
- the generated machine report contained a wrong-type `profile_version` because the supplied template represented that field as a quoted placeholder;
- no blind retry is authorized;
- the run is not accepted as the completed Package E proof.

## Slice 2: Dispatch-Only Courier

Lifecycle State: Next

Required behavior:

1. preserve exact source and destination URLs;
2. wait for exact Worker history, identity, and composer hydration;
3. send one correlated bounded assignment;
4. prove the correlated user turn exists;
5. record dispatch evidence on the existing runtime state;
6. return to source HQ immediately;
7. release the browser execution gate without waiting for Worker output;
8. remove response capture, response stability waiting, and assistant-turn interpretation from the courier path;
9. preserve stop-before-send and no-blind-retry behavior;
10. retain a zero-authority courier self-test.

Completion condition:

- a live bounded dispatch reaches `engineering_worker`, records `DISPATCH_SUBMITTED`, returns to HQ, and frees the courier while the Worker remains independently active.

## Slice 3: Engineering Worker Result-Outbox Pilot

Lifecycle State: Planned after Slice 2

Required behavior:

1. define versioned report, rejection, HQ-review, and Rob-validation JSON schemas;
2. define deterministic paths and immutable attempt rules;
3. add exact schema examples whose numeric and boolean fields use correct JSON types;
4. authorize `engineering_worker` through an Engineering-owned profile or procedure update for create-only report attempts inside its own current run folder;
5. prohibit overwrites, deletion, unrelated writes, re-execution, and scope expansion;
6. add parser and schema tests for malformed, missing, unknown, wrong-type, conflicting, duplicate, stale, and unauthorized artifacts;
7. preserve GitHub commit, blob, path, and checksum evidence.

Completion condition:

- one synthetic and one bounded live Engineering Worker report appear as immutable schema-valid GitHub artifacts without granting general write authority.

## Slice 4: Result Ingester and Repair Wakes

Lifecycle State: Planned after Slice 3

Required behavior:

1. discover new result artifacts without browser response scraping;
2. correlate them to the canonical assignment and existing SQLite runtime state;
3. validate schema, identity, revision, authority, scopes, tools, evidence, and checksums;
4. update the existing runtime state without creating another ledger;
5. write deterministic rejection artifacts for invalid reports;
6. queue bounded report-repair wakes;
7. ensure repair wakes authorize report correction only;
8. suppress duplicate and stale attempts;
9. route exhausted or conflicted repairs to the owning HQ;
10. expose actionable status and evidence in Worker Operations.

Completion condition:

- an intentionally malformed report is rejected, the same Worker is woken for report repair without repeating the work, a corrected immutable attempt is accepted, and the existing runtime state advances to `REPORT_VALIDATED`.

## Slice 5: Owning-HQ Wake and Verification Receipts

Lifecycle State: Planned after Slice 4

Required behavior:

1. derive the owning HQ from canonical Worker and assignment state;
2. wake the owning HQ only after report validation and according to verification mode;
3. return the courier immediately after the HQ wake;
4. provide the HQ exact report and evidence pointers without copying detailed truth into the wake text;
5. support `VERIFIED`, `REJECTED`, `REPAIR_REQUIRED`, and `ROB_VALIDATION_REQUIRED` receipts;
6. ingest the immutable HQ receipt into the existing runtime state;
7. preserve source-owner advisory lifecycle separation;
8. prevent HQ self-signoff when required evidence is unavailable.

Completion condition:

- Engineering HQ receives a validated run, independently checks available evidence, writes a schema-valid review receipt, and advances the runtime state to either `HQ_VERIFIED` or an explicit nonverified branch.

## Slice 6: Rob Validation and Real End-to-End Proof

Lifecycle State: Planned after Slice 5

Run one bounded Engineering-owned assignment through:

- canonical discovery;
- dispatch-only Worker wake;
- immediate courier release;
- immutable Worker result submission;
- deterministic ingester validation;
- repair loop if deliberately exercised;
- owning-HQ wake;
- HQ work inspection where possible;
- Rob validation branch where independent HQ verification is intentionally unavailable or simulated;
- one final consumption-ready state;
- duplicate suppression;
- source-owner lifecycle separation.

The proof must require no manual prompt or report copying by Rob.

Completion evidence must include exact run, wrapper, Worker, task, revision, procedure, authorization, result paths, report and review SHAs, receiver outcome, HQ review state, Rob-validation state when used, and what did not occur.

## Slice 7: Chief of Staff Scheduled Consumption and Unattended Operation

Lifecycle State: Deferred until Slice 6 passes and Rob separately authorizes activation

Potential bounded work includes:

- a read-only scheduled Chief of Staff task that checks consumption-ready GitHub evidence and source advisory state;
- meaningful-change filtering and no-change silence;
- a proven deduplication method that does not create duplicate truth;
- scheduled reporting of verified work, holds, elevations, rejected verification, stale reviews, and source-owner review readiness;
- local background result ingestion and courier wake processing;
- on-demand browser launch and shutdown;
- restart recovery and actionable diagnostics;
- rollback-window retirement of obsolete response-capture and legacy UI paths.

This slice must not:

- generate authority;
- select priorities;
- create advisories;
- treat unverified Worker reports as truth;
- make Chief of Staff a substitute Department HQ;
- automatically close source-owned advisories;
- create recurring dispatch without an approved task-generation and authorization model.

## Human-Readable Envelope Requirement

Before ordinary real Worker activation beyond bounded pilots, retain a display-only human-readable envelope summary derived from the same `ExecutionEnvelope` object.

The summary must show:

- Worker;
- task and revision;
- procedure and version;
- authorization source;
- verification mode;
- wrapper ID;
- run ID;
- bounded instruction.

It must remain non-authoritative, have no independent edit or parse path, and be covered by parity tests.

## Explicit Non-Scope

Package E does not authorize:

- changing another department's files;
- changing shared governance or universal boot files without coordinated authority;
- granting every Worker standing GitHub write authority;
- closing `ADV-20260718-042`, `ADV-20260720-047`, or any other source-owned advisory automatically;
- automatic Department HQ judgment;
- automatic Rob validation;
- courier wakes to Chief of Staff;
- automatic advisory acknowledgement, implementation, source verification, or closure;
- autonomous task selection or prioritization;
- new Worker profiles, connectors, spending, or external systems outside a separately approved slice;
- recurring authority generation;
- a competing runtime ledger;
- destructive removal of legacy data or schedules;
- arbitrary browser control;
- public, irreversible, privacy-sensitive, or high-consequence actions.

## Package Completion Condition

Package E may close only when:

1. one real bounded execution-ready assignment is dispatched without Rob acting as courier;
2. the courier returns immediately and remains free for another wake while the Worker executes;
3. the Worker writes one immutable schema-valid result artifact under exact narrow authority;
4. an intentionally invalid report can be rejected and repaired without re-executing the work;
5. the result ingester updates the existing runtime state without creating a second ledger;
6. the owning Department HQ is woken only after report validation;
7. HQ independently reviews report integrity, authority compliance, and the work where possible;
8. work unavailable to HQ verification follows an explicit Rob-validation path;
9. one signed result reaches `READY_FOR_COS`;
10. the Chief of Staff scheduled-consumption design is either live validated under separate authorization or explicitly deferred by Rob;
11. duplicate execution, duplicate reports, blind retries, and silent scope expansion remain prevented;
12. source-owner lifecycle authority remains separate;
13. the human-readable envelope requirement is resolved or explicitly deferred by Rob;
14. the rollback or retirement decision for superseded response-capture and legacy automation paths is recorded;
15. any shared Worker-contract or cross-department adoption changes are completed by the proper owner or explicitly left as a bounded Engineering-only pilot.

## Smallest Useful Next Action

Implement Slice 2: convert the one-tab courier from a response-blocking round trip into a dispatch-only wake that proves submission, returns immediately, releases the browser gate, and records `DISPATCH_SUBMITTED` without waiting for Worker output.

## Review Condition

Engineering HQ reviews each slice against this packet. Rob remains final authority for new authority, shared-contract changes, cross-department rollout, scheduled-task activation, and Package E closeout.