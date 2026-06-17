from __future__ import annotations

from typing import Any


def predict_evolution(state: dict[str, Any], collapse_prediction: dict[str, Any] | None = None) -> dict[str, Any]:
    vector = state.get("state_vector") or {}
    entropy = float(vector.get("strategy_entropy") or 0)
    credit = float(vector.get("credit_stability") or 0)
    drift = float(vector.get("behavioral_drift") or 0)
    collapse_probability = float((collapse_prediction or {}).get("collapse_probability") or 0)
    if collapse_probability >= 0.7 or state.get("zone") == "collapse_zone":
        path = "fragmentation"
        lifecycle = "collapse_watch"
    elif entropy >= 0.62 or drift >= 0.5:
        path = "optimization"
        lifecycle = "adaptive_instability"
    elif credit >= 0.72:
        path = "consolidation"
        lifecycle = "stabilization"
    else:
        path = "optimization"
        lifecycle = "growth"
    return {
        "civilization_id": state.get("civilization_id"),
        "evolution_path": path,
        "lifecycle_stage": lifecycle,
        "state_flow": _state_flow(lifecycle),
        "reading": _reading(state, path, lifecycle),
    }


def _state_flow(lifecycle: str) -> list[str]:
    flows = {
        "stabilization": ["birth", "growth", "peak", "stability"],
        "growth": ["birth", "growth", "adaptive_zone"],
        "adaptive_instability": ["growth", "peak", "volatility", "recovery_or_collapse"],
        "collapse_watch": ["peak", "instability", "collapse_or_reconstruction"],
    }
    return flows.get(lifecycle, ["birth", "growth"])


def _reading(state: dict[str, Any], path: str, lifecycle: str) -> str:
    label = state.get("label") or state.get("civilization_id")
    zh_path = {
        "consolidation": "稳定巩固",
        "optimization": "适应优化",
        "fragmentation": "分裂/崩溃观察",
    }.get(path, path)
    return f"{label} 当前进化路径为{zh_path}，生命周期阶段为 {lifecycle}。"


def predict_evolutions(states: list[dict[str, Any]], collapse_predictions: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {row.get("civilization_id"): row for row in collapse_predictions}
    rows = [predict_evolution(state, by_id.get(state.get("civilization_id"))) for state in states]
    return {
        "version": "evolution_engine.v1",
        "predictions": rows,
        "phase_transition_watch": [
            row for row in rows
            if row.get("lifecycle_stage") in {"adaptive_instability", "collapse_watch"}
        ],
    }
