# Chief of Staff HQ Advisory Board

Updated: 2026-07-18
Purpose: Canonical advisory text sourced from Chief of Staff HQ, including formal advisories arising from LifeOS HQ meetings. The retained filesystem path remains `coordination/boards/main-assistant.md`.

## Open Advisories

### ADV-20260718-042 — Move automated prompt verification from composer transport to receiving workers

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Engineering HQ
- Priority: High
- Status: Open / Routed
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Engineering HQ
- Record Class: Automation architecture implementation request
- Authorization: Rob-approved bounded Engineering implementation
- Related Work: Package C migration, dashboard automation, prompt database, and event-driven automation
- Completion Condition: The automation layer reliably delivers and logs a recognized envelope without exact semantic text matching; receiving workers validate the canonical prompt, parameters, authority, and scope; the worker returns one of `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`; and Engineering provides test or run-log evidence that the flow avoids duplicate execution and silent scope expansion.

#### Context

The current desktop automation successfully pastes and sends prompts to the composer, but exact composer-side copy verification produces false failures because the observed text may contain extra characters, UI artifacts, line-ending differences, or other transport noise. Rob has directly observed successful delivery while the automation reports failure. Repeated attempts to make the composer certify exact semantic integrity have consumed roughly eight hours and placed responsibility in the wrong layer.

The new architecture separates transport verification from semantic verification:

- the automation layer is the courier and verifies bounded delivery;
- the receiving department is the worker and verifies meaning, legitimacy, scope, ownership, and authority;
- the source department later verifies completed work and reports the outcome.

#### Required Transport-Layer Behavior

The automation layer should:

1. deliver one recognizable automation envelope to the intended department;
2. require only a minimum viable payload and recognizable start/end boundaries rather than exact full-text equality;
3. attach a durable `run_id`, `prompt_id`, prompt version, source, target, authorization class, advisory or approval reference when required, parameters, and checksums;
4. log the delivery attempt, send action, observed composer state, retry count, and transport result;
5. prevent duplicate delivery by correlating retries to the same `run_id`;
6. avoid interpreting, editing, approving, silently truncating, or discarding the requested work;
7. treat character counts and copied composer text as diagnostic evidence rather than the semantic safety gate.

The automation layer may verify that the envelope is present, addressed, and delivered once. It should not decide whether the enclosed work is semantically correct or authorized.

#### Proposed Automation Wrapper

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

The exact serialization may be refined by Engineering, but the envelope must remain machine-readable, versioned, correlated to one run, and sufficiently small to survive the composer transport path reliably.

#### Required Receiver-Side Validation

An automation wrapper is a warning label and routing hint, not proof of authority. The receiving worker should:

1. recognize and parse the wrapper;
2. verify that `prompt_id` and `prompt_version` exist in the canonical prompt database;
3. load the canonical prompt from the prompt database rather than trusting a long pasted prompt body when prompt-ID invocation is available;
4. normalize and verify the canonical prompt checksum and parameter checksum;
5. validate parameters against the prompt schema;
6. confirm that the stated source may issue that class of request;
7. confirm that the target department owns the work;
8. confirm that the requested action matches the authorization class, advisory, approval record, SOPs, and source-system boundaries;
9. ignore harmless transport noise outside the recognized envelope while refusing unexpected text that changes scope, destination, permanence, permissions, or requested actions;
10. preserve the `run_id` in all execution, closure, escalation, and reporting records.

#### Receiver Decision Tree

The receiving worker must choose one explicit outcome:

**IMPLEMENT**

Use when the wrapper is recognized, checksums and parameters validate, the prompt exists, ownership and authorization are correct, and the requested scope is fully workable. Execute the bounded work and report completion with evidence tied to the `run_id`.

**ELEVATE_FOR_APPROVAL**

Use when the request is legitimate but requires broader authority, a human judgment, a source conflict resolution, a new durable-write decision, unexpected financial or privacy exposure, or any other approval not already present. Do not perform the unapproved portion. Report the exact decision required.

**REPORT_AND_HOLD**

Use when the prompt ID is unknown, a checksum or required parameter fails, the target does not own the work, the request conflicts with SOPs or source boundaries, the envelope appears corrupted, the authorization record is missing, or unexpected instructions materially alter the canonical request. Perform no write. Report the failure reason and wait for correction or verification.

For read-only work, Engineering may define a narrower tolerance for harmless formatting noise. For write work, unexpected scope-changing instructions must stop the run rather than being interpreted as “close enough.”

#### Logging and Verification Requirements

The run log should preserve at minimum:

- `run_id`, `prompt_id`, and prompt version;
- source, target, authorization class, and advisory or approval reference;
- expected and observed envelope markers;
- expected and observed checksums;
- expected and observed character counts as diagnostics;
- delivery timestamp and send-action result;
- retry count and duplicate-suppression result;
- receiver decision: `IMPLEMENT`, `ELEVATE_FOR_APPROVAL`, or `REPORT_AND_HOLD`;
- execution evidence, escalation reason, or hold reason;
- final source-verification state when the larger event loop is implemented.

#### Boundaries

- Do not make exact composer-text equality a release blocker.
- Do not use minimum character count alone as proof of semantic integrity.
- Do not let the transport layer silently reinterpret or discard work.
- Do not let an automation wrapper bypass department ownership, SOPs, advisory approval, durable-write gates, or source-system boundaries.
- Do not create a competing prompt source outside the canonical prompt database.
- Do not mark this advisory implemented or closed until Engineering verifies the new flow with current test or run-log evidence.

## Acknowledged / Implemented Advisories

Historical entries below retain names and wording that were accurate when they were created.

### ADV-20260718-041 — Create a global Trello connector write SOP

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-18
- Acknowledged: 2026-07-18
- Closed: 2026-07-18
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Life OS Maintenance HQ
- Record Class: Global operating SOP request
- Durable Output: `coordination/CONNECTOR_RELIABILITY_OPERATING_PATTERN.md`

#### Outcome

Life OS Maintenance HQ updated the existing global Connector Reliability Operating Pattern rather than creating a competing Trello-only source of truth. The global SOP now documents:

- small, bounded Trello mutations;
- exactly one checklist item per connector call;
- ambiguous connector errors as inconclusive when delayed success is possible;
- mandatory live read-back before retrying or reporting failure;
- card, checklist, checklist-item, and update duplicate prevention;
- verified live-state reporting when the connector receipt is misleading;
- the separately verified success of basic Inbox card creation;
- the observed false-negative risk around checklist-item and some update paths;
- Trello's continued role as the capture, possibility, attention, and flow layer;
- and the rule that Trello writes do not authorize GitHub promotion, Todoist commitments, Calendar events, or duplicate source records.

The SOP preserves the behavior as observed evidence rather than claiming platform internals, assigns later technical compensation to Engineering only if separately authorized, and creates no duplicate system open loop. The advisory's completion condition is satisfied.

### ADV-20260716-038 — Explore a read-mostly LifeOS desktop dashboard window

- Date: 2026-07-16
- From: Main Assistant Penny / LifeOS Coordination Hub
- To: Chief Engineering Penny
- Priority: Medium
- Status: Acknowledged / Ingested / Closed
- Acknowledged: 2026-07-16
- Closed: 2026-07-16
- Related Project(s): Life OS, desktop tooling, prompt launcher, Trello, Todoist, Google Calendar, Gmail, Google Drive
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Context

Rob is developing an early concept for a LifeOS desktop dashboard. The intent is not to replace Trello, Todoist, Google Calendar, Gmail, Google Drive, or Penny. It is a single desktop window that shows the most important active state from each system while Penny remains the worker that performs changes through conversation and connector-backed actions.

#### Ingested Engineering Direction

Engineering recognizes the dashboard as an active design concept with these boundaries:

- treat the dashboard as a window into LifeOS rather than a replacement productivity platform;
- preserve Trello, Todoist, Calendar, Gmail, and Drive as authoritative source systems;
- keep Penny as the conversational worker, coordinator, and connector operator;
- retain and reuse the existing prompt launcher and prompt database;
- center the first useful view on high-signal current state, especially Trello `Now`, top `Next`, daily commitments, near-term calendar pressure, mail-attention signals, and pinned working files;
- begin read-only or read-mostly;
- avoid direct write controls until observed need justifies them;
- keep account-linked financial connector data excluded from Hub or multi-connector operation under `coordination/FINANCIAL_CONNECTOR_ISOLATION_SOP.md`;
- turn the concept into a staged specification when Rob supplies further requirements.

No software implementation was authorized or performed under this advisory. The requested Engineering ingestion is complete.

### ADV-20260715-036 — Design prompts for seven LifeOS department discussion HQs

- Date: 2026-07-15
- From: Main Assistant Penny / LifeOS Coordination Hub
- To: Chief Engineering Penny
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Rob confirmed that all seven LifeOS department discussion HQ chats are open and ready. The operating model preserves Chat/Work separation, explicit department boundaries, connector rules, truthful action reporting, Main Assistant coordination, and Rob's final authority. No separate prompt-design advisory work remains.

### ADV-20260715-035 — Standardize Rob's friction-aware daily operating pattern

- Date: 2026-07-15
- From: Main Assistant Penny / Daily Operations
- To: Chief Engineering Penny
- Priority: High
- Status: Implemented / Acknowledged / Closed
- Implemented: 2026-07-15
- Acknowledged: 2026-07-15
- Closed: 2026-07-15
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Engineering verified that `memory/06_DAILY_OPERATING_SOP.md` is included in the canonical global boot order. Every department boot inherits the friction-aware daily pattern. No external task, calendar, mail, or Drive systems were changed.

### ADV-20260709-029 — Engineering implementation request for dedicated rapid capture worker GPT

- Date: 2026-07-09
- From: Main Assistant Penny
- To: Chief Engineering Penny
- Status: Closed / Implemented Through ADV-20260709-030
- Closed: 2026-07-09
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department: Chief Engineering Penny

#### Outcome

Engineering defined a technology-independent worker contract. Life Logistics implemented the formal worker layer and Penny Raw Capture Worker package under ADV-20260709-030. No separate work remains.

## Current Board Rules

- Read `coordination/ADVISORY_INDEX.md` first rather than scanning every board.
- This retained path is the Chief of Staff HQ source board despite its legacy filename.
- When an advisory arises from a LifeOS HQ meeting, identify its source as `Chief of Staff HQ / LifeOS HQ`.
- LifeOS HQ does not maintain a separate advisory board.
- Keep canonical advisory text here and routing state in the Advisory Index.
- Do not duplicate advisory text into target boards or matching department open loops merely for visibility.
- Do not mark an advisory implemented or closed without verified handling.
- Keep all open advisories in enough detail to act and a bounded recent completed working set. Git history preserves older detail removed during compaction.