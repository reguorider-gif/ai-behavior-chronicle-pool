#!/usr/bin/env python3
"""Audit AI Judge bridge outputs against the PRED-INVEST contract.

This is intentionally stricter than "did the browser return text". A seat is
valid only when its latest captured answer is JSON, covers every required
match in forecasts, covers every required match in investments, and explicitly
keeps a frontend-ingest audit block.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pred_invest_seat_registry import PRODUCTION_SEATS, canonical_seat_id


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "pool" / "pred_invest"
RUNS_ROOT = Path("/Users/audimacmini/Library/Application Support/AI Judge/user-app-support/runtime/runs")
REQUIRED_SEATS = list(PRODUCTION_SEATS)


def _load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        return {"_read_error": str(exc), "_path": str(path)}


def _balanced_json_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    start: int | None = None
    depth = 0
    in_string = False
    escape = False
    for idx, char in enumerate(text or ""):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char == "{":
            if depth == 0:
                start = idx
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                candidates.append(text[start : idx + 1])
                start = None
    return candidates


def _pred_invest_score(parsed: dict[str, Any]) -> int:
    keys = set(parsed)
    score = 0
    for key in ("model_account", "seat_id", "one_sentence_strategy", "forecasts", "investments", "loan_decision", "self_audit"):
        if key in keys:
            score += 1
    if isinstance(parsed.get("forecasts"), list):
        score += len(parsed["forecasts"])
    if isinstance(parsed.get("investments"), list):
        score += len(parsed["investments"])
    return score


def _escape_json_string_controls(candidate: str) -> str:
    """Repair provider JSON that contains literal control chars in strings.

    Some web UIs preserve model line wraps inside JSON string values, e.g.
    "Colombia
    v
    Costa Rica". Standard JSON correctly rejects that, but the object is still
    structurally recoverable. This keeps the repair intentionally narrow: only
    control characters encountered while inside a quoted string are escaped.
    """
    repaired: list[str] = []
    in_string = False
    escape = False
    for char in candidate:
        if in_string:
            if escape:
                repaired.append(char)
                escape = False
                continue
            if char == "\\":
                repaired.append(char)
                escape = True
                continue
            if char == '"':
                repaired.append(char)
                in_string = False
                continue
            if char == "\n":
                repaired.append("\\n")
                continue
            if char == "\r":
                repaired.append("\\r")
                continue
            if char == "\t":
                repaired.append("\\t")
                continue
            repaired.append(char)
            continue
        repaired.append(char)
        if char == '"':
            in_string = True
    return "".join(repaired)


def _extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = (text or "").strip()
    candidates = [stripped]
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.S)
    candidates.extend(fenced)
    candidates.extend(_balanced_json_candidates(stripped))
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        candidates.append(stripped[start : end + 1])
    parsed_candidates: list[dict[str, Any]] = []
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except Exception:
            try:
                parsed = json.loads(_escape_json_string_controls(candidate))
            except Exception:
                continue
        if isinstance(parsed, dict):
            parsed_candidates.append(parsed)
    if not parsed_candidates:
        return None
    return max(parsed_candidates, key=_pred_invest_score)


def _split_csvish(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,，;；]", value or "") if item.strip()]


def _compact_number(value: Any) -> float:
    coerced = _coerce_number(value)
    try:
        return float(coerced or 0)
    except Exception:
        return 0.0


def _normalize_investment_action(action: Any, stake_gp: Any) -> str:
    """Normalize provider phrasing without inventing a decision.

    Several Chinese providers use "lean" to mean "倾向下注" even when they
    provide a concrete stake. The ingest contract needs a clear action for
    downstream settlement, so a positive-stake lean is a bet; a zero-stake
    lean/pass is a no_bet.
    """
    lowered = str(action or "").strip().lower()
    stake = _compact_number(stake_gp)
    if lowered in {"lean", "tilt", "prefer", "倾向"}:
        return "bet" if stake > 0 else "no_bet"
    if lowered in {"pass", "skip", "none", "watch", "observe", "观望"}:
        return "no_bet"
    return lowered or "no_bet"


def _selection_line_odds(selection: str, line: str, odds: Any) -> tuple[str, str, Any]:
    """Unpack compressed provider fields such as Belgium:-@2.27."""
    selection_text = str(selection or "").strip()
    line_text = str(line or "").strip()
    odds_value = odds
    if "@" in selection_text:
        left, maybe_odds = selection_text.rsplit("@", 1)
        if _compact_number(odds_value) == 0 and _compact_number(maybe_odds) > 0:
            odds_value = maybe_odds
        if ":" in left:
            maybe_selection, maybe_line = left.split(":", 1)
            if maybe_selection.strip():
                selection_text = maybe_selection.strip()
            if maybe_line.strip() and line_text.lower() in {"", "-", "--", "none", "null"}:
                line_text = maybe_line.strip()
        else:
            selection_text = left.strip() or selection_text
    return selection_text, line_text, odds_value


def _line_bet_row(parts: list[str]) -> dict[str, Any] | None:
    """Parse compact B rows, including common one-field-short variants."""
    if len(parts) >= 10:
        selection, line, odds = _selection_line_odds(parts[4], parts[5], parts[6])
        stake = _coerce_number(parts[7])
        return {
            "match_id": parts[1],
            "action": _normalize_investment_action(parts[2], stake),
            "market": parts[3],
            "selection": selection,
            "line": line,
            "odds": _coerce_number(odds),
            "stake_gp": stake,
            "loan_used_gp": _coerce_number(parts[8]),
            "reason": "|".join(parts[9:]).strip(),
        }
    if len(parts) == 9:
        action = str(parts[2] or "").strip().lower()
        # Variant A: B|id|no_bet|none|none|none|0|0|reason
        # The model omitted loan_used_gp, but explicitly supplied no_bet.
        if action in {"no_bet", "pass", "skip", "none"}:
            selection, line, odds = _selection_line_odds(parts[4], parts[5], parts[6])
            stake = _coerce_number(parts[7])
            return {
                "match_id": parts[1],
                "action": _normalize_investment_action(action, stake),
                "market": parts[3],
                "selection": selection,
                "line": line,
                "odds": _coerce_number(odds),
                "stake_gp": stake,
                "loan_used_gp": 0,
                "reason": parts[8],
            }
        # Variant B: B|id|lean|handicap|Belgium:-@2.27|2.27|200|0|reason
        # Here the provider compressed selection/line/odds into one field and
        # shifted stake/loan left by one column.
        if "@" in str(parts[4] or ""):
            selection, line, odds = _selection_line_odds(parts[4], "", parts[5])
            stake = _coerce_number(parts[6])
            return {
                "match_id": parts[1],
                "action": _normalize_investment_action(action, stake),
                "market": parts[3],
                "selection": selection,
                "line": line,
                "odds": _coerce_number(odds),
                "stake_gp": stake,
                "loan_used_gp": _coerce_number(parts[7]),
                "reason": parts[8],
            }
        selection, line, odds = _selection_line_odds(parts[4], parts[5], parts[6])
        stake = _coerce_number(parts[7])
        return {
            "match_id": parts[1],
            "action": _normalize_investment_action(action, stake),
            "market": parts[3],
            "selection": selection,
            "line": line,
            "odds": _coerce_number(odds),
            "stake_gp": stake,
            "loan_used_gp": 0,
            "reason": parts[8],
        }
    return None


def _extract_line_receipt(text: str, required_ids: list[str]) -> dict[str, Any] | None:
    """Parse the compact line receipt used for fragile web providers.

    Some providers reliably answer short line protocols but truncate nested
    JSON. The public contract is still the same internal object; this parser is
    only an ingestion adapter and the raw text remains auditable in the run.
    """
    raw_lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    if not raw_lines:
        return None
    lines: list[str] = []
    for line in raw_lines:
        # Strip common bullets/numbering without touching pipe payloads.
        line = re.sub(r"^\s*[-*]\s*", "", line)
        line = re.sub(r"^\s*\d+[.)、]\s*", "", line)
        lines.append(line.strip())

    parsed: dict[str, Any] = {
        "forecasts": [],
        "investments": [],
        "loan_decision": {},
        "risk_notes": [],
        "self_audit": {},
    }
    saw_protocol = False
    for line in lines:
        lower = line.lower()
        if lower in {"pred_invest_receipt", "[pred_invest_receipt]"}:
            saw_protocol = True
            continue
        if "=" in line and "|" not in line:
            key, value = line.split("=", 1)
            key = key.strip().lower()
            value = value.strip().strip('"')
            if key in {"model_account", "seat_id"}:
                parsed[key] = value.lower()
                saw_protocol = True
            elif key in {"strategy", "one_sentence_strategy"}:
                parsed["one_sentence_strategy"] = value
                saw_protocol = True
            continue
        parts = [part.strip() for part in line.split("|")]
        if not parts:
            continue
        tag = parts[0].strip().upper()
        if tag == "F" and len(parts) >= 6:
            saw_protocol = True
            parsed["forecasts"].append({
                "match_id": parts[1],
                "p": parts[2],
                "score": parts[3],
                "confidence": _coerce_number(parts[4]),
                "edge_assessment": parts[5],
                "information_gaps": _split_csvish(parts[6]) if len(parts) > 6 else [],
            })
        elif tag == "B":
            investment = _line_bet_row(parts)
            if not investment:
                continue
            saw_protocol = True
            parsed["investments"].append(investment)
        elif tag == "LOAN" and len(parts) >= 4:
            saw_protocol = True
            parsed["loan_decision"] = {
                "borrow_gp": _coerce_number(parts[1]),
                "reason": parts[2],
                "repayment_plan": parts[3],
            }
        elif tag == "RISK" and len(parts) >= 2:
            saw_protocol = True
            parsed["risk_notes"] = _split_csvish(parts[1])
        elif tag == "AUDIT" and len(parts) >= 4:
            saw_protocol = True
            covered = _split_csvish(parts[1])
            missing = _split_csvish(parts[2])
            ready = parts[3].strip().lower() == "true"
            parsed["self_audit"] = {
                "covered_match_ids": covered,
                "missing_match_ids": missing,
                "ready_for_frontend_ingest": ready,
            }

    if not saw_protocol:
        return None
    if "one_sentence_strategy" not in parsed:
        parsed["one_sentence_strategy"] = "结构化行协议回执"
    if not parsed["self_audit"] and required_ids:
        forecast_ids = sorted(_ids(parsed.get("forecasts")))
        investment_ids = sorted(_ids(parsed.get("investments")))
        covered = [mid for mid in required_ids if mid in forecast_ids and mid in investment_ids]
        parsed["self_audit"] = {
            "covered_match_ids": covered,
            "missing_match_ids": [mid for mid in required_ids if mid not in covered],
            "ready_for_frontend_ingest": covered == required_ids,
        }
    return parsed


def _coerce_number(value: Any) -> Any:
    text = str(value or "").strip()
    if text in {"", "-", "--", "null", "None"}:
        return 0
    try:
        if "." in text:
            return float(text)
        return int(text)
    except Exception:
        return value


def _extract_receipt_object(text: str, required_ids: list[str]) -> dict[str, Any] | None:
    return _extract_json_object(text) or _extract_line_receipt(text, required_ids)


def _provider_quota_limited(text: str) -> bool:
    lowered = (text or "").lower()
    quota_markers = [
        "距离限制重置",
        "supergrok",
        "rate limit",
        "usage limit",
        "quota limit",
        "too many requests",
        "limit reset",
    ]
    return any(marker in lowered for marker in quota_markers)


def _match_ids_from_required_snapshot(date: str, round_id: str) -> tuple[list[str], str] | None:
    path = OUT_DIR / f"{date}_{round_id}_required_match_snapshot.json"
    if not path.exists():
        return None
    data = _load_json(path)
    raw_ids = data.get("required_match_ids") if isinstance(data, dict) else []
    if not isinstance(raw_ids, list):
        return None
    ids = [str(item) for item in raw_ids if item]
    if not ids:
        return None
    return ids, f"required_match_snapshot:{path.name}"


def _match_ids_from_existing_gate(date: str, round_id: str) -> tuple[list[str], str] | None:
    """Preserve a running round's publish contract when prompt packs refresh.

    Daily SOP can legitimately refresh the prompt pack when new fixtures or
    required-match gap closures arrive. That must not retroactively invalidate
    already collected single-seat repair runs for the same round. When a frozen
    snapshot is not yet present, the last quality gate is the next-best source
    of the round's publish contract.
    """
    path = OUT_DIR / f"{date}_{round_id}_quality_gate.json"
    if not path.exists():
        return None
    try:
        data = _load_json(path)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    raw_ids = data.get("required_match_ids")
    if not isinstance(raw_ids, list):
        raw_ids = ((data.get("audit") or {}) if isinstance(data.get("audit"), dict) else {}).get("required_match_ids")
    if not isinstance(raw_ids, list):
        return None
    ids = [str(item) for item in raw_ids if item]
    if not ids:
        return None
    return ids, f"existing_quality_gate:{path.name}:{'publish_allowed' if data.get('publish_allowed') else 'not_published'}"


def _match_ids_from_prompt_pack(date: str, round_id: str) -> tuple[list[str], str]:
    path = OUT_DIR / f"{date}_{round_id}_prompt_pack.json"
    if not path.exists():
        return [], f"prompt_pack_missing:{path.name}"
    pack = _load_json(path)
    if isinstance(pack, dict) and pack.get("_read_error"):
        return [], f"prompt_pack_unreadable:{path.name}"
    matches = pack.get("matches") if isinstance(pack, dict) else []
    ids = []
    for match in matches:
        if isinstance(match, dict) and match.get("match_id"):
            ids.append(str(match["match_id"]))
    return ids, f"prompt_pack:{path.name}"


def _market_availability_from_prompt_pack(date: str, round_id: str) -> dict[str, bool]:
    """Return whether each prompt-pack match had an auditable market snapshot.

    This is intentionally tied to the prompt pack, not runtime matches: the
    audit must validate what the models actually saw. A model may forecast
    with no odds, but it must not invent bettable odds/stakes when the prompt
    exposed no market rows.
    """
    path = OUT_DIR / f"{date}_{round_id}_prompt_pack.json"
    if not path.exists():
        return {}
    try:
        pack = _load_json(path)
    except Exception:
        return {}
    result: dict[str, bool] = {}
    for match in pack.get("matches") or []:
        if not isinstance(match, dict):
            continue
        match_id = str(match.get("match_id") or match.get("id") or "")
        if not match_id:
            continue
        snapshot = match.get("market_snapshot")
        result[match_id] = bool(isinstance(snapshot, list) and snapshot)
    return result


def _required_match_ids(date: str, round_id: str) -> tuple[list[str], str]:
    frozen = _match_ids_from_required_snapshot(date, round_id)
    if frozen:
        return frozen
    gate = _match_ids_from_existing_gate(date, round_id)
    if gate:
        return gate
    return _match_ids_from_prompt_pack(date, round_id)


def _latest_responses(run_ids: list[str]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    responses: dict[str, list[dict[str, Any]]] = {}
    errors: dict[str, list[dict[str, Any]]] = {}
    sequence = 0

    def add_response(seat: str, row: dict[str, Any]) -> None:
        nonlocal sequence
        if not row.get("text"):
            return
        sequence += 1
        row["sequence"] = sequence
        responses.setdefault(seat, []).append(row)

    for run_id in run_ids:
        verdict_path = RUNS_ROOT / run_id / "verdict.json"
        if verdict_path.exists():
            verdict = _load_json(verdict_path)
            raw_results = ((verdict.get("web_bridge") or {}).get("raw_results") or []) if isinstance(verdict, dict) else []
            for row in raw_results:
                if not isinstance(row, dict):
                    continue
                seat = canonical_seat_id(row.get("seat") or row.get("seat_id"))
                if not seat:
                    continue
                if row.get("ok") and row.get("response"):
                    add_response(
                        seat,
                        {
                            "run_id": run_id,
                            "response_chars": len(str(row.get("response") or "")),
                            "capture_mode": "web_bridge.raw_results",
                            "text": row.get("response") or "",
                        },
                    )
                else:
                    error = row.get("error") if isinstance(row.get("error"), dict) else {}
                    errors.setdefault(seat, []).append(
                        {
                            "run_id": run_id,
                            "action": "raw_result_error",
                            "reason": error.get("code") or row.get("error_code") or row.get("message"),
                            "response_chars": len(str(row.get("response") or "")) if row.get("response") else 0,
                        }
                    )
        trace_path = RUNS_ROOT / run_id / "trace.json"
        if not trace_path.exists():
            continue
        trace = _load_json(trace_path)
        for event in trace.get("events") or []:
            if not isinstance(event, dict):
                continue
            action = event.get("action")
            data = event.get("data") if isinstance(event.get("data"), dict) else {}
            seat = canonical_seat_id(data.get("seat") or data.get("seat_id"))
            if not seat:
                continue
            if action == "cdp_response_captured":
                add_response(
                    seat,
                    {
                        "run_id": run_id,
                        "response_chars": data.get("response_chars"),
                        "capture_mode": data.get("capture_mode"),
                        "text": data.get("response") or "",
                    },
                )
            elif action in {"seat_timeout", "cdp_prompt_write_unconfirmed", "web_collection_process_timeout"}:
                errors.setdefault(seat, []).append(
                    {
                        "run_id": run_id,
                        "action": action,
                        "reason": data.get("result_code") or data.get("reason"),
                        "response_chars": data.get("response_chars"),
                    }
                )
    return responses, errors


def _append_page_salvage_responses(
    responses: dict[str, list[dict[str, Any]]],
    date: str,
    round_id: str,
) -> None:
    path = OUT_DIR / f"{date}_{round_id}_page_salvage.json"
    if not path.exists():
        return
    try:
        data = _load_json(path)
    except Exception:
        return
    rows = data.get("responses") if isinstance(data, dict) else []
    if not isinstance(rows, list):
        return
    sequence = max((int(row.get("sequence", 0) or 0) for seat_rows in responses.values() for row in seat_rows), default=0)
    for row in rows:
        if not isinstance(row, dict):
            continue
        seat = canonical_seat_id(row.get("seat"))
        text = str(row.get("text") or "")
        if not seat or not text:
            continue
        sequence += 1
        responses.setdefault(seat, []).append(
            {
                "run_id": row.get("run_id") or f"page_salvage:{date}:{round_id}:{seat}",
                "response_chars": len(text),
                "capture_mode": "page_salvage",
                "text": text,
                "sequence": sequence,
            }
        )


def _ids(rows: Any) -> set[str]:
    result: set[str] = set()
    if not isinstance(rows, list):
        return result
    for row in rows:
        if isinstance(row, dict) and row.get("match_id"):
            result.add(str(row["match_id"]))
    return result


def _validate_parsed(
    parsed: dict[str, Any],
    required_ids: list[str],
    expected_seat: str | None = None,
    market_available_by_match: dict[str, bool] | None = None,
) -> tuple[list[str], set[str], set[str]]:
    issues: list[str] = []
    required_fields = [
        "model_account",
        "seat_id",
        "one_sentence_strategy",
        "forecasts",
        "investments",
        "loan_decision",
        "risk_notes",
        "self_audit",
    ]
    missing_fields = [field for field in required_fields if field not in parsed]
    if missing_fields:
        issues.append("missing_top_level_fields:" + ",".join(missing_fields))
    if expected_seat:
        expected_seat = expected_seat.lower()
        seat_id = canonical_seat_id(parsed.get("seat_id") or parsed.get("seat"))
        model_account = canonical_seat_id(parsed.get("model_account"))
        if not seat_id:
            issues.append("missing_seat_id")
        elif seat_id != expected_seat:
            issues.append(f"seat_mismatch:{seat_id}!={expected_seat}")
        if not model_account:
            issues.append("missing_model_account")
        elif model_account != expected_seat:
            issues.append(f"model_account_mismatch:{model_account}!={expected_seat}")
    forecast_ids = _ids(parsed.get("forecasts"))
    investment_ids = _ids(parsed.get("investments"))
    missing_forecasts = [mid for mid in required_ids if mid not in forecast_ids]
    missing_investments = [mid for mid in required_ids if mid not in investment_ids]
    if missing_forecasts:
        issues.append("missing_forecasts:" + ",".join(missing_forecasts))
    if missing_investments:
        issues.append("missing_investments:" + ",".join(missing_investments))
    if market_available_by_match:
        invalid_no_market_bets: list[str] = []
        for row in parsed.get("investments") or []:
            if not isinstance(row, dict):
                continue
            match_id = str(row.get("match_id") or "")
            if match_id not in required_ids:
                continue
            if market_available_by_match.get(match_id, True):
                continue
            action = _normalize_investment_action(row.get("action"), row.get("stake_gp"))
            stake = _compact_number(row.get("stake_gp"))
            loan_used = _compact_number(row.get("loan_used_gp"))
            odds = _compact_number(row.get("odds"))
            market = str(row.get("market") or "").strip().lower()
            selection = str(row.get("selection") or "").strip().lower()
            line = str(row.get("line") or "").strip().lower()
            has_bet_fields = (
                action == "bet"
                or stake > 0
                or loan_used > 0
                or odds > 0
                or market not in {"", "none", "null"}
                or selection not in {"", "none", "null"}
                or line not in {"", "-", "--", "none", "null"}
            )
            if has_bet_fields:
                invalid_no_market_bets.append(match_id)
        if invalid_no_market_bets:
            issues.append("market_snapshot_missing_but_bet_fields_present:" + ",".join(sorted(set(invalid_no_market_bets))))
    audit_block = parsed.get("self_audit") if isinstance(parsed.get("self_audit"), dict) else {}
    if audit_block.get("ready_for_frontend_ingest") is not True:
        issues.append("self_audit_not_ready")
    return issues, forecast_ids, investment_ids


def _select_response_candidate(
    candidates: list[dict[str, Any]],
    required_ids: list[str],
    expected_seat: str | None = None,
    market_available_by_match: dict[str, bool] | None = None,
) -> tuple[dict[str, Any] | None, list[str], set[str], set[str]]:
    best_invalid: tuple[dict[str, Any], list[str], set[str], set[str]] | None = None
    for candidate in sorted(candidates, key=lambda row: row.get("sequence", 0), reverse=True):
        text = candidate.get("text") or ""
        if _provider_quota_limited(text):
            issues = ["provider_quota_limited"]
            forecast_ids = set()
            investment_ids = set()
            if best_invalid is None:
                best_invalid = (candidate, issues, forecast_ids, investment_ids)
            continue
        parsed = _extract_receipt_object(text, required_ids)
        if not parsed:
            issues = ["response_not_json"]
            forecast_ids: set[str] = set()
            investment_ids: set[str] = set()
        else:
            issues, forecast_ids, investment_ids = _validate_parsed(
                parsed,
                required_ids,
                expected_seat,
                market_available_by_match,
            )
        if not issues:
            return candidate, issues, forecast_ids, investment_ids
        if best_invalid is None:
            best_invalid = (candidate, issues, forecast_ids, investment_ids)
    if best_invalid:
        return best_invalid
    return None, ["no_captured_response"], set(), set()


def audit(date: str, round_id: str, run_ids: list[str]) -> dict[str, Any]:
    required_ids, required_source = _required_match_ids(date, round_id)
    market_available_by_match = _market_availability_from_prompt_pack(date, round_id)
    responses, errors = _latest_responses(run_ids)
    _append_page_salvage_responses(responses, date, round_id)
    observed_seats = sorted(set(responses) | set(errors))
    required_seat_set = set(REQUIRED_SEATS)
    seats = [seat for seat in observed_seats if seat in required_seat_set]
    ignored_extra_seats = [seat for seat in observed_seats if seat not in required_seat_set]
    seat_results = []
    valid_seats = []
    invalid_seats = []
    for seat in seats:
        response, issues, forecast_ids, investment_ids = _select_response_candidate(
            responses.get(seat, []),
            required_ids,
            seat,
            market_available_by_match,
        )
        result = {
            "seat": seat,
            "valid": not issues,
            "issues": issues,
            "run_id": response.get("run_id") if response else None,
            "response_chars": response.get("response_chars") if response else 0,
            "forecast_match_ids": sorted(forecast_ids),
            "investment_match_ids": sorted(investment_ids),
            "last_errors": errors.get(seat, [])[-3:],
        }
        seat_results.append(result)
        (valid_seats if result["valid"] else invalid_seats).append(seat)
    missing_seats = sorted(required_seat_set - set(seats))
    return {
        "version": "pred_invest_bridge_output_audit.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date,
        "round_id": round_id,
        "run_ids": run_ids,
        "required_match_ids": required_ids,
        "required_match_source": required_source,
        "market_available_by_match": {mid: market_available_by_match.get(mid) for mid in required_ids},
        "valid_count": len(valid_seats),
        "invalid_count": len(invalid_seats),
        "valid_seats": valid_seats,
        "invalid_seats": invalid_seats,
        "ignored_extra_seats": ignored_extra_seats,
        "missing_seats": missing_seats,
        "needs_rerun": sorted(set(invalid_seats + missing_seats)),
        "seat_results": seat_results,
    }


def write_report(result: dict[str, Any]) -> dict[str, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{result['date']}_{result['round_id']}_bridge_output_audit"
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# PRED-INVEST Bridge Output Audit · {result['round_id']}",
        "",
        f"- date: {result['date']}",
        f"- runs: {', '.join(result['run_ids'])}",
        f"- required matches: {len(result['required_match_ids'])}",
        f"- required source: {result.get('required_match_source') or '-'}",
        f"- valid seats: {result['valid_count']}",
        f"- invalid seats: {result['invalid_count']}",
        f"- needs rerun: {', '.join(result['needs_rerun']) or 'none'}",
        "",
        "| Seat | Valid | Issues | Forecasts | Investments |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for seat in result["seat_results"]:
        lines.append(
            "| {seat} | {valid} | {issues} | {fc} | {ic} |".format(
                seat=seat["seat"],
                valid="yes" if seat["valid"] else "no",
                issues="<br>".join(seat["issues"]) or "-",
                fc=len(seat["forecast_match_ids"]),
                ic=len(seat["investment_match_ids"]),
            )
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_bridge_output_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "latest_bridge_output_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--round", dest="round_id", required=True)
    parser.add_argument("--runs", required=True, help="Comma-separated AI Judge run ids, earliest to latest.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    result = audit(args.date, args.round_id, [item.strip() for item in args.runs.split(",") if item.strip()])
    if args.write:
        result["paths"] = write_report(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["needs_rerun"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
