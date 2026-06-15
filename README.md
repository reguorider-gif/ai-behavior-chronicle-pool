# AI Behavior Chronicle Pool

This repository is a working snapshot of a World Cup AI prediction pool. It is not only a prediction dashboard. The intended product direction is an AI behavior chronicle system: models make forecasts and investment decisions under rank, credit, loan, survival, and result pressure; the system records their decisions, settles outcomes, and preserves behavior trails for later analysis.

All points and loans are simulated game data. This project is for model-behavior research and product prototyping only. It is not financial advice, gambling advice, or a real-money betting system.

## What This System Does

The current game loop is:

1. Sync schedule, odds, and match results.
2. Build a prompt pack for each AI seat.
3. Ask each model to forecast all required matches.
4. Ask each model to choose investment actions: `bet` or `no_bet`.
5. Validate model receipts with strict gates.
6. Split forecast receipts from investment receipts.
7. Apply settlement, loan repayment, credit changes, and survival constraints.
8. Write per-seat journals and a god ledger.
9. Generate observer and god-view reports.
10. Publish data to the frontend/API.

The long-term product idea is to evolve this into a digital chronicle of AI behavior: raw events become behavior patterns, patterns become reusable lessons, and lessons are injected into future prompts.

## Core Game Rules

Current rule version:

```text
PRED_INVEST_CREDIT_SURVIVE_V2
```

Key rules:

- Every active seat must forecast every required match.
- Investment actions are separated from predictions.
- `no_bet` is a legal action when justified.
- Loans are allowed, but credit score and net worth constrain loan limits.
- Loan repayment and interest are applied before ranking.
- Recovery Mode activates when net worth falls below the threshold.
- Recovery Mode limits new risk, high odds exposure, and new leverage.
- A round is not fully complete unless every required seat passes the quality gate.

## Seats

The current active pool has 12 seats:

```text
chatgpt, deepseek, doubao, gemini, grok, kimi, meta, mimo, minimax, qwen, wenxin, yuanbao
```

The system intentionally keeps unavailable or incomplete seats visible. A missing or blocked seat should not be hidden behind a "complete" badge.

## Directory Map

```text
api/
  match-dates.js                # Vercel API: date index derived from match data
  pool-meta.js                  # Vercel API: rules, behavior summary, journals, credit, reports
  pool/[...path].js             # Legacy/catch-all pool API handler

pool-app-live-repair/
  index.html                    # Current production frontend snapshot
  commentary-log.html           # God-view / observer commentary page
  ops-v2.html                   # V2 operations acceptance surface
  api/                          # Vercel edge API snapshot used by the frontend
  vercel.json                   # Deployment routing config

ops/
  generate_pred_invest_prompt_pack.py
  submit_pred_invest_bridge_run.py
  run_pred_invest_daily_sop.py
  sync_pred_invest_scores.py
  generate_observer_ledger.py
  audit_pred_invest_product_health.py
  pool/
    behavior_journal.py
    credit_engine.py
    god_report_v2.py
    prompt_context_builder.py
    rules_engine.py
    survival_engine.py

data/pool/
  rules/                        # Rule versions
  forecast_receipts/            # Forecast-only receipts
  investment_receipts/          # Investment-only receipts
  credit_ledger/                # Credit score and loan terms by run
  survival_ledger/              # Recovery/survival state by run
  settlements/                  # Settlement and account updates
  seat_journals/                # Per-seat behavior event journals
  god_ledger/                   # Global event ledger
  god_reports/                  # God-view report artifacts
  observer_ledgers/             # Third-party commentary / observer reports
  prompt_contexts/              # Prompt context snapshots per seat
  pred_invest/                  # Prompt packs, current-game artifacts, SOP outputs
  match_results/                # Score sync and known score registries

tests/
  pool/                         # Engine-level tests
  test_*.py                     # API/data/SOP contract tests
```

## Daily SOP

Primary current runner:

```bash
python3 ops/run_pred_invest_daily_sop.py \
  --date 2026-06-15 \
  --round run-15 \
  --write
```

Important outputs:

```text
data/pool/behavior_summary/latest.json
data/pool/forecast_receipts/<run>.json
data/pool/investment_receipts/<run>.json
data/pool/credit_ledger/<run>.json
data/pool/survival_ledger/<run>.json
data/pool/god_ledger/runs/<run>.json
data/pool/god_reports/<date>_<run>.md
data/pool/seat_journals/<seat>/journal.jsonl
data/pool/prompt_contexts/<run>/<seat>.json
```

## Public API Contract

The Vercel API exposes a minimal validation surface:

```text
GET /api/pool/rules/current
GET /api/pool/runs/:runId/behavior-summary
GET /api/pool/seats/:seatId/journal
GET /api/pool/seats/:seatId/credit
GET /api/pool/runs/:runId/god-report
GET /api/pool/runs/:runId/market-snapshot
GET /api/matches
GET /api/match-dates
```

These endpoints are for verifying product readiness and data continuity. They are not meant to expose raw private model traces.

## Current Known Status

At the time of this snapshot:

- Forecast/investment split exists.
- Seat journals exist.
- Credit and survival ledgers exist.
- God ledger has per-seat event records.
- Match scores are partially backfilled into `/api/matches`.
- The main unresolved seat-quality risk is Grok, which can be slow or incomplete.
- The behavior pattern compression layer is not complete yet. That is the next architecture step.

## Next Architecture Step

The next real product step is not more UI. It is a behavior-memory compiler:

```text
seat_journals + settlements
  -> behavior compiler
  -> compiled behavior patterns
  -> reusable lessons
  -> next prompt context injection
```

Planned modules:

```text
ops/pool/behavior_compiler.py
data/pool/behavior_memory/compiled/<seat>.json
data/pool/behavior_patterns/patterns.json
data/pool/behavior_chronicle/runs/<run>.md
```

The key invariant should be:

```text
Raw events are facts.
Patterns are interpretations with source_event_ids.
Prompt injection may only use the seat's own private history.
```

## Tests

Run:

```bash
python3 -m unittest discover -s tests -p 'test*.py'
```

The current source snapshot has contract tests for:

- behavior journal
- prompt context builder
- market snapshot privacy
- rules engine V2
- credit engine
- survival engine
- settlement from matches
- production artifacts

## Secrets

The repository does not include API keys. Odds API access is read from:

```text
THE_ODDS_API_KEY
ODDS_API_KEY
~/.config/ai-judge/the_odds_api_key
```

Do not commit live provider credentials.
