---
procedure_id: engineering_worker_response_bridge_validation
procedure_version: 1
owning_department: engineering
task_class: engineering_read_only_verification
authorization_classes:
  - READ_ONLY
required_verification_mode: IMMEDIATE_HQ
receiver_parameter_schema_json: {"targets":"array","verification_questions":"array"}
receiver_required_parameters_json: ["targets","verification_questions"]
receiver_approved_tools_json: ["GitHub"]
receiver_source_references_required: true
---

# Engineering Worker Response Bridge Validation Procedure

Updated: 2026-07-20
Owner: Engineering HQ
Status: Active / Canonical

## Purpose

Perform one bounded read-only verification that exercises Package E Slice 2 from canonical advisory dispatch through structured Worker reporting, semantic receiver reconciliation, same-row controlled outcome, and separate Engineering HQ review.

This procedure creates no write authority, changes no advisory lifecycle state, and delegates no closure authority.

## Required Parameters

- `targets`: a JSON array of exact repository-relative paths.
- `verification_questions`: a JSON array of bounded questions to answer from those targets.

## Entry Conditions

The Worker must validate the exact envelope, advisory revision, Engineering Worker profile version 1, this procedure version 1, `READ_ONLY` authority, `IMMEDIATE_HQ` verification, exact read scopes, empty write scopes, GitHub-only tooling, route state, pause state, and duplicate state.

Failure of any entry condition requires `REPORT_AND_HOLD` unless broader authority or a Rob decision is required, in which case return `ELEVATE_FOR_APPROVAL`.

## Allowed Actions

The Worker may read only the exact authorized sources, answer the bounded verification questions, preserve source paths and current blob SHAs when available, and return one evidence-backed report.

## Prohibited Actions

The Worker must not modify GitHub or any other system, run code or tests, use terminal or desktop automation, edit the advisory or Advisory Index, alter routing or receiver state, close the advisory, broaden the source list, or create follow-up work.

## Completion Rule

The bounded verification is complete when every exact target is read, every question is answered or explicitly marked unverifiable, required evidence is reported, and no write or external action occurs.

Finding drift does not itself fail the inspection. Return `IMPLEMENT` when the authorized inspection completed truthfully. Return `REPORT_AND_HOLD` when validation or safe inspection cannot continue. Return `ELEVATE_FOR_APPROVAL` only when broader authority or a Rob decision is required.

## Required Structured Report

The final response must include exactly one line beginning with `LIFEOS_WORKER_REPORT=` followed by one compact JSON object with these exact fields:

- `wrapper_id`
- `run_id`
- `worker_id`
- `profile_version`
- `owning_department`
- `task_id`
- `task_revision`
- `procedure_id`
- `procedure_version`
- `authorization_source`
- `verification_mode`
- `controlled_outcome`
- `completion_state`
- `evidence_references`
- `actual_read_scopes`
- `actual_write_scopes`
- `actual_tools`
- `verification_state`
- `external_actions_verified`
- `approval_required_discovered`
- optional `failure_reason`

For a successful read-only inspection:

- `completion_state` is `completed`;
- `verification_state` is `pending` until Engineering HQ review;
- `actual_write_scopes` is an empty array;
- `actual_tools` is `["GitHub"]`;
- `external_actions_verified` is `true`, meaning the report verifies that no external action occurred;
- `approval_required_discovered` is `false`;
- `evidence_references` includes the exact sources read and current GitHub blob SHAs when available.

The human-readable report may precede the machine line. The machine line must be the only `LIFEOS_WORKER_REPORT=` line.

## Verification and Closure

Engineering HQ performs `IMMEDIATE_HQ` review. The Worker does not acknowledge, implement, verify, edit, or close the advisory lifecycle.
