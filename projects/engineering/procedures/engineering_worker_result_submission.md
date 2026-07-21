---
procedure_id: engineering_worker_result_submission
procedure_version: 1
owning_department: engineering
procedure_class: execution_reporting
result_contract_id: lifeos_worker_result
result_contract_version: 1
approved_tool: GitHub
required_verification_mode: IMMEDIATE_HQ
---

# Engineering Worker Result Submission Procedure

Updated: 2026-07-21
Owner: Engineering HQ
Status: Active / Canonical / Engineering pilot only

## Purpose

Define the one canonical method by which `engineering_worker` creates an immutable, machine-readable result artifact for an already-authorized run.

This procedure supplies reporting mechanics only. It does not create task authority, broaden task scope, authorize re-execution, change advisory lifecycle, or replace Engineering HQ review.

## Entry Conditions

The Worker may use this procedure only when the canonical assignment supplies all of the following:

- `Result Contract ID: lifeos_worker_result`;
- `Result Contract Version: 1`;
- `Result Submission Procedure ID: engineering_worker_result_submission`;
- `Result Submission Procedure Version: 1`;
- exact owning department;
- exact Worker ID;
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
- a required verification mode.

If any field is missing, malformed, conflicting, stale, or outside the Worker profile, return `REPORT_AND_HOLD`. Do not improvise a path or schema.

## Deterministic Path

Worker report attempts use:

`projects/<department>/worker-results/<worker_id>/<run_id>/report-<attempt>.json`

The attempt number is zero-padded to three digits. Attempt 1 therefore ends in:

`report-001.json`

The Worker must verify that the assignment's result path exactly matches the path derived from its department, Worker ID, run ID, and attempt.

## Canonical Schema

The report must validate against:

`apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-report.schema.json`

Canonical correctly typed examples live at:

`apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-examples.json`

The Worker must preserve JSON types exactly. In particular:

- versions, revisions, and attempts are integers;
- authorization flags are booleans;
- arrays remain arrays even when empty;
- `failure_reason` is either a string or `null`;
- `verification_state` remains `pending` or `unavailable`, never `verified`, until HQ review occurs.

## Allowed Action

After completing, holding, or elevating the authorized assignment, the Worker may create exactly one new report artifact at the exact path and attempt authorized by the assignment.

The Worker may use GitHub create-file behavior only. It must fetch or otherwise confirm that the exact target does not already exist before creation.

The report may truthfully state one controlled outcome:

- `IMPLEMENT`;
- `REPORT_AND_HOLD`;
- `ELEVATE_FOR_APPROVAL`.

The report is evidence pending deterministic ingestion and Department HQ review.

## Prohibited Actions

The Worker must not:

- overwrite, edit, rename, move, or delete an existing result artifact;
- create a different attempt number than the one authorized;
- create files outside the exact current-run result folder;
- modify an advisory, Advisory Index, status, open loops, profile, procedure, implementation file, routing record, runtime database, or another evidence artifact through this reporting authority;
- repeat the underlying work merely because report creation failed;
- broaden read, write, tool, connector, or external-action scope;
- claim HQ or Rob verification;
- close the source advisory;
- place the machine report only in chat instead of the exact GitHub result path.

## Existing-File Behavior

If the exact result path already exists, do not overwrite it. Return `REPORT_AND_HOLD` in chat with the path conflict and wait for a separately authorized repair attempt.

A later report-repair wake may authorize a new immutable attempt such as `report-002.json`. That repair authority permits report correction only and never authorizes work re-execution.

## Evidence

The Worker report must preserve the exact fields required by the canonical schema, including:

- envelope and assignment identity;
- profile, procedure, authorization, and verification metadata;
- requested and actual actions;
- controlled outcome and completion state;
- exact evidence references;
- actual read, write, and tool use;
- what did not occur;
- unresolved risks;
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
5. no task re-execution or scope expansion occurred;
6. Engineering HQ review remains pending.

## Ownership and Rollout

This procedure is owned by Engineering HQ and applies only to the Engineering Worker pilot.

It does not alter the shared Worker contract or grant universal Worker result-write authority. Cross-department adoption requires Life OS Maintenance HQ review and explicit authorization by each owning Department HQ.
