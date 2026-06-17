from __future__ import annotations

from typing import Any

from ..behavior_compiler import compile_behavior_memory
from ..io_utils import write_json
from ..paths import DATA_ROOT


def compile_state(seat_id: str, *, write: bool = True) -> dict[str, Any]:
    """Compile the current behavior state for one agent."""

    memory = compile_behavior_memory(seat_id, write=write)
    if write:
        write_json(DATA_ROOT / "behavior" / "compiled" / f"{seat_id}.json", memory)
    return memory


def compile_patterns(seat_id: str, *, write: bool = True) -> list[dict[str, Any]]:
    """Return top behavior patterns for one agent."""

    memory = compile_state(seat_id, write=write)
    patterns = memory.get("top_patterns") or []
    if write:
        write_json(DATA_ROOT / "behavior" / "patterns" / f"{seat_id}.json", {
            "version": "behavior_patterns_compat.v1",
            "seat_id": seat_id,
            "patterns": patterns,
        })
    return patterns
