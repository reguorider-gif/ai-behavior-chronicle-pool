#!/usr/bin/env python3
"""Product-health audit for the PRED-INVEST daily game loop.

The goal is to catch the exact class of regressions that make the product feel
incoherent: stale public fallbacks, mismatched gates, missing seat coverage,
fixtures without odds, hidden commentary logs, and V2 rules that live in docs
instead of daily SOP artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PRED_DIR = ROOT / "data" / "pool" / "pred_invest"
POOL_DIR = ROOT / "data" / "pool"
LIVE_DIR_DEFAULT = ROOT.parent / "pool-app-live-repair"
REQUIRED_RULE = "PRED_INVEST_CREDIT_SURVIVE_V2"
REQUIRED_SEATS = {"chatgpt", "deepseek", "mimo", "minimax", "doubao", "gemini", "kimi", "meta", "qwen", "wenxin", "grok", "yuanbao"}
BROWSER_WRAPPER = Path("/opt/homebrew/Caskroom/chromium/latest/chromium.wrapper.sh")


def browser_health() -> dict[str, Any]:
    """Verify the headless browser entry used by frontend smoke tests."""
    result: dict[str, Any] = {
        "command": shutil.which("chromium") or "/opt/homebrew/bin/chromium",
        "wrapper": str(BROWSER_WRAPPER),
        "ok": False,
        "uses_chrome_fallback": False,
        "do_not_delete_marker": False,
    }
    wrapper_text = ""
    if BROWSER_WRAPPER.exists():
        wrapper_text = BROWSER_WRAPPER.read_text(encoding="utf-8", errors="replace")
        result["uses_chrome_fallback"] = "Google Chrome.app" in wrapper_text
        result["do_not_delete_marker"] = "Do not delete" in wrapper_text
    command = result["command"]
    try:
        completed = subprocess.run(
            [str(command), "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
        result["returncode"] = completed.returncode
        result["version"] = (completed.stdout or completed.stderr).strip()
        result["ok"] = completed.returncode == 0
    except Exception as exc:
        result["error"] = str(exc)
    return result


def proxy_health() -> dict[str, Any]:
    proxies = {
        key: os.environ.get(key)
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")
        if os.environ.get(key)
    }
    result: dict[str, Any] = {
        "configured": bool(proxies),
        "proxies": proxies,
        "ok": True,
        "local_control_plane_bypasses_proxy": True,
    }
    if not proxies:
        return result
    targets = []
    for value in proxies.values():
        parsed = urlparse(value)
        if parsed.hostname and parsed.port:
            targets.append((parsed.hostname, parsed.port))
    unique_targets = sorted(set(targets))
    checks = []
    for host, port in unique_targets:
        reachable = False
        try:
            with socket.create_connection((host, int(port)), timeout=0.5):
                reachable = True
        except OSError as exc:
            check: dict[str, Any] = {"host": host, "port": port, "reachable": False, "error": str(exc)}
            if getattr(exc, "errno", None) == 1:
                check["python_socket_blocked_by_sandbox"] = True
                nc = shutil.which("nc")
                if nc:
                    probe = subprocess.run(
                        [nc, "-vz", host, str(port)],
                        check=False,
                        capture_output=True,
                        text=True,
                        timeout=3,
                    )
                    check["nc_probe"] = {
                        "returncode": probe.returncode,
                        "stdout": (probe.stdout or "").strip(),
                        "stderr": (probe.stderr or "").strip(),
                    }
                    if probe.returncode == 0:
                        check["reachable"] = True
                        check["reachable_via"] = "nc_probe_after_python_socket_sandbox_block"
                        reachable = True
                if not reachable:
                    check["diagnostic_only"] = True
            checks.append(check)
            continue
        checks.append({"host": host, "port": port, "reachable": reachable})
    result["checks"] = checks
    result["ok"] = all(item.get("reachable") or item.get("diagnostic_only") for item in checks) if checks else True
    result["diagnostic_only"] = bool(checks) and all(
        item.get("reachable") or item.get("diagnostic_only") for item in checks
    ) and any(item.get("python_socket_blocked_by_sandbox") for item in checks)
    return result


def split_rerun_queue(quality: dict[str, Any]) -> tuple[list[str], list[str]]:
    provider_blocked: list[str] = []
    rerunnable: list[str] = []
    queue = quality.get("rerun_queue") if isinstance(quality.get("rerun_queue"), list) else []
    modes_by_seat = {
        str(row.get("seat")): str(row.get("mode") or "")
        for row in queue
        if isinstance(row, dict) and row.get("seat")
    }
    for seat in quality.get("needs_rerun") or []:
        seat_text = str(seat)
        if modes_by_seat.get(seat_text) == "provider_quota_blocked":
            provider_blocked.append(seat_text)
        else:
            rerunnable.append(seat_text)
    return sorted(provider_blocked), sorted(rerunnable)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_read_error": str(exc)}


def latest_artifact(prefix: str) -> Path:
    return PRED_DIR / f"latest_{prefix}.json"


def count_market_rows(matches: list[Any]) -> int:
    total = 0
    for match in matches:
        if isinstance(match, dict):
            total += len(match.get("market_snapshot") or [])
    return total


def current_ids(matches: list[Any]) -> set[str]:
    return {str(match.get("match_id") or match.get("id")) for match in matches if isinstance(match, dict) and (match.get("match_id") or match.get("id"))}


def score_sync_blocking_rows(score_sync: dict[str, Any], alignment: dict[str, Any]) -> list[dict[str, Any]]:
    """Use score-sync as the authoritative overdue source.

    The alignment audit can contain historical rows that have since been
    neutralized by schedule overrides or carried-forward known scores. The
    product-health gate should only block when latest_score_sync says a score is
    still pending/blocking. Alignment is kept as a fallback for older artifacts.
    """
    pending = score_sync.get("pending_score_backfill")
    if isinstance(pending, list):
        return [row for row in pending if isinstance(row, dict) and row.get("blocking") is not False]
    overdue = alignment.get("score_missing_after_due") if isinstance(alignment.get("score_missing_after_due"), list) else []
    return [row for row in overdue if isinstance(row, dict) and row.get("blocking") is not False]


def audit(live_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    findings: list[str] = []
    browser = browser_health()

    current = read_json(latest_artifact("current_game"))
    daily = read_json(latest_artifact("daily_sop"))
    prompt = read_json(latest_artifact("prompt_pack"))
    quality = read_json(latest_artifact("quality_gate"))
    observer = read_json(POOL_DIR / "observer_ledgers" / "latest.json")
    alignment = read_json(latest_artifact("match_data_alignment_audit"))
    score_sync = read_json(latest_artifact("score_sync"))
    proxy = proxy_health()

    for name, data in {
        "current_game": current,
        "daily_sop": daily,
        "prompt_pack": prompt,
        "quality_gate": quality,
        "observer_ledger": observer,
        "match_data_alignment": alignment,
        "score_sync": score_sync,
    }.items():
        if not data:
            errors.append(f"missing_latest_artifact:{name}")
        if data.get("_read_error"):
            errors.append(f"invalid_json:{name}:{data['_read_error']}")

    rule = ((current.get("rules") or {}).get("rule_version") or (daily.get("operational_contract") or {}).get("rule_version") or (prompt.get("rules") or {}).get("rule_version"))
    if rule != REQUIRED_RULE:
        errors.append(f"rule_version_mismatch:{rule}")

    current_status = current.get("verdict")
    quality_status = quality.get("status")
    status_rank = {"NOT_READY": 0, "PARTIAL_NOT_READY": 1, "READY_WITH_WARNINGS": 1, "READY": 2}
    if (
        current_status
        and quality_status
        and status_rank.get(str(current_status), -1) > status_rank.get(str(quality_status), -1)
    ):
        errors.append(f"current_more_optimistic_than_quality:{current_status}>{quality_status}")
    current_publish = ((current.get("quality_gate") or {}).get("publish_allowed"))
    quality_publish = quality.get("publish_allowed")
    if current_publish is not None and quality_publish is not None and current_publish != quality_publish:
        errors.append("current_quality_publish_mismatch")

    matches = current.get("matches") if isinstance(current.get("matches"), list) else []
    prompt_matches = prompt.get("matches") if isinstance(prompt.get("matches"), list) else []
    if not matches:
        errors.append("current_game_has_no_matches")
    if not prompt_matches:
        errors.append("prompt_pack_has_no_matches")
    missing_odds = [str(match.get("match_id") or match.get("id")) for match in matches if isinstance(match, dict) and not match.get("market_snapshot")]
    if missing_odds:
        errors.append("current_game_matches_without_odds:" + ",".join(missing_odds))
    if count_market_rows(matches) <= 0:
        errors.append("current_game_has_no_market_rows")

    required = set(str(item) for item in quality.get("required_match_ids") or [])
    if required:
        missing_required = sorted(required - current_ids(matches))
        if missing_required:
            errors.append("required_matches_missing_from_current_game:" + ",".join(missing_required))

    prompt_required = ((prompt.get("required_coverage") or {}) if isinstance(prompt.get("required_coverage"), dict) else {})
    prompt_missing_required = prompt_required.get("missing_required_match_ids") or []
    if prompt_missing_required:
        errors.append("prompt_pack_missing_required_matches:" + ",".join(str(item) for item in prompt_missing_required))

    valid = set(str(item) for item in quality.get("valid_seats") or [])
    provider_blocked, rerunnable_needs = split_rerun_queue(quality)
    needs = set(str(item) for item in quality.get("needs_rerun") or [])
    seen = valid | needs
    missing_seat_state = sorted(REQUIRED_SEATS - seen)
    if missing_seat_state:
        errors.append("quality_gate_missing_seat_state:" + ",".join(missing_seat_state))
    if quality.get("publish_allowed") and len(valid) != 12:
        errors.append(f"publish_allowed_but_valid_count_is_{len(valid)}")
    if not quality.get("publish_allowed") and current.get("verdict") == "READY":
        errors.append("current_game_ready_while_gate_blocks")
    if rerunnable_needs:
        warnings.append("targeted_rerun_required:" + ",".join(rerunnable_needs))
    if provider_blocked:
        warnings.append("provider_blocked_wait_for_reset:" + ",".join(provider_blocked))
        findings.append("provider_blocked_seats=" + ",".join(provider_blocked))

    if not browser.get("ok"):
        errors.append(f"browser_qa_entry_broken:{browser.get('error') or browser.get('version') or browser.get('returncode')}")
    elif browser.get("uses_chrome_fallback"):
        findings.append("browser_qa_entry=ok_with_chrome_fallback")
    if not browser.get("do_not_delete_marker"):
        warnings.append("browser_wrapper_missing_do_not_delete_marker")
    if proxy.get("configured") and not proxy.get("ok"):
        warnings.append("proxy_configured_but_unreachable")
    elif proxy.get("diagnostic_only"):
        findings.append("proxy_python_socket_check_sandboxed_but_non_blocking")

    overdue_scores = score_sync_blocking_rows(score_sync, alignment)
    unique_overdue = sorted({str(row.get("match_id")) for row in overdue_scores if isinstance(row, dict) and row.get("match_id")})
    if unique_overdue:
        errors.append(f"score_sync_overdue:{len(unique_overdue)}:" + ",".join(unique_overdue[:12]))

    observer_round = observer.get("round_id")
    if observer_round and current.get("round_id") and observer_round != current.get("round_id"):
        warnings.append(f"observer_round_differs_from_current:{observer_round}!={current.get('round_id')}")
    if not observer.get("seat_commentaries"):
        warnings.append("observer_ledger_missing_seat_commentaries")

    index_path = live_dir / "index.html"
    live_current = read_json(live_dir / "data" / "pool" / "pred_invest" / "latest_current_game.json")
    live_observer = read_json(live_dir / "data" / "pool" / "observer_ledgers" / "latest.json")
    if live_current:
        if live_current.get("round_id") != current.get("round_id") or live_current.get("date") != current.get("date"):
            errors.append(
                f"live_current_game_stale:{live_current.get('date')}:{live_current.get('round_id')}!={current.get('date')}:{current.get('round_id')}"
            )
    else:
        errors.append("live_current_game_missing")
    if live_observer:
        if live_observer.get("round_id") != observer.get("round_id") or live_observer.get("date") != observer.get("date"):
            errors.append(
                f"live_observer_ledger_stale:{live_observer.get('date')}:{live_observer.get('round_id')}!={observer.get('date')}:{observer.get('round_id')}"
            )
    else:
        errors.append("live_observer_ledger_missing")
    if index_path.exists():
        html = index_path.read_text(encoding="utf-8", errors="replace")
        forbidden = [
            "PRED-INVEST v1",
            "pred_invest_v1",
            "ops-v2",
            "V2 运营链路",
            "POOL_V2_STATIC",
            "opsV2",
            "运营链路页",
        ]
        for pattern in forbidden:
            if pattern in html:
                errors.append(f"public_frontend_forbidden_pattern:{pattern}")
        stale_patterns = {
            "static_observer_ledger": r"const\s+OBSERVER_LEDGER\s*=\s*\{",
            "static_pool_fallback": r"const\s+POOL_FALLBACK_BY_DATE\s*=\s*\{",
            "static_fixture_catalog": r"const\s+allMatches\s*=\s*\{",
            "static_contextual_model_views": r"function\s+contextualModelViews\s*\(",
        }
        for label, pattern in stale_patterns.items():
            if re.search(pattern, html):
                warnings.append(f"public_frontend_still_has_{label}")
        required_ui = ["commentary-log.html", "observerLedger", "loanInterest", "principalRepaid", "dataQuality"]
        for token in required_ui:
            if token not in html:
                errors.append(f"public_frontend_missing_ui_token:{token}")
    else:
        warnings.append(f"live_index_missing:{index_path}")

    latest_rounds = {
        "current_game": current.get("round_id"),
        "daily_sop": daily.get("round_id"),
        "prompt_pack": prompt.get("round_id"),
        "quality_gate": quality.get("round_id"),
        "observer_ledger": observer.get("round_id"),
    }
    stale_latest = [name for name, round_id in latest_rounds.items() if str(round_id or "") == "run-13"]
    if stale_latest:
        warnings.append("latest_entry_still_points_to_run13:" + ",".join(stale_latest))

    status = "READY" if not errors and not warnings else ("READY_WITH_WARNINGS" if not errors else "NOT_READY")
    findings.extend(
        [
            f"current={current.get('date')} {current.get('round_id')} {current.get('verdict')}",
            f"quality={quality.get('status')} valid={len(valid)}/12 needs={','.join(sorted(needs)) or 'none'}",
            f"matches={len(matches)} market_rows={count_market_rows(matches)}",
            f"observer={observer.get('date')} {observer.get('round_id')} phase={observer.get('phase')}",
            f"browser_qa={browser.get('version') or browser.get('error') or 'unknown'}",
            f"score_sync_overdue={len(unique_overdue)}",
        ]
    )
    return {
        "version": "pred_invest_product_health.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
        "artifact_refs": {
            "current_game": str(latest_artifact("current_game")),
            "daily_sop": str(latest_artifact("daily_sop")),
            "prompt_pack": str(latest_artifact("prompt_pack")),
            "quality_gate": str(latest_artifact("quality_gate")),
            "observer_ledger": str(POOL_DIR / "observer_ledgers" / "latest.json"),
            "match_data_alignment": str(latest_artifact("match_data_alignment_audit")),
            "score_sync": str(latest_artifact("score_sync")),
            "frontend_index": str(index_path),
            "live_current_game": str(live_dir / "data" / "pool" / "pred_invest" / "latest_current_game.json"),
            "live_observer_ledger": str(live_dir / "data" / "pool" / "observer_ledgers" / "latest.json"),
            "browser_wrapper": str(BROWSER_WRAPPER),
        },
        "browser_qa": browser,
        "proxy": proxy,
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PRED-INVEST Product Health Audit",
        "",
        f"- status: **{report['status']}**",
        f"- generated_at: {report['generated_at']}",
        "",
        "## Findings",
        "",
    ]
    lines.extend(f"- {item}" for item in report["findings"])
    lines += ["", "## Errors", ""]
    lines.extend(f"- {item}" for item in report["errors"]) if report["errors"] else lines.append("- none")
    lines += ["", "## Warnings", ""]
    lines.extend(f"- {item}" for item in report["warnings"]) if report["warnings"] else lines.append("- none")
    return "\n".join(lines) + "\n"


def write_report(report: dict[str, Any]) -> dict[str, str]:
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    json_path = PRED_DIR / "latest_product_health.json"
    md_path = PRED_DIR / "latest_product_health.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-dir", default=str(LIVE_DIR_DEFAULT))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = audit(Path(args.live_dir))
    if args.write:
        report["paths"] = write_report(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] != "NOT_READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
