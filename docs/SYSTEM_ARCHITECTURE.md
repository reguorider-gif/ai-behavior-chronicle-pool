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

### Behavior Projection Layer

Files:

```text
ops/pool/behavior_compiler.py
ops/pool/behavior_replay.py
ops/pool/memory_injector.py
api/behavior/[...path].js
index.html
```

Purpose:

- Compress journals into behavior memory, pattern graph, agent profiles, and evolution traces.
- Build replay events that reconstruct what an agent knew, remembered, and decided at a point in time.
- Serve product-facing behavior objects through `/api/behavior/*`.
- Keep the public UI focused on behavior changes; schedule, odds, raw ledgers, and prompt traces stay in secondary surfaces.

### Civilization Dynamics Layer

Files:

```text
ops/pool/civilization_state_engine.py
ops/pool/collapse_predictor.py
ops/pool/evolution_engine.py
ops/pool/civilization_competitor.py
ops/pool/phase_transition_engine.py
ops/pool/civilization_field_engine.py
ops/pool/civilization_war_engine.py
ops/pool/war_phase_engine.py
ops/pool/civilization_meta_layer.py
ops/pool/memory_dynamics_engine.py
ops/pool/meta_civilization_engine.py
ops/pool/civilization_genome_engine.py
ops/pool/universe_engine.py
ops/pool/multiverse_engine.py
ops/pool/civilization_physics_core.py
ops/pool/civilization_battle.py
data/pool/civilization_battle/
```

Purpose:

- Group agents into strategy civilizations.
- Project each civilization into a state vector.
- Convert state vectors into physical-style variables: energy, entropy, tension, cohesion, aggression, fragility, adaptation, and memory depth.
- Detect phase states: stable, adaptive, volatile, critical, expansion, or collapse watch.
- Render a civilization field map without exposing raw bets or provider traces.
- Simulate abstract civilization conflict as resource, stability, strategy, or collapse-induction wars.
- Treat war interactions as possible phase-transition triggers.
- Explain why a civilization is stable, adaptive, volatile, critical, expanding, or under collapse watch.
- Compress historical behavior into memory pressure, strategy updates, and next-prompt injection contracts.
- Cluster civilizations into stable, volatile, collapsing, and expansion groups.
- Detect system-wide collapse waves and migration paths between phase clusters.
- Express civilization genomes as risk, survival, aggression, memory, and adaptation genes.
- Project civilizations into a universe field with interaction overlaps and evolution-tree branches.
- Compute multiverse coupling across civilization fields, including memory field, dominance clusters, and cross-universe drift timelines.
- Freeze the final civilization physics contract and expose a production-ready verdict.

This layer is not a real-world war model. It is a product metaphor for strategy-field interactions inside the simulated behavior game.

The final meta formula is intentionally compact:

```text
phase_law_score = entropy*0.3 + tension*0.3 + aggression*0.2 + fragility*0.2 - cohesion*0.2
```

The score is not a scientific claim. It is a deterministic product model for comparing behavior civilizations across runs.

The v9 multiverse-civilization physics contract locks the higher-level loop:

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

The compact production equations are:

```text
dC/dt = f(pressure, memory, market, interaction_with_other_civilizations)
phase_transition = entropy + tension - cohesion > threshold
collapse_risk = entropy*0.3 + leverage*0.3 + fragility*0.4
interaction(A,B) = A.energy - B.energy + A.aggression - B.cohesion
memory = compress(events); patterns = extract(memory); strategy = update(patterns)
Meta-Civilization = clusters(civilizations) + collapse_waves + migration_paths
dC/dt = Phi(external_field, interaction(C_i,C_j), memory_field, economic_constraints)
dC/dt = Phi(interaction_field, memory_field, economic_constraints, cross_universe_coupling)
phenotype = f(genome, environment); stress_high => mutate(risk_gene)
coupling(A,B) = interaction_force(A,B) = field_overlap + phase_pressure + dominance_delta
```

The expected production verdict is:

```text
PRODUCTION_READY_MULTIVERSE_CIVILIZATION_PHYSICS_ENGINE
```

## 4. Missing Layer: Pattern Compression

The current project records behavior and has a first behavior compiler/replay layer. The next maturity step is stronger evidence-backed pattern compression across more settled outcomes.

Required next layer:

```text
behavior events + settlement outcomes
  -> pattern compression
  -> compiled behavior profile
  -> reusable lessons
  -> prompt injection
  -> civilization state/phase/war projection
  -> civilization meta explanation
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
