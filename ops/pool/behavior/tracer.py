from __future__ import annotations

from typing import Any

from ..behavior_replay import build_replay_for_run


def write_trace(run_id: str, seat_ids: list[str], *, write: bool = True) -> dict[str, Any]:
    """Build a deterministic behavior trace/replay for a run."""

    return build_replay_for_run(run_id, seat_ids, write=write)
