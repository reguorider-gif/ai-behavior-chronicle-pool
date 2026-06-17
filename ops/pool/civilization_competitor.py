from __future__ import annotations

from itertools import combinations
from typing import Any


def _score(state: dict[str, Any], collapse: dict[str, Any] | None, evolution: dict[str, Any] | None) -> float:
    vector = state.get("state_vector") or {}
    stability = float(vector.get("credit_stability") or 0)
    survival = 1 - float((collapse or {}).get("collapse_probability") or 0)
    adaptability = 1 - abs(0.5 - float(vector.get("strategy_entropy") or 0)) * 2
    if (evolution or {}).get("evolution_path") == "optimization":
        adaptability = min(1.0, adaptability + 0.12)
    if (evolution or {}).get("evolution_path") == "fragmentation":
        adaptability = max(0.0, adaptability - 0.18)
    return round(stability * 0.4 + survival * 0.3 + adaptability * 0.3, 3)


def compete_pair(
    a: dict[str, Any],
    b: dict[str, Any],
    collapse_by_id: dict[str, dict[str, Any]],
    evolution_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    a_id = a.get("civilization_id")
    b_id = b.get("civilization_id")
    a_score = _score(a, collapse_by_id.get(a_id), evolution_by_id.get(a_id))
    b_score = _score(b, collapse_by_id.get(b_id), evolution_by_id.get(b_id))
    if a_score == b_score:
        winner = "draw"
    else:
        winner = a_id if a_score > b_score else b_id
    return {
        "id": f"{a_id}__dynamic_vs__{b_id}",
        "civilizations": [a_id, b_id],
        "winner": winner,
        "gap": round(abs(a_score - b_score), 3),
        "scores": {
            str(a_id): a_score,
            str(b_id): b_score,
        },
        "metrics": {
            "stability": {
                str(a_id): round(float((a.get("state_vector") or {}).get("credit_stability") or 0), 3),
                str(b_id): round(float((b.get("state_vector") or {}).get("credit_stability") or 0), 3),
            },
            "survival": {
                str(a_id): round(1 - float((collapse_by_id.get(a_id) or {}).get("collapse_probability") or 0), 3),
                str(b_id): round(1 - float((collapse_by_id.get(b_id) or {}).get("collapse_probability") or 0), 3),
            },
        },
    }


def compete_civilizations(
    states: list[dict[str, Any]],
    collapse_predictions: list[dict[str, Any]],
    evolution_predictions: list[dict[str, Any]],
) -> dict[str, Any]:
    collapse_by_id = {row.get("civilization_id"): row for row in collapse_predictions}
    evolution_by_id = {row.get("civilization_id"): row for row in evolution_predictions}
    rows = [
        compete_pair(a, b, collapse_by_id, evolution_by_id)
        for a, b in combinations(states, 2)
    ]
    leaders: dict[str, float] = {}
    for state in states:
        civ_id = str(state.get("civilization_id"))
        leaders[civ_id] = _score(state, collapse_by_id.get(civ_id), evolution_by_id.get(civ_id))
    long_term_winner = max(leaders, key=leaders.get) if leaders else None
    return {
        "version": "civilization_competitor.v1",
        "comparisons": rows,
        "long_term_winner": long_term_winner,
        "scores": leaders,
    }
