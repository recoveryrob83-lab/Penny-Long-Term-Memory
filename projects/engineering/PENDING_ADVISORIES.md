# Engineering Pending Advisory Board

Updated: 2026-07-04
Project: Chief Engineering Penny / Engineering HQ
Purpose: Local staging notebook for possible future Engineering advisories, operating-rule proposals, design guidelines, and architecture notes.

## Operating Rule

This file is not a published advisory board.

Items here are pending notes only. They should not be routed, indexed, or added to the Department Event Inbox until Rob explicitly asks Engineering to promote them into formal advisories.

Use this file when Rob says something like:

`Add this to the Pending Advisory Board.`

During a later advisory sync, Engineering may review these notes, merge duplicates, convert mature items into formal advisories, and clear or archive processed items.

## Pending Items

### PEND-ENG-20260704-001 — Demand-driven sync instead of always-on synchronization

- Date captured: 2026-07-04
- Source: Engineering discussion with Rob after scheduled-task failure
- Status: Pending
- Possible target if promoted: Life Logistics HQ / Life OS Infrastructure

#### Core Idea

Life OS should stop trying to keep every department synchronized all the time.

Instead, synchronization should be demand-driven:

1. Open the department when needed.
2. Boot from GitHub.
3. Read handoff and relevant inbox/advisory context.
4. Consume items addressed to that department.
5. Work.
6. Leave inactive departments alone.

#### Rationale

Scheduled tasks proved unreliable as persistent HQ workers because the scheduled sync created a new chat window and did not automatically warm required connectors. This made scheduled sync a source of uncertainty rather than cognitive relief.

Inactive HQs do not need synchronization. Departments should sync when they become active, not because a clock fires.

#### Possible Principle

Every active department should be synchronized before meaningful work begins. Not every department must remain synchronized at all times.

---

### PEND-ENG-20260704-002 — Treat advisories as mail, not instant messages

- Date captured: 2026-07-04
- Source: Engineering discussion with Rob about advisory overload and ADHD/cognitive load
- Status: Pending
- Possible target if promoted: Life Logistics HQ / Life OS Infrastructure

#### Core Idea

Advisories should generally be consumed during sync, not immediately when created.

Routine advisories should wait in the system until the target department opens or performs a deliberate sync. Rob should not need to manually run between rooms every time an advisory exists.

#### Rationale

Immediate advisory consumption causes context switching and makes Rob the human mail carrier. This is cognitively expensive, especially when ADHD-style capture pressure makes every visible item feel urgent.

This pending board is a local staging notebook only. The Department Event Inbox is frozen historical record and should not be used for normal routing.

#### Possible Operating Rule

Default advisory behavior: consume at next department sync.

Only urgent advisories should be manually routed immediately.

---

### PEND-ENG-20260704-003 — Sync boot order for active core HQs

- Date captured: 2026-07-04
- Source: Rob's proposed sync-order model
- Status: Pending
- Possible target if promoted: Life Logistics HQ

#### Core Idea

When multiple HQs need daily sync, use a predictable boot order so GitHub memory and routing state are clean before specialist departments act.

Current proposed order:

1. Life Logistics HQ
2. Main Assistant / Assistant Penny
3. Finance Penny when finance becomes active enough to need daily sync
4. Engineering Penny
5. Business Penny

Near-term active daily set may be:

- Life Logistics HQ
- Main Assistant / Assistant Penny
- Engineering Penny
- Business Penny

Finance is deferred until income, transactions, bills, or financial decisions make daily sync worthwhile.

#### Rationale

Life Logistics should go first because it maintains the GitHub memory map, advisory state, operating rules, and cross-project routing. Assistant Penny should follow because it handles daily operations. Specialist departments should sync only when active or when their work is immediately needed.

---

### PEND-ENG-20260704-004 — Reduce HQ count and consolidate temporary or low-interdependency projects

- Date captured: 2026-07-04
- Source: Rob's reflection on project/HQ overload
- Status: Pending
- Possible target if promoted: Life Logistics HQ

#### Core Idea

Some existing HQs may not need to remain standalone Life OS departments.

Potential consolidation direction:

- Job Search HQ may eventually fold into Assistant Penny because it is temporary and mostly involves email, Todoist, resume/cover-letter drafting, submissions, and follow-ups.
- Caregiver-related work may eventually fold into Assistant Penny if it becomes mostly logistics and task execution.
- Recovery and Philosophy may remain as thematic chats/workbenches but may not require active Life OS HQ synchronization unless they create durable infrastructure work.
- Scriptorium may remain a distinct project because it writes to its own GitHub repository and has a real project structure.

#### Rationale

Too many HQs create too many rooms for Rob to manage. Each department must earn its operational overhead.

#### Possible Principle

A project should become or remain an HQ only when it has ongoing, cognitively heavy, cross-system work that benefits from a dedicated role, handoff, and durable operating context.

Temporary projects and ordinary daily execution should default to Assistant Penny unless complexity justifies separation.

---

### PEND-ENG-20260704-005 — Advisory routing should mostly go through Life Logistics HQ

- Date captured: 2026-07-04
- Source: Rob's reflection on department-to-department chatter
- Status: Pending
- Possible target if promoted: Life Logistics HQ / Life OS Infrastructure

#### Core Idea

Most advisories should route upward to Life Logistics HQ rather than laterally between specialist departments.

Specialist departments usually do not need to talk directly to each other unless there is a concrete cross-domain dependency.

Examples:

- Engineering to Business may be appropriate for product requirements.
- Engineering to Finance may be appropriate for cost-bearing technical decisions.
- Finance to Assistant may be appropriate for daily payment reminders.
- Wellness to Business usually does not need direct advisory traffic.

#### Rationale

Life Logistics HQ is the post office and system coordinator. Routing most advisory traffic through Logistics reduces cross-chat chatter and gives Rob one central place to manage architecture and system state.

#### Possible Operating Rule

Default advisory target should be Life Logistics HQ unless there is a specific reason the receiving specialist department must ingest the context directly.

---

### PEND-ENG-20260704-006 — Scheduled tasks are not currently viable as reliable sync infrastructure

- Date captured: 2026-07-04
- Source: Engineering scheduled-sync pilot failure
- Status: Pending
- Possible target if promoted: Life Logistics HQ / Life OS Infrastructure

#### Core Idea

Scheduled tasks should not be treated as reliable daily HQ sync infrastructure at this stage.

Observed issues:

- Scheduled task created a new chat rather than updating the existing Engineering HQ chat.
- New chat did not have GitHub connector warmed.
- Sync did not run automatically until Rob manually activated the connector.
- This increased cognitive load instead of reducing it.

#### Rationale

The current scheduled-task behavior is too unreliable for core synchronization. It may still be useful for reminders or low-stakes prompts, but not for authoritative department sync.

#### Possible Decision

Retire scheduled HQ sync as the preferred architecture and replace it with active-session synchronization.

---

### PEND-ENG-20260704-007 — Connector reliability is highest-priority Penny product architecture risk

- Date captured: 2026-07-04
- Source: Business HQ confirmation and Engineering discussion
- Status: Pending
- Possible target if promoted: Business HQ / Life Logistics HQ / Engineering implementation packet

#### Core Idea

Connector failures are not merely ChatGPT inconvenience. They are a product-level reliability risk for Penny as an execution platform.

Observed or reported failure modes:

- Connector not loaded.
- Connector schema unavailable.
- Safety triggers blocking writes.
- Safety-trigger cascades that prevent Drive, Todoist, GitHub, or related actions from completing.
- Long-running chat degradation.
- New scheduled-task chats lacking connector access until manually activated.
- Connectors that can read successfully but fail on writes.
- Possible cases where an operation appears successful unless verified.

#### Rationale

A user-facing Penny product must not claim external work succeeded until verified. Future architecture needs operation lifecycle tracking, connector health states, write-ahead logging, idempotency, retry/backoff rules, degraded-mode UX, and RPR/export/manual fallback.

#### Existing Related Work

This overlaps with the active Engineering track: Reliable Connector Execution Layer.

Do not duplicate unless promoted as a broader product/business advisory.

---

### PEND-ENG-20260704-008 — Platform-agnostic architecture and cross-platform testing

- Date captured: 2026-07-04
- Source: Rob's reflection on ChatGPT platform limitations and possible Claude testing
- Status: Pending
- Possible target if promoted: Business HQ / Engineering HQ / Life Logistics HQ

#### Core Idea

Life OS architecture should remain platform-agnostic.

GitHub as durable memory allows multiple AI platforms to boot from the same system map. ChatGPT, Claude, or other platforms could potentially read the same GitHub handoffs and operate from the same architecture.

Rob may test other platforms to compare:

- Scheduled task behavior.
- Connector reliability.
- Desktop/mobile continuity.
- Context persistence.
- Tool limits.
- File/repo integration quality.

#### Rationale

The model is not necessarily the bottleneck. Platform behavior, app design, connector reliability, scheduled-task semantics, and tool limits may determine whether Penny is operationally useful.

#### Possible Principle

Do not overfit Life OS architecture to one AI platform's current app limitations. Keep durable memory portable wherever possible.

---

### PEND-ENG-20260704-009 — Pending Advisory Boards should absorb raw architectural ideas before formal routing

- Date captured: 2026-07-04
- Source: Pending Advisory Board advisory and implementation discussion
- Status: Pending
- Possible target if promoted: Already partially implemented by ADV-20260704-004

#### Core Idea

Conversation generates useful raw ideas faster than durable architecture should evolve. Pending Advisory Boards give departments a place to capture these ideas without immediate routing.

#### Rationale

This supports ADHD-friendly capture without turning every thought into an interrupt. It also improves advisory quality by allowing batching, merging, and review before promotion.

#### Current Status

Life Logistics has adopted the standard and created `coordination/PENDING_ADVISORY_BOARDS.md`. This item may be closed after Engineering reads the new standard and decides whether to maintain this local board permanently.

## Parking Lot / Possible Cleanup

- Consider whether ADV-20260704-003 should be consumed/closed after Engineering completes the next Reliable Connector Execution Layer packet.
- Consider whether Engineering should propose a formal HQ consolidation advisory after Logistics finishes current pending-board architecture work.
- Consider whether scheduled-task architecture should be explicitly deprecated or marked experimental-only in operational rules.
