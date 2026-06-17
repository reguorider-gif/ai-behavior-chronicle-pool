from __future__ import annotations

from typing import Any

from .rules_engine import n


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _level(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def _avg_pattern_confidence(civ: dict[str, Any]) -> float:
    patterns = civ.get("shared_memory") or []
    if not patterns:
        return 0.0
    return sum(n(row.get("confidence")) for row in patterns) / max(1, len(patterns))


def compute_state(civ: dict[str, Any], drift_row: dict[str, Any] | None = None) -> dict[str, Any]:
    """Convert a civilization into a dynamic state vector.

    This is intentionally product-level: it uses normalized indices from the
    existing behavior/civilization objects and never exposes raw bets or logs.
    """

    perf = civ.get("performance") or {}
    risk = civ.get("shared_risk_profile") or {}
    memory_count = len(civ.get("shared_memory") or [])
    risk_score = clamp(n(risk.get("risk_score")))
    leverage_ratio = clamp(n(risk.get("loan_score")))
    survival = clamp(n(perf.get("survival_score")))
    stability = clamp(n(perf.get("stability_score")))
    volatility = clamp(n(perf.get("volatility_score")))
    drift = clamp(n((drift_row or {}).get("drift_rate")))
    pattern_confidence = clamp(_avg_pattern_confidence(civ))
    strategy_entropy = clamp(volatility * 0.44 + drift * 0.28 + min(1.0, memory_count / 5) * 0.12 + risk_score * 0.16)
    memory_coherence = clamp(pattern_confidence * 0.58 + min(1.0, memory_count / 4) * 0.22 + stability * 0.2)
    credit_stability = clamp(stability * 0.48 + survival * 0.38 + (1 - leverage_ratio) * 0.14)
    if credit_stability >= 0.72 and strategy_entropy < 0.42:
        zone = "stable_zone"
    elif strategy_entropy >= 0.68 or risk_score >= 0.78:
        zone = "volatile_zone"
    elif credit_stability < 0.42 and leverage_ratio >= 0.56:
        zone = "collapse_zone"
    else:
        zone = "adaptive_zone"
    return {
        "civilization_id": civ.get("id"),
        "label": civ.get("zh_name") or civ.get("name") or civ.get("id"),
        "risk_level": _level(risk_score),
        "state_vector": {
            "risk": round(risk_score, 3),
            "leverage_ratio": round(leverage_ratio, 3),
            "credit_stability": round(credit_stability, 3),
            "strategy_entropy": round(strategy_entropy, 3),
            "memory_coherence": round(memory_coherence, 3),
            "behavioral_drift": round(drift, 3),
        },
        "zone": zone,
        "zone_label": {
            "stable_zone": "Stable Zone",
            "adaptive_zone": "Adaptive Zone",
            "volatile_zone": "Volatile Zone",
            "collapse_zone": "Collapse Zone",
        }[zone],
    }


def compute_states(civilizations: list[dict[str, Any]], drift_engine: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    drift_by_id = {
        row.get("civilization_id"): row
        for row in ((drift_engine or {}).get("civilizations") or [])
    }
    return [compute_state(civ, drift_by_id.get(civ.get("id"))) for civ in civilizations]
