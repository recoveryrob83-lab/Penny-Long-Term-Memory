# Penny Raw Capture Worker Session Handoff

Updated: 2026-07-09

## Metadata

- Worker name: Penny Raw Capture Worker
- Status: Pilot / Active
- Primary user: Rob
- Downstream owner: Main Assistant Penny
- Engineering owner for architecture: Chief Engineering Penny
- System owner for cross-project memory: Life Logistics HQ

## Canonical Resource Pointer

Canonical Google Sheet title:

`Life OS Raw Capture Inbox`

Canonical Google Sheet ID:

`1CyhRsh-mByIfWwgiRSUDDD9rkHmvUj_y54iK8a327to`

Canonical Google Sheet URL:

`https://docs.google.com/spreadsheets/d/1CyhRsh-mByIfWwgiRSUDDD9rkHmvUj_y54iK8a327to`

Verification date:

2026-07-09

Verification result:

- The Sheet was found by exact title and ID.
- The Sheet contained populated capture rows.
- The required schema was present.
- Five rows with `Processed = No` were observed during verification.

Do not create, replace, rename, restructure, or duplicate the canonical Sheet without Rob's explicit authorization.

Do not delete any duplicate Sheet without Rob's explicit authorization.

If the canonical pointer stops resolving, report the failure to Rob and Life Logistics HQ rather than creating a replacement.

## Current Schema

- `Captured At`
- `Raw Note`
- `Processed`

The observed Sheet export/search surface also displayed a leading row-number/index field. The worker should treat the three named columns above as the canonical data schema and should not modify the Sheet structure.

## Timezone

Required capture timezone:

`America/Chicago`

Known discrepancy:

Engineering observed during testing that the spreadsheet metadata reported `America/Los_Angeles`.

Life Logistics has not changed the Sheet configuration.

Until Rob explicitly authorizes a configuration change, the worker must write `Captured At` values explicitly in `America/Chicago` local time.

## Known Connector Behavior

These are field observations, not claims about platform internals:

- Explicitly naming `@Google Drive` or otherwise invoking the connector improves the likelihood that a connector operation is actually attempted.
- A previous worker interaction falsely claimed successful capture when no connector call occurred.
- Tool invocation and post-write verification are therefore mandatory.
- Google Drive filename/title alone is not a sufficient durable identifier when duplicate files exist.
- Use the canonical Sheet ID or exact URL in this handoff.

## Current Operational State

The capture worker is ready for pilot use.

Main Assistant Penny remains responsible for later processing of rows where `Processed = No`.

The capture worker does not classify, prioritize, route, schedule, research, answer embedded questions, create tasks, or update project state during intake.

## Boot Order

1. `workers/WORKER_STANDARD.md`
2. `workers/penny-raw-capture/WORKER_BOOT.md`
3. This file when canonical pointer or current connector notes are needed

Do not load the full Life OS global department boot unless Rob explicitly requests broader context for troubleshooting.

## Escalation

- Rob: ambiguity, permissions, duplicate-resource decisions, authorization to change schema or Sheet settings.
- Main Assistant Penny: processing workflow and downstream inbox review.
- Life Logistics HQ: canonical pointer, worker routing, or durable-memory synchronization.
- Chief Engineering Penny: connector reliability, schema, verification, or worker architecture.
