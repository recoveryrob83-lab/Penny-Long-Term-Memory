# Maintenance HQ Worker Review Receipt Procedure

Procedure ID: `maintenance_hq_worker_review_receipt`
Procedure Version: 2
Owner: Maintenance HQ
Lifecycle State: Active
Updated: 2026-07-28

## Purpose

Define the narrow `Maintenance_HQ` procedure for reviewing one deterministically validated `Maintenance_Worker` result and creating one immutable HQ review receipt.

This procedure applies only to Maintenance-owned Worker runs whose existing SQLite execution row has reached `REPORT_VALIDATED` and whose canonical verification mode is `IMMEDIATE_HQ`.

Version 2 preserves the strict read-only review path and adds independent verification for assignments that explicitly authorized bounded writes before execution. Review verifies existing evidence; it does not authorize additional work.

## Authority

Rob authorized version 2 through `ADV-20260728-054` revision 1 and approval reference `ROB-DIRECT-MAINTENANCE-HQ-REVIEW-V2-20260728`.

This procedure authorizes `Maintenance_HQ` to review one bounded result and create one immutable review receipt at an exactly authorized attempt path. It does not authorize:

- Worker activation, route registration, route capture, deployment-state change, schedule creation, pause or resume action, send-budget reset, or unattended execution;
- source-advisory, system-loop, or department-record closure;
- re-execution or broadening of the Worker's assignment;
- modification, overwrite, renaming, moving, or deletion of a Worker report or earlier HQ review;
- review of another department's Worker;
- Chief of Staff wake or consumption;
- Rob validation;
- shared-rule or department-local repair, new tools, new connectors, spending, or new authority;
- runtime mutation, Engineering implementation, or creation of a second runtime ledger.

Publishing version 2 does not authorize Engineering runtime implementation or a later review attempt. Those require the separately bounded authorization and material advisory revision specified by `ADV-20260728-054`.

## Required Inputs

`Maintenance_HQ` must inspect:

1. the exact canonical assignment, advisory ID, and revision;
2. the current `Maintenance_Worker` profile, task procedure, and result-submission procedure versions;
3. the deterministically validated Worker report path;
4. the report checksum, creation commit, and blob SHA preserved on the existing execution row;
5. the report's authority, requested and actual scopes, tools, completion state, findings, controlled outcome, and evidence references;
6. for bounded writes, the exact authorization class, approval reference, requested write scopes, exclusions, and task-procedure version;
7. independently inspectable commit, blob, checksum, and read-back evidence for each claimed write;
8. the canonical sources needed to verify decisive findings;
9. unresolved conflicts, holds, ownership issues, correction routes, or approval requirements;
10. any earlier immutable HQ review and the exact authority for a later attempt.

A chat wake is a pointer only. It is not evidence and must not copy detailed source truth into a competing record.

## Deterministic Receipt Path

HQ review attempt `N` uses:

`projects/life-logistics-hq/worker-results/<worker_id>/<run_id>/hq-review-<NNN>.json`

The attempt number is one-based and zero-padded. Attempt 1 uses `hq-review-001.json`; attempt 2 uses `hq-review-002.json`.

Attempt 1 remains the normal path when no earlier review exists. A later attempt is permitted only when a separately authorized correction or review-resume path identifies:

- the same run, Worker, validated report, report checksum, report creation commit, and report blob;
- the same authoritative advisory, assignment revision, and task procedure;
- the earlier HQ review path, state, creation commit, blob, and checksum;
- the procedural or evidence defect that blocked a terminal review;
- the exact new attempt number and create-once path;
- confirmation that Worker re-execution, report replacement, and scope expansion remain unauthorized.

A later receipt supplements immutable history. It must not overwrite, rename, move, delete, conceal, or contradict factual evidence in an earlier receipt. It may reach a different review state only when new procedure authority or corrected evidence resolves the earlier receipt's stated blocker.

Every receipt must:

- conform to `apps/lifeos-dashboard/lifeos_dashboard/data/worker-hq-review.schema.json` version 1;
- use the exact attempt, run ID, Worker ID, reviewing HQ, and validated report path;
- correlate through concise evidence pointers to the same advisory, assignment, task procedure, report commit, report blob, and report checksum;
- be created once and never overwritten, renamed, moved, or deleted;
- be the only path in its creation commit;
- distinguish verified findings from recommendations or holds requiring an owner or Rob decision;
- remain separate from advisory, open-loop, publication, correction, and source-owner lifecycle authority.

## Allowed Review States

### `VERIFIED`

Use only when:

- report integrity is `valid`;
- authority compliance is `compliant`;
- the exact report, assignment, Worker, advisory revision, task procedure, and decisive evidence are independently correlated and verified by `Maintenance_HQ`;
- actual reads, writes, and tools stayed within exact approved authority;
- no prohibited, destructive, external, runtime, profile, procedure, advisory-lifecycle, or scope-expanding action occurred;
- `work_verification_state` is `verified`;
- `ready_for_consumption` is `true`;
- `requires_rob_validation` is `false`.

For a read-only assignment, also require that the assignment authorized no source-record repair or external action and none occurred.

For an explicitly authorized bounded-write assignment, also require that:

- the assignment carried exact bounded-write authority before execution;
- the Worker profile and task procedure permitted the task class and write scopes;
- every actual write stayed within requested scopes and exclusions;
- each completed write has independently inspectable commit and read-back evidence;
- the report truthfully distinguishes completed, partial, held, failed, and unverified work;
- unresolved holds identify the correct owner, destination, and review or resume condition.

A partial or `REPORT_AND_HOLD` result may be `VERIFIED` when the completed work and preserved holds are truthful, bounded, and independently verified. This verifies the result, not completion of every source issue.

A `VERIFIED` receipt does not authorize advisory closure, further repair, route or publication changes, activation, or new work.

### `REJECTED`

Use when the report, authority, evidence, source interpretation, or independently inspectable work is materially contradicted or noncompliant. The receipt is not consumption-ready and does not authorize re-execution.

### `REPAIR_REQUIRED`

Use when a correctable report, evidence, correlation, or review-path defect prevents verification. The receipt is not consumption-ready and must distinguish:

- a defect in the Worker report or completed work;
- a defect in evidence or correlation;
- a procedural applicability defect in the HQ review path.

A procedural applicability defect does not invalidate an otherwise valid, authority-compliant report or its completed repairs. After the procedure or review path is corrected, a later immutable review attempt may inspect the same validated report and existing work without rerunning, replacing, or broadening the assignment.

### `ROB_VALIDATION_REQUIRED`

Use only when report integrity and authority compliance are valid, but the decisive result depends on a current observation, external state, or approval that `Maintenance_HQ` cannot independently inspect. State the exact observation or decision Rob must provide. The receipt is not consumption-ready until separate Rob validation completes.

## Ready for Consumption

Set `ready_for_consumption: true` only when:

- `review_state` is `VERIFIED`;
- report integrity is `valid`;
- authority compliance is `compliant`;
- work verification is `verified`;
- the receipt is exactly correlated and immutable;
- decisive evidence has been independently checked;
- partial completion and holds are accurately represented with owners and conditions;
- no Rob validation remains required.

Consumption readiness means an authorized downstream process may use the verified report, completed-work evidence, and preserved holds. It does not close the advisory, resolve holds, authorize correction, or create a new assignment.

All other review states use `ready_for_consumption: false`.

## Ingestion

The deterministic HQ review ingester must:

- validate schema and semantic consistency;
- verify exact runtime identity and validated report correlation;
- verify the exact authorized attempt and path;
- verify earlier-review correlation for an attempt greater than 1;
- verify one immutable creation commit containing only the receipt;
- calculate the canonical content checksum;
- update only the existing `execution_history` row;
- preserve earlier immutable review evidence;
- suppress an identical duplicate receipt;
- reject an unauthorized attempt, path, or conflicting receipt;
- advance runtime only according to the accepted review state.

The ingester must not close an advisory or system loop, wake Chief of Staff, perform Rob validation, apply a correction, mutate a route, activate a Worker, re-execute work, or create another queue or ledger.

Engineering implementation for later attempts remains blocked until separately authorized under a material revision of `ADV-20260728-054`.

## Hold Conditions

Do not create a receipt when:

- the report is not deterministically validated;
- exact run, Worker, owning HQ, report, advisory, assignment revision, procedure, commit, blob, or checksum correlation fails;
- bounded writes lack explicit prior authority or exceed scope;
- decisive evidence cannot be independently inspected and the case does not fit `ROB_VALIDATION_REQUIRED`;
- the target path already exists;
- a later attempt lacks exact authorization or earlier-review correlation;
- runtime cannot accept the authorized attempt;
- the request would rerun the Worker, overwrite immutable evidence, broaden authority, close source work, or begin unauthorized Engineering implementation.

## Completion Condition

Procedure use completes when one immutable schema-valid HQ review receipt at the exact authorized attempt path is created once, read back with commit, blob, and canonical checksum evidence, ingested through a separately authorized compatible runtime path, and visible in Worker Operations.

Phase 1 of `ADV-20260728-054` completes when procedure version 2 is committed, read back, and its exact commit SHA and canonical checksum are reported to `Engineering_HQ`.

Any runtime implementation, later review attempt, correction, reconciliation, publication update, advisory lifecycle change, source-owner repair, Chief of Staff wake, or Rob validation remains separately owned and authorized.
