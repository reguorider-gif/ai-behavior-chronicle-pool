from __future__ import annotations

from itertools import combinations
from typing import Any


def _force(row: dict[str, Any]) -> float:
    physical = row.get("physical_vector") or {}
    energy = float(physical.get("energy") or 0)
    aggression = float(physical.get("aggression") or 0)
    cohesion = float(physical.get("cohesion") or 0)
    fragility = float(physical.get("fragility") or 0)
    tension = float(physical.get("tension") or 0)
    return round(energy * 0.3 + aggression * 0.22 + cohesion * 0.24 + (1 - fragility) * 0.16 + tension * 0.08, 3)


def _war_type(a: dict[str, Any], b: dict[str, Any]) -> str:
    av = a.get("physical_vector") or {}
    bv = b.get("physical_vector") or {}
    energy_gap = abs(float(av.get("energy") or 0) - float(bv.get("energy") or 0))
    cohesion_gap = abs(float(av.get("cohesion") or 0) - float(bv.get("cohesion") or 0))
    entropy_gap = abs(float(av.get("entropy") or 0) - float(bv.get("entropy") or 0))
    fragility_gap = abs(float(av.get("fragility") or 0) - float(bv.get("fragility") or 0))
    if fragility_gap >= max(energy_gap, cohesion_gap, entropy_gap):
        return "collapse_war"
    if energy_gap >= max(cohesion_gap, entropy_gap):
        return "resource_war"
    if cohesion_gap >= entropy_gap:
        return "stability_war"
    return "strategy_war"


def _reading(winner: str, loser: str, war_type: str) -> str:
    zh_type = {
        "resource_war": "资源战争",
        "stability_war": "稳定性战争",
        "strategy_war": "策略战争",
        "collapse_war": "崩溃诱导战",
    }.get(war_type, war_type)
    if winner == "draw":
        return f"{zh_type} 暂未分出胜负，双方结构力接近。"
    return f"{zh_type} 中 {winner} 占优；{loser} 需要观察是否被迫进入策略重构。"


def war_pair(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    a_id = str(a.get("civilization_id"))
    b_id = str(b.get("civilization_id"))
    force_a = _force(a)
    force_b = _force(b)
    if abs(force_a - force_b) < 0.035:
        winner = "draw"
        loser = "draw"
    elif force_a > force_b:
        winner = a_id
        loser = b_id
    else:
        winner = b_id
        loser = a_id
    phase_shift = _phase_shift(a, b)
    war_type = _war_type(a, b)
    return {
        "id": f"{a_id}__war__{b_id}",
        "civilizations": [a_id, b_id],
        "war_type": war_type,
        "forces": {
            a_id: force_a,
            b_id: force_b,
        },
        "winner": winner,
        "force_gap": round(abs(force_a - force_b), 3),
        "phase_shift": phase_shift,
        "collapse_risk_transfer": _collapse_transfer(a, b),
        "reading": _reading(winner, loser, war_type),
    }


def _phase_shift(a: dict[str, Any], b: dict[str, Any]) -> str:
    phases = {str(a.get("phase")), str(b.get("phase"))}
    if "COLLAPSE" in phases:
        return "collapse_contagion_watch"
    if "CRITICAL" in phases:
        return "critical_pressure_transfer"
    if "EXPANSION" in phases and ("STABLE" in phases or "ADAPTIVE" in phases):
        return "expansion_vs_stability"
    if "VOLATILE" in phases:
        return "volatility_spillover"
    return "low_phase_shift"


def _collapse_transfer(a: dict[str, Any], b: dict[str, Any]) -> dict[str, float]:
    av = a.get("physical_vector") or {}
    bv = b.get("physical_vector") or {}
    return {
        str(a.get("civilization_id")): round(float(bv.get("aggression") or 0) * float(av.get("fragility") or 0), 3),
        str(b.get("civilization_id")): round(float(av.get("aggression") or 0) * float(bv.get("fragility") or 0), 3),
    }


def simulate_civilization_wars(phase_rows: list[dict[str, Any]]) -> dict[str, Any]:
    battles = [war_pair(a, b) for a, b in combinations(phase_rows, 2)]
    headline = sorted(battles, key=lambda row: (row["force_gap"], max(row["collapse_risk_transfer"].values() or [0])), reverse=True)[0] if battles else {}
    type_counts: dict[str, int] = {}
    for row in battles:
        type_counts[row["war_type"]] = type_counts.get(row["war_type"], 0) + 1
    return {
        "version": "civilization_war_engine.v1",
        "battles": battles,
        "headline_war": headline,
        "war_type_counts": type_counts,
        "meaning": "war = interaction between behavioral fields; no real-world violence, betting, or financial action",
    }
