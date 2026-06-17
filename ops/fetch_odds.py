#!/usr/bin/env python3
"""Schedule, odds, and score synchronization facade for PRED-INVEST SOP.

This module deliberately reuses the existing prompt-pack and score-sync code.
It gives automation a stable class boundary without creating a second data
pipeline.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from pool.io_utils import read_json
from pred_invest_schedule_overrides import apply_schedule_override


ROOT = Path(__file__).resolve().parents[1]
POOL_DIR = ROOT / "data" / "pool"
PRED_DIR = POOL_DIR / "pred_invest"
BASE_URL = "https://pool-app-one.vercel.app"
THE_ODDS_SPORT_KEY = "soccer_fifa_world_cup"
THE_ODDS_CONFIG_PATH = Path.home() / ".config" / "ai-judge" / "the_odds_api_key"
THE_ODDS_SCORES_CACHE_PATH = POOL_DIR / "match_results" / "the_odds_scores_cache.json"
THE_ODDS_MARKET_CACHE_PATH = POOL_DIR / "market_snapshots" / "the_odds_market_cache.json"


def normalize_team(value: Any) -> str:
    text = str(value or "").casefold()
    text = text.replace("&", "and")
    text = text.replace("ç", "c")
    text = text.replace("curaçao", "curacao")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = " ".join(text.split())
    aliases = {
        "dr congo": "congo dr",
        "d r congo": "congo dr",
        "congo democratic republic": "congo dr",
        "democratic republic congo": "congo dr",
        "democratic republic of congo": "congo dr",
        "cote d ivoire": "ivory coast",
        "cote divoire": "ivory coast",
        "united states": "usa",
        "united states of america": "usa",
        "korea republic": "south korea",
        "republic of korea": "south korea",
    }
    return aliases.get(text, text)


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


def should_write_provider_cache() -> bool:
    return os.environ.get("PRED_INVEST_WRITE_PROVIDER_CACHE") == "1"


def write_provider_cache(path: Path, rows: list[dict[str, Any]], key: str, source: str) -> None:
    if not should_write_provider_cache() or not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "the_odds_api_provider_cache.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        key: rows,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


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
        primary_error = f"{type(exc).__name__}: {exc}"
        curl_system_rows, curl_system_meta = fetch_the_odds_scores_with_curl(url, system=True)
        if curl_system_meta.get("ok"):
            write_provider_cache(THE_ODDS_SCORES_CACHE_PATH, curl_system_rows, "scores", "the_odds_api_scores:curl_system")
            curl_system_meta["primary_transport_error"] = primary_error
            return curl_system_rows, {**meta, **curl_system_meta}
        curl_direct_rows, curl_direct_meta = fetch_the_odds_scores_with_curl(url)
        if curl_direct_meta.get("ok"):
            write_provider_cache(THE_ODDS_SCORES_CACHE_PATH, curl_direct_rows, "scores", "the_odds_api_scores:curl_direct")
            curl_direct_meta["primary_transport_error"] = primary_error
            curl_direct_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            return curl_direct_rows, {**meta, **curl_direct_meta}
        proxy_rows, proxy_meta = fetch_the_odds_scores_with_urllib_proxy(url)
        if proxy_meta.get("ok"):
            write_provider_cache(THE_ODDS_SCORES_CACHE_PATH, proxy_rows, "scores", "the_odds_api_scores:urllib_proxy")
            proxy_meta["primary_transport_error"] = primary_error
            proxy_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            proxy_meta["curl_direct_fallback_error"] = curl_direct_meta.get("error")
            return proxy_rows, {**meta, **proxy_meta}
        proxy_url = local_http_proxy_url()
        curl_proxy_rows, curl_proxy_meta = fetch_the_odds_scores_with_curl(url, proxy=proxy_url)
        if curl_proxy_meta.get("ok"):
            write_provider_cache(THE_ODDS_SCORES_CACHE_PATH, curl_proxy_rows, "scores", "the_odds_api_scores:curl_proxy")
            curl_proxy_meta["primary_transport_error"] = primary_error
            curl_proxy_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            curl_proxy_meta["curl_direct_fallback_error"] = curl_direct_meta.get("error")
            if proxy_meta.get("error"):
                curl_proxy_meta["urllib_proxy_fallback_error"] = proxy_meta.get("error")
            return curl_proxy_rows, {**meta, **curl_proxy_meta}
        cache_rows, cache_meta = fetch_the_odds_scores_from_cache()
        if cache_meta.get("ok"):
            cache_meta["primary_transport_error"] = primary_error
            cache_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            cache_meta["curl_direct_fallback_error"] = curl_direct_meta.get("error")
            cache_meta["urllib_proxy_fallback_error"] = proxy_meta.get("error")
            cache_meta["curl_proxy_fallback_error"] = curl_proxy_meta.get("error")
            return cache_rows, {**meta, **cache_meta}
        meta["error"] = primary_error
        meta["curl_system_fallback"] = curl_system_meta
        meta["curl_direct_fallback"] = curl_direct_meta
        meta["urllib_proxy_fallback"] = proxy_meta
        meta["curl_proxy_fallback"] = curl_proxy_meta
        meta["cache_fallback"] = cache_meta
        return [], meta
    if not isinstance(data, list):
        meta["error"] = "unexpected_scores_payload"
        return [], meta
    rows = [row for row in data if isinstance(row, dict)]
    write_provider_cache(THE_ODDS_SCORES_CACHE_PATH, rows, "scores", "the_odds_api_scores:urllib_direct")
    meta.update(
        {
            "ok": True,
            "row_count": len(rows),
            "last_updates": sorted({str(row.get("last_update")) for row in rows if row.get("last_update")})[-3:],
        }
    )
    return rows, meta


def fetch_the_odds_scores_from_cache(path: Path | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Read the last externally fetched scores payload.

    This is intentionally a fallback, not the primary source. Some local
    automation environments can reach The Odds API through system curl while
    Python DNS/proxy sockets are restricted. Keeping the cache as a raw
    provider payload lets the SOP continue with auditable external data rather
    than silently using model predictions as results.
    """

    cache_path = path or THE_ODDS_SCORES_CACHE_PATH
    meta: dict[str, Any] = {
        "transport": "cache_fallback",
        "ok": False,
        "error": None,
        "row_count": 0,
        "source_path": str(cache_path),
    }
    if not cache_path.exists():
        meta["error"] = "the_odds_scores_cache_missing"
        return [], meta
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception as exc:
        meta["error"] = f"cache_read_failed:{type(exc).__name__}: {exc}"
        return [], meta
    if isinstance(payload, dict):
        data = payload.get("scores") or payload.get("events") or payload.get("rows") or payload.get("data")
    else:
        data = payload
    if not isinstance(data, list):
        meta["error"] = "unexpected_scores_cache_payload"
        return [], meta
    rows = [row for row in data if isinstance(row, dict)]
    if not rows:
        meta["error"] = "empty_scores_cache"
        return [], meta
    try:
        meta["cache_mtime"] = datetime.fromtimestamp(cache_path.stat().st_mtime, timezone.utc).isoformat()
    except Exception:
        pass
    meta.update(
        {
            "ok": True,
            "row_count": len(rows),
            "last_updates": sorted({str(row.get("last_update")) for row in rows if row.get("last_update")})[-3:],
        }
    )
    return rows, meta


def fetch_the_odds_scores_with_urllib_proxy(url: str, timeout: int = 30) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Retry urllib through an explicit proxy before shelling out to curl."""

    meta: dict[str, Any] = {
        "transport": "urllib_proxy_fallback",
        "ok": False,
        "error": None,
        "row_count": 0,
    }
    proxy = local_http_proxy_url()
    if not proxy:
        meta["error"] = "no_explicit_proxy_configured"
        return [], meta
    meta["explicit_proxy"] = proxy
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {
                "http": proxy,
                "https": proxy,
            }
        )
    )
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with opener.open(request, timeout=timeout) as response:
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
    meta.update(
        {
            "ok": True,
            "row_count": len(rows),
            "last_updates": sorted({str(row.get("last_update")) for row in rows if row.get("last_update")})[-3:],
        }
    )
    return rows, meta


def fetch_the_odds_scores_with_curl(
    url: str,
    timeout: int = 30,
    *,
    proxy: str | None = None,
    system: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Fallback through curl with system, explicit direct, or proxy modes.

    Python urllib DNS can fail in the Codex sandbox. Curl direct sometimes
    succeeds when urllib does not, while the local 7897 proxy is intermittent.
    Plain system curl can also succeed when macOS routes traffic through a
    system-level proxy that is not visible in HTTP_PROXY/HTTPS_PROXY. The caller
    tries system curl before forcing direct DNS or explicit proxy modes.
    """

    meta: dict[str, Any] = {
        "transport": "curl_system_fallback" if system else ("curl_proxy_fallback" if proxy else "curl_direct_fallback"),
        "ok": False,
        "error": None,
        "row_count": 0,
    }
    cmd = [
        "curl",
        "-sS",
        "--connect-timeout",
        "10",
        "--retry",
        "2",
        "--retry-delay",
        "1",
        "-m",
        str(timeout),
        "-H",
        "Accept: application/json",
        url,
    ]
    if proxy:
        cmd[1:1] = ["--proxy", proxy]
        meta["explicit_proxy"] = proxy
    elif not system:
        cmd[1:1] = ["--noproxy", "*"]
    try:
        completed = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=timeout + 10)
    except Exception as exc:
        meta["error"] = f"{type(exc).__name__}: {exc}"
        return [], meta
    if completed.returncode != 0:
        meta["curl_returncode"] = completed.returncode
        meta["error"] = (completed.stderr or completed.stdout or "curl_failed")[:500]
        return [], meta
    raw = completed.stdout
    try:
        data = json.loads(raw)
    except Exception as exc:
        meta["error"] = f"curl_non_json_response:{type(exc).__name__}"
        meta["raw"] = raw[:500]
        return [], meta
    if not isinstance(data, list):
        meta["error"] = "unexpected_scores_payload"
        meta["raw"] = raw[:500]
        return [], meta
    rows = [row for row in data if isinstance(row, dict)]
    meta.update(
        {
            "ok": True,
            "row_count": len(rows),
            "last_updates": sorted({str(row.get("last_update")) for row in rows if row.get("last_update")})[-3:],
        }
    )
    return rows, meta


def fetch_the_odds_market_odds(
    *,
    regions: str = "us,eu",
    markets: str = "h2h,spreads,totals",
    odds_format: str = "decimal",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    key = the_odds_api_key()
    meta = {
        "source": "the_odds_api_odds",
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
        f"https://api.the-odds-api.com/v4/sports/{THE_ODDS_SPORT_KEY}/odds/"
        f"?regions={regions}&markets={markets}&oddsFormat={odds_format}&apiKey={key}"
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
        primary_error = f"{type(exc).__name__}: {exc}"
        curl_system_rows, curl_system_meta = fetch_the_odds_scores_with_curl(url, system=True)
        if curl_system_meta.get("ok"):
            write_provider_cache(THE_ODDS_MARKET_CACHE_PATH, curl_system_rows, "odds", "the_odds_api_odds:curl_system")
            curl_system_meta["primary_transport_error"] = primary_error
            return curl_system_rows, {**meta, **curl_system_meta}
        curl_direct_rows, curl_direct_meta = fetch_the_odds_scores_with_curl(url)
        if curl_direct_meta.get("ok"):
            write_provider_cache(THE_ODDS_MARKET_CACHE_PATH, curl_direct_rows, "odds", "the_odds_api_odds:curl_direct")
            curl_direct_meta["primary_transport_error"] = primary_error
            curl_direct_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            return curl_direct_rows, {**meta, **curl_direct_meta}
        proxy_url = local_http_proxy_url()
        curl_proxy_rows, curl_proxy_meta = fetch_the_odds_scores_with_curl(url, proxy=proxy_url)
        if curl_proxy_meta.get("ok"):
            write_provider_cache(THE_ODDS_MARKET_CACHE_PATH, curl_proxy_rows, "odds", "the_odds_api_odds:curl_proxy")
            curl_proxy_meta["primary_transport_error"] = primary_error
            curl_proxy_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            curl_proxy_meta["curl_direct_fallback_error"] = curl_direct_meta.get("error")
            return curl_proxy_rows, {**meta, **curl_proxy_meta}
        cache_rows, cache_meta = fetch_the_odds_market_odds_from_cache()
        if cache_meta.get("ok"):
            cache_meta["primary_transport_error"] = primary_error
            cache_meta["curl_system_fallback_error"] = curl_system_meta.get("error")
            cache_meta["curl_direct_fallback_error"] = curl_direct_meta.get("error")
            cache_meta["curl_proxy_fallback_error"] = curl_proxy_meta.get("error")
            return cache_rows, {**meta, **cache_meta}
        meta["error"] = primary_error
        meta["curl_system_fallback"] = curl_system_meta
        meta["curl_direct_fallback"] = curl_direct_meta
        meta["curl_proxy_fallback"] = curl_proxy_meta
        meta["cache_fallback"] = cache_meta
        return [], meta
    if not isinstance(data, list):
        meta["error"] = "unexpected_odds_payload"
        return [], meta
    rows = [row for row in data if isinstance(row, dict)]
    write_provider_cache(THE_ODDS_MARKET_CACHE_PATH, rows, "odds", "the_odds_api_odds:urllib_direct")
    meta.update({"ok": True, "row_count": len(rows)})
    return rows, meta


def fetch_the_odds_market_odds_from_cache(path: Path | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cache_path = path or THE_ODDS_MARKET_CACHE_PATH
    meta: dict[str, Any] = {
        "transport": "market_cache_fallback",
        "ok": False,
        "error": None,
        "row_count": 0,
        "source_path": str(cache_path),
    }
    if not cache_path.exists():
        meta["error"] = "the_odds_market_cache_missing"
        return [], meta
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception as exc:
        meta["error"] = f"cache_read_failed:{type(exc).__name__}: {exc}"
        return [], meta
    data = payload.get("odds") or payload.get("events") or payload.get("rows") or payload.get("data") if isinstance(payload, dict) else payload
    if not isinstance(data, list):
        meta["error"] = "unexpected_market_cache_payload"
        return [], meta
    rows = [row for row in data if isinstance(row, dict)]
    if not rows:
        meta["error"] = "empty_market_cache"
        return [], meta
    try:
        meta["cache_mtime"] = datetime.fromtimestamp(cache_path.stat().st_mtime, timezone.utc).isoformat()
    except Exception:
        pass
    meta.update({"ok": True, "row_count": len(rows)})
    return rows, meta


def local_http_proxy_url() -> str:
    """Best-effort local proxy fallback for Python processes without env proxy.

    macOS network proxy settings are not automatically visible to urllib in
    this CLI environment, while curl from an interactive shell can still use a
    local proxy. The fallback is only tried after urllib has already failed,
    so prefer the known local AI Judge/Clash port and let curl report if it is
    unavailable.
    """

    configured = os.environ.get("THE_ODDS_PROXY") or os.environ.get("AI_JUDGE_HTTP_PROXY")
    return configured.strip() if configured else "http://127.0.0.1:7897"


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
        pending.append(
            {
                **base,
                "status": "scheduled",
                "result_state": "awaiting_provider_final",
                "gap": "provider_not_completed" if not blocking else "provider_score_overdue_after_kickoff",
                "blocking": blocking,
            }
        )
    meta["mapped_settled_count"] = len(settled)
    meta["mapped_pending_count"] = len(pending)
    return settled, pending, meta


def _market_name(provider_key: Any) -> str:
    key = str(provider_key or "").lower()
    if key == "h2h":
        return "h2h"
    if key == "spreads":
        return "handicap"
    if key == "totals":
        return "total_goals"
    return key or "unknown"


def _provider_market_rows(event: dict[str, Any], local_match_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bookmaker in event.get("bookmakers") or []:
        if not isinstance(bookmaker, dict):
            continue
        provider = bookmaker.get("title") or bookmaker.get("key") or "the_odds_api"
        provider_last_update = bookmaker.get("last_update")
        for market in bookmaker.get("markets") or []:
            if not isinstance(market, dict):
                continue
            market_name = _market_name(market.get("key"))
            for outcome in market.get("outcomes") or []:
                if not isinstance(outcome, dict):
                    continue
                price = outcome.get("price")
                if price in (None, ""):
                    continue
                row = {
                    "match_id": local_match_id,
                    "market": market_name,
                    "selection": outcome.get("name"),
                    "line": outcome.get("point"),
                    "odds": price,
                    "provider": provider,
                    "bookmaker_or_provider": provider,
                    "provider_event_id": event.get("id"),
                    "provider_last_update": provider_last_update or event.get("last_update"),
                    "source": "the_odds_api_odds",
                    "status": "ok",
                }
                rows.append(row)
    return rows


def provider_odds_by_match(matches: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Return The Odds API market rows keyed by internal match_id.

    Mapping is intentionally by normalized team pair because The Odds API uses
    provider event ids, while the product registry uses internal WC-* ids.
    """

    provider_events, meta = fetch_the_odds_market_odds()
    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    for event in provider_events:
        key = (normalize_team(event.get("home_team")), normalize_team(event.get("away_team")))
        reverse = (key[1], key[0])
        if all(key):
            by_pair[key] = event
            by_pair.setdefault(reverse, event)

    grouped: dict[str, list[dict[str, Any]]] = {}
    missing: list[str] = []
    for match in matches:
        match = apply_schedule_override(match)
        local_id = str(match.get("match_id") or match.get("id") or "")
        if not local_id:
            continue
        key = candidate_key(match)
        event = by_pair.get(key)
        if not event:
            missing.append(local_id)
            continue
        rows = _provider_market_rows(event, local_id)
        if rows:
            grouped[local_id] = rows
        else:
            missing.append(local_id)

    meta["mapped_match_count"] = len(grouped)
    meta["mapped_market_row_count"] = sum(len(rows) for rows in grouped.values())
    meta["missing_match_ids"] = missing
    return grouped, meta


class OddsFetcher:
    """Thin orchestration wrapper around the existing data sync functions."""

    def __init__(self, alignment_path: Path | None = None, *, base_url: str = BASE_URL) -> None:
        self.alignment_path = alignment_path or (PRED_DIR / "latest_match_data_alignment_audit.json")
        self.base_url = base_url.rstrip("/")

    def fetch_schedule(self) -> dict[str, Any]:
        alignment = read_json(self.alignment_path, {})
        candidates = local_match_candidates(alignment)
        return {
            "ok": True,
            "source": str(self.alignment_path),
            "match_count": len(candidates),
            "matches": candidates,
        }

    def fetch_odds(self, date: str, round_id: str, base_url: str | None = None, *, write_contexts: bool = False) -> dict[str, Any]:
        from generate_pred_invest_prompt_pack import build_prompt_pack

        pack = build_prompt_pack(date, round_id, base_url or self.base_url, write_contexts=write_contexts)
        return {
            "ok": bool(pack.get("matches")) and any((match.get("market_snapshot") for match in pack.get("matches") or [] if isinstance(match, dict))),
            "date": date,
            "round_id": round_id,
            "market_source_meta": pack.get("market_source_meta") or {},
            "models": pack.get("models"),
            "match_count": pack.get("match_count"),
            "matches_with_odds": sum(1 for match in pack.get("matches") or [] if isinstance(match, dict) and match.get("market_snapshot")),
            "missing_odds_match_ids": [
                str(match.get("match_id") or match.get("id") or "unknown")
                for match in pack.get("matches") or []
                if isinstance(match, dict) and not match.get("market_snapshot")
            ],
            "matches": pack.get("matches") or [],
            "prompt_pack": pack,
        }

    def build_market_board(self, date: str, run_id: str) -> dict[str, Any]:
        odds = self.fetch_odds(date, run_id)
        return {
            "ok": odds.get("ok"),
            "date": date,
            "run_id": run_id,
            "selection_policy": (odds.get("prompt_pack") or {}).get("selection_policy"),
            "market_source_meta": odds.get("market_source_meta") or {},
            "matches": odds.get("matches") or [],
            "match_count": odds.get("match_count", 0),
            "matches_with_odds": odds.get("matches_with_odds", 0),
            "missing_odds_match_ids": odds.get("missing_odds_match_ids") or [],
            "pack": odds.get("prompt_pack") or {},
        }

    def fetch_scores(self, days_from: int = 3) -> dict[str, Any]:
        rows, meta = fetch_the_odds_scores(days_from=days_from)
        alignment = read_json(self.alignment_path, {})
        settled, pending, mapped_meta = provider_rows(alignment)
        return {
            "ok": bool(meta.get("ok")),
            "source": meta,
            "raw_count": len(rows),
            "settled": settled,
            "pending": pending,
            "mapped": mapped_meta,
        }

    def sync_scores(self, *, write: bool = False) -> dict[str, Any]:
        from sync_pred_invest_scores import build_sync, write_sync

        score_sync = build_sync(self.alignment_path)
        if write:
            score_sync["paths"] = write_sync(score_sync)
        result = {key: value for key, value in score_sync.items() if key != "by_output_date"}
        result["ok"] = not bool(score_sync.get("blocking_pending_score_count"))
        external = score_sync.get("external_score_source") or {}
        if not external.get("ok"):
            result["warnings"] = [f"external_score_source_unavailable:{external.get('error') or 'unknown'}"]
        return result

    def sync_all(self, date: str, round_id: str, base_url: str | None = None, *, write: bool = False) -> dict[str, Any]:
        from sync_pred_invest_scores import build_sync, write_sync

        schedule = self.fetch_schedule()
        odds = self.fetch_odds(date, round_id, base_url, write_contexts=write)
        score_sync = build_sync(self.alignment_path)
        paths: dict[str, Any] = {}
        if write:
            from generate_pred_invest_prompt_pack import write_outputs as write_prompt_pack

            paths["prompt_pack"] = write_prompt_pack(odds["prompt_pack"])
            paths["score_sync"] = write_sync(score_sync)
        market_board = {
            "ok": odds.get("ok"),
            "date": date,
            "run_id": round_id,
            "selection_policy": (odds.get("prompt_pack") or {}).get("selection_policy"),
            "market_source_meta": odds.get("market_source_meta") or {},
            "match_count": odds.get("match_count"),
            "matches_with_odds": odds.get("matches_with_odds"),
            "missing_odds_match_ids": odds.get("missing_odds_match_ids") or [],
        }
        return {
            "ok": bool(odds.get("ok")) and not score_sync.get("blocking_pending_score_count"),
            "date": date,
            "round_id": round_id,
            "schedule": {key: value for key, value in schedule.items() if key != "matches"},
            "odds": {key: value for key, value in odds.items() if key != "prompt_pack"},
            "market_board": market_board,
            "score_sync": {key: value for key, value in score_sync.items() if key != "by_output_date"},
            "paths": paths,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch schedule, odds, and scores for PRED-INVEST SOP")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", "--run-id", dest="round_id", required=True)
    parser.add_argument("--base-url", default="https://pool-app-one.vercel.app")
    parser.add_argument("--alignment", default=str(PRED_DIR / "latest_match_data_alignment_audit.json"))
    parser.add_argument("--sync", choices=["all", "scores", "market"], default="all")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.write:
        os.environ.setdefault("PRED_INVEST_WRITE_PROVIDER_CACHE", "1")

    fetcher = OddsFetcher(Path(args.alignment), base_url=args.base_url)
    if args.sync == "scores":
        result = fetcher.sync_scores(write=args.write)
    elif args.sync == "market":
        result = {key: value for key, value in fetcher.build_market_board(args.date, args.round_id).items() if key != "pack"}
        if args.write:
            full = fetcher.build_market_board(args.date, args.round_id)
            if full.get("pack"):
                from generate_pred_invest_prompt_pack import write_outputs as write_prompt_pack

                result["prompt_pack_paths"] = write_prompt_pack(full["pack"])
    else:
        result = fetcher.sync_all(args.date, args.round_id, write=args.write)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
