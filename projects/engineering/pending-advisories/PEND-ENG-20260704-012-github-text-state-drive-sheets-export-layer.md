# PEND-ENG-20260704-012 — GitHub text state and Drive/Sheets export layer

Date captured: 2026-07-04
Status: Pending
Origin: Chief Engineering Penny / Connector Reliability Test Lab observations
Tags: connector reliability, data architecture, Google Drive, Google Sheets, GitHub, source of truth, export layer

## Core idea

For database-like files, especially tables and structured records, Life OS should prefer GitHub-native text files as the operational source of truth instead of treating Google Sheets as the live working database.

Google Drive and Google Sheets should be treated primarily as forward-facing human-readable presentation/export layers.

## Proposed pattern

Use GitHub for operational state:

- CSV for simple tables.
- TSV when comma handling becomes annoying.
- JSONL for append-oriented records, events, logs, and operation ledgers.
- YAML or TOML for structured configuration.
- Markdown tables only when human readability matters more than machine parsing.

Generate or copy to Google Drive/Sheets only when a human-facing sheet is needed.

Conceptual flow:

```text
GitHub data file -> script/export process -> Google Sheet / Drive presentation copy
```

## Rationale

Current connector observations suggest different connectors have different safety and reliability profiles.

GitHub appears more tolerant of repeated small text writes, fetches, and multi-HQ activity. Its remaining practical limitation appears more related to batch size and full-file rewrite complexity.

Google Drive appears more restrictive around repeated write/create operations in a short period, especially for file creation and Sheet writes. Read-only Drive operations may remain available after a write/create safety block, but write/create status can become uncertain.

This suggests Life OS should minimize direct Google Drive writes during normal operation and reserve Drive/Sheets writes for export, review, sharing, or presentation.

## Expected benefits

- Fewer Google Drive write/create operations.
- Lower exposure to Drive-specific safety blocks.
- Better Git history and diff visibility.
- Easier rollback.
- Easier validation and automated testing.
- Cleaner operation ledger design.
- More predictable source-of-truth management.
- Reduced risk of corrupting human-facing spreadsheets.

## Engineering implications

Reliable Connector Execution Layer should treat connectors as having different write-risk profiles.

Candidate principle:

> Prefer GitHub/text-file operational state. Use Drive/Sheets as generated presentation output.

Possible implementation directions:

1. Store operational tables as GitHub text files.
2. Use small modular files for append-heavy records where possible.
3. Build export scripts/processes that can convert source files into Sheets when needed.
4. Keep human-facing Sheets disposable/regenerable where possible.
5. Avoid treating Google Sheets as the only copy of important operational data.

## Open questions

- Which Life OS data types should be represented as CSV, TSV, JSONL, YAML, TOML, or Markdown?
- Should each department have a `data/` directory for machine-readable records?
- What export process should be used for Drive/Sheets presentation copies?
- How often should presentation exports occur?
- Should exports be manual, demand-driven, scheduled, or event-driven?
- How should generated Sheets be marked as generated to prevent accidental source-of-truth confusion?

## Current recommendation

Keep this as a pending Engineering advisory until more connector reliability experiments are complete.

Do not route globally yet unless Rob asks to promote it or unless Engineering is ready to propose a formal Life OS data architecture standard.
