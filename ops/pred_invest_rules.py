#!/usr/bin/env python3
"""PRED-INVEST V2 rules for the AI World Cup pool.

The contract separates mandatory forecasts from optional investments. It is
deterministic and intentionally conservative: missing forecast-ledger data never
creates free leverage.
"""

from __future__ import annotations

import math
from typing import Any


RULE_VERSION = "PRED_INVEST_CREDIT_SURVIVE_V2"

CREDIT_WEIGHTS = {
    "forecast_accuracy": 0.40,
    "probability_calibration": 0.20,
    "risk_control": 0.15,
    "repayment_record": 0.10,
    "net_worth_health": 0.10,
    "ranking_performance": 0.05,
}

CREDIT_TIERS = [
    {"grade": "S", "min_score": 800, "loan_multiplier": 1.20, "base_interest_rate": 0.04},
    {"grade": "A", "min_score": 700, "loan_multiplier": 0.80, "base_interest_rate": 0.07},
    {"grade": "B", "min_score": 600, "loan_multiplier": 0.50, "base_interest_rate": 0.11},
    {"grade": "C", "min_score": 500, "loan_multiplier": 0.20, "base_interest_rate": 0.18},
    {"grade": "D", "min_score": 0, "loan_multiplier": 0.00, "base_interest_rate": None},
]

ODDS_STAKE_CAPS = [
    {"min_odds": 1.00, "max_odds": 2.50, "net_worth_fraction": 0.25},
    {"min_odds": 2.50, "max_odds": 5.00, "net_worth_fraction": 0.15},
    {"min_odds": 5.00, "max_odds": 10.00, "net_worth_fraction": 0.08},
    {"min_odds": 10.00, "max_odds": 20.00, "net_worth_fraction": 0.05},
    {"min_odds": 20.00, "max_odds": float("inf"), "net_worth_fraction": 0.03},
]

PROMPT_JSON_SCHEMA = {
    "forecast": {
        "match_id": "string",
        "home_win_prob": "0-1 number",
        "draw_prob": "0-1 number",
        "away_win_prob": "0-1 number",
        "most_likely_score": "string",
        "confidence": "0-1 number",
        "fair_odds": {"home": "number", "draw": "number", "away": "number"},
        "edge_assessment": "no_bet | bettable | low_confidence",
        "information_gaps": ["string"],
    },
    "investment": {
        "match_id": "string",
        "action": "bet | no_bet",
        "selection": "string or null",
        "market": "h2h | handicap | totals | null",
        "line": "number or null",
        "odds": "number or null",
        "stake_gp": "number",
        "own_funds_gp": "number",
        "loan_used_gp": "number",
        "model_prob": "0-1 number",
        "market_implied_prob": "0-1 number",
        "estimated_ev": "number",
        "max_loss_gp": "number",
        "survival_plan_if_loss": "string",
    },
}


def n(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(number) or math.isinf(number):
        return default
    return number


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def gp(value: Any) -> str:
    number = n(value)
    if abs(number - round(number)) < 0.001:
        return f"{int(round(number)):,} GP"
    return f"{number:,.1f} GP"


def net_worth(account: dict[str, Any]) -> float:
    balance = n(account.get("balance_gp") or account.get("confirmed_current_balance_gp"))
    loan = n(account.get("loan_gp") or account.get("remaining_loan_gp"))
    accrued_interest = n(account.get("accrued_interest_gp") or account.get("loan_interest_gp"))
    return balance - loan - accrued_interest


def credit_score(account: dict[str, Any], forecast_ledger: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a conservative credit score.

    Until a real forecast ledger exists, this uses a proxy and labels it
    explicitly. This prevents investment ranking from silently becoming credit.
    """
    forecast_ledger = forecast_ledger or {}
    if forecast_ledger.get("credit_score") is not None:
        score = clamp(n(forecast_ledger["credit_score"]), 0, 900)
        return {
            "score": score,
            "basis": "forecast_ledger",
            "grade": credit_tier(score)["grade"],
            "components": forecast_ledger.get("components") or {},
        }

    balance = n(account.get("balance_gp") or account.get("confirmed_current_balance_gp"))
    loan = n(account.get("loan_gp") or account.get("remaining_loan_gp"))
    nw = net_worth(account)
    rank = n(account.get("rank") or account.get("computed_rank"), 12)
    delta_component = clamp((balance - 1000.0) / 30.0, -80.0, 80.0)
    debt_component = -clamp((loan / max(balance, 1.0)) * 120.0, 0.0, 180.0)
    survival_component = clamp((nw - 500.0) / 20.0, -60.0, 60.0)
    rank_component = clamp((13.0 - rank) * 4.0, 0.0, 48.0)
    score = clamp(620.0 + delta_component + debt_component + survival_component + rank_component, 350.0, 780.0)
    return {
        "score": round(score, 1),
        "basis": "proxy_pending_forecast_ledger",
        "grade": credit_tier(score)["grade"],
        "components": {
            "forecast_accuracy": "pending",
            "probability_calibration": "pending",
            "risk_control_proxy": round(delta_component + debt_component, 1),
            "net_worth_health_proxy": round(survival_component, 1),
            "ranking_proxy": round(rank_component, 1),
        },
    }


def credit_tier(score: float) -> dict[str, Any]:
    for tier in CREDIT_TIERS:
        if score >= tier["min_score"]:
            return tier
    return CREDIT_TIERS[-1]


def loan_terms(account: dict[str, Any], forecast_ledger: dict[str, Any] | None = None) -> dict[str, Any]:
    credit = credit_score(account, forecast_ledger)
    tier = credit_tier(credit["score"])
    nw = net_worth(account)
    max_loan = max(0.0, nw * n(tier["loan_multiplier"]))
    outstanding = n(account.get("loan_gp") or account.get("remaining_loan_gp"))
    available = max(0.0, max_loan - outstanding)
    return {
        "credit_score": credit["score"],
        "credit_grade": tier["grade"],
        "credit_basis": credit["basis"],
        "net_worth_gp": round(nw, 2),
        "outstanding_loan_gp": round(outstanding, 2),
        "max_loan_gp": round(max_loan, 2),
        "available_loan_gp": round(available, 2),
        "base_interest_rate": tier["base_interest_rate"],
        "components": credit["components"],
    }


def stake_cap_for_odds(odds: Any, net_worth_gp: float) -> dict[str, Any]:
    price = max(1.0, n(odds, 1.0))
    for row in ODDS_STAKE_CAPS:
        if row["min_odds"] <= price < row["max_odds"]:
            cap = max(0.0, net_worth_gp * row["net_worth_fraction"])
            return {
                "odds": price,
                "net_worth_fraction": row["net_worth_fraction"],
                "max_stake_gp": round(cap, 2),
            }
    return {"odds": price, "net_worth_fraction": 0.03, "max_stake_gp": round(max(0.0, net_worth_gp * 0.03), 2)}


def risk_surcharge(
    *,
    odds: Any,
    stake_gp: Any,
    net_worth_gp: float,
    consecutive_loss: bool = False,
    research_missing: bool = False,
    overdue_loan: bool = False,
) -> dict[str, Any]:
    surcharges: list[dict[str, Any]] = []
    price = n(odds, 1.0)
    stake = n(stake_gp)
    if price >= 20:
        surcharges.append({"reason": "20倍以上冷门", "rate": 0.05})
    if stake > max(net_worth_gp, 1.0) * 0.30:
        surcharges.append({"reason": "单场投入超过净资产30%", "rate": 0.05})
    if consecutive_loss:
        surcharges.append({"reason": "连续两轮亏损", "rate": 0.03})
    if research_missing:
        surcharges.append({"reason": "研究缺失仍下注", "rate": 0.05})
    if overdue_loan:
        surcharges.append({"reason": "上轮逾期未还，禁贷", "rate": None})
    total = sum(row["rate"] for row in surcharges if row["rate"] is not None)
    return {"total_surcharge_rate": round(total, 4), "items": surcharges, "credit_lock": overdue_loan}


def evaluate_investment(bet: dict[str, Any], account: dict[str, Any]) -> dict[str, Any]:
    terms = loan_terms(account)
    nw = terms["net_worth_gp"]
    odds = bet.get("odds")
    stake = n(bet.get("stake_gp"))
    loan_used = n(bet.get("loan_used_gp") or bet.get("loan_gp"))
    cap = stake_cap_for_odds(odds, nw)
    surcharge = risk_surcharge(odds=odds, stake_gp=stake, net_worth_gp=nw)
    warnings: list[str] = []
    status = "allowed"
    if stake <= 0:
        status = "no_bet_or_invalid"
        warnings.append("未提交正数下注金额；在新规则下可作为 no-bet，但必须保留预测。")
    if stake > cap["max_stake_gp"]:
        status = "cap_warning" if status == "allowed" else status
        warnings.append(f"超过赔率仓位上限：允许上限 {gp(cap['max_stake_gp'])}。")
    if loan_used > terms["available_loan_gp"]:
        status = "loan_over_limit"
        warnings.append(f"贷款超出授信：可用 {gp(terms['available_loan_gp'])}。")
    if terms["base_interest_rate"] is None and loan_used > 0:
        status = "loan_rejected"
        warnings.append("信用等级 D 不可贷款。")
    return {
        "status": status,
        "warnings": warnings,
        "credit": terms,
        "stake_cap": cap,
        "surcharge": surcharge,
        "required_action": "forecast_required_in_all_cases",
    }


def daily_rules_text() -> str:
    return """PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。"""


def prompt_schema_text() -> str:
    return """输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}"""
