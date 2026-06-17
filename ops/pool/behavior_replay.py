from __future__ import annotations

import re
from typing import Any

from .behavior_compiler import PRODUCTION_SEATS, compile_behavior_memory, timeline_events_for_seat
from .io_utils import now_iso, read_json, read_jsonl, write_json
from .paths import DATA_ROOT
from .rules_engine import n


def _seat_events(seat_id: str) -> list[dict[str, Any]]:
    return read_jsonl(DATA_ROOT / "seat_journals" / seat_id / "journal.jsonl")


def _safe_token(value: str) -> str:
    token = re.sub(r"[^a-zA-Z0-9_.-]+", "-", str(value or "").strip())
    return token.strip("-") or "event"


def _prompt_context(seat_id: str, run_id: str) -> dict[str, Any]:
    return read_json(DATA_ROOT / "prompt_contexts" / run_id / f"{seat_id}.json", {})


def _state_from_events(seat_id: str, events: list[dict[str, Any]], memory: dict[str, Any]) -> dict[str, Any]:
    profile = memory.get("profile") or {}
    state = {
        "seat_id": seat_id,
        "balance_gp": 1000.0,
        "credit_score": profile.get("credit_score") or 600,
        "credit_grade": profile.get("credit_grade") or "B",
        "outstanding_loan_gp": 0.0,
        "accrued_interest_gp": 0.0,
        "net_worth_gp": 1000.0,
        "recovery_mode": False,
        "risk_level": profile.get("risk_level") or "unknown",
        "behavior_type": profile.get("behavior_type") or "observing",
        "loan_dependency": profile.get("loan_dependency") or "unknown",
        "strategy_drift": profile.get("strategy_drift") or "stable",
        "active_patterns": [
            {
                "name": pattern.get("name"),
                "label": pattern.get("label"),
                "confidence": pattern.get("confidence"),
            }
            for pattern in (memory.get("top_patterns") or [])[:3]
        ],
        "recent_memory": timeline_events_for_seat(seat_id, events=events, limit=4),
    }
    for event in events:
        event_type = event.get("event_type")
        if event_type == "credit_updated":
            state["credit_score"] = event.get("credit_score", state["credit_score"])
            state["credit_grade"] = event.get("credit_grade", state["credit_grade"])
            state["outstanding_loan_gp"] = n(event.get("outstanding_loan_gp"), state["outstanding_loan_gp"])
        elif event_type == "survival_updated":
            state["outstanding_loan_gp"] = n(event.get("outstanding_loan_gp"), state["outstanding_loan_gp"])
            state["accrued_interest_gp"] = n(event.get("accrued_interest_gp"), state["accrued_interest_gp"])
            state["net_worth_gp"] = n(event.get("net_worth_gp"), state["net_worth_gp"])
            state["recovery_mode"] = bool(event.get("recovery_mode", state["recovery_mode"]))
        elif event_type == "settlement_recorded":
            settlement = event.get("settlement") or {}
            state["last_profit_gp"] = n(settlement.get("profit_gp"))
            if settlement.get("balance_gp") is not None:
                state["balance_gp"] = n(settlement.get("balance_gp"), state["balance_gp"])
        elif event_type == "investment_recorded":
            investments = [row for row in event.get("investments") or [] if isinstance(row, dict)]
            state["last_investment_count"] = len(investments)
            state["last_stake_gp"] = round(sum(n(row.get("stake_gp")) for row in investments), 2)
            state["last_loan_used_gp"] = round(sum(n(row.get("loan_used_gp")) for row in investments), 2)
        elif event_type == "forecast_recorded":
            state["last_forecast_count"] = len(event.get("forecasts") or [])
    return state


def _action_for_event(event: dict[str, Any]) -> str:
    event_type = str(event.get("event_type") or "event")
    return {
        "prompt_context_recorded": "context",
        "forecast_recorded": "forecast",
        "investment_recorded": "investment",
        "credit_updated": "credit",
        "survival_updated": "survival",
        "settlement_recorded": "settlement",
    }.get(event_type, event_type.replace("_recorded", "").replace("_updated", ""))


def _outcome_for_event(event: dict[str, Any]) -> str:
    event_type = str(event.get("event_type") or "")
    if event_type == "forecast_recorded":
        return f"{len(event.get('forecasts') or [])} forecasts"
    if event_type == "investment_recorded":
        investments = [row for row in event.get("investments") or [] if isinstance(row, dict)]
        bets = [row for row in investments if str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0]
        no_bets = len(investments) - len(bets)
        stake = sum(n(row.get("stake_gp")) for row in bets)
        return f"{len(bets)} bet / {no_bets} no-bet · {stake:.0f} GP"
    if event_type == "credit_updated":
        return f"{event.get('credit_grade', 'B')} · {n(event.get('credit_score'), 0):.0f}"
    if event_type == "survival_updated":
        return "recovery" if event.get("recovery_mode") else "normal"
    if event_type == "settlement_recorded":
        return f"{n((event.get('settlement') or {}).get('profit_gp')):+.0f} GP"
    return str(event.get("status") or event_type or "event")


def _risk_shift(event: dict[str, Any], before: dict[str, Any], after: dict[str, Any]) -> str:
    event_type = str(event.get("event_type") or "")
    if event_type == "investment_recorded":
        if n(after.get("last_loan_used_gp")) > 0:
            return "loan_used"
        if n(after.get("last_stake_gp")) <= 0:
            return "risk_reduction"
        return "selective_risk"
    if event_type == "settlement_recorded":
        profit = n((event.get("settlement") or {}).get("profit_gp"))
        if profit < 0:
            return "loss_review"
        if profit > 0:
            return "profit_lock"
        return "neutral"
    if before.get("credit_grade") != after.get("credit_grade"):
        return "credit_shift"
    return "constraint_update" if event_type in {"credit_updated", "survival_updated"} else "information_update"


def reconstruct_decision(event: dict[str, Any], prompt_context: dict[str, Any], memory: dict[str, Any]) -> dict[str, Any]:
    event_type = str(event.get("event_type") or "")
    private_context = prompt_context.get("private_context") or {}
    public_context = prompt_context.get("public_context") or {}
    profile = (memory.get("profile") or {})
    markets = public_context.get("markets") or public_context.get("matches") or []
    if event_type == "forecast_recorded":
        decision = f"generated {len(event.get('forecasts') or [])} forecasts"
    elif event_type == "investment_recorded":
        investments = [row for row in event.get("investments") or [] if isinstance(row, dict)]
        primary = next((row for row in investments if str(row.get("action") or "").lower() == "bet"), investments[0] if investments else {})
        if primary:
            decision = f"{primary.get('action', 'decision')} {primary.get('match_id', '')} {primary.get('market', '')} {n(primary.get('stake_gp')):.0f} GP".strip()
        else:
            decision = "no investment decision"
    elif event_type == "settlement_recorded":
        decision = f"settled profit {n((event.get('settlement') or {}).get('profit_gp')):+.0f} GP"
    else:
        decision = _outcome_for_event(event)
    return {
        "prompt_available": bool(prompt_context),
        "prompt_summary": {
            "market_count": len(markets) if isinstance(markets, list) else 0,
            "rule_version": prompt_context.get("rule_version") or public_context.get("rule_version"),
            "memory_contract": bool(private_context.get("behavior_kernel")),
        },
        "memory_summary": {
            "behavior_type": profile.get("behavior_type"),
            "risk_level": profile.get("risk_level"),
            "loan_dependency": profile.get("loan_dependency"),
            "dominant_pattern": ((memory.get("top_patterns") or [{}])[0]).get("name"),
        },
        "decision": decision,
    }


def generate_counterfactual(event: dict[str, Any], before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    event_type = str(event.get("event_type") or "")
    if event_type == "investment_recorded":
        stake = n(after.get("last_stake_gp"))
        loan = n(after.get("last_loan_used_gp"))
        if loan > 0:
            return {
                "question": "如果不使用贷款会怎样？",
                "alternative": f"将本轮敞口限制在自有资金内，最多减少 {loan:.0f} GP 债务压力。",
                "expected_effect": "降低爆仓和末位惩罚风险，但可能牺牲追排名速度。",
            }
        if stake <= 0:
            return {
                "question": "如果强制下注会怎样？",
                "alternative": "使用最小仓位测试最高置信市场，而不是完全 no-bet。",
                "expected_effect": "获得结果样本，但会降低纪律分并暴露不必要风险。",
            }
        return {
            "question": "如果降低仓位会怎样？",
            "alternative": f"将 {stake:.0f} GP 投入拆成更小单位或保留现金。",
            "expected_effect": "降低单场波动，增加后续回合生存能力。",
        }
    if event_type == "settlement_recorded":
        profit = n((event.get("settlement") or {}).get("profit_gp"))
        if profit < 0:
            return {
                "question": "如果赛前选择 no-bet 会怎样？",
                "alternative": "避免本场亏损，把信用和本金留给下一轮。",
                "expected_effect": "排名短期少动，但减少亏损后的策略扭曲。",
            }
        if profit > 0:
            return {
                "question": "如果赛前更保守会怎样？",
                "alternative": "盈利减少但波动更低。",
                "expected_effect": "更稳，但可能错过排名奖励窗口。",
            }
    return {
        "question": "这个事件如何影响下一轮？",
        "alternative": "下一轮 prompt 必须引用该事件，并说明是否改变仓位、贷款或 no-bet 策略。",
        "expected_effect": "让行为记忆产生可检验的因果影响。",
    }


def build_replay_for_run(
    run_id: str,
    seat_ids: list[str] | None = None,
    *,
    write: bool = True,
) -> dict[str, Any]:
    seat_ids = seat_ids or PRODUCTION_SEATS
    events: list[dict[str, Any]] = []
    snapshots: dict[str, dict[str, Any]] = {}
    for seat_id in seat_ids:
        seat_events = [event for event in _seat_events(seat_id) if str(event.get("run_id")) == str(run_id)]
        memory = compile_behavior_memory(seat_id, write=False)
        prompt_context = _prompt_context(seat_id, run_id)
        history_before: list[dict[str, Any]] = []
        for index, event in enumerate(seat_events):
            before = _state_from_events(seat_id, history_before, memory)
            after_history = [*history_before, event]
            after = _state_from_events(seat_id, after_history, memory)
            event_id = f"{run_id}:{seat_id}:{index}:{event.get('event_type') or 'event'}"
            snapshot_id = _safe_token(event_id)
            replay_event = {
                "event_id": event_id,
                "run_id": run_id,
                "seat_id": seat_id,
                "timestamp": event.get("ts") or now_iso(),
                "event_type": event.get("event_type") or "event",
                "action": _action_for_event(event),
                "outcome": _outcome_for_event(event),
                "risk_shift": _risk_shift(event, before, after),
                "state_before": before,
                "state_after": after,
                "decision_reconstruction": reconstruct_decision(event, prompt_context, memory),
                "counterfactual": generate_counterfactual(event, before, after),
                "source_event": {
                    "event_type": event.get("event_type"),
                    "status": event.get("status"),
                    "forecast_count": len(event.get("forecasts") or []),
                    "investment_count": len(event.get("investments") or []),
                },
                "snapshot_ref": f"data/pool/replay/snapshots/{snapshot_id}.json",
            }
            events.append(replay_event)
            snapshots[snapshot_id] = {
                "version": "behavior_replay_snapshot.v1",
                "generated_at": now_iso(),
                "event": replay_event,
            }
            history_before = after_history
    events.sort(key=lambda row: (str(row.get("timestamp") or ""), str(row.get("seat_id") or ""), str(row.get("event_type") or "")))
    seat_index: dict[str, dict[str, Any]] = {}
    for event in events:
        row = seat_index.setdefault(event["seat_id"], {
            "seat_id": event["seat_id"],
            "event_count": 0,
            "risk_shifts": [],
            "events": [],
        })
        row["event_count"] += 1
        row["risk_shifts"].append(event["risk_shift"])
        row["events"].append(event["event_id"])
    replay = {
        "version": "behavior_replay.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "event_count": len(events),
        "seat_count": len(seat_index),
        "timeline": events,
        "seat_index": seat_index,
    }
    if write:
        write_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", replay)
        write_json(DATA_ROOT / "replay" / "runs" / "latest.json", replay)
        for snapshot_id, payload in snapshots.items():
            write_json(DATA_ROOT / "replay" / "snapshots" / f"{snapshot_id}.json", payload)
    return replay
