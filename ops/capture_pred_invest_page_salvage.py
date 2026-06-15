#!/usr/bin/env python3
"""Capture visible provider-page answers that the bridge failed to ingest.

This is not a relaxed gate. It only writes raw page text candidates; the normal
PRED-INVEST audit still parses and validates JSON identity + match coverage.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
LOCAL_NO_PROXY = "127.0.0.1,localhost,::1"


def _force_local_no_proxy() -> None:
    os.environ["NO_PROXY"] = ",".join(filter(None, [os.environ.get("NO_PROXY"), LOCAL_NO_PROXY]))
    os.environ["no_proxy"] = ",".join(filter(None, [os.environ.get("no_proxy"), LOCAL_NO_PROXY]))
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
        os.environ.pop(key, None)

SEAT_URL_HINTS = {
    "chatgpt": ["chatgpt.com", "chat.openai.com"],
    "doubao": ["doubao.com/chat"],
    "gemini": ["gemini.google.com/app"],
    "grok": ["grok.com/"],
    "kimi": ["kimi.com/chat"],
    "meta": ["meta.ai"],
    "mimo": ["aistudio.xiaomimimo.com"],
    "minimax": ["agent.minimax.io"],
    "qwen": ["chat.qwen.ai", "tongyi.aliyun.com"],
    "wenxin": ["wenxin.baidu.com", "yiyan.baidu.com"],
    "yuanbao": ["yuanbao.tencent.com"],
}


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _parse_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def _extract_marked_answer(text: str, seat: str) -> tuple[str, str]:
    pattern = re.compile(
        rf"\[AIJUDGE_ANSWER_START:AIJUDGE-{re.escape(seat)}-[^\]]+\](.*?)\[AIJUDGE_ANSWER_END:AIJUDGE-{re.escape(seat)}-[^\]]+\]",
        flags=re.S | re.I,
    )
    matches = pattern.findall(text or "")
    usable = [item.strip() for item in matches if item.strip() and item.strip() not in {"你的最终答案", "(你的最终答案)"}]
    if usable:
        return usable[-1], "answer_marker"
    return (text or "").strip(), "page_text"


def _cdp_connect_endpoint(endpoint: str) -> str:
    """Return a Playwright-compatible CDP endpoint.

    Some locally launched Chrome builds return 400 for `/json/version/` while
    accepting `/json/version`. Playwright's HTTP endpoint path can hit the
    trailing-slash variant, so resolve the browser websocket ourselves.
    """
    text = str(endpoint or "").strip().rstrip("/")
    if text.startswith("ws://") or text.startswith("wss://"):
        return text
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(f"{text}/json/version", timeout=8) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
        ws = data.get("webSocketDebuggerUrl")
        if ws:
            return str(ws)
    except Exception:
        pass
    return str(endpoint or "")


async def _capture(endpoint: str, seats: list[str]) -> dict[str, Any]:
    _force_local_no_proxy()
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(_cdp_connect_endpoint(endpoint))
        responses: list[dict[str, Any]] = []
        pages = [page for ctx in browser.contexts for page in ctx.pages]
        for seat in seats:
            hints = SEAT_URL_HINTS.get(seat, [])
            candidates = [page for page in pages if any(hint in page.url for hint in hints)]
            if not candidates:
                responses.append({"seat": seat, "ok": False, "reason": "tab_not_found"})
                continue
            page = candidates[-1]
            try:
                text = await page.evaluate('() => document.body?.innerText || document.body?.textContent || ""')
                title = await page.title()
            except Exception as exc:
                responses.append({"seat": seat, "ok": False, "reason": "page_eval_failed", "error": str(exc), "url": page.url})
                continue
            answer, mode = _extract_marked_answer(text, seat)
            responses.append(
                {
                    "seat": seat,
                    "ok": bool(answer),
                    "mode": mode,
                    "title": title,
                    "url": page.url,
                    "chars": len(answer),
                    "run_id": f"page_salvage:{seat}",
                    "text": answer,
                }
            )
        await browser.close()
        return {"responses": responses}


def write_salvage(date: str, round_id: str, result: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{date}_{round_id}_page_salvage.json"
    latest = OUT_DIR / "latest_page_salvage.json"
    existing = _load_json(path)
    existing_rows = existing.get("responses") if isinstance(existing.get("responses"), list) else []
    merged_by_seat: dict[str, dict[str, Any]] = {}
    for row in existing_rows:
        if isinstance(row, dict) and row.get("seat"):
            merged_by_seat[str(row["seat"]).lower()] = row
    for row in result["responses"]:
        if isinstance(row, dict) and row.get("seat"):
            merged_by_seat[str(row["seat"]).lower()] = row
    merged = {
        **result,
        "responses": [merged_by_seat[seat] for seat in sorted(merged_by_seat)],
        "seats": sorted(merged_by_seat),
        "merge_note": "Write mode merges by seat so single-seat salvage does not delete other recovered page outputs.",
    }
    text = json.dumps(merged, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")
    latest.write_text(text, encoding="utf-8")
    return {"json": str(path), "latest_json": str(latest)}


def capture_and_write(date: str, round_id: str, seats: list[str], endpoint: str) -> dict[str, Any]:
    result = asyncio.run(_capture(endpoint, seats))
    result.update(
        {
            "version": "pred_invest_page_salvage.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "date": date,
            "round_id": round_id,
            "seats": seats,
            "note": "Raw provider-page candidates only; quality gate still validates structured JSON and coverage.",
        }
    )
    result["paths"] = write_salvage(date, round_id, result)
    return result


def main(argv: list[str] | None = None) -> int:
    _force_local_no_proxy()
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--seats", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:9333")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    seats = _parse_list(args.seats)
    result = asyncio.run(_capture(args.endpoint, seats))
    result.update(
        {
            "version": "pred_invest_page_salvage.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "date": args.date,
            "round_id": args.round_id,
            "seats": seats,
            "note": "Raw provider-page candidates only; quality gate still validates structured JSON and coverage.",
        }
    )
    if args.write:
        result["paths"] = write_salvage(args.date, args.round_id, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
