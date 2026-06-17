from __future__ import annotations

from typing import Any

from .io_utils import now_iso, read_json, write_json
from .paths import DATA_ROOT
from .pattern_compiler import PRODUCTION_SEATS, compile_patterns
from .rules_engine import n


def _lesson_type(pattern: dict[str, Any]) -> str:
    correlation = n(pattern.get("outcome_correlation"))
    if correlation <= -0.2:
        return "avoid"
    if correlation >= 0.2:
        return "maintain"
    return "observe"


def _lesson_text(pattern: dict[str, Any], lesson_type: str) -> str:
    recommendation = str(pattern.get("recommendation") or "").strip()
    claim = str(pattern.get("claim") or "").strip()
    prefix = {
        "avoid": "避免复现",
        "maintain": "可以延续",
        "observe": "继续观察",
    }.get(lesson_type, "继续观察")
    return f"{prefix}：{recommendation or claim or pattern.get('pattern_id')}"


def compile_lessons(seat_id: str, *, write: bool = True) -> dict[str, Any]:
    patterns = read_json(DATA_ROOT / "behavior_patterns" / f"{seat_id}.json", {})
    if not patterns.get("patterns"):
        patterns = compile_patterns(seat_id, write=write)
    lessons = []
    for pattern in patterns.get("patterns") or []:
        if not isinstance(pattern, dict):
            continue
        lesson_type = _lesson_type(pattern)
        lessons.append({
            "lesson_id": f"{seat_id}:{pattern.get('pattern_id')}",
            "seat_id": seat_id,
            "type": lesson_type,
            "pattern_id": pattern.get("pattern_id"),
            "claim": pattern.get("claim"),
            "lesson": _lesson_text(pattern, lesson_type),
            "confidence": pattern.get("confidence"),
            "evidence_count": pattern.get("evidence_count"),
            "source_event_ids": pattern.get("source_event_ids") or [],
        })
    avoid = [item for item in lessons if item["type"] == "avoid"]
    maintain = [item for item in lessons if item["type"] == "maintain"]
    observe = [item for item in lessons if item["type"] == "observe"]
    injection_lines = ["行为通鉴经验（只来自你自己的历史）："]
    if avoid:
        injection_lines.append("必须规避：")
        injection_lines.extend(f"- {item['lesson']}" for item in avoid[:3])
    if maintain:
        injection_lines.append("可以延续：")
        injection_lines.extend(f"- {item['lesson']}" for item in maintain[:3])
    if observe:
        injection_lines.append("继续观察：")
        injection_lines.extend(f"- {item['lesson']}" for item in observe[:3])
    injection_lines.append("本轮输出必须说明：哪些历史经验被采用，哪些被拒绝，以及原因。")
    payload = {
        "version": "behavior_chronicle_lessons.v1",
        "seat_id": seat_id,
        "generated_at": now_iso(),
        "lesson_count": len(lessons),
        "lessons": lessons,
        "prompt_injection": "\n".join(injection_lines),
    }
    if write:
        root = DATA_ROOT / "behavior_chronicle" / seat_id
        write_json(root / "lessons.json", payload)
        md = [
            f"# {seat_id} 行为通鉴",
            "",
            f"- generated_at: {payload['generated_at']}",
            f"- lesson_count: {payload['lesson_count']}",
            "",
            "## Prompt Injection",
            "",
            payload["prompt_injection"],
            "",
            "## Lessons",
            "",
        ]
        for item in lessons:
            md.append(f"- [{item['type']}] {item['lesson']}（pattern={item['pattern_id']}, confidence={item['confidence']}）")
        (root / "chronicle.md").parent.mkdir(parents=True, exist_ok=True)
        (root / "chronicle.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return payload


def compile_all_lessons(seat_ids: list[str] | None = None, *, write: bool = True) -> dict[str, Any]:
    seat_ids = seat_ids or PRODUCTION_SEATS
    seats = {seat_id: compile_lessons(seat_id, write=write) for seat_id in seat_ids}
    payload = {
        "version": "behavior_chronicle_index.v1",
        "generated_at": now_iso(),
        "seat_count": len(seats),
        "lesson_count": sum(int(row.get("lesson_count") or 0) for row in seats.values()),
        "seats": seats,
    }
    if write:
        write_json(DATA_ROOT / "behavior_chronicle" / "index.json", payload)
    return payload


def generate_run_chronicle(date: str, run_id: str, seat_ids: list[str] | None = None, *, write: bool = True) -> dict[str, Any]:
    seat_ids = seat_ids or PRODUCTION_SEATS
    lesson_index = compile_all_lessons(seat_ids, write=write)
    lines = [
        f"# 上帝行为通鉴 · {date} · {run_id}",
        "",
        "这份通鉴不是原始流水账，而是把各席位的行为模式压缩成下一轮可复用经验。",
        "",
    ]
    highlights: list[dict[str, Any]] = []
    for seat_id, payload in (lesson_index.get("seats") or {}).items():
        lessons = payload.get("lessons") or []
        if not lessons:
            continue
        strongest = sorted(lessons, key=lambda item: (n(item.get("confidence")), n(item.get("evidence_count"))), reverse=True)[0]
        highlights.append({"seat_id": seat_id, **strongest})
        lines.append(f"- **{seat_id}**：{strongest.get('lesson')}（confidence={strongest.get('confidence')}）")
    payload = {
        "version": "run_behavior_chronicle.v1",
        "generated_at": now_iso(),
        "date": date,
        "run_id": run_id,
        "seat_count": len(seat_ids),
        "lesson_count": lesson_index.get("lesson_count", 0),
        "highlights": highlights,
        "markdown": "\n".join(lines) + "\n",
    }
    if write:
        write_json(DATA_ROOT / "behavior_chronicle" / "runs" / f"{run_id}.json", payload)
        path = DATA_ROOT / "behavior_chronicle" / "runs" / f"{run_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload["markdown"], encoding="utf-8")
    return payload
