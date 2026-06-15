#!/usr/bin/env python3
"""Compatibility runtime-summary adapter for the AI Judge World Cup pool.

The desktop bridge expects a ``pool_data`` module in the pool-app directory.
This project currently stores the repaired PRED-INVEST V2 artifacts under
``data/pool/pred_invest``; this adapter exposes those artifacts through the
runtime-summary contract used by ``/api/worldcup-pool/*``.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PRED_DIR = ROOT / "data" / "pool" / "pred_invest"
POOL_DIR = ROOT / "data" / "pool"


def _detect_latest_date_round() -> tuple[str, str] | None:
    """Return the newest date/run current_game artifact.

    The product SOP is artifact-driven. Hard-coding an old date makes local API
    consumers look stale even after the daily pipeline writes newer bundles.
    """
    if not PRED_DIR.exists():
        return None
    latest: tuple[str, int, str] | None = None
    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})_(run-[0-9]+)_current_game\.json$")
    for path in PRED_DIR.glob("*_run-*_current_game.json"):
        match = pattern.match(path.name)
        if not match:
            continue
        date = match.group(1)
        round_id = match.group(2)
        try:
            run_no = int(round_id.split("-", 1)[1])
        except Exception:
            run_no = -1
        candidate = (date, run_no, round_id)
        if latest is None or candidate > latest:
            latest = candidate
    return (latest[0], latest[2]) if latest else None


_LATEST_ARTIFACT = _detect_latest_date_round()
DEFAULT_DATE = os.environ.get("POOL_ACTIVE_DATE") or (_LATEST_ARTIFACT[0] if _LATEST_ARTIFACT else "2026-06-14")


def _detect_latest_round_id(date: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(date)}_(run-[0-9]+)_current_game\.json$")
    latest: tuple[int, str] | None = None
    if not PRED_DIR.exists():
        return None
    for path in PRED_DIR.glob(f"{date}_run-*_current_game.json"):
        match = pattern.match(path.name)
        if not match:
            continue
        round_id = match.group(1)
        try:
            number = int(round_id.split("-", 1)[1])
        except Exception:
            number = -1
        if latest is None or number > latest[0]:
            latest = (number, round_id)
    return latest[1] if latest else None


ACTIVE_ROUND_ID = (
    os.environ.get("POOL_ACTIVE_ROUND_ID")
    or _detect_latest_round_id(DEFAULT_DATE)
    or (_LATEST_ARTIFACT[1] if _LATEST_ARTIFACT else None)
    or "run-14"
)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_read_error": f"{path.name}: {exc}"}


def _read_pool_json(*parts: str) -> dict[str, Any]:
    return _read_json(POOL_DIR.joinpath(*parts))


def _read_pool_jsonl(*parts: str) -> list[dict[str, Any]]:
    path = POOL_DIR.joinpath(*parts)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def _public_artifact_ref(*parts: str) -> str:
    return "/".join(("data", "pool", *parts))


def _artifact(date: str, round_id: str, suffix: str) -> Path:
    exact = PRED_DIR / f"{date}_{round_id}_{suffix}.json"
    if exact.exists():
        return exact
    latest = PRED_DIR / f"latest_{suffix}.json"
    return latest


def _exact_artifact(date: str, round_id: str, suffix: str) -> Path:
    return PRED_DIR / f"{date}_{round_id}_{suffix}.json"


def _model_to_summary(model: dict[str, Any]) -> dict[str, Any]:
    loan_terms = model.get("loan_terms") if isinstance(model.get("loan_terms"), dict) else {}
    net_worth = loan_terms.get("net_worth_gp")
    loan = loan_terms.get("outstanding_loan_gp")
    balance = (float(net_worth or 0) + float(loan or 0)) if net_worth is not None else None
    return {
        "model_account": model.get("model_account"),
        "seat_id": model.get("model_account"),
        "display_name": model.get("display_name") or model.get("model_account"),
        "rank": model.get("rank"),
        "balance_gp": round(balance, 2) if balance is not None else None,
        "net_worth_gp": net_worth,
        "loan_gp": loan,
        "credit_grade": loan_terms.get("credit_grade"),
        "credit_score": loan_terms.get("credit_score"),
        "bet_count": model.get("bet_count", 0),
        "allowed": model.get("allowed", 0),
        "warned": model.get("warned", 0),
        "rejected": model.get("rejected", 0),
        "required_next_action": model.get("required_next_action"),
    }


def _merge_model_rows(current: dict[str, Any], daily: dict[str, Any], quality: dict[str, Any]) -> list[dict[str, Any]]:
    """Build the authoritative 12-seat account view for runtime consumers.

    ``latest_current_game`` may intentionally contain only valid strict report
    seats (for example 11/12 when Grok is blocked). Ranking and loan displays
    still need a 12-seat account surface that marks missing seats honestly.
    """
    strict_rows = current.get("model_summaries") if isinstance(current.get("model_summaries"), list) else []
    daily_rows = (((daily.get("shadow_rerun") or {}) if isinstance(daily.get("shadow_rerun"), dict) else {}).get("models_detail") or [])
    required = list(quality.get("valid_seats") or [])
    for seat in quality.get("needs_rerun") or []:
        if seat not in required:
            required.append(seat)

    by_account: dict[str, dict[str, Any]] = {}
    for row in daily_rows:
        if not isinstance(row, dict):
            continue
        account = str(row.get("model_account") or row.get("seat_id") or row.get("display_name") or "").lower()
        if account:
            by_account[account] = dict(row)
    for row in strict_rows:
        if not isinstance(row, dict):
            continue
        account = str(row.get("model_account") or row.get("seat") or row.get("display_name") or "").lower()
        if not account:
            continue
        merged = by_account.get(account, {})
        merged.update(
            {
                "model_account": account,
                "display_name": row.get("display_name") or row.get("seat") or merged.get("display_name") or account,
                "bet_count": row.get("bet_count", merged.get("bet_count", 0)),
                "required_next_action": row.get("required_next_action") or merged.get("required_next_action"),
                "strict_valid": True,
            }
        )
        if row.get("loan_terms"):
            merged["loan_terms"] = row.get("loan_terms")
        by_account[account] = merged
    for seat in required:
        account = str(seat).lower()
        by_account.setdefault(
            account,
            {
                "model_account": account,
                "display_name": "xAI Grok" if account == "grok" else account,
                "rank": None,
                "loan_terms": {},
                "bet_count": 0,
                "required_next_action": "needs_targeted_rerun",
                "strict_valid": False,
            },
        )
    rows = list(by_account.values())
    rows.sort(key=lambda row: (row.get("rank") is None, row.get("rank") or 999, str(row.get("model_account") or "")))
    return rows


def _compact_decisions(current: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in current.get("model_summaries") or []:
        if not isinstance(model, dict):
            continue
        account = model.get("model_account") or model.get("display_name") or model.get("seat")
        display = model.get("display_name") or model.get("seat") or account
        round_id = current.get("round_id")
        for bet in model.get("bets") or []:
            if not isinstance(bet, dict):
                continue
            stake = bet.get("original_stake_gp", bet.get("stake_gp", bet.get("converted_stake_gp", 0)))
            rows.append(
                {
                    "round_id": round_id,
                    "seat_id": account,
                    "model_account": account,
                    "display_name": display,
                    "match_id": bet.get("match_id"),
                    "market": bet.get("market"),
                    "selection": bet.get("selection") or bet.get("pick"),
                    "line": bet.get("line"),
                    "odds": bet.get("odds"),
                    "stake_gp": stake or 0,
                    "loan_used_gp": bet.get("loan_used_gp", 0),
                    "one_line": model.get("required_next_action") or model.get("one_sentence_strategy") or "",
                    "one_line_full": model.get("required_next_action") or model.get("one_sentence_strategy") or "",
                    "reason_short": model.get("required_next_action") or "",
                    "reason_full": model.get("required_next_action") or "",
                    "risk_short": "; ".join(str(item) for item in (model.get("warnings") or [])),
                    "risk_full": "; ".join(str(item) for item in (model.get("warnings") or [])),
                }
            )
    return rows


def _provider_summary(current: dict[str, Any]) -> dict[str, Any]:
    scoreboard = current.get("scoreboard") if isinstance(current.get("scoreboard"), dict) else {}
    matches = current.get("matches") if isinstance(current.get("matches"), list) else []
    valid_rows = 0
    for match in matches:
        if isinstance(match, dict):
            valid_rows += len(match.get("market_snapshot") or [])
    return {
        "provider": "pred_invest_artifact",
        "valid_odds_rows": valid_rows,
        "matches_with_odds": scoreboard.get("matches_with_odds", 0),
        "forecast_matches": scoreboard.get("forecast_matches", len(matches)),
        "source": "data/pool/pred_invest",
    }


def _betting_summary(current: dict[str, Any], shadow: dict[str, Any]) -> dict[str, Any]:
    scoreboard = current.get("scoreboard") if isinstance(current.get("scoreboard"), dict) else {}
    shadow_summary = shadow.get("summary") if isinstance(shadow.get("summary"), dict) else {}
    compact = _compact_decisions(current)
    return {
        "accepted_bets": scoreboard.get("existing_bets", shadow.get("total_existing_bets", 0)),
        "compact_decisions": compact,
        "summary": {
            "accepted_bets": scoreboard.get("existing_bets", shadow.get("total_existing_bets", 0)),
            "allowed": scoreboard.get("allowed", shadow_summary.get("allowed", 0)),
            "warned": scoreboard.get("warned", shadow_summary.get("warned", 0)),
            "rejected": scoreboard.get("rejected", shadow_summary.get("rejected", 0)),
            "models_without_bets": scoreboard.get("models_without_bets", shadow_summary.get("models_without_bets", 0)),
            "original_stake_total_gp": scoreboard.get("original_stake_total_gp"),
            "rule_converted_stake_total_gp": scoreboard.get("rule_converted_stake_total_gp"),
        },
        "models_detail": shadow.get("models_detail") or current.get("model_summaries") or [],
    }


def _normalize_team(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _hk_date_from_kickoff(value: Any) -> str | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None
    return dt.astimezone(timezone(timedelta(hours=8))).date().isoformat()


def _match_date_values(row: dict[str, Any]) -> set[str]:
    values = {
        str(row.get("date") or ""),
        str(row.get("matchday_hk") or ""),
        str(row.get("source_date_query") or ""),
    }
    hk_date = _hk_date_from_kickoff(row.get("kickoff_at"))
    if hk_date:
        values.add(hk_date)
    return {item for item in values if item and item != "None"}


def _score_rows() -> list[dict[str, Any]]:
    """Read the durable match-result registry used by scoreSync.

    The public API must expose settled results from the match registry itself.
    The frontend may still have a defensive scoreSync merge, but it should not
    be the primary owner of score truth.
    """
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    sources = [
        _read_pool_json("match_results", "latest_known_scores.json"),
        _read_pool_json("pred_invest", "latest_score_sync.json"),
    ]
    for data in sources:
        if not isinstance(data, dict):
            continue
        candidates = data.get("matches") or data.get("known_scores") or []
        for row in candidates:
            if not isinstance(row, dict):
                continue
            key = str(row.get("match_id") or "") or "|".join(
                (
                    _normalize_team(row.get("home_team")),
                    _normalize_team(row.get("away_team")),
                    str(row.get("kickoff_at") or row.get("matchday_hk") or ""),
                )
            )
            if not key or key in seen:
                continue
            seen.add(key)
            rows.append(row)
    return rows


def _score_key(row: dict[str, Any]) -> tuple[str, str]:
    return (_normalize_team(row.get("home_team")), _normalize_team(row.get("away_team")))


def _score_indexes(score_rows: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    by_id: dict[str, dict[str, Any]] = {}
    by_teams: dict[tuple[str, str], dict[str, Any]] = {}
    for row in score_rows:
        match_id = str(row.get("match_id") or "")
        if match_id:
            by_id[match_id] = row
        key = _score_key(row)
        if all(key):
            by_teams.setdefault(key, row)
    return by_id, by_teams


def _apply_score(match: dict[str, Any], score: dict[str, Any]) -> dict[str, Any]:
    merged = dict(match)
    for key in (
        "score",
        "home_score",
        "away_score",
        "outcome",
        "status",
        "result_state",
        "provider_event_id",
        "provider_last_update",
        "matchday_hk",
        "source_date_query",
    ):
        if score.get(key) is not None:
            merged[key] = score.get(key)
    merged["score_source"] = score.get("source") or "match_result_registry"
    merged["score_registry_applied"] = True
    return merged


def _score_only_match(score: dict[str, Any], requested_date: str | None = None) -> dict[str, Any]:
    date_values = _match_date_values(score)
    public_date = requested_date if requested_date in date_values else None
    public_date = public_date or score.get("source_date_query") or score.get("matchday_hk") or _hk_date_from_kickoff(score.get("kickoff_at"))
    return {
        "match_id": score.get("match_id"),
        "date": public_date,
        "kickoff_at": score.get("kickoff_at"),
        "home_team": score.get("home_team"),
        "away_team": score.get("away_team"),
        "status": score.get("status") or "settled",
        "result_state": score.get("result_state") or "finished",
        "score": score.get("score"),
        "home_score": score.get("home_score"),
        "away_score": score.get("away_score"),
        "outcome": score.get("outcome"),
        "market_snapshot": [],
        "available_markets": [],
        "matchday_hk": score.get("matchday_hk"),
        "source_date_query": score.get("source_date_query"),
        "provider_event_id": score.get("provider_event_id"),
        "provider_last_update": score.get("provider_last_update"),
        "score_source": score.get("source") or "match_result_registry",
        "score_registry_applied": True,
        "registry_only": True,
    }


def _merge_score_registry(matches: list[dict[str, Any]], requested_date: str | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    score_rows = _score_rows()
    by_id, by_teams = _score_indexes(score_rows)
    merged: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    applied = 0
    for raw in matches:
        if not isinstance(raw, dict):
            continue
        match = dict(raw)
        score = by_id.get(str(match.get("match_id") or "")) or by_teams.get(_score_key(match))
        if score:
            match = _apply_score(match, score)
            applied += 1
            if score.get("match_id"):
                seen_ids.add(str(score.get("match_id")))
        if match.get("match_id"):
            seen_ids.add(str(match.get("match_id")))
        merged.append(match)

    appended = 0
    for score in score_rows:
        match_id = str(score.get("match_id") or "")
        if match_id and match_id in seen_ids:
            continue
        if requested_date and requested_date not in _match_date_values(score):
            continue
        merged.append(_score_only_match(score, requested_date=requested_date))
        appended += 1
        if match_id:
            seen_ids.add(match_id)

    merged.sort(key=lambda row: (str(row.get("kickoff_at") or ""), str(row.get("match_id") or "")))
    return merged, {
        "score_registry_rows": len(score_rows),
        "score_registry_applied": applied,
        "score_registry_appended": appended,
    }


def _automation_summary(current: dict[str, Any], daily: dict[str, Any]) -> dict[str, Any]:
    missing = current.get("missing_data") if isinstance(current.get("missing_data"), dict) else {}
    errors = daily.get("errors") if isinstance(daily.get("errors"), list) else []
    warnings = daily.get("warnings") if isinstance(daily.get("warnings"), list) else []
    verdict = current.get("verdict") or daily.get("verdict") or "UNKNOWN"
    return {
        "pipeline_status": "ready" if verdict == "READY" and not errors else "attention_required",
        "verdict": verdict,
        "errors": errors + list(missing.get("sop_errors") or []),
        "warnings": warnings + list(missing.get("sop_warnings") or []),
        "matches_without_odds": missing.get("matches_without_odds") or [],
        "missing_models": missing.get("missing_models") or [],
        "generated_at": current.get("generated_at") or daily.get("generated_at"),
    }


def get_runtime_summary(round_id: str | None = None, date: str | None = None) -> dict[str, Any]:
    round_id = str(round_id or ACTIVE_ROUND_ID)
    date = str(date or DEFAULT_DATE)
    current_path = _artifact(date, round_id, "current_game")
    daily_path = _artifact(date, round_id, "daily_sop")
    prompt_path = _artifact(date, round_id, "prompt_pack")
    shadow_path = _artifact(date, round_id, "shadow_rerun")
    current_exact = _exact_artifact(date, round_id, "current_game").exists()
    prompt_exact = _exact_artifact(date, round_id, "prompt_pack").exists()

    current = _read_json(current_path)
    daily = _read_json(daily_path)
    prompts = _read_json(prompt_path)
    shadow = _read_json(shadow_path)
    quality = _read_json(_artifact(date, round_id, "quality_gate"))

    models = _merge_model_rows(current, daily, quality)
    active_models = [_model_to_summary(model) for model in models if isinstance(model, dict)]
    if (not current_exact or str(current.get("date") or "") != date or str(current.get("round_id") or "") != round_id) and prompt_exact:
        matches = prompts.get("matches") if isinstance(prompts.get("matches"), list) else []
    else:
        matches = current.get("matches") if isinstance(current.get("matches"), list) else []
    matches, score_audit = _merge_score_registry(matches, requested_date=date)
    dates = sorted({str(match.get("date")) for match in matches if isinstance(match, dict) and match.get("date")})

    return {
        "ok": True,
        "version": "pred_invest_pool_data_compat.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date,
        "round_id": round_id,
        "current_round": round_id,
        "authority": "pred_invest_artifacts",
        "source_policy": "read_latest_or_exact_artifacts_without_mutating_receipts",
        "operational_contract": {
            "rule_version": "PRED_INVEST_CREDIT_SURVIVE_V2",
            "mode": "daily_product_sop",
            "public_surface_policy": "show_results_logs_and_health_not_internal_sop_explainers",
            "complete_badge_requires": "quality_gate_publish_allowed_and_12_valid_seats",
        },
        "artifact_paths": {
            "current_game": str(current_path),
            "daily_sop": str(daily_path),
            "prompt_pack": str(prompt_path),
            "shadow_rerun": str(shadow_path),
            "current_game_exact": current_exact,
            "prompt_pack_exact": prompt_exact,
        },
        "provider": _provider_summary(current),
        "betting": _betting_summary(current, shadow),
        "automation": _automation_summary(current, daily),
        "matches": matches,
        "match_dates": [{"date": item, "count": sum(1 for m in matches if isinstance(m, dict) and m.get("date") == item)} for item in dates],
        "current_ranking": active_models,
        "historical_ranking": active_models,
        "active_models": active_models,
        "prompt_pack": {
            "models": prompts.get("models"),
            "match_count": prompts.get("match_count"),
            "prompts_count": len(prompts.get("prompts") or []),
            "rules": prompts.get("rules"),
        },
        "reports": {
            "current_game_html": str(PRED_DIR / "latest_current_game.html"),
            "current_game_md": str(PRED_DIR / "latest_current_game.md"),
            "daily_sop_md": str(PRED_DIR / "latest_daily_sop.md"),
            "prompt_pack_md": str(PRED_DIR / "latest_prompt_pack.md"),
            "shadow_rerun_md": str(PRED_DIR / "latest_shadow_rerun.md"),
        },
        "audit": {
            "date_span_in_artifact": dates,
            "requested_date": date,
            **score_audit,
            "note": "Artifacts may include repaired prior-date matches when SOP gap-filling is active.",
        },
    }


def get_current_rules(rule_version: str = "PRED_INVEST_CREDIT_SURVIVE_V2") -> dict[str, Any]:
    data = _read_pool_json("rules", f"{rule_version}.json")
    return {
        "ok": bool(data),
        "rule_version": data.get("rule_version"),
        "forecast_required": data.get("forecast_required"),
        "allow_no_bet": data.get("allow_no_bet"),
        "repay_before_ranking": data.get("repay_before_ranking"),
        "credit": data.get("credit"),
        "recovery_mode": data.get("recovery_mode"),
        "artifact_ref": _public_artifact_ref("rules", f"{rule_version}.json"),
    }


def get_behavior_summary(run_id: str) -> dict[str, Any]:
    run = _read_pool_json("god_ledger", "runs", f"{run_id}.json")
    events = run.get("events") if isinstance(run.get("events"), list) else []
    seats = sorted({str(event.get("seat_id")) for event in events if event.get("seat_id")})
    return {
        "ok": bool(run),
        "run_id": run_id,
        "event_count": len(events),
        "seats": seats,
        "event_counts": run.get("event_counts") or {},
        "artifact_ref": _public_artifact_ref("god_ledger", "runs", f"{run_id}.json"),
    }


def get_god_report(run_id: str, date: str | None = None) -> dict[str, Any]:
    date = date or DEFAULT_DATE
    json_report = _read_pool_json("god_reports", f"{date}_{run_id}.json")
    md_path = POOL_DIR / "god_reports" / f"{date}_{run_id}.md"
    markdown = md_path.read_text(encoding="utf-8") if md_path.exists() else json_report.get("markdown", "")
    return {
        "ok": bool(json_report or markdown),
        "date": date,
        "run_id": run_id,
        "summary": {key: json_report.get(key) for key in ("seat_count", "event_count", "action_counts") if key in json_report},
        "markdown": markdown,
        "artifact_ref": _public_artifact_ref("god_reports", f"{date}_{run_id}.md"),
    }


def get_seat_journal(seat_id: str, limit: int = 20) -> dict[str, Any]:
    rows = _read_pool_jsonl("seat_journals", seat_id, "journal.jsonl")[-limit:]
    summary = _read_pool_json("seat_journals", seat_id, "summary.json")
    return {
        "ok": bool(rows or summary),
        "seat_id": seat_id,
        "summary": summary,
        "events": rows,
        "artifact_ref": _public_artifact_ref("seat_journals", seat_id, "journal.jsonl"),
    }


def get_credit_history(seat_id: str) -> dict[str, Any]:
    rows = []
    ledger_dir = POOL_DIR / "credit_ledger"
    for path in sorted(ledger_dir.glob("*.json")) if ledger_dir.exists() else []:
        data = _read_json(path)
        seat = (data.get("seats") or {}).get(seat_id) if isinstance(data, dict) else None
        if isinstance(seat, dict):
            rows.append({"run_id": data.get("run_id"), **seat})
    return {"ok": True, "seat_id": seat_id, "history": rows}


def get_market_snapshot(run_id: str, date: str | None = None) -> dict[str, Any]:
    date = date or DEFAULT_DATE
    snapshot = _read_pool_json("market_snapshots", f"{date}_{run_id}.json")
    return {
        "ok": bool(snapshot),
        "date": date,
        "run_id": run_id,
        "privacy": snapshot.get("privacy"),
        "matches": snapshot.get("matches") or [],
        "artifact_ref": _public_artifact_ref("market_snapshots", f"{date}_{run_id}.json"),
    }
