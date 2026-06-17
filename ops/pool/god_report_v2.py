from __future__ import annotations

from collections import Counter
from typing import Any

from .behavior_journal import build_god_run_summary
from .io_utils import read_json, write_json
from .paths import DATA_ROOT
from .rules_engine import n

try:
    from pred_invest_seat_registry import PRODUCTION_SEATS, canonical_seat_id
except Exception:  # pragma: no cover - fallback for direct package imports
    PRODUCTION_SEATS = [
        "chatgpt",
        "deepseek",
        "mimo",
        "minimax",
        "doubao",
        "gemini",
        "kimi",
        "meta",
        "qwen",
        "wenxin",
        "grok",
        "yuanbao",
    ]

    def canonical_seat_id(value: Any) -> str:
        raw = str(value or "").strip().lower()
        return {"xai": "grok", "xai grok": "grok"}.get(raw, raw.replace(" ", ""))


def _fmt_gp(value: Any) -> str:
    return f"{n(value):.0f} GP"


def _production_seat_map(payload: dict[str, Any]) -> dict[str, Any]:
    required = set(PRODUCTION_SEATS)
    result: dict[str, Any] = {}
    seats = payload.get("seats") if isinstance(payload.get("seats"), dict) else {}
    for raw_seat, row in seats.items():
        seat_id = canonical_seat_id(raw_seat)
        if seat_id in required:
            result[seat_id] = row
    return result


def generate_god_report(date: str, run_id: str) -> dict[str, Any]:
    run_summary = build_god_run_summary(run_id)
    forecasts = read_json(DATA_ROOT / "forecast_receipts" / f"{run_id}.json", {"seats": {}})
    investments = read_json(DATA_ROOT / "investment_receipts" / f"{run_id}.json", {"seats": {}})
    credit = read_json(DATA_ROOT / "credit_ledger" / f"{run_id}.json", {"seats": {}})
    survival = read_json(DATA_ROOT / "survival_ledger" / f"{run_id}.json", {"seats": {}})
    settlement = read_json(DATA_ROOT / "settlements" / f"{run_id}.json", {"seats": {}})
    pattern_graph = read_json(DATA_ROOT / "pattern_graph" / f"{run_id}.json", {})
    if not pattern_graph.get("top_patterns"):
        pattern_graph = read_json(DATA_ROOT / "pattern_graph" / "latest.json", {"top_patterns": []})
    agent_profiles = read_json(DATA_ROOT / "agent_profiles" / f"{run_id}.json", {})
    if not agent_profiles.get("seats"):
        agent_profiles = read_json(DATA_ROOT / "agent_profiles" / "latest.json", {"seats": {}})
    evolution_trace = read_json(DATA_ROOT / "evolution_traces" / f"{run_id}.json", {})
    if not evolution_trace.get("traces"):
        evolution_trace = read_json(DATA_ROOT / "evolution_traces" / "latest.json", {"traces": []})
    behavior_replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    if not behavior_replay.get("timeline"):
        behavior_replay = read_json(DATA_ROOT / "replay" / "runs" / "latest.json", {"timeline": []})
    forecast_seats = _production_seat_map(forecasts)
    investment_seats = _production_seat_map(investments)
    credit_seats = _production_seat_map(credit)
    survival_seats = _production_seat_map(survival)
    settlement_seats = _production_seat_map(settlement)
    profile_seats = _production_seat_map(agent_profiles)
    required = set(PRODUCTION_SEATS)
    run_events = [
        event
        for event in run_summary.get("events") or []
        if not event.get("seat_id") or canonical_seat_id(event.get("seat_id")) in required
    ]
    seats_seen = {
        canonical_seat_id(seat_id)
        for seat_id in (run_summary.get("seats") or [])
        if canonical_seat_id(seat_id) in required
    }
    seats_seen |= set(forecast_seats) | set(investment_seats)
    seats = [seat_id for seat_id in PRODUCTION_SEATS if seat_id in seats_seen]

    seat_cards = []
    action_counts: Counter[str] = Counter()
    no_bet_count = 0
    bet_count = 0
    recovery_count = 0
    for seat_id in seats:
        receipt = investment_seats.get(seat_id, {})
        forecast = forecast_seats.get(seat_id, {})
        credit_row = credit_seats.get(seat_id, {})
        survival_row = survival_seats.get(seat_id, {})
        settlement_row = settlement_seats.get(seat_id, {})
        profile = profile_seats.get(seat_id, {})
        items = receipt.get("investments") or []
        bets = [item for item in items if item.get("action") == "bet"]
        no_bets = [item for item in items if item.get("action") == "no_bet"]
        bet_count += len(bets)
        no_bet_count += len(no_bets)
        recovery_count += 1 if survival_row.get("recovery_mode") else 0
        for item in items:
            action_counts[str(item.get("action") or "unknown")] += 1
        stake = sum(n(item.get("stake_gp")) for item in bets)
        loan = sum(n(item.get("loan_used_gp")) for item in bets)
        seat_cards.append({
            "seat_id": seat_id,
            "forecast_count": len(forecast.get("forecasts") or []),
            "bet_count": len(bets),
            "no_bet_count": len(no_bets),
            "stake_gp": round(stake, 2),
            "loan_used_gp": round(loan, 2),
            "credit_delta": credit_row.get("credit_delta", 0),
            "credit_grade": credit_row.get("credit_grade"),
            "net_worth_gp": survival_row.get("net_worth_gp"),
            "recovery_mode": bool(survival_row.get("recovery_mode")),
            "settlement_profit_gp": settlement_row.get("profit_gp", 0),
            "behavior_type": profile.get("behavior_type"),
            "risk_level": profile.get("risk_level"),
            "loan_dependency": profile.get("loan_dependency"),
            "no_bet_rate": profile.get("no_bet_rate"),
            "strategy_drift": profile.get("strategy_drift"),
            "top_patterns": (profile.get("top_patterns") or [])[:3],
        })

    top_patterns = pattern_graph.get("top_patterns") or []
    lines = [
        f"# AI Judge 上帝日报 V2 - {date} {run_id}",
        "",
        "## 总览",
        f"- 本轮席位：{len(seats)}",
        f"- 投注动作：{bet_count} 笔；no-bet：{no_bet_count} 笔",
        f"- Recovery Mode 席位：{recovery_count}",
        f"- 上帝 ledger 事件：{len(run_events)} 条",
        "",
        "## 预测-投资偏离",
        "- 观察 forecast 覆盖与实际下注分离：预测必须全覆盖，下注允许 no-bet，避免模型为了下注而伪造确定性。",
        "",
        "## 贷款压力",
        "- 贷款额度由信用分和净资产共同决定；净资产小于等于 0 的席位进入重整状态并冻结新增贷款。",
        "",
        "## no-bet 纪律",
        f"- 本轮 no-bet {no_bet_count} 笔。no-bet 不是缺席，而是需要写明边际不足、信息缺口或生存约束。",
        "",
        "## 重整状态",
        f"- 当前重整席位 {recovery_count} 个。重整席位仍可 forecast，但投资被限制为小额恢复或 no-bet。",
        "",
        "## 策略漂移",
        "- 本日报记录行为路径、模式压缩和个体漂移；下一轮每个模型只收到自己的历史摘要。",
        "",
        "## 行为回放",
        f"- 本轮可回放事件 {behavior_replay.get('event_count', len(behavior_replay.get('timeline') or []))} 条，"
        f"覆盖席位 {behavior_replay.get('seat_count', len(behavior_replay.get('seat_index') or {}))} 个。",
        "- 回放节点包含当时状态、决策重建和反事实，不暴露 raw prompt。",
        "",
        "## 行为通鉴 Top Patterns",
    ]
    if top_patterns:
        for pattern in top_patterns:
            seats_text = ", ".join(pattern.get("seats") or [])
            lines.append(
                f"- {pattern.get('label') or pattern.get('name')}：confidence {pattern.get('confidence')}，"
                f"support {pattern.get('supporting_events')}，来源席位 {seats_text or 'n/a'}。"
            )
    else:
        lines.append("- 暂无足够行为模式，下一轮继续观察。")
    lines += [
        "",
        "## 席位点评",
    ]
    for card in seat_cards:
        posture = "重整" if card["recovery_mode"] else "正常"
        profile_text = (
            f"行为 {card.get('behavior_type') or 'unknown'}，风险 {card.get('risk_level') or 'unknown'}，"
            f"贷款依赖 {card.get('loan_dependency') or 'unknown'}，漂移 {card.get('strategy_drift') or 'unknown'}"
        )
        lines.append(
            f"- {card['seat_id']}: forecast {card['forecast_count']} 场，bet {card['bet_count']} 笔，"
            f"no-bet {card['no_bet_count']} 笔，投入 {_fmt_gp(card['stake_gp'])}，贷款 {_fmt_gp(card['loan_used_gp'])}，"
            f"信用Δ {card['credit_delta']}，净值 {_fmt_gp(card['net_worth_gp'])}，状态 {posture}；{profile_text}。"
        )
    report = {
        "date": date,
        "run_id": run_id,
        "seat_count": len(seats),
        "event_count": len(run_events),
        "action_counts": dict(action_counts),
        "seat_cards": seat_cards,
        "behavior_patterns": top_patterns,
        "agent_profiles": agent_profiles,
        "evolution_trace": evolution_trace,
        "behavior_replay": {
            "version": behavior_replay.get("version"),
            "run_id": behavior_replay.get("run_id"),
            "event_count": behavior_replay.get("event_count", len(behavior_replay.get("timeline") or [])),
            "seat_count": behavior_replay.get("seat_count", len(behavior_replay.get("seat_index") or {})),
        },
        "markdown": "\n".join(lines) + "\n",
    }
    write_json(DATA_ROOT / "god_reports" / f"{date}_{run_id}.json", report)
    path = DATA_ROOT / "god_reports" / f"{date}_{run_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report["markdown"], encoding="utf-8")
    return report
