from __future__ import annotations

from itertools import combinations
from typing import Any

from .civilization_competitor import compete_civilizations
from .civilization_field_engine import compute_field
from .civilization_genome_engine import build_civilization_genomes
from .civilization_meta_layer import build_civilization_meta_layer
from .civilization_physics_core import build_civilization_physics_core
from .civilization_state_engine import compute_states
from .civilization_war_engine import simulate_civilization_wars
from .collapse_predictor import predict_collapses
from .evolution_engine import predict_evolutions
from .meta_civilization_engine import build_meta_civilization_physics
from .phase_transition_engine import detect_phase_transitions
from .universe_engine import build_universe_engine
from .war_phase_engine import build_war_phase_triggers
from .memory_dynamics_engine import build_memory_dynamics
from .multiverse_engine import build_multiverse_engine
from .civilization_state import LOAN_SCORE, RISK_SCORE
from .io_utils import now_iso, write_json
from .paths import DATA_ROOT
from .rules_engine import n


class Civilization:
    """Product-level civilization object built from a group of agents."""

    def __init__(self, payload: dict[str, Any]):
        self.payload = payload
        self.id = str(payload.get("id") or "unknown")
        self.agents = list(payload.get("agents") or [])
        self.memory = list(payload.get("shared_memory") or [])
        self.strategy_profile = {
            "strategy_type": payload.get("strategy_type"),
            "behavior_identity": payload.get("behavior_identity"),
            "risk": payload.get("shared_risk_profile") or {},
            "performance": payload.get("performance") or {},
        }
        self.credit = self._credit_score()

    def _credit_score(self) -> float:
        perf = self.payload.get("performance") or {}
        risk = self.payload.get("shared_risk_profile") or {}
        survival = n(perf.get("survival_score"))
        stability = n(perf.get("stability_score"))
        loan = n(risk.get("loan_score"))
        return round(_clamp(survival * 0.54 + stability * 0.34 + (1 - loan) * 0.12), 3)

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "agents": self.agents,
            "shared_memory_count": len(self.memory),
            "credit": self.credit,
            "strategy_profile": self.strategy_profile,
        }


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _level(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def _civilization_id(agent: dict[str, Any]) -> str:
    behavior_type = str(agent.get("behavior_type") or "")
    archetype = str(agent.get("archetype") or "")
    risk_level = str(agent.get("risk_level") or "unknown")
    no_bet = n(agent.get("no_bet_rate"))
    if behavior_type in {"leveraged_survival_player", "aggressive_edge_hunter"} or archetype == "Risk Explorer" or risk_level == "high":
        return "risk_explorers"
    if behavior_type == "discipline_first_observer" or archetype in {"Survival Optimizer", "Stability Agent"} or no_bet >= 0.65 or risk_level in {"low", "guarded"}:
        return "stability_survival"
    return "adaptive_capital"


def _profile_for(civ_id: str) -> dict[str, str]:
    profiles = {
        "stability_survival": {
            "name": "Stable Survival Civilization",
            "zh_name": "稳态生存文明",
            "strategy_type": "conservative + no-bet + credit preservation",
            "behavior_identity": "Survival-first collective",
        },
        "risk_explorers": {
            "name": "High Risk Explorer Civilization",
            "zh_name": "高风险探索文明",
            "strategy_type": "aggressive + leverage-aware + high variance",
            "behavior_identity": "Risk-seeking collective",
        },
        "adaptive_capital": {
            "name": "Adaptive Capital Civilization",
            "zh_name": "自适应资本文明",
            "strategy_type": "selective allocation + medium risk + pattern following",
            "behavior_identity": "Balanced allocator collective",
        },
    }
    return profiles.get(civ_id, {
        "name": "Observer Civilization",
        "zh_name": "观察文明",
        "strategy_type": "observe + wait for evidence",
        "behavior_identity": "Observer collective",
    })


def _agent_scores(agent: dict[str, Any]) -> dict[str, float]:
    risk = RISK_SCORE.get(str(agent.get("risk_level") or "unknown"), RISK_SCORE["unknown"])
    loan = LOAN_SCORE.get(str(agent.get("loan_dependency") or "unknown"), LOAN_SCORE["unknown"])
    stake = n(agent.get("total_stake_gp"))
    profit = n(agent.get("settlement_profit_gp"))
    no_bet = _clamp(n(agent.get("no_bet_rate")))
    exposure = _clamp(stake / 1000)
    survival = _clamp(1.0 - (risk * 0.32) - (loan * 0.24) - max(0.0, -profit / 1000) + no_bet * 0.18)
    return {
        "risk": risk,
        "loan": loan,
        "stake": stake,
        "profit": profit,
        "no_bet": no_bet,
        "exposure": exposure,
        "survival": survival,
    }


def _aggregate_patterns(agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for agent in agents:
        for pattern in agent.get("top_patterns") or []:
            name = str(pattern.get("name") or pattern.get("label") or "pattern")
            row = grouped.setdefault(name, {
                "name": name,
                "label": pattern.get("label") or name,
                "confidence_values": [],
                "supporting_events": 0,
                "source_event_ids": [],
                "seats": [],
            })
            row["confidence_values"].append(n(pattern.get("confidence")))
            row["supporting_events"] += int(n(pattern.get("supporting_events")))
            row["source_event_ids"].extend(pattern.get("source_event_ids") or [])
            if agent.get("seat_id"):
                row["seats"].append(agent["seat_id"])
    patterns: list[dict[str, Any]] = []
    for row in grouped.values():
        values = row.pop("confidence_values") or [0]
        patterns.append({
            **row,
            "confidence": round(sum(values) / max(1, len(values)), 2),
            "source_event_ids": sorted(set(row["source_event_ids"]))[:12],
            "seats": sorted(set(row["seats"])),
        })
    return sorted(patterns, key=lambda item: (item["supporting_events"], item["confidence"]), reverse=True)[:5]


def _civilization(civ_id: str, agents: list[dict[str, Any]]) -> dict[str, Any]:
    profile = _profile_for(civ_id)
    scores = [_agent_scores(agent) for agent in agents]
    count = max(1, len(scores))
    avg_risk = sum(row["risk"] for row in scores) / count
    avg_loan = sum(row["loan"] for row in scores) / count
    avg_no_bet = sum(row["no_bet"] for row in scores) / count
    total_stake = sum(row["stake"] for row in scores)
    total_profit = sum(row["profit"] for row in scores)
    total_exposure = sum(row["exposure"] for row in scores)
    survival = sum(row["survival"] for row in scores) / count
    roi = (total_profit / total_stake) if total_stake else 0.0
    stability = _clamp((survival * 0.62) + ((1 - avg_risk) * 0.24) + (avg_no_bet * 0.14))
    volatility = _clamp((avg_risk * 0.48) + (avg_loan * 0.24) + (total_exposure / count * 0.28))
    return {
        "id": civ_id,
        **profile,
        "agent_count": len(agents),
        "agents": [agent.get("seat_id") for agent in agents],
        "shared_memory": _aggregate_patterns(agents),
        "shared_risk_profile": {
            "risk_score": round(avg_risk, 3),
            "risk_level": _level(avg_risk),
            "loan_score": round(avg_loan, 3),
            "loan_level": _level(avg_loan),
            "no_bet_rate": round(avg_no_bet, 3),
        },
        "performance": {
            "survival_score": round(survival, 3),
            "stability_score": round(stability, 3),
            "volatility_score": round(volatility, 3),
            "total_stake_gp": round(total_stake, 2),
            "capital_result_gp": round(total_profit, 2),
            "roi": round(roi, 4),
        },
    }


def _compare(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    a_perf = a.get("performance") or {}
    b_perf = b.get("performance") or {}
    a_risk = (a.get("shared_risk_profile") or {}).get("risk_score") or 0
    b_risk = (b.get("shared_risk_profile") or {}).get("risk_score") or 0
    a_profit = n(a_perf.get("capital_result_gp"))
    b_profit = n(b_perf.get("capital_result_gp"))
    a_survival = n(a_perf.get("survival_score"))
    b_survival = n(b_perf.get("survival_score"))
    a_stability = n(a_perf.get("stability_score"))
    b_stability = n(b_perf.get("stability_score"))
    short_winner = a["id"] if a_profit > b_profit else (b["id"] if b_profit > a_profit else "draw")
    long_a = a_survival * 0.62 + a_stability * 0.38
    long_b = b_survival * 0.62 + b_stability * 0.38
    long_winner = a["id"] if long_a > long_b else (b["id"] if long_b > long_a else "draw")
    risk_gap = abs(a_risk - b_risk)
    return {
        "id": f"{a['id']}__vs__{b['id']}",
        "civilizations": [a["id"], b["id"]],
        "risk_efficiency_gap": round(risk_gap, 3),
        "profit_gap_gp": round(a_profit - b_profit, 2),
        "survival_gap": round(a_survival - b_survival, 3),
        "short_term_winner": short_winner,
        "long_term_stability_winner": long_winner,
        "contrast_label": f"{a['zh_name']} vs {b['zh_name']}",
        "reading": _interaction_reading(a, b, short_winner, long_winner),
    }


def _interaction_reading(a: dict[str, Any], b: dict[str, Any], short_winner: str, long_winner: str) -> str:
    if short_winner == "draw" and long_winner == "draw":
        return "短期收益和长期稳定性暂未拉开差距，下一轮主要观察压力场变化。"
    short_name = "平局" if short_winner == "draw" else _profile_for(short_winner)["zh_name"]
    long_name = "平局" if long_winner == "draw" else _profile_for(long_winner)["zh_name"]
    return f"短期由{short_name}占优；长期稳定性由{long_name}占优。"


def _evolution(civilizations: list[dict[str, Any]], flow: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    flow_by_seat = {row.get("seat_id"): row for row in flow}
    for civ in civilizations:
        steps = []
        for seat in civ["agents"]:
            row = flow_by_seat.get(seat) or {}
            steps.append({
                "seat_id": seat,
                "run_id": row.get("run_id"),
                "flow_label": row.get("flow_label") or "observe → stable",
                "dominant_pattern": row.get("dominant_pattern"),
            })
        rows.append({
            "civilization_id": civ["id"],
            "label": civ["zh_name"],
            "steps": steps,
        })
    return rows


def _headline_battle(interactions: list[dict[str, Any]]) -> dict[str, Any]:
    if not interactions:
        return {}
    return sorted(
        interactions,
        key=lambda row: (row["risk_efficiency_gap"], abs(row["profit_gap_gp"]), abs(row["survival_gap"])),
        reverse=True,
    )[0]


def _collapse_level(score: float) -> str:
    if score >= 0.68:
        return "critical"
    if score >= 0.44:
        return "watch"
    return "stable"


def _civilization_state_label(civ: dict[str, Any]) -> str:
    perf = civ.get("performance") or {}
    risk = civ.get("shared_risk_profile") or {}
    volatility = n(perf.get("volatility_score"))
    survival = n(perf.get("survival_score"))
    risk_level = str(risk.get("risk_level") or "unknown")
    if volatility >= 0.66:
        return "volatile expansion"
    if survival >= 0.7 and risk_level in {"low", "medium"}:
        return "stable convergence"
    if risk_level == "high":
        return "risk expansion"
    return "adaptive drift"


def _interaction_graph(civilizations: list[dict[str, Any]], interactions: list[dict[str, Any]]) -> dict[str, Any]:
    layout = {
        "stability_survival": {"x": 0.18, "y": 0.72},
        "adaptive_capital": {"x": 0.5, "y": 0.46},
        "risk_explorers": {"x": 0.78, "y": 0.22},
    }
    nodes = []
    for index, civ in enumerate(civilizations):
        perf = civ.get("performance") or {}
        risk = civ.get("shared_risk_profile") or {}
        position = layout.get(civ["id"], {"x": round(0.24 + index * 0.22, 2), "y": round(0.5, 2)})
        nodes.append({
            "id": civ["id"],
            "label": civ.get("zh_name") or civ.get("name") or civ["id"],
            "x": position["x"],
            "y": position["y"],
            "size": round(0.8 + n(perf.get("volatility_score")) * 0.42 + len(civ.get("agents") or []) * 0.04, 2),
            "risk_level": risk.get("risk_level") or "unknown",
            "state": _civilization_state_label(civ),
            "agent_count": len(civ.get("agents") or []),
        })
    edges = []
    for row in interactions:
        a, b = row.get("civilizations") or [None, None]
        edges.append({
            "from": a,
            "to": b,
            "type": "behavioral_divergence",
            "weight": round(max(n(row.get("risk_efficiency_gap")), abs(n(row.get("survival_gap"))), min(1.0, abs(n(row.get("profit_gap_gp"))) / 1000)), 3),
            "short_term_winner": row.get("short_term_winner"),
            "long_term_stability_winner": row.get("long_term_stability_winner"),
            "label": row.get("contrast_label"),
        })
    return {"nodes": nodes, "edges": edges, "meaning": "node=civilization state, edge=behavioral divergence"}


def _civilization_timeline(civilizations: list[dict[str, Any]], flow: list[dict[str, Any]]) -> list[dict[str, Any]]:
    legacy = _evolution(civilizations, flow)
    by_id = {row["civilization_id"]: row for row in legacy}
    rows = []
    for civ in civilizations:
        old = by_id.get(civ["id"], {})
        run_ids = sorted({step.get("run_id") for step in old.get("steps", []) if step.get("run_id")})
        current_state = _civilization_state_label(civ)
        rows.append({
            "civilization_id": civ["id"],
            "label": civ.get("zh_name") or civ.get("name") or civ["id"],
            "run_sequence": run_ids or [None],
            "trajectory": [
                {"phase": "memory", "state": f"{len(civ.get('shared_memory') or [])} shared patterns"},
                {"phase": "current", "state": current_state},
                {"phase": "next_watch", "state": _next_watch(civ)},
            ],
            "agent_steps": old.get("steps", []),
        })
    return rows


def _next_watch(civ: dict[str, Any]) -> str:
    risk = civ.get("shared_risk_profile") or {}
    perf = civ.get("performance") or {}
    if n(perf.get("volatility_score")) >= 0.62:
        return "watch volatility crash risk"
    if n(risk.get("no_bet_rate")) >= 0.62:
        return "watch survival discipline persistence"
    return "watch strategy convergence"


def _clash_view(civilizations: list[dict[str, Any]], interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    civ_by_id = {civ["id"]: civ for civ in civilizations}
    rows = []
    for row in interactions:
        a_id, b_id = row.get("civilizations") or [None, None]
        a = civ_by_id.get(a_id, {})
        b = civ_by_id.get(b_id, {})
        rows.append({
            "id": row.get("id"),
            "title": row.get("contrast_label"),
            "civilization_a": {
                "id": a_id,
                "strategy": a.get("strategy_type"),
                "label": a.get("zh_name") or a.get("name") or a_id,
            },
            "civilization_b": {
                "id": b_id,
                "strategy": b.get("strategy_type"),
                "label": b.get("zh_name") or b.get("name") or b_id,
            },
            "outcome": {
                "short_term": row.get("short_term_winner"),
                "long_term": row.get("long_term_stability_winner"),
                "reading": row.get("reading"),
            },
            "metrics": {
                "risk_efficiency_gap": row.get("risk_efficiency_gap"),
                "profit_gap_gp": row.get("profit_gap_gp"),
                "survival_gap": row.get("survival_gap"),
            },
        })
    return rows


def _drift_engine(civilizations: list[dict[str, Any]], flow: list[dict[str, Any]]) -> dict[str, Any]:
    flow_by_seat = {row.get("seat_id"): row for row in flow}
    rows = []
    for civ in civilizations:
        drifts = [str((flow_by_seat.get(seat) or {}).get("strategy_drift") or "stable") for seat in civ.get("agents") or []]
        non_stable = sum(1 for item in drifts if item != "stable")
        rate = round(non_stable / max(1, len(drifts)), 3)
        rows.append({
            "civilization_id": civ["id"],
            "drift_rate": rate,
            "dominant_drift": max(set(drifts), key=drifts.count) if drifts else "stable",
            "state": "strategy_shifting" if rate >= 0.5 else "mostly_stable",
        })
    return {
        "version": "civilization_drift.v1",
        "civilizations": rows,
        "global_drift_rate": round(sum(row["drift_rate"] for row in rows) / max(1, len(rows)), 3),
    }


def _collapse_signals(civilizations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for civ in civilizations:
        perf = civ.get("performance") or {}
        risk = civ.get("shared_risk_profile") or {}
        roi = n(perf.get("roi"))
        score = _clamp(
            n(perf.get("volatility_score")) * 0.34
            + n(risk.get("loan_score")) * 0.24
            + max(0.0, -roi) * 0.22
            + (1 - n(perf.get("survival_score"))) * 0.2
        )
        rows.append({
            "civilization_id": civ["id"],
            "collapse_risk": round(score, 3),
            "level": _collapse_level(score),
            "reason": _collapse_reason(civ, score),
        })
    return rows


def _collapse_reason(civ: dict[str, Any], score: float) -> str:
    risk = civ.get("shared_risk_profile") or {}
    perf = civ.get("performance") or {}
    if score >= 0.68:
        return "高波动、贷款或负 ROI 已形成崩溃观察点。"
    if n(perf.get("volatility_score")) >= 0.55:
        return "波动偏高，下一轮重点看是否扩大杠杆。"
    if n(risk.get("no_bet_rate")) >= 0.62:
        return "纪律性较强，崩溃风险主要来自机会成本而非破产。"
    return "结构暂稳，继续观察策略漂移。"


def _meta_strategy(civilizations: list[dict[str, Any]], collapse_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not civilizations:
        return {}
    by_id = {civ["id"]: civ for civ in civilizations}
    safest = max(civilizations, key=lambda civ: n((civ.get("performance") or {}).get("survival_score")))
    expansion = max(civilizations, key=lambda civ: n((civ.get("performance") or {}).get("capital_result_gp")) + n((civ.get("performance") or {}).get("volatility_score")) * 100)
    fragile_id = max(collapse_rows, key=lambda row: n(row.get("collapse_risk")))["civilization_id"] if collapse_rows else safest["id"]
    fragile = by_id.get(fragile_id, {})
    return {
        "best_for_high_volatility": safest["id"],
        "best_for_short_term_expansion": expansion["id"],
        "most_fragile": fragile_id,
        "reading": (
            f"高波动环境下更适合{(safest.get('zh_name') or safest.get('name'))}；"
            f"短期扩张由{(expansion.get('zh_name') or expansion.get('name'))}承担；"
            f"当前最需要风控观察的是{(fragile.get('zh_name') or fragile.get('name') or fragile_id)}。"
        ),
    }


def _civilization_dynamics(civilizations: list[dict[str, Any]], drift_engine: dict[str, Any]) -> dict[str, Any]:
    states = compute_states(civilizations, drift_engine)
    collapse = predict_collapses(states)
    evolution = predict_evolutions(states, collapse["predictions"])
    competition = compete_civilizations(states, collapse["predictions"], evolution["predictions"])
    phase_transition = detect_phase_transitions(states, collapse["predictions"], evolution["predictions"])
    civilization_field = compute_field(phase_transition["phases"])
    war_engine = simulate_civilization_wars(phase_transition["phases"])
    war_phase = build_war_phase_triggers(phase_transition["phases"], war_engine["battles"])
    meta_layer = build_civilization_meta_layer(phase_transition["phases"], war_phase)
    memory_dynamics = build_memory_dynamics(civilizations, phase_transition["phases"], meta_layer)
    genome_engine = build_civilization_genomes(civilizations, phase_transition["phases"], memory_dynamics)
    meta_civilization = build_meta_civilization_physics(
        phase_rows=phase_transition["phases"],
        war_engine=war_engine,
        collapse_predictor=collapse,
        memory_dynamics=memory_dynamics,
    )
    universe = build_universe_engine(
        phase_rows=phase_transition["phases"],
        genome_engine=genome_engine,
        meta_civilization=meta_civilization,
    )
    multiverse = build_multiverse_engine(
        universe=universe,
        meta_civilization=meta_civilization,
        memory_dynamics=memory_dynamics,
    )
    dynamics = {
        "version": "civilization_dynamics.v7",
        "state_vectors": states,
        "collapse_predictor": collapse,
        "evolution_engine": evolution,
        "competition_model": competition,
        "phase_transition_engine": phase_transition,
        "civilization_field": civilization_field,
        "war_engine": war_engine,
        "war_phase_engine": war_phase,
        "meta_layer": meta_layer,
        "memory_dynamics_engine": memory_dynamics,
        "genome_engine": genome_engine,
        "meta_civilization_layer": meta_civilization,
        "universe_engine": universe,
        "multiverse_engine": multiverse,
        "state_space": {
            "zones": ["stable_zone", "adaptive_zone", "volatile_zone", "critical_state", "expansion_state", "collapse_zone"],
            "axis_x": "strategy_entropy",
            "axis_y": "collapse_probability",
            "physical_variables": ["energy", "entropy", "tension", "cohesion", "aggression", "fragility", "adaptation", "memory_depth"],
        },
        "final_loop": [
            "events",
            "state_update",
            "multiverse_coupling",
            "phase_transition",
            "war_dynamics",
            "collapse_prediction",
            "memory_field_update",
            "next_universe_step",
        ],
    }
    dynamics["physics_core"] = build_civilization_physics_core(dynamics)
    return dynamics


def build_civilization_battle(
    *,
    run_id: str | None,
    civilization_state: dict[str, Any],
    write: bool = True,
) -> dict[str, Any]:
    agents = civilization_state.get("agents") or []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for agent in agents:
        grouped.setdefault(_civilization_id(agent), []).append(agent)
    civilizations = [_civilization(civ_id, members) for civ_id, members in sorted(grouped.items()) if members]
    interactions = [_compare(a, b) for a, b in combinations(civilizations, 2)]
    flow = civilization_state.get("behavior_flow") or []
    collapse_rows = _collapse_signals(civilizations)
    drift_engine = _drift_engine(civilizations, flow)
    dynamics = _civilization_dynamics(civilizations, drift_engine)
    battle = {
        "version": "civilization_battle.v9",
        "generated_at": now_iso(),
        "run_id": run_id or civilization_state.get("run_id"),
        "title": "Multiverse Civilization Physics Engine",
        "question": "多个 AI 文明如何在耦合宇宙场中演化、相变、战争、崩溃与形成主导簇？",
        "engine": {
            "version": "multiverse_civilization_physics_engine.v1",
            "loop": [
                "events",
                "state_update",
                "multiverse_coupling",
                "phase_transition",
                "war_dynamics",
                "collapse_prediction",
                "memory_field_update",
                "next_universe_step",
            ],
            "capabilities": [
                "civilization_grouping",
                "civilization_interaction_graph",
                "civilization_clash_view",
                "civilization_drift_tracking",
                "collapse_signal_watch",
                "meta_strategy_reading",
                "civilization_state_vector",
                "collapse_prediction",
                "evolution_path_prediction",
                "civilization_fate_curve",
                "phase_transition_detection",
                "civilization_field_projection",
                "civilization_war_simulation",
                "civilization_phase_law",
                "war_as_phase_trigger",
                "memory_dynamics",
                "civilization_physics_core",
                "meta_civilization_clustering",
                "systemic_collapse_wave_detection",
                "civilization_migration_paths",
                "civilization_genome_expression",
                "universe_field_projection",
                "civilization_evolution_tree",
                "phase_field_overlay",
                "multiverse_coupling",
                "memory_field",
                "dominance_cluster",
                "cross_universe_drift",
            ],
        },
        "civilization_models": [Civilization(civ).to_public() for civ in civilizations],
        "civilizations": civilizations,
        "interactions": interactions,
        "headline_battle": _headline_battle(interactions),
        "interaction_graph": _interaction_graph(civilizations, interactions),
        "evolution_timeline": _evolution(civilizations, flow),
        "civilization_timeline": _civilization_timeline(civilizations, flow),
        "clash_view": _clash_view(civilizations, interactions),
        "drift_engine": drift_engine,
        "collapse_signals": collapse_rows,
        "dynamics": dynamics,
        "phase_transitions": dynamics["phase_transition_engine"],
        "civilization_field": dynamics["civilization_field"],
        "war_engine": dynamics["war_engine"],
        "war_phase_engine": dynamics["war_phase_engine"],
        "meta_layer": dynamics["meta_layer"],
        "memory_dynamics": dynamics["memory_dynamics_engine"],
        "genome_engine": dynamics["genome_engine"],
        "meta_civilization": dynamics["meta_civilization_layer"],
        "universe": dynamics["universe_engine"],
        "multiverse": dynamics["multiverse_engine"],
        "physics_core": dynamics["physics_core"],
        "fate_curve": dynamics["collapse_predictor"]["fate_curve"],
        "meta_strategy": _meta_strategy(civilizations, collapse_rows),
        "map_contract": {
            "primary_ui_extension": "civilization_vs_civilization",
            "primary_ui": "multiverse_civilization_map_v9",
            "unit": "civilization",
            "source_object": "civilization_state",
            "show_strategy_competition_not_raw_bets": True,
            "hide_odds_bets_ledger_by_default": True,
            "show_interaction_graph": True,
            "show_clash_view": True,
            "show_fate_curve": True,
            "show_collapse_prediction": True,
            "show_phase_transition": True,
            "show_war_map": True,
            "show_meta_layer": True,
            "show_phase_law": True,
            "show_memory_dynamics": True,
            "show_physics_core": True,
            "show_meta_civilization_layer": True,
            "show_genome_layer": True,
            "show_universe_layer": True,
            "show_multiverse_layer": True,
        },
    }
    if write:
        write_json(DATA_ROOT / "civilization_battle" / "latest.json", battle)
        if battle.get("run_id"):
            write_json(DATA_ROOT / "civilization_battle" / f"{battle['run_id']}.json", battle)
    return battle
