# Start Here

Updated: 2026-07-02
Project: Penny Long-Term Memory / Life OS
Purpose: Fast boot file for future Penny sessions using GitHub as the durable memory layer.

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

## Startup Procedure

Preferred new-chat workflow:

1. Rob may ask Penny to open Google Drive first as a connector warm-up.
2. Then open this repository: `recoveryrob83-lab/Penny-Long-Term-Memory`.
3. Read `memory/STARTUP_BOOT.md`.
4. Follow the boot order listed there.

## Boot Sequence Summary

Read in this order:

1. `memory/STARTUP_BOOT.md`
2. `memory/01_SESSION_HANDOFF.md`
3. `memory/02_BOOT_LOG.md`
4. `memory/03_OPERATIONAL_RULES.md`
5. `memory/04_ACTIVE_PROJECTS.md`
6. `memory/05_OPEN_LOOPS.md`
7. `MIGRATION_PLAN.md`
8. `MIRROR_STATUS.md`

Then read project files only as needed.

## Connector Recovery Rule

If a long-running chat stops invoking connectors reliably, treat it as an environment/session degradation problem.

Start a fresh Penny chat, warm up Drive if useful, boot from this repository, and continue.

Do not waste excessive time trying to force a degraded chat to recover.

## Source-of-Truth Transition

Previous durable memory lived primarily in Google Drive.

As of 2026-07-02, GitHub is the durable memory map and Drive is the working records cabinet.

The Life OS Pointer Registry in Drive resolves references between GitHub and detailed operational records.
