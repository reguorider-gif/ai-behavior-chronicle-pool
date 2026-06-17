from __future__ import annotations

from typing import Any

from .behavior_compiler import compile_behavior_memory
from .behavior_production_kernel import KERNEL_VERSION


def behavior_memory_for_prompt(seat_id: str) -> dict[str, Any]:
    memory = compile_behavior_memory(seat_id, write=True)
    profile = memory.get("profile") or {}
    patterns = memory.get("top_patterns") or []
    timeline = memory.get("recent_timeline_events") or []
    return {
        "kernel_version": KERNEL_VERSION,
        "profile": {
            "behavior_type": profile.get("behavior_type"),
            "risk_level": profile.get("risk_level"),
            "loan_dependency": profile.get("loan_dependency"),
            "no_bet_rate": profile.get("no_bet_rate"),
            "strategy_drift": profile.get("strategy_drift"),
            "settlement_profit_gp": profile.get("settlement_profit_gp"),
            "recovery_mode": profile.get("recovery_mode"),
        },
        "active_patterns": patterns[:5],
        "recent_timeline_events": timeline[-6:],
        "decision_contract": {
            "must_consider_memory": True,
            "kernel_version": KERNEL_VERSION,
            "required_receipt_fields": [
                "memory_used",
                "memory_not_used_reason",
                "strategy_change_from_memory",
            ],
            "instruction": "下一轮必须说明历史行为模式是否影响本轮 forecast/investment；如未影响，必须给出原因。",
        },
    }


def inject_behavior_memory(context: dict[str, Any], seat_id: str) -> dict[str, Any]:
    memory = behavior_memory_for_prompt(seat_id)
    private_context = dict(context.get("private_context") or {})
    private_context["behavior_kernel"] = memory
    public_context = dict(context.get("public_context") or {})
    output_contract = dict(public_context.get("output_contract") or {})
    output_contract["behavior_memory_required_fields"] = memory["decision_contract"]["required_receipt_fields"]
    public_context["output_contract"] = output_contract
    return {
        **context,
        "public_context": public_context,
        "private_context": private_context,
        "behavior_kernel_version": KERNEL_VERSION,
    }


def behavior_memory_prompt_text(memory: dict[str, Any]) -> str:
    profile = memory.get("profile") or {}
    patterns = memory.get("active_patterns") or []
    timeline = memory.get("recent_timeline_events") or []
    pattern_lines = []
    for pattern in patterns[:5]:
        pattern_lines.append(
            f"- {pattern.get('label') or pattern.get('name')}: confidence={pattern.get('confidence')}, "
            f"support={pattern.get('supporting_events')}, note={pattern.get('note') or ''}"
        )
    timeline_lines = []
    for event in timeline[-5:]:
        timeline_lines.append(
            f"- {event.get('run_id')}: {event.get('action')} → {event.get('outcome')}；risk_shift={event.get('risk_shift')}"
        )
    return "\n".join([
        "你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：",
        f"- 行为类型：{profile.get('behavior_type') or 'unknown'}",
        f"- 风险等级：{profile.get('risk_level') or 'unknown'}",
        f"- 贷款依赖：{profile.get('loan_dependency') or 'unknown'}",
        f"- no-bet 比率：{profile.get('no_bet_rate')}",
        f"- 策略漂移：{profile.get('strategy_drift') or 'unknown'}",
        "- 活跃模式：",
        *(pattern_lines or ["- insufficient_history: 暂无足够历史，保持谨慎。"]),
        "- 最近行为节点：",
        *(timeline_lines or ["- 暂无历史节点。"]),
        "本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。",
    ])
