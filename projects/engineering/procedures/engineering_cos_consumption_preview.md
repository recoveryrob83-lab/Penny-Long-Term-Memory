# Engineering Chief of Staff Consumption Preview Procedure

Procedure ID: `engineering_cos_consumption_preview`
Procedure Version: 1
Owner: Engineering HQ
Lifecycle State: Active
Priority: Normal

## Purpose

Define the manual-first Package E Slice 7 procedure for reading signed Worker results that are already consumption-ready, producing one compact Chief of Staff preview, and recording delivery deduplication on the same SQLite `execution_history` row only after Chief of Staff has actually consumed the batch.

This procedure proves the consumption contract before any unattended schedule is activated.

## Authority

Rob authorized Package E Slice 7 after the Slice 6 live chain reached `READY_FOR_COS`.

This procedure authorizes Engineering-owned technical implementation and local runtime validation only. It does not authorize:

- a courier wake to Chief of Staff;
- an unattended ChatGPT schedule without a separately chosen cadence;
- edits to Chief of Staff department files;
- source-advisory acknowledgement, implementation, source verification, or closure;
- task creation, prioritization, or new authority;
- consumption of raw or unsigned Worker reports;
- a second queue, ledger, or GitHub mirror of SQLite runtime state.

## Eligible Initial Results

The first Slice 7 consumer accepts only rows that satisfy all of these conditions:

- `mode: send`;
- `prompt_type: worker`;
- `controlled_outcome: IMPLEMENT`;
- `ready_for_consumption: true`;
- `result_state: HQ_VERIFIED` or `READY_FOR_COS`;
- a nonempty final verification actor and reason;
- one uniquely resolvable source advisory and lifecycle state.

Holds, elevations, rejected verification, stale reviews, and broader source-owner readiness reporting remain later bounded extensions after the verified-success path is proven.

## Preview

The preview is read-only.

For each eligible row it returns only compact pointers and state:

- run, Worker, task, revision, and owning department;
- controlled outcome and final result state;
- final verification actor and reason;
- immutable report, HQ-review, and Rob-validation pointers where present;
- source advisory board path and lifecycle state;
- a deterministic fingerprint derived from signed runtime and source state.

A batch ID is derived deterministically from the sorted item fingerprints. No preview row, file, queue, advisory, or external system is written.

When no eligible unconsumed results exist, the preview reports `meaningful_change: false` and produces no batch ID.

## Acknowledgement

Acknowledgement occurs only after Chief of Staff has actually consumed the preview.

It must:

1. receive the exact deterministic batch ID and exact run IDs;
2. recompute every item from current signed runtime and source state;
3. fail closed if evidence or source lifecycle changed;
4. update only the existing execution rows;
5. set the same-row consumption state, fingerprint, batch ID, timestamp, and consumer;
6. suppress an identical duplicate acknowledgement;
7. reject partial or conflicting acknowledgement.

Acknowledgement does not change `result_state`, verification state, source advisory lifecycle, task priority, ownership, or durable source records.

## Deduplication Contract

SQLite `execution_history` remains the sole operational ledger.

The consumption cursor lives only on the existing Worker execution row. GitHub result folders remain immutable evidence surfaces and are not used as a consumption queue.

A later scheduled bridge must consume this same preview contract and preserve the same-row acknowledgement rule rather than inventing a cloud-side or GitHub-side shadow ledger.

## Manual Proof

The first live proof uses:

`RUN-ADV-20260722-049-R1`

Expected sequence:

1. preview the signed `READY_FOR_COS` row;
2. confirm its source advisory remains independently owned and unchanged;
3. present the compact batch to Chief of Staff;
4. acknowledge the exact batch on the same row;
5. rerun preview and prove no-change silence;
6. rerun acknowledgement and prove duplicate suppression.

## Completion Condition

This procedure is validated when focused tests and one live manual proof demonstrate:

- unsigned or unready rows are excluded;
- the source advisory is read but never modified;
- preview is read-only;
- acknowledgement updates only the existing execution row;
- no second ledger or GitHub queue is created;
- identical acknowledgement is suppressed;
- source-state drift invalidates the prior batch;
- a second preview is silent after consumption.

Scheduled Chief of Staff activation remains a separate step requiring a concrete cadence and a bridge that can truthfully access the local consumption contract.
