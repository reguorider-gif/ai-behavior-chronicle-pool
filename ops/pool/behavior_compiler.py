from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from .behavior_journal import load_recent_seat_events
from .civilization_battle import build_civilization_battle
from .civilization_state import build_civilization_state
from .io_utils import now_iso, read_json, read_jsonl, write_json
from .paths import DATA_ROOT
from .rules_engine import n
from .seat_registry import PRODUCTION_SEATS


def _seat_events(seat_id: str) -> list[dict[str, Any]]:
    return read_jsonl(DATA_ROOT / "seat_journals" / seat_id / "journal.jsonl")


def _source_ids(events: list[dict[str, Any]], event_type: str | None = None) -> list[str]:
    ids: list[str] = []
    for index, event in enumerate(events):
        if event_type and event.get("event_type") != event_type:
            continue
        run_id = str(event.get("run_id") or "unknown")
        ids.append(f"{run_id}:{event.get('event_type') or 'event'}:{index}")
    return ids[-8:]


def _investment_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "investment_recorded":
            continue
        for item in event.get("investments") or []:
            if isinstance(item, dict):
                rows.append({**item, "_run_id": event.get("run_id")})
    return rows


def _forecast_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "forecast_recorded":
            continue
        for item in event.get("forecasts") or []:
            if isinstance(item, dict):
                rows.append({**item, "_run_id": event.get("run_id")})
    return rows


def _settlement_profit(events: list[dict[str, Any]]) -> float:
    total = 0.0
    for event in events:
        if event.get("event_type") != "settlement_recorded":
            continue
        total += n((event.get("settlement") or {}).get("profit_gp"))
    return round(total, 2)


def _latest_event(events: list[dict[str, Any]], event_type: str) -> dict[str, Any]:
    for event in reversed(events):
        if event.get("event_type") == event_type:
            return event
    return {}


def _risk_level(total_stake: float, total_loan: float, bet_count: int, no_bet_rate: float) -> str:
    if total_loan > 0 or total_stake >= 800 or bet_count >= 6:
        return "high"
    if total_stake >= 200 or bet_count >= 2:
        return "medium"
    if no_bet_rate >= 0.7:
        return "low"
    return "guarded"


def _loan_dependency(total_loan: float, outstanding: float) -> str:
    if total_loan > 500 or outstanding > 1000:
        return "high"
    if total_loan > 0 or outstanding > 0:
        return "medium"
    return "low"


def _strategy_drift(no_bet_rate: float, total_stake: float, profit: float, recent_summary: str) -> str:
    text = recent_summary.lower()
    if no_bet_rate >= 0.75:
        return "risk_reduction"
    if total_stake >= 800 or "aggressive" in text or "激进" in recent_summary:
        return "aggressive_shift"
    if profit < 0 and total_stake > 0:
        return "loss_response_under_observation"
    return "stable"


def _behavior_type(risk_level: str, loan_dependency: str, no_bet_rate: float, bet_count: int) -> str:
    if loan_dependency == "high":
        return "leveraged_survival_player"
    if no_bet_rate >= 0.75:
        return "discipline_first_observer"
    if risk_level == "high":
        return "aggressive_edge_hunter"
    if bet_count >= 2:
        return "selective_allocator"
    return "balanced_trader"


def _pattern(
    name: str,
    label: str,
    confidence: float,
    source_event_ids: list[str],
    seats: list[str] | None = None,
    note: str = "",
) -> dict[str, Any]:
    return {
        "name": name,
        "label": label,
        "confidence": round(max(0.0, min(1.0, confidence)), 2),
        "source_event_ids": source_event_ids,
        "supporting_events": len(source_event_ids),
        "seats": seats or [],
        "note": note,
    }


def compile_behavior_memory(seat_id: str, *, write: bool = True) -> dict[str, Any]:
    events = _seat_events(seat_id)
    investments = _investment_rows(events)
    forecasts = _forecast_rows(events)
    bets = [row for row in investments if str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0]
    no_bets = [row for row in investments if str(row.get("action") or "").lower() == "no_bet" or n(row.get("stake_gp")) <= 0]
    total_decisions = len(investments)
    no_bet_rate = round(len(no_bets) / total_decisions, 3) if total_decisions else 0.0
    total_stake = round(sum(n(row.get("stake_gp")) for row in bets), 2)
    total_loan_used = round(sum(n(row.get("loan_used_gp")) for row in bets), 2)
    settlement_profit = _settlement_profit(events)
    latest_credit = _latest_event(events, "credit_updated")
    latest_survival = _latest_event(events, "survival_updated")
    latest_investment = _latest_event(events, "investment_recorded")
    recent_note = " ".join(
        str(item)
        for item in [
            latest_investment.get("status"),
            (latest_investment.get("loan_decision") or {}).get("reason"),
            latest_survival.get("recovery_mode"),
        ]
        if item is not None
    )
    outstanding_loan = n(latest_survival.get("outstanding_loan_gp") or latest_credit.get("outstanding_loan_gp"))
    risk_level = _risk_level(total_stake, total_loan_used, len(bets), no_bet_rate)
    loan_dependency = _loan_dependency(total_loan_used, outstanding_loan)
    drift = _strategy_drift(no_bet_rate, total_stake, settlement_profit, recent_note)
    behavior_type = _behavior_type(risk_level, loan_dependency, no_bet_rate, len(bets))

    patterns: list[dict[str, Any]] = []
    if no_bet_rate >= 0.5:
        patterns.append(_pattern(
            "uncertainty_to_no_bet",
            "uncertainty → no-bet",
            0.58 + min(0.35, no_bet_rate / 2),
            _source_ids(events, "investment_recorded"),
            [seat_id],
            "信息缺口或 EV 不足时倾向观望。",
        ))
    if total_loan_used > 0 or outstanding_loan > 0:
        patterns.append(_pattern(
            "loan_pressure_shapes_risk",
            "loan → risk constraint",
            0.62 + min(0.25, (total_loan_used + outstanding_loan) / 4000),
            _source_ids(events, "credit_updated") + _source_ids(events, "survival_updated"),
            [seat_id],
            "贷款和信用状态正在约束下一轮仓位。",
        ))
    if total_stake >= 300:
        patterns.append(_pattern(
            "capital_to_selective_allocation",
            "capital → selective allocation",
            0.57 + min(0.3, total_stake / 3000),
            _source_ids(events, "investment_recorded"),
            [seat_id],
            "有资金暴露，但仍需观察是否来自正期望而非排名压力。",
        ))
    if settlement_profit < 0:
        patterns.append(_pattern(
            "loss_requires_strategy_change",
            "loss → strategy review",
            0.68,
            _source_ids(events, "settlement_recorded"),
            [seat_id],
            "亏损后下一轮必须说明是否降杠杆或改变市场选择。",
        ))
    if settlement_profit > 0:
        patterns.append(_pattern(
            "profit_to_stability_check",
            "profit → stabilize strategy",
            0.62,
            _source_ids(events, "settlement_recorded"),
            [seat_id],
            "盈利后需要验证是否保持纪律，而不是盲目放大仓位。",
        ))
    if not patterns:
        patterns.append(_pattern(
            "insufficient_history",
            "insufficient history → observe",
            0.4,
            _source_ids(events) or [f"missing:{seat_id}"],
            [seat_id],
            "历史事件不足，下一轮只注入基础风险提醒。",
        ))

    memory = {
        "version": "behavior_memory.v1",
        "seat_id": seat_id,
        "generated_at": now_iso(),
        "event_count": len(events),
        "runs_seen": sorted({str(event.get("run_id")) for event in events if event.get("run_id")}),
        "profile": {
            "behavior_type": behavior_type,
            "risk_level": risk_level,
            "loan_dependency": loan_dependency,
            "no_bet_rate": no_bet_rate,
            "strategy_drift": drift,
            "bet_count": len(bets),
            "forecast_count": len(forecasts),
            "total_stake_gp": total_stake,
            "total_loan_used_gp": total_loan_used,
            "settlement_profit_gp": settlement_profit,
            "credit_grade": latest_credit.get("credit_grade"),
            "credit_score": latest_credit.get("credit_score"),
            "recovery_mode": bool(latest_survival.get("recovery_mode")),
        },
        "top_patterns": sorted(patterns, key=lambda row: row["confidence"], reverse=True)[:5],
        "recent_timeline_events": timeline_events_for_seat(seat_id, events=events, limit=8),
        "memory_contract": {
            "must_reference_in_next_decision": True,
            "required_output_fields": ["memory_used", "memory_not_used_reason", "strategy_change_from_memory"],
        },
    }
    if write:
        write_json(DATA_ROOT / "behavior_memory" / "compiled" / f"{seat_id}.json", memory)
        write_json(DATA_ROOT / "behavior_patterns" / f"{seat_id}.json", {
            "version": "behavior_patterns.v1",
            "seat_id": seat_id,
            "generated_at": memory["generated_at"],
            "patterns": memory["top_patterns"],
        })
    return memory


def timeline_events_for_seat(seat_id: str, *, events: list[dict[str, Any]] | None = None, limit: int = 8) -> list[dict[str, Any]]:
    events = events if events is not None else load_recent_seat_events(seat_id, limit=limit * 3)
    timeline: list[dict[str, Any]] = []
    for index, event in enumerate(events):
        event_type = str(event.get("event_type") or "")
        if event_type == "forecast_recorded":
            timeline.append({
                "event_id": f"{event.get('run_id')}:{event_type}:{index}",
                "run_id": event.get("run_id"),
                "action": "forecast",
                "outcome": f"{len(event.get('forecasts') or [])} forecasts",
                "risk_shift": "information_gathering",
            })
        elif event_type == "investment_recorded":
            investments = event.get("investments") or []
            bet_count = sum(1 for row in investments if isinstance(row, dict) and str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0)
            no_bet_count = len(investments) - bet_count
            loan = sum(n(row.get("loan_used_gp")) for row in investments if isinstance(row, dict))
            timeline.append({
                "event_id": f"{event.get('run_id')}:{event_type}:{index}",
                "run_id": event.get("run_id"),
                "action": "investment",
                "outcome": f"{bet_count} bet / {no_bet_count} no-bet",
                "risk_shift": "loan_used" if loan > 0 else ("risk_reduction" if no_bet_count >= bet_count else "selective_risk"),
            })
        elif event_type == "settlement_recorded":
            profit = n((event.get("settlement") or {}).get("profit_gp"))
            timeline.append({
                "event_id": f"{event.get('run_id')}:{event_type}:{index}",
                "run_id": event.get("run_id"),
                "action": "settlement",
                "outcome": f"{profit:+.0f} GP",
                "risk_shift": "loss_review" if profit < 0 else ("profit_lock" if profit > 0 else "neutral"),
            })
        elif event_type in {"credit_updated", "survival_updated"}:
            timeline.append({
                "event_id": f"{event.get('run_id')}:{event_type}:{index}",
                "run_id": event.get("run_id"),
                "action": event_type.replace("_updated", ""),
                "outcome": event.get("credit_grade") or ("recovery" if event.get("recovery_mode") else "normal"),
                "risk_shift": "constraint_update",
            })
    return timeline[-limit:]


def compile_all_behavior_memory(seat_ids: list[str] | None = None, *, run_id: str | None = None, write: bool = True) -> dict[str, Any]:
    seat_ids = seat_ids or PRODUCTION_SEATS
    compiled = {seat_id: compile_behavior_memory(seat_id, write=write) for seat_id in seat_ids}
    graph = build_pattern_graph(compiled, run_id=run_id, write=write)
    profiles = build_agent_profiles(compiled, run_id=run_id, write=write)
    trace = build_evolution_trace(compiled, run_id=run_id, write=write)
    civilization_state = build_civilization_state(
        run_id=run_id,
        agent_profiles=profiles,
        pattern_graph=graph,
        evolution_trace=trace,
        write=write,
    )
    civilization_battle = build_civilization_battle(
        run_id=run_id,
        civilization_state=civilization_state,
        write=write,
    )
    return {
        "version": "behavior_kernel_bundle.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "seat_count": len(compiled),
        "compiled": compiled,
        "pattern_graph": graph,
        "agent_profiles": profiles,
        "evolution_trace": trace,
        "civilization_state": civilization_state,
        "civilization_battle": civilization_battle,
    }


def build_pattern_graph(compiled: dict[str, dict[str, Any]], *, run_id: str | None = None, write: bool = True) -> dict[str, Any]:
    grouped: dict[str, dict[str, Any]] = {}
    for seat_id, memory in compiled.items():
        for pattern in memory.get("top_patterns") or []:
            name = str(pattern.get("name") or "unknown")
            row = grouped.setdefault(name, {
                "name": name,
                "label": pattern.get("label") or name,
                "confidence_values": [],
                "source_event_ids": [],
                "seats": [],
                "supporting_events": 0,
                "note": pattern.get("note") or "",
            })
            row["confidence_values"].append(n(pattern.get("confidence")))
            row["source_event_ids"].extend(pattern.get("source_event_ids") or [])
            row["seats"].append(seat_id)
            row["supporting_events"] += n(pattern.get("supporting_events"))
    patterns = []
    for row in grouped.values():
        confidence_values = row.pop("confidence_values")
        source_ids = sorted(set(row["source_event_ids"]))
        seats = sorted(set(row["seats"]))
        patterns.append({
            **row,
            "confidence": round(sum(confidence_values) / max(1, len(confidence_values)), 2),
            "source_event_ids": source_ids[:20],
            "seats": seats,
            "supporting_events": int(row["supporting_events"]),
        })
    graph = {
        "version": "pattern_graph.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "top_patterns": sorted(patterns, key=lambda item: (item["supporting_events"], item["confidence"]), reverse=True)[:5],
    }
    if write:
        write_json(DATA_ROOT / "pattern_graph" / "latest.json", graph)
        if run_id:
            write_json(DATA_ROOT / "pattern_graph" / f"{run_id}.json", graph)
    return graph


def build_agent_profiles(compiled: dict[str, dict[str, Any]], *, run_id: str | None = None, write: bool = True) -> dict[str, Any]:
    seats = {
        seat_id: {
            "seat_id": seat_id,
            **memory.get("profile", {}),
            "timeline_events": memory.get("recent_timeline_events") or [],
            "top_patterns": memory.get("top_patterns") or [],
        }
        for seat_id, memory in compiled.items()
    }
    payload = {
        "version": "agent_profiles.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "seats": seats,
    }
    if write:
        write_json(DATA_ROOT / "agent_profiles" / "latest.json", payload)
        if run_id:
            write_json(DATA_ROOT / "agent_profiles" / f"{run_id}.json", payload)
    return payload


def build_evolution_trace(compiled: dict[str, dict[str, Any]], *, run_id: str | None = None, write: bool = True) -> dict[str, Any]:
    traces = []
    for seat_id, memory in compiled.items():
        profile = memory.get("profile") or {}
        patterns = memory.get("top_patterns") or []
        primary = patterns[0] if patterns else {}
        traces.append({
            "seat_id": seat_id,
            "run_id": run_id,
            "behavior_type": profile.get("behavior_type"),
            "risk_level": profile.get("risk_level"),
            "loan_dependency": profile.get("loan_dependency"),
            "strategy_drift": profile.get("strategy_drift"),
            "memory_used": bool(patterns),
            "dominant_pattern": primary.get("name"),
            "source_event_ids": primary.get("source_event_ids") or [],
            "decision_pressure": {
                "no_bet_rate": profile.get("no_bet_rate"),
                "total_stake_gp": profile.get("total_stake_gp"),
                "settlement_profit_gp": profile.get("settlement_profit_gp"),
                "recovery_mode": profile.get("recovery_mode"),
            },
        })
    payload = {
        "version": "evolution_trace.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "traces": traces,
    }
    if write and run_id:
        write_json(DATA_ROOT / "evolution_traces" / f"{run_id}.json", payload)
        write_json(DATA_ROOT / "evolution_traces" / "latest.json", payload)
    elif write:
        write_json(DATA_ROOT / "evolution_traces" / "latest.json", payload)
    return payload


def load_behavior_memory(seat_id: str) -> dict[str, Any]:
    return read_json(DATA_ROOT / "behavior_memory" / "compiled" / f"{seat_id}.json", {})
