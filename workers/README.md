# Life OS Workers

Updated: 2026-07-19
Purpose: Compatibility registry for the two pre-existing top-level Worker pilots and pointer to the canonical department-owned Worker architecture.

## Canonical Worker Architecture

Current authority lives in:

- `memory/STARTUP_BOOT.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

A Life OS Worker is a narrow execution role owned by one department. It performs already-authorized bounded procedures, verifies operations, preserves scope, reports truthfully, and returns one controlled outcome:

- `IMPLEMENT`
- `REPORT_AND_HOLD`
- `ELEVATE_FOR_APPROVAL`

Workers do not own department strategy, project prioritization, independent backlogs, durable source-of-truth decisions, advisory policy, financial decisions, or broad life planning.

## Department-Owned Profiles

New Worker profiles live at:

`projects/<department>/workers/<profile>.md`

The owning Department HQ creates a profile only when a real Worker is activated.

Do not create speculative profiles, empty Worker directories, or top-level Worker packages for possible future roles.

One general Worker per department is the default. Specialized Workers require repeated operational evidence that the specialization reduces meaningful friction.

## Technology Independence

A Worker may be implemented as:

- a dedicated ChatGPT chat;
- a custom GPT;
- a Gemini Gem or dedicated Gemini chat;
- a scheduled task;
- a Python utility;
- an automation workflow;
- an API-backed service;
- a future PennyOS component.

Technology does not change the authority ceiling.

## Canonical Boot

Every Worker begins at `memory/STARTUP_BOOT.md` and follows the Worker branch.

The Worker loads:

1. the universal operating kernel;
2. `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`;
3. `coordination/WORKER_EXECUTION_CONTRACT.md`;
4. the owning department identity;
5. the exact Worker profile;
6. the referenced advisory, task definition, or schedule;
7. only the records and SOPs required for the bounded task.

Workers do not automatically load full department histories, notebooks, backlogs, unrelated open loops, or unrelated advisories.

## Grandfathered Pilot Registry

The following top-level packages predate the department-owned profile convention:

| Status | Worker | Compatibility Path | Purpose | Current Ownership / Consumer |
|---|---|---|---|---|
| Grandfathered Pilot / Active | Penny Raw Capture Worker | `workers/penny-raw-capture/` | Append raw information to the canonical Life OS Raw Capture Inbox for later processing | Primary consumer: Chief of Staff HQ; technical reliability: Engineering HQ; shared routing and governance: Life OS Maintenance HQ |
| Grandfathered Pilot / Active | Penny Inventory Worker | `workers/penny-inventory/` | Convert uploaded sale-item photographs into verified rows in the canonical For Sale Inventory Sheet | Downstream consumers: Chief of Staff HQ and later sale workflows; technical reliability: Engineering HQ; shared routing and governance: Life OS Maintenance HQ |

These packages may continue under their existing bounded purposes until separately migrated, retired, or relocated.

Their `WORKER_BOOT.md` files function as compatibility profiles and task procedures. Their instructions are subordinate to the current canonical shared protocols.

No new top-level package may be created by analogy.

## Compatibility Pointer

`workers/WORKER_STANDARD.md` is retained only because the grandfathered pilot packages reference it.

It points to the canonical global boot and Worker contract and does not define a separate authority model.

## Durable State Rule

Worker state belongs in:

- the canonical advisory or task definition;
- the durable run record;
- automation logs;
- permitted department records;
- the department-owned profile for stable identity and authority only.

Do not create independent Worker status files, open-loop files, backlogs, advisory boards, or department-style scaffolds.

## Governance

- Rob is final authority.
- The owning Department HQ owns Worker purpose, profile, permissions within existing authority, holds, verification, and retirement.
- Life OS Maintenance HQ owns the shared Worker contract, profile convention, canonical boot coherence, and source-boundary protection.
- Engineering HQ owns routing registry implementation, transport, stable-ID handling, receiver state, revision deduplication, verification queues, wake suppression, and technical reliability.
- Chief of Staff HQ may route Rob-authorized work into an existing profile without taking ownership of specialist judgment.

Creating a Worker does not create a new department, source of truth, priority, commitment, or independent backlog.