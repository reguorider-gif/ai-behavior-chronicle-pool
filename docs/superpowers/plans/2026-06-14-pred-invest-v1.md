# PRED-INVEST v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the World Cup AI pool SOP from forced betting into a three-ledger game: forecast, investment, and credit.

**Architecture:** Add a deterministic rule engine that computes credit grade, loan limits, interest, stake caps, and prompt requirements from the same contract. Add a prompt-pack generator for daily AI Judge runs and a shadow rerun tool that converts existing/latest structured data into a PRED-INVEST v1 audit report without inventing model answers.

**Tech Stack:** Python standard library, existing pool API endpoints on `pool-app-one.vercel.app`, local JSON/Markdown artifacts under `data/pool/pred_invest`.

---

### Task 1: Rule Contract

**Files:**
- Create: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/ops/pred_invest_rules.py`

- [x] Define `PRED_INVEST_V1` constants for forecast/investment/credit ledgers.
- [x] Implement credit grade and base interest rate mapping.
- [x] Implement `net_worth = balance_gp - loan_gp - accrued_interest_gp`.
- [x] Implement loan limit by credit grade.
- [x] Implement odds-based stake caps.
- [x] Implement risk surcharge rules.
- [x] Implement daily prompt text shared by all models.

### Task 2: Daily Prompt Pack

**Files:**
- Create: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/ops/generate_pred_invest_prompt_pack.py`

- [x] Fetch runtime summary for the requested date/round.
- [x] Build one prompt per active model.
- [x] Require every model to forecast every listed match.
- [x] Allow `no_bet` when edge is absent.
- [x] Require investment fields only when `action=bet`.
- [x] Write JSON and Markdown artifacts.

### Task 3: Shadow Rerun

**Files:**
- Create: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/ops/run_pred_invest_shadow.py`

- [x] Fetch runtime summary and current/latest receipts if available.
- [x] Re-score existing structured bets under PRED-INVEST v1.
- [x] Identify whether each existing bet would be allowed, capped, warned, or rejected.
- [x] Produce latest betting-method report with credit/loan interpretation.
- [x] Write JSON and Markdown artifacts.

### Task 4: Verification

**Commands:**
- [x] `python3 -m py_compile ops/pred_invest_rules.py ops/generate_pred_invest_prompt_pack.py ops/run_pred_invest_shadow.py`
- [x] `python3 ops/generate_pred_invest_prompt_pack.py --date 2026-06-14 --round run-13 --write`
- [x] `python3 ops/run_pred_invest_shadow.py --date 2026-06-14 --round run-13 --write`

### Current Known Constraint

The live Vercel backend/frontend source for `pool-app-one.vercel.app` is still not present locally. This plan lands the SOP/rule/prompt/report layer locally and avoids overwriting production from stale static HTML.
