from __future__ import annotations

from typing import Any

from .io_utils import write_json
from .paths import DATA_ROOT
from .rules_engine import RULE_VERSION, load_rule_version, n


def calculate_net_worth(balance_gp: Any, outstanding_loan_gp: Any, accrued_interest_gp: Any = 0) -> float:
    return round(n(balance_gp) - n(outstanding_loan_gp) - n(accrued_interest_gp), 2)


def detect_recovery_mode(seat_id: str, account: dict[str, Any] | None = None) -> bool:
    account = account or {}
    net = account.get("net_worth_gp")
    if net is None:
        net = calculate_net_worth(account.get("balance_gp"), account.get("outstanding_loan_gp") or account.get("loan_gp"), account.get("accrued_interest_gp"))
    return n(net) <= n(load_rule_version(RULE_VERSION)["recovery_mode"]["trigger_net_worth_lte"])


def apply_recovery_constraints(seat_id: str, account: dict[str, Any] | None = None) -> dict[str, Any]:
    active = detect_recovery_mode(seat_id, account)
    rule = load_rule_version(RULE_VERSION)["recovery_mode"]
    return {
        "seat_id": seat_id,
        "recovery_mode": active,
        "freeze_new_loan": bool(active and rule.get("freeze_new_loan")),
        "max_single_match_stake_gp": rule.get("max_single_match_stake_gp") if active else None,
        "max_odds": rule.get("max_odds") if active else None,
        "allowed_actions": ["forecast", "no_bet", "small_recovery_bet"] if active else ["forecast", "bet", "no_bet"],
    }


def write_survival_ledger(run_id: str, accounts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    seats = {}
    for seat_id, account in accounts.items():
        net = calculate_net_worth(account.get("balance_gp"), account.get("outstanding_loan_gp") or account.get("loan_gp"), account.get("accrued_interest_gp"))
        enriched = {**account, "net_worth_gp": net}
        seats[seat_id] = {
            "seat_id": seat_id,
            "balance_gp": n(account.get("balance_gp")),
            "outstanding_loan_gp": n(account.get("outstanding_loan_gp") or account.get("loan_gp")),
            "accrued_interest_gp": n(account.get("accrued_interest_gp")),
            "net_worth_gp": net,
            **apply_recovery_constraints(seat_id, enriched),
        }
    ledger = {"run_id": run_id, "rule_version": RULE_VERSION, "seats": seats}
    write_json(DATA_ROOT / "survival_ledger" / f"{run_id}.json", ledger)
    return ledger
