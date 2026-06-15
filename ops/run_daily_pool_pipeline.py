#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pool.behavior_journal import append_god_event, append_seat_event, update_seat_summary, write_seat_run
from pool.credit_engine import calculate_loan_limit, write_credit_ledger
from pool.god_report_v2 import generate_god_report
from pool.io_utils import now_iso, read_json, write_json
from pool.paths import DATA_ROOT, FIXTURE_ROOT
from pool.prompt_context_builder import build_market_snapshot, build_prompt_context
from pool.rules_engine import RULE_VERSION, validate_forecast_receipt, validate_investment_receipt, validate_no_cross_seat_leakage
from pool.survival_engine import calculate_net_worth, detect_recovery_mode, write_survival_ledger


def _fixture_output_name(run_id: str) -> str:
    lower = run_id.lower()
    if lower.endswith("-a") or lower.endswith("_a"):
        return "model_outputs_run_a.json"
    if lower.endswith("-b") or lower.endswith("_b"):
        return "model_outputs_run_b.json"
    return "model_outputs.json"


def _load_fixture(run_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    root = FIXTURE_ROOT / "smoke_behavior_v2"
    matches = read_json(root / "matches.json", [])
    seats = read_json(root / "seats.json", [])
    outputs = read_json(root / _fixture_output_name(run_id), {"seats": {}})
    results = read_json(root / f"results_{run_id}.json", {})
    if not results and (root / "results_run_a.json").exists() and (run_id.endswith("-a") or run_id.endswith("_a")):
        results = read_json(root / "results_run_a.json", {})
    return matches, seats, outputs, results


def _account_map(seats: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    accounts = {}
    for row in seats:
        seat_id = str(row.get("seat_id"))
        account = dict(row.get("account") or {})
        account.setdefault("balance_gp", 1000)
        account.setdefault("outstanding_loan_gp", account.get("loan_gp", 0))
        account.setdefault("accrued_interest_gp", 0)
        account["net_worth_gp"] = calculate_net_worth(account.get("balance_gp"), account.get("outstanding_loan_gp"), account.get("accrued_interest_gp"))
        accounts[seat_id] = account
    return accounts


def _market_odds(matches: list[dict[str, Any]], match_id: str, market: str, selection: str) -> float:
    for match in matches:
        if match.get("match_id") != match_id:
            continue
        for row in match.get("markets") or []:
            if row.get("market") == market and row.get("selection") == selection:
                try:
                    return float(row.get("odds"))
                except Exception:
                    return 1.0
    return 1.0


def _normalize_token(value: Any) -> str:
    import re
    import unicodedata

    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("&", "and").replace("ç", "c").replace("Ç", "C")
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def _score_parts(row: dict[str, Any]) -> tuple[int, int] | None:
    home = row.get("home_score")
    away = row.get("away_score")
    if home is None or away is None:
        score = str(row.get("score") or "").replace("–", "-")
        if "-" not in score:
            return None
        left, right = score.split("-", 1)
        home, away = left.strip(), right.strip()
    try:
        return int(home), int(away)
    except Exception:
        return None


def _result_outcome(score: str) -> str:
    left, right = score.replace("–", "-").split("-", 1)
    home = int(left.strip())
    away = int(right.strip())
    if home > away:
        return "home"
    if away > home:
        return "away"
    return "draw"


def _result_rows_from_matches(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert /api/matches-style rows with explicit scores into result rows.

    This is the settlement trigger bridge: score sync writes into the match
    registry, /api/matches exposes the merged rows, and settlement must be able
    to consume those rows directly instead of waiting for a separate results
    fixture/file.
    """
    rows: list[dict[str, Any]] = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        scores = _score_parts(match)
        if scores is None:
            continue
        status = str(match.get("status") or match.get("result_state") or "").casefold()
        if status and status not in {"settled", "finished", "done", "closed", "complete", "completed", "ft"}:
            # Explicit scores win, but avoid settling rows that declare a live
            # or cancelled state.
            if status in {"live", "in_play", "running", "cancelled", "postponed"}:
                continue
        home, away = scores
        score = f"{home}-{away}"
        rows.append({
            "match_id": match.get("match_id"),
            "home_team": match.get("home_team") or match.get("home"),
            "away_team": match.get("away_team") or match.get("away"),
            "score": score,
            "home_score": home,
            "away_score": away,
            "outcome": _result_outcome(score),
            "status": "settled",
            "result_state": "finished",
            "kickoff_at": match.get("kickoff_at"),
            "source": match.get("score_source") or match.get("source") or "matches_api_score_registry",
            "score_registry_applied": bool(match.get("score_registry_applied")),
        })
    return rows


def _merge_results_with_matches(results: dict[str, Any], matches: list[dict[str, Any]]) -> dict[str, Any]:
    by_id: dict[str, dict[str, Any]] = {}
    for row in results.get("matches", []) if isinstance(results.get("matches"), list) else []:
        if isinstance(row, dict) and row.get("match_id"):
            by_id[str(row["match_id"])] = row
    for row in _result_rows_from_matches(matches):
        if row.get("match_id") and str(row["match_id"]) not in by_id:
            by_id[str(row["match_id"])] = row
    return {
        "version": "pipeline_results_from_explicit_scores.v1",
        "source_policy": "explicit_result_file_plus_matches_api_score_registry",
        "matches": sorted(by_id.values(), key=lambda item: str(item.get("kickoff_at") or item.get("match_id") or "")),
    }


def _match_by_id(matches: list[dict[str, Any]], match_id: Any) -> dict[str, Any]:
    target = str(match_id or "")
    for match in matches:
        if str(match.get("match_id") or "") == target:
            return match
    return {}


def _selection_to_outcome(selection: Any, match: dict[str, Any]) -> str:
    token = _normalize_token(selection)
    if token in {"home", "h", "1", "homewin", "teamhome"}:
        return "home"
    if token in {"away", "a", "2", "awaywin", "teamaway"}:
        return "away"
    if token in {"draw", "tie", "x", "d"}:
        return "draw"
    if token and token == _normalize_token(match.get("home_team") or match.get("home")):
        return "home"
    if token and token == _normalize_token(match.get("away_team") or match.get("away")):
        return "away"
    return ""


def _line_value(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    text = str(value).strip().replace("−", "-")
    try:
        return float(text)
    except Exception:
        return 0.0


def _asian_line_parts(line: float) -> list[float]:
    doubled = round(line * 2)
    if abs(line * 2 - doubled) < 1e-9:
        return [line]
    lower = (int(line * 2) / 2.0)
    if line < 0 and abs(line * 2 - int(line * 2)) > 1e-9:
        lower = ((int(line * 2) - 1) / 2.0)
    upper = lower + 0.5
    return [lower, upper]


def _handicap_profit(stake: float, odds: float, selected_score: int, other_score: int, line: float) -> tuple[float, str]:
    parts = _asian_line_parts(line)
    part_stake = stake / len(parts)
    profit = 0.0
    states: list[str] = []
    for part in parts:
        adjusted = selected_score + part - other_score
        if adjusted > 1e-9:
            profit += part_stake * (odds - 1)
            states.append("win")
        elif adjusted < -1e-9:
            profit -= part_stake
            states.append("lose")
        else:
            states.append("push")
    unique = set(states)
    if unique == {"win"}:
        status = "win"
    elif unique == {"lose"}:
        status = "lose"
    elif unique == {"push"}:
        status = "push"
    elif "win" in unique and "push" in unique:
        status = "half_win"
    elif "lose" in unique and "push" in unique:
        status = "half_lose"
    else:
        status = "mixed"
    return profit, status


def _settle_bet(item: dict[str, Any], result: dict[str, Any], match: dict[str, Any], fallback_odds: float) -> dict[str, Any]:
    scores = _score_parts(result)
    if scores is None:
        return {"status": "unsettled", "profit_gp": 0.0, "payout_gp": 0.0}
    home_score, away_score = scores
    stake = float(item.get("stake_gp") or 0)
    odds = float(item.get("odds") or fallback_odds or 1.0)
    market = str(item.get("market") or "").casefold()
    selection = item.get("selection")
    profit = 0.0
    status = "lose"

    if market in {"h2h", "moneyline", "1x2"}:
        selected = _selection_to_outcome(selection, match)
        actual = result.get("outcome") or _result_outcome(f"{home_score}-{away_score}")
        status = "win" if selected == actual else "lose"
        profit = stake * (odds - 1) if status == "win" else -stake
    elif "handicap" in market or "spread" in market:
        selected = _selection_to_outcome(selection, match)
        line = _line_value(item.get("line"))
        if selected == "home":
            profit, status = _handicap_profit(stake, odds, home_score, away_score, line)
        elif selected == "away":
            profit, status = _handicap_profit(stake, odds, away_score, home_score, line)
        else:
            status = "unsettled"
            profit = 0.0
    elif "total" in market or "over" in market or "under" in market:
        total = home_score + away_score
        line = _line_value(item.get("line"))
        token = _normalize_token(selection or item.get("side"))
        if token.startswith("over") or token in {"o", "big", "大"}:
            status = "win" if total > line else ("push" if abs(total - line) < 1e-9 else "lose")
        elif token.startswith("under") or token in {"u", "small", "小"}:
            status = "win" if total < line else ("push" if abs(total - line) < 1e-9 else "lose")
        else:
            status = "unsettled"
        profit = stake * (odds - 1) if status == "win" else (-stake if status == "lose" else 0.0)
    else:
        status = "unsettled"

    payout = stake + profit if status not in {"unsettled"} else 0.0
    return {"status": status, "profit_gp": round(profit, 2), "payout_gp": round(payout, 2)}


def _settle(run_id: str, matches: list[dict[str, Any]], results: dict[str, Any], investment_receipts: dict[str, Any]) -> dict[str, Any]:
    results = _merge_results_with_matches(results, matches)
    result_by_match = {row.get("match_id"): row for row in results.get("matches", []) if isinstance(row, dict)}
    seats = {}
    settlement_rows = []
    settled_bets = 0
    winning_bets = 0
    losing_bets = 0
    push_bets = 0
    total_stake = 0.0
    total_payout = 0.0
    total_profit = 0.0
    for seat_id, receipt in (investment_receipts.get("seats") or {}).items():
        profit = 0.0
        settled = []
        for item in receipt.get("investments") or []:
            if item.get("action") != "bet":
                settled.append({"match_id": item.get("match_id"), "action": "no_bet", "profit_gp": 0})
                continue
            result = result_by_match.get(item.get("match_id"))
            if not result:
                continue
            match = _match_by_id(matches, item.get("match_id"))
            odds = item.get("odds") or _market_odds(matches, item.get("match_id"), item.get("market"), item.get("selection"))
            stake = float(item.get("stake_gp") or 0)
            outcome = _settle_bet(item, result, match, float(odds or 1.0))
            item_profit = float(outcome["profit_gp"])
            profit += item_profit
            total_stake += stake
            total_payout += float(outcome["payout_gp"])
            total_profit += item_profit
            settled_bets += 1
            if outcome["status"] in {"win", "half_win"}:
                winning_bets += 1
            elif outcome["status"] in {"lose", "half_lose"}:
                losing_bets += 1
            elif outcome["status"] == "push":
                push_bets += 1
            row = {
                "seat_id": seat_id,
                "match_id": item.get("match_id"),
                "market": item.get("market"),
                "selection": item.get("selection"),
                "line": item.get("line"),
                "odds": float(odds or 1.0),
                "stake_gp": round(stake, 2),
                "loan_used_gp": round(float(item.get("loan_used_gp") or 0), 2),
                "payout_gp": outcome["payout_gp"],
                "profit_gp": round(item_profit, 2),
                "status": outcome["status"],
                "score": result.get("score"),
            }
            settled.append(row)
            settlement_rows.append(row)
        seats[seat_id] = {"seat_id": seat_id, "run_id": run_id, "profit_gp": round(profit, 2), "settled": settled}
    payload = {
        "run_id": run_id,
        "settlement_status": "settled" if settled_bets else "pending_match_results",
        "matches": results.get("matches", []),
        "settlements": settlement_rows,
        "seats": seats,
        "summary": {
            "settled_bets": settled_bets,
            "winning_bets": winning_bets,
            "losing_bets": losing_bets,
            "push_bets": push_bets,
            "total_stake_gp": round(total_stake, 2),
            "total_payout_gp": round(total_payout, 2),
            "total_profit_gp": round(total_profit, 2),
            "roi": round(total_profit / total_stake, 4) if total_stake else 0,
            "result_source_policy": results.get("source_policy"),
        },
    }
    write_json(DATA_ROOT / "settlements" / f"{run_id}.json", payload)
    write_json(DATA_ROOT / "match_results" / f"{run_id}.json", results)
    return payload


def _loan_used_by_seat(investment_receipts: dict[str, Any]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for seat_id, receipt in (investment_receipts.get("seats") or {}).items():
        total = 0.0
        for item in receipt.get("investments") or []:
            if item.get("action") == "bet":
                total += float(item.get("loan_used_gp") or 0)
        totals[str(seat_id)] = round(total, 2)
    return totals


def _apply_settlement_to_accounts(
    accounts: dict[str, dict[str, Any]],
    settlement: dict[str, Any] | None,
    investment_receipts: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Apply post-match settlement, then repay debt before ranking snapshots."""
    if not settlement:
        return {}
    loan_used = _loan_used_by_seat(investment_receipts)
    updates: dict[str, dict[str, Any]] = {}
    for seat_id, account in accounts.items():
        row = (settlement.get("seats") or {}).get(seat_id, {})
        profit = float(row.get("profit_gp") or 0)
        new_loan = float(loan_used.get(seat_id, 0))
        balance_before = float(account.get("balance_gp") or 0)
        outstanding_before = float(account.get("outstanding_loan_gp") or account.get("loan_gp") or 0)
        accrued_before = float(account.get("accrued_interest_gp") or 0)

        balance = balance_before + new_loan + profit
        outstanding = outstanding_before + new_loan
        terms = calculate_loan_limit(seat_id, calculate_net_worth(balance_before, outstanding_before, accrued_before))
        interest_rate = terms.get("interest_rate")
        interest_due = round(outstanding * float(interest_rate or 0), 2) if interest_rate is not None else 0.0
        accrued = accrued_before + interest_due

        interest_paid = min(max(balance, 0.0), accrued)
        balance -= interest_paid
        accrued -= interest_paid
        principal_paid = min(max(balance, 0.0), outstanding)
        balance -= principal_paid
        outstanding -= principal_paid
        net_worth = calculate_net_worth(balance, outstanding, accrued)

        account.update({
            "balance_gp": round(balance, 2),
            "outstanding_loan_gp": round(outstanding, 2),
            "loan_gp": round(outstanding, 2),
            "accrued_interest_gp": round(accrued, 2),
            "net_worth_gp": net_worth,
        })
        updates[seat_id] = {
            "seat_id": seat_id,
            "run_id": settlement.get("run_id"),
            "balance_before_gp": round(balance_before, 2),
            "settlement_profit_gp": round(profit, 2),
            "new_loan_used_gp": round(new_loan, 2),
            "interest_due_gp": round(interest_due, 2),
            "interest_paid_gp": round(interest_paid, 2),
            "principal_repaid_gp": round(principal_paid, 2),
            "balance_after_debt_service_gp": round(balance, 2),
            "outstanding_loan_gp": round(outstanding, 2),
            "accrued_interest_gp": round(accrued, 2),
            "net_worth_gp": net_worth,
            "ranking_basis": "net_worth_after_settlement_interest_and_principal_repayment",
        }
    settlement["account_updates"] = updates
    write_json(DATA_ROOT / "settlements" / f"{settlement.get('run_id')}.json", settlement)
    return updates


def _write_behavior_summary(args: argparse.Namespace, summary: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    run_id = args.round
    forecast_path = DATA_ROOT / "forecast_receipts" / f"{run_id}.json"
    investment_path = DATA_ROOT / "investment_receipts" / f"{run_id}.json"
    prompt_dir = DATA_ROOT / "prompt_contexts" / run_id
    seat_journal_dir = DATA_ROOT / "seat_journals"
    prompt_count = len(list(prompt_dir.glob("*.json"))) if prompt_dir.exists() else 0
    journal_count = len([path for path in seat_journal_dir.glob("*/summary.json") if path.parent.name != "unit_journal_alpha"]) if seat_journal_dir.exists() else 0
    god_report_json = DATA_ROOT / "god_reports" / f"{args.date}_{run_id}.json"
    god_report_md = DATA_ROOT / "god_reports" / f"{args.date}_{run_id}.md"
    behavior = {
        "ok": bool(summary.get("ok")),
        "generated_at": now_iso(),
        "date": args.date,
        "run_id": run_id,
        "rule_version": args.rule_version,
        "operational_mode": summary.get("operational_mode"),
        "surface_policy": summary.get("surface_policy"),
        "public_frontend_contract": {
            "rule_version_label": f"规则版本：{args.rule_version}",
            "seat_journal_label": "行为日志：可查看",
            "credit_ledger_label": "信用账本：可查看",
            "forecast_investment_label": "预测/投资分账：可查看",
            "no_bet_label": "no-bet：合法动作",
            "recovery_label": "Recovery Mode：已接入",
        },
        "features": [
            "Seat Journal",
            "Credit",
            "Loan Limit",
            "Recovery Mode",
            "forecast_receipts",
            "investment_receipts",
            "no-bet",
            "god_report_v2",
        ],
        "counts": {
            "seat_count": summary.get("seat_count", 0),
            "required_match_count": summary.get("required_match_count", 0),
            "forecast_receipt_count": summary.get("forecast_receipt_count", 0),
            "investment_receipt_count": summary.get("investment_receipt_count", 0),
            "prompt_context_count": prompt_count,
            "seat_journal_count": journal_count,
            "god_report_seat_count": report.get("seat_count", 0),
            "god_report_event_count": report.get("event_count", 0),
        },
        "separation": {
            "forecast_receipts_exists": forecast_path.exists(),
            "investment_receipts_exists": investment_path.exists(),
            "forecast_and_investment_are_separate": forecast_path.exists() and investment_path.exists() and forecast_path != investment_path,
        },
        "artifact_refs": {
            "seat_journals": "data/pool/seat_journals/",
            "prompt_contexts": f"data/pool/prompt_contexts/{run_id}/",
            "forecast_receipts": f"data/pool/forecast_receipts/{run_id}.json",
            "investment_receipts": f"data/pool/investment_receipts/{run_id}.json",
            "credit_ledger": f"data/pool/credit_ledger/{run_id}.json",
            "survival_ledger": f"data/pool/survival_ledger/{run_id}.json",
            "god_ledger": f"data/pool/god_ledger/runs/{run_id}.json",
            "god_report_v2_json": f"data/pool/god_reports/{args.date}_{run_id}.json",
            "god_report_v2_md": f"data/pool/god_reports/{args.date}_{run_id}.md",
            "pipeline_smoke": f"data/pool/pipeline_smoke/{args.date}_{run_id}.json",
            "behavior_summary": "data/pool/behavior_summary/latest.json",
        },
        "readiness": {
            "god_report_v2_generated": god_report_json.exists() and god_report_md.exists(),
            "behavior_summary_readable": True,
            "public_frontend_minimum_markers": [
                f"规则版本：{args.rule_version}",
                "行为日志：可查看",
                "信用账本：可查看",
                "预测/投资分账：可查看",
            ],
        },
    }
    write_json(DATA_ROOT / "behavior_summary" / f"{args.date}_{run_id}.json", behavior)
    write_json(DATA_ROOT / "behavior_summary" / "latest.json", behavior)
    md_lines = [
        f"# Behavior Summary - {args.date} {run_id}",
        "",
        f"- 规则版本：{args.rule_version}",
        "- 行为日志：可查看",
        "- 信用账本：可查看",
        "- 预测/投资分账：可查看",
        "- no-bet：合法动作",
        "- Recovery Mode：已接入",
        f"- forecast_receipts：{behavior['counts']['forecast_receipt_count']}",
        f"- investment_receipts：{behavior['counts']['investment_receipt_count']}",
        f"- prompt_contexts：{behavior['counts']['prompt_context_count']}",
        f"- seat_journals：{behavior['counts']['seat_journal_count']}",
        f"- god_report_v2：{'generated' if behavior['readiness']['god_report_v2_generated'] else 'missing'}",
    ]
    md_path = DATA_ROOT / "behavior_summary" / "latest.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return behavior


def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    if args.odds_provider != "fixture":
        raise ValueError("This implementation currently supports --odds-provider fixture for deterministic smoke runs.")
    matches, seats, outputs, results = _load_fixture(args.round)
    accounts = _account_map(seats)
    seat_ids = [str(row.get("seat_id")) for row in seats]
    required_match_ids = [str(match.get("match_id")) for match in matches]

    market_snapshot = build_market_snapshot(args.date, args.round, matches) if args.build_market_snapshot else {"matches": matches}
    leak_results = {}
    for seat_id in seat_ids:
        context = build_prompt_context(
            args.date,
            args.round,
            seat_id,
            args.rule_version,
            accounts=accounts,
            matches=matches,
            market_snapshot=market_snapshot,
        )
        leak_results[seat_id] = validate_no_cross_seat_leakage(context, seat_id, seat_ids)

    forecast_receipts = {"run_id": args.round, "rule_version": args.rule_version, "seats": {}}
    investment_receipts = {"run_id": args.round, "rule_version": args.rule_version, "seats": {}}
    validation = {"forecasts": {}, "investments": {}, "leakage": leak_results}

    for seat_id in seat_ids:
        receipt = (outputs.get("seats") or {}).get(seat_id)
        if not isinstance(receipt, dict):
            validation["forecasts"][seat_id] = {"ok": False, "errors": ["missing_model_output"]}
            validation["investments"][seat_id] = {"ok": False, "errors": ["missing_model_output"]}
            continue
        account = accounts[seat_id]
        net_worth = float(account.get("net_worth_gp") or 0)
        recovery_mode = detect_recovery_mode(seat_id, account)
        loan_terms = calculate_loan_limit(seat_id, net_worth)
        forecast_check = validate_forecast_receipt(receipt, required_match_ids, args.rule_version)
        investment_check = validate_investment_receipt(
            receipt,
            required_match_ids,
            loan_limit_gp=float(loan_terms.get("loan_limit_gp") or 0),
            recovery_mode=recovery_mode,
            net_worth_gp=net_worth,
            rule_version=args.rule_version,
        )
        validation["forecasts"][seat_id] = forecast_check
        validation["investments"][seat_id] = investment_check
        if forecast_check["ok"]:
            forecast_receipts["seats"][seat_id] = {
                "seat_id": seat_id,
                "forecasts": receipt.get("forecasts") or [],
                "self_review": receipt.get("self_review") or {},
            }
        if investment_check["ok"]:
            investment_receipts["seats"][seat_id] = {
                "seat_id": seat_id,
                "investments": receipt.get("investments") or [],
                "loan_decision": receipt.get("loan_decision") or {},
                "survival_plan": receipt.get("survival_plan") or {},
            }
        if args.write_seat_journals:
            append_seat_event(seat_id, {"event_type": "self_review_recorded", "run_id": args.round, "self_review": receipt.get("self_review") or {}})
            append_seat_event(seat_id, {"event_type": "forecast_recorded", "run_id": args.round, "forecasts": receipt.get("forecasts") or []})
            append_seat_event(seat_id, {"event_type": "investment_recorded", "run_id": args.round, "investments": receipt.get("investments") or []})
            write_seat_run(seat_id, args.round, {"receipt": receipt, "validation": {"forecast": forecast_check, "investment": investment_check}})
        if args.write_god_ledger:
            append_god_event({
                "event_type": "seat_receipt_validated",
                "run_id": args.round,
                "seat_id": seat_id,
                "forecast_ok": forecast_check["ok"],
                "investment_ok": investment_check["ok"],
                "investment_warnings": investment_check.get("warnings", []),
            })

    write_json(DATA_ROOT / "forecast_receipts" / f"{args.round}.json", forecast_receipts)
    write_json(DATA_ROOT / "investment_receipts" / f"{args.round}.json", investment_receipts)

    settlement = None
    account_updates = {}
    settlement_results = _merge_results_with_matches(results, matches)
    if settlement_results.get("matches"):
        settlement = _settle(args.round, matches, settlement_results, investment_receipts)
        account_updates = _apply_settlement_to_accounts(accounts, settlement, investment_receipts)
        for seat_id, row in (settlement.get("seats") or {}).items():
            append_seat_event(seat_id, {"event_type": "settlement_recorded", "run_id": args.round, "settlement": row})
            if seat_id in account_updates:
                append_seat_event(seat_id, {"event_type": "debt_service_recorded", "run_id": args.round, **account_updates[seat_id]})
            if args.write_god_ledger:
                append_god_event({"event_type": "settlement_recorded", "run_id": args.round, "seat_id": seat_id, "profit_gp": row.get("profit_gp")})
                if seat_id in account_updates:
                    append_god_event({"event_type": "debt_service_recorded", "run_id": args.round, "seat_id": seat_id, **account_updates[seat_id]})
    survival = write_survival_ledger(args.round, accounts)
    credit = write_credit_ledger(args.round, seat_ids)
    for seat_id, row in (credit.get("seats") or {}).items():
        append_seat_event(seat_id, {"event_type": "credit_updated", "run_id": args.round, **row})
        append_seat_event(seat_id, {
            "event_type": "account_snapshot",
            "run_id": args.round,
            "balance_gp": accounts[seat_id].get("balance_gp"),
            "outstanding_loan_gp": accounts[seat_id].get("outstanding_loan_gp"),
            "accrued_interest_gp": accounts[seat_id].get("accrued_interest_gp"),
            "net_worth_gp": accounts[seat_id].get("net_worth_gp"),
        })
        update_seat_summary(seat_id, args.round)
    report = generate_god_report(args.date, args.round)
    ok = all(row.get("ok") for row in validation["forecasts"].values()) and all(row.get("ok") for row in validation["investments"].values()) and all(row.get("ok") for row in leak_results.values())
    summary = {
        "ok": ok,
        "generated_at": now_iso(),
        "date": args.date,
        "run_id": args.round,
        "rule_version": args.rule_version,
        "operational_mode": "daily_product_sop",
        "surface_policy": "public_frontend_shows_results_logs_health_only",
        "daily_sequence": [
            "settle_finished_matches_before_new_predictions",
            "repay_debt_before_ranking",
            "apply_rewards_and_penalties",
            "collect_forecasts_for_all_matches",
            "collect_investment_rows_for_all_matches",
            "quality_gate_before_publish",
        ],
        "seat_count": len(seat_ids),
        "required_match_count": len(required_match_ids),
        "forecast_receipt_count": len(forecast_receipts["seats"]),
        "investment_receipt_count": len(investment_receipts["seats"]),
        "settlement_written": bool(settlement),
        "settlement_status": settlement.get("settlement_status") if settlement else "pending_match_results",
        "settled_bets": (settlement.get("summary") or {}).get("settled_bets") if settlement else 0,
        "account_updates_written": len(account_updates),
        "survival_ledger_seats": len(survival.get("seats") or {}),
        "god_report": str(DATA_ROOT / "god_reports" / f"{args.date}_{args.round}.md"),
        "validation": validation,
    }
    write_json(DATA_ROOT / "pipeline_smoke" / f"{args.date}_{args.round}.json", summary)
    _write_behavior_summary(args, summary, report)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", required=True)
    parser.add_argument("--odds-provider", default="fixture")
    parser.add_argument("--rule-version", default=RULE_VERSION)
    parser.add_argument("--with-behavior-memory", action="store_true")
    parser.add_argument("--require-forecast", action="store_true")
    parser.add_argument("--allow-no-bet", action="store_true")
    parser.add_argument("--build-market-snapshot", action="store_true")
    parser.add_argument("--write-god-ledger", action="store_true")
    parser.add_argument("--write-seat-journals", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    print(json.dumps(run_pipeline(parse_args()), ensure_ascii=False, indent=2))
