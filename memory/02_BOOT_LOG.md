# Penny Boot Log

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ / Penny Long-Term Memory
Purpose: Long-term working memory and startup instructions for Penny across new chat windows.

## Current Durable Architecture Decision

GitHub is being promoted to the preferred durable memory layer for Life OS / personal-assistant Penny.

Reason:
- Real Markdown files.
- Commit history.
- Diffs.
- Rollback.
- Better auditability than Google Drive Docs for memory files.
- GitHub connector appears reliable for text file operations.

Google Drive remains useful and active for operational artifacts:
- Google Docs.
- Google Sheets.
- Checkbook Register.
- Job-search files.
- Generated documents.
- Meeting notes.
- Practical working files.

## Startup Protocol

When a new Penny chat begins for Life OS work:

1. Open GitHub repo `recoveryrob83-lab/Penny-Long-Term-Memory`.
2. Read `memory/STARTUP_BOOT.md`.
3. Read `memory/00_START_HERE.md`.
4. Read `memory/01_SESSION_HANDOFF.md`.
5. Read `memory/02_BOOT_LOG.md`.
6. Read `memory/03_OPERATIONAL_RULES.md`.
7. Read Active Projects and Open Loops as needed.
8. Use project-specific files and connectors only as required by Rob's task.

## Connector Recovery Lessons

A long-running chat may stop invoking connectors reliably. This should not be assumed to be a state problem, implementation problem, or user error.

Original preferred recovery workflow:

1. Stop over-debugging the degraded session.
2. Start a fresh Penny session.
3. Boot from GitHub memory.
4. Continue from the current handoff.

2026-07-02 field note:

Rob discovered that explicitly invoking a connector by name, such as `@Google Drive`, may help wake or route a connector before requiring a full fresh-chat reset.

This is not yet proven as a guaranteed fix, but it should be tried before abandoning a session.

Updated recovery order:

1. Explicitly name or tag the connector.
2. Try a small harmless read.
3. If the connector responds, continue normal work.
4. If it fails, use the fresh-chat GitHub boot workflow.

Rob summarized the broader attitude as: life on life's terms.

## Drive Connector Editing Lessons

2026-07-02 field note from Caregiver Project HQ:

Small, incremental Drive updates were more reliable than large complex batch edits.

When a complex update fails, retry as several tiny edits rather than repeatedly sending the same payload.

For Sheets and structured records, verify the target row, range, or document section after each update so mistakes are caught immediately.

If a Drive update is blocked because it appears to contain sensitive information or triggers safety checks, simplify the update and use abstract notes instead of repeatedly retrying detailed personal content.

When actively working with a connector over many turns, explicitly reference the connector in the conversation to maintain clear operational context.

These are operational guidelines based on repeated field observations, not claims about internal connector implementation.

## Project Chat Architecture Lesson

Project-specific chats should handle their own project work during the day.

Life Logistics HQ should perform cross-project review and nightly housekeeping.

This reduces connector pressure, keeps chats focused, makes project history easier for Rob to find, and prevents one Penny from repeatedly hitting every connector for every domain.

Project chats create project knowledge.

Life Logistics HQ curates operational memory.

## Current Context Snapshot

Rob and Penny are building a persistent Life OS for practical life organization.

Primary practical domains:
- Caregiver support / possible income project for Marqueto.
- Marqueto's mom house cleanup project in Alton, Illinois.
- Job search and interview tracking.
- Recovery routine and meeting schedule.
- Housing, benefits, medical, and general logistics.
- Finance tracking.
- Health and wellness expansion.
- Life OS infrastructure.

## Important Current Facts

Sober date: February 20, 2026.

Operating region: Metro East, Illinois. Use America/Chicago unless Rob says otherwise.

Major cleanup service area: Alton, Illinois.

Known cleanup contacts:
- The Junkluggers: 314-764-6855. Status unknown / needs call.
- Affordable Dumpster Rentals: 636-202-0730. Called. 10-yard dumpster quoted at $409.

Job search facts:
- Resume updated for marketing/social media positions.
- Plug Tech application submitted for Social Media Coordinator.
- Application number: 50364011.
- Wendy's interview scheduled for July 6, 2026 at 2:00 PM CDT in Fairview Heights, Illinois.
- Gmail label for job emails: Job Search.
- Top Tier Events interview scheduled July 2, 2026 at noon CDT; Zoom/details may arrive by SMS rather than Gmail.

Recovery routine includes:
- Step work.
- It Works reading.
- Meditation reading.
- Gratitude routine.
- Call Donald.
- Story reading.
- NA meeting.
- Step 11 prayer.
- Recovery journal.
- Weekly call three recovery people.

## Immediate Open Loops

- Continue collecting cleanup quotes for Alton, Illinois.
- Continue caregiver-income research for Illinois.
- Prepare for Wendy's interview.
- Use Checkbook Register for real transactions when data is ready.
- Keep recovery routine active.
- Continue migration from Drive-memory to GitHub-memory only when useful.
- Use Life OS for real daily operations and record lessons as they appear.

## Drive Source Files Imported / Mirrored

Initial Drive sources read during GitHub migration:

- Penny Boot Log: https://docs.google.com/document/d/1WXklLnp7DDPM0ZxYBgVH8NWHypbwcJ_p_59r5fDHNpY/edit
- Session Handoff: https://docs.google.com/document/d/1YNmrdoPkfWLlTjdDrZygYikKVTzfNmW4UC-v1Wfsh4I/edit
- 00_ROB_PROFILE_REFERENCE.md: https://docs.google.com/document/d/11nJ7Bdd3OvIqlpWS6AgUac4eoxKKAFu1Ac25tOj4MPw/edit
- 01_ACTIVE_PROJECTS.md: https://docs.google.com/document/d/1SBiQ-ykJGjJkhq-0UuEj29uPaDfmtTA0-VVPcKBVrXc/edit
- 02_STRATEGY_BOOT.md: https://docs.google.com/document/d/1YL9USMAwpbUdq16PrLktvJepOpLtWd3V0-XfG2GZl00/edit
- 07_WEEKLY_PLAN.md: https://docs.google.com/document/d/1qBq0zy9ZZmQka50qtEVAXxxNK673TS5s1ev9fvluX0w/edit
- 08_OPEN_LOOPS.md: https://docs.google.com/document/d/11VVd4i1ZCZBlVMnGFYhd3KcpSjEqTnbmTWHVAzqfJzg/edit
- 09_IMPLEMENTATION_PACKET_TEMPLATE.md: https://docs.google.com/document/d/1_4HSsukTLLToXkxhRN7EIKfyCTFTbIH9KwprGlpc-bk/edit
- 10_APP_INTEGRATIONS_REFERENCE.md: https://docs.google.com/document/d/1A3bqvltzgfXYIoAeaf1UVaM2lxzZyGZY4Bho7y5lpyM/edit
- 11_OPERATIONAL_RULES.md: https://docs.google.com/document/d/1fQbpXeUgGhdGyUzzDuyLRegaSvFztx5sG2eFXvjMifA/edit

## Penny Working Style

Act as Rob's practical executive assistant.

Prioritize:
- Accurate records.
- Clear open loops.
- Verified connector results.
- Short dated updates.
- Practical next actions.
- Separation of practical Life OS from philosophy unless Rob explicitly connects them.

Do not fabricate connector results. Label uncertainty.
