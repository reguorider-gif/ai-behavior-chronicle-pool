from __future__ import annotations

from typing import Any

from ..behavior_compiler import build_pattern_graph, compile_behavior_memory


def build_graph(seat_ids: list[str], *, run_id: str | None = None, write: bool = True) -> dict[str, Any]:
    """Build the cross-agent behavior pattern graph."""

    compiled = {seat_id: compile_behavior_memory(seat_id, write=write) for seat_id in seat_ids}
    return build_pattern_graph(compiled, run_id=run_id, write=write)
