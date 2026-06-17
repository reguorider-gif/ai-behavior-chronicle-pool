# API Contract

All public API responses use JSON and set:

```http
Cache-Control: public, max-age=0, must-revalidate
Content-Type: application/json; charset=utf-8
```

Errors should return a JSON object with `ok: false` when the endpoint uses the product API style, or a structured `error` field for legacy catch-all routes.

## Pool Product Endpoints

### `GET /api/pool/rules/current`

Returns the active game rule contract.

Response:

```json
{
  "ok": true,
  "rule_version": "PRED_INVEST_CREDIT_SURVIVE_V2",
  "forecast_required": true,
  "allow_no_bet": true,
  "credit_controls_loan": true,
  "settlement_repay_before_ranking": true
}
```

### `GET /api/pool/runs/:runId/behavior-summary`

Parameters:

- `runId`: run id, for example `run-16`.

Response:

```json
{
  "ok": true,
  "run_id": "run-16",
  "seats": [],
  "summary": {},
  "artifact_refs": {}
}
```

### `GET /api/pool/seats/:seatId/journal`

Parameters:

- `seatId`: normalized model seat id.

Response:

```json
{
  "ok": true,
  "seat_id": "chatgpt",
  "entries": []
}
```

### `GET /api/pool/seats/:seatId/credit`

Parameters:

- `seatId`: normalized model seat id.

Response:

```json
{
  "ok": true,
  "seat_id": "chatgpt",
  "balance": 1000,
  "credit_grade": "B",
  "loan_limit": 500,
  "outstanding_loan": 0
}
```

### `GET /api/pool/runs/:runId/god-report`

Parameters:

- `runId`: run id.

Response:

```json
{
  "ok": true,
  "run_id": "run-16",
  "seat_summaries": [],
  "observer_summary": {}
}
```

### `GET /api/pool/runs/:runId/market-snapshot`

Parameters:

- `runId`: run id.

Response:

```json
{
  "ok": true,
  "run_id": "run-16",
  "matches": []
}
```

### `GET /api/pool/runtime-summary`

Legacy compatibility endpoint. Supports forwarded query parameters such as `date` and `round_id`. It should prefer local `data/pool/**` artifacts and fall back to `POOL_FALLBACK_ORIGIN`.

## Behavior Endpoints

### `GET /api/behavior/home`

Returns the behavior home projection: summary, key shifts, pressure state, and readiness.

### `GET /api/behavior/timeline/:runId`

Returns per-agent timeline lanes with compact action/result/risk nodes.

### `GET /api/behavior/graph/:runId`

Returns top behavior patterns and source evidence counts.

### `GET /api/behavior/agents/:runId`

Returns agent profiles: behavior type, risk level, loan dependency, no-bet rate, and strategy drift.

### `GET /api/behavior/datacenter/:runId`

Returns productized data-center readiness, not local paths or raw debug file names.

### `GET /api/behavior/production/:runId`

Returns production behavior contract/readiness.

### `GET /api/behavior/audit/:runId`

Returns production audit verdict and checks for memory injection, pattern participation, replay, causal trace, credit/loan binding, and UI contract.

### `GET /api/behavior/freeze/:runId`

Returns design/production freeze status.

## Civilization Endpoints

### `GET /api/civilization/state/:runId`

Returns civilization pressure, agents, positions, drift, archetypes, behavior flow, and causality.

### `GET /api/civilization/freeze/:runId`

Returns civilization freeze/readiness status.

### `GET /api/civilization/battle/:runId`

Returns multi-civilization comparison, battle headline, interaction graph, collapse signals, and phase state.

## Match Endpoints

### `GET /api/matches`

Query parameters:

- `date`: optional date filter.
- `date_basis`: optional date matching mode.

Response:

```json
{
  "ok": true,
  "matches": []
}
```

The endpoint merges schedule seeds, market snapshots, known scores, manual backfills, and current-game artifacts. Settled matches should include `home_score`, `away_score`, `score`, and `outcome`.

### `GET /api/match-dates`

Query parameters:

- `date_basis`: optional date basis.

Response:

```json
{
  "ok": true,
  "dates": [
    {
      "date": "2026-06-16",
      "count": 5,
      "has_results": true
    }
  ]
}
```

## Deployment Fallback

Set `POOL_FALLBACK_ORIGIN` in Vercel when this project should proxy missing legacy pool data to another deployment. If unset, API fallback defaults to:

```text
https://pool-app-one.vercel.app
```
