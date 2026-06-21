#!/usr/bin/env python3
"""Generate PRED-INVEST V2 prompt packs for daily AI Judge runs.

This is an operational input to the daily SOP, not a product-explainer page.
The generated prompts are the contract the bridge sends to each model.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from pred_invest_quality_gate import REQUIRED_SEATS
from pred_invest_rules import daily_rules_text, gp, loan_terms, prompt_schema_text
from pred_invest_schedule_overrides import apply_schedule_override


BASE_URL = "https://pool-app-one.vercel.app"
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
REQUIRED_MATCHES_PATH = OUT_DIR / "required_matches.json"
MATCH_RESULTS_PATH = ROOT / "data" / "pool" / "match_results" / "latest_known_scores.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.pool.prompt_context_builder import build_market_snapshot, build_prompt_context

SEAT_DISPLAY_NAMES = {
    "chatgpt": "ChatGPT",
    "deepseek": "DeepSeek",
    "mimo": "MiMo",
    "minimax": "MiniMax",
    "doubao": "Doubao",
    "gemini": "Gemini",
    "kimi": "Kimi",
    "meta": "Meta AI",
    "qwen": "Qwen",
    "wenxin": "Wenxin",
    "grok": "xAI Grok",
    "yuanbao": "Yuanbao",
}
MODEL_ACCOUNT_BY_SEAT = {"grok": "xai"}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def fetch_json(url: str, timeout: int = 45) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} while fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while fetching {url}: {exc}") from exc
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected JSON object from {url}")
    return data


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def settled_match_ids() -> set[str]:
    payload = read_json(MATCH_RESULTS_PATH)
    ids: set[str] = set()
    for row in payload.get("matches") or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("status") or "").lower() == "settled" and row.get("match_id"):
            ids.add(str(row["match_id"]))
    return ids


def api_url(base_url: str, path: str, **query: str) -> str:
    encoded = urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    return f"{base_url.rstrip('/')}{path}" + (f"?{encoded}" if encoded else "")


def account_key(row: dict[str, Any]) -> str:
    raw = str(row.get("seat_id") or row.get("model_account") or "").lower()
    return "grok" if raw == "xai" else raw


def display_name(row: dict[str, Any]) -> str:
    return str(row.get("display_name") or row.get("model_account") or row.get("seat_id") or "unknown")


def set_missing(row: dict[str, Any], key: str, value: Any) -> None:
    if row.get(key) in (None, ""):
        row[key] = value


def active_accounts(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    ranking = [row for row in runtime.get("current_ranking") or [] if isinstance(row, dict)]
    active = [row for row in runtime.get("active_models") or [] if isinstance(row, dict)]
    by_key = {account_key(row): row for row in ranking if account_key(row)}
    for row in active:
        key = account_key(row)
        if key:
            by_key[key] = {**row, **by_key.get(key, {})}
    rows: list[dict[str, Any]] = []
    for index, seat in enumerate(REQUIRED_SEATS, start=1):
        row = dict(by_key.get(seat) or {})
        set_missing(row, "seat_id", seat)
        set_missing(row, "model_account", MODEL_ACCOUNT_BY_SEAT.get(seat, seat))
        set_missing(row, "display_name", SEAT_DISPLAY_NAMES.get(seat, seat))
        set_missing(row, "rank", row.get("computed_rank") or index)
        set_missing(row, "computed_rank", row.get("rank") or index)
        set_missing(row, "balance_gp", row.get("confirmed_current_balance_gp") or 1000)
        set_missing(row, "confirmed_current_balance_gp", row.get("balance_gp") or 1000)
        set_missing(row, "loan_gp", row.get("remaining_loan_gp") or 0)
        set_missing(row, "remaining_loan_gp", row.get("loan_gp") or 0)
        if seat not in by_key:
            row["account_source"] = "required_seat_placeholder"
            row["status_label"] = "待补跑/待同步"
        rows.append(row)
    return rows


def match_date_keys(match: dict[str, Any]) -> set[str]:
    match = apply_schedule_override(match)
    keys = {
        str(match.get("date") or ""),
        str(match.get("matchday_hk") or ""),
        str(match.get("kickoff_date_utc") or ""),
    }
    for key in ("automation_date", "automation_dates"):
        value = match.get(key)
        if isinstance(value, str):
            keys.add(value)
        elif isinstance(value, list):
            keys.update(str(item) for item in value)
    return {key for key in keys if key}


def match_pool(runtime: dict[str, Any], date: str, include_fallback: bool = True, settled_ids: set[str] | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    settled_ids = settled_ids or set()
    for source_key in ("matches", "future_matches"):
        for match in runtime.get(source_key) or []:
            if not isinstance(match, dict):
                continue
            match = apply_schedule_override(match)
            match_id = str(match.get("match_id") or match.get("id") or "")
            if not match_id or match_id in seen:
                continue
            if match_id in settled_ids:
                continue
            if date in match_date_keys(match) and str(match.get("status") or "").lower() != "settled":
                rows.append(match)
                seen.add(match_id)
    if rows or not include_fallback:
        return rows
    future = [
        apply_schedule_override(match) for match in (runtime.get("future_matches") or runtime.get("matches") or [])
        if isinstance(match, dict)
        and str(match.get("status") or "").lower() != "settled"
        and str(match.get("match_id") or match.get("id") or "") not in settled_ids
    ]
    future.sort(key=lambda row: str(row.get("kickoff_at") or row.get("date") or ""))
    return future[:4]


def match_id(match: dict[str, Any]) -> str:
    return str(match.get("match_id") or match.get("id") or "")


def required_matches(date: str | None = None, settled_ids: set[str] | None = None) -> list[dict[str, Any]]:
    settled_ids = settled_ids or set()
    if not REQUIRED_MATCHES_PATH.exists():
        return []
    try:
        payload = json.loads(REQUIRED_MATCHES_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = payload.get("matches") if isinstance(payload, dict) else []
    filtered = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        row = apply_schedule_override(row)
        if not row.get("include_in_prompt_pack", True):
            continue
        if str(row.get("status") or "").lower() == "settled":
            continue
        if not match_id(row):
            continue
        if match_id(row) in settled_ids:
            continue
        if date and date not in match_date_keys(row):
            continue
        filtered.append(row)
    return filtered


def frozen_required_match_snapshot(date: str, round_id: str) -> list[dict[str, Any]]:
    """Return a run-specific historical match contract when one is frozen.

    Daily pre-match generation should skip settled matches. Historical
    acceptance/replay runs are different: they must rebuild the exact original
    run contract even after score backfill marks those matches settled.
    """

    snapshot_path = OUT_DIR / f"{date}_{round_id}_required_match_snapshot.json"
    payload = read_json(snapshot_path)
    rows = payload.get("matches") if isinstance(payload, dict) else []
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict) and match_id(row)]


def hydrate_frozen_match_markets(matches: list[dict[str, Any]], date: str, round_id: str) -> list[dict[str, Any]]:
    if not matches:
        return matches
    by_id: dict[str, dict[str, Any]] = {}
    for rel in (f"{date}_{round_id}_current_game.json", "latest_current_game.json"):
        payload = read_json(OUT_DIR / rel)
        if payload.get("date") not in (None, "", date) and payload.get("round_id") not in (None, "", round_id):
            continue
        for row in payload.get("matches") or []:
            if isinstance(row, dict) and match_id(row):
                by_id.setdefault(match_id(row), row)
    hydrated: list[dict[str, Any]] = []
    for row in matches:
        merged = dict(row)
        source = by_id.get(match_id(row)) or {}
        if not merged.get("market_snapshot") and source.get("market_snapshot"):
            merged["market_snapshot"] = source["market_snapshot"]
        if not merged.get("available_markets") and source.get("available_markets"):
            merged["available_markets"] = source["available_markets"]
        hydrated.append(merged)
    return hydrated


def merge_required_matches(matches: list[dict[str, Any]], required: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = list(matches)
    seen = {match_id(match) for match in merged if match_id(match)}
    for match in required:
        identifier = match_id(match)
        if identifier and identifier not in seen:
            merged.append(match)
            seen.add(identifier)
    return merged


def required_coverage(matches: list[dict[str, Any]], required: list[dict[str, Any]]) -> dict[str, Any]:
    required_ids = [match_id(match) for match in required if match_id(match)]
    included_ids = {match_id(match) for match in matches if match_id(match)}
    missing = [identifier for identifier in required_ids if identifier not in included_ids]
    return {
        "required_match_ids": required_ids,
        "included_required_match_ids": [identifier for identifier in required_ids if identifier in included_ids],
        "missing_required_match_ids": missing,
    }


def market_snapshot(match: dict[str, Any], odds_by_match: dict[str, list[dict[str, Any]]] | None = None) -> list[dict[str, Any]]:
    match_id = str(match.get("match_id") or match.get("id") or "")
    if odds_by_match and odds_by_match.get(match_id):
        compact_rows = []
        for row in odds_by_match[match_id][:12]:
            compact_rows.append(
                {
                    "market": row.get("market"),
                    "selection": row.get("selection"),
                    "line": row.get("line"),
                    "odds": row.get("odds"),
                    "provider": row.get("bookmaker_or_provider") or row.get("provider"),
                }
            )
        return compact_rows
    existing_snapshot = match.get("market_snapshot")
    if isinstance(existing_snapshot, list):
        compact_rows = []
        for row in existing_snapshot[:12]:
            if not isinstance(row, dict):
                continue
            compact_rows.append(
                {
                    "market": row.get("market"),
                    "selection": row.get("selection"),
                    "line": row.get("line"),
                    "odds": row.get("odds"),
                    "provider": row.get("bookmaker_or_provider") or row.get("provider"),
                }
            )
        if compact_rows:
            return compact_rows
    samples = []
    for sample in match.get("odds_samples") or match.get("snapshot_odds_samples") or []:
        if isinstance(sample, dict):
            samples.append(sample)
    if samples:
        return samples[:8]
    fallback = []
    if match.get("odds_home"):
        fallback.append({"market": "h2h", "selection": match.get("home_team"), "odds": match.get("odds_home")})
    if match.get("odds_draw"):
        fallback.append({"market": "h2h", "selection": "Draw", "odds": match.get("odds_draw")})
    if match.get("odds_away"):
        fallback.append({"market": "h2h", "selection": match.get("away_team"), "odds": match.get("odds_away")})
    return fallback


def compact_match(match: dict[str, Any], odds_by_match: dict[str, list[dict[str, Any]]] | None = None) -> dict[str, Any]:
    match = apply_schedule_override(match)
    return {
        "match_id": match.get("match_id") or match.get("id"),
        "date": match.get("date"),
        "kickoff_at": match.get("kickoff_at"),
        "home_team": match.get("home_team"),
        "away_team": match.get("away_team"),
        "status": match.get("status"),
        "available_markets": match.get("eligible_markets") or match.get("snapshot_markets") or [],
        "market_snapshot": market_snapshot(match, odds_by_match),
    }


def odds_by_match(odds_snapshot: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in odds_snapshot.get("odds") or []:
        if not isinstance(row, dict):
            continue
        match_id = str(row.get("match_id") or "")
        if not match_id or row.get("status") not in (None, "ok"):
            continue
        grouped.setdefault(match_id, []).append(row)
    for rows in grouped.values():
        rows.sort(key=lambda row: (str(row.get("market") or ""), str(row.get("selection") or ""), str(row.get("bookmaker_or_provider") or "")))
    return grouped


def build_prompt(
    account: dict[str, Any],
    matches: list[dict[str, Any]],
    date: str,
    round_id: str,
    match_odds: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    terms = loan_terms(account)
    identity = display_name(account)
    account_text = (
        f"模型：{identity}\n"
        f"当前排名：{account.get('rank') or account.get('computed_rank') or '未知'}\n"
        f"当前余额：{gp(account.get('balance_gp') or account.get('confirmed_current_balance_gp'))}\n"
        f"未还贷款：{gp(account.get('loan_gp') or account.get('remaining_loan_gp'))}\n"
        f"净资产：{gp(terms['net_worth_gp'])}\n"
        f"信用等级：{terms['credit_grade']}（{terms['credit_score']}，basis={terms['credit_basis']}）\n"
        f"本轮可新增贷款：{gp(terms['available_loan_gp'])}\n"
        f"基础利率：{terms['base_interest_rate'] if terms['base_interest_rate'] is not None else '禁贷'}"
    )
    match_text = json.dumps([compact_match(match, match_odds) for match in matches], ensure_ascii=False, indent=2)
    prompt = f"""你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：{date}
轮次：{round_id}

{daily_rules_text()}

你的账户状态：
{account_text}

今日必须评估的比赛：
{match_text}

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {{，末字符必须是 }}。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

{prompt_schema_text()}
"""
    return {
        "model_account": account_key(account),
        "display_name": identity,
        "loan_terms": terms,
        "prompt": prompt,
    }


def build_prompt_pack(date: str, round_id: str, base_url: str = BASE_URL, *, write_contexts: bool = False) -> dict[str, Any]:
    source_warning = None
    try:
        runtime = fetch_json(api_url(base_url, "/api/pool/runtime-summary", date=date, round_id=round_id))
    except RuntimeError as exc:
        source_warning = f"runtime_summary_api_unavailable_using_local_artifact:{exc}"
        from pool_data import get_runtime_summary

        runtime = get_runtime_summary(round_id=round_id, date=date)
    runtime_date = str(runtime.get("date") or "")
    runtime_round = str(runtime.get("round_id") or runtime.get("current_round") or "")
    runtime_stale = bool((runtime_date and runtime_date != date) or (runtime_round and runtime_round != round_id))
    matches_endpoint = {}
    try:
        matches_endpoint = fetch_json(api_url(base_url, "/api/matches"))
    except RuntimeError:
        matches_endpoint = {}
    if (not runtime.get("matches") or runtime_stale) and isinstance(matches_endpoint.get("matches"), list):
        runtime = dict(runtime)
        runtime["matches"] = matches_endpoint["matches"]
        source_warning = (source_warning + "; " if source_warning else "") + "runtime_summary_stale_or_empty_using_matches_endpoint"
    odds_snapshot = {}
    try:
        odds_snapshot = fetch_json(api_url(base_url, f"/api/pool/odds-snapshots/{date}/T-1h"))
    except RuntimeError:
        odds_snapshot = {}
    match_odds = odds_by_match(odds_snapshot)
    accounts = active_accounts(runtime)
    settled_ids = settled_match_ids()
    frozen_required = frozen_required_match_snapshot(date, round_id)
    if frozen_required:
        required = hydrate_frozen_match_markets(frozen_required, date, round_id)
        matches = required
    else:
        required = required_matches(date, settled_ids=settled_ids)
        matches = merge_required_matches(match_pool(runtime, date, include_fallback=False, settled_ids=settled_ids), required)
    compact_matches = [compact_match(match, match_odds) for match in matches]
    prompt_context_status = {"written": False, "count": 0, "seats": []}
    if write_contexts:
        accounts_by_seat = {account_key(account): account for account in accounts if account_key(account)}
        market_context = build_market_snapshot(date, round_id, compact_matches, write=True)
        written_seats: list[str] = []
        for account in accounts:
            seat_id = account_key(account)
            if not seat_id:
                continue
            build_prompt_context(
                date,
                round_id,
                seat_id,
                accounts=accounts_by_seat,
                matches=compact_matches,
                market_snapshot=market_context,
                write=True,
            )
            written_seats.append(seat_id)
        prompt_context_status = {"written": True, "count": len(written_seats), "seats": written_seats}
    prompts = [build_prompt(account, matches, date, round_id, match_odds) for account in accounts]
    return {
        "version": "pred_invest_prompt_pack.v2",
        "generated_at": now_iso(),
        "source_base_url": base_url,
        "date": date,
        "round_id": round_id,
        "operational_contract": {
            "rule_version": "PRED_INVEST_CREDIT_SURVIVE_V2",
            "purpose": "daily_ai_judge_execution_contract",
            "not_public_feature_copy": True,
            "daily_sequence": [
                "sync_match_results_and_odds",
                "settle_finished_matches",
                "repay_interest_and_principal_before_ranking",
                "apply_daily_rewards_and_bottom_penalties",
                "build_full_match_prompt_pack",
                "collect_12_model_forecasts_and_investments",
                "quality_gate_and_targeted_rerun_only_missing_seats",
                "write_god_report_and_frontend_artifacts",
            ],
            "surface_policy": "front_end_shows_results_logs_and_health_only; internal_sop_details_remain_artifacts",
        },
        "runtime_version": runtime.get("version"),
        "current_round": runtime.get("current_round"),
        "source_warning": source_warning,
        "settled_match_filter_count": len(settled_ids),
        "match_count": len(matches),
        "required_coverage": required_coverage(matches, required),
        "prompt_contexts": prompt_context_status,
        "models": len(prompts),
        "matches": compact_matches,
        "prompts": prompts,
        "rules": {
            "rule_version": "PRED_INVEST_CREDIT_SURVIVE_V2",
            "forecast_required": True,
            "investment_optional": True,
            "credit_controls_loan": True,
            "repay_before_ranking": True,
            "top5_daily_reward": True,
            "bottom3_penalty": True,
            "forced_debt_when_cash_insufficient": True,
        },
    }


def markdown_prompt_pack(pack: dict[str, Any]) -> str:
    lines = [
        f"# PRED-INVEST-CREDIT-SURVIVE V2 Prompt Pack · {pack['date']} · {pack['round_id']}",
        "",
        f"- 模型：{pack['models']}",
        f"- 比赛：{pack['match_count']}",
        f"- 规则：先结算/偿债/排名，再发起全赛事预测与投资；下注可 no-bet，贷款由信用控制。",
        "",
        "## 今日比赛",
        "",
    ]
    for match in pack["matches"]:
        lines.append(f"- {match.get('match_id')} · {match.get('home_team')} vs {match.get('away_team')} · {match.get('kickoff_at')}")
    lines += ["", "## 每席提示词摘要", ""]
    for item in pack["prompts"]:
        terms = item["loan_terms"]
        lines.append(
            f"- {item['display_name']}：信用 {terms['credit_grade']} / {terms['credit_score']}，净资产 {gp(terms['net_worth_gp'])}，可新增贷款 {gp(terms['available_loan_gp'])}。"
        )
    lines += ["", "## 完整提示词", ""]
    for item in pack["prompts"]:
        lines.extend([f"### {item['display_name']}", "", "```text", item["prompt"].strip(), "```", ""])
    return "\n".join(lines)


def write_outputs(pack: dict[str, Any], out_dir: pathlib.Path = OUT_DIR) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{pack['date']}_{pack['round_id']}_prompt_pack"
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown_prompt_pack(pack) + "\n", encoding="utf-8")
    (out_dir / "latest_prompt_pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "latest_prompt_pack.md").write_text(markdown_prompt_pack(pack) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PRED-INVEST-CREDIT-SURVIVE V2 prompt pack")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    pack = build_prompt_pack(args.date, args.round_id, args.base_url)
    if args.write:
        paths = write_outputs(pack)
        print(json.dumps({"ok": True, "paths": paths, "models": pack["models"], "matches": pack["match_count"]}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(pack, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
