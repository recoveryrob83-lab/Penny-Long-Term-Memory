# Engineering Worker Rob Validation Receipt Procedure

Procedure ID: `engineering_worker_rob_validation_receipt`
Procedure Version: 1
Owner: Engineering HQ
Validator: Rob
Lifecycle State: Active

## Purpose

Define the narrow method for recording Rob's explicit observation after Engineering HQ has issued one immutable `ROB_VALIDATION_REQUIRED` review for an Engineering Worker run.

This procedure records validation evidence only. It does not create task authority, repeat Worker work, change another receipt, close a source advisory, wake Chief of Staff, activate a schedule, or create another runtime ledger.

## Entry Conditions

Rob validation may proceed only when the existing execution row has:

- `result_state: ROB_VALIDATION_REQUIRED`;
- `hq_review_state: ROB_VALIDATION_REQUIRED`;
- `requires_rob_validation: true`;
- `ready_for_consumption: false`;
- one immutable validated Worker report;
- one immutable HQ review receipt;
- exactly one deterministic observation marker named in the HQ review reason.

The marker must use:

`LIFEOS_ROB_OBSERVATION=<bounded-token>`

If the HQ receipt does not name exactly one marker, stop. Do not infer or improvise the required observation.

## Rob Observation

Rob inspects the exact user-facing surface named by the HQ review and reports whether the marker was actually observed.

Rob is not asked to copy a Worker prompt, report, receipt, or evidence bundle between rooms. The observation is only a direct yes-or-no validation of the exact marker and surface named by HQ.

## Deterministic Receipt Path

For attempt 1:

`projects/engineering/worker-results/<worker_id>/<run_id>/rob-validation-001.json`

The receipt must:

- conform to `apps/lifeos-dashboard/lifeos_dashboard/data/worker-rob-validation.schema.json` version 1;
- use the exact run ID and Worker ID;
- use `validator: Rob`;
- be created once and never overwritten, renamed, moved, or deleted;
- be the only path in its creation commit;
- include the exact HQ-requested marker in `observation`;
- include these exact evidence references:
  - `hq-review:<hq_review_path>@<hq_review_blob_sha>`;
  - `rob-observation:<exact-marker>`.

## Allowed Validation States

### `VERIFIED`

Use only when Rob observed the exact marker on the exact surface named by HQ.

- `ready_for_consumption` must be `true`.
- Ingestion records `ROB_VERIFIED` and advances the final runtime state to `READY_FOR_COS`.

### `REJECTED`

Use when Rob did not observe the exact marker or observed a contradictory result.

- `ready_for_consumption` must be `false`.
- Ingestion records and retains `ROB_REJECTED`.

## Ingestion

The deterministic Rob-validation ingester must:

- validate schema and semantic consistency;
- verify exact runtime identity and pending HQ correlation;
- require the exact marker named by HQ;
- verify one immutable creation commit containing only the receipt;
- calculate the canonical checksum;
- update only the existing `execution_history` row;
- suppress an identical duplicate receipt;
- reject a conflicting receipt;
- record Rob as the final verification actor.

It must not close the source advisory, wake Chief of Staff, create work, select priorities, perform the observation for Rob, or create another ledger.

## Completion Condition

The procedure completes when one immutable schema-valid Rob receipt is created, read back with Git and checksum evidence, ingested into the existing execution row, and the runtime reaches either `READY_FOR_COS` or `ROB_REJECTED`.
