from __future__ import annotations

from typing import Any

from ..behavior_journal import append_seat_event
from ..io_utils import append_jsonl
from ..paths import DATA_ROOT


def log_event(seat_id: str, run_id: str, event: dict[str, Any]) -> dict[str, Any]:
    """Append one behavior event to the seat journal and compatibility stream."""

    event_type = str(event.get("event_type") or event.get("type") or "behavior_event")
    row = append_seat_event(seat_id, {"run_id": run_id, "event_type": event_type, **event})
    append_jsonl(DATA_ROOT / "behavior" / "events" / f"{seat_id}.jsonl", row)
    return row
