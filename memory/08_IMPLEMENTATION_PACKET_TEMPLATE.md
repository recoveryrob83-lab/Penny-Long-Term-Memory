# Life OS Implementation Packet Template

Updated: 2026-07-02
Project: Life OS / Life Logistics HQ
Purpose: Reusable template for Strategy Penny to create clean, bounded work packets for Implementation Penny.
Source: Google Drive `09_IMPLEMENTATION_PACKET_TEMPLATE.md`

## Operating Rule

Strategy Penny uses this template when Rob and Penny finish planning a work batch.

Implementation Penny uses the completed packet as execution instructions.

Do not treat this template itself as the work packet. Copy the structure, fill it out, and give the filled packet to the Implementation chat.

## Why This Exists

Life OS now uses two modes:

- Strategy / Planning: chat, clarify, prioritize, decide, and design the batch.
- Implementation: perform connector work in bounded batches, verify results, update logs, and report back.

This protects connector context, reduces tool-call drift, and keeps Session Handoff and Open Loops fresher.

## Implementation Packet

### Packet Name

[Short name for the batch]

### Date

[YYYY-MM-DD]

### Strategy Source

[Name of Strategy chat or planning context]

### Goal

[One or two sentences describing the desired outcome.]

### Mode

Implementation only. Do not expand strategy unless the packet is blocked by missing facts.

### Required Startup Reads

Implementation Penny should open/read these before acting:

- `memory/00_START_HERE.md`
- `memory/01_SESSION_HANDOFF.md`
- `memory/02_BOOT_LOG.md`
- `memory/03_OPERATIONAL_RULES.md`
- `memory/10_PROFILE_REFERENCE.md`, if profile facts are needed.
- `memory/04_ACTIVE_PROJECTS.md`, if project context is needed.
- `memory/05_OPEN_LOOPS.md`.
- `memory/06_WEEKLY_PLAN.md`, if weekly priorities or dated commitments are relevant.
- `memory/09_APP_INTEGRATIONS_REFERENCE.md`, if tool routing is relevant.
- Any project-specific file named in this packet.

### Source Facts / Inputs

[Paste the exact facts, user decisions, screenshots, emails, dates, links, file names, and constraints needed for the work.]

### Constraints / Do Not Do

[List hard limits. Examples: do not send emails unless Rob explicitly asks; draft first; do not pursue deprioritized leads; do not store sensitive data; do not duplicate existing Calendar or Todoist items.]

### Connector Actions to Perform

Break actions into numbered chunks.

1. GitHub:
   - [Create/update/read durable memory files.]

2. Google Drive:
   - [Create/update/read working documents, Sheets, generated files, or Drive-hosted artifacts.]

3. Todoist:
   - [Add/update/complete/reschedule tasks.]

4. Google Calendar:
   - [Create/update/read events.]

5. Gmail:
   - [Search/read/label/draft emails.]

6. Other connectors:
   - [Use only if needed and available.]

### Verification Requirements

Implementation Penny must verify the result before reporting completion.

Examples:
- Fetch the created/updated GitHub file.
- Read back the created/updated Drive file.
- Re-list Todoist project tasks after changes.
- Re-search Calendar date range after event creation.
- Re-check Gmail labels or read relevant messages after label changes.

### Required Log Updates

After verified work, update:
- Session Handoff: always for meaningful work batches.
- Open Loops: always when loops are created, closed, changed, or clarified.
- Boot Log: only for durable architecture changes, major new files, important workflow decisions, or technical lessons.
- Active Projects: only when project structure/status changes.
- Weekly Plan: only when weekly priorities or dated commitments change.
- App Integrations Reference: only when tool routing or integration lessons change.

### Report Back Format

Implementation Penny should report back in this structure:

Completed:
- [What was successfully done.]

Verified:
- [What was checked/read back.]

Changed Files / Apps:
- [GitHub files, Drive files, Todoist projects, Calendar events, Gmail labels, etc.]

Important Findings:
- [Any important emails, dates, conflicts, missing links, or new facts.]

Blocked / Failed:
- [Anything that failed, was blocked by connector safety checks, or needs Rob's input.]

Open Loops Created or Updated:
- [Clear next actions.]

Logs Updated:
- [List exactly which logs were updated.]

### Strategy Return Note

Implementation Penny should end with:

"Ready to return this result to Strategy Penny."

## Packet Quality Checklist

Before handing the packet to Implementation Penny, Strategy Penny should check:

- Is the goal clear?
- Are all necessary links, dates, names, and constraints included?
- Are actions bounded enough for one implementation batch?
- Are sensitive actions clearly limited?
- Are verification steps explicit?
- Are log updates specified?
- Is there a clear report-back format?

## Sensitive Information Rule

Do not store or request sensitive vault-level information in implementation packets, including:
- Social Security Number.
- Passwords.
- Banking information.
- Exact street address unless Rob explicitly approves it for a specific task.
- Full birthdate.
- Government identification numbers.
- Sensitive medical records.

Use `memory/10_PROFILE_REFERENCE.md` for stable practical profile facts, but remember it is not a secure vault.
