#!/usr/bin/env python3
"""Run targeted PRED-INVEST single-seat reruns.

This is the repair executor behind the daily SOP gate: it only submits seats
that currently fail the quality gate, waits for each isolated bridge run to
finish, then regenerates the audit/gate/current-game/observer artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import audit_pred_invest_bridge_outputs
import build_pred_invest_current_game
import capture_pred_invest_page_salvage
import generate_observer_ledger
import pred_invest_quality_gate
import pred_invest_sop_guard
import run_pred_invest_daily_sop
from submit_pred_invest_bridge_run import submit


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
RUNTIME_PYTHON = Path("/Users/audimacmini/Library/Application Support/AI Judge/user-app-support/runtime/.venv/bin/python")
DEFAULT_TARGET_SEATS = ["doubao", "gemini", "grok", "kimi", "mimo", "minimax", "wenxin"]
LOCAL_NO_PROXY = "127.0.0.1,localhost,::1"


def _is_local_url(url: str) -> bool:
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    return host in {"127.0.0.1", "localhost", "::1"}


def _local_subprocess_env() -> dict[str, str]:
    env = dict(os.environ)
    env["NO_PROXY"] = ",".join(filter(None, [env.get("NO_PROXY"), LOCAL_NO_PROXY]))
    env["no_proxy"] = ",".join(filter(None, [env.get("no_proxy"), LOCAL_NO_PROXY]))
    # CDP and bridge calls are local control-plane calls. They must not be sent
    # through a user/system HTTP proxy, or Playwright will try 127.0.0.1:7897.
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
        env.pop(key, None)
    return env


def _http_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if _is_local_url(url) else urllib.request
        with opener.open(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                return json.loads(raw)
            except Exception:
                return {"ok": False, "error": "non_json_response", "status": response.status, "raw": raw[:1200]}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw[:1200]}
        body.setdefault("ok", False)
        body.setdefault("status", exc.code)
        return body
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}


def _parse_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def _bridge_busy(status: dict[str, Any]) -> bool:
    return bool(status.get("busy") or (status.get("bridge_run") or {}).get("busy"))


def _bridge_run_id(status: dict[str, Any]) -> str | None:
    value = status.get("active_run_id") or (status.get("bridge_run") or {}).get("run_id")
    return str(value) if value else None


def _bridge_elapsed(status: dict[str, Any]) -> float:
    value = status.get("elapsed_sec")
    if value is None:
        value = (status.get("bridge_run") or {}).get("elapsed_seconds")
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def _wait_for_bridge_idle(base_url: str, recover_after: float, wait_seconds: float = 900) -> dict[str, Any]:
    deadline = time.time() + wait_seconds
    last: dict[str, Any] = {}
    while time.time() < deadline:
        status = _http_json(f"{base_url}/api/bridge/status", timeout=45)
        last = status
        if not _bridge_busy(status):
            return {"ok": True, "status": status, "recovered": False}
        elapsed = _bridge_elapsed(status)
        active = _bridge_run_id(status)
        if elapsed >= recover_after:
            recovery = _http_json(
                f"{base_url}/api/bridge/recover",
                payload={"run_id": active, "reason": "pred_invest_attempt4_single_seat_recover"},
                timeout=45,
            )
            after = _http_json(f"{base_url}/api/bridge/status", timeout=45)
            return {"ok": not _bridge_busy(after), "status": after, "recovered": True, "recovery": recovery}
        time.sleep(10)
    return {"ok": False, "status": last, "error": "bridge_wait_timeout"}


def _wait_for_verdict(base_url: str, run_id: str, timeout_seconds: float, poll_seconds: float) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    last_verdict: dict[str, Any] = {}
    bridge_idle_since: float | None = None
    while time.time() < deadline:
        verdict = _http_json(f"{base_url}/api/judge/{run_id}/verdict", timeout=45)
        last_verdict = verdict
        if isinstance(verdict, dict) and (verdict.get("web_bridge") or verdict.get("answer_contract") or verdict.get("verdict_status")):
            return {"ok": True, "verdict": verdict}
        bridge = _http_json(f"{base_url}/api/bridge/status", timeout=20)
        active = _bridge_run_id(bridge)
        if not _bridge_busy(bridge) or (active and active != run_id):
            bridge_idle_since = bridge_idle_since or time.time()
            if time.time() - bridge_idle_since >= max(10.0, poll_seconds):
                verdict = _http_json(f"{base_url}/api/judge/{run_id}/verdict", timeout=45)
                if verdict.get("web_bridge") or verdict.get("answer_contract") or verdict.get("verdict_status"):
                    return {"ok": True, "verdict": verdict, "bridge": bridge}
                return {"ok": False, "error": "bridge_idle_without_verdict", "last_verdict": verdict, "bridge": bridge}
        else:
            bridge_idle_since = None
        time.sleep(poll_seconds)
    return {
        "ok": False,
        "error": "verdict_timeout",
        "last_verdict": last_verdict,
    }


def _write_attempt_report(report: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "_dry_run" if report.get("dry_run") else ""
    stem = f"{report['date']}_{report['round_id']}_attempt{report['attempt_no']}_single_seat_reruns{suffix}"
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    json_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    json_path.write_text(json_text, encoding="utf-8")
    if not report.get("dry_run"):
        (OUT_DIR / "latest_single_seat_reruns.json").write_text(json_text, encoding="utf-8")

    lines = [
        f"# PRED-INVEST Attempt {report['attempt_no']} Single-Seat Reruns · {report['round_id']}",
        "",
        f"- date: {report['date']}",
        f"- requested seats: {', '.join(report['requested_seats']) or 'none'}",
        f"- executed seats: {', '.join(row['seat'] for row in report['runs']) or 'none'}",
        f"- provider blocked skipped: {', '.join(report.get('provider_blocked_skipped') or []) or 'none'}",
        f"- final gate: {report.get('final_quality_gate', {}).get('status')} "
        f"({report.get('final_quality_gate', {}).get('valid_count')}/"
        f"{report.get('final_quality_gate', {}).get('required_seat_count')})",
        f"- publish allowed: {report.get('final_quality_gate', {}).get('publish_allowed')}",
        "",
        "## Seat Runs",
        "",
        "| Seat | Run ID | Submit | Wait | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["runs"]:
        lines.append(
            "| {seat} | {run_id} | {submit} | {wait} | {notes} |".format(
                seat=row["seat"],
                run_id=row.get("run_id") or "-",
                submit="ok" if row.get("submit_ok") else "fail",
                wait="ok" if row.get("wait_ok") else "fail",
                notes=str(row.get("error") or row.get("status") or "").replace("|", "/") or "-",
            )
        )
    salvage = report.get("page_salvage") or {}
    if salvage:
        lines += ["", "## Page Salvage", ""]
        lines.append(f"- ok: {salvage.get('ok')}")
        if salvage.get("error"):
            lines.append(f"- error: {salvage.get('error')} · {salvage.get('message')}")
        for row in salvage.get("responses") or []:
            lines.append(f"- {row.get('seat')}: {row.get('mode')} · ok={row.get('ok')} · chars={row.get('chars')}")
    lines += ["", "## Final Needs Rerun", ""]
    needs = report.get("final_quality_gate", {}).get("needs_rerun") or []
    lines.append("- " + (", ".join(needs) if needs else "none"))
    md_text = "\n".join(lines) + "\n"
    md_path.write_text(md_text, encoding="utf-8")
    if not report.get("dry_run"):
        (OUT_DIR / "latest_single_seat_reruns.md").write_text(md_text, encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def _capture_page_salvage(
    *,
    date: str,
    round_id: str,
    targets: list[str],
    endpoint: str,
) -> dict[str, Any]:
    """Capture visible page outputs, falling back to AI Judge's runtime venv.

    The daily repair script is often launched with system Python, while the
    Playwright dependency is installed in the AI Judge runtime venv. Treating
    the wrong interpreter as a hard failure caused recoverable page answers to
    be missed, so this helper makes the runtime interpreter the safety net.
    """
    try:
        return capture_pred_invest_page_salvage.capture_and_write(date, round_id, targets, endpoint)
    except Exception as direct_exc:
        direct_error = {"type": type(direct_exc).__name__, "message": str(direct_exc)}
        current_python = Path(sys.executable).resolve()
        if not RUNTIME_PYTHON.exists() or RUNTIME_PYTHON.resolve() == current_python:
            raise
        command = [
            str(RUNTIME_PYTHON),
            str(ROOT / "ops" / "capture_pred_invest_page_salvage.py"),
            "--date",
            date,
            "--round",
            round_id,
            "--seats",
            ",".join(targets),
            "--endpoint",
            endpoint,
            "--write",
        ]
        proc = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, timeout=120, env=_local_subprocess_env())
        if proc.returncode != 0:
            raise RuntimeError(
                "runtime_python_page_salvage_failed: "
                + json.dumps(
                    {
                        "direct_error": direct_error,
                        "returncode": proc.returncode,
                        "stdout": proc.stdout[-1200:],
                        "stderr": proc.stderr[-1200:],
                    },
                    ensure_ascii=False,
                )
            ) from direct_exc
        try:
            result = json.loads(proc.stdout)
        except Exception as parse_exc:
            raise RuntimeError(
                "runtime_python_page_salvage_non_json: "
                + json.dumps(
                    {
                        "direct_error": direct_error,
                        "stdout": proc.stdout[-1200:],
                        "stderr": proc.stderr[-1200:],
                    },
                    ensure_ascii=False,
                )
            ) from parse_exc
        result["fallback_python"] = str(RUNTIME_PYTHON)
        result["direct_error"] = direct_error
        return result


def _regenerate_artifacts(
    *,
    date: str,
    round_id: str,
    run_ids: list[str],
    base_url: str,
    bridge_base_url: str,
    recover_stuck_bridge: bool,
    stuck_seconds: float,
) -> dict[str, Any]:
    audit = audit_pred_invest_bridge_outputs.audit(date, round_id, run_ids)
    audit_paths = audit_pred_invest_bridge_outputs.write_report(audit)
    gate = pred_invest_quality_gate.build_gate(date, round_id, run_ids)
    gate_paths = pred_invest_quality_gate.write_gate(gate)
    guard = pred_invest_sop_guard.build_guard(
        date,
        round_id,
        run_ids,
        bridge_base_url=bridge_base_url,
        recover_stuck=recover_stuck_bridge,
        stuck_seconds=stuck_seconds,
    )
    guard_paths = pred_invest_sop_guard.write_guard(guard)
    daily_rc = run_pred_invest_daily_sop.main([
        "--date", date,
        "--round", round_id,
        "--base-url", base_url,
        "--bridge-base-url", bridge_base_url,
        "--runs", ",".join(run_ids),
        "--write",
    ])
    current_rc = build_pred_invest_current_game.main(["--date", date, "--round", round_id, "--write"])
    observer_paths: dict[str, str] = {}
    observer_error: dict[str, str] | None = None
    try:
        observer = generate_observer_ledger.build_observer_ledger(date, round_id, "pre", base_url)
        observer_paths = generate_observer_ledger.write_outputs(observer)
    except Exception as exc:
        # A partial bridge repair can legitimately have no seat archives yet.
        # Do not lose the new run ids or quality-gate output just because the
        # commentary layer has no publishable archive rows.
        observer_error = {
            "type": type(exc).__name__,
            "message": str(exc),
            "note": "observer ledger skipped; quality gate remains authoritative for partial reruns",
        }
    return {
        "audit": audit,
        "audit_paths": audit_paths,
        "quality_gate": gate,
        "quality_gate_paths": gate_paths,
        "sop_guard": guard,
        "sop_guard_paths": guard_paths,
        "daily_sop_return_code": daily_rc,
        "current_game_return_code": current_rc,
        "observer_paths": observer_paths,
        "observer_error": observer_error,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    base_url = args.bridge_base_url.rstrip("/")
    production_base_url = args.base_url.rstrip("/")
    run_ids = _parse_list(args.runs)
    if not run_ids:
        raise SystemExit("--runs is required so existing valid seats are preserved")

    gate = pred_invest_quality_gate.build_gate(args.date, args.round_id, run_ids)
    needs = set(gate.get("needs_rerun") or [])
    valid = set(gate.get("valid_seats") or [])
    provider_blocked = set(gate.get("provider_blocked_seats") or [])
    requested = _parse_list(args.seats) or list(DEFAULT_TARGET_SEATS)
    targets = []
    provider_blocked_skipped: list[str] = []
    for seat in requested:
        if seat in valid and not args.force_valid_seats:
            continue
        if seat not in needs and not args.force_valid_seats:
            continue
        if seat in provider_blocked and not args.force_provider_blocked:
            if seat not in provider_blocked_skipped:
                provider_blocked_skipped.append(seat)
            continue
        if seat not in targets:
            targets.append(seat)

    report: dict[str, Any] = {
        "version": "pred_invest_single_seat_reruns.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": args.date,
        "round_id": args.round_id,
        "attempt_no": args.attempt,
        "base_url": production_base_url,
        "bridge_base_url": base_url,
        "input_run_ids": run_ids[:],
        "requested_seats": requested,
        "initial_quality_gate": {
            "status": gate.get("status"),
            "valid_count": gate.get("valid_count"),
            "required_seat_count": gate.get("required_seat_count"),
            "valid_seats": gate.get("valid_seats") or [],
            "needs_rerun": gate.get("needs_rerun") or [],
        },
        "targets": targets,
        "provider_blocked_skipped": provider_blocked_skipped,
        "provider_blocked_policy": "skip ordinary rerun unless --force-provider-blocked is set",
        "runs": [],
    }
    if args.dry_run:
        report["dry_run"] = True
        report["paths"] = _write_attempt_report(report)
        return report

    for seat in targets:
        row: dict[str, Any] = {"seat": seat, "started_at": datetime.now(timezone.utc).isoformat()}
        ready = _wait_for_bridge_idle(base_url, recover_after=args.recover_after_seconds, wait_seconds=args.bridge_wait_seconds)
        row["bridge_ready"] = ready
        if not ready.get("ok"):
            row.update({"submit_ok": False, "wait_ok": False, "error": "bridge_not_idle"})
            report["runs"].append(row)
            report["paths"] = _write_attempt_report(report)
            continue
        receipt = submit(
            base_url,
            args.date,
            args.round_id,
            dry_run=False,
            requested_seats=[seat],
            compact=True,
            ultra_compact=True,
            attempt_no=args.attempt,
            judge_mode=args.judge_mode,
        )
        row["receipt"] = {
            key: receipt.get(key)
            for key in ("ok", "error", "selected_seats", "blocked_seats", "prompt_chars", "attempt_no")
        }
        response = receipt.get("response") if isinstance(receipt.get("response"), dict) else {}
        run_id = response.get("run_id")
        row["run_id"] = run_id
        row["submit_ok"] = bool(receipt.get("ok") and run_id)
        if not row["submit_ok"]:
            row["wait_ok"] = False
            row["error"] = receipt.get("error") or response.get("error") or "submit_failed"
            report["runs"].append(row)
            report["paths"] = _write_attempt_report(report)
            continue
        run_ids.append(str(run_id))
        wait = _wait_for_verdict(base_url, str(run_id), timeout_seconds=args.verdict_timeout_seconds, poll_seconds=args.poll_seconds)
        row["wait_ok"] = bool(wait.get("ok"))
        row["wait"] = {
            "ok": wait.get("ok"),
            "error": wait.get("error"),
            "progress": wait.get("progress") or wait.get("last_progress"),
        }
        if not wait.get("ok"):
            row["error"] = wait.get("error") or "wait_failed"
            recover = _wait_for_bridge_idle(base_url, recover_after=0, wait_seconds=30)
            row["post_timeout_recover"] = recover
        row["finished_at"] = datetime.now(timezone.utc).isoformat()
        report["runs"].append(row)
        report["paths"] = _write_attempt_report(report)

    if targets and not args.skip_page_salvage:
        try:
            salvage = _capture_page_salvage(
                date=args.date,
                round_id=args.round_id,
                targets=targets,
                endpoint=args.cdp_endpoint,
            )
            report["page_salvage"] = {
                "ok": True,
                "seats": salvage.get("seats"),
                "responses": [
                    {
                        "seat": row.get("seat"),
                        "ok": row.get("ok"),
                        "mode": row.get("mode"),
                        "chars": row.get("chars"),
                    }
                    for row in salvage.get("responses") or []
                ],
                "paths": salvage.get("paths"),
            }
        except Exception as exc:
            report["page_salvage"] = {
                "ok": False,
                "error": type(exc).__name__,
                "message": str(exc),
                "note": "Page salvage is best-effort; quality gate remains authoritative.",
            }
        report["paths"] = _write_attempt_report(report)

    artifacts = _regenerate_artifacts(
        date=args.date,
        round_id=args.round_id,
        run_ids=run_ids,
        base_url=production_base_url,
        bridge_base_url=base_url,
        recover_stuck_bridge=args.recover_stuck_bridge,
        stuck_seconds=args.recover_after_seconds,
    )
    report["final_run_ids"] = run_ids
    report["artifacts"] = {
        "audit": artifacts["audit_paths"],
        "quality_gate": artifacts["quality_gate_paths"],
        "sop_guard": artifacts["sop_guard_paths"],
        "observer": artifacts["observer_paths"],
        "observer_error": artifacts.get("observer_error"),
        "daily_sop_return_code": artifacts["daily_sop_return_code"],
        "current_game_return_code": artifacts["current_game_return_code"],
    }
    final_gate = artifacts["quality_gate"]
    report["final_quality_gate"] = {
        "status": final_gate.get("status"),
        "publish_allowed": final_gate.get("publish_allowed"),
        "valid_count": final_gate.get("valid_count"),
        "required_seat_count": final_gate.get("required_seat_count"),
        "valid_seats": final_gate.get("valid_seats") or [],
        "needs_rerun": final_gate.get("needs_rerun") or [],
    }
    report["paths"] = _write_attempt_report(report)
    return report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run PRED-INVEST single-seat reruns")
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--runs", required=True, help="Comma-separated existing AI Judge run ids.")
    parser.add_argument("--seats", default=",".join(DEFAULT_TARGET_SEATS), help="Comma-separated seats to consider.")
    parser.add_argument("--attempt", type=int, default=4)
    parser.add_argument("--judge-mode", default="quick_judge")
    parser.add_argument("--base-url", default="https://pool-app-one.vercel.app")
    parser.add_argument("--bridge-base-url", default="http://127.0.0.1:8501")
    parser.add_argument("--verdict-timeout-seconds", type=float, default=720.0)
    parser.add_argument("--poll-seconds", type=float, default=15.0)
    parser.add_argument("--bridge-wait-seconds", type=float, default=900.0)
    parser.add_argument("--recover-after-seconds", type=float, default=540.0)
    parser.add_argument("--recover-stuck-bridge", action="store_true")
    parser.add_argument("--force-valid-seats", action="store_true")
    parser.add_argument("--force-provider-blocked", action="store_true")
    parser.add_argument("--skip-page-salvage", action="store_true")
    parser.add_argument("--cdp-endpoint", default="http://127.0.0.1:9333")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = run(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    final_gate = report.get("final_quality_gate") or {}
    if args.dry_run:
        return 0
    return 0 if final_gate.get("publish_allowed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
