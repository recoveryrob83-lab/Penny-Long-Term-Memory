# Projects

Updated: 2026-07-18
Purpose: Durable project folders for Penny's Life OS work with Rob.

Each active department or project should maintain a README, status, open loops, session handoff, department identity, and any project-specific notes that are safe to keep in GitHub.

LifeOS HQ is the shared meeting room and does not maintain an independent department project folder or backlog.

## Canonical HQ Naming

Top-level HQ display names follow:

- `memory/HQ_NAMING_STANDARD.md`

Authority and meeting-room behavior follow:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`

Project folder names remain stable filesystem paths and do not need to match display names exactly.

## Current Project Folders

- `life-logistics-hq/` - Life OS Maintenance HQ; global GitHub maintenance, boot integrity, governance, audits, shared infrastructure, migrations, and reconciliation
- `main-assistant/` - Chief of Staff HQ; Rob's primary point of contact, personal assistant, daily operations, Hub chairing, routing, reports, and follow-through
- `job-search/` - dormant / consolidated work-search history
- `caregiver-income/` - dormant / consolidated support-pathway history
- `cleanup/` - Site Cleanup project
- `finance-benefits/` - Finance HQ
- `business-development/` - Business HQ
- `office-leaks-consulting/` - Office Leaks HQ; active business-unit department under Business HQ
- `engineering/` - Engineering HQ
- `wellness/` - Wellness HQ
- `recovery-logistics/` - dormant Recovery Logistics history
- `philosophy/` - dormant Philosophy HQ history
- `life-os-infrastructure/` - shared Life OS infrastructure and policies
- `health-medical/` - Health Medical HQ
- `housing-logistics/` - Housing Logistics HQ scaffold

Archived historical project context lives outside the active project tree:

- `archive/projects/virtual-assistant-business/` - historical predecessor and redirect context for Office Leaks HQ; active Office Leaks state lives in `projects/office-leaks-consulting/`

## Eight Top-Level Rooms

When Rob starts or boots a top-level LifeOS room, use the canonical display name:

1. `LifeOS HQ` - shared meeting room
2. `Chief of Staff HQ`
3. `Life OS Maintenance HQ`
4. `Engineering HQ`
5. `Finance HQ`
6. `Business HQ`
7. `Office Leaks HQ`
8. `Wellness HQ`

LifeOS HQ is not a department. Chief of Staff HQ chairs it. Real actions transfer to the owning department and authoritative destination.

Other project names may use their established descriptive labels, such as Site Cleanup, Recovery Logistics, Philosophy HQ, Life OS Infrastructure, Health Medical HQ, or Housing Logistics HQ.

## Stable Path Mapping

The official role names changed without renaming project folders:

- Chief of Staff HQ uses `projects/main-assistant/`.
- Life OS Maintenance HQ uses `projects/life-logistics-hq/`.

Legacy path names are implementation details. They do not override the official role names.

Department-local identity, handoff, status, open-loop, notebook, and procedure files may retain legacy names until the owning department completes an authorized Phase Two alignment.

## Project Session Handoffs

Each department or project folder uses `SESSION_HANDOFF.md` as its project-specific continuity anchor.

LifeOS HQ uses:

- `coordination/LIFEOS_HUB_OPERATING_CONTRACT.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/04_ACTIVE_PROJECTS.md`
- `memory/05_OPEN_LOOPS.md`

A newly booted department should read the universal kernel first, then the matching project `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, and `open_loops.md` when they exist or are maintained.

## Department Identity Files

Department identity files are concise role cards.

They define:

- department name;
- mission;
- primary responsibilities;
- what is not the department's job;
- reports and coordination;
- advisory role;
- authoritative memory;
- first response after sync.

Use `SESSION_HANDOFF.md` for full project continuity.

## Reporting Structure

- Rob is final authority.
- Chief of Staff HQ is the normal daily point of contact and receives department reports.
- Life OS Maintenance HQ owns global GitHub integrity and governance enforcement.
- Engineering HQ owns technical architecture and implementation mechanisms.
- Specialist departments own judgment and durable state within their domains.
- Reporting through Chief of Staff does not transfer department ownership.

## RPR Procedure for Project Files

RPR means Rob → Penny → Rob.

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