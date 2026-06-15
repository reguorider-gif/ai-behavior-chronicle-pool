#!/usr/bin/env python3
"""Synchronize verified PRED-INVEST match scores into match_results artifacts.

The scorer is intentionally conservative: it only imports rows that already
carry an explicit score in the match-data alignment audit. Missing scores are
written to a backfill queue instead of being guessed from model forecasts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from pred_invest_schedule_overrides import apply_schedule_override, score_due_after_grace


ROOT = Path(__file__).resolve().parents[1]
POOL_DIR = ROOT / "data" / "pool"
PRED_DIR = POOL_DIR / "pred_invest"
MATCH_RESULTS_DIR = POOL_DIR / "match_results"
THE_ODDS_SPORT_KEY = "soccer_fifa_world_cup"
THE_ODDS_CONFIG_PATH = Path.home() / ".config" / "ai-judge" / "the_odds_api_key"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_team(value: Any) -> str:
    text = str(value or "").casefold()
    text = text.replace("&", "and")
    text = text.replace("ç", "c")
    text = text.replace("curaçao", "curacao")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def parse_utc(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value)
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def hk_date_from_utc(value: Any) -> str:
    instant = parse_utc(value)
    if not instant:
        return ""
    return (instant + timedelta(hours=8)).date().isoformat()


def the_odds_api_key() -> str:
    env = os.environ.get("THE_ODDS_API_KEY") or os.environ.get("ODDS_API_KEY")
    if env:
        return env.strip()
    if THE_ODDS_CONFIG_PATH.exists():
        return THE_ODDS_CONFIG_PATH.read_text(encoding="utf-8").strip()
    return ""


def fetch_the_odds_scores(days_from: int = 3) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    key = the_odds_api_key()
    meta = {
        "source": "the_odds_api_scores",
        "sport_key": THE_ODDS_SPORT_KEY,
        "configured": bool(key),
        "ok": False,
        "error": None,
        "row_count": 0,
    }
    if not key:
        meta["error"] = "the_odds_api_key_missing"
        return [], meta
    url = (
        f"https://api.the-odds-api.com/v4/sports/{THE_ODDS_SPORT_KEY}/scores/"
        f"?daysFrom={int(days_from)}&apiKey={key}"
    )
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8", errors="replace")
        data = json.loads(payload)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        meta["error"] = f"HTTP {exc.code}: {raw[:300]}"
        return [], meta
    except Exception as exc:
        meta["error"] = f"{type(exc).__name__}: {exc}"
        return [], meta
    if not isinstance(data, list):
        meta["error"] = "unexpected_scores_payload"
        return [], meta
    rows = [row for row in data if isinstance(row, dict)]
    meta.update({"ok": True, "row_count": len(rows), "last_updates": sorted({str(row.get("last_update")) for row in rows if row.get("last_update")})[-3:]})
    return rows, meta


def local_match_candidates(alignment: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in alignment.get("rows") or []:
        if isinstance(row, dict):
            rows.append(row)
    for path in sorted(PRED_DIR.glob("*_prompt_pack.json")) + sorted(PRED_DIR.glob("*_current_game.json")):
        data = read_json(path, {}) or {}
        for match in data.get("matches") or []:
            if isinstance(match, dict):
                item = apply_schedule_override(dict(match))
                item.setdefault("artifact_source", path.name)
                rows.append(item)
    required = read_json(PRED_DIR / "required_matches.json", {}) or {}
    for match in required.get("matches") or []:
        if isinstance(match, dict):
            item = apply_schedule_override(dict(match))
            item.setdefault("artifact_source", "required_matches.json")
            rows.append(item)
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        row = apply_schedule_override(row)
        match_id = str(row.get("match_id") or row.get("id") or "").strip()
        if not match_id:
            continue
        by_id.setdefault(match_id, row)
    return list(by_id.values())


def candidate_key(row: dict[str, Any]) -> tuple[str, str]:
    return (
        normalize_team(row.get("home") or row.get("home_team")),
        normalize_team(row.get("away") or row.get("away_team")),
    )


def provider_score(row: dict[str, Any]) -> str:
    scores = row.get("scores")
    if not isinstance(scores, list):
        return ""
    by_team = {normalize_team(item.get("name")): str(item.get("score") or "") for item in scores if isinstance(item, dict)}
    home = by_team.get(normalize_team(row.get("home_team")))
    away = by_team.get(normalize_team(row.get("away_team")))
    if home is None or away is None:
        return ""
    try:
        return f"{int(home)}-{int(away)}"
    except Exception:
        return ""


def provider_rows(alignment: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    scores, meta = fetch_the_odds_scores()
    candidates = local_match_candidates(alignment)
    by_pair: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        key = candidate_key(row)
        if all(key):
            by_pair[key].append(row)
    settled: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc)
    for event in scores:
        key = (normalize_team(event.get("home_team")), normalize_team(event.get("away_team")))
        local = (by_pair.get(key) or [None])[0]
        if not local:
            continue
        completed = bool(event.get("completed"))
        score = provider_score(event)
        kickoff = event.get("commence_time") or local.get("kickoff_at")
        base = {
            "match_id": local.get("match_id") or local.get("id"),
            "home": local.get("home") or local.get("home_team") or event.get("home_team"),
            "away": local.get("away") or local.get("away_team") or event.get("away_team"),
            "home_team": local.get("home_team") or local.get("home") or event.get("home_team"),
            "away_team": local.get("away_team") or local.get("away") or event.get("away_team"),
            "kickoff_at": kickoff,
            "matchday_hk": hk_date_from_utc(kickoff) or local.get("matchday_hk"),
            "date_query": local.get("date_query") or local.get("date") or hk_date_from_utc(kickoff),
            "provider_event_id": event.get("id"),
            "provider_last_update": event.get("last_update"),
            "provider_completed": completed,
        }
        if completed and score:
            settled.append({**base, "score": score, "status": "settled", "result_state": "finished", "source": "the_odds_api_scores"})
            continue
        kickoff_dt = parse_utc(kickoff)
        blocking = bool(kickoff_dt and kickoff_dt < now - timedelta(hours=2) and not completed)
        pending.append({
            **base,
            "status": "scheduled",
            "result_state": "awaiting_provider_final",
            "gap": "provider_not_completed" if not blocking else "provider_score_overdue_after_kickoff",
            "blocking": blocking,
        })
    meta["mapped_settled_count"] = len(settled)
    meta["mapped_pending_count"] = len(pending)
    return settled, pending, meta


def normalize_score(value: Any) -> str:
    score = str(value or "").replace("–", "-").strip()
    if "-" not in score:
        return ""
    left, right = score.split("-", 1)
    try:
        return f"{int(left.strip())}-{int(right.strip())}"
    except Exception:
        return ""


def outcome_from_score(score: str) -> str:
    normalized = normalize_score(score)
    if not normalized:
        return "unknown"
    left, right = normalized.split("-", 1)
    home = int(left)
    away = int(right)
    if home > away:
        return "home"
    if away > home:
        return "away"
    return "draw"


def unique_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        match_id = str(row.get("match_id") or row.get("id") or "").strip()
        if not match_id or match_id in seen:
            continue
        seen.add(match_id)
        result.append(row)
    return result


def result_entry(row: dict[str, Any]) -> dict[str, Any]:
    score = normalize_score(row.get("score"))
    home_score, away_score = score.split("-", 1)
    return {
        "match_id": row.get("match_id"),
        "home_team": row.get("home") or row.get("home_team"),
        "away_team": row.get("away") or row.get("away_team"),
        "score": score,
        "home_score": int(home_score),
        "away_score": int(away_score),
        "outcome": outcome_from_score(score),
        "status": "settled",
        "result_state": "finished",
        "kickoff_at": row.get("kickoff_at"),
        "matchday_hk": row.get("matchday_hk"),
        "source": row.get("source") or "match_data_alignment_audit",
        "source_date_query": row.get("date_query"),
        "provider_event_id": row.get("provider_event_id"),
        "provider_last_update": row.get("provider_last_update"),
    }


def pending_entry(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_id": row.get("match_id"),
        "home_team": row.get("home") or row.get("home_team"),
        "away_team": row.get("away") or row.get("away_team"),
        "status": row.get("status"),
        "result_state": row.get("result_state"),
        "kickoff_at": row.get("kickoff_at"),
        "matchday_hk": row.get("matchday_hk"),
        "date_query": row.get("date_query"),
        "reason": row.get("gap") or "score_missing_after_due",
        "blocking": bool(row.get("blocking", True)),
        "provider_event_id": row.get("provider_event_id"),
        "provider_completed": row.get("provider_completed"),
        "required_next_action": "fetch_score_from_trusted_source_or_manual_admin_backfill_before_settlement",
    }


def merge_match_results(path: Path, new_rows: list[dict[str, Any]]) -> dict[str, Any]:
    existing = read_json(path, {"matches": []}) or {"matches": []}
    existing_rows = existing.get("matches") if isinstance(existing.get("matches"), list) else []
    by_id = {
        str(row.get("match_id")): row
        for row in existing_rows
        if isinstance(row, dict) and row.get("match_id")
    }
    for row in new_rows:
        if row.get("match_id"):
            by_id[str(row["match_id"])] = row
    merged = {
        "version": "pred_invest_match_results.v1",
        "generated_at": now_iso(),
        "source_policy": "verified_scores_only_no_forecast_scores",
        "matches": sorted(by_id.values(), key=lambda item: str(item.get("kickoff_at") or item.get("match_id") or "")),
    }
    return merged


def build_sync(alignment_path: Path | None = None) -> dict[str, Any]:
    alignment_path = alignment_path or (PRED_DIR / "latest_match_data_alignment_audit.json")
    alignment = read_json(alignment_path, {}) or {}
    all_rows = [apply_schedule_override(row) for row in alignment.get("rows") or [] if isinstance(row, dict)]
    scored = unique_rows([row for row in all_rows if normalize_score(row.get("score"))])
    pending_source = alignment.get("score_missing_after_due")
    if not isinstance(pending_source, list):
        pending_source = [row for row in all_rows if row.get("gap") == "score_missing_after_due"]
    pending_source = [
        apply_schedule_override(row)
        for row in pending_source
        if isinstance(row, dict) and score_due_after_grace(apply_schedule_override(row))
    ]
    provider_scored, provider_pending, provider_meta = provider_rows(alignment)
    scored_by_id: dict[str, dict[str, Any]] = {}
    for row in scored + provider_scored:
        match_id = str(row.get("match_id") or row.get("id") or "")
        if match_id:
            scored_by_id[match_id] = row
    if not provider_meta.get("ok"):
        previous = read_json(MATCH_RESULTS_DIR / "latest_known_scores.json", {}) or {}
        for row in previous.get("matches") or []:
            if not isinstance(row, dict):
                continue
            match_id = str(row.get("match_id") or "")
            if match_id and match_id not in scored_by_id:
                carried = dict(row)
                carried.setdefault("source", row.get("source") or "previous_known_scores_carried_forward")
                carried["carried_forward_due_to_source_error"] = provider_meta.get("error")
                scored_by_id[match_id] = carried
    pending_by_id: dict[str, dict[str, Any]] = {}
    for row in [item for item in pending_source if isinstance(item, dict)] + provider_pending:
        match_id = str(row.get("match_id") or row.get("id") or "")
        if match_id and match_id not in scored_by_id:
            pending_by_id[match_id] = row
    result_rows = [result_entry(row) for row in scored_by_id.values()]
    pending_rows = [pending_entry(row) for row in pending_by_id.values()]

    by_output_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in scored_by_id.values():
        entry = result_entry(raw)
        for key in (raw.get("date_query"), raw.get("matchday_hk"), hk_date_from_utc(raw.get("kickoff_at"))):
            if key:
                by_output_date[str(key)].append(entry)

    return {
        "version": "pred_invest_score_sync.v1",
        "generated_at": now_iso(),
        "alignment_path": str(alignment_path),
        "source_policy": "import_only_rows_with_explicit_score; never_use_model_forecast_as_result",
        "known_score_count": len(result_rows),
        "pending_score_count": len(pending_rows),
        "known_scores": result_rows,
        "pending_score_backfill": pending_rows,
        "blocking_pending_score_count": sum(1 for row in pending_rows if row.get("blocking", True)),
        "external_score_source": provider_meta,
        "output_dates": sorted(by_output_date),
        "by_output_date": by_output_date,
    }


def write_sync(sync: dict[str, Any]) -> dict[str, str]:
    MATCH_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    for date, rows in (sync.get("by_output_date") or {}).items():
        path = MATCH_RESULTS_DIR / f"{date}.json"
        merged = merge_match_results(path, rows)
        write_json(path, merged)
        paths[f"match_results:{date}"] = str(path)

    known_path = MATCH_RESULTS_DIR / "latest_known_scores.json"
    pending_path = MATCH_RESULTS_DIR / "pending_score_backfill.json"
    write_json(known_path, {
        "version": "pred_invest_known_scores.v1",
        "generated_at": sync["generated_at"],
        "source_policy": sync["source_policy"],
        "matches": sync.get("known_scores") or [],
    })
    write_json(pending_path, {
        "version": "pred_invest_pending_score_backfill.v1",
        "generated_at": sync["generated_at"],
        "source_policy": sync["source_policy"],
        "matches": sync.get("pending_score_backfill") or [],
    })
    paths["latest_known_scores"] = str(known_path)
    paths["pending_score_backfill"] = str(pending_path)

    json_path = PRED_DIR / "latest_score_sync.json"
    md_path = PRED_DIR / "latest_score_sync.md"
    serializable = {k: v for k, v in sync.items() if k != "by_output_date"}
    serializable["paths"] = paths
    write_json(json_path, serializable)
    lines = [
        "# PRED-INVEST Score Sync",
        "",
        f"- generated_at: {sync['generated_at']}",
        f"- known scores imported: {sync['known_score_count']}",
        f"- pending score backfill: {sync['pending_score_count']}",
        f"- blocking pending scores: {sync.get('blocking_pending_score_count', 0)}",
        f"- external source: {json.dumps(sync.get('external_score_source') or {}, ensure_ascii=False)}",
        f"- policy: {sync['source_policy']}",
        "",
        "## Known Scores",
        "",
    ]
    for row in sync.get("known_scores") or []:
        lines.append(f"- {row['match_id']} · {row.get('home_team')} vs {row.get('away_team')} · {row['score']}")
    lines += ["", "## Pending Backfill", ""]
    pending = sync.get("pending_score_backfill") or []
    if pending:
        for row in pending:
            lines.append(f"- {row['match_id']} · {row.get('home_team')} vs {row.get('away_team')} · {row.get('kickoff_at')} · {row['required_next_action']}")
    else:
        lines.append("- none")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths["score_sync_json"] = str(json_path)
    paths["score_sync_markdown"] = str(md_path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alignment", default=str(PRED_DIR / "latest_match_data_alignment_audit.json"))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    sync = build_sync(Path(args.alignment))
    if args.write:
        sync["paths"] = write_sync(sync)
    print(json.dumps({k: v for k, v in sync.items() if k != "by_output_date"}, ensure_ascii=False, indent=2))
    return 0 if not sync.get("blocking_pending_score_count") else 2


if __name__ == "__main__":
    raise SystemExit(main())
