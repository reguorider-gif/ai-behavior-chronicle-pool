from __future__ import annotations

from typing import Any


def _field_color(phase: str) -> str:
    return {
        "STABLE": "emerald",
        "ADAPTIVE": "blue",
        "VOLATILE": "amber",
        "CRITICAL": "orange",
        "EXPANSION": "violet",
        "COLLAPSE": "rose",
    }.get(phase, "slate")


def compute_field(phase_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a product-level civilization field projection.

    x = entropy/disorder, y = tension/pressure. Size and color are derived from
    the physical vector so the UI can render a civilization field without
    exposing raw ledgers or provider traces.
    """

    nodes = []
    for row in phase_rows:
        physical = row.get("physical_vector") or {}
        energy = float(physical.get("energy") or 0)
        entropy = float(physical.get("entropy") or 0)
        tension = float(physical.get("tension") or 0)
        aggression = float(physical.get("aggression") or 0)
        fragility = float(physical.get("fragility") or 0)
        nodes.append({
            "id": row.get("civilization_id"),
            "label": row.get("label"),
            "x": round(0.08 + entropy * 0.84, 3),
            "y": round(0.9 - tension * 0.78, 3),
            "size": round(0.76 + energy * 0.58, 3),
            "color": _field_color(str(row.get("phase"))),
            "phase": row.get("phase"),
            "motion": round(entropy * 0.5 + aggression * 0.28 + fragility * 0.22, 3),
            "energy": round(energy, 3),
            "fragility": round(fragility, 3),
        })
    return {
        "version": "civilization_field_engine.v1",
        "axis": {
            "x": "entropy",
            "y": "tension",
            "size": "energy",
            "motion": "entropy + aggression + fragility",
        },
        "nodes": nodes,
        "meaning": "civilization node position represents dynamic pressure, not match odds or raw betting data",
    }
