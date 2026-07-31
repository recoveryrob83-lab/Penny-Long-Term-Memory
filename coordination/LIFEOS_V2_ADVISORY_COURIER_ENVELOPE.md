# LifeOS V2 Advisory Courier Envelope

- Owner: Maintenance_HQ
- Record Class: Shared transport contract
- Lifecycle State: ACTIVE
- Priority: HIGH
- Approved: 2026-07-29
- Authority: Rob-approved coordinated Maintenance and Engineering repair
- Implementation Target: `apps/lifeos_dashboardv2`

## Purpose

This contract defines the small machine-readable transport envelope required on every active advisory that may be dispatched by the LifeOS V2 courier.

The envelope does not replace the full advisory. The full source-board section remains the authoritative record for scope, authority, procedures, evidence, completion conditions, holds, and judgment. The courier reads only this envelope to identify and transport actionable work.

Primary rule:

> The advisory carries authority. The envelope carries routing metadata. The courier transports without interpreting judgment.

## Canonical Envelope

Every dispatch-eligible advisory must contain one exact level-four subsection named `V2 Courier Envelope` inside its authoritative advisory section:

```markdown
#### V2 Courier Envelope

- Advisory Revision: 1
- Source Department: chief_of_staff
- Target Department: engineering
- Task Summary: Implement the bounded work described in this advisory.
- Authorized Scope: Read and act only within the authority and boundaries stated in this advisory.
- Lifecycle State: OPEN
- Outcome:
- Blocker:
- Updated At: 2026-07-29T11:52:00-05:00
```

The subsection ends at the next level-four heading or the end of the advisory section. Fields elsewhere in the advisory are authority or operational metadata and must not be interpreted as transport-envelope fields.

## Required Fields

All nine envelope fields are required, including `Outcome` and `Blocker` when their values are empty.

- `Advisory Revision`: positive integer. Increment only for a material change to the same authoritative advisory.
- `Source Department`: canonical route identifier for the issuing department.
- `Target Department`: one canonical route identifier for the current owner or receiver.
- `Task Summary`: concise human-readable summary of the wake purpose.
- `Authorized Scope`: concise transport-facing scope statement. It points to, but does not replace, the full authority and boundaries in the advisory.
- `Lifecycle State`: one canonical V2 advisory state.
- `Outcome`: current outcome text or an intentionally empty value.
- `Blocker`: current blocker text or an intentionally empty value.
- `Updated At`: ISO 8601 timestamp with timezone offset.

The advisory ID remains in the advisory heading and Advisory Index. The source path and source URL are derived from the Advisory Index and source-board location.

## Canonical States

- `OPEN`
- `IN_PROGRESS`
- `BLOCKED`
- `NEEDS_ROB`
- `COMPLETED`
- `CLOSED`

Only `OPEN` and `IN_PROGRESS` are dispatch-actionable.

## Canonical Route Identifiers

Route identifiers are lowercase snake_case transport keys, not display names. Initial Department HQ identifiers are:

- `chief_of_staff`
- `maintenance`
- `engineering`
- `business`
- `office_leaks`
- `finance`
- `wellness`

`LifeOS_HQ` is a shared meeting room and does not receive an independent department route. Hub-originated formal advisories use `chief_of_staff` as the source route.

A bounded Worker route may use its canonical Worker ID when a current approved Worker profile and advisory explicitly authorize direct routing.

## Revision and Command Identity

Command identity is:

```text
<advisory_id>-r<advisory_revision>
```

Adding or correcting the envelope without changing the underlying work does not automatically require a new advisory. Rob or the source owner determines whether the correction is material enough to increment the revision.

## Source and Ownership Rules

- `coordination/ADVISORY_INDEX.md` remains the sole active routing dashboard.
- Full advisory text remains on one source department board under `coordination/boards/`.
- The envelope must appear inside that same authoritative advisory section.
- Do not duplicate the full advisory into target boards, open loops, dashboard state, or local courier persistence.
- Maintenance_HQ owns this shared contract.
- Source departments own the accuracy of envelope values on their advisories.
- Engineering_HQ owns parser and runtime enforcement.

## Parser Behavior

The V2 parser must:

- locate exactly one `#### V2 Courier Envelope` subsection inside the indexed advisory section;
- parse canonical fields only within that subsection;
- ignore legacy, authority, lifecycle, revision, and operational fields elsewhere in the advisory;
- require the exact canonical field names;
- reject missing, duplicate, or empty required routing fields inside the envelope;
- require present `Outcome` and `Blocker` fields even when empty;
- validate revision, lifecycle state, route identifiers, and timestamp shape;
- isolate malformed advisories without blocking valid advisories;
- derive advisory ID from the heading and index;
- derive source path and URL from the index;
- never infer authority from prose or legacy aliases.

Historical closed advisories are not required to be backfilled. Active advisories become dispatch-eligible only after their source owner adds a valid envelope.

## Completion and Review Condition

This contract remains active until Rob approves a revision. A change to required fields, lifecycle semantics, route identifiers, or parser authority is a shared-rule change owned by Maintenance_HQ and implemented by Engineering_HQ under bounded authority.
