from __future__ import annotations

from collections import Counter
from typing import Any

from .civilization_state_engine import clamp
from .rules_engine import n


PHASE_CLUSTERS = {
    "STABLE": "stable_cluster",
    "ADAPTIVE": "stable_cluster",
    "VOLATILE": "volatile_cluster",
    "CRITICAL": "volatile_cluster",
    "COLLAPSE": "collapsing_cluster",
    "EXPANSION": "expansion_cluster",
}


def _cluster_for(phase: str) -> str:
    return PHASE_CLUSTERS.get(str(phase or "STABLE"), "stable_cluster")


def _avg(rows: list[dict[str, Any]], key: str) -> float:
    if not rows:
        return 0.0
    return round(sum(n((row.get("physical_vector") or {}).get(key)) for row in rows) / len(rows), 3)


def _collapse_by_id(collapse_predictor: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("civilization_id")): row
        for row in (collapse_predictor.get("predictions") or [])
    }


def _memory_by_id(memory_dynamics: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("civilization_id")): row
        for row in (memory_dynamics.get("civilizations") or [])
    }


def _build_clusters(phase_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in phase_rows:
        grouped.setdefault(_cluster_for(str(row.get("phase"))), []).append(row)
    clusters = []
    for cluster_id, rows in sorted(grouped.items()):
        phases = Counter(str(row.get("phase") or "UNKNOWN") for row in rows)
        clusters.append({
            "cluster_id": cluster_id,
            "civilization_ids": [str(row.get("civilization_id")) for row in rows],
            "civilization_count": len(rows),
            "phase_counts": dict(sorted(phases.items())),
            "avg_vector": {
                "energy": _avg(rows, "energy"),
                "entropy": _avg(rows, "entropy"),
                "tension": _avg(rows, "tension"),
                "cohesion": _avg(rows, "cohesion"),
                "aggression": _avg(rows, "aggression"),
                "fragility": _avg(rows, "fragility"),
            },
            "reading": _cluster_reading(cluster_id, rows),
        })
    return clusters


def _cluster_reading(cluster_id: str, rows: list[dict[str, Any]]) -> str:
    count = len(rows)
    if cluster_id == "collapsing_cluster":
        return f"{count} 个文明进入崩溃观察，元文明层需要关注连锁风险。"
    if cluster_id == "volatile_cluster":
        return f"{count} 个文明处在波动/临界区，是系统性相变的主要来源。"
    if cluster_id == "expansion_cluster":
        return f"{count} 个文明具备扩张态，短期可能放大交互场压力。"
    return f"{count} 个文明处在稳定/适应区，构成系统的低熵基础。"


def _systemic_wave(
    phase_rows: list[dict[str, Any]],
    war_engine: dict[str, Any],
    collapse_predictor: dict[str, Any],
) -> dict[str, Any]:
    collapse_by_id = _collapse_by_id(collapse_predictor)
    if not phase_rows:
        return {
            "wave_probability": 0.0,
            "level": "low",
            "drivers": [],
            "reading": "暂无文明相变数据，无法形成系统性崩溃波判断。",
        }
    critical = [row for row in phase_rows if row.get("phase") in {"CRITICAL", "COLLAPSE"}]
    avg_collapse = sum(n(collapse_by_id.get(str(row.get("civilization_id")), {}).get("collapse_probability")) for row in phase_rows) / len(phase_rows)
    triggered_wars = [row for row in (war_engine.get("battles") or []) if row.get("phase_shift") not in {"low_phase_shift", None, ""}]
    avg_fragility = sum(n((row.get("physical_vector") or {}).get("fragility")) for row in phase_rows) / len(phase_rows)
    probability = clamp(avg_collapse * 0.42 + (len(critical) / len(phase_rows)) * 0.28 + min(1.0, len(triggered_wars) / 3) * 0.18 + avg_fragility * 0.12)
    if probability >= 0.7:
        level = "high"
    elif probability >= 0.4:
        level = "medium"
    else:
        level = "low"
    drivers = []
    if critical:
        drivers.append("critical_or_collapse_phases")
    if triggered_wars:
        drivers.append("phase_shifting_war_interactions")
    if avg_fragility >= 0.55:
        drivers.append("high_average_fragility")
    if avg_collapse >= 0.45:
        drivers.append("elevated_collapse_probability")
    return {
        "wave_probability": round(probability, 3),
        "level": level,
        "drivers": drivers,
        "triggered_war_count": len(triggered_wars),
        "critical_civilization_count": len(critical),
        "reading": f"系统性崩溃波概率 {probability:.0%}，等级 {level}；主要驱动：{', '.join(drivers) if drivers else 'low_pressure_baseline'}。",
    }


def _migration_paths(
    phase_rows: list[dict[str, Any]],
    memory_dynamics: dict[str, Any],
    collapse_predictor: dict[str, Any],
) -> list[dict[str, Any]]:
    memory_by_id = _memory_by_id(memory_dynamics)
    collapse_by_id = _collapse_by_id(collapse_predictor)
    paths = []
    for row in phase_rows:
        civ_id = str(row.get("civilization_id"))
        phase = str(row.get("phase") or "STABLE")
        memory = memory_by_id.get(civ_id, {})
        collapse = n(collapse_by_id.get(civ_id, {}).get("collapse_probability"))
        if phase in {"CRITICAL", "COLLAPSE"} or collapse >= 0.62:
            target = "reconstruction_or_survival_cluster"
        elif phase == "EXPANSION":
            target = "expansion_cluster"
        elif phase == "VOLATILE":
            target = "adaptive_cluster"
        else:
            target = "stable_cluster"
        paths.append({
            "civilization_id": civ_id,
            "from_phase": phase,
            "target_cluster": target,
            "memory_strategy_update": memory.get("strategy_update") or "reuse_high_confidence_patterns",
            "migration_pressure": round(clamp(collapse * 0.5 + n(memory.get("memory_pressure")) * 0.32 + n((row.get("physical_vector") or {}).get("tension")) * 0.18), 3),
        })
    return paths


def build_meta_civilization_physics(
    *,
    phase_rows: list[dict[str, Any]],
    war_engine: dict[str, Any],
    collapse_predictor: dict[str, Any],
    memory_dynamics: dict[str, Any],
) -> dict[str, Any]:
    """Build the system-of-civilizations layer.

    This is a product-level meta model: it clusters civilizations by phase,
    detects possible system-wide collapse waves, and translates memory pressure
    into migration targets for the next run. It never exposes raw bets,
    provider transcripts, or local file paths.
    """

    clusters = _build_clusters(phase_rows)
    wave = _systemic_wave(phase_rows, war_engine, collapse_predictor)
    migration = _migration_paths(phase_rows, memory_dynamics, collapse_predictor)
    dominant = max(clusters, key=lambda row: row["civilization_count"])["cluster_id"] if clusters else "unknown"
    return {
        "version": "meta_civilization_engine.v1",
        "definition": "Meta-Civilization = system of civilizations moving through phase space",
        "state_model": {
            "civilization": "vector in phase space",
            "state_vector": ["energy", "entropy", "tension", "cohesion", "aggression", "fragility"],
            "dynamics": "dC/dt = f(market_pressure, memory_field, interaction_field, internal_strategy)",
        },
        "clusters": clusters,
        "dominant_cluster": dominant,
        "systemic_collapse_wave": wave,
        "migration_paths": migration,
        "interaction_field": {
            "battle_count": len(war_engine.get("battles") or []),
            "headline": war_engine.get("headline_war") or {},
            "meaning": "civilization field interactions can trigger phase migration, not real-world conflict",
        },
        "production_contract": {
            "no_raw_provider_trace": True,
            "no_real_world_war_claim": True,
            "product_metaphor_only": True,
            "meta_layer_visible": True,
        },
        "final_loop": [
            "events",
            "state_engine",
            "phase_transition",
            "interaction_field",
            "war_engine",
            "collapse_predictor",
            "meta_layer_analysis",
            "replay_engine",
            "next_run",
        ],
    }
