#!/usr/bin/env python3
"""Shadow-rerun existing pool bets under PRED-INVEST-CREDIT-SURVIVE V2.

This tool does not invent new model answers. It audits the latest structured
receipts against the new forecast/investment/credit contract and produces the
betting-method report needed before the real AI Judge rerun.
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
from collections import defaultdict
from typing import Any

from pred_invest_quality_gate import REQUIRED_SEATS
from pred_invest_rules import evaluate_investment, gp, loan_terms


BASE_URL = "https://pool-app-one.vercel.app"
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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


def api_url(base_url: str, path: str, **query: str) -> str:
    encoded = urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    return f"{base_url.rstrip('/')}{path}" + (f"?{encoded}" if encoded else "")


def key(row: dict[str, Any]) -> str:
    raw = str(row.get("seat_id") or row.get("model_account") or row.get("model") or "").lower()
    return "grok" if raw == "xai" else raw


def display(row: dict[str, Any], account: str) -> str:
    return str(row.get("display_name") or row.get("seat_name") or row.get("model_name") or account)


def n(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def set_missing(row: dict[str, Any], key_name: str, value: Any) -> None:
    if row.get(key_name) in (None, ""):
        row[key_name] = value


def load_context(base_url: str, date: str, round_id: str) -> dict[str, Any]:
    try:
        runtime = fetch_json(api_url(base_url, "/api/pool/runtime-summary", date=date, round_id=round_id))
    except RuntimeError as exc:
        from pool_data import get_runtime_summary

        runtime = get_runtime_summary(round_id=round_id, date=date)
        runtime["source_warning"] = f"runtime_summary_api_unavailable_using_local_artifact:{exc}"
    try:
        receipts = fetch_json(api_url(base_url, f"/api/pool/bet-receipts/{round_id}"))
    except RuntimeError as exc:
        receipts = {
            "missing": True,
            "missing_reason": "bet_receipts_not_available_for_round",
            "error": str(exc),
            "accepted_bets": [],
            "missing_models": [],
        }
    archives = {}
    try:
        archives = fetch_json(api_url(base_url, f"/api/pool/seat-archives/{round_id}"))
    except RuntimeError:
        archives = {}
    daily = {}
    try:
        daily = fetch_json(api_url(base_url, f"/api/pool/daily-reports/{date}/{round_id}"))
    except RuntimeError:
        daily = {}
    return {"runtime": runtime, "receipts": receipts, "daily": daily, "archives": archives}


def account_map(runtime: dict[str, Any], archives: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in runtime.get("current_ranking") or []:
        if isinstance(row, dict) and key(row):
            result[key(row)] = row
    for row in (archives or {}).get("seats") or []:
        if isinstance(row, dict) and key(row):
            result[key(row)] = {**result.get(key(row), {}), **row}
    for row in runtime.get("active_models") or []:
        if isinstance(row, dict) and key(row) and key(row) not in result:
            result[key(row)] = row
    canonical: dict[str, dict[str, Any]] = {}
    for index, seat in enumerate(REQUIRED_SEATS, start=1):
        row = dict(result.get(seat) or {})
        set_missing(row, "seat_id", seat)
        set_missing(row, "model_account", MODEL_ACCOUNT_BY_SEAT.get(seat, seat))
        set_missing(row, "display_name", SEAT_DISPLAY_NAMES.get(seat, seat))
        set_missing(row, "rank", row.get("computed_rank") or index)
        set_missing(row, "computed_rank", row.get("rank") or index)
        set_missing(row, "balance_gp", row.get("confirmed_current_balance_gp") or 1000)
        set_missing(row, "confirmed_current_balance_gp", row.get("balance_gp") or 1000)
        set_missing(row, "loan_gp", row.get("remaining_loan_gp") or 0)
        set_missing(row, "remaining_loan_gp", row.get("loan_gp") or 0)
        if seat not in result:
            row["account_source"] = "required_seat_placeholder"
            row["status_label"] = "待补跑/待同步"
        canonical[seat] = row
    return canonical


def parse_board_id(board_id: Any) -> dict[str, Any]:
    text = str(board_id or "")
    parts = text.split("_")
    parsed: dict[str, Any] = {}
    if len(parts) >= 3:
        parsed["market"] = parts[2]
    if len(parts) >= 4:
        parsed["selection"] = parts[3]
    return parsed


def normalize_bet(raw: dict[str, Any], account: str) -> dict[str, Any]:
    board = parse_board_id(raw.get("board_id"))
    loan_used = raw.get("loan_used_gp")
    if loan_used is None:
        loan_used = raw.get("loan_gp") or raw.get("borrowed_gp") or 0
    stake = raw.get("stake_gp") or raw.get("stake") or raw.get("amount_gp") or raw.get("amount") or 0
    odds = raw.get("odds") or raw.get("price") or raw.get("decimal_odds")
    return {
        "model_account": account,
        "match_id": raw.get("match_id") or raw.get("event_id"),
        "selection": raw.get("selection") or raw.get("pick") or raw.get("team") or board.get("selection"),
        "market": raw.get("market") or board.get("market"),
        "line": raw.get("line"),
        "odds": odds,
        "stake_gp": stake,
        "loan_used_gp": loan_used,
        "model_prob": raw.get("model_prob") or raw.get("probability"),
        "market_implied_prob": raw.get("market_implied_prob") or (1 / n(odds, 1) if n(odds, 1) else None),
        "estimated_ev": raw.get("estimated_ev"),
        "rationale": raw.get("rationale") or raw.get("reason") or "",
    }


def flatten_receipts(receipts: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    bets_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    missing: list[str] = []
    seen_bets: set[tuple[Any, ...]] = set()

    def add_bet(raw: dict[str, Any], account: str) -> None:
        bet = normalize_bet(raw, account)
        signature = (
            account,
            bet.get("match_id"),
            bet.get("selection"),
            bet.get("market"),
            str(bet.get("line")),
            str(bet.get("odds")),
            str(bet.get("stake_gp")),
        )
        if signature in seen_bets:
            return
        seen_bets.add(signature)
        bets_by_model[account].append(bet)

    for field in ("missing_models", "unavailable_seats"):
        value = receipts.get(field)
        if isinstance(value, list):
            missing.extend(str(item) for item in value)

    top_bets = receipts.get("accepted_bets")
    if isinstance(top_bets, list):
        for raw in top_bets:
            if isinstance(raw, dict):
                account = key(raw)
                if account:
                    add_bet(raw, account)

    receipt_rows: list[Any] = []
    for field in ("accepted_receipts", "receipts", "model_receipts", "items"):
        value = receipts.get(field)
        if isinstance(value, list):
            receipt_rows.extend(value)

    for receipt in receipt_rows:
        if not isinstance(receipt, dict):
            continue
        account = key(receipt)
        if not account:
            continue
        status = str(receipt.get("status") or "").lower()
        if status and "accepted" not in status and "ok" not in status and "valid" not in status:
            if account not in missing:
                missing.append(account)
        payload = receipt.get("receipt") if isinstance(receipt.get("receipt"), dict) else receipt
        authoritative_fields = ("bet_ledger",) if isinstance(payload.get("bet_ledger"), list) else ("accepted_bets", "investments", "bets")
        for field in authoritative_fields:
            rows = payload.get(field)
            if isinstance(rows, list):
                for raw in rows:
                    if isinstance(raw, dict):
                        add_bet(raw, account)
    return bets_by_model, sorted(set(missing))


def audit_model(account: str, account_row: dict[str, Any], bets: list[dict[str, Any]]) -> dict[str, Any]:
    terms = loan_terms(account_row)
    audits = []
    allowed = warned = rejected = 0
    for bet in bets:
        result = evaluate_investment(bet, account_row)
        audits.append({"bet": bet, "audit": result})
        status = result["status"]
        if status == "allowed":
            allowed += 1
        elif "rejected" in status or "over_limit" in status:
            rejected += 1
        else:
            warned += 1
    if not bets:
        stance = "必须补 forecast；投资可 no-bet，但不能缺席判断。"
    elif rejected:
        stance = "现有投注在新规则下存在贷款/授信硬冲突，真实重跑必须降杠杆或 no-bet。"
    elif warned:
        stance = "现有投注可作为投资方向参考，但需要按赔率仓位上限降额。"
    else:
        stance = "现有投注在新规则下可进入投资账本，但仍需补全 forecast 概率校准字段。"
    return {
        "model_account": account,
        "display_name": display(account_row, account),
        "rank": account_row.get("rank") or account_row.get("computed_rank"),
        "loan_terms": terms,
        "bet_count": len(bets),
        "allowed": allowed,
        "warned": warned,
        "rejected": rejected,
        "audits": audits,
        "required_next_action": stance,
    }


def build_shadow_report(date: str, round_id: str, base_url: str = BASE_URL) -> dict[str, Any]:
    ctx = load_context(base_url, date, round_id)
    runtime = ctx["runtime"]
    receipts = ctx["receipts"]
    archives = ctx["archives"]
    accounts = account_map(runtime, archives)
    bets_by_model, missing = flatten_receipts(receipts)
    rows = []
    for account, account_row in sorted(accounts.items(), key=lambda item: int(item[1].get("rank") or item[1].get("computed_rank") or 99)):
        rows.append(audit_model(account, account_row, bets_by_model.get(account, [])))
    total_bets = sum(row["bet_count"] for row in rows)
    return {
        "version": "pred_invest_shadow_rerun.v2",
        "generated_at": now_iso(),
        "source_base_url": base_url,
        "date": date,
        "round_id": round_id,
        "runtime_version": runtime.get("version"),
        "current_round": runtime.get("current_round"),
        "receipt_version": receipts.get("version"),
        "receipt_missing": bool(receipts.get("missing")),
        "receipt_missing_reason": receipts.get("missing_reason"),
        "models": len(rows),
        "total_existing_bets": total_bets,
        "missing_or_unavailable_models": missing,
        "summary": {
            "allowed": sum(row["allowed"] for row in rows),
            "warned": sum(row["warned"] for row in rows),
            "rejected": sum(row["rejected"] for row in rows),
            "models_without_bets": sum(1 for row in rows if row["bet_count"] == 0),
        },
        "models_detail": rows,
        "rule_interpretation": {
            "forecast_required": "所有模型、所有当日比赛必须先预测；缺下注不等于缺判断。",
            "investment_optional": "下注只在存在 edge 时进行；no-bet 是合法动作。",
            "credit_controls_loan": "信用分和净资产决定新增贷款额度，当前无 forecast ledger 时使用保守 proxy。",
            "repay_before_ranking": "每次结算先还息还本，再进入投资榜排名。",
        },
    }


def markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        f"# PRED-INVEST-CREDIT-SURVIVE V2 Shadow Rerun · {report['date']} · {report['round_id']}",
        "",
        "## 总览",
        "",
        f"- 模型：{report['models']}",
        f"- 现有结构化投注：{report['total_existing_bets']}",
        f"- 新规则允许：{s['allowed']}",
        f"- 需要降额/补字段：{s['warned']}",
        f"- 贷款/授信冲突：{s['rejected']}",
        f"- 无投注模型：{s['models_without_bets']}",
        f"- 缺席/不可用：{', '.join(report['missing_or_unavailable_models']) or '无'}",
        "",
        "## 新规则投注方式",
        "",
        "| 席位 | 信用 | 净资产 | 可贷款 | 现有下注 | 结论 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in report["models_detail"]:
        terms = row["loan_terms"]
        lines.append(
            "| {name} | {grade}/{score} | {nw} | {loan} | {bets} | {action} |".format(
                name=row["display_name"],
                grade=terms["credit_grade"],
                score=terms["credit_score"],
                nw=gp(terms["net_worth_gp"]),
                loan=gp(terms["available_loan_gp"]),
                bets=row["bet_count"],
                action=row["required_next_action"].replace("|", "/"),
            )
        )
    lines += ["", "## 逐席审计", ""]
    for row in report["models_detail"]:
        terms = row["loan_terms"]
        lines.extend(
            [
                f"### {row['display_name']}",
                "",
                f"- 信用/贷款：{terms['credit_grade']} / {terms['credit_score']}；净资产 {gp(terms['net_worth_gp'])}；可新增贷款 {gp(terms['available_loan_gp'])}。",
                f"- 投注方式：{row['required_next_action']}",
            ]
        )
        for item in row["audits"][:4]:
            bet = item["bet"]
            audit = item["audit"]
            warnings = "；".join(audit["warnings"]) or "无"
            lines.append(
                f"- {bet.get('match_id') or 'match'} · {bet.get('selection') or 'selection'} {bet.get('market') or ''} @ {bet.get('odds') or '—'} · stake {gp(bet.get('stake_gp'))}：{audit['status']}；{warnings}"
            )
        if not row["audits"]:
            lines.append("- 无结构化下注：下一轮仍必须提交全量 forecast，可选择 no-bet。")
        lines.append("")
    return "\n".join(lines)


def write_outputs(report: dict[str, Any], out_dir: pathlib.Path = OUT_DIR) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{report['date']}_{report['round_id']}_shadow_rerun"
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report) + "\n", encoding="utf-8")
    (out_dir / "latest_shadow_rerun.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "latest_shadow_rerun.md").write_text(markdown(report) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit latest bets under PRED-INVEST-CREDIT-SURVIVE V2")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    report = build_shadow_report(args.date, args.round_id, args.base_url)
    if args.write:
        paths = write_outputs(report)
        print(json.dumps({"ok": True, "paths": paths, "summary": report["summary"], "total_existing_bets": report["total_existing_bets"]}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
