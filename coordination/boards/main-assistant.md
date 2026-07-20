# Chief of Staff HQ Advisory Board

Updated: 2026-07-19
Purpose: Canonical advisory text sourced from Chief of Staff HQ, including formal advisories arising from LifeOS HQ meetings. The retained filesystem path remains `coordination/boards/main-assistant.md`.

## Open Advisories

### ADV-20260719-045 — Acknowledge the project and chat source memory architecture discovery

- Date: 2026-07-19
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Lifecycle State: OPEN
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department and Owner: Life OS Maintenance HQ
- Record Class: Architecture discovery and bounded awareness advisory
- Authorization Basis: Rob explicitly directed Chief of Staff HQ to issue this advisory
- Requested Target Action: Consume the discovery, acknowledge it, close this advisory under standard advisory procedures, and report completion to Rob
- Prohibited Scope: Do not generate a handbook, alter global boot or source rules, create implementation work, open a new loop, modify project sources, or perform any other architecture change under this advisory
- Completion Condition: Life OS Maintenance HQ confirms it has consumed the findings and boundaries, updates this advisory and the Advisory Index through the appropriate acknowledgement and closure states, creates no duplicate implementation record, and reports the closed result to Rob

#### Purpose

Preserve and transfer a verified ChatGPT Projects context-management discovery to Life OS Maintenance HQ before Rob separately authorizes handbook-generation work.

This advisory is intentionally informational and bounded. It carries no implementation request beyond normal advisory acknowledgement and closure. Rob will issue separate instructions for Maintenance HQ to generate its own room handbook first and later generate a role-neutral global handbook for promotion to the project level.

#### Verified Discovery

LifeOS HQ tested the current ChatGPT Projects source and Library behavior and observed the following:

1. A response generated inside a project chat can be promoted by Rob into the project's shared sources.
2. The first promoted-response test reported success immediately, but the source did not appear in the visible project-source list until the ChatGPT app was closed and restarted.
3. After restart, the promoted response appeared in project sources and was accessible as shared project context.
4. A generated Markdown artifact created inside the LifeOS HQ chat appeared automatically in the Library associated with that chat.
5. The generated artifact `LIFEOS_HQ_CHAT_HANDBOOK.md` is available to this Hub chat for later reference.
6. The Hub handbook contains room identity, department tags, authority boundaries, source-system rules, write safety, advisory routing, Worker interfaces, Chat-versus-Work boundaries, context recovery, current state, and a canonical GitHub source manifest.
7. The observed behavior provides a practical durable-context layer that can reduce ordinary context loss and the need to reconstruct a room from a full boot.

#### Memory-Layer Model

The discovery supports a layered context architecture:

##### 1. GitHub canonical truth

GitHub remains the authoritative durable source for:

- operating rules and contracts;
- room and department identity;
- handoffs, status, and open loops;
- advisory state and canonical advisory text;
- Worker profiles and authority boundaries;
- architecture, decisions, validated knowledge, and meaningful history.

No ChatGPT source, Library artifact, promoted response, dashboard view, or automation copy may replace GitHub as the canonical record.

##### 2. Project-level shared sources

Project sources feed shared context to chats inside the project.

Therefore project-level material must remain role-neutral and safe for every room. It may contain global Life OS rules, organization, source boundaries, command language, durable-write gates, common advisory logic, Worker ceilings, and conflict procedures.

Project-level sources must not assign the active chat a specific department or Hub identity. A Hub-specific handbook promoted to project level could cause specialist chats to adopt Hub authority or behavior. A department-specific handbook promoted to project level could cause sibling rooms to inherit the wrong role, ownership, or backlog.

Current documented Plus-plan project-file capacity observed during research on 2026-07-19 is 20 files per project. Treat this as a product constraint subject to change and verify it before future capacity planning.

##### 3. Chat-specific sources and generated artifacts

A room-specific handbook may live as a generated artifact or chat-associated source for one chat.

This layer is appropriate for:

- exact room or department identity;
- local `[Department]` voice tags;
- ownership and exclusions;
- local procedures and decision rules;
- current handoff, status, and open-loop context;
- local Worker interfaces;
- room-specific context-recovery instructions.

The Hub handbook test demonstrates that a room may carry a comprehensive local context artifact without exposing its identity to every project chat.

Library presence alone should not be treated as universal project availability. Confirm that the intended chat can retrieve or reference the artifact. When a new or replacement chat is created, attach, reference, or otherwise make the intended room handbook available and verify retrieval.

##### 4. Conversation

Conversation remains the temporary reasoning, drafting, deliberation, and execution-coordination layer.

Conversation may use the local handbook to recover identity and procedures without manufacturing new durable truth.

#### Implications for Boot and Continuity

The discovery may eliminate one major cause of routine rebooting: gradual loss of room identity, department boundaries, procedures, and important context.

A room with a current local handbook can often recover from mild context drift through a compact instruction such as:

> Read your room handbook and return to your documented identity, authority, source boundaries, and operating procedures.

Full Boot remains necessary or prudent when:

- a fresh or replacement chat is created without reliable local context;
- the room handbook is missing, stale, corrupted, or unavailable;
- the conversation becomes technically degraded or excessively bloated;
- a major architecture migration changes the universal kernel;
- authoritative sources conflict;
- a governance-sensitive action requires current canonical verification;
- connector behavior indicates session degradation.

Boot remains read-only context loading. Sync remains read-only comparison. Local handbooks reduce routine loading friction but do not authorize maintenance or external actions.

#### Handbook Architecture Boundaries

Future generated handbooks should follow these boundaries:

1. **GitHub first:** Update and verify canonical GitHub sources before regenerating a handbook.
2. **Generated mirror:** Label every handbook as a generated, read-only context mirror rather than authoritative truth.
3. **Source manifest:** Record the source repository, source paths, generation date, handbook version, and repository commit or comparable snapshot identifier.
4. **Conflict rule:** State that GitHub wins after visible reconciliation when the handbook conflicts with canonical files.
5. **No manual canonical edits:** Manual edits to the artifact do not change GitHub authority.
6. **Role isolation:** Room identity and local state stay in chat-specific handbooks. Shared project sources remain role-neutral.
7. **Stable versus volatile content:** Separate stable operating rules from dated current-state snapshots where practical.
8. **One artifact per intended scope:** Avoid multiple competing room handbooks or numbered duplicates.
9. **Verified publication:** Confirm the target chat or project can retrieve the newly published source.
10. **Retire stale copies:** Remove or stop referencing superseded artifacts so retrieval does not become ambiguous.

#### Publication Paths Observed

Two practical publication paths now exist:

##### Promoted response to project sources

1. Generate a reviewed, role-neutral response inside a project chat.
2. Rob uses the response menu to promote or save it to project sources.
3. Restart or refresh the app if the source does not immediately appear.
4. Verify the promoted source from the project-source list and, when useful, from another project chat.
5. Avoid repeated promotion before refresh, because a delayed display could tempt duplicate creation.

##### Generated artifact to a room's Library/context

1. Generate the handbook or context artifact inside the intended chat.
2. Confirm the file appears in Library.
3. Confirm that the intended room can reference the file.
4. Use the artifact as the room's local context anchor.
5. Regenerate from GitHub when meaningful canonical changes occur.
6. Retire stale duplicate copies.

If an uploaded project file is being replaced rather than a response being promoted, delete the old project file before uploading the fresh file with the canonical filename. Otherwise the interface may preserve both by adding a numerical suffix and create ambiguous competing sources.

#### Proposed Long-Term Topology

The discovery supports the following topology, subject to separate authorization and implementation:

```text
GitHub canonical sources
        ↓
Maintenance-generated context artifacts
        ↓
Shared project source
  - role-neutral global operating handbook
        ↓
Chat-specific room handbooks
  - LifeOS HQ
  - Chief of Staff HQ
  - Life OS Maintenance HQ
  - Engineering HQ
  - Finance HQ
  - Business HQ
  - Office Leaks HQ
  - Wellness HQ
  - activated Worker chats as justified
        ↓
Active conversation and bounded execution
```

This creates one canonical durable layer, one shared role-neutral project layer, and many isolated room-specific context layers.

#### Expected Benefits

Potential benefits include:

- less routine boot overhead;
- faster recovery from mild identity drift;
- reduced dependence on desktop composer transport for large boot prompts;
- fewer failures from copied or truncated boot text;
- more consistent department tags and authority boundaries;
- easier creation of replacement chats;
- durable specialist expertise without contaminating sibling rooms;
- a human-reviewed promotion gate for shared project context;
- easier synchronization through regenerated artifacts;
- fewer reasons to keep excessively long, degraded conversations alive merely to preserve context.

These benefits are architectural expectations supported by the initial tests. They should be validated through ordinary use rather than treated as proof that every context-loss mechanism is solved.

#### Risks and Controls

##### Role contamination

Risk: a Hub or department handbook promoted to project level could make every chat adopt the wrong identity.

Control: project-level sources remain role-neutral; room identity remains chat-specific.

##### Duplicate truth

Risk: GitHub, project sources, Library files, and conversation could become competing detailed ledgers.

Control: GitHub remains canonical; artifacts are labeled generated mirrors; other systems contain concise context or publication copies only.

##### Stale context

Risk: a handbook may continue to load old rules or state after GitHub changes.

Control: include generation metadata and source manifests; regenerate after meaningful canonical changes; use Sync or Boot when staleness is suspected.

##### Duplicate or numbered files

Risk: replacement uploads may create `filename (2)` or similar copies.

Control: generate and verify the replacement first, delete the old project file, then upload the fresh canonical filename and verify read-back.

##### False publication failure

Risk: delayed UI refresh may make a successful promotion appear missing.

Control: restart or refresh the app and verify before retrying.

##### Library over-assumption

Risk: a file may exist in Library but not be reliably available to every intended chat.

Control: verify retrieval in the target room and explicitly attach or reference the artifact when necessary.

##### Boot removal overreach

Risk: treating the handbook as a total replacement for canonical boot and verification.

Control: redefine Boot as an exception and recovery tool, not abolish it. Governance-sensitive work still verifies current GitHub authority.

##### Uncontrolled handbook churn

Risk: regenerating artifacts after trivial edits creates noise and version confusion.

Control: no meaningful canonical change means no artifact replacement. Refresh only when identity, authority, procedures, interfaces, or current-state context materially changes.

#### Current Evidence Artifact

LifeOS HQ generated:

- `LIFEOS_HQ_CHAT_HANDBOOK.md`
- generated 2026-07-19;
- source repository `recoveryrob83-lab/Penny-Long-Term-Memory`;
- repository snapshot recorded in the artifact;
- local artifact SHA-256 recorded at generation time;
- confirmed by Rob to appear in the Library for the Hub chat and remain available for reference.

The artifact includes all canonical Hub perspective tags:

- `[MAIN]`
- `[MAINTENANCE]`
- `[ENGINEERING]`
- `[FINANCE]`
- `[BUSINESS]`
- `[OFFICE LEAKS]`
- `[WELLNESS]`

This evidence demonstrates the local-handbook path for the Hub. It does not authorize copying that Hub identity into shared project sources.

#### Reserved Future Work

Rob stated the intended next sequence:

1. direct Life OS Maintenance HQ to generate its own room handbook;
2. then direct Maintenance HQ to generate a role-neutral global handbook;
3. review the global handbook;
4. promote the global handbook to project sources;
5. verify cross-chat availability and role neutrality.

Those steps are reserved for separate direct authorization. This advisory must not initiate them.

#### Required Maintenance Response

Life OS Maintenance HQ should:

1. read and consume this advisory;
2. confirm understanding of the verified observations, architecture boundaries, risks, controls, and reserved future sequence;
3. acknowledge the advisory;
4. close it under standard operating procedures without marking unrelated implementation complete;
5. avoid creating a duplicate open loop, advisory, notebook implementation plan, handbook, or global rule under this advisory;
6. report the acknowledgement and closure to Rob, including the exact advisory state and any advisory/index files changed solely for lifecycle closure.

No other action is requested or authorized.

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