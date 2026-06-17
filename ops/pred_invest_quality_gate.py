#!/usr/bin/env python3
"""PRED-INVEST publish gate and rerun queue.

This turns bridge audit output into a product-level safety state. The frontend
and daily SOP should consume this instead of guessing whether a round is
complete from "some seats answered".
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import audit_pred_invest_bridge_outputs as bridge_audit
from pred_invest_seat_registry import PRODUCTION_SEATS, REQUIRED_SEAT_COUNT, display_name_for_seat


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
REQUIRED_SEATS = list(PRODUCTION_SEATS)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _classify_action(seat_result: dict[str, Any]) -> dict[str, Any]:
    seat = seat_result.get("seat")
    issues = seat_result.get("issues") or []
    errors = seat_result.get("last_errors") or []
    issue_text = ",".join(str(item) for item in issues)
    error_text = ",".join(str((item or {}).get("reason") or (item or {}).get("action") or "") for item in errors)
    text = f"{issue_text},{error_text}".lower()
    latest_blocking_error = next(
        (
            error
            for error in reversed(errors)
            if str((error or {}).get("reason") or "").lower() == "provider_quota_limited"
        ),
        None,
    )
    display_run_id = (
        latest_blocking_error.get("run_id")
        if isinstance(latest_blocking_error, dict) and latest_blocking_error.get("run_id")
        else seat_result.get("run_id")
    )
    display_response_chars = (
        latest_blocking_error.get("response_chars")
        if isinstance(latest_blocking_error, dict) and latest_blocking_error.get("response_chars") is not None
        else seat_result.get("response_chars")
    )
    if "provider_quota_limited" in text:
        mode = "provider_quota_blocked"
        prompt_mode = "wait_for_quota_reset"
        reason = "供应商额度限制，页面未生成当前轮答案；不能继续普通补跑，需额度恢复后单席重试。"
    elif "no_captured_response" in text or "response_not_relevant" in text or "existing page answer marker did not match" in text:
        mode = "fresh_chat_marker_required"
        prompt_mode = "compact_json_no_ultra"
        reason = "未捕获当前轮答案或页面仍停留旧上下文，必须新会话/新 marker 重投。"
    elif "response_not_json" in text:
        mode = "json_truncation_or_schema_failure"
        prompt_mode = "compact_json_no_ultra"
        reason = "有文本但不是可解析完整 JSON，多数是网页截断或混入 UI 文案。"
    elif "missing_forecasts" in text or "missing_investments" in text:
        mode = "coverage_failure"
        prompt_mode = "compact_json_no_ultra"
        reason = "JSON 可读但没有覆盖全部赛事，必须按最短合同重跑。"
    elif "market_snapshot_missing_but_bet_fields_present" in text:
        mode = "no_market_no_bet_repair_required"
        prompt_mode = "compact_json_no_ultra"
        reason = "该席位在无盘口赛事上填了赔率或 stake，必须按无盘口 no-bet 硬门禁重跑。"
    else:
        mode = "rerun_required"
        prompt_mode = "compact"
        reason = "未通过发布门禁，需要补跑。"
    return {
        "seat": seat,
        "display_name": display_name_for_seat(seat),
        "mode": mode,
        "prompt_mode": prompt_mode,
        "reason": reason,
        "last_run_id": display_run_id,
        "response_chars": display_response_chars,
        "issues": issues,
        "last_errors": errors,
    }


def build_gate(date: str, round_id: str, run_ids: list[str]) -> dict[str, Any]:
    audit = bridge_audit.audit(date, round_id, run_ids)
    prompt_path = OUT_DIR / f"{date}_{round_id}_prompt_pack.json"
    prompt_pack = _load_json(prompt_path) if prompt_path.exists() else {}
    required_match_ids = audit.get("required_match_ids") or []
    invalid_rows = [row for row in audit.get("seat_results") or [] if not row.get("valid")]
    rerun_queue = [_classify_action(row) for row in invalid_rows]
    queued = {str(row.get("seat")) for row in rerun_queue if row.get("seat")}
    for seat in audit.get("needs_rerun") or []:
        seat_text = str(seat)
        if seat_text in queued:
            continue
        rerun_queue.append({
            "seat": seat_text,
            "display_name": display_name_for_seat(seat_text),
            "mode": "missing_required_seat_no_response",
            "prompt_mode": "compact_json_no_ultra",
            "reason": "固定席位未捕获本轮结构化回执，必须新会话/新 marker 单席补跑。",
            "last_run_id": None,
            "response_chars": 0,
            "issues": ["required_seat_missing"],
            "last_errors": [],
        })
    provider_blocked_seats = sorted(
        str(row.get("seat"))
        for row in rerun_queue
        if row.get("seat") and row.get("mode") == "provider_quota_blocked"
    )
    rerunnable_seats = sorted(
        str(row.get("seat"))
        for row in rerun_queue
        if row.get("seat") and row.get("mode") != "provider_quota_blocked"
    )
    publish_allowed = len(audit.get("valid_seats") or []) == REQUIRED_SEAT_COUNT and not rerun_queue
    if publish_allowed:
        status = "READY"
        frontend_badge = f"{REQUIRED_SEAT_COUNT}/{REQUIRED_SEAT_COUNT} 已验证"
    elif audit.get("valid_seats"):
        status = "PARTIAL_NOT_READY"
        frontend_badge = f"{len(audit.get('valid_seats') or [])}/{REQUIRED_SEAT_COUNT} 部分回收"
    else:
        status = "NOT_READY"
        frontend_badge = f"0/{REQUIRED_SEAT_COUNT} 未回收"
    return {
        "version": "pred_invest_quality_gate.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date,
        "round_id": round_id,
        "status": status,
        "publish_allowed": publish_allowed,
        "frontend_badge": frontend_badge,
        "valid_count": len(audit.get("valid_seats") or []),
        "required_seat_count": REQUIRED_SEAT_COUNT,
        "valid_seats": audit.get("valid_seats") or [],
        "needs_rerun": audit.get("needs_rerun") or [],
        "valid_seat_labels": [
            {"seat": seat, "display_name": display_name_for_seat(seat)}
            for seat in audit.get("valid_seats") or []
        ],
        "needs_rerun_labels": [
            {"seat": seat, "display_name": display_name_for_seat(seat)}
            for seat in audit.get("needs_rerun") or []
        ],
        "rerun_queue": rerun_queue,
        "provider_blocked_seats": provider_blocked_seats,
        "rerunnable_seats": rerunnable_seats,
        "required_match_ids": required_match_ids,
        "required_match_source": audit.get("required_match_source"),
        "match_count": len(required_match_ids),
        "prompt_pack_match_count": prompt_pack.get("match_count"),
        "prompt_pack_models": prompt_pack.get("models"),
        "product_findings": [
            "发布状态必须来自 quality_gate.publish_allowed，不得只看有无任意模型答案。",
            "前端必须展示 frontend_badge 和 needs_rerun，避免用户误以为本轮已全量。",
            "日报可以引用部分上帝报告，但标题必须标注 PARTIAL_NOT_READY。",
            "自动化下一步只能补跑 rerun_queue，不应重跑已合格席位。",
            "provider_blocked_seats 不进入普通自动补跑；供应商额度/慢响应恢复后才能单席强制重试。",
            "同一轮发布门禁使用 required_match_snapshot 或上次质量门禁冻结口径，避免 prompt_pack 刷新后误伤已合格席位。",
            "供应商额度限制必须作为阻塞态呈现，不得被误判为普通 coverage failure 反复补跑。",
        ],
        "audit": audit,
    }


def write_gate(gate: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{gate['date']}_{gate['round_id']}_quality_gate"
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    json_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# PRED-INVEST Quality Gate · {gate['round_id']}",
        "",
        f"- date: {gate['date']}",
        f"- status: **{gate['status']}**",
        f"- publish allowed: {gate['publish_allowed']}",
        f"- frontend badge: {gate['frontend_badge']}",
        f"- valid seats: {gate['valid_count']}/{gate['required_seat_count']} ({', '.join(gate['valid_seats']) or '-'})",
        f"- needs rerun: {', '.join(gate['needs_rerun']) or 'none'}",
        "",
        "## Rerun Queue",
        "",
    ]
    if gate["rerun_queue"]:
        lines += ["| Seat | Mode | Prompt | Reason |", "| --- | --- | --- | --- |"]
        for row in gate["rerun_queue"]:
            lines.append(f"| {row['seat']} | {row['mode']} | {row['prompt_mode']} | {row['reason']} |")
    else:
        lines.append("- none")
    lines += ["", "## Product Findings", ""]
    lines.extend(f"- {item}" for item in gate["product_findings"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_quality_gate.json").write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_quality_gate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--runs", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    gate = build_gate(args.date, args.round_id, [item.strip() for item in args.runs.split(",") if item.strip()])
    if args.write:
        gate["paths"] = write_gate(gate)
    print(json.dumps(gate, ensure_ascii=False, indent=2))
    return 0 if gate["publish_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
