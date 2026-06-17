#!/usr/bin/env python3
"""Generate the strict PRED-INVEST god-view report from the publish gate.

The report is intentionally downstream of the quality gate. It must never turn
partial bridge recovery into a full report, and it filters every model output
to the frozen required-match contract for the round.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import audit_pred_invest_bridge_outputs as bridge_audit
import pred_invest_quality_gate


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
REQUIRED_SEATS = pred_invest_quality_gate.REQUIRED_SEATS
REQUIRED_SEAT_COUNT = len(REQUIRED_SEATS)


def _filter_match_rows(rows: Any, required_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict) and str(row.get("match_id")) in required_ids]


def _loan_text(value: Any) -> str:
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _num(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"none", "null", "nan", "-", "--"}:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        return float(match.group(0))
    except Exception:
        return None


def _prob(value: Any) -> float | None:
    number = _num(value)
    if number is None:
        return None
    if 0 <= number <= 1:
        return number
    if 1 < number <= 100:
        return number / 100
    return None


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _selection_side(selection: Any, match: dict[str, Any] | None) -> str | None:
    text = _norm(selection)
    if not text or text in {"none", "null", "-", "--"}:
        return None
    if text in {"home", "主", "主队", "主胜"}:
        return "home"
    if text in {"away", "客", "客队", "客胜"}:
        return "away"
    if text in {"draw", "tie", "平", "平局"}:
        return "draw"
    if not match:
        return None
    home = _norm(match.get("home_team"))
    away = _norm(match.get("away_team"))
    if home and (text == home or home in text or text in home):
        return "home"
    if away and (text == away or away in text or text in away):
        return "away"
    if "draw" in text or "平" in text:
        return "draw"
    return None


def _line_equal(left: Any, right: Any) -> bool:
    left_num = _num(left)
    right_num = _num(right)
    if left_num is not None and right_num is not None:
        return abs(left_num - right_num) < 0.001
    left_text = _norm(left)
    right_text = _norm(right)
    return not left_text or not right_text or left_text == right_text or left_text in {"none", "null", "-", "--"}


def _forecast_lean_side(forecast: dict[str, Any] | None, match: dict[str, Any] | None) -> str | None:
    if not forecast:
        return None
    for key in ("p", "prediction", "pick", "winner"):
        side = _selection_side(forecast.get(key), match)
        if side:
            return side
    lean_text = " ".join(
        str(forecast.get(key) or "")
        for key in ("p", "prediction", "pick", "winner", "edge_assessment")
    )
    side = _selection_side(lean_text, match)
    if side:
        return side
    probabilities = {
        "home": _prob(forecast.get("home_win_prob")),
        "draw": _prob(forecast.get("draw_prob")),
        "away": _prob(forecast.get("away_win_prob")),
    }
    probabilities = {key: value for key, value in probabilities.items() if value is not None}
    if probabilities:
        return max(probabilities.items(), key=lambda item: item[1])[0]
    return None


def _market_odds(inv: dict[str, Any], match: dict[str, Any] | None, target_side: str | None = None) -> tuple[float | None, str]:
    direct = _num(inv.get("odds"))
    if direct and direct > 1:
        return direct, "investment.odds"
    if not match:
        return None, "missing_match_market"
    selection_side = _selection_side(inv.get("selection"), match) or target_side
    selection_text = _norm(inv.get("selection"))
    market_text = _norm(inv.get("market"))
    for row in match.get("market_snapshot") or []:
        if not isinstance(row, dict):
            continue
        row_selection = _norm(row.get("selection"))
        row_side = _selection_side(row.get("selection"), match)
        row_market = _norm(row.get("market"))
        if market_text and row_market and market_text not in {"none", "null"} and row_market != market_text:
            continue
        if selection_side and row_side and selection_side != row_side:
            continue
        if selection_text and row_selection and selection_text not in {"none", "null"} and row_selection != selection_text and not selection_side:
            continue
        if not _line_equal(inv.get("line"), row.get("line")):
            continue
        odds = _num(row.get("odds"))
        if odds and odds > 1:
            return odds, "market_snapshot"
    return None, "missing_market_odds"


def _forecast_for_match(seat: dict[str, Any], match_id: str) -> dict[str, Any] | None:
    for row in seat.get("forecasts") or []:
        if isinstance(row, dict) and str(row.get("match_id")) == str(match_id):
            return row
    return None


def _forecast_probability(
    forecast: dict[str, Any] | None,
    inv: dict[str, Any],
    match: dict[str, Any] | None,
    target_side: str | None = None,
) -> tuple[float | None, str]:
    direct = _prob(inv.get("model_prob"))
    if direct and direct > 0:
        return direct, "investment.model_prob"
    if not forecast:
        return None, "missing_forecast"
    side = _selection_side(inv.get("selection"), match) or target_side or _forecast_lean_side(forecast, match)
    if side == "home":
        value = _prob(forecast.get("home_win_prob"))
        if value is not None:
            return value, "forecast.home_win_prob"
    if side == "draw":
        value = _prob(forecast.get("draw_prob"))
        if value is not None:
            return value, "forecast.draw_prob"
    if side == "away":
        value = _prob(forecast.get("away_win_prob"))
        if value is not None:
            return value, "forecast.away_win_prob"

    lean_text = " ".join(
        str(forecast.get(key) or "")
        for key in ("p", "prediction", "pick", "score", "edge_assessment")
    )
    lean_side = _selection_side(lean_text, match)
    if side and lean_side == side:
        score_prob = _prob(forecast.get("score"))
        if score_prob is not None:
            return score_prob, "forecast.score_probability_proxy"
        confidence = _prob(forecast.get("confidence"))
        if confidence is not None:
            return confidence, "forecast.confidence_proxy"

    confidence = _prob(forecast.get("confidence"))
    if confidence is not None and str(inv.get("action") or "").lower() == "bet":
        return confidence, "forecast.confidence_fallback_proxy"
    if confidence is not None and side:
        return confidence, "forecast.no_bet_confidence_proxy"
    return None, "missing_model_probability"


def _estimated_ev(model_prob: float | None, odds: float | None, explicit_ev: Any) -> tuple[float | None, str]:
    explicit = _num(explicit_ev)
    if explicit is not None and explicit != 0:
        return round(explicit, 4), "investment.estimated_ev"
    if model_prob is None or odds is None or odds <= 1:
        return None, "not_computable"
    return round(model_prob * odds - 1, 4), "model_prob_times_odds_minus_one"


def _load_prompt_matches(date: str, round_id: str) -> dict[str, dict[str, Any]]:
    path = OUT_DIR / f"{date}_{round_id}_prompt_pack.json"
    if not path.exists():
        return {}
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {
        str(match.get("match_id")): match
        for match in pack.get("matches") or []
        if isinstance(match, dict) and match.get("match_id")
    }


def _ev_coverage(action: str, model_prob: float | None, odds: float | None, model_source: str) -> str:
    if action != "bet" and (odds is None or odds <= 1):
        return "not_applicable_no_bet"
    if model_prob is None:
        return "data_gap"
    if model_source == "investment.model_prob":
        return "complete_explicit"
    if "proxy" in model_source:
        return "complete_proxy_inferred"
    return "complete_inferred"


def _ev_analysis(valid: list[dict[str, Any]], matches: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    coverage_counts: dict[str, int] = defaultdict(int)
    for seat in valid:
        for inv in seat.get("investments") or []:
            if not isinstance(inv, dict):
                continue
            match_id = str(inv.get("match_id") or "")
            action = str(inv.get("action") or "").lower()
            match = matches.get(match_id)
            forecast = _forecast_for_match(seat, match_id)
            target_side = _selection_side(inv.get("selection"), match) or _forecast_lean_side(forecast, match)
            odds, odds_source = _market_odds(inv, match, target_side)
            market_prob = _prob(inv.get("market_implied_prob"))
            market_source = "investment.market_implied_prob" if market_prob and market_prob > 0 else ""
            if (market_prob is None or market_prob <= 0) and odds and odds > 1:
                market_prob = round(1 / odds, 4)
                market_source = f"{odds_source}:1/odds"
            model_prob, model_source = _forecast_probability(forecast, inv, match, target_side)
            ev, ev_source = _estimated_ev(model_prob, odds, inv.get("estimated_ev"))
            coverage = _ev_coverage(action, model_prob, odds, model_source)
            coverage_counts[coverage] += 1
            rows.append(
                {
                    "seat": seat.get("seat"),
                    "match_id": match_id,
                    "action": action or "no_bet",
                    "market": inv.get("market"),
                    "selection": inv.get("selection"),
                    "probability_target": target_side,
                    "line": inv.get("line"),
                    "odds": odds,
                    "model_prob": round(model_prob, 4) if model_prob is not None else None,
                    "market_implied_prob": round(market_prob, 4) if market_prob is not None else None,
                    "estimated_ev": ev,
                    "coverage": coverage,
                    "model_prob_source": model_source,
                    "market_prob_source": market_source or "not_available",
                    "ev_source": ev_source,
                    "note": inv.get("reason") or "",
                }
            )
    actionable_rows = [row for row in rows if row["coverage"] != "not_applicable_no_bet"]
    data_gaps = [row for row in rows if row["coverage"] == "data_gap"]
    return {
        "version": "ev_analysis.v2",
        "method": "explicit model_prob first; otherwise infer from forecast win/draw/away probability or confidence proxy. For no_bet without selection, compare the model forecast lean against market odds as opportunity-cost EV. Market implied probability is 1/decimal odds.",
        "rows": rows,
        "actionable_rows": actionable_rows,
        "coverage_counts": dict(sorted(coverage_counts.items())),
        "data_gap_rows": data_gaps,
    }


def _seat_summaries(date: str, round_id: str, run_ids: list[str], required_ids: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    responses, errors = bridge_audit._latest_responses(run_ids)
    bridge_audit._append_page_salvage_responses(responses, date, round_id)
    required = set(required_ids)
    valid: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    for seat in REQUIRED_SEATS:
        candidate, issues, forecast_ids, investment_ids = bridge_audit._select_response_candidate(responses.get(seat, []), required_ids, seat)
        if issues:
            invalid.append(
                {
                    "seat": seat,
                    "issues": issues,
                    "run_id": candidate.get("run_id") if candidate else None,
                    "response_chars": candidate.get("response_chars") if candidate else 0,
                    "last_errors": errors.get(seat, [])[-3:],
                }
            )
            continue
        parsed = bridge_audit._extract_receipt_object(candidate.get("text") or "", required_ids) if candidate else None
        if not isinstance(parsed, dict):
            invalid.append({"seat": seat, "issues": ["response_not_parseable_after_gate"], "run_id": candidate.get("run_id") if candidate else None})
            continue
        valid.append(
            {
                "seat": seat,
                "model_account": parsed.get("model_account"),
                "run_id": candidate.get("run_id") if candidate else None,
                "one_sentence_strategy": parsed.get("one_sentence_strategy"),
                "loan_decision": parsed.get("loan_decision"),
                "risk_notes": parsed.get("risk_notes"),
                "forecasts": _filter_match_rows(parsed.get("forecasts"), required),
                "investments": _filter_match_rows(parsed.get("investments"), required),
                "forecast_match_ids": sorted(forecast_ids & required),
                "investment_match_ids": sorted(investment_ids & required),
            }
        )
    return valid, invalid


def _match_consensus(valid: list[dict[str, Any]], required_ids: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for match_id in required_ids:
        bets: list[dict[str, Any]] = []
        no_bet: list[str] = []
        selection_counts: dict[str, int] = defaultdict(int)
        total_stake = 0.0
        for seat in valid:
            for inv in seat.get("investments") or []:
                if inv.get("match_id") != match_id:
                    continue
                action = str(inv.get("action") or "").lower()
                stake = float(inv.get("stake_gp") or 0)
                if action == "bet" and stake > 0:
                    selection = " ".join(str(part) for part in (inv.get("market"), inv.get("selection"), inv.get("line")) if part not in (None, ""))
                    selection_counts[selection] += 1
                    total_stake += stake
                    bets.append(
                        {
                            "seat": seat["seat"],
                            "selection": selection,
                            "odds": inv.get("odds"),
                            "stake_gp": stake,
                            "loan_used_gp": inv.get("loan_used_gp"),
                            "reason": inv.get("reason"),
                        }
                    )
                else:
                    no_bet.append(seat["seat"])
        rows.append(
            {
                "match_id": match_id,
                "bet_count": len(bets),
                "no_bet_count": len(no_bet),
                "total_stake_gp": round(total_stake, 2),
                "top_selection": max(selection_counts.items(), key=lambda item: item[1])[0] if selection_counts else None,
                "bets": bets,
                "no_bet_seats": no_bet,
            }
        )
    return rows


def build_report(date: str, round_id: str, run_ids: list[str]) -> dict[str, Any]:
    gate = pred_invest_quality_gate.build_gate(date, round_id, run_ids)
    required_ids = gate.get("required_match_ids") or []
    valid, invalid = _seat_summaries(date, round_id, run_ids, required_ids)
    matches = _load_prompt_matches(date, round_id)
    ev = _ev_analysis(valid, matches)
    return {
        "version": "pred_invest_strict_god_report.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date,
        "round_id": round_id,
        "status": gate.get("status"),
        "publish_allowed": gate.get("publish_allowed"),
        "frontend_badge": gate.get("frontend_badge"),
        "valid_count": len(valid),
        "required_seat_count": len(REQUIRED_SEATS),
        "valid_seats": [row["seat"] for row in valid],
        "needs_rerun": gate.get("needs_rerun") or [],
        "rerun_queue": gate.get("rerun_queue") or [],
        "required_matches": required_ids,
        "required_match_source": gate.get("required_match_source"),
        "seat_summaries": valid,
        "invalid_details": invalid,
        "match_consensus": _match_consensus(valid, required_ids),
        "ev_analysis": ev,
        "hard_gate_notice": f"不到 {REQUIRED_SEAT_COUNT}/{REQUIRED_SEAT_COUNT} publish_allowed=true，不允许前端或日报显示为全量完成报告。",
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# AI 世界杯预测池上帝报告 · {report['round_id']} 严格审计版",
        "",
        f"- 日期：{report['date']}",
        f"- 状态：{report['status']}",
        f"- 发布允许：{report['publish_allowed']}",
        f"- 有效席位：{report['valid_count']}/{report['required_seat_count']}（{', '.join(report['valid_seats']) or '-'}）",
        f"- 待处理席位：{', '.join(report['needs_rerun']) or 'none'}",
        f"- 门禁提示：{report['hard_gate_notice']}",
        "",
        "## 一句话结论",
        "",
    ]
    if report["publish_allowed"]:
        lines.append(f"本轮 {report['required_seat_count']} 席全部通过硬门禁，可作为完整上帝视角报告发布。")
    else:
        lines.append(
            f"本轮已补回到 {report['valid_count']}/{report['required_seat_count']}；"
            f"仍因 {', '.join(report['needs_rerun']) or '未知席位'} 未过门禁，报告只能作为部分上帝视角。"
        )
    lines += ["", "## 逐席投注摘要", ""]
    for seat in report["seat_summaries"]:
        lines += [
            f"### {seat['seat']}",
            f"- 策略：{seat.get('one_sentence_strategy') or '-'}",
            f"- 贷款：{_loan_text(seat.get('loan_decision'))}",
            f"- 风险：{seat.get('risk_notes') or '-'}",
        ]
        for inv in seat.get("investments") or []:
            lines.append(
                "- {match_id} · {action} · {market} {selection} {line} · @{odds} · stake {stake}GP · loan {loan}GP".format(
                    match_id=inv.get("match_id"),
                    action=inv.get("action"),
                    market=inv.get("market"),
                    selection=inv.get("selection"),
                    line=inv.get("line"),
                    odds=inv.get("odds"),
                    stake=inv.get("stake_gp"),
                    loan=inv.get("loan_used_gp"),
                )
            )
        lines.append("")
    ev = report.get("ev_analysis") if isinstance(report.get("ev_analysis"), dict) else {}
    lines += [
        "## EV 分析：模型概率 vs 市场隐含概率",
        "",
        f"- 方法：{ev.get('method') or '-'}",
        f"- 覆盖：{json.dumps(ev.get('coverage_counts') or {}, ensure_ascii=False)}",
        f"- 真正数据缺口：{len(ev.get('data_gap_rows') or [])}",
        "",
        "| Seat | Match | Action | Pick | Odds | Model P | Market P | EV | Coverage | Source |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in ev.get("actionable_rows") or []:
        pick = " ".join(str(part) for part in (row.get("market"), row.get("selection"), row.get("line")) if part not in (None, "", "none"))
        if not pick and row.get("probability_target"):
            pick = f"forecast:{row.get('probability_target')}"
        model_prob = "" if row.get("model_prob") is None else f"{row['model_prob']:.3f}"
        market_prob = "" if row.get("market_implied_prob") is None else f"{row['market_implied_prob']:.3f}"
        estimated_ev = "" if row.get("estimated_ev") is None else f"{row['estimated_ev']:.3f}"
        odds = "" if row.get("odds") is None else f"{row['odds']:.2f}"
        lines.append(
            "| {seat} | {match} | {action} | {pick} | {odds} | {mp} | {ip} | {evv} | {coverage} | {source} |".format(
                seat=row.get("seat"),
                match=row.get("match_id"),
                action=row.get("action"),
                pick=pick or "-",
                odds=odds,
                mp=model_prob,
                ip=market_prob,
                evv=estimated_ev,
                coverage=row.get("coverage"),
                source=row.get("model_prob_source"),
            )
        )
    lines.append("")
    lines += ["## 赛事共识", ""]
    for row in report["match_consensus"]:
        lines += [
            f"### {row['match_id']}",
            f"- 投注席位：{row['bet_count']}；观望席位：{row['no_bet_count']}；总下注：{row['total_stake_gp']}GP",
            f"- 主方向：{row.get('top_selection') or '无集中下注'}",
        ]
        for bet in row["bets"]:
            lines.append(f"- {bet['seat']}: {bet['selection']} @{bet.get('odds')} · {bet['stake_gp']}GP")
        lines.append("")
    lines += ["## 未通过席位", ""]
    for row in report["invalid_details"]:
        lines.append(f"- {row['seat']}: {', '.join(row.get('issues') or []) or 'unknown'}")
    return "\n".join(lines) + "\n"


def write_report(report: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{report['date']}_{report['round_id']}_god_report_strict"
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    (OUT_DIR / "latest_god_report_strict.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_god_report_strict.md").write_text(markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--runs", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    run_ids = [item.strip() for item in args.runs.split(",") if item.strip()]
    report = build_report(args.date, args.round_id, run_ids)
    if args.write:
        report["paths"] = write_report(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("publish_allowed") else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
