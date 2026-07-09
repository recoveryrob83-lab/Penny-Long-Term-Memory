# NOTE-20260708-005 — Office Leak Delivery Playbooks v1

Date: 2026-07-08
Project: Chief Engineering Penny / Engineering HQ
Related Projects: Virtual Assistant Business, Chief Business HQ, HVAC Office Cleanup, future PennyOS / Penny Platform
Status: Active delivery architecture draft / process definition

## Purpose

This note defines Delivery Playbook v1 for the six Office Leak categories currently identified by Business HQ:

1. Lead leak
2. Scheduling / dispatch leak
3. Paperwork / job-notes leak
4. Invoice-to-cash leak
5. Owner bottleneck leak
6. Software / habit leak

The focus is delivery quality and repeatability, not marketing, pricing, branding, or final product packaging.

The goal is to give Rob a repeatable implementation method for one-problem office cleanup sprints without letting a scoped repair turn into a full-office rescue mission.

## Universal Delivery Rules

These rules apply to every Office Leak category.

### Unit of Work

The unit of work is one leak.

Not the whole company.
Not the whole office.
Not every broken process.
Not years of accumulated records.

### Universal Sprint Shape

Every One-Problem Office Cleanup Sprint should follow this pattern:

1. Confirm the selected leak.
2. Confirm the current failure pattern.
3. Confirm the desired future habit.
4. Confirm required client inputs.
5. Confirm exclusions and stop conditions.
6. Map the tiny workflow around the leak.
7. Build the minimum useful artifact.
8. Test with one real or simulated example.
9. Adjust based on the test.
10. Train owner/staff on the new routine.
11. Verify the client can use it without Rob driving every step.
12. Document what changed and what remains out of scope.

### Universal Required Client Inputs

Every sprint needs:

- One decision-maker.
- One point of contact.
- One staff person who actually touches the process, if different from the decision-maker.
- 2-5 recent examples of the leak, not years of records.
- Access to the current tool, spreadsheet, paper form, or workflow view if needed.
- Permission to change or introduce the specific artifact/process inside the sprint scope.
- Agreement on completion criteria.

### Universal Completion Criteria

A sprint is complete when:

- The agreed artifact exists.
- The responsible person knows where it lives.
- The responsible person knows when to use it.
- The new process has been tested with one real or simulated example.
- The client can explain the new routine in plain language.
- Remaining out-of-scope problems are documented.
- The handoff package is delivered.

### Universal Verification Method

Do not verify by document delivery alone.

Verify through demonstration:

- Show the artifact.
- Walk through a realistic example.
- Ask the client or staff member to explain the next step.
- Confirm ownership of the habit.
- Confirm when the habit happens.
- Confirm what happens if the habit breaks.

### Universal Stop Conditions

Stop, rescope, or refuse if:

- The leak is not scoped.
- Required inputs are missing.
- No decision-maker is available.
- The work requires accounting, tax, legal, HR, payroll, or compliance judgment.
- The client expects guaranteed recovered revenue.
- The client wants automation before the manual workflow is understood.
- The sprint is expanding into full-office cleanup.
- The client expects Rob to permanently own the process.
- Sensitive system access is requested or required beyond the scoped need.
- The problem is primarily a personnel conflict, not a workflow leak.

---

# 1. Lead Leak Playbook

## Definition

A lead leak occurs when a potential customer inquiry is missed, delayed, forgotten, inconsistently followed up, or not converted into a clear next action.

Common examples:

- Missed calls are not reviewed.
- Web form submissions sit unseen.
- Referral leads are texted to the owner and forgotten.
- Estimates are sent but not followed up.
- Leads live in voicemail, email, text, paper notes, and memory at the same time.

## Repeatable Implementation Process

### Step 1 — Identify Lead Sources

List every current lead source:

- Phone calls.
- Voicemail.
- Website forms.
- Email.
- Google Business Profile.
- Facebook or local groups.
- Referrals.
- Existing customer callbacks.
- Vendor or partner referrals.

Output: Lead Source Inventory.

### Step 2 — Map Current Lead Capture

For each source, answer:

- Who sees it first?
- Where is it recorded?
- What counts as a response?
- What is the expected response time?
- What happens if nobody responds?
- How does the lead become scheduled, quoted, declined, or followed up?

Output: Current Lead Capture Map.

### Step 3 — Identify Failure Pattern

Classify the lead leak:

- Not captured.
- Captured but not assigned.
- Assigned but not followed up.
- Followed up but not tracked.
- Estimate sent but not revisited.
- Lead outcome unknown.

Output: Lead Leak Type.

### Step 4 — Build Minimum Lead Control

Create the simplest control artifact that makes every lead visible.

Possible artifacts:

- Lead tracker sheet.
- Missed-call review checklist.
- Daily lead review checklist.
- Estimate follow-up tracker.
- Callback rule.
- Lead outcome codes.

Output: Lead Control Artifact.

### Step 5 — Define Daily Lead Habit

Define:

- Who checks new leads?
- When do they check?
- Where do they record them?
- What counts as done?
- What gets escalated to owner?

Output: Daily Lead Habit.

### Step 6 — Test

Run 2-3 sample leads through the new control.

Include one simple lead and one messy lead if possible.

Output: Tested lead flow.

### Step 7 — Handoff

Train owner/staff on:

- Where leads go.
- How to update status.
- How to mark next action.
- How to review open leads.
- How to follow up estimates.

Output: Lead Leak Handoff Note.

## Required Client Inputs

- List of lead sources.
- Recent examples of missed or delayed leads.
- Current phone/email/form process.
- Staff person responsible for lead intake.
- Desired response expectations.
- Current estimate follow-up practice.

## Internal Templates

- Lead Source Inventory.
- Lead Tracker.
- Missed-Call Review Checklist.
- Estimate Follow-Up Tracker.
- Daily Lead Review Checklist.
- Lead Outcome Codes.
- Lead Leak Handoff Note.

## Completion Criteria

- All known lead sources are listed.
- One lead capture location or lead review routine is defined.
- Open leads have visible status and next action.
- Responsible person is named.
- Client can run a sample lead through the tracker/checklist.

## Verification Method

Ask the client/staff member to demonstrate:

1. Where a new lead is entered.
2. How status is updated.
3. Where next action is recorded.
4. How overdue follow-up is found.
5. What gets escalated to owner.

## Risks

- Client has too many lead channels with no owner.
- Owner expects the tracker to replace sales discipline.
- Staff do not consistently enter leads.
- Follow-up expectations are vague.
- Lead sources are mixed with customer service, callbacks, or warranty work.

## Stop Conditions

Stop or rescope if:

- Client refuses to choose a lead owner.
- Client wants marketing strategy, ad management, or sales coaching instead of lead control.
- Client expects guaranteed conversion or recovered revenue.
- Lead data is spread across systems the client will not show or explain.
- Lead volume is too high for a manual tracker and requires software/process review beyond sprint scope.

---

# 2. Scheduling / Dispatch Leak Playbook

## Definition

A scheduling / dispatch leak occurs when jobs are booked, assigned, moved, or communicated inconsistently, causing missed appointments, confused technicians, callbacks, idle time, or owner intervention.

Common examples:

- Schedule changes live in the owner's head.
- Techs do not receive clear job notes.
- Customer expectations are not captured.
- Urgent calls disrupt the day's plan with no visible priority rule.
- Warranty/callback jobs are mixed into normal work without tracking.

## Repeatable Implementation Process

### Step 1 — Map Scheduling Intake

Identify how a job becomes scheduled:

- Who books it?
- What information is required?
- Where is it recorded?
- How is time/date confirmed?
- How are changes handled?

Output: Scheduling Intake Map.

### Step 2 — Map Dispatch Handoff

Identify what the technician receives:

- Customer name/contact.
- Address.
- Problem description.
- Equipment notes.
- Access instructions.
- Warranty/callback status.
- Estimate or approved work status.

Output: Dispatch Handoff Map.

### Step 3 — Identify Failure Pattern

Classify leak:

- Job scheduled without complete info.
- Schedule changed without notifying all parties.
- Tech lacks job context.
- Priority/urgent work not triaged.
- Callback/warranty not flagged.
- End-of-day open jobs not reviewed.

Output: Scheduling Leak Type.

### Step 4 — Build Minimum Dispatch Control

Possible artifacts:

- Dispatch Notes Checklist.
- Daily Schedule Review Checklist.
- Job Change Rule.
- Callback/Warranty Tracker.
- End-of-Day Open Job Review.

Output: Dispatch Control Artifact.

### Step 5 — Define Daily Schedule Habit

Define:

- Morning schedule review.
- Who owns schedule changes.
- How changes are communicated.
- What techs must know before leaving.
- How unfinished jobs are reviewed.

Output: Daily Schedule Habit.

### Step 6 — Test

Run one normal job and one changed/urgent job through the new process.

Output: Tested dispatch flow.

### Step 7 — Handoff

Train office/owner on checklist and schedule review habit.

Output: Scheduling / Dispatch Handoff Note.

## Required Client Inputs

- Current schedule view.
- Examples of scheduling confusion.
- Current dispatch notes or job tickets.
- Staff/tech roles.
- Current callback/warranty handling.
- Owner rules for urgent jobs.

## Internal Templates

- Scheduling Intake Map.
- Dispatch Notes Checklist.
- Daily Schedule Review Checklist.
- Job Change Rule Template.
- Callback/Warranty Tracker.
- End-of-Day Open Job Review.
- Scheduling / Dispatch Handoff Note.

## Completion Criteria

- Required job information is defined.
- Schedule change process is defined.
- Dispatch checklist exists.
- Responsible schedule owner is named.
- Client can walk through a normal and changed job scenario.

## Verification Method

Ask client/staff to demonstrate:

1. How a job is scheduled.
2. What information is required before dispatch.
3. How a schedule change is communicated.
4. How a callback or warranty job is flagged.
5. How unfinished jobs are reviewed.

## Risks

- Owner overrides schedule constantly.
- Staff avoid enforcing required job information.
- Techs resist checklist use.
- Existing field-service software is underused.
- Emergency work makes the schedule unstable.

## Stop Conditions

Stop or rescope if:

- Client wants full dispatch management instead of process cleanup.
- No one can own schedule updates.
- Client refuses to define required job information.
- Tech behavior/personnel issues are the true root problem.
- The work requires software migration or full field-service platform redesign.

---

# 3. Paperwork / Job-Notes Leak Playbook

## Definition

A paperwork / job-notes leak occurs when job information, photos, forms, customer history, parts notes, approvals, or technician notes are missing, scattered, illegible, late, or impossible to find.

Common examples:

- Office has to chase techs for notes.
- Photos stay on phones.
- Paper forms pile up.
- Customer history is hard to locate.
- Invoice is delayed because job details are incomplete.
- Warranty/callback context is missing.

## Repeatable Implementation Process

### Step 1 — Identify Required Job Record

Define what a complete job record must include.

Possible fields:

- Customer.
- Date.
- Address.
- Technician.
- Problem reported.
- Work performed.
- Parts/materials.
- Photos.
- Customer approval.
- Follow-up needed.
- Billing status.

Output: Complete Job Record Definition.

### Step 2 — Map Current Job Notes Flow

Identify:

- Where notes start.
- Who writes them.
- When they are submitted.
- Where photos go.
- Who checks completeness.
- Where documents are stored.

Output: Job Notes Flow Map.

### Step 3 — Identify Failure Pattern

Classify leak:

- Notes missing.
- Notes late.
- Photos missing.
- Paper not scanned/uploaded.
- Files named inconsistently.
- Office cannot find customer/job history.
- Incomplete notes delay invoice.

Output: Paperwork Leak Type.

### Step 4 — Build Minimum Job Packet Control

Possible artifacts:

- Job Packet Checklist.
- End-of-Job Notes Requirement.
- Photo Saving Rule.
- File Naming Guide.
- Scan/Upload Routine.
- Missing Notes Tracker.

Output: Job Packet Control.

### Step 5 — Define Closeout Habit

Define:

- What must happen before a job is considered office-complete.
- Who checks job packet completeness.
- When missing notes are chased.
- Where final job records live.

Output: Job Closeout Habit.

### Step 6 — Test

Run one completed job through the checklist. Identify missing fields and adjust.

Output: Tested job packet process.

### Step 7 — Handoff

Train office/owner on complete job packet standard and storage routine.

Output: Paperwork / Job-Notes Handoff Note.

## Required Client Inputs

- Recent completed job example.
- Recent messy/incomplete job example.
- Current forms or job tickets.
- Current storage location.
- Current photo process.
- Person responsible for checking completeness.

## Internal Templates

- Complete Job Record Definition.
- Job Notes Flow Map.
- Job Packet Checklist.
- End-of-Job Notes Requirement.
- File Naming Guide.
- Scan/Upload Routine.
- Missing Notes Tracker.
- Paperwork / Job-Notes Handoff Note.

## Completion Criteria

- Complete job record is defined.
- Checklist exists.
- Storage/naming routine exists.
- Missing notes process is defined.
- Client can process one sample job packet.

## Verification Method

Ask client/staff to demonstrate:

1. Where job notes are captured.
2. What makes a job packet complete.
3. Where photos/documents are stored.
4. How missing notes are flagged.
5. How a job record is found later.

## Risks

- Techs do not comply.
- Notes are too detailed or too burdensome.
- Storage locations multiply.
- Paper and digital systems conflict.
- Client expects historical records cleanup.

## Stop Conditions

Stop or rescope if:

- Client wants years of paper records organized under one sprint.
- Required documents include sensitive legal, HR, payroll, tax, or compliance records.
- Staff refuse to provide sample job records.
- Client wants Rob to chase technicians indefinitely.
- The issue is primarily technician management, not process design.

---

# 4. Invoice-to-Cash Leak Playbook

## Definition

An invoice-to-cash leak occurs when completed work is not billed promptly, unpaid invoices are not reviewed, payment reminders are inconsistent, or the office lacks a visible process from job completion to payment.

Common examples:

- Completed jobs sit unbilled.
- Invoices wait on missing notes.
- Nobody reviews unpaid invoices weekly.
- Payment reminders are irregular.
- Owner has to remember who owes money.

## Repeatable Implementation Process

### Step 1 — Map Billing Trigger

Identify what triggers invoice creation:

- Job marked complete.
- Technician submits notes.
- Owner approves.
- Office receives parts/labor info.
- Customer approval is documented.

Output: Billing Trigger Map.

### Step 2 — Map Current Invoice Flow

Identify:

- Who creates invoices.
- When invoices are created.
- What information is required.
- Where unpaid invoices are visible.
- Who reviews accounts receivable.
- How reminders are sent.

Output: Invoice Flow Map.

### Step 3 — Identify Failure Pattern

Classify leak:

- Completed jobs not billed.
- Missing job info delays billing.
- Unpaid invoices not reviewed.
- Reminder process inconsistent.
- Payment status not visible.
- Owner is the only AR memory.

Output: Invoice-to-Cash Leak Type.

### Step 4 — Build Minimum Billing Control

Possible artifacts:

- Completed-but-not-billed tracker.
- Unpaid Invoice Tracker.
- Weekly AR Review Checklist.
- Payment Reminder Template.
- Billing Readiness Checklist.
- Same-day / next-business-day billing rule.

Output: Invoice Control Artifact.

### Step 5 — Define Weekly Cash Habit

Define:

- When invoices are reviewed.
- Who reviews them.
- What status categories exist.
- When reminders are sent.
- What gets escalated.

Output: Weekly Invoice-to-Cash Habit.

### Step 6 — Test

Run one completed job and one unpaid invoice through the control.

Output: Tested billing review flow.

### Step 7 — Handoff

Train office/owner on tracker/checklist and escalation rule.

Output: Invoice-to-Cash Handoff Note.

## Required Client Inputs

- Current invoicing tool/process.
- One recent completed job that was billed properly.
- One recent delayed invoice example.
- One unpaid invoice example, with sensitive details minimized.
- Person responsible for billing.
- Existing payment reminder language, if any.

## Internal Templates

- Billing Trigger Map.
- Invoice Flow Map.
- Billing Readiness Checklist.
- Completed-But-Not-Billed Tracker.
- Unpaid Invoice Tracker.
- Weekly AR Review Checklist.
- Payment Reminder Template.
- Invoice-to-Cash Handoff Note.

## Completion Criteria

- Billing trigger is defined.
- Unbilled/completed work has a visible control.
- Unpaid invoices have a review routine.
- Reminder/escalation rule is defined.
- Client can process one sample invoice through the routine.

## Verification Method

Ask client/staff to demonstrate:

1. How a completed job becomes ready for billing.
2. Where unbilled jobs are visible.
3. Where unpaid invoices are reviewed.
4. When reminders happen.
5. What gets escalated to owner.

## Risks

- Missing job notes are the real bottleneck.
- Client expects collections service.
- Client expects accounting advice.
- Unpaid invoices involve disputes.
- Existing accounting software is underused or messy.

## Stop Conditions

Stop or rescope if:

- Client requests accounting, tax, bookkeeping cleanup, collections, or legal advice.
- Invoice problems involve disputed work, contracts, liens, or legal escalation.
- Client wants guarantee of recovered cash.
- Historical AR cleanup is too large for one sprint.
- Required billing information is unavailable.

---

# 5. Owner Bottleneck Leak Playbook

## Definition

An owner bottleneck leak occurs when routine decisions, repeated questions, approvals, or next steps depend on the owner's memory, availability, or direct intervention even when the work could be standardized.

Common examples:

- Staff ask the owner the same questions repeatedly.
- Owner is the only one who knows how to handle routine exceptions.
- Work pauses until owner replies.
- Owner carries too many open loops mentally.
- Recurring tasks are not delegated because there is no checklist or decision rule.

## Repeatable Implementation Process

### Step 1 — Identify Repeated Owner Interruptions

Ask:

- What questions do staff ask repeatedly?
- What decisions always come to owner?
- What work waits because only owner knows the answer?
- What does owner have to remember every week?

Output: Owner Interruption Inventory.

### Step 2 — Select One Bottleneck

Pick one repeated decision or task, not every owner problem.

Selection criteria:

- Frequent.
- Low-risk.
- Explainable.
- Not legal/HR/accounting/compliance.
- Can be turned into a checklist, FAQ, or decision rule.

Output: Selected Bottleneck.

### Step 3 — Capture Owner Logic

Interview owner for:

- When this issue happens.
- What information is needed.
- What normal answer is.
- What exceptions exist.
- When staff should escalate.

Output: Owner Logic Notes.

### Step 4 — Build Minimum Delegation Artifact

Possible artifacts:

- FAQ Sheet.
- Decision Rule.
- Escalation Rule.
- Recurring Task Checklist.
- Office Quick Reference.
- Owner Approval Thresholds.

Output: Bottleneck Relief Artifact.

### Step 5 — Define Delegation Habit

Define:

- Who uses the artifact.
- When they use it.
- What they can decide without owner.
- What must still go to owner.
- How exceptions are recorded.

Output: Delegation Habit.

### Step 6 — Test

Run 2-3 common questions/decisions through the artifact.

Output: Tested decision/checklist flow.

### Step 7 — Handoff

Train owner and staff on the new decision boundary.

Output: Owner Bottleneck Handoff Note.

## Required Client Inputs

- List of repeated owner interruptions.
- Owner availability for short interview.
- Staff perspective if possible.
- Examples of repeated questions.
- Owner's preferred rules/thresholds.
- Staff person who will use the artifact.

## Internal Templates

- Owner Interruption Inventory.
- Owner Logic Capture Sheet.
- FAQ Template.
- Decision Rule Template.
- Escalation Rule Template.
- Recurring Task Checklist.
- Owner Bottleneck Handoff Note.

## Completion Criteria

- One repeated bottleneck is selected.
- Owner logic is captured.
- A reusable artifact exists.
- Staff know when to use it.
- Escalation boundary is clear.
- Client can run sample situations through the artifact.

## Verification Method

Ask owner/staff to demonstrate:

1. Where the FAQ/rule/checklist lives.
2. Which question/task it handles.
3. What staff can do without owner.
4. What still requires owner.
5. How exceptions are handled.

## Risks

- Owner does not want to delegate.
- Staff do not trust the artifact.
- Bottleneck is actually authority/control, not missing documentation.
- Decision requires professional judgment.
- Artifact becomes too complicated.

## Stop Conditions

Stop or rescope if:

- The bottleneck is HR discipline, legal risk, tax/accounting judgment, or compliance-sensitive.
- Owner refuses to define delegation boundaries.
- Staff conflict is the core problem.
- Owner expects Rob to become the decision-maker.
- Scope expands into full management consulting.

---

# 6. Software / Habit Leak Playbook

## Definition

A software / habit leak occurs when tools exist but are inconsistently used, duplicated, avoided, misunderstood, or bypassed by informal habits. The leak is usually not lack of software. It is lack of agreed workflow behavior around the software.

Common examples:

- Field-service software exists but staff use texts and sticky notes.
- Customer info lives in multiple places.
- Spreadsheets duplicate software fields.
- Staff do not know which tool is authoritative.
- New software is requested before the current process is understood.

## Repeatable Implementation Process

### Step 1 — Inventory Current Tools

List tools used for:

- Leads.
- Scheduling.
- Dispatch.
- Job notes.
- Photos/files.
- Invoicing/payment.
- Customer follow-up.
- Internal communication.

Output: Tool Inventory.

### Step 2 — Identify Source of Truth Confusion

For each major workflow item, ask:

- Where should this information live?
- Where does it actually live?
- Who updates it?
- Who trusts it?
- What workaround exists?

Output: Source-of-Truth Confusion Map.

### Step 3 — Identify Habit Failure Pattern

Classify leak:

- Tool not used.
- Tool partially used.
- Duplicate entry.
- Shadow spreadsheet/paper process.
- Staff unclear on authoritative location.
- Owner distrusts tool because data is stale.
- Tool is too complex for current habit maturity.

Output: Software / Habit Leak Type.

### Step 4 — Build Minimum Usage Rule

Possible artifacts:

- Existing-Tool Usage Rule.
- Source-of-Truth Rule.
- Quick Reference Guide.
- Weekly Tool Cleanup Checklist.
- Minimum Viable Workflow Map.
- Do/Do Not Use This For list.

Output: Tool Habit Artifact.

### Step 5 — Define Maintenance Habit

Define:

- What must be updated.
- Who updates it.
- When updates happen.
- Which system is authoritative.
- What workaround is retired.
- What gets reviewed weekly.

Output: Tool Maintenance Habit.

### Step 6 — Test

Run one workflow example through the tool usage rule.

Example: new lead, scheduled job, completed job, or unpaid invoice.

Output: Tested software habit flow.

### Step 7 — Handoff

Train owner/staff on the source-of-truth rule and quick reference.

Output: Software / Habit Handoff Note.

## Required Client Inputs

- List of current tools.
- Examples of duplicated/conflicting records.
- Staff explanation of actual habits.
- Owner explanation of desired tool use.
- Access by screen-share or screenshots if possible.
- One workflow example to test.

## Internal Templates

- Tool Inventory.
- Source-of-Truth Confusion Map.
- Existing-Tool Usage Rule.
- Quick Reference Guide.
- Weekly Tool Cleanup Checklist.
- Minimum Viable Workflow Map.
- Software / Habit Handoff Note.

## Completion Criteria

- Current tools are inventoried.
- One source-of-truth confusion is selected.
- Usage rule is documented.
- Responsible person is named.
- One example is processed through the rule.
- Client understands that new software is not the default answer.

## Verification Method

Ask client/staff to demonstrate:

1. Which tool is authoritative for the selected workflow.
2. Where the information is entered.
3. What old workaround is retired or limited.
4. Who maintains the tool habit.
5. How weekly cleanup happens.

## Risks

- Client thinks software alone fixes habits.
- Staff resist changing workarounds.
- Owner wants a new platform too early.
- Existing tool is genuinely inadequate but migration is out of scope.
- Rob gets pulled into software implementation beyond the sprint.

## Stop Conditions

Stop or rescope if:

- Client wants full software migration or implementation.
- Client wants Rob to administer software indefinitely.
- Process is unclear and client wants automation anyway.
- Tool access requires sensitive credentials beyond the scoped need.
- Software problem is actually a management compliance or training issue too large for the sprint.

---

# Cross-Category Internal Template List

Engineering should eventually convert these into working Docs/Sheets if Business confirms the delivery direction.

## Audit / Diagnostic Templates

- Office Leak Audit Intake Form
- Lead-to-Payment Workflow Map
- Leak Scoring Sheet
- Top Three Leaks Summary
- Fit / No-Fit Decision Note

## Sprint Templates

- Sprint Scope Sheet
- Client Input Checklist
- Stop Conditions Checklist
- Verification Checklist
- What Changed Summary
- Training / Walkthrough Note
- Follow-Up Check Form

## Leak-Specific Templates

Lead Leak:
- Lead Source Inventory
- Lead Tracker
- Missed-Call Review Checklist
- Estimate Follow-Up Tracker
- Daily Lead Review Checklist

Scheduling / Dispatch Leak:
- Scheduling Intake Map
- Dispatch Notes Checklist
- Daily Schedule Review Checklist
- Job Change Rule
- Callback/Warranty Tracker

Paperwork / Job-Notes Leak:
- Complete Job Record Definition
- Job Packet Checklist
- File Naming Guide
- Scan/Upload Routine
- Missing Notes Tracker

Invoice-to-Cash Leak:
- Billing Trigger Map
- Billing Readiness Checklist
- Completed-But-Not-Billed Tracker
- Unpaid Invoice Tracker
- Weekly AR Review Checklist
- Payment Reminder Template

Owner Bottleneck Leak:
- Owner Interruption Inventory
- Owner Logic Capture Sheet
- FAQ Template
- Decision Rule Template
- Escalation Rule Template
- Recurring Task Checklist

Software / Habit Leak:
- Tool Inventory
- Source-of-Truth Confusion Map
- Existing-Tool Usage Rule
- Quick Reference Guide
- Weekly Tool Cleanup Checklist
- Minimum Viable Workflow Map

# Recommended Next Engineering Step

Do not create every template at once.

Suggested first template batch:

1. Sprint Scope Sheet
2. Verification Checklist
3. What Changed Summary
4. Lead-to-Payment Workflow Map
5. Leak Scoring Sheet
6. Client Input Checklist

These are cross-category and would support all six leak types.

After those exist, choose one first-market leak category and build its specific templates.

# Productization Signal

If these playbooks survive real client use, they may become the service-side foundation for future PennyOS primitives:

- Workflow state engine
- Open-loop register
- Checklist/SOP generator
- Client workspace generator
- Follow-up reminder engine
- Verification ledger
- Leak scoring/routing assistant

But for now: service method first, software later.
