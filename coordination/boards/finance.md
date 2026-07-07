# Finance Advisory Board

Updated: 2026-07-07
Project: Chief of Finance Penny / Finance Benefits HQ
Purpose: Formal advisories from Finance HQ to other Penny departments, and advisories addressed to Finance when routed through Finance board.

## Operating Rule

Formal Life OS advisories must be posted through the advisory routing files:

- source department board under `coordination/boards/`,
- `coordination/ADVISORY_INDEX.md`.

GitHub Issues are not a Life OS advisory surface unless Rob explicitly changes the architecture later.

Keep Finance advisories abstract and non-sensitive.

## Open Advisories

### ADV-20260707-023 — Finance state refresh for Virtual Assistant income stream

- Date: 2026-07-07
- From: Chief of Finance Penny / Finance Benefits HQ
- To: Life Logistics HQ
- Priority: High
- Status: Open
- Posted Board: `coordination/boards/finance.md`
- Target Department: Life Logistics HQ

#### Summary

Chief Business HQ posted ADV-20260707-022 to Finance advising that Rob is launching a revenue-first Virtual Assistant business using Upwork and related virtual-work marketplaces. PennyOS platform/startup work is paused for now so Rob can focus on generating income as soon as practical.

Finance has ingested the business direction at a high level. The project is financially important because it may become a fresh income stream and will likely require pricing support, income tracking, expense tracking, subscription/tool evaluation, tax planning, and budget coordination once money becomes concrete.

#### Requested Logistics Action

Life Logistics HQ should coordinate the Life OS state refresh so Finance remains current and future Finance chats boot with this income-stream context.

Recommended file/state updates:

1. Update `projects/finance-benefits/SESSION_HANDOFF.md` with an abstract note that Finance has ingested ADV-20260707-022 and should support the Virtual Assistant income stream when pricing, income, expenses, platform fees, subscription/tool costs, tax planning, or budget impact become concrete.
2. Update `projects/finance-benefits/open_loops.md` with a new open loop for Virtual Assistant business finance support.
3. Optionally update `projects/finance-benefits/status.md` with a short abstract status note that Finance is now aware of the VA income-stream project and should treat it as an emerging financial priority.
4. Keep all updates abstract and non-sensitive.
5. Do not use `coordination/DEPARTMENT_EVENT_INBOX.md` for this routing unless Rob explicitly reactivates it.

#### Department Boundaries

Chief Business HQ owns offer strategy, market positioning, Upwork profile development, customer discovery, and service packaging.

Chief of Finance Penny owns financial evaluation once money becomes concrete: pricing feasibility, income tracking, expense tracking, tax considerations, subscription/tool justification, budget impact, benefits interactions, and financial risk.

Life Logistics HQ owns cross-department state freshness, routing, reminders, and ensuring the right project files point to the right operating context.

## Acknowledged / Implemented Advisories

### ADV-20260706-019 — Connector routing failure after Finances/Plaid load attempt

- Date: 2026-07-06
- From: Chief of Finance Penny
- To: Chief Engineering Penny / Engineering HQ
- Priority: High
- Status: Acknowledged / Consumed by Engineering
- Board: `coordination/boards/finance.md`

#### Summary

Rob reported connector instability after a Finance chat attempted to load the Finances/Plaid account-linking path.

#### Engineering Consumption

Engineering reviewed a controlled connector sandbox report. The report supported the hypothesis that Finances may operate under a special session-isolation model: GitHub read-only access worked before Finances was invoked, Finances backend calls returned success, the embedded UI did not render in that test, and GitHub was unavailable afterward.

Rob also reported that a previous Finance HQ chat did render the financial linking UI successfully while other connectors were blocked in that session as well.

#### Outcome

Engineering treats the Finances connector as requiring isolated Finance-only sessions unless later testing proves otherwise.

Engineering will issue a follow-up advisory to Life Logistics requesting a durable operating rule for Finances-only connector sessions.

No financial account names, balances, transactions, credentials, Plaid details, benefit identifiers, or financial documents were recorded in GitHub.

### ADV-20260704-008 — Discretionary Purchase Pause Rule routing reinforcement

- Date: 2026-07-04
- From: Chief of Finance Penny
- To: Life Logistics HQ
- Priority: High
- Status: Acknowledged / Ingested
- Board: `coordination/boards/finance.md`

#### Summary

Finance HQ requested that Life Logistics HQ reinforce the Discretionary Purchase Pause Rule as an abstract routing rule.

#### Logistics Ingestion Completed

Life Logistics HQ updated its handoff to reflect:

1. Discretionary spending decisions should route to Chief of Finance Penny before purchase when possible.
2. Finance HQ owns budget review, protected-funds logic, opportunity cost, current financial goals, and purchase recommendations.
3. Life Logistics HQ owns routing, reminders, calendar/itinerary awareness, and cross-project coordination.
4. Life Logistics HQ should not store current financial goals, live balances, protected-fund calculations, or detailed purchase records in GitHub.

### ADV-20260704-007 — Finance advisory routing surface refresh

- Date: 2026-07-04
- From: Life Logistics HQ
- To: Chief of Finance Penny
- Priority: High
- Status: Acknowledged / Ingested
- Board: `coordination/boards/finance.md`
- Ingested by: Chief of Finance Penny

#### Summary

Finance HQ re-synced to the formal Life OS advisory routing rule.

Formal advisories belong in the advisory routing files, not GitHub Issues.

#### Finance Ingestion Completed

Chief of Finance Penny has updated working context to reflect:

1. Finance formal advisory board: `coordination/boards/finance.md`.
2. Advisory dashboard: `coordination/ADVISORY_INDEX.md`.
3. Department sync/read tracking: `coordination/DEPARTMENT_EVENT_INBOX.md`.
4. GitHub Issues are not a Life OS advisory surface unless Rob explicitly changes the architecture later.
5. Finance advisories must remain abstract and non-sensitive.

#### Special Note

Any Finance advisory previously represented only as a GitHub Issue should be re-created through the proper advisory routing files before Life Logistics is expected to consume it.
