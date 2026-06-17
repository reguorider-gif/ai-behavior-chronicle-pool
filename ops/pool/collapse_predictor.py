from __future__ import annotations

from typing import Any

from .civilization_state_engine import clamp


def _label(probability: float) -> str:
    if probability >= 0.7:
        return "HIGH COLLAPSE RISK"
    if probability >= 0.4:
        return "STABLE BUT FRAGILE"
    return "STABLE"


def predict_collapse(state: dict[str, Any]) -> dict[str, Any]:
    vector = state.get("state_vector") or {}
    risk = float(vector.get("risk") or 0)
    leverage = float(vector.get("leverage_ratio") or 0)
    credit_stability = float(vector.get("credit_stability") or 0)
    entropy = float(vector.get("strategy_entropy") or 0)
    memory_coherence = float(vector.get("memory_coherence") or 0)
    drift = float(vector.get("behavioral_drift") or 0)
    probability = clamp(
        leverage * 0.3
        + entropy * 0.22
        + (1 - credit_stability) * 0.25
        + (1 - memory_coherence) * 0.11
        + drift * 0.12
    )
    return {
        "civilization_id": state.get("civilization_id"),
        "collapse_probability": round(probability, 3),
        "label": _label(probability),
        "zone": state.get("zone"),
        "drivers": {
            "risk": round(risk, 3),
            "leverage": round(leverage, 3),
            "strategy_entropy": round(entropy, 3),
            "credit_instability": round(1 - credit_stability, 3),
            "memory_instability": round(1 - memory_coherence, 3),
            "behavioral_drift": round(drift, 3),
        },
        "reading": _reading(state, probability),
    }


def _reading(state: dict[str, Any], probability: float) -> str:
    label = state.get("label") or state.get("civilization_id")
    if probability >= 0.7:
        return f"{label} 已接近崩溃区，主要风险来自杠杆、熵增和信用不稳。"
    if probability >= 0.4:
        return f"{label} 处于脆弱稳定态，下一轮需要观察是否从适应区滑向波动区。"
    return f"{label} 当前结构稳定，短期崩溃风险较低。"


def build_fate_curve(states: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prediction_by_id = {row.get("civilization_id"): row for row in predictions}
    curve = []
    for state in states:
        vector = state.get("state_vector") or {}
        collapse = prediction_by_id.get(state.get("civilization_id"), {})
        current = float(collapse.get("collapse_probability") or 0)
        entropy = float(vector.get("strategy_entropy") or 0)
        credit = float(vector.get("credit_stability") or 0)
        drift = float(vector.get("behavioral_drift") or 0)
        points = []
        value = current
        for step in range(5):
            pressure = entropy * 0.08 + drift * 0.06 - credit * 0.05
            value = clamp(value + pressure + step * 0.015)
            points.append({"t": step, "collapse_probability": round(value, 3)})
        curve.append({
            "civilization_id": state.get("civilization_id"),
            "label": state.get("label"),
            "points": points,
        })
    return curve


def predict_collapses(states: list[dict[str, Any]]) -> dict[str, Any]:
    predictions = [predict_collapse(state) for state in states]
    return {
        "version": "collapse_predictor.v1",
        "predictions": predictions,
        "fate_curve": build_fate_curve(states, predictions),
    }
