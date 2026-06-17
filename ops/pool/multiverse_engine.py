from __future__ import annotations

from collections import Counter
from typing import Any

from .civilization_state_engine import clamp
from .rules_engine import n


def _node_energy(node: dict[str, Any]) -> float:
    vector = node.get("field_vector") or {}
    return round(clamp(n(vector.get("energy")) * 0.58 + n(node.get("field_strength")) * 0.42), 3)


def _node_entropy_drift(node: dict[str, Any]) -> float:
    vector = node.get("field_vector") or {}
    return round(clamp(n(vector.get("entropy")) * 0.44 + n(vector.get("tension")) * 0.34 + n(vector.get("fragility")) * 0.22), 3)


def _phase_state(node: dict[str, Any]) -> str:
    phase = str(node.get("phase") or "").upper()
    zone = str(node.get("zone") or "")
    if phase in {"COLLAPSE", "CRITICAL"} or zone == "collapse_zone":
        return "critical"
    if phase == "EXPANSION" or zone == "expansion_zone":
        return "expansion"
    if zone == "adaptive_zone":
        return "adaptive"
    if zone == "volatile_zone":
        return "volatile"
    return "stable"


def _multiverse_nodes(universe: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for node in universe.get("nodes") or []:
        civ_id = str(node.get("civilization_id") or "")
        rows.append({
            "civilization_id": civ_id,
            "label": node.get("label") or civ_id,
            "phase_state": _phase_state(node),
            "zone": node.get("zone") or "stable_zone",
            "energy": _node_energy(node),
            "entropy_drift": _node_entropy_drift(node),
            "field_strength": node.get("field_strength") or 0,
            "position": node.get("position") or {},
            "meaning": "node=civilization, size=energy, color=phase state, motion=entropy drift",
        })
    return sorted(rows, key=lambda row: (row["energy"], -row["entropy_drift"]), reverse=True)


def _coupling_force(edge: dict[str, Any]) -> float:
    return round(clamp(
        n(edge.get("field_overlap")) * 0.38
        + n(edge.get("phase_pressure")) * 0.36
        + (0.18 if edge.get("result") == "dominates_field" else 0.08)
        + (0.08 if edge.get("dominant") != "balanced_field" else 0.0)
    ), 3)


def _couplings(universe: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for edge in universe.get("edges") or []:
        civs = edge.get("civilizations") or []
        rows.append({
            "id": edge.get("id"),
            "civilizations": civs,
            "coupling_force": _coupling_force(edge),
            "field_overlap": edge.get("field_overlap") or 0,
            "phase_pressure": edge.get("phase_pressure") or 0,
            "dominant": edge.get("dominant") or "balanced_field",
            "interaction_result": edge.get("result") or "co-evolution",
            "reading": _coupling_reading(edge),
        })
    return sorted(rows, key=lambda row: row["coupling_force"], reverse=True)


def _coupling_reading(edge: dict[str, Any]) -> str:
    civs = edge.get("civilizations") or []
    label = " / ".join(str(item) for item in civs)
    dominant = edge.get("dominant") or "balanced_field"
    if dominant == "balanced_field":
        return f"{label} 当前处于共演耦合，下一轮重点看记忆场是否打破平衡。"
    return f"{label} 的耦合场由 {dominant} 占优，下一轮观察是否形成扩张或崩溃压力。"


def _dominance_cluster(nodes: list[dict[str, Any]], couplings: list[dict[str, Any]]) -> dict[str, Any]:
    if not nodes:
        return {"dominant_civilization": None, "cluster_type": "empty", "members": []}
    counts = Counter(row["dominant"] for row in couplings if row.get("dominant") and row.get("dominant") != "balanced_field")
    if counts:
        dominant = counts.most_common(1)[0][0]
    else:
        dominant = max(nodes, key=lambda row: row["energy"])["civilization_id"]
    members = sorted({
        civ
        for row in couplings
        if row.get("dominant") == dominant
        for civ in (row.get("civilizations") or [])
    }) or [dominant]
    dominant_node = next((row for row in nodes if row["civilization_id"] == dominant), {})
    return {
        "dominant_civilization": dominant,
        "cluster_type": _cluster_type(dominant_node),
        "members": members,
        "coupling_count": counts.get(dominant, 0),
        "reading": f"{dominant} 形成当前主导簇；其优势来自能量、记忆深度与耦合压力的综合场。",
    }


def _cluster_type(node: dict[str, Any]) -> str:
    phase = node.get("phase_state")
    if phase == "critical":
        return "fragile_dominance_cluster"
    if phase == "expansion":
        return "expansion_cluster"
    if phase == "adaptive":
        return "adaptive_memory_cluster"
    return "stable_cluster"


def _memory_field(memory_dynamics: dict[str, Any], couplings: list[dict[str, Any]]) -> dict[str, Any]:
    pressure = n(memory_dynamics.get("global_memory_pressure"))
    high_coupling = sum(1 for row in couplings if row.get("coupling_force", 0) >= 0.62)
    return {
        "global_memory_pressure": round(pressure, 3),
        "field_level": "high" if pressure >= 0.62 else ("medium" if pressure >= 0.36 else "low"),
        "high_coupling_count": high_coupling,
        "compress_all_history": True,
        "next_prompt_effect": _memory_effect(pressure, high_coupling),
    }


def _memory_effect(pressure: float, high_coupling: int) -> str:
    if pressure >= 0.62 or high_coupling >= 2:
        return "下一轮 prompt 必须注入跨文明记忆场，并要求模型解释是否被主导簇影响。"
    if pressure >= 0.36:
        return "下一轮 prompt 应提示模型复用有效模式，但保留独立判断。"
    return "下一轮 prompt 以轻量记忆提醒为主，避免过度历史锚定。"


def _drift_timeline(universe: dict[str, Any], nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["civilization_id"]: row for row in nodes}
    rows = []
    for item in universe.get("evolution_tree") or []:
        civ_id = str(item.get("civilization_id") or "")
        node = by_id.get(civ_id, {})
        branches = item.get("branches") or []
        current = item.get("phenotype") or "mixed_line"
        next_branch = branches[0] if branches else current
        rows.append({
            "civilization_id": civ_id,
            "current_line": current,
            "next_line": next_branch,
            "phase_state": node.get("phase_state") or "stable",
            "entropy_drift": node.get("entropy_drift") or 0,
            "reading": f"{civ_id}: {current} → {next_branch}，当前相位 {node.get('phase_state') or 'stable'}。",
        })
    return rows


def _phase_overlay(universe: dict[str, Any], nodes: list[dict[str, Any]]) -> dict[str, Any]:
    overlay = universe.get("phase_field_overlay") or {}
    return {
        "entropy_field": overlay.get("entropy_field") or 0,
        "tension_field": overlay.get("tension_field") or 0,
        "collapse_zones": overlay.get("collapse_zones") or [],
        "critical_nodes": [row["civilization_id"] for row in nodes if row.get("phase_state") == "critical"],
    }


def build_multiverse_engine(
    *,
    universe: dict[str, Any],
    meta_civilization: dict[str, Any],
    memory_dynamics: dict[str, Any],
) -> dict[str, Any]:
    nodes = _multiverse_nodes(universe)
    couplings = _couplings(universe)
    return {
        "version": "multiverse_engine.v1",
        "definition": "Multiverse = coupled universe field of civilizations, memory, phase pressure, and dominance clusters",
        "equation": "dC/dt = Phi(interaction_field, memory_field, economic_constraints, cross_universe_coupling)",
        "state_vector": ["energy", "entropy", "tension", "cohesion", "aggression", "fragility", "adaptation", "memory_depth"],
        "nodes": nodes,
        "couplings": couplings,
        "dominance_cluster": _dominance_cluster(nodes, couplings),
        "memory_field": _memory_field(memory_dynamics, couplings),
        "drift_timeline": _drift_timeline(universe, nodes),
        "phase_overlay": _phase_overlay(universe, nodes),
        "meta_context": {
            "clusters": meta_civilization.get("clusters") or [],
            "migration_paths": meta_civilization.get("migration_paths") or [],
            "systemic_collapse_wave": meta_civilization.get("systemic_collapse_wave") or {},
        },
        "production_contract": {
            "abstract_behavior_model": True,
            "no_raw_bets_or_paths": True,
            "cross_universe_coupling_enabled": True,
            "memory_field_updates_next_prompt": True,
            "not_financial_or_gambling_advice": True,
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
