# Start Here

Updated: 2026-07-06
Project: Penny Long-Term Memory / Life OS
Purpose: Orientation file for future Penny sessions using GitHub as the durable memory layer.

## Core Instruction

This repository is the preferred durable memory map for Penny's personal-assistant work with Rob.

Use GitHub for:
- Long-term memory map.
- Session handoffs.
- Boot files.
- Operating rules.
- Active project maps.
- Open loops.
- Strategy and implementation workflow files.
- Auditable state changes.

Use Google Drive for:
- Working documents.
- Google Sheets and operational trackers.
- Notes that need human-friendly Google Docs editing.
- PDFs and generated artifacts.
- Detailed project records.

## Boot Authority

`memory/STARTUP_BOOT.md` is the single canonical boot sequence.

This file is orientation only. It should not define a separate boot order or instruct a model already following `STARTUP_BOOT.md` to restart the boot sequence.

If this file is opened directly in a fresh chat, read `memory/STARTUP_BOOT.md` next and follow that file's boot order.

If this file is being read as step 2 from `memory/STARTUP_BOOT.md`, continue to the next file listed there.

## Connector Recovery Rule

If a long-running chat stops invoking connectors reliably, treat it as an environment/session degradation problem.

Do not waste excessive time trying to force a degraded chat to recover.

Recommended sequence:

1. Explicitly reference the intended connector in the conversation, such as `@Google Drive`, `@Gmail`, `@Google Calendar`, or `@Todoist`.
2. Try a tiny harmless read.
3. If the connector responds, continue with small scoped operations.
4. If it fails or behaves inconsistently, start a fresh Penny chat, warm up Drive if useful, boot from this repository, and continue.

## Drive Editing Field Lessons

When working with Google Drive records, prefer small incremental edits over large complex batch edits.

For Sheets or structured records, verify the row or target range after each edit.

If an update appears blocked because the content may be sensitive or triggers safety checks, simplify the payload and use abstract notes instead of repeatedly retrying the same detailed text.

These are operational field notes from Life OS use, not claims about internal connector implementation.

## Source-of-Truth Transition

Previous durable memory lived primarily in Google Drive.

As of 2026-07-02, GitHub is the durable memory map and Drive is the working records cabinet.

The Life OS Pointer Registry in Drive resolves references between GitHub and detailed operational records.