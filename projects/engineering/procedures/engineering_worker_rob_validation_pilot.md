---
procedure_id: engineering_worker_rob_validation_pilot
procedure_version: 1
owning_department: engineering
task_class: engineering_read_only_verification
authorization_classes:
  - BOUNDED_WRITE
required_verification_mode: IMMEDIATE_HQ
receiver_parameter_schema_json: {"targets":"array","verification_questions":"array","rob_observation_marker":"string"}
receiver_required_parameters_json: ["targets","verification_questions","rob_observation_marker"]
receiver_approved_tools_json: ["GitHub"]
receiver_source_references_required: true
result_submission_procedure_id: engineering_worker_result_submission
result_submission_procedure_version: 1
result_contract_id: lifeos_worker_result
result_contract_version: 1
---

# Engineering Worker Rob Validation Pilot Procedure

Updated: 2026-07-22
Owner: Engineering HQ
Status: Active / Canonical / Package E Slice 6 pilot

## Purpose

Perform one bounded Engineering read-only verification, submit one immutable Worker report, and then render one exact observation marker in the Worker chat so the explicit Rob-validation branch can be proven without browser response scraping.

The substantive repository work is read-only. `BOUNDED_WRITE` authorizes only the exact current-run report artifact named by the advisory.

## Required Parameters

- `targets`: a JSON array of exact repository-relative paths.
- `verification_questions`: a JSON array of bounded questions answered only from those targets.
- `rob_observation_marker`: one exact token beginning with `LIFEOS_ROB_OBSERVATION=`.

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
- route, pause, duplicate, and existing-file state;
- one nonempty observation marker with no spaces.

Failure of an entry condition requires `REPORT_AND_HOLD` unless a genuine Rob approval is required, in which case return `ELEVATE_FOR_APPROVAL`.

## Allowed Work

The Worker may:

1. read only the exact authorized targets and required canonical boot, profile, advisory, and procedure sources;
2. answer the bounded verification questions;
3. create exactly one schema-valid `report-001.json` at the deterministic current-run path;
4. read back the report and preserve commit, blob, path, and checksum evidence when available;
5. after successful report creation and read-back, render the exact `rob_observation_marker` once in the final Worker chat response.

## Required Report Meaning

For a successful `IMPLEMENT` report:

- `completion_state` is `completed`;
- `verification_state` remains `pending`;
- `actual_action_attempted` truthfully states that the bounded inspection and report creation completed and that the exact marker was rendered in the final Worker response;
- `unresolved_risks` states that Engineering HQ cannot independently inspect the final Worker-chat marker without violating the courier no-response-scraping boundary;
- `review_condition` asks Engineering HQ to validate report integrity, authority, and repository evidence, then use `ROB_VALIDATION_REQUIRED` unless the exact marker is independently available through an authorized source.

The report does not itself prove that Rob saw the marker.

## Final Chat Response

After the immutable report has been created and read back, the final response must:

- identify the controlled outcome;
- state the report path and available commit/blob evidence;
- display the exact `rob_observation_marker` on its own line exactly once;
- not ask Rob to copy any prompt, report, receipt, or evidence bundle;
- not claim HQ or Rob verification.

## Prohibited Work

The Worker must not:

- modify any inspected target;
- modify GitHub except for the exact authorized report artifact;
- run code or tests unless separately authorized;
- use terminal or desktop automation;
- edit the advisory, Advisory Index, status, open loops, profile, procedure, routing, runtime database, or any other record;
- create more than one report attempt;
- overwrite an existing artifact;
- broaden the source list;
- close the advisory;
- claim HQ or Rob verification;
- capture, scrape, or transport its own assistant response as machine evidence.

## Completion Rule

The bounded pilot work is complete when:

- every exact target is read;
- every question is answered or explicitly marked unverifiable;
- one schema-valid immutable report is created and read back;
- no other write or external action occurs;
- the exact observation marker is rendered once in the final Worker response;
- Engineering HQ and Rob validation remain pending.

## Required Result Procedure

Load and follow:

`projects/engineering/procedures/engineering_worker_result_submission.md`

## Verification and Closure

Engineering HQ performs `IMMEDIATE_HQ` review after deterministic ingestion. Because the decisive marker exists only in the Worker chat, Engineering HQ should use `ROB_VALIDATION_REQUIRED` when report integrity and authority are valid but the marker cannot be independently inspected. Rob then follows `projects/engineering/procedures/engineering_worker_rob_validation_receipt.md`.

Neither the Worker, HQ receipt, Rob receipt, courier, ingester, nor dashboard closes the source advisory automatically.
