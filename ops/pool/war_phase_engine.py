from __future__ import annotations

from typing import Any


def _risk_transfer(row: dict[str, Any]) -> float:
    values = list((row.get("collapse_risk_transfer") or {}).values())
    return max([float(value or 0) for value in values] or [0.0])


def _interaction_score(row: dict[str, Any]) -> float:
    return round(max(float(row.get("force_gap") or 0), _risk_transfer(row)), 3)


def _pressure_type(row: dict[str, Any]) -> str:
    phase_shift = str(row.get("phase_shift") or "")
    war_type = str(row.get("war_type") or "")
    if phase_shift in {"collapse_contagion_watch", "critical_pressure_transfer"}:
        return "collapse_pressure"
    if phase_shift == "expansion_vs_stability":
        return "expansion_pressure"
    if war_type == "collapse_war":
        return "fragility_pressure"
    if war_type == "resource_war":
        return "resource_pressure"
    return "strategy_pressure"


def build_war_phase_triggers(phase_rows: list[dict[str, Any]], battles: list[dict[str, Any]]) -> dict[str, Any]:
    phase_by_id = {row.get("civilization_id"): row for row in phase_rows}
    triggers = []
    for battle in battles:
        score = _interaction_score(battle)
        winner = battle.get("winner")
        participants = battle.get("civilizations") or []
        loser = next((item for item in participants if item != winner), "draw") if winner != "draw" else "draw"
        triggered = score >= 0.42 or battle.get("phase_shift") != "low_phase_shift"
        triggers.append({
            "id": f"{battle.get('id')}__phase_trigger",
            "battle_id": battle.get("id"),
            "civilizations": participants,
            "winner": winner,
            "loser": loser,
            "triggered": triggered,
            "interaction_score": score,
            "pressure_type": _pressure_type(battle),
            "phase_shift": battle.get("phase_shift"),
            "before_phase": {
                str(civ_id): (phase_by_id.get(civ_id) or {}).get("phase")
                for civ_id in participants
            },
            "predicted_after_pressure": _predicted_after_pressure(winner, loser, battle),
            "reading": _reading(winner, loser, battle, score, triggered),
        })
    return {
        "version": "war_phase_engine.v1",
        "triggers": triggers,
        "triggered_count": sum(1 for row in triggers if row["triggered"]),
        "highest_trigger": max(triggers, key=lambda row: row["interaction_score"]) if triggers else {},
        "meaning": "war interactions are treated as phase-transition triggers inside the simulated civilization field",
    }


def _predicted_after_pressure(winner: str, loser: str, battle: dict[str, Any]) -> dict[str, str]:
    if winner == "draw":
        return {"draw": "metastable_pressure"}
    pressure = _pressure_type(battle)
    winner_state = "expansion_watch" if pressure in {"resource_pressure", "strategy_pressure", "expansion_pressure"} else "stabilization_test"
    loser_state = "collapse_watch" if pressure in {"collapse_pressure", "fragility_pressure"} else "reconstruction_pressure"
    return {
        str(winner): winner_state,
        str(loser): loser_state,
    }


def _reading(winner: str, loser: str, battle: dict[str, Any], score: float, triggered: bool) -> str:
    if not triggered:
        return "场交互尚未越过相变阈值，当前更像普通策略竞争。"
    if winner == "draw":
        return f"相互作用强度 {score:.2f} 已形成亚稳态压力，但双方暂未分出结构性胜负。"
    return f"相互作用强度 {score:.2f} 已触发相变观察：{winner} 获得扩张/稳定压力，{loser} 进入重构或崩溃观察。"
