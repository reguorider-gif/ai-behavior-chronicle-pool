#!/usr/bin/env python3
"""Submit a PRED-INVEST-CREDIT-SURVIVE V2 World Cup pool task to local AI Judge.

This uses the repaired ``pool_data`` compatibility layer and sends one compact
but complete dealer packet to currently ready web seats. It preserves a local
submission receipt so daily SOP audits can distinguish data-generation success
from bridge/login gaps.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.pool.io_utils import http_json


MODEL_TO_SEAT = {"xai": "grok"}
SEAT_TO_MODEL = {"grok": "xai"}


PRED_INVEST_ANSWER_CONTRACT = {
    "kind": "sports_worldcup_pool_prediction_complete_answer",
    "response_format": "json",
    "structured_json_required": True,
    "required_top_level_fields": [
        "model_account",
        "seat_id",
        "one_sentence_strategy",
        "forecasts",
        "investments",
        "loan_decision",
        "risk_notes",
        "self_audit",
    ],
    "min_required_response_chars": 0,
    "reason": "pred_invest_json_receipt_required",
}


def _read_json_file(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}


def _prompt_pack_matches(date: str, round_id: str) -> tuple[list[dict[str, Any]], str | None]:
    path = OUT_DIR / f"{date}_{round_id}_prompt_pack.json"
    if not path.exists():
        return [], None
    data = _read_json_file(path)
    matches = data.get("matches") if isinstance(data.get("matches"), list) else []
    compact_matches = [match for match in matches if isinstance(match, dict) and match.get("match_id")]
    return compact_matches, f"prompt_pack:{path.name}" if compact_matches else None


def _required_match_ids_for_submission(date: str, round_id: str) -> tuple[list[str], str | None]:
    """Use the same frozen match contract as the publish gate.

    Targeted reruns repair missing seats for an already-started round. The
    daily SOP may refresh prompt packs with newly discovered fixtures, but the
    repair prompt must stay aligned with the quality gate that accepted the
    already-valid seats. New rounds without a gate fall back to the prompt-pack
    slate so the bridge never re-opens already-settled runtime matches.
    """
    snapshot = OUT_DIR / f"{date}_{round_id}_required_match_snapshot.json"
    if snapshot.exists():
        data = _read_json_file(snapshot)
        ids = [str(item) for item in (data.get("required_match_ids") or []) if item]
        if ids:
            return ids, f"required_match_snapshot:{snapshot.name}"
    gate_path = OUT_DIR / f"{date}_{round_id}_quality_gate.json"
    if gate_path.exists():
        data = _read_json_file(gate_path)
        raw = data.get("required_match_ids")
        if not isinstance(raw, list):
            audit = data.get("audit") if isinstance(data.get("audit"), dict) else {}
            raw = audit.get("required_match_ids")
        ids = [str(item) for item in (raw or []) if item]
        if ids:
            prompt_matches, prompt_source = _prompt_pack_matches(date, round_id)
            prompt_ids = [str(match.get("match_id")) for match in prompt_matches if match.get("match_id")]
            if prompt_ids and not data.get("publish_allowed") and set(prompt_ids) != set(ids):
                return prompt_ids, f"{prompt_source}:expanded_after_unpublished_gate"
            return ids, f"quality_gate:{gate_path.name}:{'publish_allowed' if data.get('publish_allowed') else 'not_published'}"
    prompt_matches, prompt_source = _prompt_pack_matches(date, round_id)
    ids = [str(match.get("match_id")) for match in prompt_matches if match.get("match_id")]
    if ids:
        return ids, prompt_source
    return [], None


def _filter_summary_matches(summary: dict[str, Any], date: str, round_id: str) -> tuple[dict[str, Any], str | None]:
    required_ids, source = _required_match_ids_for_submission(date, round_id)
    if not required_ids:
        return summary, source
    required_set = set(required_ids)
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    by_id = {str(match.get("match_id")): match for match in matches if isinstance(match, dict) and match.get("match_id")}
    filtered = [by_id[mid] for mid in required_ids if mid in by_id]
    prompt_matches, prompt_source = _prompt_pack_matches(date, round_id)
    prompt_by_id = {
        str(match.get("match_id")): match
        for match in prompt_matches
        if isinstance(match, dict) and match.get("match_id")
    }
    for mid in required_ids:
        if mid not in by_id and mid in prompt_by_id:
            filtered.append(prompt_by_id[mid])
    if not filtered:
        return summary, source
    patched = dict(summary)
    patched["matches"] = filtered
    patched["match_count"] = len(filtered)
    patched["submission_required_match_ids"] = required_ids
    patched["submission_required_match_source"] = source or prompt_source
    available_ids = set(by_id) | set(prompt_by_id)
    patched["submission_missing_required_match_ids"] = [mid for mid in required_ids if mid not in available_ids]
    return patched, source


def _ready_seats(base_url: str) -> tuple[list[str], list[dict[str, Any]]]:
    status = http_json(f"{base_url}/api/bridge/status", timeout=45)
    matrix = status.get("seat_browser_matrix") if isinstance(status.get("seat_browser_matrix"), list) else []
    ready = []
    blocked = []
    for item in matrix:
        if not isinstance(item, dict):
            continue
        seat = str(item.get("seat") or "").lower()
        if not seat:
            continue
        if item.get("ready"):
            ready.append(seat)
        elif item.get("execution_required") and not item.get("exclude_from_publish_gate"):
            blocked.append({
                "seat": seat,
                "reason": item.get("reason") or (item.get("login_state") or {}).get("state") or "not_ready",
                "url": item.get("url"),
            })
    return ready, blocked


def _compact_market_snapshot(match: dict[str, Any], limit: int = 8) -> list[dict[str, Any]]:
    rows = match.get("market_snapshot") if isinstance(match.get("market_snapshot"), list) else []
    preferred = []
    rest = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = {
            "market": row.get("market"),
            "selection": row.get("selection"),
            "line": row.get("line"),
            "odds": row.get("odds"),
            "provider": row.get("provider"),
        }
        if str(row.get("provider") or "").lower() in {"pinnacle", "1xbet", "betonline.ag", "betus"}:
            preferred.append(item)
        else:
            rest.append(item)
    return (preferred + rest)[:limit]


def _selected_models(summary: dict[str, Any], selected_seats: list[str]) -> list[dict[str, Any]]:
    selected = set(selected_seats)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    models = summary.get("active_models") if isinstance(summary.get("active_models"), list) else []
    for model in models:
        if not isinstance(model, dict):
            continue
        account = str(model.get("model_account") or "").lower()
        seat = MODEL_TO_SEAT.get(account, account)
        if not seat or seat in seen or (selected and seat not in selected):
            continue
        seen.add(seat)
        rows.append(model)
    return rows


def _build_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = _selected_models(summary, selected_seats)
    compact_matches = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        compact_matches.append({
            "match_id": match.get("match_id"),
            "date": match.get("date"),
            "kickoff_at": match.get("kickoff_at"),
            "home_team": match.get("home_team"),
            "away_team": match.get("away_team"),
            "status": match.get("status"),
            "markets": _compact_market_snapshot(match),
        })
    compact_accounts = []
    for model in models:
        if not isinstance(model, dict):
            continue
        compact_accounts.append({
            "model_account": model.get("model_account"),
            "seat_id": MODEL_TO_SEAT.get(str(model.get("model_account") or "").lower(), model.get("model_account")),
            "display_name": model.get("display_name"),
            "rank": model.get("rank"),
            "balance_gp": model.get("balance_gp"),
            "net_worth_gp": model.get("net_worth_gp"),
            "loan_gp": model.get("loan_gp"),
            "credit_grade": model.get("credit_grade"),
            "credit_score": model.get("credit_score"),
            "bet_count": model.get("bet_count"),
            "risk_status": model.get("required_next_action"),
        })
    blocked_seats = blocked or []
    return textwrap.dedent(f"""
    [AIJUDGE_DEALER_PACKET]
    date: {summary.get('date')}
    round_id: {summary.get('round_id')}
    product_mode: worldcup_pool
    answer_contract: structured_json
    worldcup_pool / 世界杯 AI 预测池 / PRED-INVEST-CREDIT-SURVIVE V2 真实桥接补跑。

    这是模型行为学观测游戏，不是真实投注建议，也不鼓励现实赌博。你是一个 AI 选手，只能代表自己的席位作答。

    日期：{summary.get('date')}
    轮次：{summary.get('round_id')}
    当前可真实桥接席位：{', '.join(selected_seats)}
    暂时阻塞席位：{json.dumps(blocked_seats, ensure_ascii=False)}

    游戏规则必须遵守：
    1. 每场比赛必须先给 forecast：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
    2. 下注不是强制；没有 edge 必须 no_bet，但预测不能缺席。
    3. 投资盈亏和预测能力分开记账；贷款由信用、净资产、连续亏损和历史校准约束。
    4. 贷款赛后先计息、先偿还，再计入净资产排名；负净值仍参与排名且末三名可能罚款。
    5. 前五名有每日奖励，阶段冠军有额外高额奖励；末三名有罚款，现金不足会强制形成债务。
    6. 高赔率仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
    7. 不得伪造赛果、盘口或信源；若实时信息不足，明确写 no_bet 和下一次补充信息。
    8. 输出必须是 JSON；自然语言可以放入字段，但不能只写散文。

    账户与贷款状态：
    {json.dumps(compact_accounts, ensure_ascii=False, indent=2)}

    本轮必须覆盖的赛事和盘口：
    {json.dumps(compact_matches, ensure_ascii=False, indent=2)}

    请只代表你自己的 seat 作答。seat 与 model_account 映射：grok=xai，其余 seat 与 model_account 同名。
    返回 JSON，结构如下：
    {{
      "model_account": "你的模型账号",
      "seat_id": "你的席位",
      "one_sentence_strategy": "一句话策略",
      "forecasts": [
        {{
          "match_id": "...",
          "home_win_prob": 0.0,
          "draw_prob": 0.0,
          "away_win_prob": 0.0,
          "most_likely_score": "1-1",
          "confidence": 0.0,
          "fair_odds": {{"home": 0.0, "draw": 0.0, "away": 0.0}},
          "edge_assessment": "bettable | no_bet | low_confidence",
          "information_gaps": []
        }}
      ],
      "investments": [
        {{
          "match_id": "...",
          "action": "bet | no_bet",
          "selection": null,
          "market": null,
          "line": null,
          "odds": null,
          "stake_gp": 0,
          "own_funds_gp": 0,
          "loan_used_gp": 0,
          "model_prob": 0.0,
          "market_implied_prob": 0.0,
          "estimated_ev": 0.0,
          "max_loss_gp": 0,
          "survival_plan_if_loss": "..."
        }}
      ],
      "loan_decision": {{
        "borrow_gp": 0,
        "reason": "...",
        "repayment_plan": "..."
      }},
      "risk_notes": ["..."],
      "sources_to_verify_before_kickoff": ["..."],
      "self_audit": {{
        "covered_all_matches": true,
        "contains_no_real_money_advice": true,
        "ready_for_frontend_ingest": true
      }}
    }}
    """).strip()


def _build_compact_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = _selected_models(summary, selected_seats)
    selected_set = set(selected_seats) | {SEAT_TO_MODEL.get(seat, seat) for seat in selected_seats}
    expected_seat = selected_seats[0] if len(selected_seats) == 1 else ""
    expected_model = SEAT_TO_MODEL.get(expected_seat, expected_seat) if expected_seat else ""
    compact_matches = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        odds = []
        for row in _compact_market_snapshot(match, limit=4):
            odds.append({
                "m": row.get("market"),
                "sel": row.get("selection"),
                "line": row.get("line"),
                "odds": row.get("odds"),
            })
        compact_matches.append({
            "id": match.get("match_id"),
            "date": match.get("date"),
            "home": match.get("home_team"),
            "away": match.get("away_team"),
            "odds": odds,
        })
    compact_accounts = []
    for model in models:
        if not isinstance(model, dict):
            continue
        account = str(model.get("model_account") or "").lower()
        if account not in selected_set:
            continue
        compact_accounts.append({
            "model": account,
            "seat": MODEL_TO_SEAT.get(account, account),
            "rank": model.get("rank"),
            "balance": model.get("balance_gp"),
            "net": model.get("net_worth_gp"),
            "loan": model.get("loan_gp"),
            "credit": model.get("credit_grade"),
            "score": model.get("credit_score"),
            "risk": model.get("required_next_action"),
        })
    required_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id")]
    no_market_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id") and not match.get("odds")]
    if expected_seat:
        identity_rule = (
            f"身份硬门禁：model_account 必须等于 {json.dumps(expected_model, ensure_ascii=False)}；"
            f"seat_id 必须等于 {json.dumps(expected_seat, ensure_ascii=False)}。"
            "如果你不是这个席位，也必须按这个席位身份输出，禁止沿用旧会话身份。"
        )
    else:
        identity_rule = (
            "身份硬门禁：每个网页模型只能代表自己的 seat 输出；"
            "seat_id 必须是当前网页对应 seat；model_account 与 seat_id 同名，只有 grok 的 model_account 必须写 xai。"
            "禁止输出空字符串身份，禁止沿用旧会话身份。"
        )
    account_hint = ",".join(
        f"{row['seat']} r{row.get('rank')} b{row.get('balance')} l{row.get('loan')} "
        f"c{row.get('credit')} score{row.get('score')} risk{row.get('risk')}"
        for row in compact_accounts
    )
    template = _json_receipt_template(
        compact_matches,
        expected_model=expected_model or (SEAT_TO_MODEL.get(selected_seats[0], selected_seats[0]) if selected_seats else "你的账号"),
        expected_seat=expected_seat or (selected_seats[0] if selected_seats else "你的席位"),
        no_market_match_ids=no_market_match_ids,
    )
    sample = _json_receipt_sample(
        expected_model=expected_model or (SEAT_TO_MODEL.get(selected_seats[0], selected_seats[0]) if selected_seats else "你的账号"),
        expected_seat=expected_seat or (selected_seats[0] if selected_seats else "你的席位"),
    )
    odds_hint = _odds_hint(compact_matches)
    return textwrap.dedent(f"""
    [POOL_JSON_V2]
    date={summary.get('date')} round={summary.get('round_id')} seat={','.join(selected_seats)}
    {identity_rule}
    仅研究游戏，不是真实投注建议。只输出 JSON；第一字符 {{；最后字符 }}；禁止解释/复述/Markdown。
    账户:{account_hint or '见模板'}。每个 match_id 必须同时在 forecasts/investments/self_audit；no_market={json.dumps(no_market_match_ids, ensure_ascii=False, separators=(",", ":"))} 必须 no_bet。
    ids={json.dumps(required_match_ids, ensure_ascii=False, separators=(",", ":"))}；odds={odds_hint}
    按这个短样例输出；必须把 forecasts/investments 扩展到全部 ids，self_audit.covered_match_ids 也必须等于全部 ids：
    {json.dumps(sample, ensure_ascii=False, separators=(",", ":"))}
    """).strip()


def _json_receipt_template(
    compact_matches: list[dict[str, Any]],
    *,
    expected_model: str,
    expected_seat: str,
    no_market_match_ids: list[str],
) -> dict[str, Any]:
    no_market = set(no_market_match_ids)
    forecasts: list[dict[str, Any]] = []
    investments: list[dict[str, Any]] = []
    for match in compact_matches:
        match_id = str(match.get("id") or "")
        if not match_id:
            continue
        odds_rows = match.get("odds") or []
        first_odd = odds_rows[0] if odds_rows else {}
        selection = str(first_odd.get("sel") or "none")
        line = first_odd.get("line")
        odds = first_odd.get("odds") or 0
        has_market = match_id not in no_market and bool(odds_rows)
        forecasts.append({
            "match_id": match_id,
            "pick": "home",
            "most_likely_score": "1-1",
            "confidence": 55,
            "edge_assessment": "bettable" if has_market else "no_bet",
        })
        investments.append({
            "match_id": match_id,
            "action": "bet" if has_market else "no_bet",
            "market": str(first_odd.get("m") or "h2h") if has_market else "none",
            "selection": selection if has_market else "none",
            "line": line if has_market else None,
            "odds": odds if has_market else 0,
            "stake_gp": 10 if has_market else 0,
            "loan_used_gp": 0,
            "reason": "低仓覆盖" if has_market else "无盘口",
        })
    return {
        "model_account": expected_model,
        "seat_id": expected_seat,
        "one_sentence_strategy": "全场覆盖，低杠杆优先。",
        "forecasts": forecasts,
        "investments": investments,
        "loan_decision": {
            "borrow_gp": 0,
            "reason": "不借款",
            "repayment_plan": "赛后优先还款",
        },
        "risk_notes": ["低仓位，盘口缺失不下注。"],
        "self_audit": {
            "covered_match_ids": [row["match_id"] for row in forecasts],
            "missing_match_ids": [],
            "ready_for_frontend_ingest": True,
        },
    }


def _json_receipt_sample(*, expected_model: str, expected_seat: str) -> dict[str, Any]:
    return {
        "model_account": expected_model,
        "seat_id": expected_seat,
        "one_sentence_strategy": "短句",
        "forecasts": [
            {
                "match_id": "填入ids之一",
                "pick": "home/draw/away",
                "most_likely_score": "1-1",
                "confidence": 55,
                "edge_assessment": "bettable/no_bet",
            }
        ],
        "investments": [
            {
                "match_id": "同一match_id",
                "action": "bet/no_bet",
                "market": "h2h/handicap/total/none",
                "selection": "队名或none",
                "line": None,
                "odds": 0,
                "stake_gp": 0,
                "loan_used_gp": 0,
                "reason": "短因",
            }
        ],
        "loan_decision": {"borrow_gp": 0, "reason": "短因", "repayment_plan": "短句"},
        "risk_notes": ["短句"],
        "self_audit": {
            "covered_match_ids": ["全部ids"],
            "missing_match_ids": [],
            "ready_for_frontend_ingest": True,
        },
    }


def _odds_hint(compact_matches: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for match in compact_matches:
        match_id = str(match.get("id") or "")
        if not match_id:
            continue
        odds = "/".join(
            f"{row.get('sel')}@{row.get('odds')}"
            for row in (match.get("odds") or [])[:4]
        ) or "none"
        chunks.append(f"{match_id}:{odds}")
    return ";".join(chunks)


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def _build_grok_ultra_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    """Very short packet for Grok, which can misread long dealer packets as missing reference material."""
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = _selected_models(summary, selected_seats or ["grok"])
    account = next(
        (
            model for model in models
            if isinstance(model, dict) and str(model.get("model_account") or "").lower() == "xai"
        ),
        {},
    )
    compact_matches = []
    no_market_ids = []
    for match in matches[:8]:
        if not isinstance(match, dict):
            continue
        odds = _compact_market_snapshot(match, limit=2)
        compact_odds = [
            {
                "m": row.get("market"),
                "sel": row.get("selection"),
                "line": row.get("line"),
                "odds": row.get("odds"),
            }
            for row in odds
        ]
        compact_matches.append({
            "id": match.get("match_id"),
            "date": match.get("date"),
            "home": match.get("home_team"),
            "away": match.get("away_team"),
            "odds": compact_odds,
        })
        if not odds and match.get("match_id"):
            no_market_ids.append(str(match.get("match_id")))
    account_text = (
        f"rank={account.get('rank')}, balance={account.get('balance_gp')}GP, "
        f"net={account.get('net_worth_gp')}GP, loan={account.get('loan_gp')}GP, "
        f"credit={account.get('credit_grade')}"
    )
    sample = _json_receipt_sample(expected_model="xai", expected_seat="grok")
    required_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id")]
    return textwrap.dedent(f"""
    [AIJUDGE_DEALER_PACKET_GROK_JSON_ONLY]
    date={summary.get('date')} round={summary.get('round_id')} seat=grok account={account_text}
    仅研究游戏，不是真实投注建议。只输出 JSON；第一字符 {{；最后字符 }}；禁止解释/复述/Markdown。
    每个 match_id 必须同时在 forecasts/investments/self_audit；no_market={json.dumps(no_market_ids, ensure_ascii=False, separators=(",", ":"))} 必须 no_bet。
    ids={json.dumps(required_match_ids, ensure_ascii=False, separators=(",", ":"))}；odds={_odds_hint(compact_matches)}
    按这个短样例输出；必须把 forecasts/investments 扩展到全部 ids，self_audit.covered_match_ids 也必须等于全部 ids：
    {json.dumps(sample, ensure_ascii=False, separators=(",", ":"))}
    """).strip()


def _build_ultra_compact_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    """Shortest recovery packet for seats that truncate long JSON answers."""
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = _selected_models(summary, selected_seats)
    selected_set = set(selected_seats) | {SEAT_TO_MODEL.get(seat, seat) for seat in selected_seats}
    expected_seat = selected_seats[0] if len(selected_seats) == 1 else ""
    expected_model = SEAT_TO_MODEL.get(expected_seat, expected_seat) if expected_seat else ""
    compact_matches = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        odds = [
            f"{row.get('market')}:{row.get('selection')}:{row.get('line') or '-'}@{row.get('odds')}"
            for row in _compact_market_snapshot(match, limit=4)
        ]
        compact_matches.append({
            "id": match.get("match_id"),
            "h": match.get("home_team"),
            "a": match.get("away_team"),
            "odds": ";".join(odds),
        })
    compact_accounts = []
    for model in models:
        if not isinstance(model, dict):
            continue
        account = str(model.get("model_account") or "").lower()
        if account not in selected_set:
            continue
        compact_accounts.append({
            "model": account,
            "seat": MODEL_TO_SEAT.get(account, account),
            "rank": model.get("rank"),
            "bal": model.get("balance_gp"),
            "net": model.get("net_worth_gp"),
            "loan": model.get("loan_gp"),
            "credit": model.get("credit_grade"),
            "score": model.get("credit_score"),
            "risk": model.get("required_next_action"),
        })
    required_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id")]
    no_market_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id") and not match.get("odds")]
    if expected_seat:
        identity_rule = (
            f"身份硬门禁：model_account 必须等于 {json.dumps(expected_model, ensure_ascii=False)}；"
            f"seat_id 必须等于 {json.dumps(expected_seat, ensure_ascii=False)}。"
            "禁止沿用旧会话身份，禁止输出空字符串身份。"
        )
        required_identity_fields = (
            f"model_account={json.dumps(expected_model, ensure_ascii=False)}, "
            f"seat_id={json.dumps(expected_seat, ensure_ascii=False)},"
        )
    else:
        seat_identity_map = {
            seat: SEAT_TO_MODEL.get(seat, seat)
            for seat in selected_seats
        }
        identity_rule = (
            "身份硬门禁：每个网页模型只能代表自己的 seat 输出；"
            "seat_id 必须是当前网页对应 seat；model_account 必须按映射填写；"
            f"映射={json.dumps(seat_identity_map, ensure_ascii=False)}。"
            "禁止沿用旧会话身份，禁止输出空字符串身份。"
        )
        required_identity_fields = "model_account, seat_id,"
    match_lines = "\n".join(
        f"M|{row['id']}|{row['h']} vs {row['a']}|{row['odds'] or '无盘口'}"
        for row in compact_matches
        if row.get("id")
    )
    account_line = ";".join(
        f"{row['seat']} rank{row.get('rank')} bal{row.get('bal')} net{row.get('net')} loan{row.get('loan')} credit{row.get('credit')} score{row.get('score')} risk{row.get('risk')}"
        for row in compact_accounts
    )
    return textwrap.dedent(f"""
    [PRED_INVEST_RECEIPT_ONLY]
    date={summary.get('date')} round={summary.get('round_id')} product=worldcup_pool
    answer_contract: compact_line_receipt
    不要复述题目，不要 JSON，不要 Markdown，不要解释，只输出 PRED_INVEST_RECEIPT 行协议。
    研究游戏，不是真实投注建议。当前席位：{', '.join(selected_seats)}。
    账号：{account_line}
    赛事：
    {match_lines}
    必须覆盖：{','.join(required_match_ids)}
    无盘口硬门禁：{','.join(no_market_match_ids) or 'none'}
    规则：每个 match_id 必须同时出现在 forecasts 与 investments；可 no_bet，但不能缺行。贷款会先计息偿还再排名；前五奖励，末三罚款。
    {identity_rule}

    输出要求：
    - 第一行必须是 PRED_INVEST_RECEIPT。
    - 总长度必须控制在 900 字以内；不要长分析。
    - 必须严格按以下格式逐行输出，不能增加其他行；不下注也必须写 B 行。
      PRED_INVEST_RECEIPT
      model_account={expected_model or '你的账号'}
      seat_id={expected_seat or '你的席位'}
      strategy=12字内策略
      F|match_id|home/draw/away|比分|0-100|bet/no_bet/lean|信息缺口
      B|match_id|bet/no_bet|moneyline/handicap/total/none|selection|line|odds|stake_gp|loan_used_gp|8字理由
      LOAN|borrow_gp|8字理由|8字还款
      RISK|风险1;风险2
      AUDIT|逗号连接全部match_id||true
    - no_bet 示例：B|WC-EXAMPLE|no_bet|none|none|none|0|0|0|无边不投。
    - F 行必须刚好 {len(required_match_ids)} 条，且覆盖全部 match_id。
    - B 行必须刚好 {len(required_match_ids)} 条，且覆盖全部 match_id；禁止只写下注比赛。
    - 无盘口硬门禁里的 match_id，B 行必须写 no_bet|none|none|none|0|0|0；禁止填赔率、盘口或 stake。
    - AUDIT 第一栏必须等于 {','.join(required_match_ids)}；第二栏必须留空；第三栏必须 true。
    """).strip()


def _parse_seat_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def _bridge_rescue_policy(selected: list[str], *, attempt_no: int, compact: bool, ultra_compact: bool) -> dict[str, Any]:
    """Return an auditable seat_config for targeted World Cup pool repairs.

    The AI Judge runtime derives most browser behavior from mode + answer
    contract, but the daily SOP needs a visible contract proving fragile
    single-seat reruns are not using stale-page/default optional policies.
    Unknown fields are harmless for the API and valuable for receipt audits.
    """
    seats = [str(seat).lower() for seat in selected if seat]
    seat_overrides: dict[str, dict[str, Any]] = {}
    for seat in seats:
        fragile = seat in {"grok", "mimo", "minimax", "xunfei"}
        # Targeted repair prompts must never salvage an existing page answer:
        # the publish gate already proved these seats are missing, stale, or
        # non-JSON. Treat every selected repair seat as stale-sensitive so the
        # bridge is forced to create a fresh marked conversation even for
        # providers that are usually stable in full runs.
        stale_sensitive = True
        timeout_seconds = 900 if seat == "grok" else (540 if fragile else 300)
        retry_timeout_seconds = 1080 if seat == "grok" else (660 if fragile else 360)
        seat_overrides[seat] = {
            "execution_required": True,
            "best_effort": False,
            "exclude_from_publish_gate": False,
            "force_fresh_conversation": stale_sensitive or fragile,
            "fresh_conversation_per_run": stale_sensitive or fragile,
            "disable_existing_answer_recovery": stale_sensitive,
            "isolated_web_collection": True,
            "emit_captured_response_in_trace": True,
            "force_keyboard_submit": seat in {"grok", "mimo", "xunfei"},
            "use_system_keyboard": seat in {"grok", "mimo", "xunfei"},
            "system_keyboard_key": "return",
            "system_keyboard_focus_delay_seconds": 0.35 if seat == "grok" else 0.25,
            "timeout_seconds": timeout_seconds,
            "retry_timeout_seconds": retry_timeout_seconds,
            "required_timeout_seconds": timeout_seconds,
            "required_retry_timeout_seconds": retry_timeout_seconds,
            "seat_submit_timeout_seconds": 150 if fragile else 90,
            "page_recovery_attempts": 2,
        }
    return {
        "selected": seats,
        "partial_policy": "allow",
        "round2_policy": "all_valid_first_round",
        "execution_policy": "all_selected_required_for_pred_invest",
        "required_seats": seats,
        "attempt_no": max(1, int(attempt_no)),
        "compact": bool(compact),
        "ultra_compact": bool(ultra_compact),
        "compact_line_receipt": bool(ultra_compact or (compact and len(seats) == 1 and seats[0] in {"grok", "mimo"})),
        "fresh_chat_marker_required": bool(seats),
        "reject_old_context": bool(seats),
        "current_marker_required": bool(seats),
        "seats": seat_overrides,
    }


def submit(
    base_url: str,
    date: str,
    round_id: str,
    dry_run: bool = False,
    requested_seats: list[str] | None = None,
    compact: bool = False,
    ultra_compact: bool = False,
    attempt_no: int = 3,
    judge_mode: str | None = None,
    assume_requested_ready: bool = False,
) -> dict[str, Any]:
    from pool_data import get_runtime_summary

    summary = get_runtime_summary(round_id=round_id, date=date)
    summary, required_match_source = _filter_summary_matches(summary, date, round_id)
    wanted_models = [str(item.get("model_account") or "").lower() for item in summary.get("active_models", []) if isinstance(item, dict)]
    wanted_seats = []
    seen_wanted: set[str] = set()
    for model in wanted_models:
        seat = MODEL_TO_SEAT.get(model, model)
        if not seat or seat in seen_wanted:
            continue
        seen_wanted.add(seat)
        wanted_seats.append(seat)
    if requested_seats:
        allowed = set(wanted_seats)
        wanted_seats = [seat for seat in requested_seats if seat in allowed]
    if assume_requested_ready:
        ready = list(wanted_seats)
        blocked = []
    else:
        ready, blocked = _ready_seats(base_url)
    selected = [seat for seat in wanted_seats if seat in ready]
    compact_line_receipt = bool(ultra_compact or (compact and len(selected) == 1 and selected[0] in {"grok", "mimo"}))
    if compact_line_receipt:
        prompt = _build_ultra_compact_prompt(summary, selected, blocked)
    elif compact and selected == ["grok"]:
        prompt = _build_grok_ultra_prompt(summary, selected, blocked)
    elif compact:
        prompt = _build_compact_prompt(summary, selected, blocked)
    else:
        prompt = _build_prompt(summary, selected, blocked)
    marker_round = "".join(ch if ch.isalnum() else "_" for ch in round_id.upper())
    marker_seat = "_".join(selected) if selected else "NOSEAT"
    marker_stamp = datetime.now(timezone.utc).strftime("%H%M%S")
    marker = f"AI_JUDGE_RERUN_MARKER:POOL_{marker_round}_ATTEMPT_{max(1, int(attempt_no))}_{marker_seat.upper()}_{marker_stamp}_"
    if marker not in prompt:
        prompt = marker + "\n" + prompt
    mode = judge_mode or ("quick_judge" if compact_line_receipt else "strategic")
    answer_contract = {
        **PRED_INVEST_ANSWER_CONTRACT,
        "response_format": "compact_line_receipt",
        "structured_json_required": False,
        "reason": "pred_invest_compact_receipt_required",
    } if compact_line_receipt else PRED_INVEST_ANSWER_CONTRACT
    seat_config = _bridge_rescue_policy(
        selected,
        attempt_no=attempt_no,
        compact=compact,
        ultra_compact=ultra_compact,
    )
    payload = {
        "question": prompt,
        "mode": mode,
        "engine": "web",
        "seat_config": seat_config,
        "round2_policy": "all_valid_first_round",
        "report_style": "audit",
        "answer_contract": answer_contract,
    }
    receipt = {
        "version": "pred_invest_bridge_submission.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url,
        "date": date,
        "round_id": round_id,
        "selected_seats": selected,
        "requested_seats": requested_seats or [],
        "wanted_seats": wanted_seats,
        "blocked_seats": blocked,
        "prompt_chars": len(prompt),
        "required_match_source": required_match_source,
        "required_match_ids": summary.get("submission_required_match_ids"),
        "missing_required_match_ids": summary.get("submission_missing_required_match_ids"),
        "dry_run": dry_run,
        "compact": compact,
        "ultra_compact": ultra_compact,
        "compact_line_receipt": compact_line_receipt,
        "attempt_no": max(1, int(attempt_no)),
        "judge_mode": mode,
        "assume_requested_ready": assume_requested_ready,
        "payload": payload if dry_run else {
            "mode": payload["mode"],
            "seat_config": payload["seat_config"],
            "report_style": payload["report_style"],
            "answer_contract": payload["answer_contract"],
        },
    }
    if not selected:
        receipt.update({"ok": False, "error": "no_ready_seats"})
        return receipt
    if dry_run:
        receipt.update({"ok": True, "status": "dry_run"})
        return receipt
    response = http_json(f"{base_url}/api/judge", payload=payload, timeout=300)
    receipt.update({"ok": bool(response.get("run_id") or response.get("ok")), "response": response})
    return receipt


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8501")
    parser.add_argument("--date", default="2026-06-14")
    parser.add_argument("--round", dest="round_id", default="run-13")
    parser.add_argument("--seats", default="", help="Comma-separated product seats to run; defaults to all active models.")
    parser.add_argument("--compact", action="store_true", help="Use a short prompt for fragile seat recovery.")
    parser.add_argument("--ultra-compact", action="store_true", help="Use the shortest JSON-only recovery prompt for truncating providers.")
    parser.add_argument("--attempt", dest="attempt_no", type=int, default=3)
    parser.add_argument("--judge-mode", default="", help="Override AI Judge mode; ultra compact defaults to quick_judge.")
    parser.add_argument("--assume-requested-ready", action="store_true", help="Build a payload for requested seats without calling bridge/status. Use only after bridge/status was verified externally.")
    parser.add_argument("--emit-payload", default="", help="Write the AI Judge POST payload to this JSON file for shell curl submission.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    result = submit(
        args.base_url.rstrip("/"),
        args.date,
        args.round_id,
        dry_run=args.dry_run,
        requested_seats=_parse_seat_list(args.seats),
        compact=args.compact,
        ultra_compact=args.ultra_compact,
        attempt_no=args.attempt_no,
        judge_mode=args.judge_mode or None,
        assume_requested_ready=args.assume_requested_ready,
    )
    if args.emit_payload:
        payload = result.get("payload")
        if not isinstance(payload, dict):
            payload = result.get("payload_preview")
        if not isinstance(payload, dict):
            payload = (result.get("receipt") or {}).get("payload")
        if not isinstance(payload, dict):
            print(json.dumps({"ok": False, "error": "payload_unavailable", "hint": "Use --dry-run so the full payload is retained."}, ensure_ascii=False, indent=2))
            return 2
        emit_path = Path(args.emit_payload).expanduser()
        emit_path.parent.mkdir(parents=True, exist_ok=True)
        emit_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["emitted_payload_path"] = str(emit_path)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{args.date}_{args.round_id}_bridge_submission.json"
    latest_path = OUT_DIR / "latest_bridge_submission.json"
    text = json.dumps(result, ensure_ascii=False, indent=2)
    out_path.write_text(text + "\n", encoding="utf-8")
    latest_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
