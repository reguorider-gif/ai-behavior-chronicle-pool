from __future__ import annotations

import json
from typing import Any

from .paths import DATA_ROOT


RULE_VERSION = "PRED_INVEST_CREDIT_SURVIVE_V2"


def n(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_rule_version(rule_version: str = RULE_VERSION) -> dict[str, Any]:
    path = DATA_ROOT / "rules" / f"{rule_version}.json"
    if not path.exists():
        raise FileNotFoundError(f"missing rule version: {rule_version}")
    return json.loads(path.read_text(encoding="utf-8"))


def _ids(rows: Any) -> list[str]:
    if not isinstance(rows, list):
        return []
    return [str(row.get("match_id")) for row in rows if isinstance(row, dict) and row.get("match_id")]


def validate_required_forecasts(receipt: dict[str, Any], required_match_ids: list[str]) -> list[str]:
    forecast_ids = set(_ids(receipt.get("forecasts")))
    missing = [match_id for match_id in required_match_ids if match_id not in forecast_ids]
    return [f"missing_forecast:{match_id}" for match_id in missing]


def validate_required_investments(receipt: dict[str, Any], required_match_ids: list[str]) -> list[str]:
    investment_ids = set(_ids(receipt.get("investments")))
    missing = [match_id for match_id in required_match_ids if match_id not in investment_ids]
    return [f"missing_investment:{match_id}" for match_id in missing]


def validate_optional_investments(receipt: dict[str, Any], required_match_ids: list[str]) -> list[str]:
    """Investment rows are required for coverage, while each row may choose action=no_bet."""
    return validate_required_investments(receipt, required_match_ids)


def validate_forecast_receipt(receipt: dict[str, Any], required_match_ids: list[str], rule_version: str = RULE_VERSION) -> dict[str, Any]:
    rule = load_rule_version(rule_version)
    errors: list[str] = []
    if receipt.get("rule_version") != rule_version:
        errors.append(f"rule_version_mismatch:{receipt.get('rule_version')}!={rule_version}")
    for field in rule["prompt_contract"]["required_top_level_fields"]:
        if field not in receipt:
            errors.append(f"missing_top_level:{field}")
    errors.extend(validate_required_forecasts(receipt, required_match_ids))
    for forecast in receipt.get("forecasts") or []:
        if not isinstance(forecast, dict):
            errors.append("forecast_not_object")
            continue
        total = n(forecast.get("home_win_prob")) + n(forecast.get("draw_prob")) + n(forecast.get("away_win_prob"))
        if not (rule["prompt_contract"]["forecast_probability_sum_min"] <= total <= rule["prompt_contract"]["forecast_probability_sum_max"]):
            errors.append(f"forecast_probability_sum:{forecast.get('match_id')}:{total:.3f}")
        for key in ("home_win_prob", "draw_prob", "away_win_prob", "confidence"):
            value = n(forecast.get(key), -1)
            if not 0 <= value <= 1:
                errors.append(f"forecast_probability_range:{forecast.get('match_id')}:{key}")
        if not forecast.get("forecast_rationale"):
            errors.append(f"missing_forecast_rationale:{forecast.get('match_id')}")
    audit = receipt.get("self_audit") if isinstance(receipt.get("self_audit"), dict) else {}
    if audit.get("json_valid") is not True:
        errors.append("self_audit_json_valid_not_true")
    return {"ok": not errors, "errors": errors, "forecast_match_ids": _ids(receipt.get("forecasts"))}


def _stake_cap(rule: dict[str, Any], odds: float, net_worth_gp: float) -> float:
    for row in rule.get("stake_caps") or []:
        if n(row.get("min_odds")) <= odds < n(row.get("max_odds"), 1000000):
            return max(0.0, net_worth_gp * n(row.get("net_worth_fraction")))
    return max(0.0, net_worth_gp * 0.03)


def validate_investment_receipt(
    receipt: dict[str, Any],
    required_match_ids: list[str],
    *,
    loan_limit_gp: float,
    recovery_mode: bool,
    net_worth_gp: float,
    rule_version: str = RULE_VERSION,
) -> dict[str, Any]:
    rule = load_rule_version(rule_version)
    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(validate_required_investments(receipt, required_match_ids))
    total_loan_used = 0.0
    total_stake = 0.0
    for item in receipt.get("investments") or []:
        if not isinstance(item, dict):
            errors.append("investment_not_object")
            continue
        match_id = item.get("match_id")
        action = str(item.get("action") or "").lower()
        stake = n(item.get("stake_gp"))
        loan = n(item.get("loan_used_gp"))
        odds = n(item.get("odds"), 1.0)
        total_loan_used += loan
        total_stake += stake
        if action not in {"bet", "no_bet"}:
            errors.append(f"invalid_action:{match_id}:{action}")
        if action == "no_bet":
            if stake != 0 or loan != 0:
                errors.append(f"no_bet_must_have_zero_stake:{match_id}")
            if not item.get("why_bet_or_no_bet"):
                errors.append(f"no_bet_missing_reason:{match_id}")
            continue
        if stake <= 0:
            errors.append(f"bet_stake_must_be_positive:{match_id}")
        if loan > stake:
            errors.append(f"loan_exceeds_stake:{match_id}")
        if stake > _stake_cap(rule, odds, net_worth_gp):
            warnings.append(f"stake_cap_warning:{match_id}")
        if recovery_mode:
            recovery = rule["recovery_mode"]
            if loan > 0:
                errors.append(f"recovery_mode_new_loan_forbidden:{match_id}")
            if stake > n(recovery.get("max_single_match_stake_gp")):
                errors.append(f"recovery_mode_stake_too_high:{match_id}")
            if odds > n(recovery.get("max_odds")):
                errors.append(f"recovery_mode_odds_too_high:{match_id}")
    loan_request = receipt.get("loan_decision") if isinstance(receipt.get("loan_decision"), dict) else {}
    requested = n(loan_request.get("request_loan_gp"))
    if recovery_mode and requested > 0:
        errors.append("recovery_mode_loan_request_forbidden")
    if requested > loan_limit_gp:
        errors.append(f"loan_request_exceeds_limit:{requested:g}>{loan_limit_gp:g}")
    if total_loan_used > loan_limit_gp:
        errors.append(f"loan_used_exceeds_limit:{total_loan_used:g}>{loan_limit_gp:g}")
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "investment_match_ids": _ids(receipt.get("investments")),
        "total_stake_gp": round(total_stake, 2),
        "total_loan_used_gp": round(total_loan_used, 2),
    }


def validate_no_cross_seat_leakage(prompt_context: dict[str, Any], seat_id: str, all_seat_ids: list[str]) -> dict[str, Any]:
    serialized = json.dumps(prompt_context, ensure_ascii=False).lower()
    private_context = prompt_context.get("private_context") or {}
    leaked: list[str] = []
    identity_keys = {"seat_id", "model_account", "model_id", "display_name", "owner_seat_id"}

    def walk(value: Any, path: tuple[str, ...] = ()) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_text = str(key).lower()
                if key_text in {str(other).lower() for other in all_seat_ids if str(other).lower() != seat_id.lower()}:
                    leaked.append(key_text)
                walk(child, (*path, key_text))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, (*path, str(index)))
        elif path and path[-1] in identity_keys:
            text = str(value).lower()
            for other in all_seat_ids:
                other_text = str(other).lower()
                if other_text and other_text != seat_id.lower() and text == other_text:
                    leaked.append(other_text)

    walk(private_context)
    forbidden_keys = [key for key in ("other_seat_logs", "opponent_investments", "opponent_bets", "seat_private_logs") if key in serialized]
    return {"ok": not leaked and not forbidden_keys, "leaked_seats": sorted(set(leaked)), "forbidden_keys": forbidden_keys}
