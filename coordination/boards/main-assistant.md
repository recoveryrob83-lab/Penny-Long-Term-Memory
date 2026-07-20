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

### ADV-20260719-045 — Acknowledge the project and chat source memory architecture discovery

- Date: 2026-07-19
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Lifecycle State: CLOSED
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Acknowledged: 2026-07-19
- Closed: 2026-07-19
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department and Owner: Life OS Maintenance HQ
- Record Class: Architecture discovery and bounded awareness advisory

#### Acknowledgement and Outcome

Life OS Maintenance HQ consumed and acknowledged the verified ChatGPT Projects context-memory discovery and its boundaries:

- promoted responses may become shared project sources, with application refresh or restart sometimes required before visible confirmation;
- generated artifacts may provide durable room-specific Library context when retrieval is verified in the intended room;
- GitHub remains the canonical durable source;
- shared project sources must remain role-neutral;
- room identity, local procedures, and local context belong in chat-specific handbooks or artifacts;
- local handbooks may reduce routine boot overhead but do not replace Boot for fresh, stale, conflicted, degraded, or governance-sensitive contexts;
- replacement publication must avoid duplicate or numbered competing copies;
- handbook publication must include source manifests, conflict rules, meaningful-refresh discipline, and verified retrieval;
- the reserved sequence begins with a Maintenance room handbook and later a role-neutral global handbook only after separate direct authorization from Rob.

No handbook was generated. No boot rule, source rule, project source, architecture file, open loop, notebook plan, implementation advisory, or duplicate durable record was created. The advisory was informational only and is now acknowledged and closed.

### ADV-20260719-043 — Create canonical LifeOS operational and Worker protocols

- Lifecycle State: CLOSED
- Acknowledged: 2026-07-19
- Implemented: 2026-07-19
- Source Verified: 2026-07-19
- Closed: 2026-07-19

Life OS Maintenance HQ created the canonical shared execution protocol and Worker contract, integrated one HQ and Worker boot entry point, preserved the universal-kernel order, and retained the two root Worker pilots as compatibility packages.

### ADV-20260718-041 — Create a global Trello connector write SOP

- Lifecycle State: CLOSED
- Implemented: 2026-07-18
- Acknowledged: 2026-07-18
- Closed: 2026-07-18

Life OS Maintenance HQ extended the existing global Connector Reliability Operating Pattern with the Trello false-negative write protocol, live read-back, duplicate prevention, truthful reporting, and source-boundary protections.

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