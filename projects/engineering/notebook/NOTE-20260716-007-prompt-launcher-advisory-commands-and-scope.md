# NOTE-20260716-007 — Prompt Launcher Advisory Commands and Scope Metadata

Date: 2026-07-16
Project: Chief Engineering Penny / Engineering HQ
Status: Deferred / Captured for later implementation

## Context

The Life OS Prompt Launcher currently supports advisory drafting and system-wide advisory synchronization, but it does not provide a dedicated command for reading one advisory or consuming one advisory for the current department.

The launcher also uses a department dropdown without making command scope fully explicit. Rob understands the current behavior, but the ambiguity would become a product-quality problem if the launcher were shared, sold, or used by another person.

This note preserves two future improvements without promoting them into the active Engineering open-loop stack tonight.

## Deferred Improvement 1 — Dedicated Advisory Commands

### `/READADVISORY @GitHub`

Purpose: read and interpret one advisory without changing durable state.

Expected behavior:

- accept an advisory ID or clear advisory reference;
- read `coordination/ADVISORY_INDEX.md`;
- resolve and read the canonical source board;
- summarize the request, current status, department relevance, required action, boundaries, dependencies, and recommended response;
- remain read-only;
- do not acknowledge, consume, implement, close, or modify GitHub.

Candidate prompt:

```text
/READADVISORY @GitHub

Advisory: {custom_block}

Read the Advisory Index and the advisory's canonical source board. Summarize the request, relevance to this department, required action, boundaries, dependencies, and recommended response. Do not modify GitHub or acknowledge the advisory.
```

### `/CONSUMEADVISORY @GitHub`

Purpose: consume an advisory for the current department and reconcile durable advisory state.

Expected behavior:

- read the Advisory Index and canonical source board;
- identify the current department and its requested response;
- perform only work explicitly authorized by Rob and owned by that department;
- record the department's acknowledgement or ingestion on the source board;
- reconcile the Advisory Index;
- preserve per-target acknowledgement state for multi-department advisories;
- do not close the advisory unless all closure conditions are satisfied;
- report exact files and state changes.

Candidate prompt:

```text
/CONSUMEADVISORY @GitHub

Advisory: {custom_block}

Read the Advisory Index and the advisory's canonical source board. Consume it for the current department, carry out only authorized department-level documentation work, record the department acknowledgement on the source board, and reconcile the Advisory Index. Do not close the advisory unless all closure conditions are satisfied.
```

## Deferred Improvement 2 — Explicit Launcher Scope Metadata

Do not create a fake department named `Any`.

Instead, add explicit prompt scope metadata so the UI can distinguish command ownership from command target.

Candidate values:

- `universal` — usable from any HQ and requires no department selection;
- `department` — operates on the selected department's files or state;
- `target_department` — selected department is the recipient or target, as with advisory drafting;
- `current_department` — operates on the HQ currently consuming the prompt, when that context can be represented reliably.

Potential JSON shape:

```json
{
  "scope": "universal"
}
```

or:

```json
{
  "scope": "department",
  "department_label": "Run for department"
}
```

UI behavior should then be:

- universal command: hide or disable the department dropdown and show `Scope: Any HQ`;
- department command: show `Run for department:`;
- advisory creation: show `Target department:`;
- read/consume advisory: make current-department assumptions explicit or ask only when truly ambiguous.

## Guardrails

- `memory/CONTEXT_REMINDER.md` remains the canonical command vocabulary.
- `engineering/classroom/prompt_launcher/prompt_library.json` remains a secondary interface.
- Read and consume must remain separate because one is read-only and the other changes durable state.
- Consuming an advisory must not silently authorize unrelated implementation.
- Multi-target advisories require per-target tracking until closure conditions are met.
- UI clarity should come from scope semantics, not invented departments.

## Promotion Trigger

Promote this note into active implementation only when Rob selects the launcher improvement as the current Engineering task.

At promotion time:

1. update the canonical command vocabulary;
2. update the prompt-library schema and entries;
3. update launcher UI behavior and labels;
4. validate JSON loading;
5. verify rendered prompts;
6. test read-only and write-enabled boundaries against a real advisory workflow.

## Process Observation

Engineering notebook capture is useful but currently easy to forget, while the active open-loop list is growing. That resurfacing problem deserves a separate workflow review rather than turning every captured idea into another immediate open loop.