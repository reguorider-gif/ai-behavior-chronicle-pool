from __future__ import annotations

from typing import Any

from .civilization_state_engine import clamp


def _label_for_phase(phase: str) -> str:
    return {
        "STABLE": "Stable",
        "ADAPTIVE": "Adaptive",
        "VOLATILE": "Volatile",
        "CRITICAL": "Critical",
        "EXPANSION": "Expansion",
        "COLLAPSE": "Collapse Watch",
    }.get(phase, phase)


def _transition_for_phase(phase: str) -> str:
    return {
        "STABLE": "Stable → Stable consolidation",
        "ADAPTIVE": "Stable → Adaptive optimization",
        "VOLATILE": "Adaptive → Volatile oscillation",
        "CRITICAL": "Volatile → Critical state",
        "EXPANSION": "Stable → Expansion burst",
        "COLLAPSE": "Critical → Collapse or reconstruction",
    }.get(phase, "Observe → Reclassify")


def compute_physical_vector(
    state: dict[str, Any],
    collapse_prediction: dict[str, Any] | None = None,
) -> dict[str, float]:
    """Project the behavior state vector into civilization-dynamics variables."""

    vector = state.get("state_vector") or {}
    risk = float(vector.get("risk") or 0)
    leverage = float(vector.get("leverage_ratio") or 0)
    credit = float(vector.get("credit_stability") or 0)
    entropy = float(vector.get("strategy_entropy") or 0)
    memory = float(vector.get("memory_coherence") or 0)
    drift = float(vector.get("behavioral_drift") or 0)
    collapse_probability = float((collapse_prediction or {}).get("collapse_probability") or 0)
    energy = clamp(credit * 0.42 + memory * 0.24 + (1 - collapse_probability) * 0.22 + (1 - leverage) * 0.12)
    tension = clamp(collapse_probability * 0.42 + risk * 0.24 + leverage * 0.18 + drift * 0.16)
    cohesion = clamp(memory * 0.46 + credit * 0.38 + (1 - entropy) * 0.16)
    aggression = clamp(risk * 0.42 + leverage * 0.32 + entropy * 0.18 + max(0.0, energy - 0.55) * 0.08)
    fragility = clamp(collapse_probability * 0.5 + (1 - cohesion) * 0.28 + tension * 0.22)
    return {
        "energy": round(energy, 3),
        "entropy": round(entropy, 3),
        "tension": round(tension, 3),
        "cohesion": round(cohesion, 3),
        "aggression": round(aggression, 3),
        "fragility": round(fragility, 3),
    }


def detect_phase(
    state: dict[str, Any],
    collapse_prediction: dict[str, Any] | None = None,
    evolution_prediction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    physical = compute_physical_vector(state, collapse_prediction)
    energy = physical["energy"]
    entropy = physical["entropy"]
    tension = physical["tension"]
    cohesion = physical["cohesion"]
    aggression = physical["aggression"]
    fragility = physical["fragility"]
    if cohesion < 0.32 or fragility >= 0.74:
        phase = "COLLAPSE"
        trigger = "low_cohesion_or_high_fragility"
    elif entropy >= 0.74 and tension >= 0.62:
        phase = "CRITICAL"
        trigger = "entropy_tension_spike"
    elif energy >= 0.72 and aggression >= 0.62:
        phase = "EXPANSION"
        trigger = "energy_aggression_burst"
    elif entropy >= 0.58 or tension >= 0.56:
        phase = "VOLATILE"
        trigger = "volatility_pressure"
    elif tension >= 0.34 or (evolution_prediction or {}).get("evolution_path") == "optimization":
        phase = "ADAPTIVE"
        trigger = "adaptive_pressure"
    else:
        phase = "STABLE"
        trigger = "cohesive_low_pressure"
    return {
        "civilization_id": state.get("civilization_id"),
        "label": state.get("label"),
        "phase": phase,
        "phase_label": _label_for_phase(phase),
        "transition": _transition_for_phase(phase),
        "trigger": trigger,
        "physical_vector": physical,
        "reading": _phase_reading(state, phase, trigger),
    }


def _phase_reading(state: dict[str, Any], phase: str, trigger: str) -> str:
    label = state.get("label") or state.get("civilization_id")
    if phase == "COLLAPSE":
        return f"{label} 已进入崩溃观察区，关键触发来自 {trigger}。"
    if phase == "CRITICAL":
        return f"{label} 处于临界态，熵增和压力可能导致下一轮结构跃迁。"
    if phase == "EXPANSION":
        return f"{label} 具备扩张冲动，短期可能提高风险暴露。"
    if phase == "VOLATILE":
        return f"{label} 进入波动态，策略会更容易被输赢结果扰动。"
    if phase == "ADAPTIVE":
        return f"{label} 正处于适应优化期，记忆与压力会共同塑造下一轮决策。"
    return f"{label} 结构稳定，当前更像低压巩固状态。"


def detect_phase_transitions(
    states: list[dict[str, Any]],
    collapse_predictions: list[dict[str, Any]],
    evolution_predictions: list[dict[str, Any]],
) -> dict[str, Any]:
    collapse_by_id = {row.get("civilization_id"): row for row in collapse_predictions}
    evolution_by_id = {row.get("civilization_id"): row for row in evolution_predictions}
    phases = [
        detect_phase(
            state,
            collapse_by_id.get(state.get("civilization_id")),
            evolution_by_id.get(state.get("civilization_id")),
        )
        for state in states
    ]
    critical = [row for row in phases if row.get("phase") in {"CRITICAL", "COLLAPSE"}]
    expansion = [row for row in phases if row.get("phase") == "EXPANSION"]
    return {
        "version": "phase_transition_engine.v1",
        "phases": phases,
        "critical_count": len(critical),
        "expansion_count": len(expansion),
        "state_flow": ["Stable", "Adaptive", "Volatile", "Critical", "Collapse or Expansion"],
    }
