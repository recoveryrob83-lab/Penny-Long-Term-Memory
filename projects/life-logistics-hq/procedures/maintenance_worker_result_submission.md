---
procedure_id: maintenance_worker_result_submission
procedure_version: 1
owning_department: maintenance
procedure_class: execution_reporting
result_contract_id: lifeos_worker_result
result_contract_version: 1
approved_tool: GitHub
required_verification_mode: IMMEDIATE_HQ
---

# Maintenance Worker Result Submission Procedure

Updated: 2026-07-25
Owner: Maintenance HQ
Status: Active / Canonical / Maintenance pilot only

## Purpose

Define the one canonical method by which `maintenance_worker` creates an immutable, machine-readable result artifact for an already-authorized run.

This procedure supplies reporting mechanics only. It does not create task authority, broaden task scope, authorize repair, change advisory lifecycle, or replace `Maintenance_HQ` review.

## Entry Conditions

The Worker may use this procedure only when the canonical assignment supplies all of the following:

- `Result Contract ID: lifeos_worker_result`;
- `Result Contract Version: 1`;
- `Result Submission Procedure ID: maintenance_worker_result_submission`;
- `Result Submission Procedure Version: 1`;
- `Owning Department: maintenance`;
- `Worker ID: maintenance_worker`;
- exact run ID;
- positive result attempt number;
- exact deterministic result path;
- `Result Create Only: true`;
- `Result Overwrite Allowed: false`;
- `Result Work Reexecution Authorized: false`;
- `Result Scope Expansion Authorized: false`;
- the exact result path inside `Requested Write Scopes JSON`;
- `GitHub` inside `Requested Tools JSON`;
- an authorization class permitting the exact reporting write;
- `Verification Mode: IMMEDIATE_HQ`.

If any field is missing, malformed, conflicting, stale, or outside the Worker profile, return `REPORT_AND_HOLD`. Do not improvise a path, attempt, schema, or authority.

## Deterministic Path

Worker report attempts use:

`projects/life-logistics-hq/worker-results/maintenance_worker/<run_id>/report-<attempt>.json`

The attempt number is zero-padded to three digits. Attempt 1 therefore ends in:

`report-001.json`

The Worker must verify that the assignment's result path exactly matches the path derived from its department path, Worker ID, run ID, and attempt.

## Canonical Schema

The report must validate against:

`apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-report.schema.json`

Canonical correctly typed examples live at:

`apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-examples.json`

The Worker must preserve JSON types exactly. Versions, revisions, and attempts are integers; authorization flags are booleans; arrays remain arrays; `failure_reason` is a string or `null`; and `verification_state` remains `pending` or `unavailable` until HQ review occurs.

## Allowed Action

After completing, holding, or elevating the authorized read-only assignment, the Worker may create exactly one new report artifact at the exact path and attempt authorized by the assignment.

The Worker may use GitHub create-file behavior only. It must confirm that the exact target does not already exist before creation.

The report may truthfully state one controlled outcome:

- `IMPLEMENT`;
- `REPORT_AND_HOLD`;
- `ELEVATE_FOR_APPROVAL`.

The report is evidence pending deterministic ingestion and `Maintenance_HQ` review.

## Prohibited Actions

The Worker must not:

- overwrite, edit, rename, move, or delete an existing result artifact;
- create a different attempt number than the one authorized;
- create files outside the exact current-run result folder;
- modify an advisory, Advisory Index, shared contract, status, open loops, handoff, profile, procedure, implementation file, publication artifact, route, runtime database, or another evidence artifact;
- repeat or broaden the underlying audit because report creation failed;
- claim HQ or Rob verification;
- close the source advisory or system loop;
- place the machine report only in chat instead of the exact GitHub result path.

## Existing-File Behavior

If the exact result path already exists, do not overwrite it. Return `REPORT_AND_HOLD` in chat with the path conflict and wait for a separately authorized correction attempt.

A later report-repair wake may authorize a new immutable attempt such as `report-002.json`. That correction authority permits report repair only and never authorizes audit re-execution or scope expansion.

## Evidence

The Worker report must preserve the exact fields required by the canonical schema, including:

- envelope and assignment identity;
- profile, procedure, authorization, and verification metadata;
- requested and actual actions;
- controlled outcome and completion state;
- exact evidence and source references;
- actual read, write, and tool use;
- what did not occur;
- unresolved risks or conflicts;
- routed owner and destination where applicable;
- review condition;
- external-action verification;
- approval discovery;
- failure reason when applicable.

After creation, the Worker must read back the file and report the exact path, commit SHA, blob SHA when available, and canonical content checksum.

## Completion Rule

Result submission is complete only when:

1. the exact schema-valid artifact was created at the authorized path;
2. no earlier artifact was overwritten;
3. read-back confirms the stored content;
4. commit, blob, path, and checksum evidence are preserved;
5. no maintenance repair, task re-execution, or scope expansion occurred;
6. `Maintenance_HQ` review remains pending.

## Ownership and Rollout

This procedure is owned by `Maintenance_HQ` and applies only to the initial bounded `Maintenance_Worker` pilot approved by Rob after the Package F Wave 0B governance review.

It does not alter the shared Worker contract, activate the Worker, register a route, grant maintenance-write authority, or authorize adoption by another department.