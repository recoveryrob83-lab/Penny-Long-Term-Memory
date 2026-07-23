# Chief of Staff HQ Advisory Board

Updated: 2026-07-23
Purpose: Canonical advisory text sourced from Chief of Staff HQ, including formal advisories arising from LifeOS HQ meetings. The retained filesystem path remains `coordination/boards/main-assistant.md`.

## Open Advisories

None.

## Recently Acknowledged / Implemented Advisories

### ADV-20260718-042 — Move automated prompt verification from composer transport to receiving Workers

- Date: 2026-07-18
- From: Chief of Staff HQ / LifeOS HQ
- To: Engineering HQ
- Lifecycle State: CLOSED
- Priority: HIGH
- Implemented: 2026-07-23
- Source Verified: 2026-07-23
- Closed: 2026-07-23
- Closeout Authority: Rob
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department and Owner: Engineering HQ
- Record Class: Automation architecture implementation request

#### Implementation and Closeout

Engineering completed the receiver-side validation and supporting automation machinery requested by this advisory. The implemented system includes durable run correlation, canonical prompt and parameter validation, authority and ownership checks, duplicate suppression, fail-closed handling, explicit Worker outcomes, immutable result evidence, HQ verification, and bounded scheduled consumption.

Current Package D and Package E records and live-run evidence establish that the system was built and tested without transferring source-owner lifecycle authority, permitting silent scope expansion, or creating a competing operational ledger. Rob confirmed on 2026-07-23 that the system is complete and ready for slow rollout and authorized Chief of Staff HQ to close the source advisory.

Slow rollout remains an operational pacing decision, not an unresolved implementation condition. This advisory is implemented, source-verified, and closed.

### ADV-20260719-045 — Acknowledge the project and chat source memory architecture discovery

- Date: 2026-07-19
- From: Chief of Staff HQ / LifeOS HQ
- To: Life OS Maintenance HQ
- Lifecycle State: CLOSED
- Priority: NORMAL
- Advisory Revision: 1
- Verification Mode: IMMEDIATE_HQ
- Acknowledged: 2026-07-19
- Closed: 2026-07-19
- Posted Board: `coordination/boards/main-assistant.md`
- Target Department and Owner: Life OS Maintenance HQ
- Record Class: Architecture discovery and bounded awareness advisory

#### Acknowledgement and Outcome

Life OS Maintenance HQ consumed and acknowledged the verified ChatGPT Projects context-memory discovery and its boundaries:

- promoted responses may become shared project sources, with application refresh or restart sometimes required before visible confirmation;
- generated artifacts may provide durable room-specific Library context when retrieval is verified in the intended room;
- GitHub remains the canonical durable source;
- shared project sources must remain role-neutral;
- room identity, local procedures, and local context belong in chat-specific handbooks or artifacts;
- local handbooks may reduce routine boot overhead but do not replace Boot for fresh, stale, conflicted, degraded, or governance-sensitive contexts;
- replacement publication must avoid duplicate or numbered competing copies;
- handbook publication must include source manifests, conflict rules, meaningful-refresh discipline, and verified retrieval;
- the reserved sequence begins with a Maintenance room handbook and later a role-neutral global handbook only after separate direct authorization from Rob.

No handbook was generated. No boot rule, source rule, project source, architecture file, open loop, notebook plan, implementation advisory, or duplicate durable record was created. The advisory was informational only and is now acknowledged and closed.

### ADV-20260719-043 — Create canonical LifeOS operational and Worker protocols

- Lifecycle State: CLOSED
- Acknowledged: 2026-07-19
- Implemented: 2026-07-19
- Source Verified: 2026-07-19
- Closed: 2026-07-19

Life OS Maintenance HQ created the canonical shared execution protocol and Worker contract, integrated one HQ and Worker boot entry point, preserved the universal-kernel order, and retained the two root Worker pilots as compatibility packages.

### ADV-20260718-041 — Create a global Trello connector write SOP

- Lifecycle State: CLOSED
- Implemented: 2026-07-18
- Acknowledged: 2026-07-18
- Closed: 2026-07-18

Life OS Maintenance HQ extended the existing global Connector Reliability Operating Pattern with the Trello false-negative write protocol, live read-back, duplicate prevention, truthful reporting, and source-boundary protections.

## Board Rules

- Read `coordination/ADVISORY_INDEX.md` first.
- This retained path is the Chief of Staff HQ source board despite its legacy filename.
- LifeOS HQ formal advisories use Chief of Staff HQ as the source department.
- LifeOS HQ does not maintain a separate advisory board.
- Keep full actionable text for every open advisory and a bounded recent completed working set.
- Keep canonical advisory text here and routing state in the Advisory Index.
- Do not duplicate advisory text into target boards or department open loops merely for visibility.
- Use canonical lifecycle states and keep priority separate.
- Do not mark an advisory `IMPLEMENTED`, `SOURCE_VERIFIED`, or `CLOSED` without current evidence.
- Git history preserves the detailed text removed during compaction.