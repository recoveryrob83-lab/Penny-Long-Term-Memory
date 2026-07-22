# Engineering HQ Worker Review Receipt Procedure

Procedure ID: `engineering_hq_worker_review_receipt`
Procedure Version: 1
Owner: Engineering HQ
Lifecycle State: Active

## Purpose

Define the narrow Engineering HQ procedure for reviewing one deterministically validated Engineering Worker result and creating one immutable HQ review receipt.

This procedure applies only to Engineering-owned Worker runs whose existing SQLite execution row has reached `REPORT_VALIDATED` and whose canonical verification mode requires Department HQ review.

## Authority

This procedure is authorized for the Package E Engineering pilot by Rob's explicit authorization to proceed with Slice 5 owning-HQ wakes and verification receipts.

It does not authorize:

- source-advisory closure or lifecycle change;
- re-execution of the Worker's assignment;
- modification or overwrite of a Worker report;
- cross-department review or receipt creation;
- Chief of Staff wake or consumption;
- Rob validation;
- scope expansion, new tools, new connectors, or new authority;
- creation of a second runtime ledger.

## Required Inputs

Engineering HQ must inspect:

1. the exact canonical assignment and revision;
2. the deterministically validated Worker report path;
3. the report checksum, creation commit, and blob SHA preserved on the existing execution row;
4. the report's authority, requested and actual scopes, tools, completion state, and evidence references;
5. the actual work and source evidence wherever independent inspection is possible;
6. unresolved uncertainty, holds, or approval requirements.

A chat wake is a pointer only. It is not evidence and must not copy detailed source truth into a competing record.

## Deterministic Receipt Path

For attempt 1:

`projects/engineering/worker-results/<worker_id>/<run_id>/hq-review-001.json`

The receipt must:

- conform to `apps/lifeos-dashboard/lifeos_dashboard/data/worker-hq-review.schema.json` version 1;
- use the exact run ID, Worker ID, reviewing HQ, and validated report path;
- be created once and never overwritten, renamed, moved, or deleted;
- be the only path in its creation commit;
- preserve concise evidence pointers rather than copying detailed truth;
- remain separate from advisory lifecycle authority.

## Allowed Review States

### `VERIFIED`

Use only when:

- report integrity is `valid`;
- authority compliance is `compliant`;
- the actual work is independently `verified`;
- `ready_for_consumption` is `true`;
- `requires_rob_validation` is `false`.

Engineering HQ must not self-sign work whose decisive postcondition is unavailable to HQ inspection.

### `REJECTED`

Use when the report, authority, evidence, or independently inspectable work is materially contradicted or noncompliant. The receipt is not consumption-ready and does not authorize work re-execution.

### `REPAIR_REQUIRED`

Use when a correctable report or evidence defect prevents verification. The receipt is not consumption-ready. Any later repair must use a separately bounded correction-only path and must not repeat or broaden the underlying work.

### `ROB_VALIDATION_REQUIRED`

Use only when report integrity and authority compliance are valid, but the decisive work result cannot be independently inspected by Engineering HQ. The receipt must state the exact observation or decision Rob must provide. It is not consumption-ready until the separate Rob-validation path completes.

## Ingestion

The deterministic HQ review ingester must:

- validate schema and semantic consistency;
- verify exact runtime identity and validated report correlation;
- verify one immutable creation commit containing only the receipt;
- calculate the canonical content checksum;
- update only the existing `execution_history` row;
- suppress an identical duplicate receipt;
- reject a conflicting receipt;
- advance the runtime to `HQ_VERIFIED`, `HQ_REJECTED`, `REPORT_REPAIR_PENDING`, or `ROB_VALIDATION_REQUIRED` as appropriate.

The ingester must not close the source advisory, wake Chief of Staff, perform Rob validation, or create another queue or ledger.

## Completion Condition

The procedure completes when one immutable schema-valid HQ review receipt is created, read back with Git and checksum evidence, ingested into the existing execution row, and the resulting review branch is visible in Worker Operations.
