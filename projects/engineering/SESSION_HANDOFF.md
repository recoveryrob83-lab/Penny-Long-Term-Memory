# Engineering HQ Session Handoff

Updated: 2026-07-20
Project: Engineering HQ
Purpose: Current handoff for technical architecture, Package E Worker Operations and Receiver Integration, browser automation, connector reliability, the LifeOS Dashboard, and bounded Worker execution infrastructure.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Closed / Package E Slice 1 Live Validated / Slice 2 Receiver Integration Next
- Primary Systems: GitHub, ChatGPT Department and Worker rooms, local LifeOS Dashboard, SQLite Command Center execution history, Engineering advisory board, Advisory Index when needed, and other source systems only when explicitly required
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md` whenever Worker Operations, browser courier, response capture, receiver integration, HQ review, unattended orchestration, or legacy automation retirement is in scope.
7. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` only when Package D history, its runtime design, validation evidence, or closeout is directly relevant.
8. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker routing, authority, or execution behavior is in scope.
9. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
10. Read current Engineering notebook records only when directly referenced by active work.
11. Keep connector and browser work small, explicit, fail-closed, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, prompt systems, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own canonical shared Worker governance, global boot coherence, profile conventions, another department’s Worker authority, source-owner advisory lifecycle, or domain judgment. Life OS Maintenance HQ owns shared governance surfaces. Departments own Worker profiles, procedures, judgment, and authority. Engineering owns technical routing, transport, logging, duplicate suppression, response capture, verification mechanics, runtime evidence, tests, and reliability infrastructure.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared governance and global memory hygiene to Life OS Maintenance HQ, and wellbeing or sustainability judgment to Wellness HQ.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The operating model is:

- the Department HQ owns the Worker profile, authority, procedures, and domain judgment;
- GitHub holds the canonical profile, approved procedures, task or advisory state, and durable evidence;
- the Worker chat receives a bounded envelope, reads required canonical GitHub sources, validates the request, performs only authorized work, and returns one controlled outcome with evidence;
- browser and Python infrastructure preserve exact delivery, correlation, response capture, duplicate suppression, and evidence;
- the receiver independently validates the assignment and evidence before accepting a controlled outcome;
- the Department HQ performs required review and retains ownership;
- the source owner retains advisory lifecycle and closure authority.

Python and browser automation are not the Worker. A Worker-reported outcome is evidence, not accepted authority.

## Chat and Work Model

Use regular Chat for architecture, planning, GitHub synchronization, prompt and procedure work, debugging analysis, advisories, and bounded connector updates.

Use Work for substantial coding, local terminal work, full test execution, browser control, packaging, or complex artifacts.

Never claim an action, test, deployment, browser round trip, or connector write occurred without current evidence.

## Primary Current Work Package

### Package E: Worker Operations and Receiver Integration

Lifecycle State: Active
Priority: Normal

Canonical packet:

- `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`

Objective:

Complete the bridge from an already-authorized canonical Worker assignment through one-tab browser dispatch, correlated response capture, semantic receiver validation, one same-row controlled outcome, and Department HQ review without Rob manually carrying text or evidence between rooms.

### Slice 1: One-Tab Courier and Worker Operations Cockpit

Status: Implemented and live validated.

Current implementation includes:

- exact Engineering HQ source-chat preservation;
- exact `Engineering_Worker` URL and title verification;
- empty-composer and no-generation preflight;
- one-tab navigation to the Worker and return to the exact source URL;
- correlated request and response markers;
- captured assistant response and turn ID;
- zero-authority courier self-test;
- Worker Operations dashboard health, dispatch, route, history, and review visibility;
- legacy prompt-and-scheduler UI removed from view;
- legacy definitions preserved for rollback;
- legacy scheduler dormant by default.

Live evidence reported by Rob:

- `SYNTH-BROWSER-WRAP-1784575398-7e1b422eac`;
- `SYNTH-BROWSER-RUN-1784575398-7e1b422eac`;
- exact acknowledgement captured at `conversation-turn-27`;
- `returned_to_source: true`;
- `durable_authority_created: false`;
- dashboard self-test returned to HQ with `conversation-turn-29`.

### Slice 2: Captured Response to Semantic Receiver Integration

Status: Next valid action.

Implement the smallest bounded bridge that:

1. stores captured response evidence on the existing execution row;
2. parses one Worker-reported controlled outcome without accepting it automatically;
3. loads or reconstructs the canonical receiver assignment from the advisory, profile, and procedure;
4. validates exact transport history, identity, revision, parameters, authority, scopes, tools, and procedure;
5. accepts only a newer valid revision;
6. creates `ExecutionEvidence` only from verifiable report content;
7. records exactly one same-row controlled outcome;
8. sends `IMMEDIATE_HQ` work to the existing review path;
9. preserves source-owner closure authority;
10. holds safely on missing, conflicting, stale, duplicate, unauthorized, or unverifiable evidence.

## Package D Closeout

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Closed
Closed: 2026-07-20

Package D’s seven technical slices, synthetic backend pilot, desktop transport proof, Engineering Worker profile and route, canonical read-only procedure, and first live operational advisory pilot are complete.

Canonical historical packet:

- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`

Primary closeout evidence:

- `ADV-20260720-046` revision 1 returned `REPORT_AND_HOLD` when required boot read scope was missing;
- commit `8cfa874` repaired safe draft/send transport-row ambiguity;
- revision 2 authorized the complete boot chain and returned `IMPLEMENT`;
- the Worker read exact canonical sources and performed no writes;
- the existing execution row preserved receiver acceptance, controlled outcome, evidence, and verified `IMMEDIATE_HQ` review;
- duplicate processing and further verification wakes are suppressed;
- `ADV-20260720-046` is closed, implemented, and source verified;
- no recurring authority, second ledger, automatic HQ judgment, or automatic advisory closure was created.

`ADV-20260718-042` remains open under its source owner. Package D closure does not change its lifecycle.

## Package E Boundary

Package E may build the technical orchestration path. It must not:

- invent or broaden authority;
- select priorities or create assignments;
- modify another department’s files;
- modify shared governance without coordinated authority;
- create a second run, response, outcome, verification, wake, or queue ledger;
- treat browser success as semantic acceptance;
- auto-verify `IMMEDIATE_HQ` work;
- auto-close advisories;
- control arbitrary browser tabs;
- blind-retry uncertain sends;
- create recurring Worker authority without an approved task-generation model.

## Human-Readable Envelope Requirement

Before ordinary real Worker activation beyond pilots, add a display-only human-readable summary beside the canonical JSON envelope.

The summary must derive all fields from the same `ExecutionEnvelope`, remain non-authoritative, have no independent edit or parse path, and be covered by parity tests.

## Browser and Composer Boundary

The preferred Package E path is the one-tab Edge/CDP courier.

Required safeguards:

- exact canonical source and Worker URLs;
- exactly one controlled page context;
- empty composer before navigation;
- no active response generation;
- preserved source URL;
- exact Worker title and project verification;
- bounded wrapper and correlation markers;
- stable captured response;
- verified return to source;
- disconnect after completion;
- stop before send or preserve forensic state after uncertain send status.

The general full-text composer investigation remains paused. Do not resume repeated selection, character-range comparison, dual witnesses, focus hacks, or broad timeout experiments without demonstrated failure.

## Advisory State

As of 2026-07-20:

- `ADV-20260720-046` is CLOSED with revision 2 `IMPLEMENT`, same-row receiver evidence, and verified `IMMEDIATE_HQ` review.
- `ADV-20260718-042` remains OPEN under the Chief of Staff source board. Engineering may provide Package E evidence but may not close it.
- `ADV-20260719-043` is CLOSED after Life OS Maintenance created the canonical execution and Worker protocols.
- `ADV-20260719-044` is CLOSED, implemented, and source verified after Life OS Maintenance reconciled Worker filesystem and continuity drift.

Do not duplicate these advisories or create parallel open-loop wrappers.

## Other Active Tracks

- Observe corrected role-routed specialist boots and inspect demonstrated defects.
- Observe four-source dashboard behavior during ordinary use.
- Continue Raw Capture and Inventory pilots only as grandfathered evidence sources.
- Align the Reliable Connector Execution Layer, operation ledger, and connector-health policy with the validated envelope, evidence, controlled-outcome, verification-state, wake-suppression, transport-integrity, and browser-receipt model.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Production Boundary

- Browser transport requires an authenticated, responsive Edge session with the loopback CDP endpoint available.
- The dashboard server must remain running for the Worker Operations UI.
- Failed or uncertain sends must not be retried blindly.
- Existing Python validation is technical infrastructure and defense in depth, not autonomous domain ownership.
- Worker-reported outcomes remain evidence until receiver validation.
- `IMMEDIATE_HQ` results remain pending until Engineering HQ review.
- Receiver or HQ review does not close source advisories.
- Additional Worker activation requires separate bounded authority and a source-owned profile.
- Windows service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Next Valid Action

Implement Package E Slice 2 under `projects/engineering/PACKAGE_E_IMPLEMENTATION_PACKET.md`: captured Worker response to semantic receiver validation, one same-row controlled outcome, and existing HQ review, with focused failure-path tests and no automatic advisory closure.