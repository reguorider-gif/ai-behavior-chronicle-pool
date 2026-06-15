#!/usr/bin/env python3
"""SOP wrapper for Observer Ledger generation."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_observer_ledger import BASE_URL, build_observer_ledger, write_outputs  # noqa: E402


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Observer Ledger SOP step")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--phase", choices=["auto", "pre", "post"], default="auto")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    ledger = build_observer_ledger(args.date, args.round_id, args.phase, args.base_url)
    seat_count = len(ledger.get("seat_commentaries") or [])
    settled_bets = int((ledger.get("scoreboard") or {}).get("settled_bets") or 0)
    accepted_bets = int((ledger.get("scoreboard") or {}).get("accepted_bets") or 0)
    errors: list[str] = []
    warnings: list[str] = []

    if seat_count == 0:
        errors.append("observer_ledger_no_seat_commentaries")
    if accepted_bets == 0:
        warnings.append("observer_ledger_no_accepted_bets")
    if ledger.get("phase") == "post" and settled_bets == 0:
        errors.append("observer_ledger_post_without_settled_bets")
    if ledger.get("phase") == "pre" and ledger.get("settlement_status") == "settled":
        warnings.append("observer_ledger_pre_requested_for_settled_round")

    paths = write_outputs(ledger) if args.write else {}
    result = {
        "ok": not errors,
        "date": args.date,
        "round_id": args.round_id,
        "phase": ledger.get("phase"),
        "settlement_status": ledger.get("settlement_status"),
        "seat_commentaries": seat_count,
        "accepted_bets": accepted_bets,
        "settled_bets": settled_bets,
        "errors": errors,
        "warnings": warnings,
        "paths": paths,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
