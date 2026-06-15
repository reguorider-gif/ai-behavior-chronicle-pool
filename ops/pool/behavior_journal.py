from __future__ import annotations

from collections import Counter
from typing import Any

from .io_utils import append_jsonl, now_iso, read_jsonl, write_json
from .paths import DATA_ROOT


def _seat_dir(seat_id: str):
    return DATA_ROOT / "seat_journals" / seat_id


def append_seat_event(seat_id: str, event: dict[str, Any]) -> dict[str, Any]:
    row = {"ts": now_iso(), "seat_id": seat_id, **event}
    append_jsonl(_seat_dir(seat_id) / "journal.jsonl", row)
    return row


def load_recent_seat_events(seat_id: str, limit: int = 20) -> list[dict[str, Any]]:
    return read_jsonl(_seat_dir(seat_id) / "journal.jsonl")[-limit:]


def load_seat_summary(seat_id: str) -> dict[str, Any]:
    path = _seat_dir(seat_id) / "summary.json"
    if not path.exists():
        return {
            "seat_id": seat_id,
            "runs_seen": [],
            "credit_score": 600,
            "credit_grade": "B",
            "balance_gp": 1000,
            "outstanding_loan_gp": 0,
            "accrued_interest_gp": 0,
            "net_worth_gp": 1000,
            "recovery_mode": False
        }
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def update_seat_summary(seat_id: str, run_id: str) -> dict[str, Any]:
    events = read_jsonl(_seat_dir(seat_id) / "journal.jsonl")
    runs = sorted({str(event.get("run_id")) for event in events if event.get("run_id")})
    latest: dict[str, Any] = {}
    for event in events:
        if event.get("event_type") in {
            "account_snapshot",
            "credit_updated",
            "survival_updated",
            "settlement_recorded",
            "self_review_recorded"
        }:
            latest.update(event)
    summary = {
        "seat_id": seat_id,
        "updated_at": now_iso(),
        "last_run_id": run_id,
        "runs_seen": runs,
        "event_counts": dict(Counter(str(event.get("event_type") or "unknown") for event in events)),
        "recent_events": events[-8:],
        "last_self_review": latest.get("self_review") or latest.get("review") or {},
        "last_forecasts": latest.get("forecasts") or [],
        "last_investments": latest.get("investments") or [],
        "last_settlement": latest.get("settlement") or {},
        "credit_score": latest.get("credit_score", 600),
        "credit_grade": latest.get("credit_grade", "B"),
        "credit_delta": latest.get("credit_delta", 0),
        "balance_gp": latest.get("balance_gp", 1000),
        "outstanding_loan_gp": latest.get("outstanding_loan_gp", 0),
        "accrued_interest_gp": latest.get("accrued_interest_gp", 0),
        "net_worth_gp": latest.get("net_worth_gp", 1000),
        "recovery_mode": bool(latest.get("recovery_mode", False)),
        "strategy_drift_note": latest.get("strategy_change_this_round") or latest.get("strategy_note") or ""
    }
    write_json(_seat_dir(seat_id) / "summary.json", summary)
    return summary


def write_seat_run(seat_id: str, run_id: str, payload: dict[str, Any]) -> str:
    path = _seat_dir(seat_id) / "runs" / f"{run_id}.json"
    write_json(path, {"seat_id": seat_id, "run_id": run_id, **payload})
    return str(path)


def append_god_event(event: dict[str, Any]) -> dict[str, Any]:
    row = {"ts": now_iso(), **event}
    append_jsonl(DATA_ROOT / "god_ledger" / "events.jsonl", row)
    return row


def build_god_run_summary(run_id: str) -> dict[str, Any]:
    events = [event for event in read_jsonl(DATA_ROOT / "god_ledger" / "events.jsonl") if event.get("run_id") == run_id]
    seats = sorted({str(event.get("seat_id")) for event in events if event.get("seat_id")})
    summary = {
        "run_id": run_id,
        "generated_at": now_iso(),
        "event_count": len(events),
        "seats": seats,
        "event_counts": dict(Counter(str(event.get("event_type") or "unknown") for event in events)),
        "events": events
    }
    write_json(DATA_ROOT / "god_ledger" / "runs" / f"{run_id}.json", summary)
    return summary
