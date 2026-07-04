# Decision Rules Registry

Updated: 2026-07-04
Purpose: Central Life OS registry for reusable decision rules that route important choices to the correct Penny department for structured evaluation.

## Status

Active Life OS architecture standard.

## Purpose

Decision Rules are reusable decision procedures.

They help Life OS pause before important choices and route the decision to the department that owns the relevant evaluation.

Decision Rules are not ordinary reminders, open loops, or advisories.

They define:

- what type of decision triggers the rule,
- which department owns the evaluation,
- what inputs the department should check,
- what logic or criteria should be applied,
- what standardized recommendation scale should be returned,
- where sensitive or domain-specific data belongs.

## Core Principle

Important decisions should not be handled by vibes in the moment.

Route the decision to the right department, evaluate it through a predefined rule, and return a structured recommendation.

## Standard Locations

Central registry:

- `coordination/DECISION_RULES_REGISTRY.md`

Department-owned decision rules:

- `projects/<department-folder>/DECISION_RULES.md`

Examples:

- `projects/finance-benefits/DECISION_RULES.md`
- `projects/engineering/DECISION_RULES.md`
- `projects/business-development/DECISION_RULES.md`
- `projects/life-logistics-hq/DECISION_RULES.md`

Create department decision-rule files only when useful.

## Registry Index

| Rule ID | Rule Name | Owning Department | Rule File | Status |
|---|---|---|---|---|
| DR-FIN-20260704-001 | Discretionary Purchase Pause Rule | Chief of Finance Penny | `projects/finance-benefits/DECISION_RULES.md` | Active |

## Standard Rule Template

```markdown
### <Rule ID> — <Rule Name>

- Status:
- Owning Department:
- Applies To:
- Trigger:
- Required Inputs:
- Evaluation Criteria:
- Recommendation Scale:
- Sensitive Data Boundary:
- Output Format:
- Routing Notes:
```

## Recommendation Scales

A rule may define its own recommendation scale when domain-specific language is useful.

Common examples:

- Approved / Delay / Not Recommended / Strongly Recommend Against
- Adopt / Pilot / Defer / Reject
- Proceed / Pause / Escalate / Stop

The owning department should explain what each recommendation means.

## Routing Rule

When a Penny department detects that a decision matches a registered rule, it should route the decision to the owning department before acting when practical.

Rob remains the final decision-maker.

Penny departments provide structured recommendations, not commands.

## Sensitive Data Boundary

Decision Rules may require sensitive or domain-specific data for evaluation.

The registry should store only abstract rule logic.

Live financial details, medical details, credentials, protected identifiers, detailed transactions, or other sensitive records belong in the appropriate working system, not in the central registry.

## Relationship To Other Systems

Decision Rules differ from:

- Advisory Boards: cross-department routing notices.
- Pending Advisory Boards: possible future advisories.
- Department Notebooks: durable idea capture.
- Todoist: Rob-facing tasks.
- Calendar: timed commitments.
- Handoffs/status/open loops: operational continuity.

Decision Rules are reusable evaluation procedures.