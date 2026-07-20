# Package E Implementation Packet

Updated: 2026-07-20
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal
Record Class: Engineering implementation packet

## Title

**Worker Operations and Receiver Integration**

## Authorization Basis

Rob explicitly authorized the Automation Command Center UI rebuild on 2026-07-20 and agreed that the resulting work is Package E after Package D closeout.

This packet authorizes only the bounded Engineering-owned implementation described here. It does not create Worker authority, advisory authority, cross-department authority, recurring task-generation authority, or source-owner closure authority.

## Objective

Complete the operational bridge from an already-authorized canonical Worker assignment to a verified Department HQ review without requiring Rob to manually carry text or evidence between ChatGPT rooms.

The intended chain is:

1. one canonical advisory, task, or approved source authorizes a bounded assignment;
2. the Worker Operations surface resolves the exact execution-ready revision;
3. the one-tab browser courier preserves the current HQ chat, visits the exact Worker chat, sends the bounded wrapper, captures the correlated response, and returns to HQ;
4. transport evidence is attached to the existing `execution_history` row;
5. the captured Worker report is parsed without treating its self-reported outcome as authority;
6. the receiver validates the assignment, profile, procedure, revision, parameters, scopes, tools, evidence, and controlled outcome;
7. the same execution row records the accepted controlled outcome and verification state;
8. the owning Department HQ performs the required review;
9. the source owner retains advisory lifecycle and closure authority.

## Canonical Architecture

### One owner and one durable run record

- Engineering HQ owns the technical machinery and this implementation packet.
- Department HQs own Worker profiles, procedures, authority, and domain judgment.
- Source owners own advisory lifecycle and closure.
- SQLite `execution_history` remains the sole durable runtime record for transport, response evidence, receiver outcome, and verification state.
- GitHub remains authoritative for packages, profiles, procedures, advisories, tasks, decisions, and durable Engineering state.

No second execution, response, outcome, queue, wake, or verification ledger may be created.

### Browser transport boundary

The browser courier may:

- operate only against canonical exact ChatGPT conversation URLs;
- temporarily borrow the one known Engineering HQ tab after preflight;
- require an empty composer and no active generation;
- preserve the source HQ URL;
- navigate to the exact registered Worker URL;
- send one exact bounded wrapper;
- capture one correlated assistant response;
- return to the exact source URL;
- disconnect after the run;
- stop before send or preserve visible forensic state after uncertain send status.

It must not:

- act on an arbitrary tab or conversation;
- reinterpret, edit, approve, broaden, or close the assignment;
- navigate away from an occupied composer;
- blind-retry after uncertain submission;
- treat transport success as semantic acceptance;
- leave the browser in the Worker room after a clean success.

### Receiver boundary

A Worker-reported `IMPLEMENT`, `REPORT_AND_HOLD`, or `ELEVATE_FOR_APPROVAL` is captured evidence, not accepted authority.

The receiver must independently validate the existing successful send row and the canonical assignment semantics before recording a controlled outcome on that same row.

`IMMEDIATE_HQ` work must remain pending until Department HQ review. Neither receiver finalization nor HQ review closes the source advisory automatically.

## Implemented Slice 1: One-Tab Courier and Worker Operations Cockpit

Lifecycle State: Implemented / Live validated

Implemented components include:

- `apps/lifeos-dashboard/automation/chatgpt_worker_browser_roundtrip.py`;
- `apps/lifeos-dashboard/automation/run_synthetic_worker_browser_pilot.py`;
- `apps/lifeos-dashboard/automation/run_synthetic_worker_browser_pilot.cmd`;
- `apps/lifeos-dashboard/automation/validate_and_run_worker_operations.cmd`;
- `apps/lifeos-dashboard/lifeos_dashboard/worker_operations.py`;
- Worker Operations API routes in `apps/lifeos-dashboard/lifeos_dashboard/main.py`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/worker-operations.js`;
- `apps/lifeos-dashboard/lifeos_dashboard/static/worker-operations.css`;
- the Worker Operations dashboard surface;
- focused browser, backend, application, and UI tests.

The visible legacy prompt-and-scheduler controls were retired from the dashboard. Their backend definitions remain intact for rollback. The legacy scheduler is dormant by default unless `LIFEOS_LEGACY_SCHEDULER_ENABLED` is explicitly enabled.

Live evidence reported by Rob:

- synthetic one-tab browser wrapper: `SYNTH-BROWSER-WRAP-1784575398-7e1b422eac`;
- run: `SYNTH-BROWSER-RUN-1784575398-7e1b422eac`;
- exact captured acknowledgement from `conversation-turn-27`;
- `returned_to_source: true`;
- `durable_authority_created: false`;
- dashboard courier self-test later returned to HQ with `conversation-turn-29`;
- no manual copy-and-paste courier step was required.

Slice 1 proves the browser transport and dashboard control surface. It does not yet prove automatic receiver acceptance of a captured real Worker report.

## Slice 2: Captured Response to Semantic Receiver Integration

Lifecycle State: Next

### Required behavior

For one execution-ready Worker assignment:

1. capture the correlated assistant response and browser receipt;
2. preserve raw response evidence without creating a second ledger;
3. parse exactly one controlled-outcome marker or hold for inspection;
4. reconstruct or load the canonical receiver assignment from the authoritative advisory, profile, and procedure;
5. validate the successful transport row and exact envelope metadata;
6. run receiver preflight;
7. accept only a newer valid revision;
8. translate the Worker report into bounded `ExecutionEvidence` without inventing missing evidence;
9. finalize one same-row controlled outcome;
10. place `IMMEDIATE_HQ` work in the existing HQ review queue;
11. preserve source-owner closure authority.

### Fail-closed conditions

Return or preserve `REPORT_AND_HOLD` when:

- no unique controlled outcome is present;
- required evidence fields cannot be parsed or verified;
- the response conflicts with the envelope, profile, procedure, advisory, scopes, tools, or authorization;
- duplicate or stale processing is detected;
- the transport row is missing, ambiguous, failed, or mismatched;
- actual actions cannot be verified;
- a required source cannot be loaded;
- the run requires Department HQ judgment beyond the receiver’s contract.

Use `ELEVATE_FOR_APPROVAL` only when the Worker report or receiver validation identifies a real need for Rob’s new authority, exception, spending, permission, cross-department authority, or material architecture decision.

## Slice 3: Real End-to-End Operations Proof

Lifecycle State: Planned after Slice 2

Run one execution-ready, bounded Engineering-owned advisory through:

- canonical discovery;
- one-tab browser dispatch;
- correlated response capture;
- same-row transport evidence;
- semantic receiver validation;
- exactly one controlled outcome;
- `IMMEDIATE_HQ` review;
- duplicate suppression;
- source-owner lifecycle separation.

Completion evidence must include exact run, wrapper, Worker, task, revision, procedure, authorization, source paths, response turn, receiver outcome, evidence references, verification state, and what did not occur.

The proof must require no manual copy-and-paste transport or response reconciliation by Rob.

## Slice 4: On-Demand and Unattended Orchestration

Lifecycle State: Deferred until Slice 3 passes

Potential bounded work includes:

- on-demand browser launch and shutdown around Worker runs;
- execution-ready advisory scanning;
- scheduled dispatch under existing authority;
- recovery after browser or dashboard restart;
- actionable diagnostics and notification;
- rollback-window retirement of unused legacy UI/backend paths.

This slice must not generate authority, select priorities, create advisories, or automatically close work. Recurring dispatch requires an already-approved task-generation and authorization model.

## Human-Readable Envelope Requirement

Before ordinary real Worker activation beyond pilots, add a display-only human-readable envelope summary derived from the same `ExecutionEnvelope` object.

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

- changing another department’s files;
- changing shared governance or universal boot files;
- closing `ADV-20260718-042` or any other source-owned advisory;
- automatic Engineering HQ judgment;
- automatic advisory acknowledgement, implementation, source verification, or closure;
- autonomous task selection or prioritization;
- new Worker profiles, permissions, connectors, spending, or external systems;
- recurring authority generation;
- a competing runtime ledger;
- destructive removal of legacy data or schedules;
- arbitrary browser control;
- public, irreversible, privacy-sensitive, or high-consequence actions.

## Package Completion Condition

Package E may close only when:

1. one real bounded execution-ready assignment completes without Rob acting as manual courier;
2. the exact Worker response is captured and correlated;
3. receiver validation records exactly one same-row controlled outcome;
4. required evidence is present and truthful;
5. `IMMEDIATE_HQ` review is completed through the existing verification path;
6. duplicate execution and silent scope expansion remain prevented;
7. browser uncertainty fails closed;
8. source-owner lifecycle authority remains separate;
9. the human-readable envelope requirement is resolved or explicitly deferred by Rob;
10. the rollback or retirement decision for legacy automation surfaces is recorded.

## Smallest Useful Next Action

Implement Slice 2: captured Worker response to semantic receiver validation and same-row controlled outcome, with focused tests that prove missing, conflicting, duplicate, stale, and incomplete reports hold safely.

## Review Condition

Engineering HQ reviews each slice against this packet. Rob remains final authority for new scope. Package E closure requires an explicit closeout decision and current evidence.