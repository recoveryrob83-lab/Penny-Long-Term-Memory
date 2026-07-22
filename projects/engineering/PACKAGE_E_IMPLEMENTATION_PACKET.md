# Package E Implementation Packet

Updated: 2026-07-21
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal
Record Class: Engineering implementation packet

## Title

**Worker Dispatch, Result Outbox, HQ Verification, and CoS Consumption**

## Authorization Basis

Rob authorized the Automation Command Center UI rebuild on 2026-07-20, designated the resulting work as Package E after Package D closeout, and on 2026-07-21 directed Engineering HQ to reshape Package E around a standardized Worker work log, nonblocking courier dispatch, Department HQ validation, explicit Rob validation when HQ cannot inspect the work, and scheduled Chief of Staff consumption.

This packet authorizes only the bounded Engineering-owned technical architecture and implementation work described here. It does not by itself:

- grant universal Worker durable-write authority;
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

The first Package E response-bridge pilot exposed three architectural defects:

1. the browser could reach a Worker conversation before its history finished hydrating;
2. after successful submission, the courier could remain occupied waiting for a legitimate long-running Worker response and then lose confidence during post-send capture;
3. a generated response template represented `profile_version` as a quoted placeholder, leading the Worker to emit a string where the receiver required an integer.

The first live dispatch-only and outbox pilot, `ADV-20260721-048`, then exposed a fourth transport defect:

4. the correlated Worker wake succeeded and the Worker completed independently, but the controlled browser tab did not return to Engineering HQ after dispatch.

These observations demonstrate that browser transport, Worker execution, result reporting, deterministic report validation, Department HQ review, Rob validation, and Chief of Staff consumption must remain separate stages. A successful Worker wake must not be treated as successful browser restoration, and a successful report artifact must not be treated as deterministic ingestion or HQ signoff.

## Objective

Complete a nonblocking operational chain from one already-authorized canonical assignment to a signed Department HQ result available for later Chief of Staff consumption without requiring Rob to manually carry prompts, reports, or evidence between rooms.

The intended chain is:

1. one canonical advisory, task, or approved source authorizes a bounded assignment;
2. Worker Operations resolves the exact execution-ready revision;
3. the browser courier wakes the exact Worker, proves submission, records dispatch evidence, returns to the source HQ, and becomes available for another wake;
4. the Worker performs the authorized work independently of browser automation;
5. the Worker creates one immutable schema-valid result attempt in its deterministic GitHub result folder;
6. a local result ingester discovers the report, validates it against the canonical assignment and existing runtime state, and updates the same SQLite execution row;
7. invalid reports produce bounded rejection evidence and report-repair wakes that authorize correction only;
8. valid reports trigger the owning Department HQ review path according to verification mode;
9. Department HQ reviews report integrity, authority compliance, evidence, and the work where independent verification is possible;
10. work unavailable to HQ verification follows an explicit Rob-validation path;
11. a signed HQ or Rob receipt makes the result ready for Chief of Staff consumption;
12. a separately authorized ChatGPT scheduled task periodically reads only consumption-ready results and reports meaningful changes.

## Canonical Architecture

### One owner and one operational ledger

- Engineering HQ owns the technical machinery and this implementation packet.
- Department HQs own Worker profiles, procedures, authority, holds, verification, and domain judgment.
- Source owners own advisory lifecycle and closure.
- Rob remains final authority and validates work that cannot be independently checked by the owning HQ.
- SQLite `execution_history` remains the sole operational runtime ledger for assignment, dispatch, report state, repair state, receiver outcome, HQ review, Rob validation, and consumption readiness.
- GitHub remains authoritative for packages, profiles, procedures, advisories, tasks, decisions, and immutable evidence artifacts.
- Worker result folders are evidence surfaces and audit trails, not competing runtime queues or lifecycle ledgers.
- Dashboard views remain interfaces over GitHub and SQLite state, not independent truth.

No second execution, response, outcome, wake, queue, verification, or consumption ledger may be created.

### Courier boundary

The courier has exactly two short transport roles:

1. wake a Worker with one already-authorized assignment;
2. wake the owning Department HQ when a schema-valid report is ready for review.

For either wake, the courier may:

- operate only against canonical exact ChatGPT conversation URLs;
- borrow the one controlled ChatGPT tab after preflight;
- require the exact room to finish hydrating;
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
- blind-retry after uncertain or confirmed submission.

A confirmed send and an exact source-room return are separate transport postconditions. A failed return must preserve the confirmed dispatch as nonretryable and report browser restoration failure explicitly.

### Deterministic Worker result outbox

The Engineering pilot uses:

`projects/<department>/worker-results/<worker_id>/<run_id>/`

Immutable attempt files use zero-padded sequence numbers:

- `report-001.json`
- `rejection-001.json`
- `report-002.json`
- `hq-review-001.json`
- `rob-validation-001.json`, only when Rob validation is required

Rules:

- a Worker creates a new report attempt and never overwrites an earlier artifact;
- path department, Worker ID, and run ID must match the canonical assignment;
- every artifact uses a strict versioned schema;
- unknown fields, missing fields, wrong types, mismatched identities, stale revisions, conflicting attempts, unauthorized scopes, or unverifiable claims fail closed;
- commit SHA, blob SHA, path, and canonical content checksum become evidence references on the existing runtime state;
- the ingester calculates the canonical checksum when the Worker connector cannot provide it;
- prohibited secrets or private data must never enter the outbox;
- report files do not change advisory lifecycle or constitute HQ verification.

### Narrow report-write authority

Writing a result file is execution reporting, but it remains a durable GitHub write.

Before a Worker may use the outbox, its owning Department HQ must explicitly authorize a narrow create-only reporting scope that:

- applies only to the Worker's own deterministic result folder;
- applies only to the current authorized `run_id`;
- permits new immutable report attempts only;
- prohibits overwrites and deletion;
- prohibits edits to advisories, status, open loops, procedures, profiles, implementation files, or unrelated evidence;
- does not convert a read-only task into general write authority;
- does not authorize re-execution, scope expansion, or lifecycle change.

Package E may pilot this authority with `engineering_worker` inside Engineering-owned paths. Shared adoption requires Life OS Maintenance HQ review of the universal contract and explicit owning-department profile or procedure updates.

### Result ingester boundary

The local result ingester is deterministic technical machinery. It may:

- poll or watch approved result locations;
- discover new immutable artifacts;
- verify exact path identity, schema version, field types, run identity, Worker identity, task revision, procedure, authorization source, verification mode, scopes, tools, evidence, and checksums;
- calculate the canonical content checksum from stored JSON;
- compare the report against canonical GitHub assignment sources and existing SQLite runtime state;
- update report and receiver fields on the existing execution row;
- write a bounded machine rejection artifact when a report is invalid;
- queue a repair wake or HQ-review wake;
- suppress duplicates and stale attempts.

It must not:

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

A deterministic rejection records:

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

The courier may then wake the same Worker with a bounded report-repair request. A repair wake uses the same run, grants no new task authority, permits only a new immutable report attempt, and stops after the configured conservative attempt ceiling or any authority conflict.

### Department HQ review

A schema-valid Worker report triggers the owning Department HQ review path according to verification mode.

- `IMMEDIATE_HQ`: wake the owning HQ promptly.
- `ROUTINE_BATCH`: enter the existing department review queue unless a hold, conflict, or time-sensitive condition justifies an immediate wake.
- `AUTOMATIC`: permitted only when the authoritative procedure defines an explicit deterministic postcondition.

The owning Department HQ reviews:

1. report integrity and correlation;
2. authority and scope compliance;
3. evidence sufficiency;
4. the actual work where independent inspection is possible;
5. unresolved uncertainty, holds, or approval requirements.

HQ writes one immutable receipt with one review state:

- `VERIFIED`
- `REJECTED`
- `REPAIR_REQUIRED`
- `ROB_VALIDATION_REQUIRED`

HQ review never closes the source advisory automatically.

### Rob-validation path

When the work cannot be independently verified by the owning HQ, the HQ receipt must state:

- report integrity result;
- authority-compliance result;
- evidence checked;
- why direct verification is unavailable;
- the exact observation or decision Rob must provide.

The result is not ready for ordinary Chief of Staff consumption until Rob records `VERIFIED` or `REJECTED`, unless an urgent hold or elevation requires coordination.

### Chief of Staff consumption boundary

The courier never wakes Chief of Staff.

A separately authorized ChatGPT scheduled task may periodically inspect only consumption-ready states, including:

- HQ-verified completion;
- Rob-verified completion;
- HQ-confirmed `REPORT_AND_HOLD`;
- HQ-confirmed `ELEVATE_FOR_APPROVAL`;
- verification rejection requiring coordination;
- stale or unresolved reviews that meet a defined reporting threshold.

The task may synthesize meaningful changes for Rob and identify source-owner follow-through. It must not consume raw Worker reports as truth, replace Department HQ review, create authority, or close source advisories automatically.

## Runtime State Model

These are technical runtime states, not advisory lifecycle states:

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

## Implemented Foundation

Lifecycle State: Implemented

Implemented foundation includes:

- exact Worker and source URL verification;
- stable Worker-history hydration checks;
- empty-composer and no-generation preflight;
- one-tab browser navigation;
- shared pause and one-job execution gate;
- canonical advisory discovery;
- existing SQLite execution history and HQ review views;
- Worker Operations dashboard surface;
- zero-authority courier self-test;
- focused browser, runtime, application, and UI tests;
- visible retirement of the former prompt-and-scheduler UI while preserving rollback definitions.

`ADV-20260720-047` revision 2 remains architecture-discovery evidence. It must not be retried or treated as Package E completion proof.

## Slice 2: Dispatch-Only Courier

Lifecycle State: Implemented / Locally validated / Live dispatch partially validated

Implemented behavior:

1. preserves exact source and destination URLs;
2. waits for exact Worker history, identity, and composer hydration;
3. sends one correlated bounded assignment;
4. proves the correlated user turn exists;
5. records `DISPATCH_SUBMITTED`, user-turn evidence, return status, and dispatch receipt on the existing execution row;
6. releases the browser gate without waiting for Worker output;
7. performs no assistant-response capture or interpretation;
8. preserves stop-before-send and no-blind-retry behavior;
9. blocks duplicate sends after confirmed submission or recorded submission uncertainty;
10. retains a zero-authority courier self-test.

Implementation locations include:

- `apps/lifeos-dashboard/automation/chatgpt_worker_browser_dispatch.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_dispatch_runtime.py`;
- dispatch-only runtime installation in `apps/lifeos-dashboard/lifeos_dashboard/__init__.py`;
- updated Worker Operations UI and focused tests.

Local validation evidence reported by Rob on 2026-07-21:

- focused validation result: **40 passed, 13 warnings**;
- LifeOS Dashboard relaunched successfully;
- browser state ready;
- execution gate ready;
- Worker Operations ready.

Live evidence from `ADV-20260721-048`:

- the courier reached `engineering_worker` and the correlated wake succeeded;
- the Worker continued independently and completed;
- the courier did not return the controlled browser tab to Engineering HQ;
- no resend is authorized because the dispatch succeeded;
- the exact return-to-source postcondition remains unproven and requires repair.

Slice 2 is not fully live-validated until a later bounded wake proves successful correlated dispatch, exact source-room return, and gate release without duplicate execution.

## Slice 3: Engineering Worker Result-Outbox Pilot

Lifecycle State: Implemented / Locally validated / Bounded live artifact validated

Implemented behavior:

1. versioned Worker report, rejection, HQ-review, and Rob-validation JSON schemas;
2. deterministic paths and immutable attempt rules;
3. correctly typed canonical examples;
4. one canonical result-submission procedure;
5. Engineering-only create-once current-run reporting authority through the exact task procedure and advisory;
6. advisory validation of contract version, attempt, deterministic path, flags, tool, and exact write scope;
7. overwrite, deletion, unrelated writes, re-execution, and scope expansion prohibitions;
8. focused parser and schema tests, including the prior wrong-type `profile_version` defect;
9. preservation of commit, blob, path, and stored-content evidence;
10. `IMMEDIATE_HQ` remains pending after Worker report creation.

Local validation evidence reported by Rob:

- the result-outbox validation gate passed;
- the dashboard relaunched live and ready.

Bounded live evidence from `ADV-20260721-048`:

- exact path: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260721-048-R1/report-001.json`;
- creation commit: `fbe75f13bc1b3a2dd35815e0d145c25da8695e22`;
- blob SHA: `f218d63519d38352b8aee4a790ed20807b1bebee`;
- controlled outcome: `IMPLEMENT`;
- verification state: `pending`;
- numeric and boolean JSON fields are correctly typed;
- the only durable write was the authorized report artifact;
- no external action, advisory lifecycle change, re-execution, or scope expansion occurred;
- Rob observed the successful package outbox in the live dashboard;
- the Worker could not provide a separate canonical SHA-256 content checksum through its authorized connector surface, so the ingester must calculate it;
- deterministic ingestion and formal Engineering HQ signoff have not occurred.

The live artifact satisfies the bounded Slice 3 outbox proof. `ADV-20260721-048` remains OPEN until deterministic ingestion and required HQ review establish its accepted state.

## Slice 4: Result Ingester and Repair Wakes

Lifecycle State: Next

Required behavior:

1. discover new result artifacts without browser response scraping;
2. correlate them to the canonical assignment and existing SQLite runtime state;
3. validate schema, identity, revision, authority, scopes, tools, evidence, and checksums;
4. calculate canonical content checksum from the stored artifact;
5. update the existing runtime state without creating another ledger;
6. write deterministic rejection artifacts for invalid reports;
7. queue bounded report-repair wakes;
8. ensure repair wakes authorize report correction only;
9. suppress duplicate and stale attempts;
10. route exhausted or conflicted repairs to the owning HQ;
11. expose actionable status and evidence in Worker Operations.

Completion condition:

- the existing valid ADV-048 report advances through `REPORT_DISCOVERED` and `REPORT_VALIDATED` on its existing execution row;
- an intentionally malformed synthetic report is rejected;
- the same Worker can be woken for report repair without repeating the work;
- a corrected immutable attempt is accepted;
- no second runtime ledger is created.

## Slice 5: Owning-HQ Wake and Verification Receipts

Lifecycle State: Planned after Slice 4

Required behavior:

1. derive the owning HQ from canonical Worker and assignment state;
2. wake the owning HQ only after report validation and according to verification mode;
3. return the courier immediately after the HQ wake;
4. provide exact report and evidence pointers without copying detailed truth into wake text;
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
- immediate courier release and exact source-room return;
- immutable Worker result submission;
- deterministic ingester validation;
- repair loop if deliberately exercised;
- owning-HQ wake;
- HQ work inspection where possible;
- Rob validation where HQ verification is unavailable or intentionally simulated;
- one final consumption-ready state;
- duplicate suppression;
- source-owner lifecycle separation.

The proof must require no manual prompt or report copying by Rob.

## Slice 7: Chief of Staff Scheduled Consumption and Unattended Operation

Lifecycle State: Deferred until Slice 6 passes and Rob separately authorizes activation

Potential bounded work includes:

- a read-only scheduled Chief of Staff task that checks consumption-ready evidence and source advisory state;
- meaningful-change filtering and no-change silence;
- a proven deduplication method that does not create duplicate truth;
- scheduled reporting of verified work, holds, elevations, rejected verification, stale reviews, and source-owner review readiness;
- local background result ingestion and courier wake processing;
- restart recovery and actionable diagnostics;
- rollback-window retirement of obsolete response-capture and legacy UI paths.

This slice must not generate authority, select priorities, create advisories, treat unverified reports as truth, replace Department HQ review, or automatically close source-owned advisories.

## Human-Readable Envelope Requirement

Before ordinary real Worker activation beyond bounded pilots, retain a display-only human-readable envelope summary derived from the same `ExecutionEnvelope` object.

It must show Worker, task and revision, procedure and version, authorization source, verification mode, wrapper ID, run ID, and bounded instruction. It must remain non-authoritative, have no independent edit or parse path, and be covered by parity tests.

## Explicit Non-Scope

Package E does not authorize:

- changing another department's files;
- changing shared governance or universal boot files without coordinated authority;
- granting every Worker standing GitHub write authority;
- closing `ADV-20260718-042`, `ADV-20260720-047`, `ADV-20260721-048`, or any other source-owned advisory automatically;
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

1. one real bounded assignment is dispatched without Rob acting as courier;
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

1. inspect the existing ADV-048 execution row and dispatch receipt without resending the advisory;
2. repair and regression-test exact return-to-source behavior while preserving the successful send as nonretryable;
3. implement Slice 4 deterministic ingestion using the existing ADV-048 `report-001.json` as the first valid live artifact;
4. leave formal Engineering HQ signoff and advisory closure pending until ingestion exists.

## Review Condition

Engineering HQ reviews each slice against this packet. Rob remains final authority for new authority, shared-contract changes, cross-department rollout, scheduled-task activation, and Package E closeout.