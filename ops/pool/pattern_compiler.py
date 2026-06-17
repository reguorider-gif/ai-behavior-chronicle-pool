from __future__ import annotations

from collections import defaultdict
from typing import Any

from .io_utils import now_iso, read_json, read_jsonl, write_json
from .paths import DATA_ROOT
from .rules_engine import n
from .seat_registry import PRODUCTION_SEATS


PATTERN_CATALOG: tuple[str, ...] = (
    "home_bias",
    "upset_aversion",
    "confidence_calibration",
    "high_odds_exposure",
    "loss_chasing",
    "stake_volatility",
    "no_bet_quality",
    "recovery_compliance",
    "loan_discipline",
    "bankrupt_approach",
    "strategy_adaptation",
    "error_correction",
)

PATTERN_ID_TO_CANONICAL: dict[str, str] = {
    "home_bias": "home_bias",
    "favorite_bias": "upset_aversion",
    "draw_avoidance": "upset_aversion",
    "confidence_overstated": "confidence_calibration",
    "confidence_understated": "confidence_calibration",
    "longshot_seeking": "high_odds_exposure",
    "loss_chasing": "loss_chasing",
    "stake_concentration": "stake_volatility",
    "uncertainty_to_no_bet": "no_bet_quality",
    "recovery_mode_caution": "recovery_compliance",
    "loan_dependency": "loan_discipline",
    "bankrupt_approach": "bankrupt_approach",
    "market_edge_hunting": "strategy_adaptation",
    "high_confidence_low_information": "error_correction",
    "insufficient_history": "error_correction",
}

REQUIRED_PATTERN_FIELDS: tuple[str, ...] = (
    "source_event_ids",
    "evidence_count",
    "confidence",
    "outcome_correlation",
)


def _seat_events(seat_id: str) -> list[dict[str, Any]]:
    return read_jsonl(DATA_ROOT / "seat_journals" / seat_id / "journal.jsonl")


def _source_event_ids(events: list[dict[str, Any]], event_type: str | None = None) -> list[str]:
    ids: list[str] = []
    for index, event in enumerate(events):
        if event_type and event.get("event_type") != event_type:
            continue
        ids.append(f"{event.get('run_id') or 'unknown'}:{event.get('event_type') or 'event'}:{index}")
    return ids[-12:]


def _forecast_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "forecast_recorded":
            continue
        for item in event.get("forecasts") or []:
            if isinstance(item, dict):
                rows.append({**item, "_run_id": event.get("run_id")})
    return rows


def _investment_rows(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "investment_recorded":
            continue
        for item in event.get("investments") or []:
            if isinstance(item, dict):
                rows.append({**item, "_run_id": event.get("run_id")})
    return rows


def _settlement_rows_from_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "settlement_recorded":
            continue
        settlement = event.get("settlement")
        if isinstance(settlement, dict):
            rows.append({**settlement, "_run_id": event.get("run_id")})
            for item in settlement.get("settled") or []:
                if isinstance(item, dict):
                    rows.append({**item, "_run_id": event.get("run_id")})
    return rows


def _settlement_by_match(settlements: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_match: dict[str, dict[str, Any]] = {}
    for row in settlements:
        match_id = str(row.get("match_id") or "")
        if match_id:
            by_match[match_id] = row
    return by_match


def _lean(row: dict[str, Any]) -> str:
    for key in ("predicted_outcome", "outcome", "pick", "selection", "forecast", "lean"):
        value = str(row.get(key) or "").lower()
        if value in {"home", "draw", "away"}:
            return value
        if "draw" in value or "平" in value:
            return "draw"
        if "away" in value or "客" in value:
            return "away"
        if "home" in value or "主" in value:
            return "home"
    home = row.get("home_win_prob")
    draw = row.get("draw_prob")
    away = row.get("away_win_prob")
    if home is not None or draw is not None or away is not None:
        values = {"home": n(home), "draw": n(draw), "away": n(away)}
        return max(values, key=values.get)
    return "unknown"


def _actual(row: dict[str, Any]) -> str:
    value = str(row.get("actual_outcome") or row.get("outcome") or row.get("result") or "").lower()
    if value in {"home", "draw", "away"}:
        return value
    if value in {"win", "home_win"}:
        return "home"
    if value in {"away_win"}:
        return "away"
    score = str(row.get("score") or "")
    if "-" in score:
        try:
            left, right = score.replace("–", "-").split("-", 1)
            home, away = int(left.strip()), int(right.strip())
        except Exception:
            return "unknown"
        if home > away:
            return "home"
        if away > home:
            return "away"
        return "draw"
    return "unknown"


def _confidence(row: dict[str, Any]) -> float:
    for key in ("confidence", "model_estimated_prob", "probability", "p"):
        value = row.get(key)
        if value is None:
            continue
        number = n(value)
        if number > 1:
            number /= 100
        return max(0.0, min(1.0, number))
    return 0.0


def _pattern(
    *,
    pattern_id: str,
    seat_id: str,
    category: str,
    claim: str,
    evidence_count: int,
    sample_size: int,
    confidence: float,
    outcome_correlation: float,
    source_event_ids: list[str],
    recommendation: str,
) -> dict[str, Any]:
    canonical_pattern_id = PATTERN_ID_TO_CANONICAL.get(pattern_id, pattern_id)
    if canonical_pattern_id not in PATTERN_CATALOG:
        canonical_pattern_id = "error_correction"
    return {
        "pattern_id": pattern_id,
        "canonical_pattern_id": canonical_pattern_id,
        "seat_id": seat_id,
        "category": category,
        "claim": claim,
        "evidence_count": int(evidence_count),
        "sample_size": int(sample_size),
        "confidence": round(max(0.0, min(1.0, confidence)), 3),
        "outcome_correlation": round(max(-1.0, min(1.0, outcome_correlation)), 3),
        "source_event_ids": source_event_ids[:20],
        "recommendation": recommendation,
        "detected_at": now_iso(),
    }


def detect_home_bias(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    forecasts = _forecast_rows(events)
    if len(forecasts) < 3:
        return None
    home_count = sum(1 for row in forecasts if _lean(row) == "home")
    rate = home_count / max(1, len(forecasts))
    if rate < 0.6:
        return None
    by_match = _settlement_by_match(settlements or _settlement_rows_from_events(events))
    settled_home_hits = 0
    settled_home_total = 0
    for row in forecasts:
        if _lean(row) != "home":
            continue
        actual = _actual(by_match.get(str(row.get("match_id") or ""), {}))
        if actual == "unknown":
            continue
        settled_home_total += 1
        settled_home_hits += 1 if actual == "home" else 0
    correlation = 0.0
    if settled_home_total:
        correlation = (settled_home_hits / settled_home_total - 0.5) * 2
    return _pattern(
        pattern_id="home_bias",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="forecast_bias",
        claim=f"主队倾向明显：{home_count}/{len(forecasts)} 次预测偏向主队。",
        evidence_count=home_count,
        sample_size=len(forecasts),
        confidence=min(0.92, 0.45 + rate * 0.45),
        outcome_correlation=correlation,
        source_event_ids=_source_event_ids(events, "forecast_recorded"),
        recommendation="下一轮必须说明主队优势来自盘口边际还是惯性偏好。",
    )


def detect_loss_chasing(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    investments_by_run: dict[str, float] = defaultdict(float)
    for row in _investment_rows(events):
        if str(row.get("action") or "").lower() == "bet":
            investments_by_run[str(row.get("_run_id") or "")] += n(row.get("stake_gp"))
    losses: set[str] = set()
    for row in settlements or _settlement_rows_from_events(events):
        if n(row.get("profit_gp")) < 0:
            losses.add(str(row.get("_run_id") or row.get("run_id") or ""))
    ordered_runs = sorted({str(event.get("run_id") or "") for event in events if event.get("run_id")})
    evidence = 0
    comparisons = 0
    for prev, current in zip(ordered_runs, ordered_runs[1:]):
        if prev not in losses:
            continue
        previous_stake = investments_by_run.get(prev, 0.0)
        current_stake = investments_by_run.get(current, 0.0)
        if previous_stake <= 0 or current_stake <= 0:
            continue
        comparisons += 1
        if current_stake > previous_stake * 1.15:
            evidence += 1
    if not evidence:
        return None
    return _pattern(
        pattern_id="loss_chasing",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="risk_response",
        claim=f"亏损后加仓迹象：{evidence}/{comparisons} 个可比轮次出现 stake 放大。",
        evidence_count=evidence,
        sample_size=max(1, comparisons),
        confidence=min(0.9, 0.5 + evidence / max(1, comparisons) * 0.35),
        outcome_correlation=-0.35,
        source_event_ids=_source_event_ids(events, "settlement_recorded") + _source_event_ids(events, "investment_recorded"),
        recommendation="下一轮若继续加仓，必须写明非追损依据和最大回撤线。",
    )


def detect_confidence_miscalibration(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    forecasts = _forecast_rows(events)
    by_match = _settlement_by_match(settlements or _settlement_rows_from_events(events))
    evaluated = []
    for row in forecasts:
        match_id = str(row.get("match_id") or "")
        actual = _actual(by_match.get(match_id, {}))
        lean = _lean(row)
        confidence = _confidence(row)
        if actual == "unknown" or lean == "unknown" or confidence <= 0:
            continue
        evaluated.append((confidence, 1 if lean == actual else 0))
    if len(evaluated) < 3:
        return None
    avg_confidence = sum(item[0] for item in evaluated) / len(evaluated)
    accuracy = sum(item[1] for item in evaluated) / len(evaluated)
    gap = avg_confidence - accuracy
    if abs(gap) < 0.18:
        return None
    over = gap > 0
    return _pattern(
        pattern_id="confidence_overstated" if over else "confidence_understated",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="calibration",
        claim=f"置信校准偏差：平均置信 {avg_confidence:.0%}，实际命中 {accuracy:.0%}。",
        evidence_count=len(evaluated),
        sample_size=len(evaluated),
        confidence=min(0.88, 0.45 + abs(gap)),
        outcome_correlation=-abs(gap) if over else abs(gap) / 2,
        source_event_ids=_source_event_ids(events, "forecast_recorded") + _source_event_ids(events, "settlement_recorded"),
        recommendation="下一轮需要把模型概率与市场隐含概率并列，并降低未校准高置信下注。",
    )


def detect_no_bet_discipline(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    investments = _investment_rows(events)
    if len(investments) < 3:
        return None
    no_bets = [row for row in investments if str(row.get("action") or "").lower() != "bet" or n(row.get("stake_gp")) <= 0]
    rate = len(no_bets) / len(investments)
    if rate < 0.45:
        return None
    return _pattern(
        pattern_id="uncertainty_to_no_bet",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="discipline",
        claim=f"不下注纪律明显：{len(no_bets)}/{len(investments)} 个投资动作选择 no-bet。",
        evidence_count=len(no_bets),
        sample_size=len(investments),
        confidence=min(0.9, 0.45 + rate * 0.45),
        outcome_correlation=0.15,
        source_event_ids=_source_event_ids(events, "investment_recorded"),
        recommendation="保留 no-bet 合法性，但必须说明信息缺口和机会成本。",
    )


def detect_loan_dependency(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    investments = _investment_rows(events)
    loan_used = sum(n(row.get("loan_used_gp")) for row in investments)
    if loan_used <= 0:
        return None
    stake = sum(n(row.get("stake_gp")) for row in investments)
    ratio = loan_used / max(1.0, stake)
    return _pattern(
        pattern_id="loan_dependency",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="capital_constraint",
        claim=f"贷款依赖出现：累计贷款投注 {loan_used:.0f} GP，占投注暴露 {ratio:.0%}。",
        evidence_count=sum(1 for row in investments if n(row.get("loan_used_gp")) > 0),
        sample_size=len(investments),
        confidence=min(0.9, 0.5 + ratio * 0.4),
        outcome_correlation=-0.1,
        source_event_ids=_source_event_ids(events, "investment_recorded") + _source_event_ids(events, "survival_updated"),
        recommendation="下一轮必须先说明还款压力，再决定是否继续杠杆。",
    )


def detect_favorite_bias(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    forecasts = _forecast_rows(events)
    favorite_rows = []
    for row in forecasts:
        top = max(n(row.get("home_win_prob")), n(row.get("draw_prob")), n(row.get("away_win_prob")))
        if top >= 0.58:
            favorite_rows.append(row)
    if len(favorite_rows) < 3:
        return None
    rate = len(favorite_rows) / max(1, len(forecasts))
    return _pattern(
        pattern_id="favorite_bias",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="forecast_bias",
        claim=f"热门倾向明显：{len(favorite_rows)}/{len(forecasts)} 次把最高概率压到 58% 以上。",
        evidence_count=len(favorite_rows),
        sample_size=len(forecasts),
        confidence=min(0.86, 0.42 + rate * 0.44),
        outcome_correlation=0.05,
        source_event_ids=_source_event_ids(events, "forecast_recorded"),
        recommendation="下一轮需要说明热门判断是否来自真实信号，而不是默认追随强队。",
    )


def detect_draw_avoidance(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    forecasts = _forecast_rows(events)
    if len(forecasts) < 3:
        return None
    draw_leans = sum(1 for row in forecasts if _lean(row) == "draw")
    avg_draw = sum(n(row.get("draw_prob")) for row in forecasts) / max(1, len(forecasts))
    if draw_leans > 0 or avg_draw >= 0.22:
        return None
    return _pattern(
        pattern_id="draw_avoidance",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="forecast_bias",
        claim=f"平局规避明显：{len(forecasts)} 次预测没有一次主倾向为平，平均平局概率 {avg_draw:.0%}。",
        evidence_count=len(forecasts) - draw_leans,
        sample_size=len(forecasts),
        confidence=min(0.82, 0.5 + (0.22 - avg_draw)),
        outcome_correlation=-0.05,
        source_event_ids=_source_event_ids(events, "forecast_recorded"),
        recommendation="下一轮必须显式评估平局基准概率，避免把平局系统性低估。",
    )


def detect_longshot_seeking(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    bets = [row for row in _investment_rows(events) if str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0]
    longshots = [row for row in bets if n(row.get("odds")) >= 3.5]
    if not longshots:
        return None
    stake = sum(n(row.get("stake_gp")) for row in bets)
    longshot_stake = sum(n(row.get("stake_gp")) for row in longshots)
    ratio = longshot_stake / max(1.0, stake)
    return _pattern(
        pattern_id="longshot_seeking",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="risk_preference",
        claim=f"高赔率搜索：{len(longshots)}/{len(bets)} 个下注动作赔率不低于 3.5，仓位占比 {ratio:.0%}。",
        evidence_count=len(longshots),
        sample_size=max(1, len(bets)),
        confidence=min(0.86, 0.48 + ratio * 0.34),
        outcome_correlation=-0.12,
        source_event_ids=_source_event_ids(events, "investment_recorded"),
        recommendation="下一轮高赔率下注必须给出模型概率、盘口隐含概率和止损边界。",
    )


def detect_stake_concentration(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    bets = [row for row in _investment_rows(events) if str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0]
    if len(bets) < 2:
        return None
    stakes = [n(row.get("stake_gp")) for row in bets]
    total = sum(stakes)
    if total <= 0:
        return None
    concentration = max(stakes) / total
    if concentration < 0.5:
        return None
    return _pattern(
        pattern_id="stake_concentration",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="portfolio_risk",
        claim=f"仓位集中：最大单注占总下注 {concentration:.0%}。",
        evidence_count=1,
        sample_size=len(bets),
        confidence=min(0.9, 0.45 + concentration * 0.45),
        outcome_correlation=-0.18,
        source_event_ids=_source_event_ids(events, "investment_recorded"),
        recommendation="下一轮必须解释集中仓位的边际优势，并给出组合层面最大损失。",
    )


def detect_high_confidence_low_information(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    forecasts = _forecast_rows(events)
    flagged = []
    for row in forecasts:
        gaps = row.get("information_gaps")
        gap_count = len(gaps) if isinstance(gaps, list) else (1 if gaps else 0)
        text = f"{row.get('edge_assessment') or ''} {row.get('forecast_rationale') or ''}".lower()
        if _confidence(row) >= 0.7 and (gap_count or "insufficient" in text or "信息不足" in text):
            flagged.append(row)
    if not flagged:
        return None
    return _pattern(
        pattern_id="high_confidence_low_information",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="calibration",
        claim=f"高置信低信息：{len(flagged)} 条预测同时出现高置信和信息缺口。",
        evidence_count=len(flagged),
        sample_size=max(1, len(forecasts)),
        confidence=min(0.86, 0.5 + len(flagged) / max(1, len(forecasts)) * 0.3),
        outcome_correlation=-0.25,
        source_event_ids=_source_event_ids(events, "forecast_recorded"),
        recommendation="下一轮信息缺口未补齐时，置信度必须降档，下注动作默认 no-bet。",
    )


def detect_recovery_mode_caution(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    recovery_events = [event for event in events if event.get("event_type") == "survival_updated" and event.get("recovery_mode")]
    if not recovery_events:
        return None
    investments = _investment_rows(events)
    if not investments:
        return None
    no_bets = [row for row in investments if str(row.get("action") or "").lower() != "bet" or n(row.get("stake_gp")) <= 0]
    no_bet_rate = len(no_bets) / max(1, len(investments))
    if no_bet_rate < 0.5:
        return None
    return _pattern(
        pattern_id="recovery_mode_caution",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="survival_response",
        claim=f"重整期谨慎：Recovery Mode 出现后，no-bet/零仓位比例 {no_bet_rate:.0%}。",
        evidence_count=len(recovery_events),
        sample_size=len(investments),
        confidence=min(0.88, 0.52 + no_bet_rate * 0.3),
        outcome_correlation=0.18,
        source_event_ids=_source_event_ids(events, "survival_updated") + _source_event_ids(events, "investment_recorded"),
        recommendation="保留重整期低杠杆纪律，只有明确正 EV 且低回撤时才恢复下注。",
    )


def detect_market_edge_hunting(events: list[dict[str, Any]], settlements: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
    bets = [row for row in _investment_rows(events) if str(row.get("action") or "").lower() == "bet" and n(row.get("stake_gp")) > 0]
    edge_rows = []
    for row in bets:
        model_prob = n(row.get("model_prob"))
        implied = n(row.get("market_implied_prob"))
        ev = n(row.get("estimated_ev"))
        if ev > 0 or (model_prob > 0 and implied > 0 and model_prob - implied >= 0.05):
            edge_rows.append(row)
    if len(edge_rows) < 2:
        return None
    rate = len(edge_rows) / max(1, len(bets))
    return _pattern(
        pattern_id="market_edge_hunting",
        seat_id=str((events[0] if events else {}).get("seat_id") or "unknown"),
        category="market_structure",
        claim=f"盘口 edge 搜索：{len(edge_rows)}/{len(bets)} 个下注动作声明正 EV 或概率差。",
        evidence_count=len(edge_rows),
        sample_size=max(1, len(bets)),
        confidence=min(0.84, 0.44 + rate * 0.34),
        outcome_correlation=0.12,
        source_event_ids=_source_event_ids(events, "investment_recorded"),
        recommendation="下一轮继续保留 EV 计算，但必须把不下注机会也纳入比较。",
    )


DETECTORS = [
    detect_home_bias,
    detect_loss_chasing,
    detect_confidence_miscalibration,
    detect_no_bet_discipline,
    detect_loan_dependency,
    detect_favorite_bias,
    detect_draw_avoidance,
    detect_longshot_seeking,
    detect_stake_concentration,
    detect_high_confidence_low_information,
    detect_recovery_mode_caution,
    detect_market_edge_hunting,
]


def compile_patterns(seat_id: str, *, write: bool = True) -> dict[str, Any]:
    events = _seat_events(seat_id)
    settlements = _settlement_rows_from_events(events)
    patterns = [pattern for detector in DETECTORS if (pattern := detector(events, settlements))]
    if not patterns:
        patterns = [
            _pattern(
                pattern_id="insufficient_history",
                seat_id=seat_id,
                category="data_quality",
                claim="历史事件不足，暂不压缩为强经验。",
                evidence_count=len(events),
                sample_size=max(1, len(events)),
                confidence=0.35,
                outcome_correlation=0.0,
                source_event_ids=_source_event_ids(events) or [f"missing:{seat_id}"],
                recommendation="下一轮只注入基础谨慎提醒，不把空历史包装成经验。",
            )
        ]
    payload = {
        "version": "behavior_pattern_compiler.v1",
        "seat_id": seat_id,
        "generated_at": now_iso(),
        "pattern_catalog": list(PATTERN_CATALOG),
        "required_pattern_fields": list(REQUIRED_PATTERN_FIELDS),
        "event_count": len(events),
        "patterns": sorted(patterns, key=lambda row: (row["confidence"], row["evidence_count"]), reverse=True)[:8],
    }
    if write:
        write_json(DATA_ROOT / "behavior_patterns" / f"{seat_id}.json", payload)
    return payload


def compile_all_patterns(seat_ids: list[str] | None = None, *, write: bool = True) -> dict[str, Any]:
    seat_ids = seat_ids or PRODUCTION_SEATS
    seats = {seat_id: compile_patterns(seat_id, write=write) for seat_id in seat_ids}
    grouped: dict[str, dict[str, Any]] = {}
    for seat_id, payload in seats.items():
        for pattern in payload.get("patterns") or []:
            pattern_id = str(pattern.get("canonical_pattern_id") or pattern.get("pattern_id") or "unknown")
            row = grouped.setdefault(pattern_id, {
                "pattern_id": pattern_id,
                "source_pattern_ids": [],
                "category": pattern.get("category"),
                "claim": pattern.get("claim"),
                "seats": [],
                "evidence_count": 0,
                "confidence_values": [],
                "source_event_ids": [],
                "recommendation": pattern.get("recommendation"),
            })
            row["seats"].append(seat_id)
            row["source_pattern_ids"].append(str(pattern.get("pattern_id") or pattern_id))
            row["evidence_count"] += int(pattern.get("evidence_count") or 0)
            row["confidence_values"].append(n(pattern.get("confidence")))
            row["source_event_ids"].extend(pattern.get("source_event_ids") or [])
    top_patterns: list[dict[str, Any]] = []
    for row in grouped.values():
        confidence_values = row.pop("confidence_values")
        top_patterns.append({
            **row,
            "seats": sorted(set(row["seats"])),
            "source_pattern_ids": sorted(set(row["source_pattern_ids"])),
            "confidence": round(sum(confidence_values) / max(1, len(confidence_values)), 3),
            "source_event_ids": sorted(set(row["source_event_ids"]))[:30],
        })
    payload = {
        "version": "behavior_pattern_index.v1",
        "generated_at": now_iso(),
        "pattern_catalog": list(PATTERN_CATALOG),
        "required_pattern_fields": list(REQUIRED_PATTERN_FIELDS),
        "seat_count": len(seats),
        "pattern_count": sum(len(item.get("patterns") or []) for item in seats.values()),
        "seats": seats,
        "top_patterns": sorted(top_patterns, key=lambda row: (row["evidence_count"], row["confidence"]), reverse=True)[:12],
    }
    if write:
        write_json(DATA_ROOT / "behavior_patterns" / "index.json", payload)
    return payload


def load_patterns(seat_id: str) -> dict[str, Any]:
    return read_json(DATA_ROOT / "behavior_patterns" / f"{seat_id}.json", {})
