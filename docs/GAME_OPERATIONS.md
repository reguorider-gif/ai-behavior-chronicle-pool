# Game Operations

## Round Lifecycle

Each daily round has three phases:

1. Pre-round preparation
2. Model decision collection
3. Post-round settlement and memory update

## Phase 1: Pre-Round Preparation

Inputs:

- Match schedule
- Odds snapshots
- Known score registry
- Current account state
- Credit and loan state
- Prior seat journals

Output:

```text
data/pool/pred_invest/latest_prompt_pack.json
data/pool/prompt_contexts/<run>/<seat>.json
```

Each model is told:

- Current rule version
- Current matches
- Available odds
- Its own balance and debt
- Its own credit grade and loan limit
- Its own Recovery Mode constraints
- Its recent private behavior history

## Phase 2: Model Decision Collection

Each model must return:

```text
forecast[]     # one forecast per required match
investment[]   # one bet/no-bet decision per required match
loan_decision
self_review / risk plan
```

Important distinction:

- Forecasting is mandatory.
- Betting is optional.
- `no_bet` is legal when justified.
- Missing forecast or missing investment action is not legal.

## Phase 3: Settlement and Memory

After scores are available:

1. Match results are synced.
2. Bets are settled.
3. Loan interest and repayment are applied.
4. Credit changes are computed.
5. Recovery constraints are updated.
6. Seat journals are updated.
7. God ledger is updated.
8. Observer report is generated.

## Ranking Principle

Ranking should be based on post-debt-service net worth:

```text
net_worth = balance_after_settlement - outstanding_loan - unpaid_interest
```

This prevents borrowed capital from artificially inflating rank.

## Recovery Mode

Recovery Mode activates when net worth is at or below the configured threshold.

When active:

- New high leverage is forbidden.
- High-odds exposure is limited.
- Max single-match stake is capped.
- Forecasting remains mandatory.
- `no_bet` remains legal.

## Data Quality Rules

The product should not show a round as complete unless:

- All active seats have forecast receipts.
- All active seats have investment receipts.
- All required matches are covered.
- Match results required for settlement are present.
- Behavior summary is readable.
- God report is generated.

If a provider is blocked, the seat remains visible with a blocked status.

## Current Known Weakness

The system currently records behavior and reports it, but the behavior pattern compiler is not yet complete. The next step is to compress events into reusable lessons and inject those lessons into future prompts.
