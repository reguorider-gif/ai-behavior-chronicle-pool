from __future__ import annotations

from collections import Counter
from typing import Any

from ..behavior_production_kernel import stable_hash
from ..io_utils import read_json
from ..paths import DATA_ROOT


def _status(ok: bool, partial: bool = False) -> str:
    if ok:
        return "pass"
    return "partial" if partial else "fail"


def validate_replay(run_id: str) -> dict[str, Any]:
    replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    manifest = read_json(DATA_ROOT / "data_lake" / "replays" / f"{run_id}.json", {})
    run_manifest = read_json(DATA_ROOT / "data_lake" / "runs" / f"{run_id}.json", {})
    contract = run_manifest.get("contract") or {}
    timeline = replay.get("timeline") or []
    replay_hash = stable_hash(replay) if replay else None
    ok = bool(
        replay.get("version")
        and manifest.get("deterministic_replay")
        and contract.get("deterministic_replay")
        and manifest.get("replay_source_hash") == replay_hash
    )
    return {
        "version": "replay_validator.v1",
        "run_id": run_id,
        "status": _status(ok),
        "event_count": replay.get("event_count", 0),
        "seat_count": replay.get("seat_count", 0),
        "snapshot_count": manifest.get("snapshot_count", 0),
        "input_hash": manifest.get("input_hash"),
        "timeline_event_types": dict(Counter(str(row.get("event_type") or "event") for row in timeline)),
        "replay_source_hash_matches": manifest.get("replay_source_hash") == replay_hash,
    }
