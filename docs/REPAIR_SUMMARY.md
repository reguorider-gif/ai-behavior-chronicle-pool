# Repair Summary

Date: 2026-06-17

## Scope

This repair pass closed the structural cleanup requested for the current repository snapshot:

1. converged the production frontend to root `index.html`;
2. deprecated the old `pool-app-live-repair/` working copy;
3. fixed fallback API origins;
4. consolidated local proxy diagnostics;
5. merged scattered local SOP notes;
6. moved bulky rerun/debug artifacts out of active product data;
7. documented frontend structure, API contracts, data lifecycle, and deployment rules.
8. added the automated SOP facade and behavior chronicle compiler layer.
9. centralized repeated HTTP/local-proxy utilities and hardened JSON reads.
10. moved credit delta and privacy checks into auditable rule/contract logic.

## Changes

### Frontend Authority

- Copied the production SPA entry from the legacy repair folder to root `index.html`.
- Copied `commentary-log.html` and `ops-v2.html` to the root deployment surface.
- Copied `api/matches.js` to the root `api/` directory.
- Updated `vercel.json` so `/`, `/index.html`, `/commentary-log.html`, and `/ops-v2.html` resolve to root files.
- Renamed `pool-app-live-repair/` to `pool-app-live-repair.DEPRECATED/`.
- Added `pool-app-live-repair.DEPRECATED/DEPRECATED.md`.

### API Fallback

- Replaced the obsolete hardcoded preview origin in:
  - `api/pool-meta.js`
  - `api/pool/[...path].js`
- Both now use:

```text
process.env.POOL_FALLBACK_ORIGIN || "https://pool-app-one.vercel.app"
```

### Proxy Diagnostics

- Added `ops/fixes/proxy_diagnostic_and_fix.sh`.
- Added `ops/fixes/README.md`.
- The helper supports `diagnose`, `fix-local`, `fix-gateway`, and `full`.

### Local SOP Pack

- Consolidated the local AI Judge task-pack notes into:

```text
/Users/audimacmini/Downloads/ai_judge_wealth35_safe_task_pack/SOP.md
```

- Removed the five superseded local note files from that task pack.

### Data Lifecycle

- Created `docs/REPAIR_DIFF_REPORT.md` for root-vs-legacy data comparison.
- Moved bulky rerun/debug artifacts into `data/pool/_archive/`:
  - model output reruns;
  - single-seat rerun attempts;
  - shadow reruns;
  - dry-run artifacts.
- Added `data/pool/_archive/README.md`.
- Updated `.gitignore` so archive payloads are ignored but the archive README remains trackable.
- Kept active `latest_*` pointers in place when used by frontend/API contracts.

### Documentation

- Added `docs/FRONTEND_STRUCTURE.md`.
- Added `docs/API_CONTRACT.md`.
- Added `docs/CODE_MAP.md`.
- Updated `README.md` with:
  - current directory map;
  - data lifecycle;
  - deployment fallback policy;
  - known residual risks;
  - next architecture step.
- Updated `docs/SYSTEM_ARCHITECTURE.md` to point to root `index.html`.

### Stage 1 Code Quality Repairs

- Added shared HTTP/local proxy helpers in `ops/pool/io_utils.py`:
  - `http_json()`;
  - `is_local_url()`;
  - `local_subprocess_env()`;
  - safe `read_json()` fallback for missing or malformed files.
- Removed duplicated `_http_json` / `_is_local_url` implementations from the bridge/SOP scripts.
- Replaced the hardcoded local AI Judge Python path in `ops/run_pred_invest_single_seat_reruns.py` with `AI_JUDGE_PYTHON` or `sys.executable`.
- Added `@lru_cache` to `load_rule_version()` in `ops/pool/rules_engine.py`.
- Expanded `validate_no_cross_seat_leakage()` so prompt context scans all nested identity-bearing fields, not just `private_context`.
- Moved credit forecast delta values into `data/pool/rules/PRED_INVEST_CREDIT_SURVIVE_V2.json`:
  - correct forecast: `+10`;
  - wrong forecast: `-10`;
  - insufficient-info penalty: `-2`.
- Optimized credit ledger historical scans so all historical deltas are read once per ledger write instead of once per seat.
- Hardened `ops/pred_invest_quality_gate.py` JSON reads so corrupt/missing artifacts do not crash the gate.

### Automation And Chronicle Repairs

- `ops/fetch_odds.py` now exposes a stable `OddsFetcher` facade for:
  - schedule candidates;
  - market board / prompt-pack odds;
  - verified score sync;
  - structured missing-odds diagnostics.
- `ops/dispatch_seats.py` keeps the existing single-seat dispatch/retry behavior and writes auditable dispatch receipts.
- `ops/auto_sop.py` supports both old positional phases and the new `--phase/--dry-run` contract. It coordinates:
  - market and score sync;
  - optional bridge dispatch;
  - daily SOP gate;
  - settlement trigger;
  - behavior artifacts.
- Prompt-pack dry-runs no longer write `prompt_contexts/` or `market_snapshots/`; only explicit `--write` produces persistent artifacts.
- `ops/pool/pattern_compiler.py` adds independently testable pattern compression:
  - home bias;
  - loss chasing;
  - confidence miscalibration;
  - no-bet discipline;
  - loan dependency.
- `ops/pool/chronicle_compiler.py` turns patterns into reusable lessons and prompt injections:
  - `data/pool/behavior_chronicle/<seat>/lessons.json`;
  - `data/pool/behavior_chronicle/<seat>/chronicle.md`;
  - `data/pool/behavior_chronicle/runs/<run_id>.md`.
- `ops/pool/prompt_context_builder.py` now injects each seat's behavior chronicle into its private prompt context when available.
- `ops/run_pred_invest_daily_sop.py` now compiles behavior patterns and chronicle lessons after behavior memory, and includes their counts/artifact refs in `behavior_summary`.
- `ops/cron_setup.sh` provides a conservative cron/launchd-friendly command wrapper around `ops/auto_sop.py`.

## Verification

Verification commands run during the repair:

```bash
python3 -m unittest discover -s tests -p 'test*.py'
python3 -m unittest tests.test_io_utils_contract tests.pool.test_pattern_compiler tests.pool.test_chronicle_compiler -v
python3 -m unittest tests.pool.test_credit_engine tests.pool.test_prompt_context_builder tests.pool.test_rules_engine_v2 tests.pool.test_pred_invest_residual_risks tests.test_pred_invest_production_artifacts -v
python3 ops/fetch_odds.py --date 2026-06-17 --run-id dry-run-contract --sync market
python3 ops/auto_sop.py --date 2026-06-17 --round dry-run-contract --phase pre --dry-run
test ! -e data/pool/prompt_contexts/dry-run-contract-2 && test ! -e data/pool/market_snapshots/2026-06-17_dry-run-contract-2.json && echo dry_run_no_artifact_write_ok
bash ops/fixes/proxy_diagnostic_and_fix.sh diagnose
find data/pool -path 'data/pool/_archive' -prune -o \( -name '*attempt*_single_seat_reruns*' -o -name '*shadow_rerun*' -o -name '*dry_run*' \) -print
rg -n "pool-app-live-repair/|pool-app-live-repair\\.DEPRECATED|POOL_FALLBACK_ORIGIN|data/pool/_archive" README.md docs .gitignore vercel.json api tests index.html
rg -n "def _http_json|def _is_local_url|RUNTIME_PYTHON = Path\\(\"/Users|change = 12"
```

Expected active-data exception:

```text
data/pool/pred_invest/latest_shadow_rerun.json
data/pool/pred_invest/latest_shadow_rerun.md
```

Those files are retained as active `latest_*` pointers and are not archive drift.

## Residual Risks

- The frontend remains a large static single-file SPA. The next frontend step is module extraction, not another parallel repair folder.
- The behavior compiler and civilization projections have artifacts, but long-run causal compression still needs future-game evidence.
- Some provider receipts may still omit explicit `memory_used`; bridge prompts should keep requiring this field.
- The new `ops/auto_sop.py` facade is intentionally conservative; real bridge dispatch still requires `--dispatch` so dry-run and preflight can be tested without accidental submissions.
- Local proxy/DNS instability can still make local Vercel `curl` checks flaky. Use `ops/fixes/proxy_diagnostic_and_fix.sh diagnose` before treating local failures as deployment failures.
- `reference_market_seed` is still a labeled fallback board. It prevents 0/12 no-market rounds, but should be replaced by provider odds whenever match mapping succeeds.
