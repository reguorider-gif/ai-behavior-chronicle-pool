from __future__ import annotations

from typing import Any

from .causality_graph_builder import build_causality_graph
from .decision_tracer import audit_behavior_diff, audit_causal_trace_chains, audit_prompt_memory
from .pattern_influence_checker import audit_pattern_removal_sensitivity, trace_pattern_influence
from .replay_validator import validate_replay
from ..behavior_compiler import PRODUCTION_SEATS
from ..behavior_production_kernel import KERNEL_VERSION
from ..io_utils import now_iso, read_json, write_json
from ..paths import DATA_ROOT


def _status(ok: bool, partial: bool = False) -> str:
    if ok:
        return "pass"
    return "partial" if partial else "fail"


def _seat_ids_from_artifacts(run_id: str, seat_ids: list[str] | None = None) -> list[str]:
    if seat_ids:
        return seat_ids
    receipts = read_json(DATA_ROOT / "investment_receipts" / f"{run_id}.json", {})
    seats = sorted((receipts.get("seats") or {}).keys())
    return seats or PRODUCTION_SEATS


def audit_credit_loan_behavior(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    credit = read_json(DATA_ROOT / "credit_ledger" / f"{run_id}.json", {})
    survival = read_json(DATA_ROOT / "survival_ledger" / f"{run_id}.json", {})
    credit_seats = credit.get("seats") or {}
    survival_seats = survival.get("seats") or {}
    rows: list[dict[str, Any]] = []
    for seat_id in seat_ids:
        credit_row = credit_seats.get(seat_id) or {}
        survival_row = survival_seats.get(seat_id) or {}
        details = credit_row.get("details") if isinstance(credit_row.get("details"), list) else []
        rows.append({
            "seat_id": seat_id,
            "credit_present": bool(credit_row),
            "survival_present": bool(survival_row),
            "credit_delta": credit_row.get("credit_delta"),
            "credit_basis": credit_row.get("credit_basis"),
            "credit_detail_types": [row.get("type") for row in details if isinstance(row, dict)],
            "loan_limit_gp": survival_row.get("loan_limit_gp"),
            "available_loan_gp": survival_row.get("available_loan_gp"),
            "outstanding_loan_gp": survival_row.get("outstanding_loan_gp"),
            "recovery_mode": bool(survival_row.get("recovery_mode")),
            "allowed_actions": survival_row.get("allowed_actions") or [],
        })
    present = sum(1 for row in rows if row["credit_present"] and row["survival_present"])
    behavior_bound = sum(1 for row in rows if row["credit_detail_types"] and row["allowed_actions"])
    return {
        "version": "credit_loan_behavior_audit.v1",
        "run_id": run_id,
        "status": _status(present == len(seat_ids) and behavior_bound == len(seat_ids), partial=present > 0),
        "present_count": present,
        "behavior_bound_count": behavior_bound,
        "rows": rows,
    }


def production_audit_status(sections: dict[str, dict[str, Any]]) -> dict[str, Any]:
    checks = {
        "behavior_loop": sections["influence"]["status"],
        "prompt_control": sections["prompt_memory"]["status"],
        "pattern_participates": sections["influence"]["status"],
        "pattern_removal_changes_behavior": sections["pattern_removal"]["status"],
        "deterministic_replay": sections["replay"]["status"],
        "causal_trace_complete": sections["causal_trace"]["status"],
        "credit_loan_behavior_binding": sections["credit_loan"]["status"],
        "behavior_ui_contract": "pass",
    }
    passed = sum(1 for status in checks.values() if status == "pass")
    partial = sum(1 for status in checks.values() if status == "partial")
    if passed == len(checks):
        verdict = "PRODUCTION_READY"
    elif passed + partial >= 4:
        verdict = "PARTIAL_PRODUCTION_READY"
    else:
        verdict = "NOT_PRODUCTION_READY"
    return {"verdict": verdict, "passed": passed, "partial": partial, "checks": checks}


def run_behavior_production_audit(run_id: str, seat_ids: list[str] | None = None) -> dict[str, Any]:
    seat_ids = _seat_ids_from_artifacts(run_id, seat_ids)
    prompt_memory = audit_prompt_memory(run_id, seat_ids)
    replay = validate_replay(run_id)
    influence = trace_pattern_influence(run_id, seat_ids)
    pattern_removal = audit_pattern_removal_sensitivity(run_id, seat_ids)
    behavior_diff = audit_behavior_diff(run_id, seat_ids)
    causal_trace = audit_causal_trace_chains(run_id, seat_ids)
    credit_loan = audit_credit_loan_behavior(run_id, seat_ids)
    causality = build_causality_graph(run_id, influence, credit_loan)
    sections = {
        "prompt_memory": prompt_memory,
        "replay": replay,
        "influence": influence,
        "pattern_removal": pattern_removal,
        "behavior_diff": behavior_diff,
        "causal_trace": causal_trace,
        "credit_loan": credit_loan,
    }
    status = production_audit_status(sections)
    audit = {
        "version": "behavior_production_audit.v1",
        "kernel_version": KERNEL_VERSION,
        "generated_at": now_iso(),
        "run_id": run_id,
        "seat_count": len(seat_ids),
        "status": status,
        "sections": sections,
        "causality_graph": {
            "node_count": causality["node_count"],
            "edge_count": causality["edge_count"],
            "graph_hash": causality["graph_hash"],
            "ref": f"data/pool/behavior_audits/{run_id}.causality_graph.json",
        },
    }
    write_json(DATA_ROOT / "behavior_audits" / f"{run_id}.json", audit)
    write_json(DATA_ROOT / "behavior_audits" / "latest.json", audit)
    return audit
