from __future__ import annotations

import json
from typing import Any

from ..io_utils import read_json
from ..paths import DATA_ROOT


REQUIRED_MEMORY_FIELDS = {"memory_used", "memory_not_used_reason", "strategy_change_from_memory"}


def _status(ok: bool, partial: bool = False) -> str:
    if ok:
        return "pass"
    return "partial" if partial else "fail"


def audit_decision(seat_id: str, event: dict[str, Any]) -> dict[str, Any]:
    """Describe how a single decision event used behavior memory."""
    reconstruction = event.get("decision_reconstruction") or {}
    memory = reconstruction.get("memory_summary") or {}
    state_before = event.get("state_before") or {}
    state_after = event.get("state_after") or {}
    used_patterns = [
        value
        for value in [
            memory.get("dominant_pattern"),
            *((memory.get("active_patterns") or []) if isinstance(memory.get("active_patterns"), list) else []),
        ]
        if value
    ]
    before_risk = state_before.get("risk_level") or state_before.get("risk")
    after_risk = state_after.get("risk_level") or state_after.get("risk") or event.get("risk_shift")
    return {
        "seat_id": seat_id,
        "event_id": event.get("event_id"),
        "event_type": event.get("event_type"),
        "used_patterns": sorted(set(map(str, used_patterns))),
        "memory_influence": bool(memory.get("memory_used") or memory.get("dominant_pattern") or used_patterns),
        "drift_from_history": event.get("risk_shift") or memory.get("strategy_change_from_memory") or "unknown",
        "risk_alignment": {
            "before": before_risk,
            "after": after_risk,
            "changed": bool(before_risk and after_risk and before_risk != after_risk),
        },
    }


def audit_prompt_memory(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    for seat_id in seat_ids:
        context = read_json(DATA_ROOT / "prompt_contexts" / run_id / f"{seat_id}.json", {})
        private_context = context.get("private_context") or {}
        public_context = context.get("public_context") or {}
        behavior = private_context.get("behavior_kernel") or {}
        patterns = behavior.get("active_patterns") or []
        output_contract = public_context.get("output_contract") or {}
        required = set(output_contract.get("behavior_memory_required_fields") or [])
        private_blob = json.dumps(private_context, ensure_ascii=False).lower()
        leaked = [other for other in seat_ids if other != seat_id and other.lower() in private_blob]
        row = {
            "seat_id": seat_id,
            "context_exists": bool(context),
            "kernel_version": context.get("behavior_kernel_version"),
            "has_behavior_memory": bool(behavior),
            "active_pattern_count": len(patterns),
            "must_consider_memory": bool((behavior.get("decision_contract") or {}).get("must_consider_memory")),
            "required_fields_present": REQUIRED_MEMORY_FIELDS.issubset(required),
            "private_leakage": leaked,
        }
        rows.append(row)
        if not row["context_exists"]:
            violations.append({"seat_id": seat_id, "type": "missing_prompt_context"})
        if not row["has_behavior_memory"]:
            violations.append({"seat_id": seat_id, "type": "missing_behavior_memory"})
        if not row["must_consider_memory"]:
            violations.append({"seat_id": seat_id, "type": "memory_not_mandatory"})
        if not row["required_fields_present"]:
            violations.append({"seat_id": seat_id, "type": "missing_required_memory_receipt_fields"})
        if leaked:
            violations.append({"seat_id": seat_id, "type": "cross_seat_private_leakage", "leaked": leaked})
    pass_count = sum(
        1
        for row in rows
        if row["context_exists"]
        and row["has_behavior_memory"]
        and row["must_consider_memory"]
        and row["required_fields_present"]
        and not row["private_leakage"]
    )
    return {
        "version": "prompt_memory_verifier.v1",
        "run_id": run_id,
        "status": _status(pass_count == len(seat_ids)),
        "checked": len(rows),
        "pass_count": pass_count,
        "violations": violations,
        "rows": rows,
    }


def audit_behavior_diff(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    evolution = read_json(DATA_ROOT / "evolution_traces" / f"{run_id}.json", {})
    traces = {row.get("seat_id"): row for row in evolution.get("traces") or []}
    rows: list[dict[str, Any]] = []
    for seat_id in seat_ids:
        trace = traces.get(seat_id) or {}
        pressure = trace.get("decision_pressure") or {}
        drift = trace.get("strategy_drift")
        changed = drift not in {None, "", "stable"} or bool(trace.get("dominant_pattern"))
        rows.append({
            "seat_id": seat_id,
            "behavior_type": trace.get("behavior_type"),
            "risk_level": trace.get("risk_level"),
            "loan_dependency": trace.get("loan_dependency"),
            "strategy_drift": drift,
            "dominant_pattern": trace.get("dominant_pattern"),
            "decision_pressure": pressure,
            "behavior_shift_detected": changed,
        })
    detected = sum(1 for row in rows if row["behavior_shift_detected"])
    return {
        "version": "behavior_diff_checker.v1",
        "run_id": run_id,
        "status": _status(detected > 0),
        "shift_detected_count": detected,
        "rows": rows,
    }


def audit_causal_trace_chains(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    decision_types = {"forecast_recorded", "investment_recorded"}
    rows: list[dict[str, Any]] = []
    for event in replay.get("timeline") or []:
        event_type = event.get("event_type")
        seat_id = str(event.get("seat_id") or "")
        if event_type not in decision_types or seat_id not in seat_ids:
            continue
        reconstruction = event.get("decision_reconstruction") or {}
        prompt_summary = reconstruction.get("prompt_summary") or {}
        memory_summary = reconstruction.get("memory_summary") or {}
        counterfactual = event.get("counterfactual") or {}
        source = event.get("source_event") or {}
        row = {
            "seat_id": seat_id,
            "event_id": event.get("event_id"),
            "event_type": event_type,
            "has_state_before": bool(event.get("state_before")),
            "has_state_after": bool(event.get("state_after")),
            "has_memory_summary": bool(memory_summary),
            "has_dominant_pattern": bool(memory_summary.get("dominant_pattern")),
            "has_memory_contract": bool(prompt_summary.get("memory_contract")),
            "has_decision_text": bool(reconstruction.get("decision")),
            "has_counterfactual": bool(counterfactual.get("alternative") and counterfactual.get("expected_effect")),
            "has_source_event": bool(source),
            "has_snapshot_ref": bool(event.get("snapshot_ref")),
        }
        row["explanation_chain_complete"] = all(
            row[key]
            for key in [
                "has_state_before",
                "has_state_after",
                "has_memory_summary",
                "has_dominant_pattern",
                "has_memory_contract",
                "has_decision_text",
                "has_counterfactual",
                "has_source_event",
                "has_snapshot_ref",
            ]
        )
        rows.append(row)

    complete = sum(1 for row in rows if row["explanation_chain_complete"])
    return {
        "version": "causal_trace_audit.v1",
        "run_id": run_id,
        "status": _status(bool(rows) and complete == len(rows), partial=complete > 0),
        "decision_event_count": len(rows),
        "complete_chain_count": complete,
        "rows": rows,
    }
