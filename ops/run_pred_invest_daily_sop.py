#!/usr/bin/env python3
"""Run the PRED-INVEST-CREDIT-SURVIVE V2 daily SOP gate.

This is the operational contract for the daily game loop. It is not a public
feature explainer. It verifies the data chain before AI Judge dispatch, guards
receipt quality after collection, and tells the frontend/report layer whether a
round is allowed to look complete.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
from typing import Any

from generate_pred_invest_prompt_pack import build_prompt_pack, write_outputs as write_prompt_outputs
from pred_invest_rules import RULE_VERSION, gp
from pred_invest_sop_guard import build_guard, write_guard
from run_pred_invest_shadow import build_shadow_report, write_outputs as write_shadow_outputs
from run_daily_pool_pipeline import _merge_results_with_matches, _settle
from pool.behavior_compiler import compile_all_behavior_memory
from pool.behavior_audit import run_behavior_production_audit
from pool.behavior_journal import update_seat_summary, write_seat_run
from pool.behavior_production_kernel import run_behavior_production_kernel
from pool.behavior_replay import build_replay_for_run
from pool.chronicle_compiler import compile_all_lessons, generate_run_chronicle
from pool.civilization_freeze import build_civilization_freeze_manifest
from pool.god_report_v2 import generate_god_report
from pool.io_utils import append_jsonl, now_iso, read_jsonl, write_json
from pool.pattern_compiler import compile_all_patterns
from pool.paths import DATA_ROOT
from pred_invest_seat_registry import PRODUCTION_SEATS, REQUIRED_SEAT_COUNT, canonical_seat_id
import sync_pred_invest_scores


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_read_error": str(exc)}


def operational_contract() -> dict[str, Any]:
    return {
        "rule_version": RULE_VERSION,
        "surface_policy": {
            "public_frontend": "show_matches_bets_rankings_commentary_and_health",
            "data_center": "show_only_user_or_referee_useful_status",
            "hidden_internal_details": [
                "full_prompt_text",
                "bridge_recovery_payloads",
                "raw_model_outputs",
                "internal_sop_explainers",
                "smoke_fixture_pages",
            ],
        },
        "daily_sequence": [
            "sync_finished_match_results",
            "sync_next_match_odds",
            "settle_finished_matches",
            "repay_interest_and_principal_before_ranking",
            "apply_top5_daily_rewards_and_stage_rewards",
            "apply_bottom3_penalties_or_forced_debt",
            f"build_full_match_prompt_pack_for_{REQUIRED_SEAT_COUNT}_models",
            "collect_forecast_and_investment_receipts",
            "run_quality_gate",
            "targeted_rerun_only_missing_or_invalid_seats",
            "generate_god_view_report_and_observer_ledger",
            "publish_frontend_only_when_gate_allows",
        ],
        "hard_gates": {
            "prompt_pack_models": REQUIRED_SEAT_COUNT,
            "all_required_matches_in_prompt_pack": True,
            "forecast_required_for_every_match": True,
            "investment_row_required_for_every_match": True,
            "targeted_rerun_not_full_rerun": True,
            "frontend_complete_badge_requires_all_valid_seats": REQUIRED_SEAT_COUNT,
        },
    }


def match_with_odds_count(pack: dict[str, Any]) -> int:
    return sum(1 for match in pack.get("matches") or [] if match.get("market_snapshot"))


def match_ids_without_odds(pack: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for match in pack.get("matches") or []:
        if not isinstance(match, dict):
            continue
        if not match.get("market_snapshot"):
            missing.append(str(match.get("match_id") or match.get("id") or "unknown"))
    return missing


def strict_decision_state(date: str, round_id: str) -> dict[str, Any]:
    path = OUT_DIR / f"{date}_{round_id}_god_report_strict.json"
    report = read_json(path)
    seats = report.get("seat_summaries") if isinstance(report.get("seat_summaries"), list) else []
    decisions = 0
    positive_bets = 0
    stake_total = 0.0
    for seat in seats:
        if not isinstance(seat, dict):
            continue
        investments = seat.get("investments") if isinstance(seat.get("investments"), list) else []
        decisions += len(investments)
        for row in investments:
            if not isinstance(row, dict):
                continue
            stake = float(row.get("stake_gp") or 0)
            if str(row.get("action") or "").lower() == "bet" and stake > 0:
                positive_bets += 1
                stake_total += stake
    return {
        "available": bool(seats),
        "source": "strict_god_report" if seats else "shadow_receipts",
        "path": str(path) if path.exists() else None,
        "decision_count": decisions,
        "positive_bet_count": positive_bets,
        "stake_total_gp": round(stake_total, 2),
        "valid_count": report.get("valid_count"),
        "required_seat_count": report.get("required_seat_count"),
        "publish_allowed": report.get("publish_allowed"),
        "needs_rerun": report.get("needs_rerun") or [],
        "valid_seats": report.get("valid_seats") or [],
        "seat_summaries": seats,
    }


def validate(pack: dict[str, Any], shadow: dict[str, Any], decision_state: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if pack.get("models") != REQUIRED_SEAT_COUNT:
        errors.append(f"prompt_pack_models_not_{REQUIRED_SEAT_COUNT}:{pack.get('models')}")
    if pack.get("match_count", 0) <= 0:
        errors.append("prompt_pack_has_no_matches")
    missing_odds = match_ids_without_odds(pack)
    if match_with_odds_count(pack) <= 0:
        errors.append("prompt_pack_has_no_odds")
    elif missing_odds:
        errors.append("prompt_pack_missing_odds_for_matches:" + ",".join(missing_odds))
    required = pack.get("required_coverage") if isinstance(pack.get("required_coverage"), dict) else {}
    missing_required = required.get("missing_required_match_ids") if isinstance(required.get("missing_required_match_ids"), list) else []
    if missing_required:
        errors.append("required_matches_missing_from_prompt_pack:" + ",".join(str(item) for item in missing_required))
    if shadow.get("models") != REQUIRED_SEAT_COUNT:
        errors.append(f"shadow_models_not_{REQUIRED_SEAT_COUNT}:{shadow.get('models')}")
    if shadow.get("missing_or_unavailable_models"):
        errors.append("missing_models:" + ",".join(shadow["missing_or_unavailable_models"]))
    strict_available = decision_state.get("available") and decision_state.get("decision_count", 0) > 0
    if shadow.get("total_existing_bets", 0) <= 0 and not strict_available:
        warnings.append("no_existing_bets_to_shadow_audit_bridge_run_required")
    if shadow.get("receipt_missing") and not strict_available:
        warnings.append(f"bet_receipts_missing:{shadow.get('receipt_missing_reason') or 'unknown'}")
    if shadow.get("summary", {}).get("warned", 0) > shadow.get("summary", {}).get("allowed", 0):
        warnings.append("most_existing_bets_need_stake_cap_or_forecast_fields")
    return errors, warnings


def provider_error_summary(meta: dict[str, Any]) -> str:
    if not isinstance(meta, dict):
        return "missing_meta"
    parts: list[str] = []
    error = str(meta.get("error") or "")
    if error:
        parts.append(error.split("\n", 1)[0][:90])
    for key, label in (
        ("curl_system_fallback", "system"),
        ("curl_direct_fallback", "direct"),
        ("curl_proxy_fallback", "proxy"),
        ("cache_fallback", "cache"),
    ):
        payload = meta.get(key) if isinstance(meta.get(key), dict) else {}
        detail = str(payload.get("error") or "")
        if detail:
            parts.append(f"{label}:{detail.split(chr(10), 1)[0][:80]}")
    for key, label in (
        ("curl_system_fallback_error", "system"),
        ("curl_direct_fallback_error", "direct"),
        ("curl_proxy_fallback_error", "proxy"),
        ("cache_fallback_error", "cache"),
    ):
        detail = str(meta.get(key) or "")
        if detail:
            parts.append(f"{label}:{detail.split(chr(10), 1)[0][:80]}")
    return " | ".join(parts) or "unknown"


def append_provider_warnings(pack: dict[str, Any], score_sync: dict[str, Any], warnings: list[str]) -> None:
    market_meta = pack.get("market_source_meta") if isinstance(pack.get("market_source_meta"), dict) else {}
    odds_meta = market_meta.get("the_odds_api") if isinstance(market_meta.get("the_odds_api"), dict) else {}
    if odds_meta and odds_meta.get("configured") and not odds_meta.get("ok"):
        warnings.append("the_odds_api_live_odds_unavailable:" + provider_error_summary(odds_meta))
    score_meta = score_sync.get("external_score_source") if isinstance(score_sync.get("external_score_source"), dict) else {}
    if score_meta.get("transport") == "cache_fallback":
        warnings.append("the_odds_api_scores_using_cache:" + provider_error_summary(score_meta))


def strict_method_lines(decision_state: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for seat in decision_state.get("seat_summaries") or []:
        if not isinstance(seat, dict):
            continue
        investments = seat.get("investments") if isinstance(seat.get("investments"), list) else []
        positive = [row for row in investments if isinstance(row, dict) and str(row.get("action") or "").lower() == "bet" and float(row.get("stake_gp") or 0) > 0]
        stake = sum(float(row.get("stake_gp") or 0) for row in positive)
        loan = seat.get("loan_decision") if isinstance(seat.get("loan_decision"), dict) else {}
        strategy = seat.get("one_sentence_strategy") or "已提交结构化判断"
        lines.append(
            f"- {seat.get('seat') or seat.get('model_account')}：{strategy}；下注 {len(positive)} 单 / 决策 {len(investments)} 条，投入 {gp(stake)}，借款 {gp(loan.get('borrow_gp') or 0)}。"
        )
    if decision_state.get("needs_rerun"):
        lines.append("- 待补席位：" + ", ".join(str(item) for item in decision_state.get("needs_rerun") or []))
    return lines


def strict_investment_receipts(decision_state: dict[str, Any]) -> dict[str, Any]:
    seats: dict[str, Any] = {}
    for seat in decision_state.get("seat_summaries") or []:
        if not isinstance(seat, dict):
            continue
        seat_id = str(seat.get("seat") or seat.get("model_account") or "").lower()
        if not seat_id:
            continue
        investments: list[dict[str, Any]] = []
        for row in seat.get("investments") or []:
            if not isinstance(row, dict):
                continue
            action = str(row.get("action") or "no_bet").lower()
            stake = float(row.get("stake_gp") or 0)
            investments.append(
                {
                    "match_id": row.get("match_id"),
                    "action": "bet" if action == "bet" and stake > 0 else "no_bet",
                    "market": row.get("market"),
                    "selection": row.get("selection"),
                    "line": row.get("line"),
                    "odds": row.get("odds"),
                    "stake_gp": stake,
                    "loan_used_gp": float(row.get("loan_used_gp") or 0),
                    "reason": row.get("reason") or row.get("rationale"),
                    "source": "strict_god_report",
                }
            )
        seats[seat_id] = {"seat_id": seat_id, "investments": investments}
    return {
        "version": "strict_god_report_investment_receipts.v1",
        "source": decision_state.get("source"),
        "path": decision_state.get("path"),
        "seats": seats,
    }


def _seat_order_from_sources(pack: dict[str, Any], shadow: dict[str, Any], decision_state: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    required = set(PRODUCTION_SEATS)
    for source_rows in (
        pack.get("prompts") or [],
        shadow.get("models_detail") or [],
        decision_state.get("seat_summaries") or [],
    ):
        if not isinstance(source_rows, list):
            continue
        for row in source_rows:
            if not isinstance(row, dict):
                continue
            seat_id = canonical_seat_id(row.get("seat") or row.get("model_account"))
            if seat_id and seat_id in required and seat_id not in seen:
                seen.add(seat_id)
                ordered.append(seat_id)
    for seat_id in PRODUCTION_SEATS:
        if seat_id not in seen:
            seen.add(seat_id)
            ordered.append(seat_id)
    return ordered


def _index_by_seat(rows: list[dict[str, Any]], *keys: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    required = set(PRODUCTION_SEATS)
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key in keys:
            seat_id = canonical_seat_id(row.get(key))
            if seat_id and seat_id in required:
                indexed[seat_id] = row
                break
    return indexed


def _match_ids(pack: dict[str, Any], decision_state: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for row in pack.get("matches") or []:
        if isinstance(row, dict) and row.get("match_id"):
            ids.append(str(row["match_id"]))
    for match_id in decision_state.get("required_matches") or []:
        if match_id:
            ids.append(str(match_id))
    seen: set[str] = set()
    ordered: list[str] = []
    for match_id in ids:
        if match_id not in seen:
            seen.add(match_id)
            ordered.append(match_id)
    return ordered


def _missing_forecast(match_id: str, reason: str) -> dict[str, Any]:
    return {
        "match_id": match_id,
        "status": "missing_provider_blocked",
        "home_win_prob": None,
        "draw_prob": None,
        "away_win_prob": None,
        "model_estimated_prob": None,
        "most_likely_score": None,
        "confidence": 0,
        "edge_assessment": "missing",
        "information_gaps": [reason],
        "forecast_rationale": reason,
    }


def _normalize_forecast(row: dict[str, Any]) -> dict[str, Any]:
    out = dict(row)
    out.setdefault("status", "collected")
    out.setdefault("source", "strict_god_report")
    if "p" in out and "model_estimated_prob" not in out:
        out["model_estimated_prob"] = out.get("p")
    if "score" in out and "most_likely_score" not in out:
        out["most_likely_score"] = out.get("score")
    out.setdefault("information_gaps", [])
    return out


def _missing_investment(match_id: str, reason: str) -> dict[str, Any]:
    return {
        "match_id": match_id,
        "status": "missing_provider_blocked",
        "action": "missing",
        "market": "",
        "selection": "",
        "line": None,
        "odds": None,
        "stake_gp": 0,
        "loan_used_gp": 0,
        "why_bet_or_no_bet": reason,
        "reason": reason,
        "source": "quality_gate_missing_receipt",
    }


def _normalize_investment(row: dict[str, Any]) -> dict[str, Any]:
    out = dict(row)
    action = str(out.get("action") or "").lower()
    stake = float(out.get("stake_gp") or 0)
    out["action"] = "bet" if action == "bet" and stake > 0 else "no_bet"
    out["stake_gp"] = stake
    out["loan_used_gp"] = float(out.get("loan_used_gp") or 0)
    out.setdefault("status", "collected")
    out.setdefault("source", "strict_god_report")
    out.setdefault("why_bet_or_no_bet", out.get("reason") or out.get("rationale") or "")
    return out


def _append_once(path: pathlib.Path, identity: dict[str, Any], row: dict[str, Any]) -> None:
    existing = read_jsonl(path)
    for item in existing:
        if all(item.get(key) == value for key, value in identity.items()):
            return
    append_jsonl(path, row)


def _event_once(seat_id: str, run_id: str, event_type: str, payload: dict[str, Any]) -> None:
    path = DATA_ROOT / "seat_journals" / seat_id / "journal.jsonl"
    row = {"ts": now_iso(), "seat_id": seat_id, "run_id": run_id, "event_type": event_type, **payload}
    _append_once(path, {"seat_id": seat_id, "run_id": run_id, "event_type": event_type}, row)


def _god_event_once(run_id: str, event_type: str, payload: dict[str, Any], seat_id: str | None = None) -> None:
    path = DATA_ROOT / "god_ledger" / "events.jsonl"
    identity = {"run_id": run_id, "event_type": event_type}
    if seat_id:
        identity["seat_id"] = seat_id
    row = {"ts": now_iso(), "run_id": run_id, "event_type": event_type, **payload}
    if seat_id:
        row["seat_id"] = seat_id
    _append_once(path, identity, row)


def _credit_row(seat_id: str, run_id: str, shadow_row: dict[str, Any], valid: bool, reason: str) -> dict[str, Any]:
    terms = shadow_row.get("loan_terms") if isinstance(shadow_row.get("loan_terms"), dict) else {}
    credit_delta = 0 if valid else -8
    score = float(terms.get("credit_score") or 600) + credit_delta
    grade = terms.get("credit_grade") or ("B" if score >= 600 else "C")
    details: list[dict[str, Any]] = []
    if not valid:
        details.append({"type": "missing_or_invalid_receipt", "reason": reason, "credit_delta": credit_delta})
    else:
        details.append({"type": "production_receipt_collected", "reason": "本轮预测/投资分账已收录，等待完整赛果校准信用。", "credit_delta": 0})
    return {
        "seat_id": seat_id,
        "run_id": run_id,
        "credit_delta": credit_delta,
        "details": details,
        "credit_score": round(score, 2),
        "credit_grade": grade,
        "credit_basis": terms.get("credit_basis") or "production_sop_pending_result_calibration",
        "loan_limit_gp": round(float(terms.get("max_loan_gp") or 0), 2),
        "available_loan_gp": round(float(terms.get("available_loan_gp") or 0), 2),
        "outstanding_loan_gp": round(float(terms.get("outstanding_loan_gp") or 0), 2),
        "interest_rate": terms.get("base_interest_rate"),
    }


def _survival_row(seat_id: str, shadow_row: dict[str, Any], settlement_update: dict[str, Any] | None = None) -> dict[str, Any]:
    terms = shadow_row.get("loan_terms") if isinstance(shadow_row.get("loan_terms"), dict) else {}
    net_worth = float((settlement_update or {}).get("net_worth_after_gp") if settlement_update else terms.get("net_worth_gp") or 0)
    outstanding = float((settlement_update or {}).get("outstanding_loan_gp") if settlement_update else terms.get("outstanding_loan_gp") or 0)
    balance = float((settlement_update or {}).get("balance_after_debt_service_gp") if settlement_update else net_worth + outstanding)
    interest = float((settlement_update or {}).get("unpaid_interest_gp") or 0)
    recovery = net_worth <= 0
    return {
        "seat_id": seat_id,
        "balance_gp": round(balance, 2),
        "outstanding_loan_gp": round(outstanding, 2),
        "accrued_interest_gp": round(interest, 2),
        "net_worth_gp": round(net_worth, 2),
        "recovery_mode": recovery,
        "freeze_new_loan": recovery,
        "loan_limit_gp": round(float(terms.get("max_loan_gp") or 0), 2),
        "available_loan_gp": round(float(terms.get("available_loan_gp") or 0), 2),
        "allowed_actions": ["forecast", "no_bet", "small_recovery_bet"] if recovery else ["forecast", "bet", "no_bet"],
    }


def build_production_artifacts(
    date: str,
    round_id: str,
    pack: dict[str, Any],
    shadow: dict[str, Any],
    decision_state: dict[str, Any],
    settlement_trigger: dict[str, Any],
    *,
    write: bool,
) -> dict[str, Any]:
    seat_ids = _seat_order_from_sources(pack, shadow, decision_state)
    prompts = _index_by_seat(pack.get("prompts") or [], "model_account")
    shadow_rows = _index_by_seat(shadow.get("models_detail") or [], "model_account")
    decision_rows = _index_by_seat(decision_state.get("seat_summaries") or [], "seat", "model_account")
    required_match_ids = _match_ids(pack, decision_state)
    settlement = read_json(DATA_ROOT / "settlements" / f"{round_id}.json") if write else {}
    settlement_updates = settlement.get("account_updates") if isinstance(settlement.get("account_updates"), dict) else {}
    missing_reason_by_seat = {str(item).lower(): "供应商慢响应或额度阻塞，未获得本轮合格结构化回执。" for item in decision_state.get("needs_rerun") or []}

    forecast_seats: dict[str, Any] = {}
    investment_seats: dict[str, Any] = {}
    credit_seats: dict[str, Any] = {}
    survival_seats: dict[str, Any] = {}
    valid_count = 0
    missing_count = 0

    for seat_id in seat_ids:
        decision = decision_rows.get(seat_id) or {}
        shadow_row = shadow_rows.get(seat_id) or {"model_account": seat_id, "display_name": seat_id, "loan_terms": {}}
        prompt_row = prompts.get(seat_id) or {}
        missing_reason = missing_reason_by_seat.get(seat_id)
        valid = bool(decision) and not missing_reason
        valid_count += 1 if valid else 0
        missing_count += 0 if valid else 1

        raw_forecasts = [_normalize_forecast(row) for row in (decision.get("forecasts") or []) if isinstance(row, dict)]
        by_match = {str(row.get("match_id")): row for row in raw_forecasts if row.get("match_id")}
        forecasts = []
        for match_id in required_match_ids:
            forecasts.append(by_match.get(match_id) or _missing_forecast(match_id, missing_reason or "本场预测缺失，需定向补跑。"))
        for row in raw_forecasts:
            if row.get("match_id") and str(row.get("match_id")) not in required_match_ids:
                forecasts.append(row)

        raw_investments = [_normalize_investment(row) for row in (decision.get("investments") or []) if isinstance(row, dict)]
        investment_by_match = {str(row.get("match_id")): row for row in raw_investments if row.get("match_id")}
        investments = []
        for match_id in required_match_ids:
            investments.append(investment_by_match.get(match_id) or _missing_investment(match_id, missing_reason or "本场投资动作缺失，需定向补跑。"))
        for row in raw_investments:
            if row.get("match_id") and str(row.get("match_id")) not in required_match_ids:
                investments.append(row)

        self_review = {
            "what_i_did_last_round": "读取生产轮次记录；本轮以结构化预测/投资分账入库。",
            "what_i_learned": "预测必须覆盖全赛程，投资可以 bet/no-bet，但不能缺席。",
            "strategy_change_this_round": decision.get("one_sentence_strategy") or shadow_row.get("required_next_action") or "",
            "risk_commitment": (decision.get("risk_notes") or [None])[0] if isinstance(decision.get("risk_notes"), list) and decision.get("risk_notes") else "",
        }
        loan_decision = decision.get("loan_decision") if isinstance(decision.get("loan_decision"), dict) else {
            "request_loan_gp": 0,
            "reason": missing_reason or "未声明新增贷款。",
        }
        forecast_seats[seat_id] = {
            "seat_id": seat_id,
            "display_name": shadow_row.get("display_name") or prompt_row.get("display_name") or seat_id,
            "status": "collected" if valid else "missing_provider_blocked",
            "forecasts": forecasts,
            "self_review": self_review,
        }
        investment_seats[seat_id] = {
            "seat_id": seat_id,
            "display_name": shadow_row.get("display_name") or prompt_row.get("display_name") or seat_id,
            "status": "collected" if valid else "missing_provider_blocked",
            "investments": investments,
            "loan_decision": loan_decision,
            "survival_plan": {
                "current_net_worth_awareness": "按生产 SOP 账本读取净值和贷款压力。",
                "if_all_bets_lose": "优先偿还利息和本金，再进入排名与惩罚计算。",
                "if_recovery_mode_triggered": "净值小于等于 0 时进入重整，冻结新增高杠杆。",
                "next_round_adjustment": self_review["strategy_change_this_round"],
            },
        }
        credit_seats[seat_id] = _credit_row(seat_id, round_id, shadow_row, valid, missing_reason or "ok")
        survival_seats[seat_id] = _survival_row(seat_id, shadow_row, settlement_updates.get(seat_id))

        if write:
            context_path = DATA_ROOT / "prompt_contexts" / round_id / f"{seat_id}.json"
            full_context = prompt_row.get("prompt_context") if isinstance(prompt_row.get("prompt_context"), dict) else {}
            full_context = {
                **full_context,
                "run_id": round_id,
                "date": date,
                "seat_id": seat_id,
                "display_name": forecast_seats[seat_id]["display_name"],
                "rule_version": RULE_VERSION,
                "prompt": prompt_row.get("prompt"),
                "loan_terms": prompt_row.get("loan_terms") or shadow_row.get("loan_terms") or {},
                "required_match_ids": required_match_ids,
                "source": "production_pred_invest_daily_sop",
                "behavior_memory_required": True,
            }
            write_json(context_path, full_context)
            _event_once(seat_id, round_id, "prompt_context_recorded", {"prompt_context_path": str(context_path.relative_to(ROOT))})
            _event_once(seat_id, round_id, "forecast_recorded", {"forecasts": forecasts, "status": forecast_seats[seat_id]["status"]})
            _event_once(seat_id, round_id, "investment_recorded", {"investments": investments, "loan_decision": loan_decision, "status": investment_seats[seat_id]["status"]})
            _event_once(seat_id, round_id, "credit_updated", credit_seats[seat_id])
            _event_once(seat_id, round_id, "survival_updated", survival_seats[seat_id])
            _god_event_once(round_id, "seat_forecast_recorded", {"forecast_count": len(forecasts), "status": forecast_seats[seat_id]["status"]}, seat_id=seat_id)
            _god_event_once(round_id, "seat_investment_recorded", {"investment_count": len(investments), "loan_decision": loan_decision, "status": investment_seats[seat_id]["status"]}, seat_id=seat_id)
            _god_event_once(round_id, "seat_credit_updated", credit_seats[seat_id], seat_id=seat_id)
            _god_event_once(round_id, "seat_survival_updated", survival_seats[seat_id], seat_id=seat_id)
            if settlement.get("seats", {}).get(seat_id):
                _event_once(seat_id, round_id, "settlement_recorded", {"settlement": settlement["seats"][seat_id]})
                _god_event_once(round_id, "seat_settlement_recorded", {"settlement": settlement["seats"][seat_id]}, seat_id=seat_id)
            write_seat_run(seat_id, round_id, {
                "rule_version": RULE_VERSION,
                "status": "collected" if valid else "missing_provider_blocked",
                "forecasts": forecasts,
                "investments": investments,
                "credit": credit_seats[seat_id],
                "survival": survival_seats[seat_id],
                "settlement": settlement.get("seats", {}).get(seat_id, {}),
            })
            update_seat_summary(seat_id, round_id)
            _god_event_once(round_id, "seat_artifact_recorded", {"status": forecast_seats[seat_id]["status"]}, seat_id=seat_id)

    forecast_receipts = {"version": "production_forecast_receipts.v1", "run_id": round_id, "date": date, "rule_version": RULE_VERSION, "seats": forecast_seats}
    investment_receipts = {"version": "production_investment_receipts.v1", "run_id": round_id, "date": date, "rule_version": RULE_VERSION, "seats": investment_seats}
    credit_ledger = {"version": "production_credit_ledger.v1", "run_id": round_id, "date": date, "rule_version": RULE_VERSION, "seats": credit_seats}
    survival_ledger = {"version": "production_survival_ledger.v1", "run_id": round_id, "date": date, "rule_version": RULE_VERSION, "seats": survival_seats}

    counts = {
        "seat_count": len(seat_ids),
        "valid_seat_count": valid_count,
        "missing_seat_count": missing_count,
        "required_match_count": len(required_match_ids),
        "forecast_receipt_count": len(forecast_seats),
        "investment_receipt_count": len(investment_seats),
        "prompt_context_count": len(seat_ids),
        "seat_journal_count": len(seat_ids),
    }
    if write:
        write_json(DATA_ROOT / "forecast_receipts" / f"{round_id}.json", forecast_receipts)
        write_json(DATA_ROOT / "investment_receipts" / f"{round_id}.json", investment_receipts)
        write_json(DATA_ROOT / "credit_ledger" / f"{round_id}.json", credit_ledger)
        write_json(DATA_ROOT / "survival_ledger" / f"{round_id}.json", survival_ledger)
        _god_event_once(round_id, "production_artifacts_generated", {"counts": counts, "settlement_trigger": settlement_trigger})
        behavior_kernel = compile_all_behavior_memory(seat_ids, run_id=round_id, write=write)
        pattern_index = compile_all_patterns(seat_ids, write=write)
        chronicle_index = compile_all_lessons(seat_ids, write=write)
        run_chronicle = generate_run_chronicle(date, round_id, seat_ids, write=write)
        counts["behavior_memory_count"] = behavior_kernel.get("seat_count", 0)
        counts["agent_profile_count"] = len((behavior_kernel.get("agent_profiles") or {}).get("seats") or {})
        counts["pattern_count"] = len((behavior_kernel.get("pattern_graph") or {}).get("top_patterns") or [])
        counts["compiled_pattern_count"] = pattern_index.get("pattern_count", 0)
        counts["chronicle_lesson_count"] = chronicle_index.get("lesson_count", 0)
        counts["run_chronicle_highlight_count"] = len(run_chronicle.get("highlights") or [])
        counts["evolution_trace_count"] = len((behavior_kernel.get("evolution_trace") or {}).get("traces") or [])
        counts["civilization_agent_count"] = len((behavior_kernel.get("civilization_state") or {}).get("agents") or [])
        counts["civilization_count"] = len((behavior_kernel.get("civilization_battle") or {}).get("civilizations") or [])
        counts["civilization_interaction_count"] = len((behavior_kernel.get("civilization_battle") or {}).get("interactions") or [])
        replay = build_replay_for_run(round_id, seat_ids, write=write)
        counts["replay_event_count"] = replay.get("event_count", 0)
        counts["replay_seat_count"] = replay.get("seat_count", 0)
        god_report = generate_god_report(date, round_id)
        production_contract = run_behavior_production_kernel(round_id, seat_ids)
        production_audit = run_behavior_production_audit(round_id, seat_ids)
        civilization_freeze = build_civilization_freeze_manifest(
            round_id,
            production_contract=production_contract,
            production_audit=production_audit,
            civilization_state=behavior_kernel.get("civilization_state") or {},
            civilization_battle=behavior_kernel.get("civilization_battle") or {},
            write=write,
        )
        counts["production_event_count"] = production_contract.get("event_count", 0)
        counts["production_kernel_ready"] = 1 if (production_contract.get("readiness") or {}).get("ok") else 0
        counts["production_audit_passed"] = production_audit.get("status", {}).get("passed", 0)
        counts["civilization_freeze_ready"] = 1 if civilization_freeze.get("ready") else 0
    else:
        god_report = {"seat_count": len(seat_ids), "event_count": 0}
        production_contract = {}
        production_audit = {}
        civilization_freeze = build_civilization_freeze_manifest(round_id, write=False)
        behavior_kernel = compile_all_behavior_memory(seat_ids, run_id=round_id, write=write)
        pattern_index = compile_all_patterns(seat_ids, write=write)
        chronicle_index = compile_all_lessons(seat_ids, write=write)
        run_chronicle = generate_run_chronicle(date, round_id, seat_ids, write=write)
        counts["behavior_memory_count"] = behavior_kernel.get("seat_count", 0)
        counts["agent_profile_count"] = len((behavior_kernel.get("agent_profiles") or {}).get("seats") or {})
        counts["pattern_count"] = len((behavior_kernel.get("pattern_graph") or {}).get("top_patterns") or [])
        counts["compiled_pattern_count"] = pattern_index.get("pattern_count", 0)
        counts["chronicle_lesson_count"] = chronicle_index.get("lesson_count", 0)
        counts["run_chronicle_highlight_count"] = len(run_chronicle.get("highlights") or [])
        counts["evolution_trace_count"] = len((behavior_kernel.get("evolution_trace") or {}).get("traces") or [])
        counts["civilization_agent_count"] = len((behavior_kernel.get("civilization_state") or {}).get("agents") or [])
        counts["civilization_count"] = len((behavior_kernel.get("civilization_battle") or {}).get("civilizations") or [])
        counts["civilization_interaction_count"] = len((behavior_kernel.get("civilization_battle") or {}).get("interactions") or [])
        replay = build_replay_for_run(round_id, seat_ids, write=write)
        counts["replay_event_count"] = replay.get("event_count", 0)
        counts["replay_seat_count"] = replay.get("seat_count", 0)

    artifact_refs = {
        "seat_journals": "data/pool/seat_journals/",
        "prompt_contexts": f"data/pool/prompt_contexts/{round_id}/",
        "behavior_memory": "data/pool/behavior_memory/compiled/",
        "behavior_patterns": "data/pool/behavior_patterns/",
        "behavior_chronicle": "data/pool/behavior_chronicle/",
        "run_chronicle": f"data/pool/behavior_chronicle/runs/{round_id}.md",
        "pattern_graph": "data/pool/pattern_graph/latest.json",
        "agent_profiles": "data/pool/agent_profiles/latest.json",
        "evolution_trace": "data/pool/evolution_traces/latest.json",
        "civilization_state": "data/pool/civilization_state/latest.json",
        "civilization_battle": "data/pool/civilization_battle/latest.json",
        "civilization_freeze": "data/pool/civilization_freeze/latest.json",
        "behavior_replay": f"data/pool/replay/runs/{round_id}.json",
        "behavior_production_contract": "data/pool/behavior_summary/production_contract.json",
        "behavior_kernel_manifest": f"data/pool/data_lake/kernels/behavior_kernel_v1.json",
        "behavior_run_manifest": f"data/pool/data_lake/runs/{round_id}.json",
        "behavior_production_audit": f"data/pool/behavior_audits/{round_id}.json",
        "behavior_causality_graph": f"data/pool/behavior_audits/{round_id}.causality_graph.json",
        "forecast_receipts": f"data/pool/forecast_receipts/{round_id}.json",
        "investment_receipts": f"data/pool/investment_receipts/{round_id}.json",
        "credit_ledger": f"data/pool/credit_ledger/{round_id}.json",
        "survival_ledger": f"data/pool/survival_ledger/{round_id}.json",
        "god_ledger": f"data/pool/god_ledger/runs/{round_id}.json",
        "god_report_v2_json": f"data/pool/god_reports/{date}_{round_id}.json",
        "god_report_v2_md": f"data/pool/god_reports/{date}_{round_id}.md",
        "behavior_summary": "data/pool/behavior_summary/latest.json",
    }
    behavior = {
        "ok": missing_count == 0,
        "generated_at": now_iso(),
        "date": date,
        "run_id": round_id,
        "rule_version": RULE_VERSION,
        "operational_mode": "production_pred_invest_sop",
        "public_frontend_contract": {
            "rule_version_label": f"规则版本：{RULE_VERSION}",
            "seat_journal_label": "行为日志：可查看",
            "credit_ledger_label": "信用账本：可查看",
            "forecast_investment_label": "预测/投资分账：可查看",
            "no_bet_label": "no-bet：合法动作",
            "recovery_label": "Recovery Mode：已接入",
        },
        "features": ["Seat Journal", "Credit", "Loan Limit", "Recovery Mode", "forecast_receipts", "investment_receipts", "Behavior Memory", "Behavior Chronicle", "Pattern Graph", "Evolution Trace", "Behavior Replay", "no-bet", "god_report_v2"],
        "counts": {**counts, "god_report_seat_count": god_report.get("seat_count", 0), "god_report_event_count": god_report.get("event_count", 0)},
        "separation": {
            "forecast_receipts_exists": True,
            "investment_receipts_exists": True,
            "forecast_and_investment_are_separate": True,
        },
        "production_kernel": {
            "kernel_version": production_contract.get("kernel_version"),
            "append_only_event_sourcing": production_contract.get("append_only_event_sourcing"),
            "deterministic_replay": production_contract.get("deterministic_replay"),
            "memory_isolation": production_contract.get("memory_isolation"),
            "audit_layer": production_contract.get("audit_layer"),
            "readiness": production_contract.get("readiness") or {},
        },
        "production_audit": {
            "verdict": (production_audit.get("status") or {}).get("verdict"),
            "checks": (production_audit.get("status") or {}).get("checks") or {},
            "causality_graph": production_audit.get("causality_graph") or {},
        },
        "civilization_freeze": {
            "engine_version": civilization_freeze.get("engine_version"),
            "final_status": civilization_freeze.get("final_status"),
            "ready": civilization_freeze.get("ready"),
            "system_definition": civilization_freeze.get("system_definition"),
        },
        "artifact_refs": artifact_refs,
        "readiness": {
            "god_report_v2_generated": bool(god_report.get("seat_count")),
            "behavior_summary_readable": True,
            "public_frontend_minimum_markers": [
                f"规则版本：{RULE_VERSION}",
                "行为日志：可查看",
                "信用账本：可查看",
                "预测/投资分账：可查看",
            ],
            "publish_complete_badge_allowed": missing_count == 0,
            "missing_or_blocked_seats": sorted(missing_reason_by_seat),
        },
    }
    if write:
        write_json(DATA_ROOT / "behavior_summary" / f"{date}_{round_id}.json", behavior)
        write_json(DATA_ROOT / "behavior_summary" / "latest.json", behavior)
        md_lines = [
            f"# Behavior Summary - {date} {round_id}",
            "",
            f"- 规则版本：{RULE_VERSION}",
            "- 行为日志：可查看",
            "- 信用账本：可查看",
            "- 预测/投资分账：可查看",
            "- no-bet：合法动作",
            "- Recovery Mode：已接入",
            f"- seat_journals：{counts['seat_journal_count']}",
            f"- prompt_contexts：{counts['prompt_context_count']}",
            f"- behavior_memory：{counts['behavior_memory_count']}",
            f"- behavior_patterns：{counts.get('compiled_pattern_count', 0)}",
            f"- behavior_chronicle：{counts.get('chronicle_lesson_count', 0)} lessons / {counts.get('run_chronicle_highlight_count', 0)} highlights",
            f"- agent_profiles：{counts['agent_profile_count']}",
            f"- pattern_graph：{counts['pattern_count']}",
            f"- evolution_trace：{counts['evolution_trace_count']}",
            f"- civilization_state：{counts['civilization_agent_count']} agents",
            f"- civilization_battle：{counts['civilization_count']} civilizations / {counts['civilization_interaction_count']} interactions",
            f"- behavior_replay：{counts['replay_event_count']} events / {counts['replay_seat_count']} seats",
            f"- production kernel：{counts.get('production_event_count', 0)} events / ready={bool(counts.get('production_kernel_ready'))}",
            f"- civilization freeze：{civilization_freeze.get('final_status') or 'missing'}",
            f"- forecast_receipts：{counts['forecast_receipt_count']}",
            f"- investment_receipts：{counts['investment_receipt_count']}",
            f"- valid seats：{valid_count}/{REQUIRED_SEAT_COUNT}",
            f"- blocked seats：{', '.join(sorted(missing_reason_by_seat)) or 'none'}",
            f"- god_report_v2：{'generated' if behavior['readiness']['god_report_v2_generated'] else 'missing'}",
        ]
        (DATA_ROOT / "behavior_summary" / "latest.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return {
        "version": "production_artifact_writer.v1",
        "counts": counts,
        "artifact_refs": artifact_refs,
        "valid_seats": sorted(decision_rows),
        "missing_or_blocked_seats": sorted(missing_reason_by_seat),
        "seat_statuses": {seat_id: forecast_seats[seat_id]["status"] for seat_id in seat_ids},
        "god_report_seat_count": god_report.get("seat_count", 0),
        "god_report_event_count": god_report.get("event_count", 0),
    }


def build_settlement_stage(
    round_id: str,
    pack: dict[str, Any],
    decision_state: dict[str, Any],
    score_sync: dict[str, Any],
    shadow: dict[str, Any],
    *,
    write: bool,
) -> dict[str, Any]:
    investments = strict_investment_receipts(decision_state)
    matches = [row for row in pack.get("matches") or [] if isinstance(row, dict)]
    seen_match_ids = {str(row.get("match_id")) for row in matches if row.get("match_id")}
    for row in score_sync.get("known_scores") or []:
        if not isinstance(row, dict):
            continue
        match_id = str(row.get("match_id") or "")
        if match_id and match_id not in seen_match_ids:
            matches.append(row)
            seen_match_ids.add(match_id)
    results = _merge_results_with_matches(
        {
            "source_policy": "score_sync_known_scores_plus_matches_api_rows",
            "matches": [row for row in score_sync.get("known_scores") or [] if isinstance(row, dict)],
        },
        matches,
    )
    result_ids = {str(row.get("match_id")) for row in results.get("matches", []) if isinstance(row, dict) and row.get("match_id")}
    positive_bets = [
        row
        for receipt in (investments.get("seats") or {}).values()
        for row in receipt.get("investments") or []
        if row.get("action") == "bet" and float(row.get("stake_gp") or 0) > 0
    ]
    pending_bets = [row for row in positive_bets if str(row.get("match_id")) not in result_ids]
    if write:
        settlement = _settle(round_id, matches, results, investments)
    else:
        settlement = {"settlement_status": "not_written", "summary": {}, "settlements": []}
    summary = settlement.setdefault("summary", {})
    summary["positive_bet_count"] = len(positive_bets)
    summary["pending_bets"] = len(pending_bets)
    summary["pending_match_ids"] = sorted({str(row.get("match_id")) for row in pending_bets if row.get("match_id")})
    summary["strict_receipt_seats"] = len(investments.get("seats") or {})
    summary["result_match_count"] = len(result_ids)
    if summary.get("settled_bets", 0) and pending_bets:
        settlement["settlement_status"] = "partially_settled"
    elif positive_bets and not summary.get("settled_bets", 0):
        settlement["settlement_status"] = "pending_match_results"
    elif not positive_bets:
        settlement["settlement_status"] = "no_positive_bets"
    if write:
        settlement_path = ROOT / "data" / "pool" / "settlements" / f"{round_id}.json"
        account_updates = strict_account_updates(settlement, shadow)
        if account_updates:
            settlement["account_updates"] = account_updates
            summary["account_updates_written"] = len(account_updates)
        settlement_path.write_text(json.dumps(settlement, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": settlement.get("settlement_status"),
        "source": "strict_god_report+score_sync+/api/matches",
        "positive_bet_count": len(positive_bets),
        "settled_bets": summary.get("settled_bets", 0),
        "pending_bets": len(pending_bets),
        "pending_match_ids": summary.get("pending_match_ids") or [],
        "total_stake_gp": summary.get("total_stake_gp", 0),
        "total_payout_gp": summary.get("total_payout_gp", 0),
        "total_profit_gp": summary.get("total_profit_gp", 0),
        "roi": summary.get("roi", 0),
        "account_updates_written": summary.get("account_updates_written", 0),
        "path": f"data/pool/settlements/{round_id}.json" if write else None,
    }


def strict_account_updates(settlement: dict[str, Any], shadow: dict[str, Any]) -> dict[str, Any]:
    by_seat = {
        str(row.get("model_account") or "").lower(): row
        for row in shadow.get("models_detail") or []
        if isinstance(row, dict) and row.get("model_account")
    }
    updates: dict[str, Any] = {}
    for seat_id, seat_settlement in (settlement.get("seats") or {}).items():
        shadow_row = by_seat.get(str(seat_id).lower())
        if not shadow_row:
            continue
        terms = shadow_row.get("loan_terms") if isinstance(shadow_row.get("loan_terms"), dict) else {}
        net_before = float(terms.get("net_worth_gp") or 0)
        outstanding_before = float(terms.get("outstanding_loan_gp") or 0)
        balance_before = net_before + outstanding_before
        profit = float(seat_settlement.get("profit_gp") or 0)
        settled_rows = [row for row in seat_settlement.get("settled") or [] if isinstance(row, dict) and row.get("status") in {"win", "lose", "push", "half_win", "half_lose"}]
        new_loan = round(sum(float(row.get("loan_used_gp") or 0) for row in settled_rows), 2)
        balance = balance_before + profit + new_loan
        outstanding = outstanding_before + new_loan
        rate = terms.get("base_interest_rate")
        interest_due = round(outstanding * float(rate or 0), 2) if outstanding > 0 else 0.0
        interest_paid = min(max(balance, 0.0), interest_due)
        balance -= interest_paid
        unpaid_interest = interest_due - interest_paid
        principal_paid = min(max(balance, 0.0), outstanding)
        balance -= principal_paid
        outstanding -= principal_paid
        net_after = round(balance - outstanding - unpaid_interest, 2)
        updates[str(seat_id)] = {
            "seat_id": seat_id,
            "rank_before": shadow_row.get("rank"),
            "balance_before_gp": round(balance_before, 2),
            "outstanding_loan_before_gp": round(outstanding_before, 2),
            "settlement_profit_gp": round(profit, 2),
            "settled_new_loan_used_gp": new_loan,
            "interest_due_gp": interest_due,
            "interest_paid_gp": round(interest_paid, 2),
            "principal_repaid_gp": round(principal_paid, 2),
            "balance_after_debt_service_gp": round(balance, 2),
            "outstanding_loan_gp": round(outstanding, 2),
            "unpaid_interest_gp": round(unpaid_interest, 2),
            "net_worth_after_gp": net_after,
            "ranking_basis": "partial_settlement_net_worth_after_interest_and_principal_repayment",
        }
    return updates


def score_sync_overdue() -> list[dict[str, Any]]:
    sync = read_json(OUT_DIR / "latest_score_sync.json")
    rows = sync.get("pending_score_backfill")
    if not isinstance(rows, list):
        audit = read_json(OUT_DIR / "latest_match_data_alignment_audit.json")
        rows = audit.get("score_missing_after_due")
    if not isinstance(rows, list):
        return []
    by_match: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("blocking") is False:
            continue
        match_id = str(row.get("match_id") or "")
        if not match_id:
            continue
        by_match.setdefault(match_id, row)
    return list(by_match.values())


def markdown(report: dict[str, Any]) -> str:
    pack = report["prompt_pack"]
    shadow = report["shadow_rerun"]
    decision = report.get("current_decision_source") or {}
    decision_count = decision.get("decision_count", shadow["total_existing_bets"])
    receipt_state = "strict-report" if decision.get("source") == "strict_god_report" else ("missing" if shadow.get("receipt_missing") else "available")
    lines = [
        f"# PRED-INVEST-CREDIT-SURVIVE V2 Daily SOP · {report['date']} · {report['round_id']}",
        "",
        f"- verdict: **{report['verdict']}**",
        f"- rule: {report.get('operational_contract', {}).get('rule_version')}",
        f"- prompt models: {pack['models']}/{REQUIRED_SEAT_COUNT}",
        f"- forecast matches: {pack['match_count']}",
        f"- required coverage: {len((pack.get('required_coverage') or {}).get('included_required_match_ids') or [])}/{len((pack.get('required_coverage') or {}).get('required_match_ids') or [])}",
        f"- matches with odds: {report['matches_with_odds']}",
        f"- current structured decisions audited: {decision_count}",
        f"- decision source: {decision.get('source') or 'shadow_receipts'}",
        f"- receipt state: {receipt_state}",
        f"- allowed / warned / rejected: {shadow['summary']['allowed']} / {shadow['summary']['warned']} / {shadow['summary']['rejected']}",
        f"- surface: public frontend only shows results/logs/health; SOP internals stay in artifacts",
        "",
        "## Errors",
        "",
    ]
    if report["errors"]:
        lines.extend(f"- {item}" for item in report["errors"])
    else:
        lines.append("- none")
    lines += ["", "## Warnings", ""]
    if report["warnings"]:
        lines.extend(f"- {item}" for item in report["warnings"])
    else:
        lines.append("- none")
    guard = report.get("automation_guard") or {}
    quality = guard.get("quality_gate") or {}
    bridge = guard.get("bridge") or {}
    lines += [
        "",
        "## Settlement Trigger",
        "",
    ]
    settlement = report.get("settlement_trigger") or {}
    if settlement:
        lines += [
            f"- status: {settlement.get('status')}",
            f"- source: {settlement.get('source')}",
            f"- settled / positive / pending: {settlement.get('settled_bets')} / {settlement.get('positive_bet_count')} / {settlement.get('pending_bets')}",
            f"- stake / payout / profit: {gp(settlement.get('total_stake_gp'))} / {gp(settlement.get('total_payout_gp'))} / {gp(settlement.get('total_profit_gp'))}",
            f"- debt-service account updates: {settlement.get('account_updates_written') or 0}",
            f"- pending matches: {', '.join(settlement.get('pending_match_ids') or []) or 'none'}",
        ]
    else:
        lines.append("- not run")
    lines += [
        "",
        "## Automation Guard",
        "",
        f"- guard status: {guard.get('status')}",
        f"- bridge: {'busy' if bridge.get('busy') else 'idle'}",
        f"- publish frontend: {guard.get('ok_to_publish_frontend')}",
        f"- valid seats: {quality.get('valid_count')}/{quality.get('required_seat_count')}",
        f"- needs rerun: {', '.join(quality.get('needs_rerun') or []) or 'none'}",
        "",
        "## Guard Actions",
        "",
    ]
    actions = guard.get("recommended_actions") or []
    lines.extend(f"- {item}" for item in actions) if actions else lines.append("- none")
    artifacts = report.get("production_artifacts") or {}
    artifact_counts = artifacts.get("counts") or {}
    lines += [
        "",
        "## Production Artifacts",
        "",
        f"- seat journals: {artifact_counts.get('seat_journal_count', 0)}/{REQUIRED_SEAT_COUNT}",
        f"- prompt contexts: {artifact_counts.get('prompt_context_count', 0)}/{REQUIRED_SEAT_COUNT}",
        f"- forecast receipts: {artifact_counts.get('forecast_receipt_count', 0)}/{REQUIRED_SEAT_COUNT}",
        f"- investment receipts: {artifact_counts.get('investment_receipt_count', 0)}/{REQUIRED_SEAT_COUNT}",
        f"- valid / blocked seats: {artifact_counts.get('valid_seat_count', 0)} / {artifact_counts.get('missing_seat_count', 0)}",
        f"- god report seats/events: {artifacts.get('god_report_seat_count', 0)} / {artifacts.get('god_report_event_count', 0)}",
        f"- blocked: {', '.join(artifacts.get('missing_or_blocked_seats') or []) or 'none'}",
    ]
    lines += ["", "## Latest Betting Method", ""]
    if report.get("latest_betting_method"):
        lines.extend(report["latest_betting_method"])
    elif decision.get("source") == "strict_god_report":
        lines.extend(strict_method_lines(decision))
    else:
        for row in shadow["models_detail"]:
            terms = row["loan_terms"]
            lines.append(
                f"- {row['display_name']}：信用 {terms['credit_grade']}/{terms['credit_score']}，净资产 {gp(terms['net_worth_gp'])}，可贷 {gp(terms['available_loan_gp'])}；{row['required_next_action']}"
            )
    return "\n".join(lines)


def write_report(report: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{report['date']}_{report['round_id']}_daily_sop"
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_daily_sop.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_daily_sop.md").write_text(markdown(report) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run PRED-INVEST-CREDIT-SURVIVE V2 daily SOP")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--base-url", default="https://pool-app-one.vercel.app")
    parser.add_argument("--runs", default="", help="Comma-separated AI Judge run ids to audit with the publish gate.")
    parser.add_argument("--bridge-base-url", default="http://127.0.0.1:8501")
    parser.add_argument("--recover-stuck-bridge", action="store_true")
    parser.add_argument("--stuck-seconds", type=float, default=300.0)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.write:
        os.environ.setdefault("PRED_INVEST_WRITE_PROVIDER_CACHE", "1")
    pack = build_prompt_pack(args.date, args.round_id, args.base_url, write_contexts=args.write)
    shadow = build_shadow_report(args.date, args.round_id, args.base_url)
    decision_state = strict_decision_state(args.date, args.round_id)
    score_sync = sync_pred_invest_scores.build_sync()
    if args.write:
        score_sync["paths"] = sync_pred_invest_scores.write_sync(score_sync)
    settlement_trigger = build_settlement_stage(args.round_id, pack, decision_state, score_sync, shadow, write=args.write)
    errors, warnings = validate(pack, shadow, decision_state)
    append_provider_warnings(pack, score_sync, warnings)
    overdue_scores = score_sync_overdue()
    if overdue_scores:
        errors.append("score_sync_overdue:" + ",".join(str(row.get("match_id")) for row in overdue_scores[:12]))
    prompt_paths = write_prompt_outputs(pack) if args.write else {}
    shadow_paths = write_shadow_outputs(shadow) if args.write else {}
    run_ids = [item.strip() for item in args.runs.split(",") if item.strip()]
    guard = build_guard(
        args.date,
        args.round_id,
        run_ids,
        bridge_base_url=args.bridge_base_url.rstrip("/"),
        recover_stuck=args.recover_stuck_bridge,
        stuck_seconds=args.stuck_seconds,
    )
    errors.extend(f"sop_guard:{item}" for item in guard.get("errors") or [])
    warnings.extend(f"sop_guard:{item}" for item in guard.get("warnings") or [])
    if guard.get("status") == "PARTIAL_NOT_READY":
        qg = guard.get("quality_gate") or {}
        warnings.append(f"quality_gate_partial:{qg.get('valid_count')}/{qg.get('required_seat_count')}")
    guard_paths = write_guard(guard) if args.write else {}
    production_artifacts = build_production_artifacts(
        args.date,
        args.round_id,
        pack,
        shadow,
        decision_state,
        settlement_trigger,
        write=args.write,
    )
    if errors:
        verdict = "NOT_READY"
    elif guard.get("status") == "PARTIAL_NOT_READY":
        verdict = "PARTIAL_NOT_READY"
    else:
        verdict = "READY"
    report = {
        "version": "pred_invest_daily_sop.v2",
        "date": args.date,
        "round_id": args.round_id,
        "operational_contract": operational_contract(),
        "verdict": verdict,
        "errors": errors,
        "warnings": warnings,
        "score_sync_overdue": overdue_scores,
        "score_sync": {key: value for key, value in score_sync.items() if key != "by_output_date"},
        "settlement_trigger": settlement_trigger,
        "production_artifacts": production_artifacts,
        "matches_with_odds": match_with_odds_count(pack),
        "current_decision_source": {key: value for key, value in decision_state.items() if key != "seat_summaries"},
        "latest_betting_method": strict_method_lines(decision_state) if decision_state.get("source") == "strict_god_report" else [],
        "prompt_pack": {
            "models": pack["models"],
            "match_count": pack["match_count"],
            "required_coverage": pack.get("required_coverage"),
            "path": prompt_paths,
        },
        "shadow_rerun": {
            "models": shadow["models"],
            "receipt_missing": shadow.get("receipt_missing"),
            "receipt_missing_reason": shadow.get("receipt_missing_reason"),
            "total_existing_bets": shadow["total_existing_bets"],
            "summary": shadow["summary"],
            "models_detail": shadow["models_detail"],
            "path": shadow_paths,
        },
        "automation_guard": {
            "status": guard.get("status"),
            "ok_to_start_new_run": guard.get("ok_to_start_new_run"),
            "ok_to_publish_frontend": guard.get("ok_to_publish_frontend"),
            "bridge": guard.get("bridge"),
            "quality_gate": guard.get("quality_gate"),
            "recommended_actions": guard.get("recommended_actions"),
            "path": guard_paths,
        },
    }
    paths = write_report(report) if args.write else {}
    print(json.dumps({"ok": report["verdict"] == "READY", "verdict": report["verdict"], "errors": errors, "warnings": warnings, "paths": paths}, ensure_ascii=False, indent=2))
    return 0 if report["verdict"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
