# PEND-ENG-20260704-014 — Authoritative home exceptions and Finance-owned Drive files

Date captured: 2026-07-04
Status: Pending
Origin: Chief Engineering Penny / Life OS architecture discussion
Tags: connector reliability, data architecture, document architecture, Google Drive, Google Sheets, GitHub, Finance, source of truth, authoritative home

## Core idea

The emerging Life OS architecture should not become `GitHub for everything` as a rigid rule.

The better principle is:

> Every piece of information should have one authoritative home, and that home should be the system best suited to owning it.

For most Life OS operational documentation, procedures, logs, advisory records, architecture notes, source documents, and structured data, GitHub is likely the best authoritative home.

However, some records naturally belong in Google Drive or another external system as their authoritative home.

## Finance-owned Drive exception

A personal checkbook or similar Finance-owned spreadsheet is a good example of a legitimate Drive-native authoritative file.

Reasons:

- It is primarily human-edited.
- It benefits from spreadsheet formulas, formatting, and visual inspection.
- It is not updated at high connector-write frequency.
- It belongs to the sole domain of Finance.
- It is unlikely to be regenerated from another GitHub source file.
- It may be better represented as a native spreadsheet than as a text file plus generated artifact.

In this case, Google Sheets can be the authoritative home rather than merely a presentation artifact.

## Refined architecture principle

GitHub should be the default operational source for many Life OS artifacts, but not the mandatory source for all artifacts.

Preferred framing:

> Choose the natural authoritative home first. Then make every other copy clearly secondary.

Related phrasing:

> GitHub-first for operational source files, not GitHub-only for all records.

> Drive is usually a publication layer, but it can be authoritative for native office artifacts that are human-edited, low-frequency, and domain-owned.

## Source-of-truth ownership by system

Candidate ownership map:

- GitHub: durable engineering knowledge, Markdown documentation, structured operational data, logs, procedures, architecture, source artifacts.
- Google Drive: native office documents and spreadsheets when they are themselves the authoritative working document.
- Google Calendar: timed commitments and scheduled events.
- Todoist: actionable tasks.
- Gmail: correspondence and communication evidence.
- Life Logistics HQ: coordination layer that knows where the authoritative home is, rather than forcing all truth into one storage system.

## Engineering implications

Reliable Connector Execution Layer should not blindly route all updates to GitHub or all tabular data to Drive.

It should evaluate:

1. Is this record primarily machine-managed or human-managed?
2. Is it updated frequently or infrequently?
3. Does it need Git history, diffs, rollback, and modular review?
4. Does it need native spreadsheet formulas, formatting, charts, or human visual editing?
5. Which department owns it?
6. Is it a source artifact, an operational record, a presentation artifact, or a native working document?

## Current recommendation

Keep this alongside:

- `PEND-ENG-20260704-012` for GitHub text state and Drive/Sheets export layer.
- `PEND-ENG-20260704-013` for GitHub canonical source and Drive publication artifacts.

Together, the three notes should mature into a formal Life OS data/document ownership standard.

Draft standard direction:

> GitHub is the default source repository for operational state and source artifacts. Drive is the default publication repository for human-readable artifacts. Exceptions are allowed when another system is the natural authoritative home, such as Finance-owned native spreadsheets in Drive.
