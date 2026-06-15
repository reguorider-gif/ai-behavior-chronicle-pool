from __future__ import annotations

from typing import Any

from .io_utils import read_json, write_json
from .paths import DATA_ROOT
from .rules_engine import RULE_VERSION, load_rule_version, n


def _outcome_from_score(score: str) -> str:
    try:
        left, right = score.replace("–", "-").split("-", 1)
        home = int(left.strip())
        away = int(right.strip())
    except Exception:
        return "unknown"
    if home > away:
        return "home"
    if away > home:
        return "away"
    return "draw"


def _predicted_outcome(forecast: dict[str, Any]) -> str:
    probs = {
        "home": n(forecast.get("home_win_prob")),
        "draw": n(forecast.get("draw_prob")),
        "away": n(forecast.get("away_win_prob")),
    }
    return max(probs, key=probs.get)


def calculate_credit_delta(seat_id: str, run_id: str) -> dict[str, Any]:
    forecasts = read_json(DATA_ROOT / "forecast_receipts" / f"{run_id}.json", {"seats": {}}).get("seats", {}).get(seat_id, {})
    results = read_json(DATA_ROOT / "match_results" / f"{run_id}.json", {"matches": []})
    result_by_match = {row.get("match_id"): row for row in results.get("matches", []) if isinstance(row, dict)}
    delta = 0
    details = []
    for forecast in forecasts.get("forecasts") or []:
        result = result_by_match.get(forecast.get("match_id"))
        if not result:
            continue
        expected = _predicted_outcome(forecast)
        actual = _outcome_from_score(str(result.get("score") or ""))
        if actual == "unknown":
            continue
        change = 12 if expected == actual else -10
        if forecast.get("edge_assessment") == "insufficient_info":
            change -= 2
        delta += change
        details.append({"match_id": forecast.get("match_id"), "expected": expected, "actual": actual, "delta": change})
    return {"seat_id": seat_id, "run_id": run_id, "credit_delta": delta, "details": details}


def _historical_credit_delta(seat_id: str, exclude_run_id: str | None = None) -> float:
    total = 0.0
    ledger_dir = DATA_ROOT / "credit_ledger"
    for path in ledger_dir.glob("*.json") if ledger_dir.exists() else []:
        data = read_json(path, {})
        if exclude_run_id and data.get("run_id") == exclude_run_id:
            continue
        row = (data.get("seats") or {}).get(seat_id) if isinstance(data, dict) else None
        if isinstance(row, dict):
            total += n(row.get("credit_delta"))
    return total


def calculate_credit_score(seat_id: str, base_score: float = 600) -> float:
    rule = load_rule_version(RULE_VERSION)
    score = base_score + _historical_credit_delta(seat_id)
    return max(n(rule["credit"]["min_score"]), min(n(rule["credit"]["max_score"]), score))


def calculate_credit_grade(seat_id: str) -> str:
    score = calculate_credit_score(seat_id)
    return credit_grade_for_score(score)


def credit_grade_for_score(score: float) -> str:
    for row in load_rule_version(RULE_VERSION)["credit"]["grades"]:
        if score >= n(row.get("min_score")):
            return str(row.get("grade"))
    return "D"


def calculate_loan_limit(seat_id: str, net_worth_gp: float) -> dict[str, Any]:
    score = calculate_credit_score(seat_id)
    for row in load_rule_version(RULE_VERSION)["credit"]["grades"]:
        if score >= n(row.get("min_score")):
            multiplier = n(row.get("loan_multiplier"))
            return {
                "seat_id": seat_id,
                "credit_score": round(score, 2),
                "credit_grade": row.get("grade"),
                "loan_limit_gp": round(max(0.0, net_worth_gp * multiplier), 2),
                "interest_rate": row.get("interest_rate"),
            }
    return {"seat_id": seat_id, "credit_score": round(score, 2), "credit_grade": "D", "loan_limit_gp": 0, "interest_rate": None}


def write_credit_ledger(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    rule = load_rule_version(RULE_VERSION)
    min_score = n(rule["credit"]["min_score"])
    max_score = n(rule["credit"]["max_score"])
    seats = {}
    for seat_id in seat_ids:
        delta = calculate_credit_delta(seat_id, run_id)
        score = max(min_score, min(max_score, 600 + _historical_credit_delta(seat_id, exclude_run_id=run_id) + n(delta.get("credit_delta"))))
        seats[seat_id] = {
            **delta,
            "credit_score": round(score, 2),
            "credit_grade": credit_grade_for_score(score),
        }
    ledger = {"run_id": run_id, "rule_version": RULE_VERSION, "seats": seats}
    write_json(DATA_ROOT / "credit_ledger" / f"{run_id}.json", ledger)
    return ledger
