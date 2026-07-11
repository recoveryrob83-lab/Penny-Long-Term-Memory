# Life OS Workers

Updated: 2026-07-10
Purpose: Registry and routing guide for narrow Life OS execution workers.

## Worker Definition

A Life OS worker is a narrow execution role that performs one repeatable operation under a stable contract.

Workers:

- execute bounded procedures,
- preserve scope,
- use approved tools and storage,
- verify external operations,
- report failure truthfully,
- and escalate when requested work exceeds their authority.

Workers do not own:

- department strategy,
- project prioritization,
- durable source-of-truth decisions,
- cross-project state,
- advisory policy,
- financial decisions,
- or broad life planning.

## Department vs Worker Rule

Departments own judgment, strategy, systems, durable state, and cross-project decisions.

Workers execute bounded procedures under explicit contracts.

A worker is not a smaller department and should not receive a full HQ/project scaffold unless its role later changes substantially.

## Technology Independence

A worker may be implemented as:

- a dedicated ChatGPT chat,
- a custom GPT,
- a Gemini Gem or dedicated Gemini chat,
- a scheduled task,
- a Python utility,
- an automation workflow,
- an API-backed service,
- or a future PennyOS component.

The worker contract is technology-independent.

## Worker Creation Rule

Create a worker only when:

- the operation repeats,
- the scope can be stated clearly,
- inputs and outputs are known,
- success can be verified,
- failure behavior can be defined,
- and the worker reduces meaningful friction.

Do not create a worker merely because a task occurred once.

## Worker Boot Rule

A worker boots from:

1. `workers/WORKER_STANDARD.md`
2. Its worker-specific `WORKER_BOOT.md`
3. Its `SESSION_HANDOFF.md` only when mutable resource pointers or current operational notes are needed

Workers should not automatically read the entire Life OS global boot.

A worker may read a department or global file only when its worker contract explicitly requires that file for the current operation.

## Worker Registry

| Status | Worker | Path | Purpose | Owner / Consumer |
|---|---|---|---|---|
| Pilot / Active | Penny Raw Capture Worker | `workers/penny-raw-capture/` | Append raw information to the canonical Life OS Raw Capture Inbox for later processing | Primary consumer: Main Assistant Penny; architecture: Chief Engineering Penny; cross-project memory: Life Logistics HQ |
| Pilot / Active | Penny Inventory Worker | `workers/penny-inventory/` | Convert uploaded sale-item photographs into verified rows in the canonical For Sale Inventory Sheet | Downstream consumers: Main Assistant Penny and later sale/listing workflows; architecture: Chief Engineering Penny; cross-project memory: Life Logistics HQ |

## Worker Package Pattern

Minimum worker package:

```text
workers/<worker-name>/
  WORKER_BOOT.md
  SESSION_HANDOFF.md
```

Do not automatically add:

- `DEPARTMENT_IDENTITY.md`,
- `status.md`,
- `open_loops.md`,
- an advisory board,
- a project notebook,
- a decision-rules file,
- a full global boot sequence,
- or independent Todoist/Calendar state.

Add extra files only when the worker contract genuinely requires them.

## Governance

- Life Logistics HQ owns worker-root organization and durable cross-project routing.
- Chief Engineering Penny owns worker architecture and technical reliability guidance.
- The named downstream department owns later processing of worker output.
- Rob remains the final authority for creating, promoting, pausing, or retiring workers.
