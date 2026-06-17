#!/usr/bin/env python3
"""Generate Observer Ledger reports for the AI World Cup pool.

This is a deterministic commentary layer. It consumes structured pool data and
never invents match scores, odds, injuries, or model reasoning.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from typing import Any

from pred_invest_seat_registry import REQUIRED_SEAT_COUNT

BASE_URL = "https://pool-app-one.vercel.app"
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "observer_ledgers"
PRED_DIR = ROOT / "data" / "pool" / "pred_invest"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} while fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while fetching {url}: {exc}") from exc
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from {url}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected object JSON from {url}")
    return data


def api_url(base_url: str, path: str, **query: str) -> str:
    encoded = urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    return f"{base_url.rstrip('/')}{path}" + (f"?{encoded}" if encoded else "")


def load_json_safe(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_local_context(date: str, round_id: str, reason: str) -> dict[str, Any]:
    current = load_json_safe(PRED_DIR / f"{date}_{round_id}_current_game.json") or load_json_safe(PRED_DIR / "latest_current_game.json")
    daily = load_json_safe(PRED_DIR / f"{date}_{round_id}_daily_sop.json") or load_json_safe(PRED_DIR / "latest_daily_sop.json")
    strict = load_json_safe(PRED_DIR / f"{date}_{round_id}_god_report_strict.json") or load_json_safe(PRED_DIR / "latest_god_report_strict.json")
    quality = load_json_safe(PRED_DIR / f"{date}_{round_id}_quality_gate.json") or load_json_safe(PRED_DIR / "latest_quality_gate.json")
    current.setdefault("quality_gate", quality)
    return {
        "runtime": current,
        "daily_report": daily,
        "seat_archives": {"seats": []},
        "settlement": {},
        "receipts": {},
        "strict_report": strict,
        "context_source": "local_artifact_fallback",
        "context_warning": reason,
    }


def load_context(base_url: str, date: str, round_id: str) -> dict[str, Any]:
    try:
        runtime = fetch_json(api_url(base_url, "/api/pool/runtime-summary", date=date, round_id=round_id))
        daily = fetch_json(api_url(base_url, f"/api/pool/daily-reports/{date}/{round_id}"))
        archives = fetch_json(api_url(base_url, f"/api/pool/seat-archives/{round_id}"))
        settlements = fetch_json(api_url(base_url, f"/api/pool/settlements/{round_id}"))
        receipts = fetch_json(api_url(base_url, f"/api/pool/bet-receipts/{round_id}"))
    except RuntimeError as exc:
        return load_local_context(date, round_id, str(exc))
    return {
        "runtime": runtime,
        "daily_report": daily,
        "seat_archives": archives,
        "settlement": settlements,
        "receipts": receipts,
        "context_source": "api",
        "context_warning": None,
    }


def n(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(number) or math.isinf(number):
        return default
    return number


def gp(value: Any) -> str:
    number = n(value)
    if abs(number - round(number)) < 0.001:
        return f"{int(round(number)):,} GP"
    return f"{number:,.1f} GP"


def pct(value: Any) -> str:
    return f"{n(value) * 100:.1f}%"


FIELD_TRANSLATIONS = {
    "run_id": "本轮策略引用了运行编号字段，外部战报改按实际下注和结算结果解读。",
    "market": "该席位主要围绕盘口市场做选择，外部战报以实际下注结果为准。",
    "selection": "该席位给出了投注方向，外部战报以结构化投注单为准。",
    "target_top3_daily_bonus": "目标是冲击日榜前三奖励，接受一定仓位波动。",
    "target_top3_with_concentrated_bets_and_loan": "通过集中下注和贷款杠杆冲击前三，但回撤压力较高。",
    "concentrate_stakes_on_high_odds_handicap_selections_to_maximize_single_day_payout_and_climb_rankings_for_daily_bonus": "把仓位集中在高赔率让球盘，试图用单日收益冲击排名奖励。",
}

TEAM_TRANSLATIONS = {
    "Bosnia & Herzegovina": "波黑",
    "Paraguay": "巴拉圭",
    "Canada": "加拿大",
    "USA": "美国",
    "Haiti": "海地",
    "Scotland": "苏格兰",
}

MARKET_TRANSLATIONS = {
    "handicap": "让球",
    "h2h": "胜平负",
    "moneyline": "胜平负",
    "totals": "总进球",
    "total": "总进球",
}

MATCH_ID_LABELS = {
    "WC-A1": "墨西哥 vs 南非",
    "WC-A2": "韩国 vs 捷克",
    "WC-B1": "加拿大 vs 波黑",
    "WC-D1": "美国 vs 巴拉圭",
}


def is_internal_fragment(value: str) -> bool:
    if not value:
        return True
    lowered = value.strip().lower()
    if lowered in FIELD_TRANSLATIONS:
        return True
    if lowered in {"none", "null", "n/a", "na", "—", "-"}:
        return True
    if len(lowered) <= 28 and lowered.replace("_", "").replace("-", "").isalnum() and ("_" in lowered or lowered in {"market", "runid"}):
        return True
    tokens = lowered.split()
    snake_tokens = [token for token in tokens if "_" in token and token.replace("_", "").replace("-", "").isalnum()]
    return bool(tokens) and len(snake_tokens) / max(len(tokens), 1) >= 0.5


def clean_text(text: Any, fallback: str, limit: int = 130) -> str:
    if text is None:
        return fallback
    value = " ".join(str(text).replace("\n", " ").split()).strip()
    if not value:
        return fallback
    lowered = value.lower()
    for key, translated in FIELD_TRANSLATIONS.items():
        if lowered == key:
            return compact(translated, limit)
        value = value.replace(key, translated)
        value = value.replace(key.upper(), translated)
    if is_internal_fragment(value):
        return fallback
    return compact(value, limit)


def cn_team(value: Any) -> str:
    text = str(value or "").strip()
    return TEAM_TRANSLATIONS.get(text, text)


def cn_market(value: Any) -> str:
    text = str(value or "").strip()
    return MARKET_TRANSLATIONS.get(text.lower(), text or "盘口")


def compact(text: Any, limit: int = 130) -> str:
    if text is None:
        return ""
    value = " ".join(str(text).replace("\n", " ").split())
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 1)].rstrip() + "…"


def join_note_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "；".join(str(item) for item in value if item not in (None, ""))
    return str(value)


def seat_key(row: dict[str, Any]) -> str:
    return str(row.get("model_account") or row.get("seat_id") or "").lower()


def model_name(seat: dict[str, Any], account: str) -> str:
    return str(seat.get("display_name") or account or "unknown")


def match_map(runtime: dict[str, Any]) -> dict[str, dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for key in ("matches", "settled_matches", "future_matches"):
        value = runtime.get(key)
        if isinstance(value, list):
            matches.extend([m for m in value if isinstance(m, dict)])
    mapped: dict[str, dict[str, Any]] = {}
    for match in matches:
        match_id = match.get("match_id") or match.get("id")
        if match_id:
            mapped[str(match_id)] = match
    return mapped


def load_local_current_game(date: str, round_id: str) -> dict[str, Any]:
    path = ROOT / "data" / "pool" / "pred_invest" / f"{date}_{round_id}_current_game.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def load_local_strict_god_report(date: str, round_id: str) -> dict[str, Any]:
    path = ROOT / "data" / "pool" / "pred_invest" / f"{date}_{round_id}_god_report_strict.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def account_map(current_game: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for row in current_game.get("model_summaries") or []:
        if not isinstance(row, dict):
            continue
        account = str(row.get("model_account") or "").lower()
        if account:
            mapped[account] = row
    return mapped


def fallback_archives_from_strict(strict: dict[str, Any], current_game: dict[str, Any]) -> list[dict[str, Any]]:
    accounts = account_map(current_game)
    rows: list[dict[str, Any]] = []
    for summary in strict.get("seat_summaries") or []:
        if not isinstance(summary, dict):
            continue
        seat = str(summary.get("seat") or "").lower()
        if not seat:
            continue
        account = accounts.get(seat, {})
        loan_terms = account.get("loan_terms") if isinstance(account.get("loan_terms"), dict) else {}
        rows.append({
            "model_account": seat,
            "seat_id": seat,
            "display_name": account.get("display_name") or seat,
            "rank": account.get("rank"),
            "balance_gp": loan_terms.get("net_worth_gp"),
            "loan_gp": loan_terms.get("outstanding_loan_gp"),
            "bet_count": len(summary.get("investments") or []),
            "total_stake_gp": sum(n(row.get("stake_gp")) for row in summary.get("investments") or [] if isinstance(row, dict)),
            "potential_profit_gp": sum(
                n(row.get("stake_gp")) * max(n(row.get("odds")) - 1, 0)
                for row in summary.get("investments") or []
                if isinstance(row, dict) and row.get("action") == "bet"
            ),
            "analysis_summary": summary.get("strategy") or summary.get("one_sentence_strategy"),
            "risk_summary": join_note_text(summary.get("risk_notes")),
            "one_sentence_strategy": summary.get("one_sentence_strategy"),
            "risk_notes": summary.get("risk_notes"),
            "decision_record": {
                "stages": {
                    "pre_match_thinking": {"summary": summary.get("strategy")},
                    "bet_lock": {"summary": f"{len(summary.get('investments') or [])} 条投资/观望决策来自 strict god report。"},
                }
            },
        })
    return rows


def fallback_groups_from_strict(strict: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for summary in strict.get("seat_summaries") or []:
        if not isinstance(summary, dict):
            continue
        seat = str(summary.get("seat") or "").lower()
        if not seat:
            continue
        for row in summary.get("investments") or []:
            if not isinstance(row, dict):
                continue
            normalized = dict(row)
            normalized["model_account"] = seat
            normalized["seat_id"] = seat
            normalized["stake_gp"] = n(row.get("stake_gp"))
            normalized["profit_gp"] = 0
            normalized["payout_gp"] = 0
            normalized["status"] = "pending"
            groups[seat].append(normalized)
    return groups


def merge_local_match_map(mapped: dict[str, dict[str, Any]], current_game: dict[str, Any]) -> dict[str, dict[str, Any]]:
    for match in current_game.get("matches") or []:
        if not isinstance(match, dict):
            continue
        match_id = match.get("match_id") or match.get("id")
        if match_id:
            mapped.setdefault(str(match_id), match)
    return mapped


def audit_bet_groups(current_game: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in current_game.get("audit_rows") or []:
        if not isinstance(row, dict):
            continue
        account = str(row.get("model_account") or row.get("seat_id") or "").lower()
        if not account:
            continue
        normalized = dict(row)
        normalized["stake_gp"] = n(row.get("converted_stake_gp") or row.get("stake_gp") or row.get("original_stake_gp"))
        normalized["profit_gp"] = 0
        normalized["payout_gp"] = 0
        normalized["status"] = "pending"
        groups[account].append(normalized)
    return groups


def match_label(match_id: str, matches: dict[str, dict[str, Any]]) -> str:
    if match_id in MATCH_ID_LABELS:
        return MATCH_ID_LABELS[match_id]
    match = matches.get(match_id) or {}
    home = match.get("home_team") or match.get("home") or ""
    away = match.get("away_team") or match.get("away") or ""
    if home and away:
        return f"{cn_team(home)} vs {cn_team(away)}"
    return match_id


def settlement_groups(settlement: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in settlement.get("settlements") or []:
        if isinstance(row, dict):
            groups[str(row.get("model_account") or row.get("seat_id") or "").lower()].append(row)
    return groups


def settlement_by_match(settlement: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in settlement.get("settlements") or []:
        if isinstance(row, dict) and row.get("match_id"):
            groups[str(row["match_id"])].append(row)
    return groups


def grade_for(profit: float, roi: float, settled: bool) -> str:
    if not settled:
        return "待赛"
    if profit >= 500:
        return "A"
    if profit >= 100:
        return "B+"
    if profit >= 0:
        return "B"
    if profit > -250 or roi > -0.25:
        return "C"
    return "D"


def risk_label(stake: float, balance: float, loan: float, bet_count: int) -> str:
    if stake <= 0 or bet_count <= 0:
        return "零注观望"
    exposure = stake / max(balance + loan, 1)
    if loan > 0 and exposure >= 0.75:
        return "高杠杆冲榜"
    if bet_count >= 4:
        return "分散高频"
    if exposure <= 0.25:
        return "低仓位防守"
    return "中等仓位"


def top_market(settlements: list[dict[str, Any]]) -> str:
    actual_settlements = [row for row in settlements if is_actual_bet(row)]
    if not actual_settlements:
        if settlements:
            return "全场观望"
        return "无可结算下注"
    first = actual_settlements[0]
    selection = cn_team(first.get("selection")) or "投注方向"
    market = cn_market(first.get("market"))
    line = first.get("line")
    if isinstance(line, (int, float)):
        line_text = f" {line:+g}" if market == "让球" else f" {line:g}"
    else:
        line_text = f" {line}" if line not in (None, "") else ""
    odds = first.get("odds")
    odds_text = f" @ {odds:g}" if isinstance(odds, (int, float)) else ""
    return f"{selection} {market}{line_text}{odds_text}"


def build_seat_commentary(
    seat: dict[str, Any],
    account: str,
    settlements: list[dict[str, Any]],
    matches: dict[str, dict[str, Any]],
    phase: str,
) -> dict[str, Any]:
    display = model_name(seat, account)
    stake = sum(n(row.get("stake_gp")) for row in settlements) or n(seat.get("total_stake_gp"))
    payout = sum(n(row.get("payout_gp")) for row in settlements)
    profit = sum(n(row.get("profit_gp")) for row in settlements)
    wins = sum(1 for row in settlements if row.get("status") == "win")
    losses = sum(1 for row in settlements if row.get("status") == "lose")
    pushes = sum(1 for row in settlements if row.get("status") == "push")
    decision_count = len(settlements) or int(n(seat.get("bet_count")))
    bet_count = sum(1 for row in settlements if is_actual_bet(row))
    if not settlements and n(seat.get("total_stake_gp")) > 0:
        bet_count = int(n(seat.get("bet_count")))
    loan = n(seat.get("loan_gp"))
    balance = n(seat.get("balance_gp"))
    roi = profit / stake if stake else 0.0
    settled = phase == "post" and bool(settlements)
    grade = grade_for(profit, roi, settled)
    risk = risk_label(stake, balance, loan, bet_count)
    match_counter = Counter(str(row.get("match_id")) for row in settlements if row.get("match_id"))
    main_match_id = match_counter.most_common(1)[0][0] if match_counter else ""
    main_match = match_label(main_match_id, matches) if main_match_id else "本轮组合"
    decision = ((seat.get("decision_record") or {}).get("stages") or {}).get("pre_match_thinking") or {}
    primary_position = top_market(settlements)
    summary_fallback = (
        f"{display}本轮{decision_count}条决策，其中下注{bet_count}笔，主线是{primary_position}，整体属于{risk}。"
    )
    risk_fallback = f"主要风险是{main_match}结果偏离共识，贷款{gp(loan)}会放大赛后净值压力。"
    source_summary = clean_text(decision.get("summary") or seat.get("analysis_summary"), summary_fallback, 180)
    source_risk = clean_text(
        seat.get("risk_summary") or ((seat.get("decision_record") or {}).get("stages") or {}).get("behavior_profile", {}).get("risk_summary"),
        risk_fallback,
        180,
    )
    strategy_summary = summary_fallback
    risk_summary = risk_fallback

    if settled:
        data_view = f"{display} 本轮 {bet_count} 笔下注，投入 {gp(stake)}，净结果 {gp(profit)}，ROI {pct(roi)}，命中 {wins}/{max(bet_count, 1)}。"
        football_view = f"足球面看，核心暴露在 {main_match}；最终命中 {wins} 单、失手 {losses} 单，盘口兑现决定当日净值。"
        pro_view = f"职业下注视角：{risk}；贷款 {gp(loan)}，赛后应先扣利息和还本，再看排名净值。"
        one_line = f"{display}：{grade}，{gp(profit)}；{clean_text(strategy_summary, summary_fallback, 76)}"
    else:
        data_view = f"{display} 本轮给出 {decision_count} 条决策，其中下注 {bet_count} 笔，计划投入 {gp(stake)}，潜在利润约 {gp(seat.get('potential_profit_gp'))}。"
        football_view = f"足球面看，主要押注 {main_match}；尚未结算，暂不写胜负判断。"
        pro_view = f"职业下注视角：{risk}；贷款 {gp(loan)}，需在结算后先还债再计排名。"
        one_line = f"{display}：待赛；{clean_text(strategy_summary, summary_fallback, 76)}"

    return {
        "model_account": account,
        "display_name": display,
        "rank": seat.get("rank"),
        "balance_gp": balance,
        "loan_gp": loan,
        "bet_count": bet_count,
        "decision_count": decision_count,
        "stake_gp": stake,
        "payout_gp": payout,
        "profit_gp": profit,
        "roi": roi,
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "grade": grade,
        "risk_label": risk,
        "main_match_id": main_match_id,
        "main_match": main_match,
        "primary_position": primary_position,
        "one_line": one_line,
        "perspectives": {
            "data_analyst": data_view,
            "football_expert": football_view,
            "pro_bettor": pro_view,
        },
        "strategy_excerpt": strategy_summary,
        "risk_excerpt": risk_summary,
        "source_excerpt": source_summary,
        "source_risk_excerpt": source_risk,
    }


def build_match_notes(
    settlement: dict[str, Any],
    matches: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    notes = []
    for match_id, rows in sorted(settlement_by_match(settlement).items()):
        profit = sum(n(row.get("profit_gp")) for row in rows)
        stake = sum(n(row.get("stake_gp")) for row in rows)
        wins = sum(1 for row in rows if row.get("status") == "win")
        losses = sum(1 for row in rows if row.get("status") == "lose")
        selections = Counter(cn_team(row.get("selection")) for row in rows if row.get("selection"))
        score = ""
        first = rows[0] if rows else {}
        if first.get("home_score") is not None and first.get("away_score") is not None:
            score = f"{first.get('home_score')}-{first.get('away_score')}"
        notes.append(
            {
                "match_id": match_id,
                "match": match_label(match_id, matches),
                "score": score,
                "stake_gp": stake,
                "profit_gp": profit,
                "wins": wins,
                "losses": losses,
                "consensus_selection": selections.most_common(1)[0][0] if selections else "",
                "commentary": f"{match_label(match_id, matches)}：{wins} 单命中、{losses} 单失手，合计 {gp(profit)}；主流押注为 {selections.most_common(1)[0][0] if selections else '无'}。",
            }
        )
    return notes


def is_actual_bet(row: dict[str, Any]) -> bool:
    return str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0


def bet_label(row: dict[str, Any]) -> str:
    if not is_actual_bet(row):
        return "观望"
    selection = cn_team(row.get("selection")) or "方向"
    market = cn_market(row.get("market"))
    line = row.get("line")
    if isinstance(line, (int, float)):
        line_text = f" {line:+g}" if market == "让球" else f" {line:g}"
    else:
        line_text = f" {line}" if line not in (None, "") else ""
    odds = row.get("odds")
    odds_text = f" @{odds:g}" if isinstance(odds, (int, float)) else ""
    return f"{selection} {market}{line_text}{odds_text}"


def flatten_group_rows(groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for account, account_rows in groups.items():
        for row in account_rows:
            if not isinstance(row, dict):
                continue
            normalized = dict(row)
            normalized.setdefault("model_account", account)
            rows.append(normalized)
    return rows


def previous_observer_snapshot(date: str, round_id: str) -> dict[str, Any]:
    index_path = OUT_DIR / "index.json"
    data = load_json_safe(index_path)
    items = data.get("items") if isinstance(data.get("items"), list) else []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("date") == date and item.get("round_id") == round_id:
            continue
        if item.get("scoreboard"):
            return item
    return {}


def model_quote(row: dict[str, Any]) -> str:
    text = row.get("source_excerpt") or row.get("strategy_excerpt") or row.get("one_line")
    fallback = f"{row.get('display_name') or row.get('model_account')}本轮主线是{row.get('primary_position') or '观望'}。"
    return clean_text(text, fallback, 128)


def build_focus_match_scene(
    bet_rows: list[dict[str, Any]],
    matches: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    actual_rows = [row for row in bet_rows if is_actual_bet(row) and row.get("match_id")]
    if not actual_rows:
        return None
    by_match: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in actual_rows:
        by_match[str(row["match_id"])].append(row)
    focus_id, rows = max(
        by_match.items(),
        key=lambda item: (len(item[1]), sum(n(row.get("stake_gp")) for row in item[1])),
    )
    stake = sum(n(row.get("stake_gp")) for row in rows)
    selections = Counter(bet_label(row) for row in rows)
    top_selection = selections.most_common(1)[0][0] if selections else "分散方向"
    bullets = [
        f"{row.get('model_account') or 'seat'}：{bet_label(row)} · {gp(row.get('stake_gp'))}"
        for row in sorted(rows, key=lambda row: -n(row.get("stake_gp")))[:8]
    ]
    return {
        "key": "focus_match",
        "eyebrow": "SCENE · THE FOCUS MATCH",
        "title": f"本轮焦点：{match_label(focus_id, matches)}",
        "tone": "blue",
        "stats": [
            {"label": "下注席位", "value": f"{len(rows)}", "desc": "本轮最集中"},
            {"label": "总投入", "value": gp(stake), "desc": "集中暴露"},
        ],
        "bubble_title": f"{len(rows)} 个模型集中在 {top_selection}",
        "bullets": bullets,
        "commentary": (
            f"{match_label(focus_id, matches)} 是本轮最像主战场的一场：{len(rows)} 席下注，"
            f"资金合计 {gp(stake)}。这不是比分预测，而是盘口选择的集体暴露点；结算后最能检验模型是否真的读懂盘口。"
        ),
    }


def build_comic_story(
    ledger: dict[str, Any],
    groups: dict[str, list[dict[str, Any]]],
    matches: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    board = ledger["scoreboard"]
    commentaries = ledger.get("seat_commentaries") or []
    quality = ledger.get("data_quality") or {}
    bet_rows = flatten_group_rows(groups)
    actual_bets = [row for row in bet_rows if is_actual_bet(row)]
    no_bets = [row for row in bet_rows if str(row.get("action") or "").lower() == "no_bet" or n(row.get("stake_gp")) <= 0]
    zero_rows = [row for row in commentaries if n(row.get("stake_gp")) <= 0]
    active_rows = [row for row in commentaries if n(row.get("stake_gp")) > 0]
    previous = previous_observer_snapshot(str(ledger.get("date")), str(ledger.get("round_id")))
    previous_board = previous.get("scoreboard") if isinstance(previous.get("scoreboard"), dict) else {}
    title = "模型们开始学会选择下注"
    if zero_rows:
        title = "模型们学会不赌了"
    if ledger.get("phase") == "post":
        title = "模型们迎来赛后清算"
    coverage = f"{quality.get('quality_gate_valid_count') or board.get('models')}/{REQUIRED_SEAT_COUNT}"
    subtitle = (
        f"{coverage} 有效 · {len(actual_bets)} 笔下注 · {len(no_bets)} 次观望 · "
        f"总投入 {gp(board.get('total_stake_gp'))}"
    )
    scenes: list[dict[str, Any]] = [
        {
            "key": "cover",
            "eyebrow": f"AI PREDICTION POOL · {ledger.get('round_id')} · {ledger.get('date')}",
            "title": title,
            "subtitle": subtitle,
            "pills": [
                f"{coverage} 有效",
                f"{len(actual_bets)} 笔下注",
                f"{len(no_bets)} 次观望",
                gp(board.get("total_stake_gp")),
            ],
            "commentary": ledger.get("lead") or "",
        },
        {
            "key": "evolution",
            "eyebrow": "SCENE · THE EVOLUTION",
            "title": "从重仓冲榜到选择性下注",
            "tone": "green",
            "stats": [
                {
                    "label": f"{previous.get('round_id') or '上一轮'}",
                    "value": str(int(n(previous_board.get("accepted_bets")))) if previous_board else "—",
                    "desc": f"{gp(previous_board.get('total_stake_gp'))} · 贷款 {gp(previous_board.get('total_loan_gp'))}" if previous_board else "暂无对比轮次",
                },
                {
                    "label": str(ledger.get("round_id")),
                    "value": str(len(actual_bets)),
                    "desc": f"{gp(board.get('total_stake_gp'))} · {len(no_bets)} 次观望",
                },
            ],
            "commentary": (
                f"本轮最重要的变化不是押了谁，而是模型开始把“不下注”当成策略。"
                f"结构化下注 {len(actual_bets)} 笔，观望 {len(no_bets)} 次，说明决策从“必须出手”变成了“只在有边缘时出手”。"
            ),
        },
    ]

    if zero_rows:
        scenes.append(
            {
                "key": "zero_bet_club",
                "eyebrow": "SCENE · THE ZERO BET CLUB",
                "title": f"{len(zero_rows)} 个模型，全场零注",
                "tone": "red",
                "cards": [
                    {
                        "name": row.get("display_name"),
                        "role": f"{row.get('risk_label')} · {row.get('decision_count') or row.get('bet_count') or 0} 条决策",
                        "quote": model_quote(row),
                        "metric": "0 GP",
                    }
                    for row in zero_rows[:5]
                ],
                "commentary": (
                    "零注不是缺席，而是一个可被记录的行动。只要席位给出结构化 no_bet，"
                    "它就代表模型认为当前盘口没有足够边缘，或资金状态不允许继续冒险。"
                ),
            }
        )

    if active_rows:
        scenes.append(
            {
                "key": "selective_bettors",
                "eyebrow": "SCENE · THE SELECTIVE BETTORS",
                "title": "选择性下注：谁在承担主要风险",
                "tone": "gold",
                "cards": [
                    {
                        "name": row.get("display_name"),
                        "role": f"{row.get('risk_label')} · {row.get('bet_count')} 条决策",
                        "quote": model_quote(row),
                        "metric": gp(row.get("stake_gp")),
                    }
                    for row in sorted(active_rows, key=lambda row: -n(row.get("stake_gp")))[:6]
                ],
                "commentary": (
                    "投入最多的席位不一定最聪明，但一定暴露最多。赛后复盘时，"
                    "这些席位会优先被检查：他们是在抓正 EV，还是只是在用仓位制造存在感。"
                ),
            }
        )

    focus_scene = build_focus_match_scene(bet_rows, matches)
    if focus_scene:
        scenes.append(focus_scene)

    rerun = quality.get("quality_gate_needs_rerun") or []
    gaps = quality.get("data_gaps") or []
    if rerun or gaps:
        scenes.append(
            {
                "key": "gap_watch",
                "eyebrow": "SCENE · THE GAP",
                "title": "场边还有空椅子",
                "tone": "red",
                "bullets": [
                    f"待补席位：{', '.join(rerun) if rerun else 'none'}",
                    f"数据缺口：{len(gaps)} 项",
                    f"硬门禁：不到 {REQUIRED_SEAT_COUNT}/{REQUIRED_SEAT_COUNT}，不允许显示为全量完成报告。",
                ],
                "commentary": (
                    "这部分必须保留在解说里：它不是剧情装饰，而是产品可信度。"
                    "Grok 没有通过门禁时，战报只能叫“部分上帝视角”，不能假装全员到齐。"
                ),
            }
        )

    scenes.append(
        {
            "key": "summary",
            "eyebrow": "COMMENTARY · 解说席总结",
            "title": "本轮最值得盯的五件事",
            "tone": "green",
            "bullets": [
                f"下注从数量转向质量：{len(actual_bets)} 笔下注，{len(no_bets)} 次观望。",
                f"总资金暴露为 {gp(board.get('total_stake_gp'))}，贷款暴露 {gp(board.get('total_loan_gp'))}。",
                f"焦点比赛会决定主要叙事：{focus_scene['title'].replace('本轮焦点：', '') if focus_scene else '暂无集中主战场'}。",
                f"质量门禁当前为 {quality.get('quality_gate_status') or 'unknown'}，有效席位 {coverage}。",
                "赛后闭环要继续看：比分回填、贷款偿还、排名重排和模型自我复盘。",
            ],
            "commentary": "这轮的核心不是押中哪一场，而是模型行为出现了分化：有人进攻、有人防守、有人选择不赌。",
        }
    )

    return {
        "version": "comic_story.v1",
        "style": "comic_commentary",
        "title": title,
        "subtitle": subtitle,
        "scenes": scenes,
    }


def build_observer_ledger(date: str, round_id: str, phase: str = "auto", base_url: str = BASE_URL) -> dict[str, Any]:
    ctx = load_context(base_url, date, round_id)
    runtime = ctx["runtime"]
    daily = ctx["daily_report"]
    archives = ctx["seat_archives"]
    settlement = ctx["settlement"]
    receipts = ctx["receipts"]

    settlement_status = str(settlement.get("settlement_status") or settlement.get("status") or "")
    resolved_phase = "post" if phase == "auto" and settlement_status == "settled" else ("pre" if phase == "auto" else phase)
    current_game = load_local_current_game(date, round_id)
    strict_report = load_local_strict_god_report(date, round_id)
    seats = [row for row in archives.get("seats") or [] if isinstance(row, dict)]
    archive_source = "api_seat_archives"
    if not seats:
        seats = fallback_archives_from_strict(strict_report, current_game)
        archive_source = "local_strict_god_report_fallback" if seats else "missing"
    if not seats:
        raise RuntimeError(f"No seat archive rows for {round_id}")
    groups = settlement_groups(settlement)
    if resolved_phase != "post":
        audit_groups = audit_bet_groups(current_game)
        if audit_groups:
            groups = audit_groups
        elif archive_source == "local_strict_god_report_fallback":
            fallback_groups = fallback_groups_from_strict(strict_report)
            if fallback_groups:
                groups = fallback_groups
    matches = merge_local_match_map(match_map(runtime), current_game)
    commentaries = [
        build_seat_commentary(seat, seat_key(seat), groups.get(seat_key(seat), []), matches, resolved_phase)
        for seat in seats
    ]
    commentaries.sort(key=lambda row: (-(row["profit_gp"] if resolved_phase == "post" else row["stake_gp"]), str(row["display_name"])))

    total_stake = sum(row["stake_gp"] for row in commentaries)
    total_profit = sum(row["profit_gp"] for row in commentaries)
    total_loan = sum(row["loan_gp"] for row in commentaries)
    winners = [row for row in commentaries if row["profit_gp"] > 0]
    losers = [row for row in commentaries if row["profit_gp"] < 0]
    if resolved_phase == "post":
        best = max(commentaries, key=lambda row: row["profit_gp"]) if commentaries else None
        worst = min(commentaries, key=lambda row: row["profit_gp"]) if commentaries else None
    else:
        best = max(commentaries, key=lambda row: row["stake_gp"]) if commentaries else None
        worst = max(commentaries, key=lambda row: row["stake_gp"] + row["loan_gp"]) if commentaries else None
    settlement_summary = settlement.get("summary") or {}
    receipt_summary = receipts.get("summary") or {}
    daily_summary = daily.get("summary") or {}
    match_notes = build_match_notes(settlement, matches)
    fallback_accepted_bets = sum(
        1
        for rows in groups.values()
        for row in rows
        if str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0
    )
    quality_gate = current_game.get("quality_gate") if isinstance(current_game.get("quality_gate"), dict) else {}
    accepted_bets_count = int(n(receipt_summary.get("accepted_bets") or daily_summary.get("receipt_validation", {}).get("accepted_bets") or fallback_accepted_bets))
    provider_covered_count = receipt_summary.get("provider_covered_accepted_bets", daily_summary.get("receipt_validation", {}).get("provider_covered_accepted_bets"))
    if provider_covered_count in (None, "", "—"):
        provider_covered_count = fallback_accepted_bets

    if resolved_phase == "post":
        headline = f"{date} {round_id} 战报：波黑方向救场，巴拉圭方向集体拖累，总盘 {gp(total_profit)}"
        lead = (
            f"本轮 {len(commentaries)} 席全部有结构化回执，{int(n(settlement_summary.get('settled_bets')))} 笔已结算。"
            f" 总投入 {gp(total_stake)}，净结果 {gp(total_profit)}，赢家 {len(winners)} 席，亏损 {len(losers)} 席。"
        )
        football_summary = "比赛层面，已结算赛事按赛果和盘口结果点评；未结算赛事不提前写胜负结论。"
        pro_summary = f"资金层面，贷款暴露 {gp(total_loan)}，赛后必须先扣利息和还本，再进入排名。"
        if match_notes:
            top_note = max(match_notes, key=lambda row: abs(n(row.get("profit_gp"))))
            football_summary = f"比赛层面，{top_note['commentary']}"
        if total_profit < 0:
            pro_summary = f"资金层面，贷款暴露 {gp(total_loan)}，本轮净亏说明高杠杆追排名必须先过还息和本金清算门槛。"
    else:
        headline = f"{date} {round_id} 赛前战报：{len(commentaries)} 席下注计划已入账，等待赛果结算"
        lead = (
            f"本轮 {len(commentaries)} 席产生结构化策略，预计投入 {gp(total_stake)}，"
            f"贷款暴露 {gp(total_loan)}。该报告只记录赛前操作，不写赛果。"
        )
        active_match_ids = sorted({str(bet.get("match_id")) for rows in groups.values() for bet in rows if bet.get("match_id")})
        active_matches = [match_label(match_id, matches) for match_id in active_match_ids]
        football_summary = (
            "比赛层面，本报告处于赛前态，只记录投注集中方向；"
            + (f"主要覆盖 {compact('、'.join(active_matches), 90)}。" if active_matches else "尚无可结算比赛。")
        )
        pro_summary = f"资金层面，贷款暴露 {gp(total_loan)}；这一轮需要重点观察高杠杆席位是否能用胜率覆盖利息和回撤。"

    ledger = {
        "version": "observer_ledger.v1",
        "generated_at": now_iso(),
        "source_base_url": base_url,
        "date": date,
        "round_id": round_id,
        "phase": resolved_phase,
        "settlement_status": settlement_status,
        "headline": headline,
        "lead": lead,
        "scoreboard": {
            "models": len(commentaries),
            "accepted_bets": accepted_bets_count,
            "settled_bets": int(n(settlement_summary.get("settled_bets"))),
            "winning_bets": int(n(settlement_summary.get("winning_bets"))),
            "losing_bets": int(n(settlement_summary.get("losing_bets"))),
            "total_stake_gp": total_stake,
            "total_profit_gp": total_profit,
            "total_loan_gp": total_loan,
            "roi": total_profit / total_stake if total_stake else 0.0,
        },
        "observer_summary": {
            "data_analyst": f"数据层面，本轮有效结构化投注={provider_covered_count}，结算 ROI {pct(total_profit / total_stake if total_stake else 0)}。",
            "football_expert": football_summary,
            "pro_bettor": pro_summary,
        },
        "best_operation": best,
        "worst_operation": worst,
        "match_notes": match_notes,
        "seat_commentaries": commentaries,
        "data_quality": {
            "archive_source": archive_source,
            "quality_gate_status": quality_gate.get("status"),
            "quality_gate_valid_count": quality_gate.get("valid_count", len(quality_gate.get("valid_seats") or [])),
            "quality_gate_required_count": quality_gate.get("required_seat_count", 12),
            "quality_gate_needs_rerun": quality_gate.get("needs_rerun") or [],
            "daily_report_status": daily_summary.get("status") or daily.get("status"),
            "model_status_counts": daily.get("model_status_counts"),
            "data_gaps": daily.get("data_gaps") or [],
            "source_files": sorted(set((daily.get("source_files") or []) + (settlement.get("source_files") or []))),
        },
    }
    ledger["comic_story"] = build_comic_story(ledger, groups, matches)
    return ledger


def markdown_report(ledger: dict[str, Any]) -> str:
    board = ledger["scoreboard"]
    best = ledger.get("best_operation") or {}
    worst = ledger.get("worst_operation") or {}
    comic = ledger.get("comic_story") if isinstance(ledger.get("comic_story"), dict) else {}
    lines = [
        f"# Observer Ledger · {ledger['date']} · {ledger['round_id']}",
        "",
        f"## {ledger['headline']}",
        "",
        ledger["lead"],
        "",
        "## 记分牌",
        "",
        f"- 席位覆盖：{board['models']}/{REQUIRED_SEAT_COUNT}",
        f"- 下注/结算：{board['accepted_bets']} accepted · {board['settled_bets']} settled",
        f"- 命中/失手：{board['winning_bets']} / {board['losing_bets']}",
        f"- 总投入：{gp(board['total_stake_gp'])}",
        f"- 总盈亏：{gp(board['total_profit_gp'])} · ROI {pct(board['roi'])}",
        f"- 贷款暴露：{gp(board['total_loan_gp'])}",
        "",
        "## 漫画解说",
        "",
    ]
    if comic:
        lines.extend([f"### {comic.get('title') or '本轮解说'}", "", comic.get("subtitle") or "", ""])
        for scene in comic.get("scenes") or []:
            if not isinstance(scene, dict):
                continue
            if scene.get("key") == "cover":
                continue
            lines.extend([f"### {scene.get('title') or scene.get('key')}", ""])
            if scene.get("commentary"):
                lines.append(str(scene["commentary"]))
                lines.append("")
            for stat in scene.get("stats") or []:
                if isinstance(stat, dict):
                    lines.append(f"- {stat.get('label')}: {stat.get('value')}（{stat.get('desc') or '—'}）")
            for card in scene.get("cards") or []:
                if isinstance(card, dict):
                    lines.append(f"- {card.get('name')}: {card.get('metric') or ''} · {card.get('quote') or card.get('role') or ''}")
            for bullet in scene.get("bullets") or []:
                lines.append(f"- {bullet}")
            lines.append("")
    lines += [
        "## 三视角总评",
        "",
        f"- 数据分析师：{ledger['observer_summary']['data_analyst']}",
        f"- 足球专家：{ledger['observer_summary']['football_expert']}",
        f"- 职业赌徒：{ledger['observer_summary']['pro_bettor']}",
        "",
        "## 本日最佳/最差操作" if ledger.get("phase") == "post" else "## 本日重点/风险最高操作",
        "",
        f"- 最佳：{best.get('display_name', '—')} · {gp(best.get('profit_gp'))} · {best.get('one_line', '—')}" if ledger.get("phase") == "post" else f"- 重点：{best.get('display_name', '—')} · 投入 {gp(best.get('stake_gp'))} · {best.get('one_line', '—')}",
        f"- 最差：{worst.get('display_name', '—')} · {gp(worst.get('profit_gp'))} · {worst.get('one_line', '—')}" if ledger.get("phase") == "post" else f"- 风险最高：{worst.get('display_name', '—')} · 贷款 {gp(worst.get('loan_gp'))} · {worst.get('one_line', '—')}",
        "",
        "## 比赛流水",
        "",
    ]
    for note in ledger.get("match_notes") or []:
        score = f"（{note['score']}）" if note.get("score") else ""
        lines.append(f"- {note['match']} {score}：{note['wins']} 赢 / {note['losses']} 输，净 {gp(note['profit_gp'])}；共识方向 {note.get('consensus_selection') or '—'}。")
    lines += [
        "",
        "## 逐席点评",
        "",
        "| 席位 | 评级 | 盈亏 | 下注 | 杠杆/风险 | 一句话 |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in ledger.get("seat_commentaries") or []:
        lines.append(
            "| {name} | {grade} | {profit} | {bets} | {risk} | {one} |".format(
                name=row["display_name"],
                grade=row["grade"],
                profit=gp(row["profit_gp"]),
                bets=row["bet_count"],
                risk=row["risk_label"],
                one=row["one_line"].replace("|", "/"),
            )
        )
    lines += ["", "## 每席三视角", ""]
    for row in ledger.get("seat_commentaries") or []:
        p = row["perspectives"]
        lines.extend(
            [
                f"### {row['display_name']} · {row['grade']}",
                "",
                f"- 数据分析师：{p['data_analyst']}",
                f"- 足球专家：{p['football_expert']}",
                f"- 职业赌徒：{p['pro_bettor']}",
                f"- 原策略摘录：{row.get('strategy_excerpt') or '—'}",
                f"- 风险摘录：{row.get('risk_excerpt') or '—'}",
                "",
            ]
        )
    gaps = ledger.get("data_quality", {}).get("data_gaps") or []
    data_quality = ledger.get("data_quality", {})
    lines += [
        "## 数据审计",
        "",
        f"- 席位来源：{data_quality.get('archive_source') or '—'}",
        f"- 质量门禁：{data_quality.get('quality_gate_status') or '—'} · {data_quality.get('quality_gate_valid_count') or 0}/{data_quality.get('quality_gate_required_count') or 12}",
        f"- 待补席位：{', '.join(data_quality.get('quality_gate_needs_rerun') or []) or 'none'}",
        f"- 数据缺口：{len(gaps)}",
        f"- 结算状态：{ledger.get('settlement_status') or '—'}",
        "- 说明：本战报只读取结构化 API 数据，不虚构比分、盘口、伤停或模型想法。",
        "",
    ]
    return "\n".join(lines)


def write_outputs(ledger: dict[str, Any], out_dir: pathlib.Path = OUT_DIR) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{ledger['date']}_{ledger['round_id']}_{ledger['phase']}"
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    latest_json = out_dir / "latest.json"
    latest_md = out_dir / "latest.md"
    json_payload = json.dumps(ledger, ensure_ascii=False, indent=2)
    md_payload = markdown_report(ledger)
    json_path.write_text(json_payload + "\n", encoding="utf-8")
    md_path.write_text(md_payload + "\n", encoding="utf-8")
    latest_json.write_text(json_payload + "\n", encoding="utf-8")
    latest_md.write_text(md_payload + "\n", encoding="utf-8")
    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "latest_json": str(latest_json),
        "latest_markdown": str(latest_md),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AI pool observer ledger")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--phase", choices=["auto", "pre", "post"], default="auto")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    ledger = build_observer_ledger(args.date, args.round_id, args.phase, args.base_url)
    if args.write:
        paths = write_outputs(ledger)
        print(json.dumps({"ok": True, "paths": paths, "summary": ledger["scoreboard"]}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(ledger, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
