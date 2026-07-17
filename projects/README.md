# Projects

Updated: 2026-07-17
Purpose: Durable project folders for Penny's Life OS work with Rob.

Each active department or project should maintain a README, status, open loops, session handoff, department identity, and any project-specific notes that are safe to keep in GitHub.

## Canonical HQ Naming

Top-level HQ display names follow:

- `memory/HQ_NAMING_STANDARD.md`

Project folder names remain stable filesystem paths and do not need to match display names exactly.

## Current Project Folders

- `life-logistics-hq/` — Logistics HQ; GitHub operations, shared infrastructure, audits, and long-horizon coordination
- `main-assistant/` — Main Assistant HQ; daily operations and LifeOS coordination hub
- `job-search/` — dormant / consolidated work-search history
- `caregiver-income/` — dormant / consolidated support-pathway history
- `cleanup/` — Site Cleanup project
- `finance-benefits/` — Finance HQ
- `business-development/` — Business HQ
- `office-leaks-consulting/` — Office Leaks HQ; active business-unit department under Business HQ
- `virtual-assistant-business/` — legacy redirect context; active Office Leaks state lives in `office-leaks-consulting/`
- `engineering/` — Engineering HQ
- `wellness/` — Wellness HQ
- `recovery-logistics/` — dormant Recovery Logistics history
- `philosophy/` — dormant Philosophy HQ history
- `life-os-infrastructure/` — shared Life OS infrastructure and policies
- `health-medical/` — Health Medical HQ
- `housing-logistics/` — Housing Logistics HQ scaffold

## Project Session Handoffs

Each project folder uses `SESSION_HANDOFF.md` as its project-specific continuity anchor.

When Rob starts or boots a top-level HQ chat, use the canonical display name:

- Logistics HQ
- Main Assistant HQ
- Finance HQ
- Business HQ
- Office Leaks HQ
- Engineering HQ
- Wellness HQ
- LifeOS HQ for the central hub when needed

Other project names may use their established descriptive labels, such as Site Cleanup, Recovery Logistics, Philosophy HQ, Life OS Infrastructure, Health Medical HQ, or Housing Logistics HQ.

The new Penny should read the global boot files first, then the matching project `SESSION_HANDOFF.md`, `DEPARTMENT_IDENTITY.md`, `README.md`, `status.md`, and `open_loops.md` when they exist or are maintained.

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
