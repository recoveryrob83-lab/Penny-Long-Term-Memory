# Migration Plan

Updated: 2026-07-02

## Goal

Move durable Life OS memory into GitHub while keeping Google Drive for working documents, spreadsheets, and detailed operational records.

## Current Layout Built

- `memory/`
- `projects/`
- `archive/`
- `templates/`

## Registry Architecture

Life OS now uses a pointer model.

GitHub stores:
- project map
- durable state
- boot instructions
- handoffs
- abstract references

Drive stores:
- working documents
- spreadsheets
- operational records
- detailed notes

The Life OS Pointer Registry in Drive is the directory service between GitHub and source-system records.

## Project Folders Started

- `projects/job-search/`
- `projects/caregiver-income/`
- `projects/cleanup/`
- `projects/finance-benefits/`
- `projects/recovery-logistics/`
- `projects/life-os-infrastructure/`
- `projects/home-base-logistics/`
- `projects/stability-routines/`
- `projects/project-slot-07/`

## Deprecated / Avoided Labels

Some earlier project names were too direct for durable GitHub storage.

Use neutral names or project slots when a project touches sensitive life domains.

## Next Migration Order

1. Replace detailed project facts in GitHub with registry references.
2. Assign registry IDs for active projects that do not have them yet.
3. Keep detailed working notes in Drive.
4. Update handoff files after each meaningful batch.

## Rule

Migrate current state first.

Preserve history later only if useful.

Prefer references over duplicated records.
