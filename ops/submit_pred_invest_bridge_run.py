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
import urllib.parse
import sys
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


MODEL_TO_SEAT = {"xai": "grok"}
SEAT_TO_MODEL = {"grok": "xai"}
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _is_local_url(url: str) -> bool:
    return (urllib.parse.urlparse(url).hostname or "").lower() in LOCAL_HOSTS


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


def _http_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if _is_local_url(url) else urllib.request
        with opener.open(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                return json.loads(raw)
            except Exception:
                return {"ok": False, "error": "non_json_response", "raw": raw[:2000], "status": response.status}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw[:2000]}
        body.setdefault("ok", False)
        body.setdefault("status", exc.code)
        return body
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}


def _read_json_file(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}


def _required_match_ids_for_submission(date: str, round_id: str) -> tuple[list[str], str | None]:
    """Use the same frozen match contract as the publish gate.

    Targeted reruns repair missing seats for an already-started round. The
    daily SOP may refresh prompt packs with newly discovered fixtures, but the
    repair prompt must stay aligned with the quality gate that accepted the
    already-valid seats.
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
            return ids, f"quality_gate:{gate_path.name}"
    return [], None


def _filter_summary_matches(summary: dict[str, Any], date: str, round_id: str) -> tuple[dict[str, Any], str | None]:
    required_ids, source = _required_match_ids_for_submission(date, round_id)
    if not required_ids:
        return summary, source
    required_set = set(required_ids)
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    by_id = {str(match.get("match_id")): match for match in matches if isinstance(match, dict) and match.get("match_id")}
    filtered = [by_id[mid] for mid in required_ids if mid in by_id]
    if not filtered:
        return summary, source
    patched = dict(summary)
    patched["matches"] = filtered
    patched["match_count"] = len(filtered)
    patched["submission_required_match_ids"] = required_ids
    patched["submission_required_match_source"] = source
    patched["submission_missing_required_match_ids"] = [mid for mid in required_ids if mid not in by_id]
    return patched, source


def _ready_seats(base_url: str) -> tuple[list[str], list[dict[str, Any]]]:
    status = _http_json(f"{base_url}/api/bridge/status", timeout=45)
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


def _build_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = summary.get("active_models") if isinstance(summary.get("active_models"), list) else []
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
    models = summary.get("active_models") if isinstance(summary.get("active_models"), list) else []
    selected_set = set(selected_seats) | {SEAT_TO_MODEL.get(seat, seat) for seat in selected_seats}
    compact_matches = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        odds = []
        for row in _compact_market_snapshot(match, limit=3):
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
        })
    required_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id")]
    if expected_seat:
        identity_rule = (
            f"身份硬门禁：model_account 必须等于 {json.dumps(expected_model, ensure_ascii=False)}；"
            f"seat_id 必须等于 {json.dumps(expected_seat, ensure_ascii=False)}。"
            "如果你不是这个席位，也必须按这个席位身份输出，禁止沿用旧会话身份。"
        )
        required_identity_fields = (
            f"model_account={json.dumps(expected_model, ensure_ascii=False)}, "
            f"seat_id={json.dumps(expected_seat, ensure_ascii=False)},"
        )
    else:
        identity_rule = (
            "身份硬门禁：每个网页模型只能代表自己的 seat 输出；"
            "seat_id 必须是当前网页对应 seat；model_account 与 seat_id 同名，只有 grok 的 model_account 必须写 xai。"
            "禁止输出空字符串身份，禁止沿用旧会话身份。"
        )
        seat_identity_map = {
            seat: SEAT_TO_MODEL.get(seat, seat)
            for seat in selected_seats
        }
        required_identity_fields = (
            "model_account/seat_id 必须匹配当前网页 seat，映射为 "
            f"{json.dumps(seat_identity_map, ensure_ascii=False)},"
        )
    return textwrap.dedent(f"""
    [AIJUDGE_DEALER_PACKET_COMPACT]
    date: {summary.get('date')}
    round_id: {summary.get('round_id')}
    product_mode: worldcup_pool
    answer_contract: structured_json
    世界杯 AI 预测池 PRED-INVEST-CREDIT-SURVIVE V2，补齐缺失席位。仅研究游戏，不是真实投注建议。
    你只能代表自己的 seat 作答；当前席位：{', '.join(selected_seats)}。阻塞席位：{json.dumps(blocked, ensure_ascii=False)}。

    规则：每场必须 forecast；每场必须有 investment 行，可 bet 或 no_bet；贷款赛后先计息先偿还再排名；前五奖励、末三罚款；不得伪造信源。
    账户：{json.dumps(compact_accounts, ensure_ascii=False)}
    赛事盘口：{json.dumps(compact_matches, ensure_ascii=False)}
    必须覆盖的 match_id：{json.dumps(required_match_ids, ensure_ascii=False)}

    输出硬门禁：
    - 只能输出一个 JSON object；首字符必须是 {{，末字符必须是 }}。
    - 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
    - forecasts 必须正好覆盖上方全部 match_id；investments 也必须正好覆盖上方全部 match_id。
    - 任何没有 edge 的比赛也必须写 investment，action="no_bet"，stake_gp=0。
    - 不允许替换成旧比赛、热身赛历史窗口、其他 6/15 大列表或非本轮赛事。
    - 如果信息不足，仍然给低置信 forecast，并在 information_gaps 写明，不得缺席。

    请输出 JSON 字段：
    model_account, seat_id, one_sentence_strategy,
    forecasts:[{{match_id, home_win_prob, draw_prob, away_win_prob, most_likely_score, confidence, fair_odds, edge_assessment, information_gaps}}],
    investments:[{{match_id, action, market, selection, line, odds, stake_gp, own_funds_gp, loan_used_gp, model_prob, market_implied_prob, estimated_ev, max_loss_gp, survival_plan_if_loss}}],
    loan_decision:{{borrow_gp, reason, repayment_plan}},
    risk_notes, sources_to_verify_before_kickoff,
    self_audit:{{covered_match_ids, missing_match_ids, ready_for_frontend_ingest}}.
    self_audit.covered_match_ids 必须等于上方全部 match_id；missing_match_ids 必须是 []；ready_for_frontend_ingest 必须是 true。
    中文为主，紧凑，不超过 1200 字；不要只思考，必须最终输出 JSON。
    """).strip()


def _build_grok_ultra_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    """Very short packet for Grok, which can misread long dealer packets as missing reference material."""
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = summary.get("active_models") if isinstance(summary.get("active_models"), list) else []
    account = next(
        (
            model for model in models
            if isinstance(model, dict) and str(model.get("model_account") or "").lower() == "xai"
        ),
        {},
    )
    lines = []
    for match in matches[:8]:
        if not isinstance(match, dict):
            continue
        odds = _compact_market_snapshot(match, limit=2)
        odd_text = "/".join(
            f"{row.get('market')} {row.get('selection')} {row.get('line') or ''}@{row.get('odds')}"
            for row in odds
        )
        lines.append(
            f"{match.get('match_id')} {match.get('home_team')} vs {match.get('away_team')} {odd_text}"
        )
    account_text = (
        f"rank={account.get('rank')}, balance={account.get('balance_gp')}GP, "
        f"net={account.get('net_worth_gp')}GP, loan={account.get('loan_gp')}GP, "
        f"credit={account.get('credit_grade')}"
    )
    return textwrap.dedent(f"""
    [AIJUDGE_DEALER_PACKET_GROK_ULTRA]
    date: {summary.get('date')}
    round_id: {summary.get('round_id')}
    product_mode: worldcup_pool
    answer_contract: structured_json
    完整任务素材已在本消息内给出；不要再要求补充材料。仅模型行为学研究，不是真实投注建议。
    你是 Grok/xAI 席位。当前账户：{account_text}。阻塞席位：{json.dumps(blocked, ensure_ascii=False)}。
    游戏规则：每场必须 forecast；每场必须有 investment 行，可 bet/no_bet；可贷款，但赛后先计息还款再排名；前五奖励、末三罚款；不得伪造来源。
    可投注盘口：
    {'; '.join(lines)}

    请直接输出中文 JSON，不要解释过程。字段：
    model_account="xai", seat_id="grok", one_sentence_strategy,
    forecasts:[{{match_id, most_likely_score, confidence}}],
    investments:[{{match_id, action, market, selection, line, odds, stake_gp, loan_used_gp, survival_plan_if_loss}}],
    loan_decision:{{borrow_gp, reason, repayment_plan}},
    risk_notes, self_audit:{{covered_match_ids, missing_match_ids, ready_for_frontend_ingest}}。
    所有上方 match_id 必须同时出现在 forecasts 和 investments；缺任何一个就是无效答案。
    字数控制在 900 字内。
    """).strip()


def _build_ultra_compact_prompt(summary: dict[str, Any], selected_seats: list[str], blocked: list[dict[str, Any]]) -> str:
    """Shortest recovery packet for seats that truncate long JSON answers."""
    matches = summary.get("matches") if isinstance(summary.get("matches"), list) else []
    models = summary.get("active_models") if isinstance(summary.get("active_models"), list) else []
    selected_set = set(selected_seats) | {SEAT_TO_MODEL.get(seat, seat) for seat in selected_seats}
    expected_seat = selected_seats[0] if len(selected_seats) == 1 else ""
    expected_model = SEAT_TO_MODEL.get(expected_seat, expected_seat) if expected_seat else ""
    compact_matches = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        odds = [
            f"{row.get('market')}:{row.get('selection')}:{row.get('line') or '-'}@{row.get('odds')}"
            for row in _compact_market_snapshot(match, limit=2)
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
        })
    required_match_ids = [str(match.get("id") or "") for match in compact_matches if match.get("id")]
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
        f"{row['seat']} rank{row.get('rank')} bal{row.get('bal')} net{row.get('net')} loan{row.get('loan')} credit{row.get('credit')}"
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
    - AUDIT 第一栏必须等于 {','.join(required_match_ids)}；第二栏必须留空；第三栏必须 true。
    """).strip()


def _parse_seat_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


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
) -> dict[str, Any]:
    from pool_data import get_runtime_summary

    summary = get_runtime_summary(round_id=round_id, date=date)
    summary, required_match_source = _filter_summary_matches(summary, date, round_id)
    ready, blocked = _ready_seats(base_url)
    wanted_models = [str(item.get("model_account") or "").lower() for item in summary.get("active_models", []) if isinstance(item, dict)]
    wanted_seats = [MODEL_TO_SEAT.get(model, model) for model in wanted_models]
    if requested_seats:
        allowed = set(wanted_seats)
        wanted_seats = [seat for seat in requested_seats if seat in allowed]
    selected = [seat for seat in wanted_seats if seat in ready]
    if ultra_compact:
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
    mode = judge_mode or ("quick_judge" if ultra_compact else "strategic")
    answer_contract = {
        **PRED_INVEST_ANSWER_CONTRACT,
        "response_format": "compact_line_receipt",
        "structured_json_required": False,
        "reason": "pred_invest_compact_receipt_required",
    } if ultra_compact else PRED_INVEST_ANSWER_CONTRACT
    payload = {
        "question": prompt,
        "mode": mode,
        "engine": "web",
        "seat_config": {
            "selected": selected,
            "partial_policy": "allow",
            "round2_policy": "all_valid_first_round",
        },
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
        "attempt_no": max(1, int(attempt_no)),
        "judge_mode": mode,
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
    response = _http_json(f"{base_url}/api/judge", payload=payload, timeout=60)
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
    )
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
