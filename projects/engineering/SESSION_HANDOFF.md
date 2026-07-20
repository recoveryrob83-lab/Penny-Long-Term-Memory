# Engineering HQ Session Handoff

Updated: 2026-07-20
Project: Engineering HQ
Purpose: Current handoff for technical architecture, Package D Worker-runtime infrastructure, operational Worker procedures, desktop automation, connector reliability, the LifeOS Dashboard, and the Automation Command Center.

## Metadata

- Project Owner: Rob
- Primary Chat: Engineering HQ
- Current Phase: Active / Package D Backend and Desktop Milestone Complete / Operational ChatGPT Worker Model Clarified / Next Implementation-Goal Decision Pending
- Primary Systems: GitHub, ChatGPT Department and Worker rooms, local LifeOS Dashboard, SQLite Command Center history, Engineering advisory board, Advisory Index when needed, and other source systems only when explicitly required
- Sensitivity Level: Moderate
- GitHub Rule: Never store secrets, credentials, tokens, API keys, private account details, medical details, private user data, or sensitive implementation details in Life OS memory files.

## Boot Instructions

1. Follow `memory/STARTUP_BOOT.md` and its universal-kernel plus role-routed rules.
2. Read this handoff.
3. Read `projects/engineering/DEPARTMENT_IDENTITY.md`.
4. Read `projects/engineering/README.md`, `status.md`, and `open_loops.md`.
5. Treat `projects/engineering/open_loops.md` as authoritative for unfinished Engineering work.
6. Read `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md` when Package D, ADV-20260718-042, operational Worker procedure, or Worker activation is in scope.
7. Read `coordination/WORKER_EXECUTION_CONTRACT.md` and `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md` when Worker routing, authority, or execution behavior is in scope.
8. Read `coordination/ADVISORY_INDEX.md` only when advisory routing or cross-department status is relevant.
9. Read current Engineering notebook records only when directly referenced by active work.
10. Keep connector work small, explicit, and verifiable.

## Department Role

Engineering HQ owns technical architecture, software planning, repository strategy, automation design, prompt systems, APIs and connectors, data models, testing, debugging, implementation sequencing, build-readiness, and truthful verification.

Engineering does not own canonical shared Worker governance, global boot coherence, profile conventions, or department-specific Worker authority. Life OS Maintenance HQ owns shared governance surfaces. Departments own Worker profiles, procedures, judgment, and authority. Engineering owns technical routing, transport, logging, duplicate suppression, verification mechanics, runtime evidence, tests, and reliability infrastructure.

Route business strategy to Business HQ or Office Leaks HQ, cost-bearing choices to Finance HQ, daily one-off execution to Chief of Staff HQ, shared governance and global memory hygiene to Life OS Maintenance HQ, and wellbeing or sustainability judgment to Wellness HQ.

## Canonical Worker Model

A Life OS Worker is a specialized ChatGPT room operating beneath one Department HQ.

The operating model is:

- the Department HQ owns the Worker profile, authority, procedures, and domain judgment;
- GitHub holds the canonical profile, approved procedures, task state, and durable evidence;
- the Worker chat receives a bounded envelope, reads the required canonical GitHub sources, validates the request, performs only authorized work, and returns a controlled outcome with evidence;
- the Department HQ reviews the result and retains ownership;
- Python, desktop automation, SQLite, and the dashboard act as courier, routing, safety, logging, duplicate-suppression, and visibility infrastructure.

Python is not the Worker and does not need to become an autonomous interpreter of every GitHub profile, procedure, or task. Machine validation may remain useful as defense in depth, but it must not replace the ChatGPT Worker’s operational source reading, judgment, refusal behavior, or Department HQ review.

## Chat and Work Model

Use regular Chat for architecture, planning, GitHub synchronization, prompt and procedure work, debugging analysis, advisories, and bounded connector updates.

Use Work for substantial coding, local terminal work, full test execution, desktop control, packaging, or complex artifacts.

Never claim an action, test, deployment, or connector write occurred without current evidence.

## Primary Current Work Package

### Package D: Operations-Procedure and Worker-Runtime Implementation

Lifecycle State: Active
Priority: Normal

Status: Backend and physical desktop transport milestone complete. Slices 1–7 are implemented and locally validated, and one bounded synthetic wrapper passed through ChatGPT Classic with exact acknowledgement. The technical foundation is substantial. The next decision is about operational Worker procedure and evidence, not a presumed Python receiver-ingress build.

Canonical implementation packet:

- `projects/engineering/PACKAGE_D_IMPLEMENTATION_PACKET.md`

Canonical governance and authorization references:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`
- ADV-20260718-042 on `coordination/boards/main-assistant.md`

Implemented slices:

1. Worker contracts and validation.
2. Worker registry, route, and task-scoped receiver persistence.
3. Worker registry service.
4. Separate Worker Command Center execution path.
5. Receiver semantic validation and controlled outcomes.
6. Verification views, queue derivation, and wake suppression.
7. Disposable synthetic end-to-end backend pilot with transport-integrity hardening.

Bounded desktop validation:

- `apps/lifeos-dashboard/automation/run_synthetic_worker_desktop_pilot.py`
- `apps/lifeos-dashboard/tests/test_synthetic_worker_desktop_pilot.py`
- exact-title Worker transport in `apps/lifeos-dashboard/automation/open_worker_chat_group_verified.py`

Validation state:

- focused Slice 7 and receiver suite: `32 passed`;
- complete dashboard regression suite reported by Rob: `222 passed, 9 warnings in 238.78s`;
- live desktop receipt reported `status: succeeded`, `mode: send`, `exit_code: 0`, and `durable_authority_created: false`;
- exact acknowledgement: `SYNTHETIC_WRAPPER_RECEIVED SYNTH-DESKTOP-WRAP-1784515664-0de7866901`;
- no real Worker profile, registry entry, route, wake, UI mutation control, or recurring Worker authority schedule was created.

## ADV-042 Interpretation

ADV-20260718-042 states that the automation layer is the courier and that the receiving Worker validates the canonical prompt, parameters, authority, ownership, scope, and source boundaries.

For the intended Life OS model, the receiving Worker is the specialized ChatGPT Worker room. It must:

1. recognize and parse the bounded envelope;
2. load its department-owned profile and the named canonical procedure or prompt from GitHub;
3. validate version, parameters, authority, ownership, scope, procedures, and source boundaries;
4. refuse unknown, corrupted, unauthorized, ownership-conflicted, or scope-expanding work;
5. return exactly one controlled outcome: `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`;
6. preserve run, task or advisory, Worker, profile, and evidence identifiers in its report;
7. allow Department HQ and the existing run history to verify the result.

The earlier Engineering conclusion that Package D necessarily required a new Python receiver-ingress and canonical-resolution service overinterpreted the machine-runtime implementation. That scripting is not currently a required closure condition.

## Remaining Package D Evidence

The next bounded slice should be selected by Rob. Engineering’s current recommendation is operational rather than code-first:

1. define the Worker operational execution procedure and canonical source-resolution contract;
2. choose one synthetic or narrowly department-owned Worker case;
3. run one bounded ChatGPT Worker pilot through physical transport;
4. verify that the Worker reads canonical GitHub sources, returns one controlled outcome, refuses unauthorized expansion, and preserves duplicate-suppression and evidence requirements;
5. present the resulting evidence to the ADV-042 source owner for verification and closure review.

Add Python source resolution or deeper automated receiver enforcement only if the operational pilot demonstrates a concrete reliability, security, or scale gap that procedures and existing infrastructure cannot safely cover.

## Planned Production Readability Follow-up

Before the first real Worker activation, preserve the compact JSON envelope as the authoritative machine transport representation and add a generated human-readable summary beside it.

The summary must:

- derive every displayed field from the same `ExecutionEnvelope` object;
- show Worker, task and revision, procedure and version, authorization source, verification mode, wrapper ID, run ID, and bounded instruction;
- remain display-only and non-authoritative;
- have no independent edit path, parser, persistence record, or lifecycle state;
- be covered by focused field-parity tests.

## Composer Boundary

The general full-text composer investigation is paused by Rob and must not be reopened without demonstrated failure.

The Worker-only path preserves exact destination, empty-composer protection, clipboard restoration, explicit send, one-job locking, and stop-on-uncertainty safeguards. After paste it copies once and checks only whether the expected `wrapper_id` is present.

Full-text equality, repeated selection, character-range comparison, multiple witnesses, alternate paste mechanisms, focus hacks, and broader timeout experiments are out of scope.

## Advisory State

As of 2026-07-20:

- ADV-20260718-042 is OPEN and authoritative. Engineering has substantial component and transport evidence; operational ChatGPT Worker validation and source-owner lifecycle decisions remain outstanding.
- ADV-20260719-043 is CLOSED after Life OS Maintenance created the canonical execution and Worker protocols.
- ADV-20260719-044 is CLOSED, implemented, and source verified after Life OS Maintenance reconciled shared Worker filesystem, pointer, profile-state, handoff, watch, and architecture-history drift.

Do not duplicate these advisories or create parallel open-loop wrappers.

## Other Active Tracks

- Observe corrected role-routed specialist boots and inspect demonstrated defects.
- Observe four-source dashboard behavior during ordinary use.
- Continue Raw Capture and Inventory pilots only as grandfathered evidence sources.
- Align the Reliable Connector Execution Layer, operation ledger, and connector-health policy with the validated envelope, evidence, controlled-outcome, verification-state, wake-suppression, transport-integrity, and desktop-receipt model.
- Continue Office Leaks delivery architecture as concrete requirements mature.
- Keep Engineering HQ Daily Sync paused until Rob explicitly resumes it.

## Production Boundary

- ChatGPT Classic must be responsive for UI automation.
- Failed scheduled runs pause rather than retry blindly.
- Existing Python validation is technical infrastructure and testable defense in depth, not an autonomous Worker implementation.
- Package D backend and desktop validation do not authorize a real Worker, profile, route, wake, recurring authority schedule, or Package E.
- Any real activation requires a separate bounded decision and source-owned profile authority.
- Do not create recurring Worker authority schedules without an approved task-generation model.
- Windows startup, desktop shell, service packaging, richer notifications, and broader recovery remain deferred until demonstrated need.

## Next Valid Action

Have Rob select one bounded next implementation goal. Engineering recommends the operational Worker execution procedure and canonical GitHub source-resolution contract before any further Python runtime expansion or real Worker activation. This handoff does not itself authorize implementation.