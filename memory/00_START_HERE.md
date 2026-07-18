# Start Here

Updated: 2026-07-18
Project: Penny Long-Term Memory / Life OS
Purpose: Orientation file for future Penny sessions using GitHub as the durable memory layer.

## Core Instruction

This repository is the preferred durable memory map for Penny's personal-assistant work with Rob.

Use GitHub for:

- long-term memory maps;
- session handoffs;
- boot files;
- operating rules and contracts;
- active project maps;
- committed open loops;
- worker contracts and canonical resource pointers;
- strategy and implementation workflow files;
- auditable state changes.

Use Google Drive for:

- the human-facing Life OS Chief's Manual;
- working documents;
- Google Sheets and operational trackers;
- notes that need human-friendly Google Docs editing;
- PDFs and generated artifacts;
- detailed project records.

## Boot Authority

`memory/STARTUP_BOOT.md` is the single canonical department, Hub, project, and worker boot sequence.

ChatGPT Project Instructions are Layer Zero. Their canonical deployment source is:

- `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`

The official authority and Hub contract is:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`

This file is orientation only. It should not define a separate boot order or instruct a model already following `STARTUP_BOOT.md` to restart the sequence.

If this file is opened directly in a fresh chat, read `memory/STARTUP_BOOT.md` next and follow its routing rules.

If this file is being read as step 4 from `memory/STARTUP_BOOT.md`, continue to the next file listed there.

## Eight-Room Model

LifeOS uses eight top-level rooms:

- `LifeOS HQ`, the shared meeting room;
- `Chief of Staff HQ`;
- `Life OS Maintenance HQ`;
- `Engineering HQ`;
- `Finance HQ`;
- `Business HQ`;
- `Office Leaks HQ`;
- `Wellness HQ`.

LifeOS HQ is not a department and does not own an independent backlog.

Chief of Staff HQ is Rob's primary point of contact and daily-operations department.

Life OS Maintenance HQ owns the global GitHub operating structure, audits, boot integrity, and reconciliation.

Filesystem paths may retain legacy names until a separate migration is authorized.

## Department / Worker Distinction

Departments and HQs own domains, judgment, strategy, durable state, and routed decisions.

Workers perform narrow, repeatable operations under stable contracts.

Worker root:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`

Workers do not automatically read the full department boot. Use the worker route in `memory/STARTUP_BOOT.md` when Rob names a worker.

## Connector Recovery Rule

If a long-running chat stops invoking connectors reliably, treat it as an environment or session degradation problem.

Do not waste excessive time trying to force a degraded chat to recover.

Recommended sequence:

1. Explicitly reference the intended connector in the conversation, such as `@Google Drive`, `@Gmail`, `@Google Calendar`, or `@Todoist`.
2. Try a tiny harmless read.
3. If the connector responds, continue with small scoped operations.
4. If it fails or behaves inconsistently, start a fresh Penny chat, warm up the needed connector if useful, boot from this repository, and continue.

## Drive Editing Field Lessons

When working with Google Drive records, prefer small incremental edits over large complex batch edits.

For Sheets or structured records, verify the row or target range after each edit.

If an update appears blocked because the content may be sensitive or triggers safety checks, simplify the payload and use abstract notes instead of repeatedly retrying the same detailed text.

These are operational field notes from Life OS use, not claims about internal connector implementation.

## Source-of-Truth Transition

Previous durable memory lived primarily in Google Drive.

As of 2026-07-02, GitHub is the durable memory map and Drive is the working-records cabinet.

The Drive Chief's Manual explains the human operating doctrine. GitHub translates that doctrine into enforceable operating rules, boot files, contracts, and durable abstract state.

The Life OS Pointer Registry in Drive resolves references between GitHub and detailed operational records.