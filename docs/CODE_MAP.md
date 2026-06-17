# Code Map

This map names the active code paths for the AI Judge behavior chronicle pool. Deprecated repair snapshots are not product entry points.

## Runtime Entrypoints

- `ops/auto_sop.py`: pre-match and post-match orchestration facade.
- `ops/fetch_odds.py`: schedule, odds, and score synchronization wrapper.
- `ops/dispatch_seats.py`: isolated web-seat dispatch wrapper for local AI Judge.
- `ops/run_pred_invest_daily_sop.py`: authoritative daily SOP gate, settlement, behavior memory, chronicle, and production artifact writer.
- `ops/run_pred_invest_single_seat_reruns.py`: targeted rerun executor for invalid or missing seats.
- `ops/submit_pred_invest_bridge_run.py`: AI Judge bridge submission and compact prompt generation.
- `ops/cron_setup.sh`: auditable cron preview/installer for pre/post SOP phases.

## Core Engines

- `ops/pool/io_utils.py`: shared JSON, JSONL, local URL, and HTTP helpers.
- `ops/pool/rules_engine.py`: rule loading and receipt validation.
- `ops/pool/credit_engine.py`: credit delta, score, grade, loan limit, and ledger writing.
- `ops/pool/prompt_context_builder.py`: per-seat prompt context with private account state, behavior memory, and behavior chronicle.
- `ops/pool/behavior_compiler.py`: behavior memory, pattern graph, agent profiles, evolution trace, and civilization projections.
- `ops/pool/pattern_compiler.py`: 12-pattern behavior compiler for long-term model tendency extraction.
- `ops/pool/chronicle_compiler.py`: lessons, prompt injection, and run chronicle generation.
- `ops/pool/behavior_production_kernel.py`: append-only behavior production contract and readiness state.

## Frontend/API

- `index.html`: production static SPA.
- `commentary-log.html`: observer commentary surface.
- `ops-v2.html`: operations acceptance surface.
- `api/pool-meta.js`: product metadata API and fallback proxy.
- `api/pool/[...path].js`: legacy pool catch-all API.
- `api/matches.js`: match, score, and market merge API.
- `api/behavior/[...path].js`: behavior projections.
- `api/civilization/[...path].js`: civilization projections.

## Product Data

- `data/pool/forecast_receipts/`: forecast-only receipts by run.
- `data/pool/investment_receipts/`: investment-only receipts by run.
- `data/pool/credit_ledger/`: credit and loan ledger by run.
- `data/pool/survival_ledger/`: recovery/survival state by run.
- `data/pool/seat_journals/`: append-only per-seat behavior event journals.
- `data/pool/behavior_patterns/`: compiled per-seat pattern payloads and index.
- `data/pool/behavior_chronicle/`: compiled lessons and run chronicle outputs.
- `data/pool/_archive/`: bulky rerun, dry-run, and debug artifacts excluded from normal product reads.

## Test Contracts

- `tests/test_io_utils_contract.py`: shared I/O helper contract.
- `tests/pool/test_pattern_compiler.py`: 12-pattern behavior compiler contract.
- `tests/pool/test_chronicle_compiler.py`: lessons and run chronicle contract.
- `tests/pool/test_prompt_context_builder.py`: prompt context privacy plus memory/chronicle injection.
- `tests/test_frontend_quality_contract.py`: publication-grade frontend structure contract.
