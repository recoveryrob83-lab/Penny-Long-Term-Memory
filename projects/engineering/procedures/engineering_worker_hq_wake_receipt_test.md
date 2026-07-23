---
procedure_id: engineering_worker_hq_wake_receipt_test
procedure_version: 1
owning_department: engineering
procedure_class: bounded_communication_verification
result_contract_id: lifeos_worker_result
result_contract_version: 1
required_verification_mode: IMMEDIATE_HQ
---

# Engineering Worker HQ-Wake Receipt Test

Updated: 2026-07-23
Owner: Engineering HQ
Status: Active bounded pilot

## Purpose

Prove the complete GitHub-first communication chain without substantive engineering work:

1. the dashboard discovers one fresh advisory through the Advisory Index;
2. the dashboard submits the wake to `engineering_worker`;
3. the Worker reads the exact advisory revision;
4. the Worker creates one immutable schema-valid result artifact recording that the advisory was read;
5. the dashboard discovers and validates the result artifact;
6. the dashboard wakes Engineering HQ for `IMMEDIATE_HQ` review;
7. Engineering HQ reviews the evidence and reports the verified outcome to Rob.

The Worker does not sign off its own work and does not change advisory lifecycle. The result remains pending until Engineering HQ review.

## Authorized Input

- Advisory: `ADV-20260723-051`
- Revision: 1
- Wrapper ID: `WAKE-ADV-20260723-051-R1`
- Run ID: `RUN-ADV-20260723-051-R1`
- Worker ID: `engineering_worker`
- Result path: `projects/engineering/worker-results/engineering_worker/RUN-ADV-20260723-051-R1/report-001.json`
- Chat marker: `WORKER_RESULT_READY=ADV-20260723-051`

## Authorized Reads

Read only the required Worker boot chain, shared execution contracts, Engineering identity, Worker profile, the Advisory Index routing line for this advisory, the exact advisory, this procedure, the canonical result-submission procedure, the Worker result schema, and the typed result examples.

Do not inspect unrelated advisories, notebooks, status, open loops, code, tests, runtime databases, or another department's files.

## Authorized Work

The bounded work is only to confirm that the Worker loaded and understood the exact advisory revision. No technical implementation, debugging, maintenance, strategic judgment, or external action is authorized.

After the read is complete, create exactly one immutable Worker result artifact at the authorized result path using `engineering_worker_result_submission`, version 1.

For a successful test, the report must truthfully record:

- `controlled_outcome`: `IMPLEMENT`;
- `completion_state`: `completed`;
- `verification_state`: `pending`;
- `actual_action_attempted`: the exact advisory revision was read and one immutable receipt report was created;
- `actual_write_scopes`: only the exact result path;
- `actual_tools`: only `GitHub`;
- `approval_required_discovered`: false;
- `external_actions_verified`: true;
- `failure_reason`: null;
- `review_condition`: Engineering HQ must verify the report identity, authority, exact advisory-read evidence, write scope, and absence of additional work.

The report's evidence must include the exact advisory path and current blob SHA, this procedure path and blob SHA, and the result-submission procedure and schema references used.

## Chat Response

After the result artifact is created and read back, respond briefly in the Engineering Worker chat. Include this exact line once:

`WORKER_RESULT_READY=ADV-20260723-051`

Return exactly one controlled outcome:

- `IMPLEMENT` when the exact advisory was read and the immutable result was created and read back;
- `REPORT_AND_HOLD` when any required source, authority, path, schema, create-only write, or read-back cannot be completed safely;
- `ELEVATE_FOR_APPROVAL` only when broader authority or a new Rob decision is genuinely required.

## Prohibitions

Do not edit the advisory, Advisory Index, Engineering board, profile, procedure, status, open loops, runtime database, or another file. Do not create an HQ-review artifact, Rob-validation artifact, task, schedule, or duplicate advisory. Do not close or advance lifecycle state. Do not run code or tests. Do not use desktop automation or any connector other than exact GitHub reads and the one create-only result write. Do not perform substantive engineering work.

## Completion Condition

Worker execution is complete only when the exact advisory revision has been read, one schema-valid immutable report exists at the authorized result path and has been read back, the exact chat marker has been rendered once, no other work or write occurred, and Engineering HQ review remains pending.