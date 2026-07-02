# Start Here

Updated: 2026-07-02
Project: Penny Long-Term Memory / Life OS
Purpose: Fast boot file for future Penny sessions using GitHub as the durable memory layer.

## Core Instruction

This repository is the preferred durable memory layer for Penny's personal-assistant work with Rob.

Use GitHub for:
- Long-term memory.
- Session handoffs.
- Boot files.
- Operating rules.
- Active project maps.
- Open loops.
- Strategy and implementation workflow files.
- Auditable state changes.

Use Google Drive for:
- Working documents.
- Google Sheets/checkbook tracking.
- Notes that need human-friendly Google Docs editing.
- PDFs and generated artifacts.
- Job-search working files.
- Meeting notes and operational documents.

## Boot Sequence

When Rob starts a new personal-assistant / Life OS chat:

1. Open this repository: `recoveryrob83-lab/Penny-Long-Term-Memory`.
2. Read `memory/01_SESSION_HANDOFF.md`.
3. Read `memory/02_BOOT_LOG.md`.
4. Read `memory/03_OPERATIONAL_RULES.md`.
5. Read Active Projects and Open Loops when the task requires current state.
6. Use Drive, Gmail, Calendar, Todoist, GitHub, or other connectors only as needed for the task.

## Connector Recovery Rule

If a long-running chat stops invoking connectors reliably, treat it as an environment/session degradation problem. Start a fresh Penny chat, boot from this repository, and continue.

Do not waste excessive time trying to force a degraded chat to recover.

## Source-of-Truth Transition

Previous durable memory lived primarily in Google Drive. As of 2026-07-02, Rob is exploring GitHub as the stronger long-term source of truth because it is auditable, diffable, and more reliable for Markdown text.

This file begins that transition.
