#!/usr/bin/env python3
"""Synchronize verified PRED-INVEST match scores into match_results artifacts.

The scorer is intentionally conservative: it only imports rows that already
carry an explicit score in the match-data alignment audit. Missing scores are
written to a backfill queue instead of being guessed from model forecasts.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from fetch_odds import PRED_DIR, POOL_DIR, hk_date_from_utc, local_match_candidates, provider_rows
from pool.io_utils import now_iso, read_json, write_json
from pred_invest_schedule_overrides import apply_schedule_override, score_due_after_grace


MATCH_RESULTS_DIR = POOL_DIR / "match_results"
MANUAL_BACKFILL_PATH = MATCH_RESULTS_DIR / "manual_trusted_backfill.json"


def manual_backfill_rows() -> list[dict[str, Any]]:
    """Load operator-entered scores with explicit source attribution.

    This is a conservative fallback for days when the scores provider is
    temporarily unreachable. It is intentionally separate from schedule
    overrides so fixture corrections cannot silently become match results.
    """

    payload = read_json(MANUAL_BACKFILL_PATH, {}) or {}
    rows = payload.get("matches") if isinstance(payload, dict) else []
    if not isinstance(rows, list):
        return []
    result: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        score = normalize_score(row.get("score"))
        match_id = str(row.get("match_id") or "").strip()
        source_url = str(row.get("source_url") or "").strip()
        if not match_id or not score or not source_url:
            continue
        result.append(
            {
                **row,
                "match_id": match_id,
                "score": score,
                "status": "settled",
                "result_state": "finished",
                "source": row.get("source") or "manual_trusted_backfill",
                "source_policy": "operator_entered_only_with_public_source_url",
            }
        )
    return result


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
    local_due_source = []
    for row in local_match_candidates(alignment):
        row = apply_schedule_override(row)
        has_score = bool(normalize_score(row.get("score"))) or (
            row.get("home_score") is not None and row.get("away_score") is not None
        )
        if not has_score and score_due_after_grace(row):
            local_due_source.append(row)
    provider_scored, provider_pending, provider_meta = provider_rows(alignment)
    manual_scored = manual_backfill_rows()
    scored_by_id: dict[str, dict[str, Any]] = {}
    for row in scored + manual_scored + provider_scored:
        match_id = str(row.get("match_id") or row.get("id") or "")
        if match_id:
            scored_by_id[match_id] = row
    # Match results are append-only facts. Once a trusted score is in the
    # registry, later provider windows may omit that event, but they must not
    # push the match back into pending settlement.
    previous = read_json(MATCH_RESULTS_DIR / "latest_known_scores.json", {}) or {}
    for row in previous.get("matches") or []:
        if not isinstance(row, dict):
            continue
        match_id = str(row.get("match_id") or "")
        if match_id and match_id not in scored_by_id:
            carried = dict(row)
            carried.setdefault("source", row.get("source") or "previous_known_scores_carried_forward")
            if not provider_meta.get("ok"):
                carried["carried_forward_due_to_source_error"] = provider_meta.get("error")
            scored_by_id[match_id] = carried
    pending_by_id: dict[str, dict[str, Any]] = {}
    for row in [item for item in pending_source + local_due_source if isinstance(item, dict)] + provider_pending:
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
        "manual_backfill_count": len(manual_scored),
        "manual_backfill_path": str(MANUAL_BACKFILL_PATH),
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
    serializable["ok"] = not bool(sync.get("blocking_pending_score_count"))
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
