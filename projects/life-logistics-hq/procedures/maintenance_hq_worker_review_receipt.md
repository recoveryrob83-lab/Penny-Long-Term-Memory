# Maintenance HQ Worker Review Receipt Procedure

Procedure ID: `maintenance_hq_worker_review_receipt`
Procedure Version: 1
Owner: Maintenance HQ
Lifecycle State: Active

## Purpose

Define the narrow `Maintenance_HQ` procedure for reviewing one deterministically validated `Maintenance_Worker` result and creating one immutable HQ review receipt.

This procedure applies only to Maintenance-owned Worker runs whose existing SQLite execution row has reached `REPORT_VALIDATED` and whose canonical verification mode is `IMMEDIATE_HQ`.

## Authority

Rob explicitly approved creation of `Maintenance_Worker` after Package F Wave 0B passed the read-only governance review. The approved initial pilot is manually dispatched and read-only except for its exact immutable result artifact.

This procedure authorizes `Maintenance_HQ` to review that bounded result and create one immutable review receipt. It does not authorize:

- Worker activation, route registration, route capture, deployment-state change, schedule creation, pause or resume action, send-budget reset, or unattended execution;
- source-advisory, system-loop, or department-record closure;
- re-execution or broadening of the Worker's assignment;
- modification or overwrite of a Worker report;
- review of another department's Worker;
- Chief of Staff wake or consumption;
- Rob validation;
- shared-rule repair, department-local repair, new tools, new connectors, spending, or new authority;
- creation of a second runtime ledger.

## Required Inputs

`Maintenance_HQ` must inspect:

1. the exact canonical assignment and revision;
2. the current `Maintenance_Worker` profile and result-submission procedure versions;
3. the deterministically validated Worker report path;
4. the report checksum, creation commit, and blob SHA preserved on the existing execution row;
5. the report's authority, requested and actual scopes, tools, completion state, findings, and evidence references;
6. the exact canonical sources and publication artifacts needed to independently inspect the findings wherever possible;
7. any unresolved conflict, hold, ownership issue, correction route, or approval requirement.

A chat wake is a pointer only. It is not evidence and must not copy detailed source truth into a competing record.

## Deterministic Receipt Path

For attempt 1:

`projects/life-logistics-hq/worker-results/<worker_id>/<run_id>/hq-review-001.json`

The receipt must:

- conform to `apps/lifeos-dashboard/lifeos_dashboard/data/worker-hq-review.schema.json` version 1;
- use the exact run ID, Worker ID, reviewing HQ, and validated report path;
- be created once and never overwritten, renamed, moved, or deleted;
- be the only path in its creation commit;
- preserve concise evidence pointers rather than copying detailed truth;
- distinguish verified findings from recommendations requiring an owning department or Rob decision;
- remain separate from advisory, open-loop, publication, and correction lifecycle authority.

## Allowed Review States

### `VERIFIED`

Use only when:

- report integrity is `valid`;
- authority compliance is `compliant`;
- the read-only audit stayed inside the approved profile;
- the actual findings and decisive evidence are independently verified by `Maintenance_HQ`;
- no repair or external action was performed;
- `ready_for_consumption` is `true`;
- `requires_rob_validation` is `false`.

A verified audit does not itself authorize any correction, route, publication change, activation, or closure.

### `REJECTED`

Use when the report, authority, evidence, source interpretation, or independently inspectable findings are materially contradicted or noncompliant. The receipt is not consumption-ready and does not authorize audit re-execution.

### `REPAIR_REQUIRED`

Use when a correctable report or evidence defect prevents verification. The receipt is not consumption-ready. Any later repair must use a separately bounded correction-only path and must not repeat or broaden the underlying audit.

### `ROB_VALIDATION_REQUIRED`

Use only when report integrity and authority compliance are valid, but the decisive result depends on a current observation, external state, or approval that `Maintenance_HQ` cannot independently inspect. The receipt must state the exact observation or decision Rob must provide. It is not consumption-ready until the separate Rob-validation path completes.

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

The ingester must not close an advisory or system loop, wake Chief of Staff, perform Rob validation, apply a correction, mutate a route, activate a Worker, or create another queue or ledger.

## Completion Condition

The procedure completes when one immutable schema-valid HQ review receipt is created, read back with Git and checksum evidence, ingested into the existing execution row, and the resulting review branch is visible in Worker Operations.

Any correction, reconciliation, publication update, advisory lifecycle change, or department-local repair remains separate work owned by the proper source owner and authorized through the normal LifeOS path.