# Projects

Purpose: Durable project folders for Penny's Life OS work with Rob.

Each active project should eventually have its own folder with a `README.md`, `status.md`, `open_loops.md`, `SESSION_HANDOFF.md`, and any project-specific notes or research.

## Current Project Folders

- `main-assistant/`
- `job-search/`
- `caregiver-income/`
- `cleanup/`
- `finance-benefits/`
- `recovery-logistics/`
- `life-os-infrastructure/`
- `health-medical/`
- `housing-logistics/`
- `wellness/`

## Project Session Handoffs

Each project folder now has a `SESSION_HANDOFF.md` file.

Use these files as project-specific continuity anchors when a specialized Penny chat needs to be replaced, restarted, or rehydrated after connector problems.

When Rob starts a new specialist chat, the initiation message should name the project, such as:

- Main Assistant.
- Caregiver Project HQ.
- Job Search HQ.
- Cleanup Project HQ.
- Finance Benefits HQ.
- Recovery Logistics.
- Life OS Infrastructure.
- Health Medical HQ.
- Housing Logistics HQ.
- Wellness HQ.

The new Penny should read the global boot files first, then read the matching project `SESSION_HANDOFF.md`.

## Standard Session Handoff Structure

Project handoffs should use this structure when possible:

1. Metadata
2. Boot Instructions
3. Overall Project Context / Current Project Status
4. Objectives
5. Completed Work
6. Active Open Loops
7. Key Contacts / Organizations
8. Working Documents / Links
9. Source Systems
10. Connector / Safety Notes
11. Privacy Guardrails
12. Decision Log
13. Immediate Next Actions
14. Notes for Next Penny

Use this structure as a guide, not a prison. Add project-specific sections when they materially help the next Penny.

## RPR Procedure for Project Files

RPR means Rob -> Penny -> Rob.

Use user-mediated file transfer for any structured file that is likely to trigger connector safety or requires reliable editing.

Prefer RPR over connector writes whenever reliability is more important than automation.

Use connectors for discovery, lookup, scheduling, communication, and metadata, but not as the sole path for maintaining critical structured records.

Good RPR candidates:

- CSV/XLSX trackers.
- SQLite files.
- JSON exports.
- Profile/reference files.
- Sensitive-adjacent structured records.
- Critical project records where connector inconsistency would be costly.

## Project File Pattern

Recommended structure:

```text
projects/<project-name>/
  README.md
  status.md
  open_loops.md
  SESSION_HANDOFF.md
  notes.md
  sources.md
```

Use this area for durable project state. Use Drive for working docs, Sheets, PDFs, and artifacts.

## Privacy Rule

Project handoffs in GitHub should be operational and abstract.

Do not store secrets, credentials, private identifiers, sensitive medical records, banking details, policy numbers, government IDs, private family notes, or unnecessary personal data in GitHub.

When in doubt, store intent and routing, not the underlying secret.
