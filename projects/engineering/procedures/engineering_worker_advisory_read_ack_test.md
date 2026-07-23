# Engineering Worker Advisory Read-Acknowledgement Test

Procedure ID: `engineering_worker_advisory_read_ack_test`
Procedure Version: 1
Owner: Engineering HQ
Status: Active bounded pilot

## Purpose

Prove the simple GitHub-first communication path:

1. the dashboard discovers one new Engineering advisory through the Advisory Index;
2. the dashboard wakes `engineering_worker` once;
3. the Worker reads the exact advisory revision;
4. the Worker adds one exact acknowledgement block to the same authoritative advisory file;
5. the Worker reports the same confirmation in its own chat.

This procedure tests communication flow only. It does not test substantive engineering work, advisory closure, HQ verification receipts, Rob validation, Chief of Staff delivery, or automatic lifecycle changes.

## Authorized Input

- Advisory: `ADV-20260723-050`
- Revision: 1
- Run ID: `RUN-ADV-20260723-050-R1`
- Authoritative advisory file: `projects/engineering/advisories/ADV-20260723-050.md`
- Exact confirmation marker: `WORKER_READ_CONFIRMATION=ADV-20260723-050`

## Authorized Reads

Read the canonical Worker boot chain, Engineering identity and Worker profile, this procedure, the Advisory Index routing line for `ADV-20260723-050`, and the exact authoritative advisory file.

Do not read unrelated Engineering advisories, notebooks, status, open loops, code, tests, runtime data, or another department's files.

## Authorized Write

The only durable write authorized is one localized update to:

`projects/engineering/advisories/ADV-20260723-050.md`

Append exactly one block:

```markdown
#### Worker Read Acknowledgement

- Read Confirmation: `WORKER_READ_CONFIRMATION=ADV-20260723-050`
- Worker ID: `engineering_worker`
- Run ID: `RUN-ADV-20260723-050-R1`
- Advisory Revision Read: 1
- Status: READ
- Additional Work Performed: none
```

Fetch the current advisory first, use its current blob SHA as the concurrency guard, preserve every unrelated byte, and read the committed advisory back after the write.

Do not change the advisory lifecycle, priority, revision, owner, requested action, completion condition, review condition, closure authority, Advisory Index entry, or any other file.

## Chat Response

After the committed advisory update is read back successfully, report briefly in the Engineering Worker chat that the test advisory was read and acknowledged. Include this exact line once:

`WORKER_READ_CONFIRMATION=ADV-20260723-050`

Return exactly one controlled outcome:

- `IMPLEMENT` when the exact advisory was read, the acknowledgement block was committed and read back, and the chat confirmation was rendered;
- `REPORT_AND_HOLD` when the exact advisory, current SHA, localized edit, commit, or read-back cannot be completed safely;
- `ELEVATE_FOR_APPROVAL` only when broader authority or a new Rob decision is genuinely required.

## Prohibitions

Do not close or otherwise advance the advisory. Do not modify the Advisory Index. Do not create a result artifact, HQ-review receipt, Rob-validation receipt, task, schedule, open loop, or duplicate advisory. Do not run code or tests. Do not use desktop automation or any connector other than exact GitHub reads and the single authorized advisory update. Do not perform substantive engineering work.

## Completion Condition

The test is complete when the authoritative advisory contains exactly one Worker Read Acknowledgement block with the exact marker and the Engineering Worker chat contains the same marker once. Engineering HQ or Rob may then close the advisory separately.
