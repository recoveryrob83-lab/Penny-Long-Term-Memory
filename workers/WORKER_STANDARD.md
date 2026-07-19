# Life OS Worker Standard

Updated: 2026-07-19
Status: Compatibility Pointer
Purpose: Preserve the two pre-existing top-level pilot Worker packages while routing all current Worker authority and boot behavior through the canonical shared contracts.

## Canonical Authority

The authoritative Worker rules are:

- `memory/STARTUP_BOOT.md`
- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

This file no longer defines an independent Worker boot sequence or authority model.

## Compatibility Rule

The existing pilot packages remain at:

- `workers/penny-raw-capture/`
- `workers/penny-inventory/`

When either legacy pilot is invoked:

1. begin at `memory/STARTUP_BOOT.md`;
2. follow the canonical Worker branch;
3. read both shared protocols;
4. treat the pilot's `WORKER_BOOT.md` as its exact compatibility profile and bounded procedure;
5. read its `SESSION_HANDOFF.md` only when mutable pointers or current operational notes are required.

The pilot-local instructions are subordinate to current canonical role names, authority ceilings, source-system boundaries, verification rules, controlled outcomes, pause behavior, and duplicate-suppression requirements.

## No New Top-Level Worker Packages

Do not create additional top-level packages under `workers/` by analogy.

New Workers use department-owned profiles at:

`projects/<department>/workers/<profile>.md`

A new profile is created only by the owning Department HQ when a real Worker is activated under the authority rules in `coordination/WORKER_EXECUTION_CONTRACT.md`.

## Conflict Rule

When this compatibility file, a legacy pilot package, or an older instruction conflicts with the canonical shared protocols, the current canonical shared protocols control.

Migration, retirement, or relocation of either pilot requires separate owner review and authorization.