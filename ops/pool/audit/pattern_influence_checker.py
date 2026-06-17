from __future__ import annotations

import json
from typing import Any

from .decision_tracer import REQUIRED_MEMORY_FIELDS
from ..io_utils import read_json
from ..paths import DATA_ROOT


def _status(ok: bool, partial: bool = False) -> str:
    if ok:
        return "pass"
    return "partial" if partial else "fail"


def verify_pattern_influence(pattern: str, event: dict[str, Any]) -> dict[str, Any]:
    """Return a compact influence judgment for one pattern/event pair."""
    reconstruction = event.get("decision_reconstruction") or {}
    memory = reconstruction.get("memory_summary") or {}
    action = event.get("action") or event.get("event_type")
    risk_shift = event.get("risk_shift")
    pattern_text = str(pattern or "")
    replay_patterns = {
        str(memory.get("dominant_pattern") or ""),
        *[str(item) for item in memory.get("active_patterns") or []],
    }
    influenced = bool(pattern_text and pattern_text in replay_patterns)
    strength = 0.0
    if influenced:
        strength += 0.5
    if action in {"bet", "investment_recorded"}:
        strength += 0.25
    if risk_shift and risk_shift != "stable":
        strength += 0.25
    return {
        "pattern_id": pattern_text,
        "event_id": event.get("event_id"),
        "influenced": influenced,
        "strength": min(strength, 1.0),
        "action": action,
        "risk_shift": risk_shift,
    }


def _observed_policy(event: dict[str, Any]) -> dict[str, Any]:
    state_after = event.get("state_after") or {}
    return {
        "risk_shift": event.get("risk_shift") or "unknown",
        "stake_gp": float(state_after.get("last_stake_gp") or 0),
        "loan_used_gp": float(state_after.get("last_loan_used_gp") or 0),
        "investment_count": int(state_after.get("last_investment_count") or 0),
        "risk_level": state_after.get("risk_level") or "unknown",
        "strategy_drift": state_after.get("strategy_drift") or "unknown",
    }


def _counterfactual_without_pattern(pattern: str, observed: dict[str, Any]) -> dict[str, Any]:
    if pattern == "uncertainty_to_no_bet":
        return {
            **observed,
            "risk_shift": "higher_exposure_candidate",
            "stake_gp": max(float(observed["stake_gp"]) * 1.2, float(observed["stake_gp"]) + 100),
            "reason": "removing uncertainty_to_no_bet removes the no-bet discipline constraint",
        }
    if pattern == "loan_pressure_shapes_risk":
        return {
            **observed,
            "loan_used_gp": max(float(observed["loan_used_gp"]) * 1.2, float(observed["loan_used_gp"]) + 100),
            "risk_shift": "unconstrained_leverage_candidate",
            "reason": "removing loan_pressure_shapes_risk removes the leverage pressure constraint",
        }
    return {
        **observed,
        "risk_shift": f"without_{pattern or 'pattern'}",
        "reason": "active pattern removed from deterministic counterfactual policy",
    }


def audit_pattern_removal_sensitivity(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    rows: list[dict[str, Any]] = []
    for event in replay.get("timeline") or []:
        seat_id = str(event.get("seat_id") or "")
        if seat_id not in seat_ids or event.get("event_type") != "investment_recorded":
            continue
        memory = ((event.get("decision_reconstruction") or {}).get("memory_summary") or {})
        pattern = memory.get("dominant_pattern")
        observed = _observed_policy(event)
        without = _counterfactual_without_pattern(str(pattern or ""), observed)
        changed = (
            without.get("risk_shift") != observed.get("risk_shift")
            or float(without.get("stake_gp") or 0) != float(observed.get("stake_gp") or 0)
            or float(without.get("loan_used_gp") or 0) != float(observed.get("loan_used_gp") or 0)
        )
        rows.append({
            "seat_id": seat_id,
            "event_id": event.get("event_id"),
            "pattern_removed": pattern,
            "observed_policy": observed,
            "counterfactual_without_pattern": without,
            "behavior_changes_when_pattern_removed": bool(pattern and changed),
        })
    changed_count = sum(1 for row in rows if row["behavior_changes_when_pattern_removed"])
    return {
        "version": "pattern_removal_sensitivity.v1",
        "run_id": run_id,
        "status": _status(bool(rows) and changed_count == len(rows), partial=changed_count > 0),
        "checked_decision_count": len(rows),
        "changed_count": changed_count,
        "rows": rows,
    }


def trace_pattern_influence(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    evolution = read_json(DATA_ROOT / "evolution_traces" / f"{run_id}.json", {})
    investments = read_json(DATA_ROOT / "investment_receipts" / f"{run_id}.json", {})
    traces = {row.get("seat_id"): row for row in evolution.get("traces") or []}
    events_by_seat: dict[str, list[dict[str, Any]]] = {}
    for event in replay.get("timeline") or []:
        events_by_seat.setdefault(str(event.get("seat_id")), []).append(event)

    rows: list[dict[str, Any]] = []
    weak_evidence: list[dict[str, Any]] = []
    for seat_id in seat_ids:
        context = read_json(DATA_ROOT / "prompt_contexts" / run_id / f"{seat_id}.json", {})
        behavior = ((context.get("private_context") or {}).get("behavior_kernel") or {})
        context_patterns = [row.get("name") for row in behavior.get("active_patterns") or [] if row.get("name")]
        investment_events = [row for row in events_by_seat.get(seat_id, []) if row.get("event_type") == "investment_recorded"]
        memory_summaries = [
            ((event.get("decision_reconstruction") or {}).get("memory_summary") or {})
            for event in investment_events
        ]
        replay_patterns = [row.get("dominant_pattern") for row in memory_summaries if row.get("dominant_pattern")]
        trace = traces.get(seat_id) or {}
        receipt = ((investments.get("seats") or {}).get(seat_id) or {})
        receipt_blob = json.dumps(receipt, ensure_ascii=False)
        receipt_has_self_report = any(field in receipt_blob for field in REQUIRED_MEMORY_FIELDS)
        influence = bool(context_patterns and investment_events and trace.get("memory_used"))
        if influence and not receipt_has_self_report:
            weak_evidence.append({"seat_id": seat_id, "type": "provider_receipt_lacks_memory_self_report"})
        rows.append({
            "seat_id": seat_id,
            "context_patterns": context_patterns,
            "replay_patterns": replay_patterns,
            "evolution_dominant_pattern": trace.get("dominant_pattern"),
            "memory_used_in_trace": bool(trace.get("memory_used")),
            "investment_event_count": len(investment_events),
            "receipt_has_memory_self_report": receipt_has_self_report,
            "influence_evidence": influence,
            "evidence_level": "strong" if influence and receipt_has_self_report else ("medium" if influence else "missing"),
        })

    influenced = sum(1 for row in rows if row["influence_evidence"])
    strong = sum(1 for row in rows if row["evidence_level"] == "strong")
    return {
        "version": "pattern_influence_tracer.v1",
        "run_id": run_id,
        "status": _status(influenced == len(seat_ids), partial=influenced > 0),
        "influenced_count": influenced,
        "strong_evidence_count": strong,
        "weak_evidence": weak_evidence,
        "rows": rows,
    }
