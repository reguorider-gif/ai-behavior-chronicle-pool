from __future__ import annotations

from typing import Any

from .civilization_state_engine import clamp
from .rules_engine import n


GENE_KEYS = ["risk_gene", "survival_gene", "aggression_gene", "memory_gene", "adaptation_gene"]


def _phase_by_id(phase_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("civilization_id")): row for row in phase_rows}


def _memory_by_id(memory_dynamics: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("civilization_id")): row
        for row in (memory_dynamics.get("civilizations") or [])
    }


def _genome_from_phase(row: dict[str, Any], memory_row: dict[str, Any] | None = None) -> dict[str, float]:
    physical = row.get("physical_vector") or {}
    memory = memory_row or {}
    energy = n(physical.get("energy"))
    entropy = n(physical.get("entropy"))
    tension = n(physical.get("tension"))
    cohesion = n(physical.get("cohesion"))
    aggression = n(physical.get("aggression"))
    fragility = n(physical.get("fragility"))
    memory_pressure = n(memory.get("memory_pressure"))
    return {
        "risk_gene": round(clamp(entropy * 0.38 + tension * 0.28 + aggression * 0.22 + fragility * 0.12), 3),
        "survival_gene": round(clamp(cohesion * 0.42 + energy * 0.3 + (1 - fragility) * 0.2 + (1 - tension) * 0.08), 3),
        "aggression_gene": round(clamp(aggression * 0.58 + energy * 0.22 + entropy * 0.2), 3),
        "memory_gene": round(clamp((1 - memory_pressure) * 0.18 + memory_pressure * 0.46 + cohesion * 0.22 + (1 - entropy) * 0.14), 3),
        "adaptation_gene": round(clamp(memory_pressure * 0.34 + tension * 0.24 + cohesion * 0.22 + (1 - fragility) * 0.2), 3),
    }


def _phenotype(genome: dict[str, float]) -> str:
    if genome["survival_gene"] >= 0.68 and genome["risk_gene"] < 0.45:
        return "stable_line"
    if genome["aggression_gene"] >= 0.62 and genome["risk_gene"] >= 0.55:
        return "aggressive_line"
    if genome["adaptation_gene"] >= 0.58 and genome["memory_gene"] >= 0.52:
        return "adaptive_line"
    if genome["risk_gene"] >= 0.68 and genome["survival_gene"] < 0.45:
        return "collapse_line"
    return "mixed_line"


def _stress(row: dict[str, Any]) -> float:
    physical = row.get("physical_vector") or {}
    return round(clamp(n(physical.get("entropy")) * 0.32 + n(physical.get("tension")) * 0.32 + n(physical.get("fragility")) * 0.24 + (1 - n(physical.get("cohesion"))) * 0.12), 3)


def build_civilization_genomes(
    civilizations: list[dict[str, Any]],
    phase_rows: list[dict[str, Any]],
    memory_dynamics: dict[str, Any],
) -> dict[str, Any]:
    phase_map = _phase_by_id(phase_rows)
    memory_map = _memory_by_id(memory_dynamics)
    rows = []
    for civ in civilizations:
        civ_id = str(civ.get("id"))
        phase = phase_map.get(civ_id, {})
        genome = _genome_from_phase(phase, memory_map.get(civ_id))
        stress = _stress(phase)
        mutation_pressure = round(clamp(stress * 0.62 + genome["risk_gene"] * 0.22 + (1 - genome["survival_gene"]) * 0.16), 3)
        if mutation_pressure >= 0.62:
            mutation = "stress_mutates_risk_gene"
        elif genome["memory_gene"] >= 0.62:
            mutation = "memory_stabilizes_strategy"
        else:
            mutation = "low_mutation_pressure"
        rows.append({
            "civilization_id": civ_id,
            "label": civ.get("zh_name") or civ.get("name") or civ_id,
            "phase": phase.get("phase") or "UNKNOWN",
            "genome": genome,
            "phenotype": _phenotype(genome),
            "stress": stress,
            "mutation_pressure": mutation_pressure,
            "mutation_rule": mutation,
            "expression": f"phenotype = f(genome, environment); current phenotype = {_phenotype(genome)}",
        })
    return {
        "version": "civilization_genome_engine.v1",
        "definition": "genome expresses behavioral tendencies under environment stress",
        "gene_keys": GENE_KEYS,
        "civilizations": rows,
        "mutation_contract": {
            "stress_high_mutates_risk_gene": True,
            "memory_gene_can_stabilize_strategy": True,
            "product_metaphor_only": True,
        },
    }
