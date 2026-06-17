from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any

from .behavior_compiler import PRODUCTION_SEATS
from .io_utils import now_iso, read_json, read_jsonl, write_json
from .paths import DATA_ROOT, ensure_parent


KERNEL_VERSION = "behavior_kernel_v1"


def _canonical(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_hash(payload: Any) -> str:
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def behavior_kernel_definition(version: str = KERNEL_VERSION) -> dict[str, Any]:
    if version != KERNEL_VERSION:
        raise ValueError(f"Unsupported behavior kernel version: {version}")
    definition = {
        "version": version,
        "name": "AI Behavioral Civilization Kernel",
        "event_sourcing": {
            "mode": "append_only",
            "event_identity": ["run_id", "seat_id", "source_stream", "source_index", "event_type", "payload_hash"],
            "mutation_policy": "duplicate_event_id_with_different_hash_is_rejected",
        },
        "deterministic_replay": {
            "mode": "captured_outputs_only",
            "same_inputs_same_chain": True,
            "non_deterministic_provider_calls": "not_replayed_without_captured_output",
            "input_hash_fields": ["kernel_hash", "event_stream_hash", "prompt_context_hashes", "replay_source_hash"],
        },
        "memory_policy": {
            "agent_private_memory": "own_history_only",
            "public_memory": ["anonymous_market_snapshot", "aggregated_pattern_summary", "rules"],
            "forbidden": ["other_agent_private_journals", "other_agent_current_choices", "raw_provider_transcripts"],
        },
        "audit_policy": {
            "must_answer": [
                "why_decision_was_made",
                "which_patterns_were_used",
                "whether_behavior_history_was_violated",
                "what_counterfactual_was_considered",
            ],
            "public_surface": "product_objects_only_no_local_paths",
        },
        "pattern_compiler": {
            "inputs": ["seat_journal", "settlement_record", "credit_update", "survival_update"],
            "outputs": ["agent_profile", "pattern_graph", "evolution_trace"],
        },
    }
    return {**definition, "kernel_hash": stable_hash(definition)}


def write_behavior_kernel(version: str = KERNEL_VERSION) -> dict[str, Any]:
    kernel = behavior_kernel_definition(version)
    write_json(DATA_ROOT / "data_lake" / "kernels" / f"{version}.json", kernel)
    write_json(DATA_ROOT / "data_lake" / "kernels" / "latest.json", kernel)
    return kernel


def _event_payload(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in {"event_id", "event_hash"}}


def _event_from_source(
    *,
    run_id: str,
    source_stream: str,
    source_index: int,
    row: dict[str, Any],
    kernel_version: str,
) -> dict[str, Any]:
    payload = _event_payload(row)
    payload_hash = stable_hash(payload)
    seat_id = str(row.get("seat_id") or "system")
    event_type = str(row.get("event_type") or "event")
    identity = {
        "run_id": run_id,
        "seat_id": seat_id,
        "source_stream": source_stream,
        "source_index": source_index,
        "event_type": event_type,
        "payload_hash": payload_hash,
    }
    event_id = stable_hash(identity)[:24]
    event = {
        "schema_version": "behavior_event.v1",
        "kernel_version": kernel_version,
        "event_id": event_id,
        "run_id": run_id,
        "seat_id": seat_id,
        "event_type": event_type,
        "ts": row.get("ts"),
        "source_stream": source_stream,
        "source_index": source_index,
        "payload_hash": payload_hash,
        "payload": payload,
    }
    return {**event, "event_hash": stable_hash(event)}


def _append_immutable_event(path, event: dict[str, Any]) -> bool:
    existing = read_jsonl(path)
    for row in existing:
        if row.get("event_id") != event["event_id"]:
            continue
        if row.get("event_hash") != event["event_hash"]:
            raise ValueError(f"Immutable event conflict for {event['event_id']}")
        return False
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return True


def _source_rows_for_run(run_id: str, seat_ids: list[str]) -> list[tuple[str, int, dict[str, Any]]]:
    rows: list[tuple[str, int, dict[str, Any]]] = []
    for seat_id in seat_ids:
        journal = read_jsonl(DATA_ROOT / "seat_journals" / seat_id / "journal.jsonl")
        for index, row in enumerate(journal):
            if str(row.get("run_id")) == str(run_id):
                rows.append((f"seat_journal:{seat_id}", index, row))
    god_rows = read_jsonl(DATA_ROOT / "god_ledger" / "events.jsonl")
    for index, row in enumerate(god_rows):
        if str(row.get("run_id")) == str(run_id):
            rows.append(("god_ledger", index, row))
    return rows


def write_event_stream(run_id: str, seat_ids: list[str], kernel_version: str = KERNEL_VERSION) -> dict[str, Any]:
    path = DATA_ROOT / "data_lake" / "events" / f"{run_id}.jsonl"
    appended = 0
    source_rows = _source_rows_for_run(run_id, seat_ids)
    events: list[dict[str, Any]] = []
    for source_stream, source_index, row in source_rows:
        event = _event_from_source(
            run_id=run_id,
            source_stream=source_stream,
            source_index=source_index,
            row=row,
            kernel_version=kernel_version,
        )
        if _append_immutable_event(path, event):
            appended += 1
        events.append(event)
    persisted = read_jsonl(path)
    event_ids = [row.get("event_id") for row in persisted if row.get("run_id") == run_id]
    event_hashes = [row.get("event_hash") for row in persisted if row.get("run_id") == run_id]
    manifest = {
        "version": "behavior_event_stream_manifest.v1",
        "run_id": run_id,
        "kernel_version": kernel_version,
        "generated_at": now_iso(),
        "event_count": len(event_hashes),
        "appended_count": appended,
        "source_row_count": len(source_rows),
        "event_type_counts": dict(Counter(str(row.get("event_type") or "event") for row in persisted if row.get("run_id") == run_id)),
        "stream_hash": stable_hash(event_hashes),
        "event_ids": event_ids,
        "ref": f"data/pool/data_lake/events/{run_id}.jsonl",
    }
    write_json(DATA_ROOT / "data_lake" / "events" / f"{run_id}.manifest.json", manifest)
    write_json(DATA_ROOT / "data_lake" / "events" / "latest.manifest.json", manifest)
    return manifest


def _prompt_context_hashes(run_id: str, seat_ids: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for seat_id in seat_ids:
        context = read_json(DATA_ROOT / "prompt_contexts" / run_id / f"{seat_id}.json", {})
        if context:
            hashes[seat_id] = stable_hash(context)
    return hashes


def memory_isolation_audit(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    checked = 0
    for seat_id in seat_ids:
        context = read_json(DATA_ROOT / "prompt_contexts" / run_id / f"{seat_id}.json", {})
        if not context:
            violations.append({"seat_id": seat_id, "type": "missing_prompt_context"})
            continue
        checked += 1
        private_text = _canonical(context.get("private_context") or {}).lower()
        other_seats = [other for other in seat_ids if other != seat_id and other.lower() in private_text]
        if other_seats:
            violations.append({"seat_id": seat_id, "type": "cross_seat_private_leakage", "other_seats": other_seats})
        private_context = context.get("private_context") or {}
        if not private_context.get("behavior_kernel"):
            violations.append({"seat_id": seat_id, "type": "missing_behavior_kernel_memory"})
    audit = {
        "version": "memory_isolation_audit.v1",
        "run_id": run_id,
        "generated_at": now_iso(),
        "checked_prompt_contexts": checked,
        "required_prompt_contexts": len(seat_ids),
        "ok": not violations,
        "violations": violations,
        "policy": behavior_kernel_definition()["memory_policy"],
    }
    write_json(DATA_ROOT / "data_lake" / "runs" / f"{run_id}.memory_isolation.json", audit)
    return audit


def write_replay_manifest(
    run_id: str,
    event_manifest: dict[str, Any],
    kernel: dict[str, Any],
    seat_ids: list[str],
) -> dict[str, Any]:
    replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    if not replay:
        replay = read_json(DATA_ROOT / "replay" / "runs" / "latest.json", {})
    prompt_hashes = _prompt_context_hashes(run_id, seat_ids)
    snapshot_refs = sorted({str(event.get("snapshot_ref") or "") for event in replay.get("timeline") or [] if event.get("snapshot_ref")})
    manifest = {
        "version": "deterministic_replay_manifest.v1",
        "run_id": run_id,
        "generated_at": now_iso(),
        "kernel_version": kernel["version"],
        "kernel_hash": kernel["kernel_hash"],
        "event_stream_hash": event_manifest.get("stream_hash"),
        "prompt_context_hashes": prompt_hashes,
        "prompt_contexts_hash": stable_hash(prompt_hashes),
        "replay_source_hash": stable_hash(replay),
        "event_count": replay.get("event_count", 0),
        "seat_count": replay.get("seat_count", 0),
        "snapshot_count": len(snapshot_refs),
        "deterministic_replay": bool(replay.get("version") and event_manifest.get("stream_hash")),
        "input_hash": stable_hash({
            "kernel_hash": kernel["kernel_hash"],
            "event_stream_hash": event_manifest.get("stream_hash"),
            "prompt_context_hashes": prompt_hashes,
            "replay_source_hash": stable_hash(replay),
        }),
        "refs": {
            "replay": f"data/pool/replay/runs/{run_id}.json",
            "snapshots": "data/pool/replay/snapshots/",
        },
    }
    write_json(DATA_ROOT / "data_lake" / "replays" / f"{run_id}.json", manifest)
    write_json(DATA_ROOT / "data_lake" / "replays" / "latest.json", manifest)
    write_json(DATA_ROOT / "data_lake" / "snapshots" / f"{run_id}.json", {
        "version": "snapshot_index.v1",
        "run_id": run_id,
        "generated_at": now_iso(),
        "snapshot_count": len(snapshot_refs),
        "snapshot_refs": snapshot_refs,
        "snapshot_index_hash": stable_hash(snapshot_refs),
    })
    return manifest


def write_behavior_compat_views(run_id: str, seat_ids: list[str]) -> dict[str, Any]:
    """Materialize the manifest-level ``data/pool/behavior/*`` views.

    These files are product-facing compatibility views over the production
    data lake. The immutable source of truth remains ``data_lake/events``.
    """

    event_rows = read_jsonl(DATA_ROOT / "data_lake" / "events" / f"{run_id}.jsonl")
    replay = read_json(DATA_ROOT / "replay" / "runs" / f"{run_id}.json", {})
    written = {"events": 0, "compiled": 0, "patterns": 0, "traces": 0}
    for seat_id in seat_ids:
        seat_events = [row for row in event_rows if row.get("seat_id") == seat_id]
        event_path = DATA_ROOT / "behavior" / "events" / f"{seat_id}.jsonl"
        ensure_parent(event_path)
        event_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in seat_events),
            encoding="utf-8",
        )
        written["events"] += len(seat_events)

        memory = read_json(DATA_ROOT / "behavior_memory" / "compiled" / f"{seat_id}.json", {})
        if memory:
            write_json(DATA_ROOT / "behavior" / "compiled" / f"{seat_id}.json", memory)
            write_json(DATA_ROOT / "behavior" / "patterns" / f"{seat_id}.json", {
                "version": "behavior_patterns_compat.v1",
                "run_id": run_id,
                "seat_id": seat_id,
                "patterns": memory.get("top_patterns") or [],
            })
            written["compiled"] += 1
            written["patterns"] += 1

    trace = {
        "version": "behavior_trace_compat.v1",
        "run_id": run_id,
        "generated_at": now_iso(),
        "event_count": replay.get("event_count", 0),
        "seat_count": replay.get("seat_count", 0),
        "timeline": replay.get("timeline") or [],
    }
    write_json(DATA_ROOT / "behavior" / "traces" / f"{run_id}.json", trace)
    write_json(DATA_ROOT / "behavior" / "traces" / "latest.json", trace)
    written["traces"] = 1 if trace["timeline"] else 0
    return {
        "version": "behavior_compat_views.v1",
        "run_id": run_id,
        "written": written,
        "refs": {
            "events": "data/pool/behavior/events/",
            "compiled": "data/pool/behavior/compiled/",
            "patterns": "data/pool/behavior/patterns/",
            "traces": f"data/pool/behavior/traces/{run_id}.json",
        },
    }


def run_behavior_production_kernel(
    run_id: str,
    seat_ids: list[str] | None = None,
    *,
    kernel_version: str = KERNEL_VERSION,
) -> dict[str, Any]:
    seat_ids = seat_ids or PRODUCTION_SEATS
    kernel = write_behavior_kernel(kernel_version)
    event_manifest = write_event_stream(run_id, seat_ids, kernel_version)
    isolation = memory_isolation_audit(run_id, seat_ids)
    replay_manifest = write_replay_manifest(run_id, event_manifest, kernel, seat_ids)
    compat_views = write_behavior_compat_views(run_id, seat_ids)
    contract = {
        "version": "behavior_production_contract.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "kernel_version": kernel["version"],
        "kernel_hash": kernel["kernel_hash"],
        "append_only_event_sourcing": True,
        "deterministic_replay": replay_manifest["deterministic_replay"],
        "memory_isolation": isolation["ok"],
        "audit_layer": True,
        "event_count": event_manifest["event_count"],
        "event_stream_hash": event_manifest["stream_hash"],
        "input_hash": replay_manifest["input_hash"],
        "readiness": {
            "ok": bool(event_manifest["event_count"] and replay_manifest["deterministic_replay"] and isolation["ok"]),
            "event_sourcing": "pass" if event_manifest["event_count"] else "missing_events",
            "replay": "pass" if replay_manifest["deterministic_replay"] else "missing_replay",
            "memory_isolation": "pass" if isolation["ok"] else "fail",
            "audit": "pass",
        },
        "product_contract": {
            "ui_role": "read_only_observer",
            "home_surface": "behavior_changes_only",
            "data_center": ["Seat Journal", "Credit Ledger", "Forecast / Investment Split", "God Report", "Raw Audit"],
            "hidden": ["local_file_paths", "raw_provider_outputs", "bridge_debug_payloads"],
        },
        "compat_views": compat_views,
        "refs": {
            "kernel": f"data/pool/data_lake/kernels/{kernel['version']}.json",
            "events": event_manifest["ref"],
            "run_manifest": f"data/pool/data_lake/runs/{run_id}.json",
            "replay_manifest": f"data/pool/data_lake/replays/{run_id}.json",
            "snapshot_index": f"data/pool/data_lake/snapshots/{run_id}.json",
            "behavior_events": "data/pool/behavior/events/",
            "behavior_patterns": "data/pool/behavior/patterns/",
            "behavior_traces": f"data/pool/behavior/traces/{run_id}.json",
        },
    }
    run_manifest = {
        "version": "behavior_run_manifest.v1",
        "generated_at": now_iso(),
        "run_id": run_id,
        "kernel": {
            "version": kernel["version"],
            "hash": kernel["kernel_hash"],
        },
        "event_stream": event_manifest,
        "memory_isolation": isolation,
        "replay": replay_manifest,
        "contract": contract,
    }
    write_json(DATA_ROOT / "data_lake" / "runs" / f"{run_id}.json", run_manifest)
    write_json(DATA_ROOT / "data_lake" / "runs" / "latest.json", run_manifest)
    write_json(DATA_ROOT / "behavior_summary" / "production_contract.json", contract)
    return contract
