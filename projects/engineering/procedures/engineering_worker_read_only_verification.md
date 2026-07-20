---
procedure_id: engineering_worker_read_only_verification
procedure_version: 1
owning_department: engineering
task_class: engineering_read_only_verification
authorization_classes:
  - READ_ONLY
required_verification_mode: IMMEDIATE_HQ
---

# Engineering Worker Read-Only Verification Procedure

Updated: 2026-07-20
Owner: Engineering HQ
Status: Active / Canonical

## Purpose

Perform one bounded, read-only verification of explicitly named Engineering-owned GitHub sources and return an evidence-linked controlled outcome.

This procedure creates no write authority, changes no lifecycle state, and delegates no advisory closure authority.

## Entry Conditions

The Worker must confirm all of the following before accepting the assignment:

- the target Worker ID is `engineering_worker`;
- the loaded Worker profile is version 1;
- the advisory lifecycle state is `OPEN`;
- the advisory revision is newer than any revision already processed for that advisory;
- the target department is Engineering HQ;
- the caller is authorized by the Worker profile;
- the authorization class is `READ_ONLY`;
- the verification mode is `IMMEDIATE_HQ`;
- exact read targets and authoritative source references are present;
- requested write scopes are empty;
- requested tools are limited to approved GitHub read operations;
- route, pause, duplication, and source-boundary checks permit execution.

Failure of any entry condition requires `REPORT_AND_HOLD` unless Rob must authorize broader authority, in which case return `ELEVATE_FOR_APPROVAL`.

## Required Parameters

The advisory must provide:

- `targets`: a JSON array of exact repository-relative paths;
- `verification_questions`: a JSON array of bounded questions to answer from those targets.

Every target must remain under:

- `projects/engineering/`; or
- `apps/lifeos-dashboard/`.

No inferred, neighboring, or merely relevant source may be added.

## Canonical Source Loading Order

For each run, load only:

1. the canonical Worker Boot path;
2. the Life OS execution protocol;
3. the Worker execution contract;
4. Engineering HQ identity;
5. the exact `engineering_worker` profile;
6. the exact advisory revision;
7. this exact procedure, version 1;
8. only the target files explicitly named in the advisory.

The Worker must not automatically load the complete Engineering handoff, status, open loops, notebooks, history, other departments, or unrelated advisory records unless the advisory explicitly names them.

## Allowed Actions

The Worker may:

- fetch and read the current version of each exact target;
- preserve the observed GitHub path and blob SHA when available;
- answer only the bounded verification questions;
- classify each finding as aligned, drifted, conflicting, missing, or unverifiable;
- return an evidence-backed report in the Worker chat.

## Prohibited Actions

The Worker must not:

- modify GitHub or any other source;
- edit the advisory or Advisory Index;
- close, acknowledge, implement, or verify the advisory lifecycle;
- change its profile, registry, route, deployment, pause, wake, or receiver state;
- execute code, tests, terminal commands, or desktop automation;
- use Gmail, Drive, Trello, Todoist, Calendar, Slack, financial tools, or public web sources;
- propose discovered work as an active commitment;
- expand the target list because another source appears relevant.

## Execution Method

1. Validate the envelope, advisory, procedure identity, caller, target, revision, parameters, scopes, tools, and verification mode.
2. Read every exact target from GitHub.
3. Answer each verification question using only the authorized targets.
4. Distinguish verified facts from inference or unavailable evidence.
5. Record what was read and explicitly state that no writes occurred.
6. Return exactly one controlled outcome.

Discovery of drift does not by itself mean the procedure failed. The verification task may return `IMPLEMENT` when the requested inspection was completed and the drift was accurately reported.

## Required Evidence

The report must include:

- wrapper ID;
- run ID;
- Worker ID;
- Worker profile version;
- advisory ID and revision;
- procedure ID and version;
- authorization source;
- verification mode;
- exact paths read;
- current source SHAs when available;
- each verification question and finding;
- unresolved conflicts or uncertainty;
- writes performed: `None`;
- external actions performed: `None`;
- review condition;
- exactly one controlled outcome.

## Controlled Outcomes

Return `IMPLEMENT` when:

- the assignment validated;
- every authorized target was read;
- every verification question was answered or explicitly marked unverifiable;
- required evidence was reported;
- no unauthorized action occurred.

Return `REPORT_AND_HOLD` when:

- a required source, field, revision, parameter, route, procedure, or authority is missing;
- the advisory and canonical sources conflict;
- the task requests or requires a write;
- exact current sources cannot be read;
- duplicate or stale processing is detected;
- safe verification cannot continue.

Return `ELEVATE_FOR_APPROVAL` when:

- the task requires broader authority;
- a cross-department or shared-governance action is required;
- a material exception or Rob decision is necessary.

## Verification and Closure

Engineering HQ performs `IMMEDIATE_HQ` review.

The Worker does not edit or close the advisory under this procedure. Engineering HQ retains acknowledgement, verification, lifecycle, and closure authority.
