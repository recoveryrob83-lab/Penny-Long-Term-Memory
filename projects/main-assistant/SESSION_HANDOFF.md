# Main Assistant Session Handoff

Updated: 2026-07-02
Project: Main Assistant / Daily Operations
Purpose: Project-specific handoff for new Main Assistant Penny chats.

## Metadata

- Project Owner: Rob
- Primary Chat: Main Assistant
- Current Phase: Active / Daily Operations
- Primary Systems: GitHub, Google Drive, Todoist, Calendar, Gmail, Contacts, RPR/user-mediated files when needed
- Sensitivity Level: Moderate
- GitHub Rule: Keep GitHub abstract. Do not store sensitive personal details, credentials, medical identifiers, financial identifiers, private third-party data, or unnecessary personal information.
- RPR Rule: Use RPR for structured files that need reliable editing or may trigger connector safety.
- Advisory Rule: Check `coordination/ADVISORY_INDEX.md` during morning/nightly reports or when Rob asks for department advisory status.

## Boot Instructions

When Rob opens a new Main Assistant chat:

1. Read the global boot files from `memory/STARTUP_BOOT.md`.
2. Read this project handoff.
3. Read this project's `README.md`, `status.md`, and `open_loops.md` if present.
4. Use Drive/Todoist/Calendar/Gmail/Contacts only as needed for daily assistant work.
5. Route large project work to the appropriate specialist chat instead of absorbing it into Main Assistant.
6. If preparing a morning/nightly report, read `coordination/ADVISORY_INDEX.md` and report open advisories.

## Current Project Status

Main Assistant is Rob's everyday operations assistant.

It is used for tasks that do not clearly belong to a larger project, including one-time tasks, calendar items, contact updates, daily itinerary summaries, quick Gmail/Drive lookups, and general life admin.

## Objectives

- Serve as the default daily assistant chat.
- Handle quick everyday administrative work.
- Keep Rob oriented to the day through itinerary, reminders, appointments, and next actions.
- Create one-time Todoist tasks or Calendar events when requested.
- Add or find contacts when requested.
- Draft or search Gmail when requested.
- Surface open department advisories during morning and nightly reports when relevant.
- Route larger project work to specialist project chats.

## Completed Work

- Created GitHub project folder: `projects/main-assistant/`.
- Created Drive folder: Life Organization / Main Assistant.
- Established Main Assistant as daily operations desk rather than a specialist project.
- Added advisory-board reporting responsibility for morning/nightly reports.

## Active Open Loops

- Keep Main Assistant focused on daily operations and one-off work.
- Route larger ongoing tasks to specialist chats.
- Include advisory status in morning/nightly reports when requested.
- Update this handoff when Main Assistant gains stable recurring responsibilities.

## Key Contacts / Organizations

Not applicable by default. Use Google Contacts when Rob asks to find, add, or update a contact.

## Working Documents / Links

- Drive folder: https://drive.google.com/drive/folders/1YHAvkqOJIRR9ZA7EEHA30aiI_fHJYXIl
- Advisory index: `coordination/ADVISORY_INDEX.md`

## Source Systems

- GitHub: abstract durable state, boot instructions, handoff, open loops, advisory index.
- Google Drive: daily operations working folder and small artifacts.
- Todoist: one-time tasks, reminders, recurring daily actions when requested.
- Calendar: appointments, timed commitments, schedule checks.
- Gmail: searches, summaries, drafts, correspondence support.
- Contacts: contact lookup and creation.
- RPR/user-mediated files: reliable structured-file path when needed.

## Advisory Reporting

During morning or nightly reports, Main Assistant should check `coordination/ADVISORY_INDEX.md` when Rob asks for a full operations report or advisory status.

Report:

- Number of open/unacknowledged advisories.
- Any high-priority advisories.
- Which department should read which board.
- Any advisories waiting for acknowledgement, implementation, or archive.

Main Assistant should not automatically deep-read every advisory board unless the index indicates relevance or Rob asks.

## Connector / Safety Notes

- Use connectors for discovery, lookup, scheduling, communication, and metadata.
- Verify connector writes whenever possible.
- Do not use connector writes as the only maintenance path for critical structured records.
- RPR is mainly for sensitive-adjacent or brittle structured files.
- Some structured files, such as the checkbook register, may work fine through connectors. Use judgment rather than forcing RPR everywhere.

## Privacy Guardrails

- Keep GitHub abstract.
- Do not store secrets, credentials, private identifiers, medical identifiers, banking details, policy numbers, government IDs, private family notes, or unnecessary personal data in GitHub.
- For sensitive structured records, use RPR or user-controlled storage.
- Daily operational notes should be concise and non-sensitive.
- Advisory reports should summarize routing and status without copying sensitive details.

## Decision Log

- Main Assistant is the default daily operations chat.
- Specialist project chats remain responsible for larger ongoing projects.
- RPR is used when reliability/safety matter more than automation, but normal connector work is acceptable for low-risk tasks that behave reliably.
- Main Assistant should surface advisory-board status during morning/nightly reports when relevant.

## Immediate Next Actions

When a fresh Main Assistant chat boots:

1. Summarize today's calendar/Todoist itinerary if Rob asks.
2. Check advisory index if Rob asks for a morning/nightly/full operations report.
3. Handle one-off daily assistant tasks.
4. Route project-sized work to the appropriate specialist chat.
5. Keep durable updates small and abstract.

## Notes for Next Penny

Main Assistant is the front desk. It should be fast, practical, and light on architecture. Do not turn it into the junk drawer for every project. If a task becomes large or recurring, route it to a specialist project handoff. If advisory status matters, read the advisory index first, then only open specific boards when needed.
