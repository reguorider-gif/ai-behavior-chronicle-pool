from __future__ import annotations

from itertools import combinations
from typing import Any

from .civilization_state_engine import clamp
from .rules_engine import n


def _phase_by_id(phase_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("civilization_id")): row for row in phase_rows}


def _genome_by_id(genome_engine: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("civilization_id")): row
        for row in (genome_engine.get("civilizations") or [])
    }


def _field_vector(phase_row: dict[str, Any], genome_row: dict[str, Any]) -> dict[str, float]:
    physical = phase_row.get("physical_vector") or {}
    genome = genome_row.get("genome") or {}
    energy = n(physical.get("energy"))
    entropy = n(physical.get("entropy"))
    tension = n(physical.get("tension"))
    cohesion = n(physical.get("cohesion"))
    aggression = n(physical.get("aggression"))
    fragility = n(physical.get("fragility"))
    adaptation = n(genome.get("adaptation_gene"))
    memory_depth = n(genome.get("memory_gene"))
    return {
        "energy": round(energy, 3),
        "entropy": round(entropy, 3),
        "tension": round(tension, 3),
        "cohesion": round(cohesion, 3),
        "aggression": round(aggression, 3),
        "fragility": round(fragility, 3),
        "adaptation": round(adaptation, 3),
        "memory_depth": round(memory_depth, 3),
    }


def _field_strength(vector: dict[str, float]) -> float:
    return round(clamp(vector["energy"] * 0.24 + vector["cohesion"] * 0.2 + vector["adaptation"] * 0.18 + vector["memory_depth"] * 0.16 + vector["aggression"] * 0.12 + (1 - vector["fragility"]) * 0.1), 3)


def _phase_zone(vector: dict[str, float]) -> str:
    if vector["fragility"] >= 0.72 or (vector["entropy"] + vector["tension"] - vector["cohesion"]) >= 0.82:
        return "collapse_zone"
    if vector["adaptation"] >= 0.64 and vector["memory_depth"] >= 0.58:
        return "adaptive_zone"
    if vector["aggression"] >= 0.62 and vector["energy"] >= 0.58:
        return "expansion_zone"
    if vector["entropy"] >= 0.58:
        return "volatile_zone"
    return "stable_zone"


def _universe_nodes(phase_rows: list[dict[str, Any]], genome_engine: dict[str, Any]) -> list[dict[str, Any]]:
    genomes = _genome_by_id(genome_engine)
    nodes = []
    for row in phase_rows:
        civ_id = str(row.get("civilization_id"))
        genome = genomes.get(civ_id, {})
        vector = _field_vector(row, genome)
        nodes.append({
            "civilization_id": civ_id,
            "label": row.get("label") or civ_id,
            "phase": row.get("phase") or "UNKNOWN",
            "phenotype": genome.get("phenotype") or "mixed_line",
            "field_vector": vector,
            "field_strength": _field_strength(vector),
            "zone": _phase_zone(vector),
            "position": {
                "x": round(clamp(vector["entropy"] * 0.58 + vector["aggression"] * 0.42), 3),
                "y": round(clamp(vector["tension"] * 0.52 + vector["fragility"] * 0.28 + (1 - vector["cohesion"]) * 0.2), 3),
                "size": round(clamp(0.18 + vector["energy"] * 0.44 + vector["memory_depth"] * 0.24), 3),
            },
        })
    return nodes


def _overlap(a: dict[str, Any], b: dict[str, Any]) -> float:
    av = a.get("field_vector") or {}
    bv = b.get("field_vector") or {}
    return round(clamp(
        (1 - abs(n(av.get("energy")) - n(bv.get("energy")))) * 0.18
        + (1 - abs(n(av.get("entropy")) - n(bv.get("entropy")))) * 0.14
        + (1 - abs(n(av.get("tension")) - n(bv.get("tension")))) * 0.14
        + (1 - abs(n(av.get("cohesion")) - n(bv.get("cohesion")))) * 0.14
        + (1 - abs(n(av.get("adaptation")) - n(bv.get("adaptation")))) * 0.18
        + (1 - abs(n(av.get("memory_depth")) - n(bv.get("memory_depth")))) * 0.22
    ), 3)


def _edge_result(a: dict[str, Any], b: dict[str, Any], overlap: float) -> dict[str, Any]:
    a_force = n(a.get("field_strength")) + n((a.get("field_vector") or {}).get("aggression")) * 0.18
    b_force = n(b.get("field_strength")) + n((b.get("field_vector") or {}).get("aggression")) * 0.18
    if abs(a_force - b_force) < 0.035:
        dominant = "balanced_field"
        result = "co-evolution"
    elif a_force > b_force:
        dominant = a["civilization_id"]
        result = "dominates_field"
    else:
        dominant = b["civilization_id"]
        result = "dominates_field"
    return {
        "dominant": dominant,
        "result": result,
        "phase_pressure": round(clamp(overlap * 0.42 + abs(a_force - b_force) * 0.36 + max(n((a.get("field_vector") or {}).get("fragility")), n((b.get("field_vector") or {}).get("fragility"))) * 0.22), 3),
    }


def _edges(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for a, b in combinations(nodes, 2):
        overlap = _overlap(a, b)
        rows.append({
            "id": f"{a['civilization_id']}__universe__{b['civilization_id']}",
            "civilizations": [a["civilization_id"], b["civilization_id"]],
            "field_overlap": overlap,
            **_edge_result(a, b, overlap),
        })
    return sorted(rows, key=lambda row: (row["phase_pressure"], row["field_overlap"]), reverse=True)


def _evolution_tree(genome_engine: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in genome_engine.get("civilizations") or []:
        phenotype = row.get("phenotype") or "mixed_line"
        if phenotype == "stable_line":
            branches = ["stable_line", "adaptive_line"]
        elif phenotype == "aggressive_line":
            branches = ["aggressive_line", "collapse_line", "adaptive_line"]
        elif phenotype == "collapse_line":
            branches = ["collapse_line", "reconstruction_line"]
        elif phenotype == "adaptive_line":
            branches = ["adaptive_line", "stable_line", "aggressive_line"]
        else:
            branches = ["mixed_line", "adaptive_line"]
        rows.append({
            "civilization_id": row.get("civilization_id"),
            "phenotype": phenotype,
            "branches": branches,
            "mutation_pressure": row.get("mutation_pressure"),
            "reading": f"{row.get('label') or row.get('civilization_id')} 当前沿 {phenotype} 演化，下一轮主要分支：{', '.join(branches)}。",
        })
    return rows


def build_universe_engine(
    *,
    phase_rows: list[dict[str, Any]],
    genome_engine: dict[str, Any],
    meta_civilization: dict[str, Any],
) -> dict[str, Any]:
    nodes = _universe_nodes(phase_rows, genome_engine)
    edges = _edges(nodes)
    field_pressure = round(clamp(
        (sum(n(node.get("field_vector", {}).get("entropy")) for node in nodes) / max(1, len(nodes))) * 0.28
        + (sum(n(node.get("field_vector", {}).get("tension")) for node in nodes) / max(1, len(nodes))) * 0.26
        + (sum(n(node.get("field_vector", {}).get("fragility")) for node in nodes) / max(1, len(nodes))) * 0.24
        + n((meta_civilization.get("systemic_collapse_wave") or {}).get("wave_probability")) * 0.22
    ), 3)
    return {
        "version": "universe_engine.v1",
        "definition": "Universe = field of civilizations with genomes, overlaps, phase zones, and evolution branches",
        "state_vector": ["energy", "entropy", "tension", "cohesion", "aggression", "fragility", "adaptation", "memory_depth"],
        "equation": "dC/dt = Phi(external_field, interaction(C_i,C_j), memory_field, economic_constraints)",
        "field_pressure": field_pressure,
        "field_level": "high" if field_pressure >= 0.7 else ("medium" if field_pressure >= 0.4 else "low"),
        "nodes": nodes,
        "edges": edges,
        "evolution_tree": _evolution_tree(genome_engine),
        "phase_field_overlay": {
            "entropy_field": round(sum(n(node.get("field_vector", {}).get("entropy")) for node in nodes) / max(1, len(nodes)), 3),
            "tension_field": round(sum(n(node.get("field_vector", {}).get("tension")) for node in nodes) / max(1, len(nodes)), 3),
            "collapse_zones": [node["civilization_id"] for node in nodes if node.get("zone") == "collapse_zone"],
        },
        "product_boundary": {
            "abstract_behavior_model": True,
            "not_real_world_war": True,
            "not_financial_or_gambling_advice": True,
        },
    }
