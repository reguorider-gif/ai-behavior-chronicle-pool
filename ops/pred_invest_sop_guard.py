#!/usr/bin/env python3
"""PRED-INVEST automation guard.

This is the daily SOP watchdog: it checks bridge liveness, publish quality,
and required artifacts before the frontend/report layer is allowed to treat a
round as complete.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pred_invest_quality_gate
from pool.io_utils import http_json


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
REQUIRED_SEAT_COUNT = len(pred_invest_quality_gate.REQUIRED_SEATS)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_load_error": str(exc)}


def _artifact_state(date: str, round_id: str) -> dict[str, Any]:
    prompt = OUT_DIR / f"{date}_{round_id}_prompt_pack.json"
    current = OUT_DIR / f"{date}_{round_id}_current_game.json"
    quality = OUT_DIR / f"{date}_{round_id}_quality_gate.json"
    strict = OUT_DIR / f"{date}_{round_id}_god_report_strict.json"
    artifacts = {
        "prompt_pack": str(prompt),
        "current_game": str(current),
        "quality_gate": str(quality),
        "strict_god_report": str(strict),
    }
    loaded = {
        "prompt_pack": _load_json(prompt),
        "current_game": _load_json(current),
        "quality_gate": _load_json(quality),
        "strict_god_report": _load_json(strict),
    }
    missing = [name for name, path in artifacts.items() if not Path(path).exists()]
    return {"paths": artifacts, "missing": missing, "loaded": loaded}


def _bridge_check(
    base_url: str,
    recover_stuck: bool,
    stuck_seconds: float,
    recovery_reason: str,
) -> dict[str, Any]:
    status = http_json(f"{base_url.rstrip('/')}/api/bridge/status", timeout=45)
    busy = bool(status.get("busy") or (status.get("bridge_run") or {}).get("busy"))
    active_run_id = status.get("active_run_id") or (status.get("bridge_run") or {}).get("run_id")
    elapsed = status.get("elapsed_sec")
    if elapsed is None:
        elapsed = (status.get("bridge_run") or {}).get("elapsed_seconds")
    try:
        elapsed_f = float(elapsed or 0)
    except Exception:
        elapsed_f = 0.0
    result = {
        "ok": bool(status.get("available", True)) and not busy,
        "busy": busy,
        "active_run_id": active_run_id,
        "elapsed_seconds": elapsed_f,
        "can_start_new_run": bool(status.get("can_start_new_run", not busy)),
        "status": status,
        "recovered": False,
        "recovery": None,
    }
    if busy and recover_stuck and elapsed_f >= stuck_seconds:
        payload = {"run_id": active_run_id, "reason": recovery_reason}
        recovery = http_json(f"{base_url.rstrip('/')}/api/bridge/recover", payload=payload, timeout=45)
        after = http_json(f"{base_url.rstrip('/')}/api/bridge/status", timeout=45)
        after_busy = bool(after.get("busy") or (after.get("bridge_run") or {}).get("busy"))
        result.update({
            "ok": bool(after.get("available", True)) and not after_busy,
            "busy": after_busy,
            "active_run_id": after.get("active_run_id") or (after.get("bridge_run") or {}).get("run_id"),
            "can_start_new_run": bool(after.get("can_start_new_run", not after_busy)),
            "recovered": True,
            "recovery": recovery,
            "status_after_recovery": after,
        })
    return result


def _guard_status(errors: list[str], warnings: list[str], quality_gate: dict[str, Any] | None) -> str:
    if errors:
        return "NOT_READY"
    if quality_gate and quality_gate.get("status") != "READY":
        return "PARTIAL_NOT_READY"
    if warnings:
        return "READY_WITH_WARNINGS"
    return "READY"


def build_guard(
    date: str,
    round_id: str,
    run_ids: list[str],
    bridge_base_url: str = "http://127.0.0.1:8501",
    recover_stuck: bool = False,
    stuck_seconds: float = 300.0,
    rebuild_quality_gate: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    artifacts = _artifact_state(date, round_id)
    if artifacts["missing"]:
        warnings.append("missing_artifacts:" + ",".join(artifacts["missing"]))

    bridge = _bridge_check(
        bridge_base_url,
        recover_stuck=recover_stuck,
        stuck_seconds=stuck_seconds,
        recovery_reason=f"pred_invest_sop_guard_{round_id}",
    )
    if bridge.get("busy"):
        errors.append(f"bridge_busy:{bridge.get('active_run_id') or 'unknown'}")
    if bridge.get("recovered"):
        warnings.append("bridge_recovered_from_stuck_run")

    loaded_gate = artifacts["loaded"].get("quality_gate") or {}
    if not rebuild_quality_gate and loaded_gate.get("version") == "pred_invest_quality_gate.v1":
        gate = loaded_gate
        gate_source = "artifact"
    else:
        gate = pred_invest_quality_gate.build_gate(date, round_id, run_ids) if run_ids else None
        gate_source = "rebuilt" if gate else "missing"
    if gate:
        if not gate.get("publish_allowed"):
            warnings.append(f"publish_blocked_by_quality_gate:{gate.get('valid_count')}/{gate.get('required_seat_count')}")
        prompt_models = gate.get("prompt_pack_models")
        prompt_matches = gate.get("prompt_pack_match_count")
        if prompt_models != REQUIRED_SEAT_COUNT:
            errors.append(f"prompt_pack_models_not_{REQUIRED_SEAT_COUNT}:{prompt_models}")
        if not prompt_matches:
            errors.append("prompt_pack_has_no_matches")

    current = artifacts["loaded"].get("current_game") or {}
    current_gate = current.get("quality_gate") if isinstance(current.get("quality_gate"), dict) else {}
    for row in current.get("model_summaries") or []:
        if not isinstance(row, dict):
            continue
        account = str(row.get("model_account") or "").lower() or "unknown"
        terms = row.get("loan_terms") if isinstance(row.get("loan_terms"), dict) else {}
        try:
            net_worth = float(terms.get("net_worth_gp") or 0)
        except Exception:
            net_worth = 0.0
        try:
            loan_gp = float(terms.get("outstanding_loan_gp") or 0)
        except Exception:
            loan_gp = 0.0
        if net_worth < 0:
            warnings.append(f"negative_net_worth:{account}:{net_worth:g}GP")
        if loan_gp > 0 and terms.get("base_interest_rate") is None:
            warnings.append(f"loan_interest_rate_missing:{account}:{loan_gp:g}GP")
        if loan_gp > max(net_worth, 0) + 3000:
            warnings.append(f"debt_spiral_watch:{account}:loan={loan_gp:g}GP,net={net_worth:g}GP")
    if gate and current_gate:
        if current_gate.get("status") != gate.get("status"):
            errors.append(f"current_game_quality_gate_mismatch:{current_gate.get('status')}!={gate.get('status')}")
        if current_gate.get("publish_allowed") != gate.get("publish_allowed"):
            errors.append("current_game_publish_allowed_mismatch")
    if current and gate and current.get("verdict") == "READY" and not gate.get("publish_allowed"):
        errors.append("current_game_ready_but_quality_gate_blocks_publish")

    recommended_actions: list[str] = []
    if bridge.get("busy"):
        recommended_actions.append("先调用 /api/bridge/recover 释放卡住 run，再禁止启动新一轮。")
    provider_blocked = gate.get("provider_blocked_seats") if gate else []
    rerunnable = gate.get("rerunnable_seats") if gate else []
    if provider_blocked:
        recommended_actions.append(
            "供应商阻塞席位 "
            + ", ".join(str(item) for item in provider_blocked)
            + " 暂停普通补跑；额度/慢响应恢复后使用 --force-provider-blocked 做单席重试。"
        )
    if rerunnable:
        recommended_actions.append("只补跑 rerunnable_seats 中的缺席席位，不重跑已合格席位。")
    elif gate and gate.get("rerun_queue") and not provider_blocked:
        recommended_actions.append("只补跑 rerun_queue 中的缺席席位，不重跑已合格席位。")
    if gate and not gate.get("publish_allowed"):
        recommended_actions.append("前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。")
    if not recommended_actions:
        recommended_actions.append("可以进入发布/部署/日报生成。")

    status = _guard_status(errors, warnings, gate)
    return {
        "version": "pred_invest_sop_guard.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date,
        "round_id": round_id,
        "status": status,
        "ok_to_start_new_run": not bridge.get("busy"),
        "ok_to_publish_frontend": bool(gate and gate.get("publish_allowed")) and not errors,
        "errors": errors,
        "warnings": warnings,
        "bridge": {
            "busy": bridge.get("busy"),
            "active_run_id": bridge.get("active_run_id"),
            "elapsed_seconds": bridge.get("elapsed_seconds"),
            "can_start_new_run": bridge.get("can_start_new_run"),
            "recovered": bridge.get("recovered"),
            "recovery": bridge.get("recovery"),
        },
        "quality_gate": {
            "status": gate.get("status") if gate else None,
            "publish_allowed": gate.get("publish_allowed") if gate else False,
            "valid_count": gate.get("valid_count") if gate else 0,
            "required_seat_count": gate.get("required_seat_count") if gate else REQUIRED_SEAT_COUNT,
            "valid_seats": gate.get("valid_seats") if gate else [],
            "needs_rerun": gate.get("needs_rerun") if gate else [],
            "rerun_queue": gate.get("rerun_queue") if gate else [],
            "provider_blocked_seats": gate.get("provider_blocked_seats") if gate else [],
            "rerunnable_seats": gate.get("rerunnable_seats") if gate else [],
            "source": gate_source,
        },
        "artifacts": {
            "missing": artifacts["missing"],
            "paths": artifacts["paths"],
        },
        "recommended_actions": recommended_actions,
    }


def write_guard(guard: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{guard['date']}_{guard['round_id']}_sop_guard"
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    text = json.dumps(guard, ensure_ascii=False, indent=2) + "\n"
    json_path.write_text(text, encoding="utf-8")
    (OUT_DIR / "latest_sop_guard.json").write_text(text, encoding="utf-8")

    lines = [
        f"# PRED-INVEST SOP Guard · {guard['round_id']}",
        "",
        f"- date: {guard['date']}",
        f"- status: **{guard['status']}**",
        f"- bridge: {'busy' if guard['bridge']['busy'] else 'idle'}",
        f"- recovered bridge: {guard['bridge']['recovered']}",
        f"- quality gate: {guard['quality_gate']['status']} ({guard['quality_gate']['valid_count']}/{guard['quality_gate']['required_seat_count']})",
        f"- quality gate source: {guard['quality_gate'].get('source')}",
        f"- publish frontend: {guard['ok_to_publish_frontend']}",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- {item}" for item in guard["errors"]) if guard["errors"] else lines.append("- none")
    lines += ["", "## Warnings", ""]
    lines.extend(f"- {item}" for item in guard["warnings"]) if guard["warnings"] else lines.append("- none")
    lines += ["", "## Needs Rerun", ""]
    needs = guard["quality_gate"].get("needs_rerun") or []
    lines.append("- " + (", ".join(needs) if needs else "none"))
    lines += ["", "## Recommended Actions", ""]
    lines.extend(f"- {item}" for item in guard["recommended_actions"])
    md = "\n".join(lines) + "\n"
    md_path.write_text(md, encoding="utf-8")
    (OUT_DIR / "latest_sop_guard.md").write_text(md, encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--runs", default="")
    parser.add_argument("--bridge-base-url", default="http://127.0.0.1:8501")
    parser.add_argument("--recover-stuck-bridge", action="store_true")
    parser.add_argument("--stuck-seconds", type=float, default=300.0)
    parser.add_argument("--rebuild-quality-gate", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    run_ids = [item.strip() for item in args.runs.split(",") if item.strip()]
    guard = build_guard(
        args.date,
        args.round_id,
        run_ids,
        bridge_base_url=args.bridge_base_url.rstrip("/"),
        recover_stuck=args.recover_stuck_bridge,
        stuck_seconds=args.stuck_seconds,
        rebuild_quality_gate=args.rebuild_quality_gate,
    )
    if args.write:
        guard["paths"] = write_guard(guard)
    print(json.dumps(guard, ensure_ascii=False, indent=2))
    return 0 if guard["status"] in {"READY", "READY_WITH_WARNINGS", "PARTIAL_NOT_READY"} and not guard["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
