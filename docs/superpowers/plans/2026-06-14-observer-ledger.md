# Observer Ledger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable Observer Ledger that turns each pool round's structured bets, settlement, account state, and seat archives into a third-party matchday commentary report.

**Architecture:** The ledger is a deterministic reporting layer that consumes public/runtime APIs or local pool JSON, writes versioned JSON/Markdown artifacts, and can be called by the daily SOP after bet validation and again after settlement. It does not invent match results, odds, injuries, or model thoughts.

**Tech Stack:** Python 3 standard library, AI Judge pool JSON/API contract, Markdown/JSON output, optional static frontend/API consumption.

---

### Task 1: Observer Ledger Generator

**Files:**
- Create: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/ops/generate_observer_ledger.py`
- Output: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/data/pool/observer_ledgers/*.json`
- Output: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/data/pool/observer_ledgers/*.md`

- [ ] Fetch or read `runtime-summary`, `daily-reports/{date}/{round_id}`, `seat-archives/{round_id}`, and settlement data.
- [ ] Normalize every accepted model into a seat commentary row.
- [ ] Produce three perspectives for every model: data analyst, football expert, pro bettor.
- [ ] Produce deterministic summary fields: headline, lead, match notes, best operation, worst operation, leverage watch, missing-data watch.
- [ ] Write both `{date}_{round_id}_{phase}.json` and `{date}_{round_id}_{phase}.md`, plus `latest.json/md`.

### Task 2: SOP Hook

**Files:**
- Create: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/ops/run_observer_ledger_sop.py`

- [ ] Add a small wrapper that can be scheduled after the daily pipeline.
- [ ] Resolve phase automatically: `post` when settlement is settled, otherwise `pre`.
- [ ] Exit non-zero only for missing critical data: no runtime summary, no seat archive, or zero seat records.

### Task 3: Smoke Test With 2026-06-13 / run-12

**Files:**
- Output: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/data/pool/observer_ledgers/2026-06-13_run-12_post.json`
- Output: `/Users/audimacmini/Documents/Playground/.omx/ai-judge/pool-app/data/pool/observer_ledgers/2026-06-13_run-12_post.md`

- [ ] Run the generator against yesterday's settled `run-12`.
- [ ] Verify 12/12 model commentary rows exist.
- [ ] Verify post-match fields exist because run-12 is settled.
- [ ] Include the smoke excerpt in the user report.

### Task 4: Frontend/API Integration Follow-up

**Files:**
- Current live frontend/API source was not found locally in this session; the live deployment exposes `api/index.py` but the source tree is absent.

- [ ] Once the project source is restored or pulled, expose `/api/pool/observer-ledgers`.
- [ ] Add `observer_ledger` to `runtime-summary`.
- [ ] Add a `战报流水` card to Data Center, showing the latest headline and all 12 model commentary links.
- [ ] Keep the product UI as record/detail view; keep Codex-only god report private.

### Verification

- [ ] `python3 ops/generate_observer_ledger.py --date 2026-06-13 --round run-12 --phase post --write`
- [ ] `python3 ops/run_observer_ledger_sop.py --date 2026-06-13 --round run-12 --write`
- [ ] Inspect generated JSON for `seat_commentaries` length 12 and `phase=post`.
- [ ] Inspect generated Markdown for every model name and the three commentary perspectives.
