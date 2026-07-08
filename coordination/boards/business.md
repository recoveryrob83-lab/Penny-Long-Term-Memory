# Chief Business HQ Advisory Board

Updated: 2026-07-07
Purpose: Advisories from Chief Business HQ to other Penny departments.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

### ADV-20260707-025 — Engineering delivery playbook needed for bite-sized local service office cleanup offers

- Date: 2026-07-07
- From: Chief Business HQ / Virtual Assistant Business worker chat
- To: Chief Engineering Penny
- Priority: High
- Status: Acknowledged / Ingested by Engineering
- Posted Board: `coordination/boards/business.md`
- Target Department: Chief Engineering Penny
- Acknowledged: 2026-07-07
- Related Project(s): Virtual Assistant Business, local service business offers, HVAC Office Chaos Diagnostic, delivery playbook, operational systems design
- Source Location: Virtual Assistant Business worker chat, after HVAC ideal-client research and diagnostic draft

#### Summary

Business has narrowed the VA Business beachhead toward St. Louis-area HVAC and adjacent local service businesses with roughly 5–15 employees where field work is profitable but the office is leaking time, money, and owner energy.

Rob strongly prefers bite-sized, trust-building offers rather than broad promises to remodel an entire chaotic office. The delivery model should be built around fixing one concrete operational leak at a time.

Representative sales framing from Rob:

> "I get it. You don't know me. I'm a guy that looks like he plays Dungeons and Dragons in his free time and hasn't touched a pipe since I came down my mother's womb. So how about this: we fix ONE thing in your office. What's a small problem you need handled? How your leads get dealt with? The techs doing the work on time? Invoicing follow-up? We can do that job for around xxx."

#### Business Insight

The market and messaging look promising, but the offer must be deliverable. Business should not sell "I will fix your office" because that is too broad, risky, and likely to collapse into unbounded cleanup work.

Preferred direction:

- Sell controlled, bite-sized cleanup sprints.
- Diagnose first, then fix one leak.
- Use plain language and local-service-business trust building.
- Avoid leading with AI, automation, or new software.
- Do not automate chaos.
- Do not become responsible for years of unmanaged records, bookkeeping, HR, tax, legal, or compliance problems unless separately scoped.

#### Engineering Advisory Request

Chief Engineering Penny should design a delivery playbook for how Rob can reliably fulfill the promise without overextending.

Engineering should consider:

1. Diagnostic intake process
   - What Rob asks before touching any system.
   - How to identify current tools, owner/staff roles, lead sources, scheduling habits, paperwork flow, invoicing flow, and pain points.

2. Workflow map template
   - Standard map from lead to payment:
     Lead → Schedule → Dispatch → Job Completion → Invoice → Payment → Follow-up.
   - Keep the map simple enough for a skeptical service-business owner to understand.

3. Leak classification system
   - Lead leak.
   - Scheduling / dispatch leak.
   - Paperwork / job-notes leak.
   - Invoice-to-cash leak.
   - Owner bottleneck leak.
   - Software / habit leak.

4. Fix menu by leak type
   - Lead tracker, callback rules, missed-call review, estimate follow-up template.
   - Dispatch notes checklist, daily schedule review, callback / warranty tracker.
   - Job packet checklist, file naming rules, scan/upload routine, customer-history lookup process.
   - Same-day or next-business-day billing rule, unpaid invoice tracker, weekly AR review, payment reminder templates.
   - FAQ sheet, recurring task checklist, simple SOPs, decision rules.
   - Existing-software usage rules before adding new tools.

5. Sprint boundaries
   - Define what a one-problem cleanup sprint includes.
   - Define what is explicitly out of scope.
   - Define client inputs required before work starts.
   - Define stop conditions when the office is too chaotic for the scoped sprint.

6. Handoff package
   - Every sprint should end with concrete artifacts such as:
     - One workflow map.
     - One tracker or cleaned-up control sheet.
     - Three to five SOPs or checklists.
     - One weekly office control checklist.
     - One "what changed" summary.
     - One short walkthrough or training note.

7. Verification
   - Define how Rob knows the sprint is complete.
   - Define how to verify the client can actually use the new habit/system.
   - Avoid claiming recovered revenue unless measured and supported.

#### Initial Offer Shape to Evaluate

Engineering should evaluate a small paid diagnostic and one-problem sprint model.

Possible offer sequence:

1. HVAC Office Leak Audit
   - Paid diagnostic, possibly $250–$500 locally and creditable toward a sprint.
   - Outputs: diagnostic score, lead-to-payment workflow map, top three leaks, recommended cleanup sprint.

2. One-Problem Office Cleanup Sprint
   - Fixed-scope implementation focused on one leak, such as lead response, dispatch/job notes, or invoice follow-up.
   - Outputs should be limited, usable, and easy to explain.

#### Key Principle

Business can sell the promise, but Engineering must make the promise operational.

Do not build a software product yet. Build the repeatable delivery method first.

#### Engineering Acknowledgement

Engineering ingested this advisory on 2026-07-07. Initial idea capture was added to the Engineering notebook as `NOTE-20260707-002 — VA Business Delivery Architecture Watchlist`. Engineering will treat this as service-delivery architecture first, not software-product implementation.

### ADV-20260707-024 — Business HQ state maintenance needed for VA Business project

- Date: 2026-07-07
- From: Chief Business HQ
- To: Life Logistics HQ
- Priority: High
- Status: Implemented
- Posted Board: `coordination/boards/business.md`
- Target Department: Life Logistics HQ
- Implemented: 2026-07-07

Life Logistics HQ refreshed Business HQ parent state so Business HQ now treats Virtual Assistant Business as the active revenue-first sub-project and PennyOS / Penny Platform as paused, not abandoned.

Files updated:

- `projects/business-development/SESSION_HANDOFF.md`
- `projects/business-development/status.md`
- `projects/business-development/open_loops.md`
- `coordination/ADVISORY_INDEX.md`

Business HQ owns parent strategy, positioning, offers, customer discovery, marketing, and business model. Worker-level execution belongs in `projects/virtual-assistant-business/` and/or its dedicated chat once opened.

### ADV-20260707-022 — Finance awareness needed for Virtual Assistant income stream

- Date: 2026-07-07
- From: Chief Business HQ
- To: Chief of Finance Penny
- Priority: High
- Status: Acknowledged / Ingested by Finance
- Posted Board: `coordination/boards/business.md`
- Target Department: Chief of Finance Penny
- Acknowledged: 2026-07-07

Finance has ingested the VA Business income-stream context and is prepared to support pricing, income tracking, expenses, tax planning, and financial decision-making when concrete.

### ADV-20260707-021 — Virtual Assistant business project setup needed

- Date: 2026-07-07
- From: Chief Business HQ
- To: Life Logistics HQ
- Priority: High
- Status: Implemented
- Posted Board: `coordination/boards/business.md`
- Target Department: Life Logistics HQ
- Implemented: 2026-07-07

Life Logistics HQ created `projects/virtual-assistant-business/` as a Business HQ sub-project scaffold and updated the Active Projects, Open Loops, and Advisory Index files.

Remaining project work belongs primarily to Chief Business HQ: positioning, offers, Upwork profile, proposal templates, portfolio/sample packet, and lead/proposal/client operating system.

### ADV-20260704-001 — Business HQ research, Drive architecture, and reboot-state update needed

- Status: Acknowledged
- Board: `coordination/boards/business.md`

Chief Business HQ business-development state was consumed by Life Logistics HQ on 2026-07-04. Canonical Drive path remained under Chief Business HQ > Business Development.

### ADV-20260704-002 — Drive connector reliability is a major Penny product risk

- Status: Acknowledged
- Board: `coordination/boards/business.md`

Engineering HQ ingested this advisory and created Reliable Connector Execution Layer as the first concrete engineering research track.

### ADV-20260703-004 — Frequent logistics updates needed for Penny platform research

- Status: Acknowledged
- Board: `coordination/boards/business.md`

### ADV-20260703-005 — Product hypothesis feedback after Concept Notes read

- Status: Acknowledged
- Board: `coordination/boards/business.md`

### ADV-20260703-003 — Business research scaffold created

- Status: Acknowledged
- Board: `coordination/boards/business.md`
