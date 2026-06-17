from __future__ import annotations

from typing import Any


def _phase_score(physical: dict[str, Any]) -> float:
    entropy = float(physical.get("entropy") or 0)
    tension = float(physical.get("tension") or 0)
    aggression = float(physical.get("aggression") or 0)
    cohesion = float(physical.get("cohesion") or 0)
    fragility = float(physical.get("fragility") or 0)
    return round(max(0.0, min(1.0, entropy * 0.3 + tension * 0.3 + aggression * 0.2 + fragility * 0.2 - cohesion * 0.2)), 3)


def _dominant_driver(physical: dict[str, Any]) -> str:
    candidates = {
        "entropy": float(physical.get("entropy") or 0),
        "tension": float(physical.get("tension") or 0),
        "aggression": float(physical.get("aggression") or 0),
        "fragility": float(physical.get("fragility") or 0),
        "low_cohesion": 1 - float(physical.get("cohesion") or 0),
    }
    return max(candidates, key=candidates.get)


def _law_label(score: float, phase: str) -> str:
    if phase == "COLLAPSE" or score >= 0.76:
        return "critical_phase_law"
    if phase == "EXPANSION":
        return "expansion_phase_law"
    if phase == "CRITICAL":
        return "critical_transition_law"
    if phase == "VOLATILE":
        return "volatility_amplification_law"
    return "stability_or_adaptation_law"


def _irreversible_watch(score: float, physical: dict[str, Any], trigger_count: int) -> bool:
    fragility = float(physical.get("fragility") or 0)
    cohesion = float(physical.get("cohesion") or 0)
    return score >= 0.72 or fragility >= 0.72 or (trigger_count >= 2 and cohesion < 0.48)


def build_civilization_meta_layer(
    phase_rows: list[dict[str, Any]],
    war_phase: dict[str, Any],
) -> dict[str, Any]:
    triggers = war_phase.get("triggers") or []
    triggers_by_civ: dict[str, list[dict[str, Any]]] = {}
    for trigger in triggers:
        for civ_id in trigger.get("civilizations") or []:
            triggers_by_civ.setdefault(str(civ_id), []).append(trigger)
    laws = []
    irreversible = []
    for row in phase_rows:
        civ_id = str(row.get("civilization_id"))
        physical = row.get("physical_vector") or {}
        score = _phase_score(physical)
        trigger_rows = triggers_by_civ.get(civ_id, [])
        law = {
            "civilization_id": civ_id,
            "label": row.get("label"),
            "phase": row.get("phase"),
            "phase_law_score": score,
            "law": _law_label(score, str(row.get("phase"))),
            "dominant_driver": _dominant_driver(physical),
            "war_trigger_count": sum(1 for trigger in trigger_rows if trigger.get("triggered")),
            "irreversible_watch": _irreversible_watch(score, physical, len(trigger_rows)),
            "why": _why(row, score, trigger_rows),
        }
        laws.append(law)
        if law["irreversible_watch"]:
            irreversible.append(law)
    return {
        "version": "civilization_meta_layer.v1",
        "definition": "civilization = dynamic phase system in a multi-agent behavioral field",
        "phase_law": "entropy*0.3 + tension*0.3 + aggression*0.2 + fragility*0.2 - cohesion*0.2",
        "laws": laws,
        "irreversible_watch": irreversible,
        "why_phase_changes": [
            {
                "civilization_id": row["civilization_id"],
                "why": row["why"],
                "dominant_driver": row["dominant_driver"],
                "law": row["law"],
            }
            for row in laws
        ],
        "next_observation_questions": [
            "战争交互是否把高熵文明推入不可逆崩溃区？",
            "扩张文明是否会因为胜出而提高下一轮风险暴露？",
            "稳定文明能否在外部压力下保持低熵和高凝聚？",
        ],
    }


def _why(row: dict[str, Any], score: float, triggers: list[dict[str, Any]]) -> str:
    label = row.get("label") or row.get("civilization_id")
    phase = row.get("phase")
    driver = _dominant_driver(row.get("physical_vector") or {})
    trigger_count = sum(1 for trigger in triggers if trigger.get("triggered"))
    if trigger_count:
        return f"{label} 的相变分数为 {score:.2f}，主驱动是 {driver}，且受到 {trigger_count} 个战争触发器影响，因此当前 {phase} 不是静态标签，而是外部交互后的结果。"
    return f"{label} 的相变分数为 {score:.2f}，主驱动是 {driver}；当前 {phase} 主要来自自身状态向量，还没有明显战争触发。"
