# LifeOS Execution and Communication Protocol

Updated: 2026-07-19
Owner: Maintenance_HQ
Status: Active / Canonical
Purpose: Define how Rob, `LifeOS_HQ`, `Chief_of_Staff_HQ`, Department HQs, Workers, advisories, scheduled procedures, dashboards, and automation communicate, authorize, execute, verify, report, and close work.

## 1. Authority and Organizational Topology

- Rob is the final authority.
- `LifeOS_HQ` is the shared strategic meeting room.
- `LifeOS_HQ` owns no independent backlog, department state, connector authority, or durable project record.
- `Chief_of_Staff_HQ` is Rob's primary daily operational point of contact, Hub chair, reporting desk, assignment router, practical coordinator, and follow-through owner.
- Department HQs own specialist strategy, judgment, durable state, approvals, audits, and department-bound collaboration.
- Workers perform bounded execution under one owning department and one explicit contract.
- Workers do not become shadow Department HQs, independent strategists, or competing backlog owners.
- `Maintenance_HQ` owns this protocol, shared boot coherence, global governance, source boundaries, and cross-system reconciliation.
- `Engineering_HQ` owns transport, automation, dashboard, receiver-state, routing-registry, parser, validator, testing, and technical reliability implementation.
- The dashboard is a transport, visibility, diagnostic, and bounded control layer. It is not a source of truth and does not create authority.

Short form:

> Rob decides. `LifeOS_HQ` deliberates. `Chief_of_Staff_HQ` coordinates. Departments judge and own. Workers execute. `Maintenance_HQ` governs. `Engineering_HQ` builds the machinery.

## 2. Canonical Operating Surfaces

Use the smallest correct surface:

- **`LifeOS_HQ`:** cross-department strategy, LifeOS architecture, shared operating rules, major priorities, long-range planning, and decisions requiring several department perspectives.
- **`Chief_of_Staff_HQ`:** daily operations, appointments, communications, Todoist, Calendar, reminders, reporting, practical coordination, assignment routing, and Rob-facing decisions.
- **Department HQ:** specialist strategy, approvals, interpretation, high-context judgment, exceptions, audits, and work tightly bound to one department.
- **Department Worker:** already-authorized bounded execution under a valid Worker profile, task definition, advisory, or canonical timed procedure.

A real Hub decision must transfer to:

1. one owning department;
2. one authoritative destination;
3. one lifecycle state;
4. one priority field, separate from lifecycle;
5. one next action or review trigger;
6. one completion, rejection, resume, or review condition.

Chief of Staff carries operational consequences into daily planning without copying the entire strategic discussion into operational systems.

## 3. Source-System Boundaries

- **Conversation:** temporary reasoning, discussion, drafting, and working context.
- **GitHub:** durable abstract state, approved rules, architecture, decisions, advisories, Worker profiles, procedures, operating watches, validated knowledge, and meaningful history.
- **Google Drive:** human-facing Chief's Manual, detailed working records, Docs, Sheets, drafts, and deliverables.
- **Trello:** raw capture, possibilities, candidate work, experiments, questions, someday items, and current attention flow.
- **Todoist:** Rob-facing commitments and reminders.
- **Google Calendar:** timed commitments.
- **Gmail:** communication evidence.
- **Dashboard and automation logs:** transport evidence, diagnostics, run state, and bounded operational control.

No transport, dashboard, Worker, advisory, or convenience copy may create a competing source of truth.

Detailed sensitive records remain in their natural systems. GitHub stays abstract.

## 4. Work Initiation and Calling Authority

An execution-ready Worker task may be initiated by:

- `Chief_of_Staff_HQ`, when Rob has authorized the work and it fits an existing Worker profile;
- the owning Department HQ;
- an authorized cross-department advisory whose source may request that task class;
- a canonical timed procedure with existing standing authority.

The dashboard and automation layer may transport an authorized task. They may not invent, interpret, approve, prioritize, or broaden it.

Department ownership does not require an HQ relay wake for every routine task.

## 5. Direct Execution-Ready Routing

The normal bounded path is:

Rob authorizes work through `Chief_of_Staff_HQ`
→ Chief of Staff creates one execution-ready advisory or uses an already-authoritative task definition
→ the work targets the owning Department Worker
→ the Worker performs the bounded procedure
→ the Worker updates the same authoritative advisory or run record with evidence
→ verification follows the specified mode
→ Chief of Staff includes the result in the next appropriate operational report.

The normal happy path should require one event-driven desktop wake.

Wake the owning Department HQ before execution only when department-level judgment, clarification, authorization, exception handling, or strategy is genuinely required.

Do not create an HQ relay advisory merely to restate an already execution-ready Worker assignment.

## 6. Advisory Authority and Continuity

The same advisory remains authoritative through:

- acknowledgement;
- implementation;
- hold;
- elevation;
- Rob's decision;
- resume authorization;
- verification;
- closure.

One blocked work item must not generate a chain of duplicate advisories.

Formal advisory text lives on the source department board. Routing state lives in `coordination/ADVISORY_INDEX.md`.

`LifeOS_HQ` formal advisories use `Chief_of_Staff_HQ` as the source department and the retained board path `coordination/boards/main-assistant.md`.

## 7. Lifecycle and Priority

Canonical advisory lifecycle states:

- `OPEN`
- `ACKNOWLEDGED`
- `IMPLEMENTING`
- `HELD`
- `ELEVATED_FOR_APPROVAL`
- `RESUME_AUTHORIZED`
- `REJECTED`
- `IMPLEMENTED`
- `SOURCE_VERIFIED`
- `CLOSED`

Canonical priority values:

- `LOW`
- `NORMAL`
- `HIGH`
- `URGENT`

Lifecycle state and priority are separate fields. Never use urgency as lifecycle or lifecycle as priority.

A material advisory change increments `advisory_revision`.

Receivers preserve `last_processed_revision`.

Cosmetic edits do not create new work and must not trigger a wake.

## 8. Worker Decision Outcomes

Every Worker run returns exactly one controlled outcome:

- `IMPLEMENT`
- `REPORT_AND_HOLD`
- `ELEVATE_FOR_APPROVAL`

`IMPLEMENT` means the Worker completed only the authorized bounded work and recorded required evidence.

`REPORT_AND_HOLD` means execution cannot safely continue within current authority. The owning Department HQ resolves the hold.

`ELEVATE_FOR_APPROVAL` means Rob must decide, authorize an exception, or approve materially broader authority. `Chief_of_Staff_HQ` coordinates the elevation while the department retains ownership.

## 9. Verification Modes

Every execution-ready advisory or canonical timed procedure specifies one verification mode:

- `AUTOMATIC`
- `ROUTINE_BATCH`
- `IMMEDIATE_HQ`

### AUTOMATIC

Use only for low-risk, deterministic work with an explicit machine-verifiable postcondition.

Automatic closure is permitted only when both the authoritative task definition and the advisory explicitly authorize it.

### ROUTINE_BATCH

Use for ordinary completed work that deserves Department HQ review but not an immediate interruption.

Completed work enters the department verification queue and is reviewed during the next natural HQ session, approved audit, or justified batched review wake.

Routine success does not produce an immediate desktop wake merely to report completion.

### IMMEDIATE_HQ

Use for sensitive, destructive, public-facing, expensive, unusual, high-consequence, or exception-bearing work requiring prompt Department HQ validation.

## 10. Wake Eligibility and Suppression

A material authoritative revision is wake-eligible, not automatically wake-producing.

Default routing:

- `OPEN` with an execution-ready Worker target → wake Worker.
- `HELD` → wake owning Department HQ.
- `ELEVATED_FOR_APPROVAL` → wake `Chief_of_Staff_HQ`.
- `RESUME_AUTHORIZED` → wake paused Worker.
- `REJECTED` → wake Worker only when clean closure action is required.
- `IMPLEMENTED` with `AUTOMATIC` → verify the defined postcondition; suppress unnecessary chat wake.
- `IMPLEMENTED` with `ROUTINE_BATCH` → queue for review; suppress immediate desktop wake.
- `IMPLEMENTED` with `IMMEDIATE_HQ` → wake owning Department HQ.
- `SOURCE_VERIFIED` → normally no wake.
- `CLOSED` → no wake.

A receiver must suppress duplicate processing when `advisory_revision` is not greater than `last_processed_revision`.

Transport retries must not create duplicate execution.

## 11. Holds, Elevations, and Resume

A hold is resolved by the owning Department HQ.

An elevation is coordinated through `Chief_of_Staff_HQ` for Rob's decision.

The underlying department retains ownership throughout.

Resume requires an explicit `RESUME_AUTHORIZED` state or another clearly authorized canonical resume signal.

Silence, inactivity, elapsed time, or a transport retry is not approval to resume.

## 12. Reporting

- Routine success waits for scheduled or naturally requested Chief of Staff reporting.
- Chief of Staff synthesizes completed work, exceptions, risks, and decisions.
- Department HQs do not send separate routine all-clear reports to Rob.
- Immediate `Chief_of_Staff_HQ` wakes occur only when Rob must decide or a time-sensitive operational exception requires attention.
- Detailed evidence remains in its authoritative advisory, run record, department record, or automation log.
- Reports distinguish requested work, attempted work, verified work, partial work, held work, and unverified claims.

## 13. Scheduled Procedures

A scheduled procedure may execute only when:

- the schedule is canonical and active;
- the procedure has standing authority;
- the intended Worker or HQ route is defined;
- the task remains within its approved scope;
- pause state and preflight checks allow execution;
- the advisory or schedule revision has not already been processed.

A schedule transports timing. It does not create authority, broaden scope, or convert an idea into a commitment.

Missed, overdue, failed, or paused schedules follow their canonical scheduler policy and must not silently catch up or fabricate execution history.

## 14. Desktop Pause and Safe Resume

Native cloud-side scheduled tasks may continue while desktop UI automation is paused, provided their own standing authority remains valid.

Desktop automation must fail closed when the host cannot read the authoritative pause state.

A paused desktop route does not authorize alternate unverified UI transport.

Resume requires an authoritative resume action and normal destination, scope, duplication, and preflight checks.

Routine pause or resume state should not produce duplicate advisories or duplicate work.

## 15. Ownership Boundaries

- `Chief_of_Staff_HQ` may route authorized work and report outcomes without taking ownership of specialist judgment.
- Department HQs own their Worker profiles, approvals, exceptions, holds, verification, and department records.
- Workers may update only evidence and records explicitly permitted by their profile and task.
- `Maintenance_HQ` owns shared governance protocols and canonical boot coherence.
- `Engineering_HQ` owns technical routing, receiver-state, wake suppression, deduplication, transport, and validation mechanisms.
- The dashboard and automation layer may not become a policy owner.

## 16. Boot Application

`memory/STARTUP_BOOT.md` is the single canonical entry point.

After the universal operating kernel:

- every HQ reads this protocol before its role-specific files;
- every Worker reads this protocol and `coordination/WORKER_EXECUTION_CONTRACT.md` before its owning-department identity and exact Worker profile;
- routed dependencies are loaded only when required for the bounded work.

Do not copy this protocol into department subtrees.

## 17. Completion Standard

LifeOS execution is operating correctly when:

- one owner and one authoritative record exist;
- transport does not create authority;
- Workers stay bounded;
- departments retain judgment;
- `Chief_of_Staff_HQ` coordinates without absorbing ownership;
- lifecycle and priority remain separate;
- wake behavior follows verification mode and material state changes;
- holds and elevations preserve the same authoritative advisory;
- reports are verified and non-duplicative;
- source-system boundaries remain intact;
- Rob receives decisions and exceptions without routine wake noise.