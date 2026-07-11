# Penny Inventory Worker Session Handoff

Updated: 2026-07-10

## Metadata

- Worker name: Penny Inventory Worker
- Status: Pilot / Active
- Primary user: Rob
- Downstream owners: Main Assistant Penny and later sale/listing workflows
- Engineering owner for architecture: Chief Engineering Penny
- Cross-project owner: Life Logistics HQ

## Canonical Google Sheet

Title:

`For Sale Inventory`

Spreadsheet ID:

`1q3YCwIwKcV0fWAOvMlaolXAXuQ7ommVHEL2IGqt5jIg`

Spreadsheet URL:

`https://docs.google.com/spreadsheets/d/1q3YCwIwKcV0fWAOvMlaolXAXuQ7ommVHEL2IGqt5jIg/edit`

Tab:

`Inventory`

Time zone:

`America/Chicago`

Verification date:

2026-07-10

Verification result:

- Spreadsheet ID resolved successfully.
- Title matched `For Sale Inventory`.
- Tab `Inventory` exists.
- Spreadsheet time zone is `America/Chicago`.
- The expected 13-column schema is present.
- Two prototype inventory rows were present during verification.

Do not create a replacement Sheet if this pointer fails. Report the blocker to Rob and Life Logistics HQ.

## Canonical Columns

1. `Timestamp`
2. `Batch ID`
3. `Image Reference`
4. `Category`
5. `Item`
6. `Quantity`
7. `Condition`
8. `Confidence`
9. `Notes`
10. `Processed`
11. `Listing Group`
12. `Asking Price`
13. `Status`

## Google Drive Folder Structure

Expected operational folders:

- `For Sale Items/Images/`
- `For Sale Items/Inventory/`
- `For Sale Items/Listings/`
- `For Sale Items/Archive/`

The worker does not create, rename, move, or restructure these folders unless Rob explicitly authorizes it.

The canonical Sheet pointer is sufficient for normal inventory capture.

## Verified Prototype Pattern

Engineering prototype testing and Life Logistics verification support this pattern:

- Direct chat uploads can be analyzed visually.
- Drive-hosted images should not be assumed to be reliable direct vision input through the Drive connector alone.
- Stable worker-generated references such as `IMG-0001` should be used instead of temporary upload tokens.
- One row per item is the canonical output.
- One Sheets append operation per item is preferred when practical.
- A final bounded Sheet read should verify the completed batch.

## Observed Prototype Rows

The verification read found two existing test rows under batch `TEST-001`.

These rows demonstrate the schema and should not be overwritten or deleted by the worker.

## Current Operational State

The worker package is ready for pilot use in a dedicated regular chat.

The worker captures inventory only.

Future pricing, bundling, listing copy, and publication remain downstream work.

## Boot Order

1. `workers/WORKER_STANDARD.md`
2. `workers/penny-inventory/WORKER_BOOT.md`
3. This file when canonical pointers, schema, or connector observations are needed

Do not load the full Life OS global boot unless Rob explicitly requests broader troubleshooting context.

## Escalation

- Rob: ambiguity over whether an object is for sale, item identity, or authorization to change resources.
- Main Assistant Penny: downstream processing, grouping, and sale workflow coordination.
- Life Logistics HQ: worker routing and canonical-resource pointer issues.
- Chief Engineering Penny: connector reliability, image-reference strategy, schema, or worker architecture issues.
- Chief of Finance Penny: pricing decisions when Rob requests financial guidance.
