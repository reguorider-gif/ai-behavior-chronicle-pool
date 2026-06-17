#!/usr/bin/env python3
"""Build a client-review bundle for the current PRED-INVEST game state.

The bundle is intentionally separate from the live deployment. It lets us
review the new rules, existing run receipts, rule-converted stake caps, and
remaining automation gaps before publishing anything to the production client.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import sys
from typing import Any

import pred_invest_quality_gate
from pred_invest_rules import gp


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
REQUIRED_SEAT_COUNT = len(pred_invest_quality_gate.REQUIRED_SEATS)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def status_label(value: str) -> str:
    labels = {
        "allowed": "可入账",
        "cap_warning": "需降额",
        "no_bet_or_invalid": "无有效下注",
        "loan_limit_rejected": "贷款冲突",
    }
    return labels.get(value, value or "未知")


def match_label(match: dict[str, Any]) -> str:
    return f"{match.get('home_team') or '主队'} vs {match.get('away_team') or '客队'}"


def h(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def audit_rows(shadow: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in shadow.get("models_detail") or []:
        terms = model.get("loan_terms") or {}
        for item in model.get("audits") or []:
            bet = item.get("bet") or {}
            audit = item.get("audit") or {}
            cap = audit.get("stake_cap") or {}
            original_stake = float(bet.get("stake_gp") or 0)
            cap_stake = float(cap.get("max_stake_gp") or 0)
            converted_stake = min(original_stake, cap_stake) if cap_stake > 0 else original_stake
            rows.append(
                {
                    "model_account": model.get("model_account"),
                    "display_name": model.get("display_name"),
                    "rank": model.get("rank"),
                    "credit_grade": terms.get("credit_grade"),
                    "credit_score": terms.get("credit_score"),
                    "net_worth_gp": terms.get("net_worth_gp"),
                    "available_loan_gp": terms.get("available_loan_gp"),
                    "match_id": bet.get("match_id"),
                    "selection": bet.get("selection"),
                    "market": bet.get("market"),
                    "line": bet.get("line"),
                    "odds": bet.get("odds"),
                    "original_stake_gp": original_stake,
                    "converted_stake_gp": converted_stake,
                    "stake_cap_gp": cap_stake,
                    "status": audit.get("status"),
                    "status_label": status_label(str(audit.get("status") or "")),
                    "warnings": audit.get("warnings") or [],
                    "rationale": bet.get("rationale") or "",
                }
            )
    return rows


def model_summaries(shadow: dict[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for model in shadow.get("models_detail") or []:
        rows = []
        original_total = 0.0
        converted_total = 0.0
        for item in model.get("audits") or []:
            bet = item.get("bet") or {}
            audit = item.get("audit") or {}
            cap = audit.get("stake_cap") or {}
            original = float(bet.get("stake_gp") or 0)
            cap_stake = float(cap.get("max_stake_gp") or 0)
            converted = min(original, cap_stake) if cap_stake > 0 else original
            original_total += original
            converted_total += converted
            rows.append(
                {
                    "match_id": bet.get("match_id"),
                    "pick": " ".join(
                        str(part)
                        for part in (bet.get("selection"), bet.get("market"), bet.get("line"))
                        if part not in (None, "")
                    ),
                    "odds": bet.get("odds"),
                    "original_stake_gp": original,
                    "converted_stake_gp": converted,
                    "status": audit.get("status"),
                    "warnings": audit.get("warnings") or [],
                }
            )
        summaries.append(
            {
                "model_account": model.get("model_account"),
                "display_name": model.get("display_name"),
                "rank": model.get("rank"),
                "loan_terms": model.get("loan_terms") or {},
                "bet_count": model.get("bet_count"),
                "allowed": model.get("allowed"),
                "warned": model.get("warned"),
                "rejected": model.get("rejected"),
                "original_stake_total_gp": round(original_total, 2),
                "converted_stake_total_gp": round(converted_total, 2),
                "required_next_action": model.get("required_next_action"),
                "bets": rows,
            }
        )
    return summaries


def strict_decision_count(strict_report: dict[str, Any]) -> int:
    total = 0
    for seat in strict_report.get("seat_summaries") or []:
        if isinstance(seat, dict):
            total += len(seat.get("investments") or [])
    return total


def strict_model_summaries(strict_report: dict[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for seat in strict_report.get("seat_summaries") or []:
        if not isinstance(seat, dict):
            continue
        investments = seat.get("investments") if isinstance(seat.get("investments"), list) else []
        stake_total = sum(float(row.get("stake_gp") or 0) for row in investments if isinstance(row, dict))
        summaries.append(
            {
                "model_account": seat.get("model_account") or seat.get("seat"),
                "display_name": seat.get("seat"),
                "rank": None,
                "loan_terms": {},
                "bet_count": len(investments),
                "allowed": None,
                "warned": None,
                "rejected": None,
                "original_stake_total_gp": round(stake_total, 2),
                "converted_stake_total_gp": round(stake_total, 2),
                "required_next_action": "strict_report_validated_decision",
                "bets": [
                    {
                        "match_id": row.get("match_id"),
                        "pick": " ".join(
                            str(part)
                            for part in (row.get("selection"), row.get("market"), row.get("line"))
                            if part not in (None, "")
                        ),
                        "odds": row.get("odds"),
                        "original_stake_gp": row.get("stake_gp"),
                        "converted_stake_gp": row.get("stake_gp"),
                        "status": row.get("action"),
                        "warnings": [],
                    }
                    for row in investments
                    if isinstance(row, dict)
                ],
            }
        )
    return summaries


def build_bundle(date: str, round_id: str, out_dir: pathlib.Path = OUT_DIR) -> dict[str, Any]:
    daily = read_json(out_dir / f"{date}_{round_id}_daily_sop.json")
    pack = read_json(out_dir / f"{date}_{round_id}_prompt_pack.json")
    shadow = read_json(out_dir / f"{date}_{round_id}_shadow_rerun.json")
    gate_path = out_dir / f"{date}_{round_id}_quality_gate.json"
    quality_gate = read_json(gate_path) if gate_path.exists() else {}
    strict_path = out_dir / f"{date}_{round_id}_god_report_strict.json"
    strict_report = read_json(strict_path) if strict_path.exists() else {}
    rows = audit_rows(shadow)
    converted_total = sum(float(row["converted_stake_gp"] or 0) for row in rows)
    original_total = sum(float(row["original_stake_gp"] or 0) for row in rows)
    strict_decisions = strict_decision_count(strict_report)
    strict_summaries = strict_model_summaries(strict_report)
    decision_source = "shadow_receipts"
    decision_count = shadow.get("total_existing_bets")
    summaries = model_summaries(shadow)
    if not decision_count and strict_decisions:
        decision_source = "strict_god_report"
        decision_count = strict_decisions
        summaries = strict_summaries
        converted_total = sum(float(row.get("converted_stake_total_gp") or 0) for row in summaries)
        original_total = sum(float(row.get("original_stake_total_gp") or 0) for row in summaries)
    no_odds = [match for match in pack.get("matches") or [] if not match.get("market_snapshot")]
    bridge_status = quality_gate.get("status")
    if daily.get("errors"):
        verdict = "NOT_READY"
    else:
        verdict = bridge_status if bridge_status in {"READY", "PARTIAL_NOT_READY", "NOT_READY"} else daily.get("verdict")
    required_coverage = pack.get("required_coverage") or {}
    if quality_gate.get("required_match_ids"):
        required_coverage = {
            "required_match_ids": quality_gate.get("required_match_ids") or [],
            "included_required_match_ids": quality_gate.get("required_match_ids") or [],
            "missing_required_match_ids": [],
            "source": quality_gate.get("required_match_source"),
        }
    return {
        "version": "pred_invest_current_game.v2",
        "generated_at": now_iso(),
        "date": date,
        "round_id": round_id,
        "verdict": verdict,
        "rules": {
            "rule_version": "PRED_INVEST_CREDIT_SURVIVE_V2",
            "forecast_required_for_every_match": True,
            "investment_optional_no_bet_allowed": True,
            "credit_controls_loan": True,
            "settlement_repay_before_ranking": True,
            "stake_caps_by_odds": True,
        },
        "source_paths": {
            "daily_sop": str(out_dir / f"{date}_{round_id}_daily_sop.json"),
            "prompt_pack": str(out_dir / f"{date}_{round_id}_prompt_pack.json"),
            "shadow_rerun": str(out_dir / f"{date}_{round_id}_shadow_rerun.json"),
            "quality_gate": str(gate_path) if gate_path.exists() else None,
            "strict_god_report": str(strict_path) if strict_path.exists() else None,
        },
        "scoreboard": {
            "models": shadow.get("models"),
            "forecast_matches": pack.get("match_count"),
            "matches_with_odds": daily.get("matches_with_odds"),
            "existing_bets": decision_count,
            "existing_decisions": decision_count,
            "existing_bets_source": decision_source,
            "allowed": shadow.get("summary", {}).get("allowed"),
            "warned": shadow.get("summary", {}).get("warned"),
            "rejected": shadow.get("summary", {}).get("rejected"),
            "validated_seats": quality_gate.get("valid_count") if decision_source == "strict_god_report" else None,
            "pending_seats": len(quality_gate.get("needs_rerun") or []) if decision_source == "strict_god_report" else None,
            "models_without_bets": shadow.get("summary", {}).get("models_without_bets") if decision_source == "shadow_receipts" else sorted(set(pred_invest_quality_gate.REQUIRED_SEATS) - set(strict_report.get("valid_seats") or [])),
            "original_stake_total_gp": round(original_total, 2),
            "rule_converted_stake_total_gp": round(converted_total, 2),
            "bridge_valid_seats": quality_gate.get("valid_count"),
            "bridge_required_seats": quality_gate.get("required_seat_count"),
            "bridge_frontend_badge": quality_gate.get("frontend_badge"),
            "bridge_publish_allowed": quality_gate.get("publish_allowed"),
        },
        "matches": pack.get("matches") or [],
        "missing_data": {
            "matches_without_odds": [match.get("match_id") for match in no_odds],
            "missing_models": shadow.get("missing_or_unavailable_models") or [],
            "sop_errors": daily.get("errors") or [],
            "sop_warnings": daily.get("warnings") or [],
            "required_coverage": required_coverage,
            "bridge_needs_rerun": quality_gate.get("needs_rerun") or [],
            "bridge_rerun_queue": quality_gate.get("rerun_queue") or [],
        },
        "quality_gate": {
            "status": quality_gate.get("status"),
            "publish_allowed": quality_gate.get("publish_allowed"),
            "frontend_badge": quality_gate.get("frontend_badge"),
            "valid_seats": quality_gate.get("valid_seats") or [],
            "needs_rerun": quality_gate.get("needs_rerun") or [],
        },
        "strict_match_consensus": strict_report.get("match_consensus") or [],
        "model_summaries": summaries,
        "audit_rows": rows,
        "caveat": (
            f"This bundle uses strict AI Judge output as the current decision source; it remains partial until the hard gate reaches {REQUIRED_SEAT_COUNT}/{REQUIRED_SEAT_COUNT}."
            if decision_source == "strict_god_report"
            else f"This is a V2-rule shadow rerun over accepted run receipts. It does not claim the {REQUIRED_SEAT_COUNT} external models have already reanswered under PRED-INVEST-CREDIT-SURVIVE V2."
        ),
    }


def markdown(bundle: dict[str, Any]) -> str:
    s = bundle["scoreboard"]
    lines = [
        f"# 当前游戏内容 · PRED-INVEST-CREDIT-SURVIVE V2 · {bundle['date']} · {bundle['round_id']}",
        "",
        f"- verdict: **{bundle['verdict']}**",
        f"- 模型：{s['models']}/{REQUIRED_SEAT_COUNT}",
        f"- 必须预测赛事：{s['forecast_matches']} 场",
        f"- 有盘口赛事：{s['matches_with_odds']} 场",
        f"- 已收回结构化投资/观望决策：{s['existing_decisions']} 条",
        f"- 桥接席位门禁：{s.get('bridge_frontend_badge') or '未生成'}；publish_allowed={s.get('bridge_publish_allowed')}",
        (
            f"- strict 门禁：{s.get('validated_seats')}/{REQUIRED_SEAT_COUNT} 席有效，待补 {s.get('pending_seats')} 席。"
            if s.get("existing_bets_source") == "strict_god_report"
            else f"- 新规则审计：{s['allowed']} 可入账 / {s['warned']} 需降额补字段 / {s['rejected']} 贷款冲突"
        ),
        f"- 原始投注额：{gp(s['original_stake_total_gp'])}",
        f"- 按新规则仓位上限转换后：{gp(s['rule_converted_stake_total_gp'])}",
        "",
        "## 规则口径",
        "",
        "- 每场比赛必须给 forecast；可以选择 no-bet。",
        "- 投资不是强制 all-in；只有模型概率高于盘口隐含概率时才下注。",
        "- 贷款由信用分、净资产、未还贷款决定；结算先还息还本，再排名。",
        "- 旧规则下注会被保留为证据，但进入新账本前必须过仓位上限和贷款门禁。",
        "",
        "## 数据缺口",
        "",
    ]
    missing = bundle["missing_data"]
    has_missing = any(
        missing.get(key)
        for key in ("matches_without_odds", "missing_models", "sop_errors", "sop_warnings", "bridge_needs_rerun")
    )
    if has_missing:
        if missing["matches_without_odds"]:
            lines.append("- 缺盘口赛事：" + ", ".join(missing["matches_without_odds"]))
        if missing["missing_models"]:
            lines.append("- 缺模型：" + ", ".join(missing["missing_models"]))
        if missing["sop_errors"]:
            lines.append("- SOP errors：" + "; ".join(missing["sop_errors"]))
        if missing["sop_warnings"]:
            lines.append("- SOP warnings：" + "; ".join(missing["sop_warnings"]))
        if missing.get("bridge_needs_rerun"):
            lines.append("- 桥接待补跑席位：" + ", ".join(missing["bridge_needs_rerun"]))
    else:
        lines.append("- 暂无硬缺口。")
    lines += ["", "## 当前赛事", ""]
    for match in bundle["matches"]:
        markets = match.get("market_snapshot") or []
        first = markets[0] if markets else {}
        first_text = (
            f"{first.get('selection')} {first.get('market')} {first.get('line') or ''} @ {first.get('odds')}"
            if first
            else "无盘口"
        )
        lines.append(f"- {match.get('match_id')} · {match_label(match)} · {len(markets)} 条盘口样本 · {first_text}")
    lines += ["", "## 逐模型新规则投注方式", ""]
    for model in bundle["model_summaries"]:
        terms = model["loan_terms"]
        lines.extend(
            [
                f"### {model['display_name']}",
                "",
                f"- 排名/信用：#{model['rank']} · {terms.get('credit_grade')}/{terms.get('credit_score')}",
                f"- 净资产/可新增贷款：{gp(terms.get('net_worth_gp'))} / {gp(terms.get('available_loan_gp'))}",
                f"- 投注：{model['bet_count']} 笔；原始 {gp(model['original_stake_total_gp'])}，新规转换 {gp(model['converted_stake_total_gp'])}。",
                f"- 处理：{model['required_next_action']}",
            ]
        )
        for bet in model["bets"][:4]:
            warn = "；".join(bet["warnings"]) or "无"
            lines.append(
                f"- {bet['match_id']} · {bet['pick']} @ {bet['odds']}：原始 {gp(bet['original_stake_gp'])}，新规 {gp(bet['converted_stake_gp'])}，{status_label(str(bet['status'] or ''))}；{warn}"
            )
        lines.append("")
    lines.append(f"> 说明：{bundle.get('caveat')}")
    return "\n".join(lines)


def html_page(bundle: dict[str, Any]) -> str:
    s = bundle["scoreboard"]
    cards = [
        ("状态", bundle["verdict"]),
        ("模型", f"{s['models']}/{REQUIRED_SEAT_COUNT}"),
        ("赛事", f"{s['forecast_matches']} 场"),
        ("盘口覆盖", f"{s['matches_with_odds']} 场"),
        ("决策回执", f"{s['existing_decisions']} 条"),
        ("新规转换", gp(s["rule_converted_stake_total_gp"])),
    ]
    card_html = "\n".join(
        f'<section class="card"><span>{h(label)}</span><strong>{h(value)}</strong></section>'
        for label, value in cards
    )
    match_html = "\n".join(
        f"""<tr>
          <td>{h(match.get('match_id'))}</td>
          <td>{h(match_label(match))}</td>
          <td>{h(match.get('kickoff_at'))}</td>
          <td>{len(match.get('market_snapshot') or [])}</td>
        </tr>"""
        for match in bundle["matches"]
    )
    model_html = "\n".join(
        f"""<article class="model">
          <header><b>{h(model['display_name'])}</b><span>#{h(model['rank'])}</span></header>
          <p>信用 {h(model['loan_terms'].get('credit_grade'))}/{h(model['loan_terms'].get('credit_score'))} · 净资产 {h(gp(model['loan_terms'].get('net_worth_gp')))} · 可贷 {h(gp(model['loan_terms'].get('available_loan_gp')))}</p>
          <p>原始投注 {h(gp(model['original_stake_total_gp']))}，按新规则转换 {h(gp(model['converted_stake_total_gp']))}。</p>
          <p class="note">{h(model['required_next_action'])}</p>
        </article>"""
        for model in bundle["model_summaries"]
    )
    audit_html = "\n".join(
        f"""<tr>
          <td>{h(row['display_name'])}</td>
          <td>{h(row['match_id'])}</td>
          <td>{h(row['selection'])} {h(row['market'])} {h(row['line'] or '')}</td>
          <td>{h(row['odds'])}</td>
          <td>{h(gp(row['original_stake_gp']))}</td>
          <td>{h(gp(row['converted_stake_gp']))}</td>
          <td><span class="pill {h(row['status'])}">{h(row['status_label'])}</span></td>
        </tr>"""
        for row in bundle["audit_rows"]
    )
    missing = bundle["missing_data"]
    missing_text = "；".join(
        part
        for part in (
            "缺盘口赛事 " + ", ".join(missing["matches_without_odds"]) if missing["matches_without_odds"] else "",
            "缺模型 " + ", ".join(missing["missing_models"]) if missing["missing_models"] else "",
            "SOP 警告 " + ", ".join(missing["sop_warnings"]) if missing["sop_warnings"] else "",
            "SOP 错误 " + ", ".join(missing["sop_errors"]) if missing["sop_errors"] else "",
        )
        if part
    ) or "暂无硬缺口"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PRED-INVEST-CREDIT-SURVIVE V2 Current Game · {h(bundle['date'])} · {h(bundle['round_id'])}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg:#08111f; --panel:#111c2e; --panel2:#0d1728; --line:#26354d;
      --text:#edf4ff; --muted:#9fb0c9; --green:#20d6a0; --amber:#ffb23e; --red:#ff6d7a; --blue:#61a5ff;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:radial-gradient(circle at top left,#142644 0,#08111f 38%,#060b14 100%); color:var(--text); font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ max-width:1180px; margin:0 auto; padding:32px 20px 56px; }}
    h1 {{ margin:0 0 6px; font-size:28px; letter-spacing:0; }}
    h2 {{ margin:34px 0 12px; font-size:18px; }}
    .sub {{ color:var(--muted); margin:0 0 22px; }}
    .grid {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:12px; }}
    .card,.panel,.model {{ background:linear-gradient(180deg,var(--panel),var(--panel2)); border:1px solid var(--line); border-radius:8px; padding:16px; box-shadow:0 14px 40px rgba(0,0,0,.22); }}
    .card span {{ display:block; color:var(--muted); font-size:12px; margin-bottom:8px; }}
    .card strong {{ display:block; font-size:22px; }}
    .warn {{ border-color:#6f5530; background:#21180d; color:#ffdca0; padding:14px 16px; border-radius:8px; }}
    table {{ width:100%; border-collapse:collapse; overflow:hidden; border:1px solid var(--line); border-radius:8px; }}
    th,td {{ padding:11px 12px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
    th {{ color:var(--muted); font-size:12px; background:#0d1728; }}
    tr:last-child td {{ border-bottom:0; }}
    .models {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; }}
    .model header {{ display:flex; justify-content:space-between; gap:12px; font-size:17px; }}
    .model p {{ color:var(--muted); margin:9px 0 0; }}
    .model .note {{ color:#dbe8ff; }}
    .pill {{ display:inline-flex; padding:3px 8px; border-radius:999px; background:#20304a; color:#cfe0ff; font-size:12px; }}
    .pill.allowed {{ background:rgba(32,214,160,.14); color:var(--green); }}
    .pill.cap_warning {{ background:rgba(255,178,62,.14); color:var(--amber); }}
    .pill.loan_limit_rejected {{ background:rgba(255,109,122,.14); color:var(--red); }}
    @media (max-width:900px) {{ .grid,.models {{ grid-template-columns:1fr 1fr; }} }}
    @media (max-width:620px) {{ main {{ padding:22px 14px 40px; }} .grid,.models {{ grid-template-columns:1fr; }} table {{ font-size:13px; }} th,td {{ padding:9px; }} }}
  </style>
</head>
<body>
  <main>
    <h1>PRED-INVEST-CREDIT-SURVIVE V2 当前游戏内容</h1>
    <p class="sub">{h(bundle['date'])} · {h(bundle['round_id'])} · generated {h(bundle['generated_at'])}</p>
    <div class="grid">{card_html}</div>
    <h2>规则说明</h2>
    <div class="panel">
      <p>每场必须预测，下注可以 no-bet；贷款由信用和净资产控制；每次结算先还息还本，再进入排名。旧规则投注进入新账本前必须通过仓位上限与贷款门禁。</p>
    </div>
    <h2>查漏结论</h2>
    <div class="warn">{h(missing_text)}</div>
    <h2>今日赛事输入</h2>
    <table><thead><tr><th>Match</th><th>对阵</th><th>Kickoff</th><th>盘口样本</th></tr></thead><tbody>{match_html}</tbody></table>
    <h2>逐模型投注方式</h2>
    <div class="models">{model_html}</div>
    <h2>新规则投注审计明细</h2>
    <table><thead><tr><th>模型</th><th>比赛</th><th>选择</th><th>赔率</th><th>原始</th><th>新规</th><th>状态</th></tr></thead><tbody>{audit_html}</tbody></table>
  </main>
</body>
</html>
"""


def write_bundle(bundle: dict[str, Any], out_dir: pathlib.Path = OUT_DIR) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{bundle['date']}_{bundle['round_id']}_current_game"
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    html_path = out_dir / f"{stem}.html"
    json_text = json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
    md_text = markdown(bundle) + "\n"
    html_text = html_page(bundle)
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")
    html_path.write_text(html_text, encoding="utf-8")
    (out_dir / "latest_current_game.json").write_text(json_text, encoding="utf-8")
    (out_dir / "latest_current_game.md").write_text(md_text, encoding="utf-8")
    (out_dir / "latest_current_game.html").write_text(html_text, encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "html": str(html_path)}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build PRED-INVEST current game client bundle")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    bundle = build_bundle(args.date, args.round_id)
    paths = write_bundle(bundle) if args.write else {}
    s = bundle["scoreboard"]
    ok = (
        bundle["verdict"] == "READY"
        and s["models"] == 12
        and s["forecast_matches"] > 0
        and s["matches_with_odds"] == s["forecast_matches"]
        and s["existing_bets"] > 0
        and not bundle["missing_data"]["missing_models"]
        and not bundle["missing_data"]["sop_errors"]
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "verdict": bundle["verdict"],
                "scoreboard": s,
                "missing_data": bundle["missing_data"],
                "paths": paths,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
