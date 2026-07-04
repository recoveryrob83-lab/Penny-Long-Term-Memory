# Life OS Infrastructure Advisory Board

Updated: 2026-07-04
Purpose: Advisories from Life OS Infrastructure / Life Logistics HQ to all Penny departments.

## Open Advisories

None.

## Acknowledged / Implemented Advisories

### ADV-20260704-010 — Decision Rules Registry and Role Drift Check architecture adopted

- Date: 2026-07-04
- From: Life Logistics HQ / Life OS Infrastructure
- To: All Departments
- Priority: High
- Status: Acknowledged / Ingested
- Related Project(s): Life OS, all HQs, Finance, Engineering, Business, Main Assistant, Wellness, Recovery, Job Search, Caregiver, Philosophy
- Source Location:
  - `coordination/DECISION_RULES_REGISTRY.md`
  - `memory/03_OPERATIONAL_RULES.md`
- Target Board: `coordination/boards/life-os.md`

#### Summary

Life OS adopted two related architecture standards for all departments:

1. Decision Rules Registry.
2. Role Drift Check.

Decision Rules are reusable decision procedures for important choices. They route significant decisions to the department that owns the relevant evaluation and require that department to return a structured recommendation.

Role Drift Check is a gentle department-boundary safeguard. When a Penny HQ detects that Rob is asking for work that appears outside that HQ's assigned domain, it should pause gently and ask whether the discussion belongs in that HQ.

#### Outcome

All boards reported ADV-20260704-010 read and ingested.

Departments should recognize:

- Central decision rules registry: `coordination/DECISION_RULES_REGISTRY.md`.
- Department-owned decision rules may live at `projects/<department-folder>/DECISION_RULES.md`.
- Role Drift Check lives in global Operating Rules: `memory/03_OPERATIONAL_RULES.md`.
- First active Finance rule file: `projects/finance-benefits/DECISION_RULES.md`.

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