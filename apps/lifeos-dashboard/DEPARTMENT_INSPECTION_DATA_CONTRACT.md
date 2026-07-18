# Department Inspection Data Contract

Updated: 2026-07-18
Status: Approved / implementation contract
Schema version: 1
Owner: Engineering HQ

## Purpose

Define the normalized read model for the LifeOS Dashboard Department Inspection tab.

The inspector must preserve three things at once:

1. what each source file actually says;
2. what the dashboard can classify confidently;
3. what remains ambiguous and requires cleanup.

The inspector is a read-only aggregation and diagnostic layer. It does not become a new source of truth.

## Source-of-Truth Rule

- Department-owned unfinished work remains authoritative in the owning department's canonical files.
- System-level files contain only genuinely shared architecture, cross-department dependencies, multi-owner work, system-wide risks, or work with no single department owner.
- The dashboard may normalize, aggregate, filter, sort, preview, and flag anomalies.
- The dashboard must not silently merge, rewrite, promote, demote, close, or otherwise mutate source records.

## Canonical Scopes

The inspector supports seven department scopes plus one system scope.

| Scope ID | Display Label | Scope Type |
|---|---|---|
| `main-assistant` | Chief of Staff HQ | department |
| `logistics` | Life OS Maintenance HQ | department |
| `engineering` | Engineering HQ | department |
| `business` | Business HQ | department |
| `office-leaks` | Office Leaks HQ | department |
| `finance` | Finance HQ | department |
| `wellness` | Wellness HQ | department |
| `system` | System | system |

Scope IDs are fixed compatibility identifiers. Display labels are canonical presentation values.

## Normalized Record Envelope

Every inspectable item must normalize into one record envelope.

```json
{
  "id": "engineering:open_loops:department-ownership-architecture",
  "schema_version": 1,
  "department": "engineering",
  "scope": "department",
  "record_type": "work_item",
  "subtype": "open_loop",
  "title": "Department ownership architecture and dashboard inspection",
  "summary": "Formalize ownership and routing rules, then build the Department Inspection tab.",
  "state": "open",
  "priority": "high",
  "owner": "Engineering HQ",
  "cross_department": true,
  "related_departments": ["main-assistant", "logistics"],
  "dependency_type": "policy-change",
  "record_date": null,
  "created_at": null,
  "updated_at": "2026-07-18",
  "due_at": null,
  "closed_at": null,
  "tags": ["dashboard", "boot-routing", "open-loop-ownership"],
  "source_path": "projects/engineering/open_loops.md",
  "source_section": "Open",
  "source_format": "markdown-table",
  "source_authority": "authoritative",
  "raw_text": "Priority | Department ownership architecture...",
  "parse_confidence": "high",
  "warnings": []
}
```

Unknown values remain `null`, `unknown`, empty lists, or empty strings as appropriate. The parser must not invent missing metadata.

## Required Record Fields

| Field | Type | Rule |
|---|---|---|
| `id` | string | Stable normalized identifier derived from scope, source family, and record identity |
| `schema_version` | integer | `1` for this contract |
| `department` | enum | One canonical scope ID |
| `scope` | enum | `department` or `system` |
| `record_type` | enum | One normalized record type |
| `subtype` | string | More specific source meaning |
| `title` | string | Human-readable record title |
| `summary` | string | Compact normalized preview |
| `state` | enum | Lifecycle state, separate from priority |
| `priority` | enum | Urgency, separate from lifecycle state |
| `owner` | string or null | Explicit owner when available |
| `cross_department` | boolean | True only when routing or action crosses department boundaries |
| `related_departments` | list[string] | Explicitly related department IDs when confidently known |
| `dependency_type` | string or null | Optional relationship label |
| `record_date` | date or null | Authored record date, commonly from a notebook filename or header |
| `created_at` | datetime/date or null | Explicitly authored creation time only |
| `updated_at` | datetime/date or null | Explicit source update time |
| `due_at` | datetime/date or null | Explicit due time only |
| `closed_at` | datetime/date or null | Explicit closure time only |
| `tags` | list[string] | Explicit or conservatively normalized tags |
| `source_path` | string | Repository-relative source path |
| `source_section` | string or null | Source heading or table section |
| `source_format` | enum/string | Examples: `markdown-table`, `markdown-bullets`, `markdown-document` |
| `source_authority` | enum | Authority level of the source |
| `raw_text` | string | Original record text or compact source fragment |
| `parse_confidence` | enum | `high`, `medium`, or `low` |
| `warnings` | list[string] | Ambiguity, legacy format, conflict, or missing-metadata warnings |

## Record Types

Normalized `record_type` values:

- `work_item`
- `note`
- `status`
- `rule`
- `watch`
- `decision`
- `milestone`
- `log`
- `handoff`

Typical `subtype` values include:

- `open_loop`
- `waiting_item`
- `parking_lot`
- `notebook_entry`
- `status_update`
- `standing_rule`
- `operating_watch`
- `closed_item`
- `validation_record`
- `session_handoff`
- `boot_log`
- `advisory`

Examples:

| Source meaning | record_type | subtype |
|---|---|---|
| Build Department Inspector | `work_item` | `open_loop` |
| Preserve exact destination verification | `rule` | `standing_rule` |
| Observe a second recurring execution | `watch` or `work_item` | `operating_watch` or `validation_record` |
| Scheduling implementation completed | `milestone` | `closed_item` |
| Engineering notebook note | `note` | `notebook_entry` |

## Lifecycle State

Allowed normalized `state` values:

- `open`
- `active`
- `waiting`
- `paused`
- `blocked`
- `closed`
- `completed`
- `cancelled`
- `unknown`

## Priority

Allowed normalized `priority` values:

- `critical`
- `high`
- `normal`
- `low`
- `none`
- `unknown`

State and priority must remain separate.

Legacy compatibility mapping:

| Source value | Normalized state | Normalized priority | Warning |
|---|---|---|---|
| `Priority` | `open` | `high` | Legacy field mixes urgency with workflow state |
| `Active` | `active` | `normal` | None unless priority is otherwise unknown |
| `Open` | `open` | `normal` | None unless priority is otherwise unknown |
| `Waiting` | `waiting` | `normal` | None unless priority is otherwise unknown |
| `Paused` | `paused` | `normal` | None unless priority is otherwise unknown |

## Scope and Ownership Rules

A record is department-scoped when one department owns execution, judgment, and durable maintenance, even when the outcome benefits all of Life OS.

A record may be system-scoped only when at least one condition is true:

- multiple departments must act or decide;
- shared LifeOS architecture or policy changes;
- no single department can own the work;
- the matter blocks multiple departments;
- Chief of Staff HQ or Life OS Maintenance HQ must coordinate it;
- it represents a genuine system-wide operational risk.

Broad usefulness does not make work system-owned.

Example: the dashboard helps all departments, but dashboard implementation remains Engineering-owned.

## Cross-Department Routing

`cross_department` means another department needs awareness, action, judgment, or a durable dependency relationship. It does not mean the work is broadly useful.

A department-owned record may therefore use:

```json
{
  "scope": "department",
  "department": "engineering",
  "cross_department": true,
  "related_departments": ["main-assistant", "logistics"],
  "dependency_type": "policy-change"
}
```

For version 1, `related_departments` and `dependency_type` are optional and must remain empty or null when the source does not support a confident inference.

## Source Authority

Allowed `source_authority` values:

- `authoritative`
- `summary`
- `historical`
- `derived`
- `unknown`

Examples:

| Source | Authority |
|---|---|
| `projects/engineering/open_loops.md` for Engineering unfinished work | `authoritative` |
| Engineering session handoff repeating current work | `summary` |
| Older notebook describing completed work | `historical` |
| Dashboard-generated anomaly finding | `derived` |

Conflicting records must remain visible. The inspector must not silently choose or overwrite a source.

## Date Semantics

Use separate date fields:

- `record_date`
- `created_at`
- `updated_at`
- `due_at`
- `closed_at`

Rules:

- Notebook filename dates may populate `record_date`.
- Explicit `Date:` headers may populate `record_date`.
- Explicit `Updated:` headers may populate `updated_at`.
- Closed-work table dates may populate `closed_at`.
- Explicit deadlines may populate `due_at`.
- Unknown values remain `null`.
- Git commit time may be exposed later as derived metadata, but must not be presented as an authored creation or update date.

## Canonical Source Families

Expected department sources:

- `SESSION_HANDOFF.md`
- `status.md`
- `open_loops.md`
- `notebook/NOTE-*.md`

Optional sources may include:

- `logs/`
- `DECISION_RULES.md`
- `README.md`
- local procedures
- department advisory boards

The inspector must tolerate missing optional files. Missing optional files are not source failures.

## Conservative Parsing Rules

The parser may confidently interpret:

- Markdown tables with known headers;
- bullets under known section names;
- notebook metadata such as `Date`, `Status`, `Department`, and `Owner`;
- canonical note filename dates;
- explicit `Updated:` headers;
- explicit closed dates and due dates.

The parser must not infer:

- priority from dramatic wording;
- ownership from a mere mention;
- closure because a newer note exists;
- cross-department routing merely because several departments are named;
- authored dates from Git commit history;
- authority from recency alone.

Ambiguity must remain visible through `parse_confidence` and `warnings`.

## Parse Confidence

Allowed values:

- `high`: explicit fields and known structure;
- `medium`: reasonable structural mapping with one or more missing fields;
- `low`: uncertain classification or weak source structure.

Example:

```json
{
  "parse_confidence": "medium",
  "warnings": ["Priority not explicitly provided"]
}
```

## Findings and Anomalies

The inspector may generate derived findings without mutating records.

Initial anomaly types:

- `possible_duplicate`
- `stale_mirror`
- `state_priority_mixed`
- `authority_conflict`
- `status_conflict`
- `missing_metadata`
- `unclassified_record`

Example:

```json
{
  "anomaly_type": "stale_mirror",
  "severity": "high",
  "records": [
    "engineering:closed:command-center-phase-1",
    "system:open:command-center-phase-1"
  ],
  "summary": "Department work is closed locally but still appears open in a system summary."
}
```

Duplicate detection may use:

- normalized title similarity;
- matching department and subject;
- shared notebook references;
- identical or near-identical summaries;
- department records echoed in system files;
- closed department work still appearing as globally open.

Findings must say `possible` or otherwise preserve uncertainty unless the conflict is explicit.

## Inspector Categories

The user interface groups records into four primary categories.

### Work

Open, active, waiting, paused, blocked, and recently closed work.

### Knowledge

Notebooks, decisions, plans, validation records, and historical notes.

### Operations

Standing rules, operating watches, logs, handoffs, and status records.

### Findings

Possible duplicates, stale summaries, state/priority mixing, authority conflicts, missing metadata, and unclassified records.

## Version 1 Filters

The first implementation supports:

- department;
- category;
- record type;
- state;
- priority;
- date or date range;
- cross-department status;
- source authority;
- warnings only;
- text search;
- newest, oldest, department, or priority sorting.

Tags are stored when available but are not required as a version 1 filter.

## Version 1 Read-Only Boundary

The inspector may:

- aggregate;
- normalize;
- filter;
- sort;
- preview;
- show source paths;
- show raw source text;
- flag anomalies.

The inspector must not:

- create, edit, pause, close, delete, or reorder source records;
- rewrite classifications;
- merge duplicates;
- promote department work to system work;
- demote system work;
- create advisories;
- update metadata;
- write to GitHub.

Any future write workflow requires a separate explicit design, authorization boundary, verification path, and audit record.

## Implementation Foundation

Version 1 is approved on these foundations:

1. one normalized record envelope;
2. seven department scopes plus System;
3. nine normalized record types;
4. separate lifecycle state and priority;
5. explicit source authority;
6. conservative parsing with confidence and warnings;
7. read-only duplicate and stale-state findings;
8. department files remain authoritative;
9. system files contain only genuinely system-owned work;
10. the dashboard remains an aggregation and diagnostic layer, not a mirrored ledger.
