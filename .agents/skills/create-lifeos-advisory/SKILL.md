---
name: create-lifeos-advisory
description: >
  Create, draft, materially revise, route, block, complete, source-verify, or
  close a formal LifeOS cross-department advisory using the canonical GitHub
  advisory system and the current V2 courier schema. Use when Rob or an
  authorized LifeOS HQ asks to create or change an advisory, route work between
  departments, prepare dashboard-ready advisory transport, or update advisory
  lifecycle/revision state. Do not use for ordinary intra-department notes,
  raw ideas, Todoist tasks, casual FYI messages, or work that does not need a
  formal cross-department authoritative record.
---

# Create LifeOS Advisory

## Purpose

Create or change exactly one formal LifeOS advisory while preserving one owner,
one authoritative source-board record, one routing entry in the Advisory Index,
current LifeOS governance, current V2 courier compatibility, explicit authority,
bounded scope, and no duplicate truth.

Canonical repository:

`recoveryrob83-lab/Penny-Long-Term-Memory`

Navigation aid:

`MASTER_INDEX.md`

Canonical advisory authorities:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md`
- `coordination/ADVISORY_INDEX.md`

Current V2 implementation surfaces:

- `apps/lifeos_dashboardv2/lifeos_v2/contracts.py`
- `apps/lifeos_dashboardv2/lifeos_v2/reader.py`

## Core contract

- The full advisory carries authority.
- The V2 Courier Envelope carries routing metadata only.
- The dashboard/parser/courier may transport, display, validate, or quarantine.
  They do not invent or broaden authority.
- `coordination/ADVISORY_INDEX.md` is the sole active routing dashboard.
- Full advisory text lives on exactly one source department board.
- Do not duplicate full advisory text into target boards, department open loops,
  handoffs, Todoist, GitHub Issues, dashboard state, or courier storage.
- `LifeOS_HQ` is not an independent source department. Formal Hub advisories use
  `Chief_of_Staff_HQ`, route `chief_of_staff`, and
  `coordination/boards/main-assistant.md`.
- Governance lifecycle and V2 transport lifecycle are separate.
- Lifecycle and priority are separate.
- A material change increments advisory revision. Cosmetic edits do not.
- The same advisory remains authoritative through acknowledgement,
  implementation, hold, elevation, resume, verification, and closure.
- A malformed envelope may quarantine transport but does not invalidate,
  replace, close, or duplicate the underlying advisory.
- Fetch current files before every write and preserve unrelated content.
- Never claim a write, parser check, delivery, acknowledgement, verification, or
  closeout succeeded without current evidence.

## Modes

### Draft-only

Use when Rob asks to draft, design, propose, or show an advisory without
authorizing a durable GitHub write.

Return the proposed advisory and index mutation without writing.

### Authorized write

Use when Rob clearly asks to create, post, update, revise, route, block,
complete, verify, close, or otherwise change the formal advisory in GitHub.

Write only the exact authoritative records required by this Skill and the live
contracts.

## Procedure

### 1. Resolve the advisory action

Identify whether this is:

- new advisory creation;
- material revision;
- routing change;
- acknowledgement or implementation state change;
- hold;
- elevation for Rob approval;
- resume authorization;
- implementation/completion update;
- source verification;
- closure;
- envelope repair without changing underlying work.

If Rob names an existing advisory ID, use that exact advisory. Do not create a
replacement merely because transport failed, delivery is uncertain, or the
envelope is malformed.

### 2. Read the minimum live advisory context

Read these current files before authoring or changing the advisory:

1. `MASTER_INDEX.md`
2. `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
3. `coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md`
4. `coordination/ADVISORY_INDEX.md`
5. the exact source department board

For dashboard/parser compatibility work, also inspect:

6. `apps/lifeos_dashboardv2/lifeos_v2/contracts.py`
7. `apps/lifeos_dashboardv2/lifeos_v2/reader.py`

Use the master index for navigation only. Live canonical contracts and current
implementation override cached Skill knowledge.

Do not use `coordination/template.md` as controlling authority when it conflicts
with the current execution protocol or V2 envelope contract.

### 3. Pass the durable-write gate

Before creating a new advisory, establish:

- record class;
- one source owner;
- one target/current owner;
- one authoritative source board;
- governance lifecycle state;
- priority, separate from lifecycle;
- verification mode when execution-ready;
- smallest useful next action or review trigger;
- completion, rejection, resume, or review condition;
- whether an authoritative advisory already exists;
- why a formal advisory is the correct mechanism;
- the statement, rule, or direct Rob instruction authorizing the advisory.

Do not promote brainstorming, enthusiasm, repeated mention, or assistant
recommendation into a formal advisory without actual authority.

### 4. Determine source and target routes

Resolve source and target from the current master index and V2 envelope contract.

Do not invent route identifiers.

For formal Hub-originated advisories:

- source role: `Chief_of_Staff_HQ`;
- V2 source route: `chief_of_staff`;
- source board: `coordination/boards/main-assistant.md`.

### 5. Check for duplicate work

Search the current open Advisory Index and source board for the same work item,
dependency, decision, hold, elevation, or earlier revision.

Prefer continuing or revising the existing advisory when it represents the same
open loop.

Do not create a second advisory for visibility, retry, quarantine, uncertain
delivery, acknowledgement, implementation, verification, or closeout.

### 6. Allocate or preserve advisory identity

For an existing advisory:

- preserve advisory ID;
- preserve source-board continuity;
- increment revision only for a material change.

For a new advisory:

- inspect current index and boards;
- follow the current repository advisory ID convention;
- allocate a unique unused ID;
- verify uniqueness before writing.

Never guess an ID from memory when GitHub is available.

### 7. Build the full authoritative advisory

For a new execution-ready advisory include, at minimum:

- advisory heading with ID and concise subject;
- Date;
- From;
- To;
- governance Lifecycle State;
- Priority;
- Advisory Revision;
- Verification Mode;
- Posted Board;
- Target Department and Owner;
- Record Class;
- Authorization Source and useful approval reference when one exists;
- explicit authority/exception/spending/connector boundaries when relevant;
- Completion Condition;
- Advisory Closure Condition;
- exactly one V2 Courier Envelope;
- concise decision/context or summary;
- authorized outcome/task scope;
- explicit holds/forbidden actions;
- verification and closeout expectations.

Use the source board's current conventions when compatible with canonical
contracts. Keep the advisory as small as possible while still execution-ready.

### 8. Build the V2 Courier Envelope from the live schema

Read the current
`coordination/LIFEOS_V2_ADVISORY_COURIER_ENVELOPE.md` and preserve its exact
current field names, field count, route syntax, transport states, revision
semantics, and timestamp requirements.

The envelope must be inside the same authoritative advisory section under
exactly one level-four heading:

`#### V2 Courier Envelope`

When dashboard readiness matters, validate against the current
`apps/lifeos_dashboardv2/lifeos_v2/reader.py`.

At minimum confirm:

- exactly one advisory heading for this advisory ID;
- exactly one V2 Courier Envelope inside that advisory;
- every current canonical envelope field appears exactly once;
- required routing fields are non-empty;
- Outcome and Blocker are present when the live schema requires them, even empty;
- revision is a positive integer;
- transport lifecycle is a supported V2 state;
- source/target are valid lowercase snake_case route IDs;
- Updated At is ISO 8601 with timezone;
- the open index entry supplies exactly one source-board path;
- source path and URL are derived rather than duplicated into the envelope.

Do not rely on cached field wording if the live contract or parser changed.

### 9. Keep governance and transport state separate

The full advisory uses the broader governance lifecycle from the current
execution protocol.

The envelope uses the smaller V2 transport lifecycle from the courier contract.

For a new execution-ready advisory, governance `OPEN` normally pairs with
transport `OPEN`.

For later lifecycle changes, deliberately choose the transport state matching
the intended courier condition. Do not ask the parser to infer governance
judgment from prose.

If the mapping is materially ambiguous, preserve the advisory and hold the
transport change rather than inventing authority.

### 10. Choose verification mode explicitly

Every execution-ready advisory uses one current canonical verification mode from
the live execution protocol.

Choose based on actual risk and evidence requirements, not convenience.

Do not use verification mode as a substitute for lifecycle, priority, authority,
or completion condition.

### 11. Write only authoritative advisory records

For normal advisory creation or lifecycle mutation, expected durable writes are:

1. the source department board;
2. `coordination/ADVISORY_INDEX.md`.

Do not write the target board merely to notify it.
Do not duplicate the advisory into department open loops.
Do not update the frozen Department Event Inbox unless Rob explicitly
reactivates it.
Do not use GitHub Issues or Todoist as advisory-state systems.

Preserve unrelated content.

### 12. Update the Advisory Index precisely

For an open advisory, maintain exactly one unambiguous open index reference.

The current reader requires each open reference to contain:

- one advisory ID;
- exactly one backticked source-board path matching
  `coordination/boards/*.md`;
- no duplicate open advisory ID.

Include current governance lifecycle, priority, revision, verification mode,
source-board path, target, and concise purpose when supported by the current
index format.

The lifecycle shown in the index is governance lifecycle, not V2 transport
lifecycle.

On closure, preserve history according to the current closed-history convention
and remove stale open routing.

### 13. Material revision rules

Increment advisory revision only for a material change.

Keep the full advisory revision and V2 envelope revision aligned.

Do not increment for cosmetic edits.

Command identity is derived from advisory ID and revision. Do not manually create
duplicate command identities.

### 14. Holds, elevation, completion, verification, closure

Reuse the same advisory.

For a hold:

- record governance hold and blocker/evidence;
- use the current non-dispatchable blocked transport condition;
- preserve ownership.

For Rob escalation:

- record governance elevation and exact decision required;
- use the current Rob-needed non-dispatchable transport condition;
- coordinate through Chief of Staff without transferring specialist ownership.

For implementation/completion:

- record actual evidence;
- do not equate Worker claims with source verification;
- apply the verification mode;
- suppress new dispatch when transport work is complete.

For source verification:

- require current source-owner evidence;
- preserve implementation evidence;
- do not close until the actual closure condition is met.

For closure:

- source owner explicitly closes the advisory;
- transport is closed/suppressed;
- the index no longer exposes it as open;
- historical identity, outcome, and evidence remain preserved.

### 15. Validate before declaring dashboard-ready

Read back the complete advisory and index entry.

Confirm:

- advisory heading is unique;
- source board is correct;
- no duplicate advisory exists;
- governance lifecycle and priority are separate;
- revision is consistent;
- verification mode is valid when execution-ready;
- authorization is explicit;
- completion and closure conditions are explicit;
- exactly one envelope exists;
- all live envelope fields appear exactly once;
- route IDs satisfy current syntax;
- transport state is valid;
- timestamp includes timezone;
- open index entry has exactly one source-board path;
- no unrelated content changed;
- no target-board or open-loop duplicate was created.

If a local harness can run the current V2 parser/tests and testing is in scope,
use them.

If it cannot, report structural validation against the live contract/source and
do not falsely claim runtime parser execution.

### 16. Return a compact advisory receipt

For draft-only:

- Mode: DRAFT ONLY
- advisory ID or identity plan;
- source owner/board;
- target route;
- governance lifecycle;
- V2 transport state;
- revision;
- priority;
- verification mode;
- validation status;
- Writes: none.

For authorized write:

- advisory ID;
- revision;
- source board;
- target route;
- governance lifecycle;
- V2 transport state;
- priority;
- verification mode;
- exact files changed;
- parser/dashboard validation method;
- any hold or ambiguity;
- confirmation no duplicate target record was created.

Never claim delivery to a target chat merely because the advisory is
dashboard-ready.

## Stop conditions

Stop the affected write and report when:

- authority is absent;
- source owner or destination cannot be determined;
- a likely duplicate exists and cannot safely be reconciled;
- required live contracts cannot be read;
- current protocol and envelope contract materially conflict;
- parser requirements conflict with the shared transport contract;
- the change would edit unrelated department records;
- source-owner verification is required but unavailable;
- closure condition is not met;
- uncertain transport would otherwise cause a replacement advisory.

A parser quarantine is not authority to replace or close an advisory.

## Success conditions

An advisory operation succeeds only when:

1. one source owner exists;
2. one authoritative source-board advisory exists;
3. one correct index routing/history record exists;
4. authority and bounded scope are explicit;
5. lifecycle and priority remain separate;
6. revision semantics are correct;
7. verification mode is explicit when required;
8. the live V2 envelope contract is satisfied;
9. current parser structure is satisfied when dashboard readiness is claimed;
10. no competing target-board/open-loop/task-system truth was created;
11. unrelated content was preserved;
12. the receipt accurately distinguishes authored, written, validated,
    delivered, implemented, source-verified, and closed state.

## Design boundary

Keep this Skill as a stable procedural interface.

Governance belongs in canonical LifeOS contracts.
State belongs in the source-board advisory and Advisory Index.
Machine schema belongs in the V2 transport contract and Engineering
implementation.

When those authorities evolve, re-read and follow their live versions. Update
this Skill only when stable paths, trigger semantics, authoring workflow, write
boundaries, or compatibility procedure genuinely change.
