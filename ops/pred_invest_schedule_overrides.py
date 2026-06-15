#!/usr/bin/env python3
"""Shared fixture corrections for PRED-INVEST daily SOP.

These overrides correct schedule metadata only. They must never be used to
invent scores or settle matches.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
OVERRIDES_PATH = OUT_DIR / "schedule_overrides.json"


def _read_overrides() -> dict[str, Any]:
    if not OVERRIDES_PATH.exists():
        return {}
    try:
        data = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    matches = data.get("matches") if isinstance(data, dict) else {}
    return matches if isinstance(matches, dict) else {}


def apply_schedule_override(row: dict[str, Any]) -> dict[str, Any]:
    match_id = str(row.get("match_id") or row.get("id") or "").strip()
    if not match_id:
        return row
    override = _read_overrides().get(match_id)
    if not isinstance(override, dict):
        return row
    merged = dict(row)
    for key in ("date", "kickoff_at", "matchday_hk", "home_team", "away_team"):
        if override.get(key):
            merged[key] = override[key]
    # Alignment rows often use home/away while product rows use home_team/away_team.
    if override.get("home_team"):
        merged["home"] = override["home_team"]
    if override.get("away_team"):
        merged["away"] = override["away_team"]
    merged["schedule_override_applied"] = True
    merged["schedule_override_source_note"] = override.get("source_note")
    if not merged.get("status"):
        merged["status"] = "scheduled"
    return merged


def apply_schedule_overrides(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [apply_schedule_override(row) for row in rows]


def parse_utc(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def score_due_after_grace(row: dict[str, Any], *, now: datetime | None = None, grace_hours: int = 2) -> bool:
    kickoff = parse_utc(row.get("kickoff_at"))
    if not kickoff:
        return bool(row.get("score_due"))
    now = now or datetime.now(timezone.utc)
    return kickoff < now - timedelta(hours=grace_hours)
