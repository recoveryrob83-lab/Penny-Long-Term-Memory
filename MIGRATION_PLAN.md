# Migration Plan

Updated: 2026-07-11
Status: Core migration complete; maintenance mode

## Goal

Move durable Life OS memory into GitHub while keeping Google Drive for working documents, spreadsheets, and detailed operational records.

## Current Architecture

GitHub stores:
- project map
- durable state
- boot instructions
- handoffs
- operating rules
- abstract references
- worker contracts
- advisory routing state

Drive stores:
- working documents
- spreadsheets
- operational records
- detailed notes
- generated artifacts

The Life OS Pointer Registry in Drive is the directory service between GitHub and detailed working records.

## Migration State

The core durable-memory migration is complete. Current work is maintenance and synchronization:

- Keep GitHub abstract and internally consistent.
- Keep detailed working records in Drive.
- Update handoffs and open loops after meaningful state changes.
- Assign registry references to active projects when useful.
- Preserve historical project folders unless Rob authorizes archival cleanup.

## Project Structure

Current project routing is defined by:
- `memory/STARTUP_BOOT.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `projects/README.md`

The current housing scaffold is `projects/housing-logistics/`.

## Historical Preservation

This repository is a normalized operational mirror, not a byte-for-byte import of all historical Drive material. Historical detail may be preserved in `archive/` only when discoverability justifies it.

## Rules

Prefer one authoritative home per record.

Use the Advisory Index and source department boards for formal advisories.

Do not use GitHub Issues for Life OS advisory or open-loop routing.

Prefer small, verified edits over broad rewrites.
