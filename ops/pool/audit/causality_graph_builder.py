from __future__ import annotations

from typing import Any

from ..behavior_production_kernel import stable_hash
from ..io_utils import write_json
from ..paths import DATA_ROOT


def build_causality_graph(
    run_id: str,
    influence: dict[str, Any],
    credit: dict[str, Any],
) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    credit_rows = {row["seat_id"]: row for row in credit.get("rows") or []}
    for row in influence.get("rows") or []:
        seat_id = row["seat_id"]
        seat_node = f"seat:{seat_id}"
        nodes[seat_node] = {"id": seat_node, "type": "seat", "label": seat_id}
        for pattern in row.get("context_patterns") or []:
            pattern_node = f"pattern:{pattern}"
            nodes[pattern_node] = {"id": pattern_node, "type": "pattern", "label": pattern}
            edges.append({
                "from": pattern_node,
                "to": seat_node,
                "type": "pattern_injected",
                "evidence_level": row.get("evidence_level"),
            })
        decision_node = f"decision:{seat_id}:investment"
        nodes[decision_node] = {"id": decision_node, "type": "decision", "label": "investment"}
        edges.append({
            "from": seat_node,
            "to": decision_node,
            "type": "agent_decision",
            "evidence_level": row.get("evidence_level"),
        })
        credit_node = f"credit:{seat_id}"
        credit_row = credit_rows.get(seat_id) or {}
        nodes[credit_node] = {
            "id": credit_node,
            "type": "credit_survival",
            "label": f"{credit_row.get('credit_delta')} / loan {credit_row.get('outstanding_loan_gp')}",
        }
        edges.append({
            "from": decision_node,
            "to": credit_node,
            "type": "decision_updates_credit_survival",
            "evidence_level": "strong" if credit_row else "missing",
        })
    graph = {
        "version": "decision_causality_graph.v1",
        "run_id": run_id,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": list(nodes.values()),
        "edges": edges,
        "graph_hash": stable_hash({"nodes": nodes, "edges": edges}),
    }
    write_json(DATA_ROOT / "behavior_audits" / f"{run_id}.causality_graph.json", graph)
    return graph
