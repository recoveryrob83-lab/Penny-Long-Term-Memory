# Chief Engineering Penny Status

Updated: 2026-07-16

## Current Phase

Active / Connector Reliability, Worker Pilots, Prompt Systems, Office Leaks Delivery Architecture, and LifeOS Dashboard Exploration

## Summary

Chief Engineering Penny is the specialist department for technical architecture and implementation planning.

Engineering supports software architecture, repository strategy, APIs, connectors, MCP and integration research, data models, automation design, testing, technical feasibility, build sequencing, worker contracts, prompt systems, and build-ready implementation packets.

## Current Operating Model

The seven LifeOS department discussion HQ chats are open and ready.

Use regular Chat for planning, technical discussion, research, GitHub synchronization, prompt and command-system work, code-review discussion, debugging analysis, advisories, and small authorized connector-backed updates.

Reserve Work mode for substantial coding, local repository work, large file edits, test-suite execution, packaging, browser or desktop automation, complex artifact generation, and long-running implementation.

Each HQ is one structured perspective within a coherent Penny system. Main Assistant owns overall coordination and synthesis. Rob remains final authority for consequential, destructive, financial, and externally visible actions.

## Source-of-Truth Boundaries

- GitHub: durable memory map, architecture, boot files, handoffs, advisories, and stable project state.
- Google Drive: working records, design documents, Sheets, generated artifacts, and human-facing operational files.
- Trello: current attention and flow through the LifeOS Flow Board.
- Todoist: Rob-facing task management and commitments.
- Calendar: timed commitments.
- Gmail: communication evidence.
- Dedicated software repositories: code, tests, issues, PRs, and technical implementation artifacts when created.

Never store secrets, credentials, tokens, API keys, financial account details, medical details, private user data, or sensitive implementation details in Life OS GitHub memory.

## Current Focus

### Reliable Connector Execution Layer

Connector reliability remains the primary cross-worker Engineering risk.

Current design outputs:

- operation ledger / write-ahead log;
- connector health-state model;
- idempotency and duplicate prevention;
- post-write verification;
- bounded retry, backoff, and stop policy;
- degraded-mode user experience;
- RPR, export, manual-upload, or alternate-worker fallback;
- queue-first future execution model;
- explicit verified, unverified, partial, failed, and blocked states.

Observed operating lessons:

- small operations outperform broad batch writes;
- explicit connector invocation helps scope and reliability;
- one-connector-focused sessions are easier to verify;
- fresh booted chats are preferable to repeatedly retrying degraded sessions.

These are field observations, not claims about platform internals.

### Life OS Worker Architecture

Implemented:

- Penny Raw Capture Worker: `workers/penny-raw-capture/`
- Penny Inventory Worker: `workers/penny-inventory/`

Both packages are architecture-complete. The next useful evidence is real production behavior.

Inventory remains one row per physical item and excludes pricing, bundling, listing generation, publication, and sale strategy.

### Office Leaks Delivery Architecture

Engineering supports two integrated delivery layers:

1. Mechanical: map, score, scope, sprint, verify, handoff, follow up.
2. Human-system: respect, rapport, internal champion, users, Aha Moment, adoption verification, relational follow-up.

Current reference:

- `projects/engineering/notebook/NOTE-20260708-006-office-leaks-human-system-delivery-layer.md`
- Drive: `Engineering Delivery Architecture Specification - HVAC Office Cleanup`

### LifeOS Chat HQ Architecture

ADV-20260715-036 is implemented, acknowledged, and closed. Rob confirmed all seven HQ chats are open and ready.

Engineering's next role is to observe real use for routing friction, overlapping authority, stale boot assumptions, connector limitations, unnecessary model usage, and work that should move between Chat and Work.

Do not build another architecture layer unless observed friction justifies it.

### Read-Mostly LifeOS Desktop Dashboard

ADV-20260716-038 is acknowledged, ingested, and closed.

Engineering recognizes a staged desktop dashboard concept that should:

- present high-signal current state from Trello, Todoist, Calendar, Gmail, and Drive;
- preserve those systems as authoritative;
- keep Penny as the worker and conversational control layer;
- retain the prompt launcher as the primary directly usable component;
- begin read-only or read-mostly;
- center the first useful view on Trello `Now`, top `Next`, daily commitments, schedule pressure, mail-attention signals, and pinned working files;
- exclude account-linked financial connector data from multi-connector Hub operation;
- avoid implementation until Rob supplies further requirements and authorizes a staged specification or build.

## Advisory State

- No incoming Engineering advisories remain open after ADV-20260716-038 was consumed.
- ADV-20260716-039 is open from Engineering to Life Logistics HQ for reconciliation of stale shared global summaries.
- Advisory Index remains the sole active routing dashboard.
- Department Event Inbox remains frozen historical state.

## Current Open Work

- Pilot Penny Inventory Worker with 2–3 real sale items.
- Observe one-row-per-item writes, image-reference sequencing, uncertainty handling, append reliability, and final Sheet verification.
- Observe Penny Raw Capture Worker in real use.
- Turn the Reliable Connector Execution Layer design note into an implementation packet outline.
- Draft the operation ledger schema.
- Define connector health, idempotency, verification, and bounded retry behavior.
- Continue Office Leaks one-problem delivery architecture as Business requirements mature.
- Observe the Chat HQ system before proposing refinements.
- Develop a staged dashboard specification only when Rob returns with concrete requirements.
- Keep the Engineering HQ Daily Sync paused pending stronger scheduled-execution architecture and explicit authorization.

Deferred prompt-launcher improvements are recorded in `projects/engineering/notebook/NOTE-20260716-007-prompt-launcher-advisory-commands-and-scope.md` rather than added to the active open-loop stack.

## Completed Recent Work

- 2026-07-16: ADV-20260716-038 consumed; read-mostly LifeOS dashboard concept ingested without authorizing implementation.
- 2026-07-16: ADV-20260716-039 routed to Life Logistics for stale global-summary reconciliation.
- 2026-07-16: Literal newline escapes from Hub Boot onward were corrected in the prompt launcher database.
- 2026-07-15: Seven LifeOS department discussion HQ chats opened and declared ready; ADV-20260715-036 closed.
- 2026-07-15: Daily Operating SOP integrated into the global boot path; ADV-20260715-035 closed.
- 2026-07-15: Expanded response, connector, and hub shortcut vocabulary synchronized.
- 2026-07-10: Inventory Worker architecture and durable package completed.
- 2026-07-09: Formal worker layer and Raw Capture Worker implemented.
- 2026-07-08: Office Leaks delivery architecture advanced.

## Coordination Notes

- Business defines what should be built and why.
- Office Leaks owns its active service strategy and requirements.
- Engineering defines how to build safely and in what order.
- Finance owns cost-bearing choices.
- Main Assistant owns daily coordination and synthesis.
- Life Logistics owns cross-project memory hygiene and shared global reconciliation.
- Wellness owns health and recovery sustainability.

## Boundary

Chief Engineering Penny owns technical architecture and implementation planning. It does not own business strategy, financial decisions, daily administration, wellness judgment, or cross-project memory curation.