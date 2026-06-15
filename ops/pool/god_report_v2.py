from __future__ import annotations

from collections import Counter
from typing import Any

from .behavior_journal import build_god_run_summary
from .io_utils import read_json, write_json
from .paths import DATA_ROOT
from .rules_engine import n


def _fmt_gp(value: Any) -> str:
    return f"{n(value):.0f} GP"


def generate_god_report(date: str, run_id: str) -> dict[str, Any]:
    run_summary = build_god_run_summary(run_id)
    forecasts = read_json(DATA_ROOT / "forecast_receipts" / f"{run_id}.json", {"seats": {}})
    investments = read_json(DATA_ROOT / "investment_receipts" / f"{run_id}.json", {"seats": {}})
    credit = read_json(DATA_ROOT / "credit_ledger" / f"{run_id}.json", {"seats": {}})
    survival = read_json(DATA_ROOT / "survival_ledger" / f"{run_id}.json", {"seats": {}})
    settlement = read_json(DATA_ROOT / "settlements" / f"{run_id}.json", {"seats": {}})
    seats = sorted(set(run_summary.get("seats") or []) | set((forecasts.get("seats") or {}).keys()) | set((investments.get("seats") or {}).keys()))

    seat_cards = []
    action_counts: Counter[str] = Counter()
    no_bet_count = 0
    bet_count = 0
    recovery_count = 0
    for seat_id in seats:
        receipt = (investments.get("seats") or {}).get(seat_id, {})
        forecast = (forecasts.get("seats") or {}).get(seat_id, {})
        credit_row = (credit.get("seats") or {}).get(seat_id, {})
        survival_row = (survival.get("seats") or {}).get(seat_id, {})
        settlement_row = (settlement.get("seats") or {}).get(seat_id, {})
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
        })

    lines = [
        f"# AI Judge 上帝日报 V2 - {date} {run_id}",
        "",
        "## 总览",
        f"- 本轮席位：{len(seats)}",
        f"- 投注动作：{bet_count} 笔；no-bet：{no_bet_count} 笔",
        f"- Recovery Mode 席位：{recovery_count}",
        f"- 上帝 ledger 事件：{run_summary.get('event_count', 0)} 条",
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
        "- 本日报只记录行为路径，不向模型泄露其他席位明细；下一轮每个模型只收到自己的历史摘要。",
        "",
        "## 席位点评",
    ]
    for card in seat_cards:
        posture = "重整" if card["recovery_mode"] else "正常"
        lines.append(
            f"- {card['seat_id']}: forecast {card['forecast_count']} 场，bet {card['bet_count']} 笔，"
            f"no-bet {card['no_bet_count']} 笔，投入 {_fmt_gp(card['stake_gp'])}，贷款 {_fmt_gp(card['loan_used_gp'])}，"
            f"信用Δ {card['credit_delta']}，净值 {_fmt_gp(card['net_worth_gp'])}，状态 {posture}。"
        )
    report = {
        "date": date,
        "run_id": run_id,
        "seat_count": len(seats),
        "event_count": run_summary.get("event_count", 0),
        "action_counts": dict(action_counts),
        "seat_cards": seat_cards,
        "markdown": "\n".join(lines) + "\n",
    }
    write_json(DATA_ROOT / "god_reports" / f"{date}_{run_id}.json", report)
    path = DATA_ROOT / "god_reports" / f"{date}_{run_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report["markdown"], encoding="utf-8")
    return report
