# Projects

Purpose: Durable project folders for Penny's Life OS work with Rob.

Each active project should eventually have its own folder with a README, status, open loops, session handoff, department identity, and any project-specific notes that are safe to keep in GitHub.

## Current Project Folders

- `life-logistics-hq/`
- `main-assistant/`
- `job-search/`
- `caregiver-income/`
- `cleanup/`
- `finance-benefits/` — Chief of Finance Penny / CFO Penny
- `wellness/` — Chief Wellness HQ / Chief Wellness Penny
- `recovery-logistics/`
- `philosophy/`
- `life-os-infrastructure/`
- `health-medical/`
- `housing-logistics/`

## Project Session Handoffs

Each project folder should use its `SESSION_HANDOFF.md` as the project-specific continuity anchor.

When Rob starts a new specialist or coordination chat, the initiation message should name the project, such as:

- Life Logistics HQ.
- Main Assistant.
- Caregiver Project HQ.
- Job Search HQ.
- Cleanup Project HQ.
- Chief of Finance Penny / Finance Benefits HQ.
- Chief Wellness HQ / Wellness HQ.
- Recovery Logistics.
- Philosophy HQ.
- Life OS Infrastructure.
- Health Medical HQ.
- Housing Logistics HQ.

The new Penny should read the global boot files first, then read the matching project `SESSION_HANDOFF.md` and `DEPARTMENT_IDENTITY.md` if present.

## Department Identity Files

Department identity files are concise role cards.

They define:

- Department name.
- Mission.
- Primary responsibilities.
- What is not the department's job.
- Reports and coordination.
- Advisory role.
- Authoritative memory.
- First response after sync.

Use `SESSION_HANDOFF.md` for full project continuity.

## RPR Procedure for Project Files

RPR means Rob -> Penny -> Rob.

Use user-mediated file transfer when reliable structured-file handling matters more than connector automation.

Use connectors for discovery, lookup, scheduling, communication, and metadata, but not as the only maintenance path for critical records.

## Project File Pattern

Recommended structure:

```text
projects/<project-name>/
  README.md
  status.md
  open_loops.md
  SESSION_HANDOFF.md
  DEPARTMENT_IDENTITY.md
  notes.md
  sources.md
```

Use this area for durable project state. Use Drive for working docs, Sheets, PDFs, and artifacts.

## Privacy Rule

Project handoffs in GitHub should be operational and abstract.

When in doubt, store intent and routing, not detailed private records.