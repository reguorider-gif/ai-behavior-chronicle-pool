#!/usr/bin/env python3
"""Full-cycle PRED-INVEST automation facade.

The automation has two explicit phases:

- pre-match: sync schedule/odds, build prompt pack, optionally dispatch seats.
- post-match: sync scores, settle, compile behavior memory and chronicle.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from dispatch_seats import SeatDispatcher
from fetch_odds import OddsFetcher
from run_pred_invest_daily_sop import main as run_daily_sop


ROOT = Path(__file__).resolve().parents[1]
PRED_DIR = ROOT / "data" / "pool" / "pred_invest"


def _read_daily_report(date: str, round_id: str) -> dict[str, Any]:
    path = PRED_DIR / f"{date}_{round_id}_daily_sop.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


class AutoSOP:
    def __init__(self, base_url: str = "https://pool-app-one.vercel.app", bridge_base_url: str = "http://127.0.0.1:8501") -> None:
        self.base_url = base_url.rstrip("/")
        self.bridge_base_url = bridge_base_url.rstrip("/")
        self.fetcher = OddsFetcher()
        self.dispatcher = SeatDispatcher(self.bridge_base_url)

    def _daily_sop(self, date: str, round_id: str, *, write: bool, runs: list[str] | None = None) -> dict[str, Any]:
        argv = [
            "--date",
            date,
            "--round",
            round_id,
            "--base-url",
            self.base_url,
            "--bridge-base-url",
            self.bridge_base_url,
        ]
        if runs:
            argv.extend(["--runs", ",".join(runs)])
        if write:
            argv.append("--write")
        code = run_daily_sop(argv)
        report = _read_daily_report(date, round_id)
        hard_errors = report.get("errors") or []
        process_ok = code == 0 or (report.get("verdict") == "PARTIAL_NOT_READY" and not hard_errors)
        return {
            "return_code": code,
            "ok": process_ok,
            "verdict": report.get("verdict"),
            "errors": hard_errors,
            "warnings": report.get("warnings") or [],
            "publish_ready": report.get("verdict") == "READY",
        }

    def phase_pre_match(
        self,
        date: str,
        round_id: str,
        *,
        write: bool = False,
        dispatch: bool = False,
        dry_run: bool = False,
        seats: list[str] | None = None,
    ) -> dict[str, Any]:
        sync = self.fetcher.sync_all(date, round_id, self.base_url, write=write)
        dispatch_report: dict[str, Any] = {"skipped": True, "reason": "dispatch flag not set"}
        if dispatch:
            dispatch_report = self.dispatcher.dispatch(
                date=date,
                round_id=round_id,
                seats=seats,
                dry_run=dry_run,
                write=write,
            )
        sop = self._daily_sop(date, round_id, write=write, runs=dispatch_report.get("run_ids") or [])
        sync_ok = bool(sync.get("ok"))
        score_blocking = bool((sync.get("score_sync") or {}).get("blocking_pending_score_count"))
        if dry_run and not sync_ok and bool((sync.get("odds") or {}).get("ok")) and score_blocking:
            sync_ok = True
            sync.setdefault("warnings", []).append("score_blocking_softened_for_dry_run")
        return {
            "phase": "pre_match",
            "ok": sync_ok and bool(sop.get("ok")) and (dispatch_report.get("ok", True) or dispatch_report.get("skipped")),
            "sync": sync,
            "dispatch": dispatch_report,
            "daily_sop": sop,
        }

    def phase_post_match(self, date: str, round_id: str, *, write: bool = False, runs: list[str] | None = None) -> dict[str, Any]:
        sync = self.fetcher.sync_all(date, round_id, self.base_url, write=write)
        sop = self._daily_sop(date, round_id, write=write, runs=runs)
        return {
            "phase": "post_match",
            "ok": bool(sop.get("ok")),
            "sync": sync,
            "daily_sop": sop,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run automated PRED-INVEST SOP phases")
    parser.add_argument("phase", nargs="?", choices=["pre", "post", "dry-run", "auto", "full"])
    parser.add_argument("--phase", dest="phase_flag", choices=["pre", "post", "dry-run", "auto", "full"])
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--base-url", default="https://pool-app-one.vercel.app")
    parser.add_argument("--bridge-base-url", default="http://127.0.0.1:8501")
    parser.add_argument("--seats", default="")
    parser.add_argument("--runs", default="")
    parser.add_argument("--dispatch", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Compatibility flag equivalent to phase=dry-run for pre-match.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    seats = [item.strip().lower() for item in args.seats.split(",") if item.strip()]
    runs = [item.strip() for item in args.runs.split(",") if item.strip()]
    sop = AutoSOP(args.base_url, args.bridge_base_url)
    phase = args.phase_flag or args.phase or ("dry-run" if args.dry_run else "pre")
    if phase == "post":
        report = sop.phase_post_match(args.date, args.round_id, write=args.write, runs=runs)
    elif phase in {"auto", "full"}:
        pre_report = sop.phase_pre_match(
            args.date,
            args.round_id,
            write=args.write,
            dispatch=args.dispatch,
            dry_run=args.dry_run,
            seats=seats,
        )
        post_report = sop.phase_post_match(args.date, args.round_id, write=args.write, runs=runs)
        report = {
            "phase": phase,
            "ok": bool(pre_report.get("ok")) and bool(post_report.get("ok")),
            "pre_match": pre_report,
            "post_match": post_report,
        }
    else:
        report = sop.phase_pre_match(
            args.date,
            args.round_id,
            write=args.write and phase != "dry-run" and not args.dry_run,
            dispatch=args.dispatch,
            dry_run=phase == "dry-run" or args.dry_run,
            seats=seats,
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
