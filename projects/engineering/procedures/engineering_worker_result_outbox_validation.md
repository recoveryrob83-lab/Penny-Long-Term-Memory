---
procedure_id: engineering_worker_result_outbox_validation
procedure_version: 1
owning_department: engineering
task_class: engineering_read_only_verification
authorization_classes:
  - BOUNDED_WRITE
required_verification_mode: IMMEDIATE_HQ
receiver_parameter_schema_json: {"targets":"array","verification_questions":"array"}
receiver_required_parameters_json: ["targets","verification_questions"]
receiver_approved_tools_json: ["GitHub"]
receiver_source_references_required: true
result_submission_procedure_id: engineering_worker_result_submission
result_submission_procedure_version: 1
result_contract_id: lifeos_worker_result
result_contract_version: 1
---

# Engineering Worker Result Outbox Validation Procedure

Updated: 2026-07-21
Owner: Engineering HQ
Status: Active / Canonical / Package E Slice 3 pilot

## Purpose

Perform one bounded read-only Engineering verification and submit the resulting evidence through the immutable Package E Worker result outbox.

The substantive work is read-only. `BOUNDED_WRITE` authorizes only the exact current-run result artifact named by the advisory.

## Required Parameters

- `targets`: a JSON array of exact repository-relative paths.
- `verification_questions`: a JSON array of bounded questions answered only from those targets.

## Entry Conditions

The Worker must validate:

- the exact execution wrapper and advisory revision;
- `engineering_worker`, profile version 1, and owning department `engineering`;
- this procedure version 1;
- `BOUNDED_WRITE` authorization;
- `IMMEDIATE_HQ` verification;
- exact read scopes and GitHub-only tooling;
- one exact result path as the only authorized reporting write;
- the complete `lifeos_worker_result` version 1 submission contract;
- `engineering_worker_result_submission` version 1;
- route, pause, duplicate, and existing-file state.

Failure of an entry condition requires `REPORT_AND_HOLD` unless a genuine Rob approval is required, in which case return `ELEVATE_FOR_APPROVAL`.

## Allowed Work

The Worker may:

1. read only the exact authorized targets and required canonical boot, profile, advisory, and procedure sources;
2. answer the bounded verification questions;
3. preserve exact source paths and current blob SHAs when available;
4. create exactly one schema-valid `report-001.json` artifact at the deterministic current-run path authorized by the advisory;
5. read back the new artifact and preserve commit, blob, path, and checksum evidence.

## Prohibited Work

The Worker must not:

- modify the inspected targets;
- modify GitHub except for the exact authorized result artifact;
- run code or tests unless the advisory separately and explicitly authorizes them;
- use terminal or desktop automation;
- edit the advisory, Advisory Index, status, open loops, profile, procedure, routing, runtime database, or any other record;
- create more than one report attempt;
- overwrite an existing artifact;
- broaden the source list;
- create follow-up work;
- close the advisory;
- claim HQ verification.

## Completion Rule

The bounded verification is complete when:

- every exact target is read;
- every question is answered or explicitly marked unverifiable;
- one truthful controlled outcome is selected;
- one schema-valid immutable report artifact is created at the exact authorized path;
- creation is read back and evidenced;
- no other write or external action occurs;
- Engineering HQ review remains pending.

Finding drift does not itself fail the inspection. Return `IMPLEMENT` when the authorized inspection and report submission complete truthfully. Return `REPORT_AND_HOLD` when validation, inspection, or immutable reporting cannot continue safely. Return `ELEVATE_FOR_APPROVAL` only when broader authority or a Rob decision is genuinely required.

## Required Result Procedure

Load and follow:

`projects/engineering/procedures/engineering_worker_result_submission.md`

The canonical schema is:

`apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-report.schema.json`

The canonical examples are:

`apps/lifeos-dashboard/lifeos_dashboard/data/worker-result-examples.json`

## Verification and Closure

Engineering HQ performs `IMMEDIATE_HQ` review after deterministic ingestion. The Worker does not acknowledge, implement, verify, edit, or close the source advisory lifecycle.
