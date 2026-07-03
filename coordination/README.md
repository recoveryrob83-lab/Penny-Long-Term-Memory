# Coordination

Updated: 2026-07-02
Purpose: Cross-project advisory board system for Penny departments.

## Operating Idea

Penny departments do not chat with each other directly.

They publish durable advisories in GitHub when one department produces information another department may need.

Rob or Main Assistant can then instruct the receiving department to read the relevant board and mark advisories as acknowledged, implemented, or archived.

## Role Policy

Life Logistics HQ is the postmaster and curator for the advisory system.

Main Assistant is the dispatcher. Main Assistant may include advisory status in full morning or nightly operations reports when Rob asks for those reports or advisory status.

Specialist departments are consumers, not routine reporters.

Specialist departments should not include advisory summaries in their normal reports, morning reports, boot summaries, or project updates unless Rob explicitly asks.

Specialist departments should read advisory boards only when:

- Rob instructs them to check a board.
- Main Assistant routes a specific advisory to them.
- Their project handoff or startup instructions specifically say to check advisory status after a recreated-chat recovery.
- They are writing an advisory because their project produced information another department needs.

## Files

- `ADVISORY_INDEX.md`: fast dashboard of open/advisory status.
- `boards/`: department advisory boards.
- `template.md`: standard advisory format.

## Read Pattern

During normal project boot, do not read every advisory board.

Read `coordination/ADVISORY_INDEX.md` only when:

- Rob asks for advisory status.
- Main Assistant is preparing a morning or nightly report.
- A project chat is being recreated and needs to know whether another department left relevant notes.
- Rob instructs a department to check another department's board.

Read a specific board only when the index shows a relevant open or unread advisory.

## Write Rule

Post an advisory only when something materially affects another department's work.

Do not post routine updates, greetings, brainstorming fragments, or low-value chatter.

## Privacy Rule

Keep advisories abstract and operational.

Do not store secrets, credentials, private identifiers, sensitive medical details, banking details, policy numbers, government IDs, private family notes, or unnecessary personal data.

Store intent, implications, and routing rather than sensitive source details.
