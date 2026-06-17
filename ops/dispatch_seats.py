#!/usr/bin/env python3
"""Dispatch isolated AI Judge web-seat runs under the PRED-INVEST contract."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pool.io_utils import write_json
from run_pred_invest_single_seat_reruns import (
    DEFAULT_TARGET_SEATS,
    _parse_list,
    _wait_for_bridge_idle,
    _wait_for_verdict,
)
from submit_pred_invest_bridge_run import submit


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"


TRANSIENT_BRIDGE_ERRORS = {
    "curl_non_json_response",
    "non_json_response",
    "URLError",
    "ConnectionError",
    "TimeoutError",
}


def _transient_bridge_submit_error(receipt: dict[str, Any], response: dict[str, Any]) -> bool:
    error = str(receipt.get("error") or response.get("error") or "")
    raw = str(response.get("raw") or "")
    message = str(response.get("message") or "")
    if error in TRANSIENT_BRIDGE_ERRORS:
        return True
    lower_blob = f"{raw}\n{message}".lower()
    return any(
        marker in lower_blob
        for marker in (
            "failed to connect",
            "connection refused",
            "not found",
            "temporarily unavailable",
            "service unavailable",
            "gateway timeout",
            "method not allowed",
            "<!doctype html>",
        )
    )


class SeatDispatcher:
    """Submit each requested seat with bounded retries and a JSON audit trail."""

    def __init__(self, bridge_base_url: str = "http://127.0.0.1:8501") -> None:
        self.bridge_base_url = bridge_base_url.rstrip("/")

    def dispatch(
        self,
        *,
        date: str,
        round_id: str,
        seats: list[str] | None = None,
        attempt_no: int = 1,
        retries: int = 1,
        judge_mode: str = "strategic",
        verdict_timeout_seconds: float = 720.0,
        poll_seconds: float = 8.0,
        bridge_wait_seconds: float = 0.0,
        dry_run: bool = False,
        write: bool = False,
    ) -> dict[str, Any]:
        requested = seats or list(DEFAULT_TARGET_SEATS)
        rows: list[dict[str, Any]] = []
        run_ids: list[str] = []
        for seat in requested:
            row: dict[str, Any] = {"seat": seat, "attempts": [], "status": "pending"}
            for retry_index in range(max(1, retries + 1)):
                bridge_wait: dict[str, Any] | None = None
                if not dry_run and bridge_wait_seconds > 0:
                    bridge_wait = _wait_for_bridge_idle(
                        self.bridge_base_url,
                        recover_after=900.0,
                        wait_seconds=bridge_wait_seconds,
                    )
                receipt = submit(
                    self.bridge_base_url,
                    date,
                    round_id,
                    dry_run=dry_run,
                    requested_seats=[seat],
                    compact=True,
                    ultra_compact=False,
                    attempt_no=attempt_no + retry_index,
                    judge_mode=judge_mode,
                    assume_requested_ready=True,
                )
                response = receipt.get("response") if isinstance(receipt.get("response"), dict) else {}
                run_id = response.get("run_id")
                attempt = {
                    "retry_index": retry_index,
                    "ok": bool(receipt.get("ok") and (run_id or dry_run)),
                    "run_id": run_id,
                    "error": receipt.get("error") or response.get("error"),
                    "prompt_chars": receipt.get("prompt_chars"),
                }
                if bridge_wait is not None:
                    attempt["bridge_wait"] = {
                        "ok": bridge_wait.get("ok"),
                        "recovered": bridge_wait.get("recovered"),
                        "error": bridge_wait.get("error"),
                        "status_error": (bridge_wait.get("status") or {}).get("error")
                        if isinstance(bridge_wait.get("status"), dict)
                        else None,
                    }
                    if not bridge_wait.get("ok"):
                        attempt["bridge_wait_warning"] = "submit_attempted_after_bridge_wait_failure"
                if response.get("status") is not None:
                    attempt["response_status"] = response.get("status")
                if response.get("curl_returncode") is not None:
                    attempt["curl_returncode"] = response.get("curl_returncode")
                if response.get("raw"):
                    attempt["response_raw"] = str(response.get("raw"))[:500]
                if run_id and not dry_run:
                    wait = _wait_for_verdict(
                        self.bridge_base_url,
                        str(run_id),
                        timeout_seconds=verdict_timeout_seconds,
                        poll_seconds=poll_seconds,
                    )
                    attempt["wait_ok"] = bool(wait.get("ok"))
                    attempt["wait_error"] = wait.get("error")
                    if wait.get("ok"):
                        row["status"] = "submitted"
                        run_ids.append(str(run_id))
                        row["attempts"].append(attempt)
                        break
                elif dry_run and receipt.get("ok"):
                    row["status"] = "dry_run"
                    row["attempts"].append(attempt)
                    break
                row["attempts"].append(attempt)
                if (
                    not dry_run
                    and retry_index < retries
                    and _transient_bridge_submit_error(receipt, response)
                ):
                    time.sleep(8)
            if row["status"] == "pending":
                row["status"] = "failed"
            rows.append(row)
        report = {
            "version": "pred_invest_seat_dispatch.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "date": date,
            "round_id": round_id,
            "bridge_base_url": self.bridge_base_url,
            "requested_seats": requested,
            "run_ids": run_ids,
            "rows": rows,
            "ok": all(row["status"] in {"submitted", "dry_run"} for row in rows),
            "dry_run": dry_run,
        }
        if write:
            write_json(OUT_DIR / f"{date}_{round_id}_seat_dispatch.json", report)
            write_json(OUT_DIR / "latest_seat_dispatch.json", report)
        return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dispatch PRED-INVEST seats through local AI Judge")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--seats", default=",".join(DEFAULT_TARGET_SEATS))
    parser.add_argument("--bridge-base-url", default="http://127.0.0.1:8501")
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--judge-mode", default="strategic")
    parser.add_argument("--verdict-timeout-seconds", type=float, default=720.0)
    parser.add_argument("--poll-seconds", type=float, default=8.0)
    parser.add_argument("--bridge-wait-seconds", type=float, default=45.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    report = SeatDispatcher(args.bridge_base_url).dispatch(
        date=args.date,
        round_id=args.round_id,
        seats=_parse_list(args.seats),
        attempt_no=args.attempt,
        retries=args.retries,
        judge_mode=args.judge_mode,
        verdict_timeout_seconds=args.verdict_timeout_seconds,
        poll_seconds=args.poll_seconds,
        bridge_wait_seconds=args.bridge_wait_seconds,
        dry_run=args.dry_run,
        write=args.write,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
