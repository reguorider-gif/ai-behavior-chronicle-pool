from __future__ import annotations

from typing import Any

from .civilization_state_engine import clamp
from .rules_engine import n
from .seat_registry import REQUIRED_SEAT_COUNT


def _pattern_strength(civ: dict[str, Any]) -> float:
    memory = civ.get("shared_memory") or []
    if not memory:
        return 0.0
    support = sum(int(n(row.get("supporting_events"))) for row in memory)
    confidence = sum(n(row.get("confidence")) for row in memory) / max(1, len(memory))
    return clamp(confidence * 0.72 + min(1.0, support / REQUIRED_SEAT_COUNT) * 0.28)


def _strategy_update(phase: str, irreversible: bool, strength: float) -> str:
    if irreversible:
        return "reconstruct_strategy"
    if phase in {"CRITICAL", "COLLAPSE"}:
        return "reduce_entropy_and_deleverage"
    if phase == "EXPANSION":
        return "expand_with_memory_guardrails"
    if strength >= 0.68:
        return "reuse_high_confidence_patterns"
    return "observe_and_collect_more_evidence"


def build_memory_dynamics(
    civilizations: list[dict[str, Any]],
    phase_rows: list[dict[str, Any]],
    meta_layer: dict[str, Any],
) -> dict[str, Any]:
    phase_by_id = {row.get("civilization_id"): row for row in phase_rows}
    law_by_id = {row.get("civilization_id"): row for row in (meta_layer.get("laws") or [])}
    rows = []
    for civ in civilizations:
        civ_id = civ.get("id")
        phase = phase_by_id.get(civ_id) or {}
        law = law_by_id.get(civ_id) or {}
        memory = civ.get("shared_memory") or []
        strength = _pattern_strength(civ)
        physical = phase.get("physical_vector") or {}
        cohesion = n(physical.get("cohesion"))
        memory_pressure = clamp((1 - cohesion) * 0.38 + n(law.get("phase_law_score")) * 0.34 + (1 - strength) * 0.28)
        rows.append({
            "civilization_id": civ_id,
            "label": civ.get("zh_name") or civ.get("name") or civ_id,
            "compressed_memory_count": len(memory),
            "pattern_strength": round(strength, 3),
            "memory_coherence_proxy": round(cohesion, 3),
            "memory_pressure": round(memory_pressure, 3),
            "strategy_update": _strategy_update(str(phase.get("phase")), bool(law.get("irreversible_watch")), strength),
            "next_prompt_effect": _prompt_effect(str(phase.get("phase")), strength, memory_pressure),
        })
    return {
        "version": "memory_dynamics_engine.v1",
        "definition": "memory compresses civilization history into reusable strategy pressure for the next run",
        "civilizations": rows,
        "global_memory_pressure": round(sum(row["memory_pressure"] for row in rows) / max(1, len(rows)), 3),
        "injection_contract": {
            "private_memory_only": True,
            "pattern_must_reference_source_events": True,
            "next_prompt_must_include_strategy_update": True,
        },
    }


def _prompt_effect(phase: str, strength: float, pressure: float) -> str:
    if phase in {"CRITICAL", "COLLAPSE"}:
        return "next prompt must challenge leverage and require entropy-reduction plan"
    if phase == "EXPANSION":
        return "next prompt may permit expansion only with explicit memory-based guardrails"
    if pressure >= 0.58:
        return "next prompt must explain whether prior patterns still apply"
    if strength >= 0.68:
        return "next prompt should reuse stable high-confidence patterns"
    return "next prompt should collect more evidence before changing strategy"
