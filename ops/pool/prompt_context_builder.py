from __future__ import annotations

from typing import Any

from .behavior_journal import load_recent_seat_events, load_seat_summary
from .credit_engine import calculate_loan_limit
from .io_utils import read_json, write_json
from .paths import DATA_ROOT
from .rules_engine import RULE_VERSION, load_rule_version, n
from .survival_engine import apply_recovery_constraints, calculate_net_worth


def build_market_snapshot(date: str, run_id: str, matches: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for match in matches:
        markets = match.get("markets") if isinstance(match.get("markets"), list) else []
        rows.append({
            "match_id": match.get("match_id"),
            "date": match.get("date"),
            "home_team": match.get("home_team"),
            "away_team": match.get("away_team"),
            "kickoff_at": match.get("kickoff_at"),
            "markets": markets,
        })
    snapshot = {
        "date": date,
        "run_id": run_id,
        "privacy": "anonymous_market_only_no_seat_choices",
        "matches": rows,
    }
    write_json(DATA_ROOT / "market_snapshots" / f"{date}_{run_id}.json", snapshot)
    return snapshot


def _account_for_seat(seat_id: str, accounts: dict[str, dict[str, Any]] | None) -> dict[str, Any]:
    summary = load_seat_summary(seat_id)
    account = dict(summary)
    if accounts and isinstance(accounts.get(seat_id), dict):
        account.update(accounts[seat_id])
    account.setdefault("balance_gp", 1000)
    account.setdefault("outstanding_loan_gp", account.get("loan_gp", 0))
    account.setdefault("accrued_interest_gp", 0)
    account["net_worth_gp"] = calculate_net_worth(
        account.get("balance_gp"),
        account.get("outstanding_loan_gp") or account.get("loan_gp"),
        account.get("accrued_interest_gp"),
    )
    return account


def build_prompt_context(
    date: str,
    run_id: str,
    seat_id: str,
    rule_version: str = RULE_VERSION,
    *,
    accounts: dict[str, dict[str, Any]] | None = None,
    matches: list[dict[str, Any]] | None = None,
    market_snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rule = load_rule_version(rule_version)
    matches = matches if matches is not None else read_json(DATA_ROOT / "market_snapshots" / f"{date}_{run_id}.json", {"matches": []}).get("matches", [])
    market_snapshot = market_snapshot or build_market_snapshot(date, run_id, matches)
    account = _account_for_seat(seat_id, accounts)
    loan_terms = calculate_loan_limit(seat_id, n(account.get("net_worth_gp")))
    recovery = apply_recovery_constraints(seat_id, account)
    summary = load_seat_summary(seat_id)
    recent_events = load_recent_seat_events(seat_id, limit=12)
    context = {
        "date": date,
        "run_id": run_id,
        "seat_id": seat_id,
        "rule_version": rule_version,
        "public_context": {
            "current_rules": {
                "rule_version": rule["rule_version"],
                "must_forecast_every_match": True,
                "investment_action_options": ["bet", "no_bet"],
                "forecast_affects_credit": True,
                "investment_affects_gp": True,
                "loan_repaid_before_ranking": True,
                "recovery_mode": rule.get("recovery_mode"),
            },
            "anonymous_market_snapshot": market_snapshot,
            "output_contract": rule.get("prompt_contract"),
        },
        "private_context": {
            "own_account": account,
            "own_credit_and_loan": loan_terms,
            "own_recovery_constraints": recovery,
            "own_behavior_summary": summary,
            "own_recent_events": recent_events,
        },
        "privacy_guard": {
            "other_models_private_logs_visible": False,
            "other_models_current_choices_visible": False,
            "allowed_external_context": ["current_rules", "anonymous_market_snapshot", "own_history"],
        },
    }
    write_json(DATA_ROOT / "prompt_contexts" / run_id / f"{seat_id}.json", context)
    return context
