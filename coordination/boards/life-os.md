# Life OS Infrastructure Advisory Board

Updated: 2026-07-04
Purpose: Advisories from Life OS Infrastructure / Life Logistics HQ to all Penny departments.

## Open Advisories

### ADV-20260704-010 — Decision Rules Registry and Role Drift Check architecture adopted

- Date: 2026-07-04
- From: Life Logistics HQ / Life OS Infrastructure
- To: All Departments
- Priority: High
- Status: Open
- Related Project(s): Life OS, all HQs, Finance, Engineering, Business, Main Assistant, Wellness, Recovery, Job Search, Caregiver, Philosophy
- Source Location:
  - `coordination/DECISION_RULES_REGISTRY.md`
  - `memory/03_OPERATIONAL_RULES.md`
- Target Board: `coordination/boards/life-os.md`

#### Summary

Life OS has adopted two related architecture standards that all departments should ingest together:

1. Decision Rules Registry.
2. Role Drift Check.

Decision Rules are reusable decision procedures for important choices. They route significant decisions to the department that owns the relevant evaluation and require that department to return a structured recommendation.

Role Drift Check is a gentle department-boundary safeguard. When a Penny HQ detects that Rob is asking for work that appears outside that HQ's assigned domain, it should pause gently and ask whether the discussion belongs in that HQ.

#### Required Department Ingestion

All active Penny departments should update working context to recognize:

1. Central decision rules registry: `coordination/DECISION_RULES_REGISTRY.md`.
2. Department-owned decision rules may live at `projects/<department-folder>/DECISION_RULES.md`.
3. When a department detects that a decision matches a registered rule, it should route the decision to the owning department before acting when practical.
4. The owning department should apply the rule and return the standardized recommendation for that rule.
5. Rob remains the final decision-maker.
6. Sensitive or domain-specific live data stays in the appropriate working system, not in the central registry.
7. Role Drift Check lives in global Operating Rules: `memory/03_OPERATIONAL_RULES.md`.
8. When a department detects work outside its assigned domain, it should gently ask whether that work belongs in the current HQ before continuing.
9. Role Drift Check nudges but does not block. Rob may intentionally keep work in the current HQ when there is a good reason.

#### Role Drift Check Suggested Phrasing

> Rob, are you sure this belongs here? I am [Department Penny], and this sounds like [likely domain or HQ].

Principle:

> Pause at the doorway before moving work into the wrong department.

#### First Active Decision Rule

- DR-FIN-20260704-001 — Discretionary Purchase Pause Rule.
- Owner: Chief of Finance Penny.
- Rule file: `projects/finance-benefits/DECISION_RULES.md`.

Before discretionary purchases, review them against current goals and protected funds.

Recommendation scale:

- Approved
- Delay
- Not Recommended
- Strongly Recommend Against

#### Desired Outcome

Departments should stop improvising important decision evaluations when a registered rule applies.

Instead, route the decision to the owning HQ, apply the rule, and return a structured recommendation.

Departments should also avoid accidentally owning work outside their domain by using Role Drift Check as a gentle doorway pause.

## Acknowledged / Implemented Advisories

### ADV-20260702-001 — Advisory board system created

- Date: 2026-07-02
- From: Life OS Infrastructure
- To: Main Assistant / All Departments
- Priority: Medium
- Status: Acknowledged
- Related Project(s): Life OS Infrastructure, Main Assistant, all project chats
- Source Location: `coordination/README.md`, `coordination/ADVISORY_INDEX.md`, `coordination/template.md`
- Target Board: `coordination/boards/life-os.md`

### Summary

A cross-project advisory board system has been created. Departments can now post durable advisories when one project produces information another project may need.

### Acknowledgement / Outcome

Acknowledged by Main Assistant on 2026-07-02. Main Assistant will include Advisory Reports in full morning and nightly reports and will use `coordination/ADVISORY_INDEX.md` as the advisory dashboard.