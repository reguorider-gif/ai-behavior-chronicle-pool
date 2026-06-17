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

The current active pool has 12 required seats:

```text
chatgpt, deepseek, doubao, gemini, grok, kimi, meta, mimo, minimax, qwen, wenxin, yuanbao
```

The system intentionally keeps unavailable or incomplete required seats visible. A missing or blocked required seat should not be hidden behind a "complete" badge. `xunfei` can still be used as an AI Judge extension seat, but it is not part of the World Cup prediction pool hard gate.

## Directory Map

```text
api/
  match-dates.js                # Vercel API: date index derived from match data
  matches.js                    # Vercel API: match registry, scores, and market merge
  pool-meta.js                  # Vercel API: rules, behavior summary, journals, credit, reports
  pool/[...path].js             # Legacy/catch-all pool API handler
  behavior/                     # Product-facing behavior projections
  civilization/                 # Civilization / behavior-map projections

index.html                      # Production SPA entry served at /
commentary-log.html             # God-view / observer commentary page
ops-v2.html                     # V2 operations acceptance surface
vercel.json                     # Deployment routing config

pool-app-live-repair.DEPRECATED/
  DEPRECATED.md                 # Historical frontend snapshot only; do not edit for product work

ops/
  fixes/
    proxy_diagnostic_and_fix.sh # Local proxy/Vercel network diagnostic helper
    README.md
  auto_sop.py                   # Pre/post orchestration facade
  fetch_odds.py                 # Schedule, odds, and score sync wrapper
  dispatch_seats.py             # Local AI Judge seat dispatcher
  cron_setup.sh                 # Cron preview/installer for SOP phases
  generate_pred_invest_prompt_pack.py
  submit_pred_invest_bridge_run.py
  run_pred_invest_daily_sop.py
  sync_pred_invest_scores.py
  generate_observer_ledger.py
  audit_pred_invest_product_health.py
  pool/
    audit/
      behavior_audit_engine.py
      decision_tracer.py
      pattern_influence_checker.py
      replay_validator.py
      causality_graph_builder.py
    behavior_journal.py
    credit_engine.py
    pattern_compiler.py
    chronicle_compiler.py
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
  behavior_patterns/            # Long-term per-seat behavioral pattern compression
  behavior_chronicle/           # Lessons and run chronicle prompt-injection layer
  pred_invest/                  # Prompt packs, current-game artifacts, SOP outputs
  match_results/                # Score sync and known score registries
  _archive/                     # Bulky rerun/dry-run/shadow artifacts, excluded from normal product reads

docs/
  API_CONTRACT.md               # Public API surface and fallback policy
  FRONTEND_STRUCTURE.md         # Static SPA structure and migration notes
  REPAIR_DIFF_REPORT.md         # Root-vs-legacy data inventory report
  REPAIR_SUMMARY.md             # Latest structural repair verification summary

tests/
  pool/                         # Engine-level tests
  test_*.py                     # API/data/SOP contract tests
```

## Data Lifecycle

`data/pool/` is the active product data root. Runtime code should read from this root first and should not read from `pool-app-live-repair.DEPRECATED/`.

The active root keeps product artifacts only: rules, forecast receipts, investment receipts, credit/survival ledgers, settlements, seat journals, god ledgers, reports, prompt contexts, current-game artifacts, and score registries.

Bulky development artifacts are moved under `data/pool/_archive/`:

```text
model output reruns
single-seat rerun attempts
shadow reruns
dry-run artifacts
```

Append-only product logs are not truncated during cleanup:

```text
data/pool/seat_journals/
data/pool/god_ledger/
data/pool/credit_ledger/
data/pool/survival_ledger/
data/pool/settlements/
```

The `latest_*` pointers remain in active folders when they are used by the frontend or API.

## Daily SOP

Primary current runner:

```bash
python3 ops/run_pred_invest_daily_sop.py \
  --date 2026-06-15 \
  --round run-15 \
  --write
```

Automation facade:

```bash
python3 ops/auto_sop.py pre --date 2026-06-17 --round run-17 --write
python3 ops/auto_sop.py post --date 2026-06-17 --round run-17 --write
```

Use `python3 ops/auto_sop.py dry-run --date 2026-06-17 --round run-17 --dispatch` to verify bridge payload generation without sending production decisions.

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
data/pool/behavior_patterns/index.json
data/pool/behavior_chronicle/index.json
data/pool/behavior_chronicle/runs/<run>.md
```

## Deployment

Vercel serves the root SPA from `index.html`. The legacy `pool-app-live-repair/` folder has been retired to `pool-app-live-repair.DEPRECATED/` and is retained only for historical comparison.

The API fallback origin is controlled by:

```text
POOL_FALLBACK_ORIGIN
```

If unset, `api/pool-meta.js` and `api/pool/[...path].js` fall back to:

```text
https://pool-app-one.vercel.app
```

This fallback is only for missing legacy pool data. Product data should still be generated into `data/pool/` and served locally by the deployment whenever possible.

## Public API Contract

The Vercel API exposes a minimal validation surface:

```text
GET /api/pool/rules/current
GET /api/pool/runs/:runId/behavior-summary
GET /api/pool/seats/:seatId/journal
GET /api/pool/seats/:seatId/credit
GET /api/pool/runs/:runId/god-report
GET /api/pool/runs/:runId/market-snapshot
GET /api/behavior/home
GET /api/behavior/timeline/:runId
GET /api/behavior/graph/:runId
GET /api/behavior/agents/:runId
GET /api/behavior/datacenter/:runId
GET /api/behavior/production/:runId
GET /api/behavior/audit/:runId
GET /api/behavior/freeze/:runId
GET /api/civilization/state/:runId
GET /api/civilization/freeze/:runId
GET /api/matches
GET /api/match-dates
```

These endpoints are for verifying product readiness and data continuity. They are not meant to expose raw private model traces.

The `/api/behavior/*` endpoints are the product-facing behavior projection. They return behavior summary, timeline lanes, pattern graph, agent profiles, and data-center readiness without local filesystem paths or raw prompt traces.

## Frontend Product Contract

The production UI is a Behavior Civilization interface, not an odds or betting dashboard. The first screen is the Civilization Map: a pressure field + agent space + causality layer + behavior flow. It answers one product question: how agents form a behavioral civilization under economic pressure.

The primary surface is locked to four behavior pages:

```text
1. Civilization Map         # pressure field, agent space, causality, behavior flow
2. Civilization Timeline    # one behavior lane per model
3. Behavior Graph           # top behavior patterns with evidence
4. Agent Profile            # one model's behavior identity and drift
```

Schedule and market data remain a secondary surface. Credit, split receipts, god reports, and raw health checks are only exposed through the Data Center as product summaries. The Data Center must not show local filesystem paths, temporary filenames, or "open source file" style debug actions.

Civilization Map data is generated as a product object:

```text
data/pool/civilization_state/latest.json
data/pool/civilization_freeze/latest.json
GET /api/civilization/state/:runId
GET /api/civilization/freeze/:runId
GET /api/behavior/civilization/:runId
GET /api/behavior/civilizations/:runId
GET /api/behavior/freeze/:runId
GET /api/civilization/battle/:runId
```

The object exposes `pressure`, `agents`, `positions`, `drift`, `archetypes`, `behavior_flow`, and `causality`. It must not expose raw prompts, local filesystem paths, bridge recovery payloads, or temporary file names.

The design-freeze object is the v1.0 production readiness manifest. It binds the production audit, deterministic replay, memory injection, pattern influence, append-only event stream, and Civilization Map UI into one verdict: `PRODUCTION_READY_BEHAVIOR_CIVILIZATION_ENGINE` or `NOT_READY_BEHAVIOR_CIVILIZATION_ENGINE`.

The multi-civilization object upgrades the surface from agent-only observation to `AI Civilization Phase & War Laboratory`:

```text
data/pool/civilization_battle/latest.json
GET /api/civilization/battle/:runId
GET /api/behavior/civilizations/:runId
```

It groups agents into strategy civilizations, computes shared memory, civilization credit, risk profile, survival/performance metrics, pairwise interactions, headline battle, interaction graph, clash view, civilization timeline, drift engine, collapse signals, civilization state vectors, collapse predictions, evolution paths, fate curves, phase-transition states, civilization field projection, war simulations, and meta-strategy reading. It is still a product object: no raw bets, no local paths, no provider transcripts.

The v9 multiverse-civilization physics layer treats civilizations as high-dimensional particles in a coupled universe field:

```text
energy, entropy, tension, cohesion, aggression, fragility, adaptation, memory_depth
```

Those variables feed five product-facing engines:

```text
phase_transition_engine     # Stable / Adaptive / Volatile / Critical / Expansion / Collapse
civilization_field_engine   # x=entropy, y=tension, size=energy, motion=entropy+aggression+fragility
civilization_war_engine     # resource/stability/strategy/collapse-war interactions
war_phase_engine            # war interactions as phase-transition triggers
civilization_meta_layer     # why a civilization shifts phase
memory_dynamics_engine      # compresses history into reusable strategy pressure for the next run
civilization_physics_core   # freezes the state vector, equations, loop, and production-ready verdict
meta_civilization_engine    # clusters civilizations, detects systemic collapse waves, and projects migration paths
civilization_genome_engine  # expresses risk/survival/aggression/memory/adaptation genes
universe_engine             # projects civilizations into a universe field and evolution tree
multiverse_engine           # computes cross-universe coupling, memory field, dominance cluster, and drift timeline
```

The public UI presents this as Civilization Phase Transition, Civilization Field Map, Civilization War Simulation, War Phase Triggers, Civilization Meta Layer, Memory Dynamics, Civilization Physics Lock, Meta-Civilization Layer, Civilization Genome Layer, Universe Civilization Field, and Multiverse Civilization Map. These are abstract behavior-civilization models, not real-world violence, gambling, or financial advice. The physics lock answers the product-readiness question: whether state vector, phase engine, war interaction, collapse prediction, memory dynamics, meta-civilization clustering, genome expression, universe field projection, multiverse coupling, audit, and replay are all present.

The v9 production lock is:

```text
PRODUCTION_READY_MULTIVERSE_CIVILIZATION_PHYSICS_ENGINE
```

The final compact loop is:

```text
EVENTS
  -> STATE UPDATE
  -> MULTIVERSE COUPLING
  -> PHASE TRANSITION
  -> WAR DYNAMICS
  -> COLLAPSE PREDICTION
  -> MEMORY FIELD UPDATE
  -> NEXT UNIVERSE STEP
```

The final multiverse equation is:

```text
dC/dt = Phi(interaction_field, memory_field, economic_constraints, cross_universe_coupling)
```

Its compact equations are product contracts, not scientific claims:

```text
dC/dt = f(pressure, memory, market, interaction_with_other_civilizations)
phase_transition = entropy + tension - cohesion > threshold
collapse_risk = entropy*0.3 + leverage*0.3 + fragility*0.4
interaction(A,B) = A.energy - B.energy + A.aggression - B.cohesion
memory = compress(events); patterns = extract(memory); strategy = update(patterns)
Meta-Civilization = system of civilizations moving through phase space
dC/dt = Phi(external_field, interaction(C_i,C_j), memory_field, economic_constraints)
phenotype = f(genome, environment); stress_high => mutate(risk_gene)
```

## Current Known Status

At the time of this snapshot:

- Forecast/investment split exists.
- Seat journals exist.
- Credit and survival ledgers exist.
- God ledger has per-seat event records.
- Match scores are partially backfilled into `/api/matches`.
- Behavior memory, pattern graph, evolution trace, replay, and production audit artifacts exist.
- `/api/behavior/audit/:runId` exposes the behavior-loop production verdict without local file paths.
- The run-15 production audit checks behavior loop, prompt memory control, pattern participation, pattern-removal sensitivity, deterministic replay, causal trace completeness, credit/loan binding, and UI contract.
- The audit kernel is split into focused modules under `ops/pool/audit/`, so decision tracing, pattern influence, replay validation, and causality graph generation can be tested independently.
- The main residual evidence gap is provider self-report: some model receipts still do not explicitly include `memory_used`, so the audit can prove system-level injection/replay but future bridge runs should continue requiring explicit receipt fields.
- The frontend is now served from root `index.html`, but it is still a large static single-file SPA. The next frontend architecture step is module extraction, not another parallel repair folder.
- Behavior compiler, replay, pattern graph, and civilization projections have product artifacts. The remaining product-quality gap is longitudinal causal compression: proving over multiple future rounds that compressed memory changes model decisions, not merely that memory was injected.
- Local proxy or DNS instability can still make local `curl` checks flaky. Use `ops/fixes/proxy_diagnostic_and_fix.sh diagnose` to separate local network failures from Vercel deployment failures.

## Next Architecture Step

The next real product step is not more UI. It is strengthening provider-side self-report, longitudinal causal compression, and proof that memory changes future decisions:

```text
prompt memory injection
  -> explicit model memory_used receipt
  -> decision delta trace
  -> settlement / credit effect
  -> next-round strategy change proof
```

Planned modules:

```text
strict receipt gate for memory_used
cross-run behavior influence report
provider-specific bridge repair for slow/incomplete seats
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
