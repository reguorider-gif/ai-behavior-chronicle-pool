from __future__ import annotations

from collections import Counter
from typing import Any

from .io_utils import now_iso, write_json
from .paths import DATA_ROOT
from .rules_engine import n


RISK_SCORE = {
    "low": 0.18,
    "guarded": 0.32,
    "medium": 0.58,
    "high": 0.86,
    "unknown": 0.42,
}

LOAN_SCORE = {
    "low": 0.12,
    "medium": 0.56,
    "high": 0.88,
    "unknown": 0.24,
}

DRIFT_SCORE = {
    "risk_reduction": -0.34,
    "stable": 0.0,
    "loss_response_under_observation": 0.22,
    "aggressive_shift": 0.42,
}

ARCHETYPE_LABELS = {
    "leveraged_survival_player": "Risk Explorer",
    "discipline_first_observer": "Survival Optimizer",
    "aggressive_edge_hunter": "Risk Explorer",
    "selective_allocator": "Balanced Adapter",
    "balanced_trader": "Stability Agent",
    "observing": "Observer",
}


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _pressure_label(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.38:
        return "medium"
    return "low"


def _agent_position(profile: dict[str, Any]) -> dict[str, float]:
    risk = RISK_SCORE.get(str(profile.get("risk_level") or "unknown"), RISK_SCORE["unknown"])
    leverage = LOAN_SCORE.get(str(profile.get("loan_dependency") or "unknown"), LOAN_SCORE["unknown"])
    drift = DRIFT_SCORE.get(str(profile.get("strategy_drift") or "stable"), 0.0)
    exposure = _clamp(n(profile.get("total_stake_gp")) / 1000)
    no_bet = _clamp(n(profile.get("no_bet_rate")))
    x = _clamp(0.08 + risk * 0.56 + leverage * 0.22 + max(drift, 0) * 0.14)
    y = _clamp(0.12 + (1 - no_bet) * 0.46 + exposure * 0.32 + leverage * 0.10)
    size = round(0.72 + exposure * 0.7 + leverage * 0.34, 2)
    return {"x": round(x, 3), "y": round(y, 3), "size": size}


def _agent_node(seat_id: str, profile: dict[str, Any]) -> dict[str, Any]:
    behavior_type = str(profile.get("behavior_type") or "observing")
    risk_level = str(profile.get("risk_level") or "unknown")
    loan_dependency = str(profile.get("loan_dependency") or "unknown")
    strategy_drift = str(profile.get("strategy_drift") or "stable")
    return {
        "seat_id": seat_id,
        "behavior_type": behavior_type,
        "archetype": ARCHETYPE_LABELS.get(behavior_type, "Observer"),
        "risk_level": risk_level,
        "loan_dependency": loan_dependency,
        "no_bet_rate": n(profile.get("no_bet_rate")),
        "strategy_drift": strategy_drift,
        "settlement_profit_gp": n(profile.get("settlement_profit_gp")),
        "total_stake_gp": n(profile.get("total_stake_gp")),
        "total_loan_used_gp": n(profile.get("total_loan_used_gp")),
        "position": _agent_position(profile),
        "top_patterns": profile.get("top_patterns") or [],
    }


def _pressure_field(agents: list[dict[str, Any]], patterns: list[dict[str, Any]]) -> dict[str, Any]:
    seat_count = max(1, len(agents))
    high_credit_pressure = sum(1 for row in agents if row["loan_dependency"] in {"medium", "high"}) / seat_count
    high_risk = sum(1 for row in agents if row["risk_level"] == "high") / seat_count
    drift = sum(1 for row in agents if row["strategy_drift"] != "stable") / seat_count
    loss_pattern = any(str(row.get("name") or "").startswith("loss") for row in patterns)
    pattern_pressure = min(1.0, len(patterns) / 5)
    market_volatility = _clamp(0.18 + drift * 0.42 + (0.2 if loss_pattern else 0) + pattern_pressure * 0.14)
    risk_amplification = _clamp((high_risk * 0.48) + (high_credit_pressure * 0.34) + (drift * 0.18))
    credit_pressure = _clamp(high_credit_pressure)
    loan_exposure = _clamp(sum(row["total_loan_used_gp"] for row in agents) / max(1, seat_count * 500))
    return {
        "credit_pressure": {"score": round(credit_pressure, 3), "level": _pressure_label(credit_pressure)},
        "market_volatility": {"score": round(market_volatility, 3), "level": _pressure_label(market_volatility)},
        "loan_exposure": {"score": round(loan_exposure, 3), "level": _pressure_label(loan_exposure)},
        "risk_amplification": {"score": round(risk_amplification, 3), "level": _pressure_label(risk_amplification)},
    }


def _behavior_flow(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for trace in traces:
        pressure = trace.get("decision_pressure") or {}
        rows.append({
            "seat_id": trace.get("seat_id"),
            "run_id": trace.get("run_id"),
            "behavior_type": trace.get("behavior_type"),
            "risk_level": trace.get("risk_level"),
            "loan_dependency": trace.get("loan_dependency"),
            "strategy_drift": trace.get("strategy_drift"),
            "dominant_pattern": trace.get("dominant_pattern"),
            "flow_label": f"{trace.get('risk_level') or 'unknown'} → {trace.get('strategy_drift') or 'stable'}",
            "pressure": {
                "no_bet_rate": n(pressure.get("no_bet_rate")),
                "total_stake_gp": n(pressure.get("total_stake_gp")),
                "settlement_profit_gp": n(pressure.get("settlement_profit_gp")),
                "recovery_mode": bool(pressure.get("recovery_mode")),
            },
        })
    return rows


def _causal_edges(patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for pattern in patterns[:5]:
        label = str(pattern.get("label") or pattern.get("name") or "pattern")
        if "→" in label:
            cause, effect = [part.strip() for part in label.split("→", 1)]
        else:
            cause, effect = str(pattern.get("name") or "behavior"), "decision"
        edges.append({
            "pattern_id": pattern.get("name") or label,
            "cause": cause,
            "effect": effect,
            "confidence": n(pattern.get("confidence")),
            "supporting_events": int(n(pattern.get("supporting_events"))),
            "source_event_ids": pattern.get("source_event_ids") or [],
            "seats": pattern.get("seats") or [],
        })
    return edges


def build_civilization_state(
    *,
    run_id: str | None,
    agent_profiles: dict[str, Any],
    pattern_graph: dict[str, Any],
    evolution_trace: dict[str, Any],
    write: bool = True,
) -> dict[str, Any]:
    profiles = agent_profiles.get("seats") or {}
    patterns = pattern_graph.get("top_patterns") or []
    traces = evolution_trace.get("traces") or []
    agents = [_agent_node(seat_id, profile) for seat_id, profile in sorted(profiles.items())]
    archetypes = dict(Counter(row["archetype"] for row in agents))
    state = {
        "version": "civilization_state.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "title": "Behavior Civilization Map",
        "question": "多个智能体在经济压力下，如何形成行为文明结构？",
        "pressure": _pressure_field(agents, patterns),
        "agents": agents,
        "positions": {row["seat_id"]: row["position"] for row in agents},
        "drift": {row["seat_id"]: row["strategy_drift"] for row in agents},
        "archetypes": archetypes,
        "behavior_flow": _behavior_flow(traces),
        "causality": {
            "nodes": sorted({edge["cause"] for edge in _causal_edges(patterns)} | {edge["effect"] for edge in _causal_edges(patterns)}),
            "edges": _causal_edges(patterns),
        },
        "map_contract": {
            "primary_ui": "civilization_map",
            "show_behavior_structure_not_raw_data": True,
            "hide_odds_bets_ledger_by_default": True,
            "source_objects": ["agent_profiles", "pattern_graph", "evolution_trace"],
        },
    }
    if write:
        write_json(DATA_ROOT / "civilization_state" / "latest.json", state)
        if run_id:
            write_json(DATA_ROOT / "civilization_state" / f"{run_id}.json", state)
    return state
