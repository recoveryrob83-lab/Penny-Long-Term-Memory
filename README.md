# Penny Long-Term Memory

Private repository for Rob's personal-assistant / Life OS memory.

This repository is being built as the GitHub-backed durable memory layer for Penny. Google Drive remains useful for working documents, spreadsheets, checkbooks, job-search files, notes, and operational artifacts. GitHub is being promoted as the preferred durable source for auditable Markdown memory because it provides commit history, diffs, rollback, and stable text files.

## Current Boot Order

Future Penny sessions should start here:

1. Read `memory/00_START_HERE.md`.
2. Read `memory/01_SESSION_HANDOFF.md`.
3. Read `memory/02_BOOT_LOG.md`.
4. Read `memory/03_OPERATIONAL_RULES.md`.
5. Read project files as needed:
   - `memory/04_ACTIVE_PROJECTS.md`
   - `memory/05_OPEN_LOOPS.md`
   - `memory/06_WEEKLY_PLAN.md`
   - `memory/07_STRATEGY_BOOT.md`
   - `memory/08_IMPLEMENTATION_PACKET_TEMPLATE.md`
   - `memory/09_APP_INTEGRATIONS_REFERENCE.md`
   - `memory/10_PROFILE_REFERENCE.md`

## Architecture Decision

GitHub should become the canonical long-term memory layer for durable text records. Google Drive remains the operational workspace for Google Docs, Sheets, checkbook tracking, job-search artifacts, meeting notes, and working files.

Connector lesson: if a long-running chat loses reliable connector behavior, do not over-debug. Start a fresh Penny session and boot from the durable memory files.

## Privacy Rule

This is a private repository, but it is still not a vault. Do not store Social Security numbers, passwords, banking credentials, full birthdates, government ID numbers, exact street addresses, or sensitive medical records here.
