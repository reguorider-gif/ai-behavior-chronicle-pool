# System Architecture

## 1. System Definition

This project is an AI behavior experiment built around football match prediction. The system gives each model a persistent seat, simulated capital, credit constraints, loan rules, and survival pressure. Each round forces the model to make world judgments and resource-allocation choices under uncertainty.

The system has three success dimensions:

1. Prediction Success: did the model judge the world correctly?
2. Capital Success: did the model allocate simulated GP efficiently?
3. Survival Success: did the model avoid ruin, debt traps, and reckless leverage?

These dimensions are not collapsed into a single score. Different models can succeed in different ways.

## 2. Current Data Flow

```text
schedule/odds/scores
  -> prompt pack
  -> model bridge / receipt collection
  -> quality gate
  -> forecast receipts
  -> investment receipts
  -> settlement
  -> credit ledger
  -> survival ledger
  -> seat journals
  -> god ledger
  -> observer/god reports
  -> frontend/API
```

## 3. Existing Layers

### Event Layer

Files:

```text
data/pool/seat_journals/<seat>/journal.jsonl
data/pool/god_ledger/events.jsonl
data/pool/god_ledger/runs/<run>.json
```

Purpose:

- Record raw seat events.
- Preserve global run events.
- Preserve partial or blocked seats instead of hiding them.

### Rules Layer

Files:

```text
data/pool/rules/PRED_INVEST_CREDIT_SURVIVE_V2.json
ops/pool/rules_engine.py
```

Purpose:

- Enforce forecast coverage.
- Enforce investment legality.
- Permit `no_bet` as a valid action.
- Apply Recovery Mode limits.
- Prevent cross-seat private context leakage.

### Account Layer

Files:

```text
ops/pool/credit_engine.py
ops/pool/survival_engine.py
data/pool/credit_ledger/
data/pool/survival_ledger/
data/pool/settlements/
```

Purpose:

- Compute credit grade and loan limit.
- Compute net worth and Recovery Mode.
- Preserve settlement and debt service.

### Prompt Context Layer

Files:

```text
ops/pool/prompt_context_builder.py
data/pool/prompt_contexts/<run>/<seat>.json
```

Purpose:

- Build public match/rule context.
- Inject only the seat's own private state.
- Hide other models' private choices.

### Commentary Layer

Files:

```text
ops/generate_observer_ledger.py
ops/pool/god_report_v2.py
data/pool/observer_ledgers/
data/pool/god_reports/
```

Purpose:

- Produce third-party commentary.
- Explain each model's operation.
- Preserve both pre-match and post-match views.

## 4. Missing Layer: Pattern Compression

The current project records behavior, but it does not yet fully compress behavior into reusable strategy lessons.

Required next layer:

```text
behavior events + settlement outcomes
  -> pattern compression
  -> compiled behavior profile
  -> reusable lessons
  -> prompt injection
```

The compiler should generate evidence-backed claims:

```json
{
  "pattern_id": "chatgpt-low-odds-home-bias",
  "seat_id": "chatgpt",
  "claim": "Seat tends to prefer low-odds favorite positions and avoids uncertain handicap lines.",
  "source_event_ids": ["..."],
  "confidence": 0.72,
  "next_prompt_instruction": "If choosing a high-variance market, explain why this is not a repeat of prior failure."
}
```

## 5. Hard Invariants

- Raw events must be append-only.
- Interpretations must cite source events.
- A model only receives its own private behavior memory.
- `no_bet` must be distinguishable from missing data.
- A partial seat cannot produce a full-completion badge.
- Local data and deployed API must remain in sync.
