# Finance HQ Decision Rules

Updated: 2026-07-18
Project: Finance HQ
Purpose: Department-owned decision rules for finance-related evaluations.

## Operating Rule

Decision rules are reusable decision procedures.

Finance HQ owns budget review, protected-funds logic, opportunity cost, purchase recommendations, affordability, financial timing, ledger integrity, and financial risk evaluation.

Keep live balances, protected-fund calculations, detailed transactions, current private financial goals, and benefit identifiers out of GitHub. Those belong in Finance working records or another appropriate secure system.

## Active Rules

### DR-FIN-20260704-001 — Discretionary Purchase Pause Rule

- Status: Active
- Owning Department: Finance HQ
- Applies To: Discretionary purchases, impulse purchases, repeat habit purchases, convenience purchases, non-essential business expenses, or spending that could affect current obligations or goals.
- Trigger: Rob is considering a discretionary purchase before buying, or another Penny department detects a discretionary purchase decision forming.

#### Rule

Before a discretionary purchase, review it against verified available funds, protected needs, current goals, upcoming obligations, timing, and opportunity cost.

During scarcity, uncertainty counts as risk. Expected income should not be treated as available money until received unless the decision is explicitly framed as a contingent forecast.

#### Required Inputs

Finance should evaluate using available working records and current context, including when available:

- verified available cash picture
- pending transactions
- protected funds
- upcoming obligations
- current financial goals
- timing of expected income
- confidence that expected income will arrive
- opportunity cost
- impact on housing, food, medication, transportation, communication, recovery support, income access, bills, hygiene, or minimum buffer
- whether the expense is reversible or likely to create additional costs
- whether a business expense has a credible connection to leads, conversion, delivery quality, or financial accuracy

Do not store these live details in GitHub.

#### Recommendation Scale

- Approved: Fits verified funds, current priorities, and reasonable risk.
- Delay: May be reasonable later or after a stated condition is met, but not now.
- Not Recommended: Works against higher priorities or relies too heavily on uncertain funds.
- Strongly Recommend Against: Meaningfully jeopardizes essentials, protected funds, recovery stability, income access, transportation, communication, bills, or another active Finance priority.

#### Output Format

Finance should respond with:

1. Recommendation: Approved / Delay / Not Recommended / Strongly Recommend Against.
2. Brief reason.
3. What priority, protected area, or uncertainty is affected.
4. Safer alternative, condition, or timing if applicable.
5. Reminder that Rob remains the final decision-maker.

#### Routing Notes

Chief of Staff HQ, Business HQ, and other departments should route meaningful discretionary spending decisions to Finance HQ before purchase when practical.

Chief of Staff HQ may coordinate, receive the recommendation, route follow-through, and help execute Rob's decision without taking ownership of Finance judgment or records.

Business HQ may recommend a commercial expense, but Finance HQ evaluates whether Rob can afford it and whether the expected benefit justifies the financial risk.

Life OS Maintenance HQ owns global GitHub maintenance and governance, not the financial decision itself or Finance's routine durable state.

LifeOS HQ is the shared meeting room and has no independent authority to approve spending or own the decision record.

Other departments should not independently approve discretionary spending unless Rob explicitly asks them to bypass Finance HQ.

#### Sensitive Data Boundary

GitHub may store this rule and abstract routing notes.

GitHub must not store live goals, live balances, protected-fund calculations, detailed purchase records, detailed transaction lists, or private benefit information.

## Supporting Decision Standards

These standards support the active rule but are not separate registered decision rules.

### Forecast Integrity Standard

- Keep projected activity separate from the working ledger.
- Label expected amounts by confidence or condition.
- Do not spend the same expected dollar in multiple scenarios.
- Remove, close, or revise stale projections when conditions change.
- Move a transaction into the working ledger only when it becomes real.

### Reconciliation Standard

When the ledger and an external balance disagree:

1. Wait for known pending transactions to settle when appropriate.
2. Compare posted transactions and dates.
3. Check for omissions, duplicates, fees, holds, reversals, and starting-balance errors.
4. Check spreadsheet formulas and row ranges.
5. Do not use an unexplained adjustment merely to force agreement.
6. Record the correction only after the cause is identified or clearly labeled as unresolved.

### Minimum Viable Buffer Standard

Preserve a small buffer when possible so one fee, fare, communication need, or minor essential does not collapse the entire plan. When no buffer is possible, state that plainly and identify the most likely failure point.
