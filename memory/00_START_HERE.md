# Start Here

Updated: 2026-07-19
Project: Penny Long-Term Memory / LifeOS
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
- Worker contracts, department-owned Worker profiles, and canonical resource pointers;
- strategy and implementation workflow files;
- auditable state changes.

Use Google Drive for:

- the human-facing LifeOS Chief's Manual;
- working documents;
- Google Sheets and operational trackers;
- notes that need human-friendly Google Docs editing;
- PDFs and generated artifacts;
- detailed project records.

## Boot Authority

`memory/STARTUP_BOOT.md` is the single canonical Department HQ, Hub, project, and Worker boot sequence.

ChatGPT Project Instructions are Layer Zero. Their canonical deployment source is:

- `coordination/LIFEOS_PROJECT_INSTRUCTIONS.md`

The official authority and Hub contract is:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`

This file is orientation only. It should not define a separate boot order or instruct a model already following `STARTUP_BOOT.md` to restart the sequence.

If this file is opened directly in a fresh chat, read `memory/STARTUP_BOOT.md` next and follow its routing rules.

If this file is being read as step 4 from `memory/STARTUP_BOOT.md`, continue to the next file listed there.

## Eight-Room Model

LifeOS uses eight top-level rooms:

- `LifeOS_HQ`, the shared meeting room;
- `Chief_of_Staff_HQ`;
- `Maintenance_HQ`;
- `Engineering_HQ`;
- `Finance_HQ`;
- `Business_HQ`;
- `Office_Leaks_HQ`;
- `Wellness_HQ`.

`LifeOS_HQ` is not a department and does not own an independent backlog.

`Chief_of_Staff_HQ` is Rob's primary point of contact and daily-operations department.

`Maintenance_HQ` owns the global GitHub operating structure, audits, boot integrity, and reconciliation.

Filesystem paths may retain legacy names until a separate migration is authorized.

## Department / Worker Distinction

Department HQs own domains, judgment, strategy, durable state, approvals, Worker authority, and routed decisions.

Workers perform narrow, already-authorized operations under one owning department and the canonical shared contracts.

Canonical Worker rules live in:

- `coordination/LIFEOS_EXECUTION_AND_COMMUNICATION_PROTOCOL.md`
- `coordination/WORKER_EXECUTION_CONTRACT.md`

New department-owned Worker profiles live at:

- `projects/<department>/workers/<profile>.md`

Workers follow the Worker branch in `memory/STARTUP_BOOT.md`. They do not automatically read the full department boot, history, notebooks, backlog, or unrelated open loops.

The root files below are compatibility surfaces for the two grandfathered pilot packages only:

- `workers/README.md`
- `workers/WORKER_STANDARD.md`

Do not create new top-level Worker packages by analogy. Deployment state, route availability, pause state, and current chat resolution belong to the Engineering-owned routing registry and runtime rather than the department-owned profile.

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

These are operational field notes from LifeOS use, not claims about internal connector implementation.

## Source-of-Truth Transition

Previous durable memory lived primarily in Google Drive.

As of 2026-07-02, GitHub is the durable memory map and Drive is the working-records cabinet.

The Drive Chief's Manual explains the human operating doctrine. GitHub translates that doctrine into enforceable operating rules, boot files, contracts, and durable abstract state.

The external Drive artifact titled `Life OS Pointer Registry` retains its existing title and resolves references between GitHub and detailed operational records.