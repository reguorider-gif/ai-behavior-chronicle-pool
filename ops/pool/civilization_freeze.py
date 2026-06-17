from __future__ import annotations

from typing import Any

from .behavior_production_kernel import KERNEL_VERSION
from .io_utils import now_iso, read_json, write_json
from .paths import DATA_ROOT
from .seat_registry import REQUIRED_SEAT_COUNT


ENGINE_VERSION = "AI_BEHAVIORAL_CIVILIZATION_ENGINE_V1"
FREEZE_VERSION = "behavior_civilization_freeze.v1"
READY_STATUS = "PRODUCTION_READY_BEHAVIOR_CIVILIZATION_ENGINE"
NOT_READY_STATUS = "NOT_READY_BEHAVIOR_CIVILIZATION_ENGINE"

FINAL_LOOP = [
    "event",
    "behavior_kernel",
    "pattern_generation",
    "memory_injection",
    "agent_decision",
    "economic_result",
    "audit_replay",
    "next_run",
]

ARCHITECTURE_LAYERS = [
    {
        "id": "world",
        "name": "World Layer",
        "responsibility": "matches, odds, market pressure and external events",
    },
    {
        "id": "agent",
        "name": "Agent Layer",
        "responsibility": "model memory, risk profile, credit state and behavior history",
    },
    {
        "id": "behavior_kernel",
        "name": "Behavior Kernel",
        "responsibility": "event store, pattern compiler, behavior graph, memory injector and drift detector",
    },
    {
        "id": "economic_system",
        "name": "Economic System",
        "responsibility": "credit, loan, survival pressure, bankruptcy constraints and ranking",
    },
    {
        "id": "audit_system",
        "name": "Audit System",
        "responsibility": "decision trace, causality graph, replay validator and pattern influence checker",
    },
    {
        "id": "civilization_map_ui",
        "name": "Civilization Map UI",
        "responsibility": "pressure field, behavior graph, agent identity, replay and hidden data center",
    },
]

FREEZE_ASSERTIONS = {
    "memory_influences_decision": "memory → decision is enforced by prompt memory audit",
    "pattern_influences_behavior": "pattern → behavior is enforced by pattern participation and sensitivity audit",
    "audit_validates_causality": "audit → causality is enforced by causal trace and graph checks",
    "replay_ensures_determinism": "replay → deterministic reconstruction is enforced by replay audit",
    "ui_visualizes_civilization_structure": "UI → civilization map is the primary public surface",
}


def _load_latest(run_id: str | None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    summary = read_json(DATA_ROOT / "behavior_summary" / "latest.json", {})
    resolved_run = run_id or summary.get("run_id") or "run-15"
    production = read_json(DATA_ROOT / "behavior_summary" / "production_contract.json", {})
    audit = read_json(DATA_ROOT / "behavior_audits" / f"{resolved_run}.json", {})
    if not audit:
        audit = read_json(DATA_ROOT / "behavior_audits" / "latest.json", {})
    civilization = read_json(DATA_ROOT / "civilization_state" / f"{resolved_run}.json", {})
    if not civilization:
        civilization = read_json(DATA_ROOT / "civilization_state" / "latest.json", {})
    battle = read_json(DATA_ROOT / "civilization_battle" / f"{resolved_run}.json", {})
    if not battle:
        battle = read_json(DATA_ROOT / "civilization_battle" / "latest.json", {})
    return summary, production, audit, civilization, battle


def _check_status(value: Any) -> bool:
    return str(value or "").lower() == "pass"


def _audit_checks(audit: dict[str, Any]) -> dict[str, str]:
    return ((audit.get("status") or {}).get("checks") or {}) if isinstance(audit, dict) else {}


def _evidence(
    *,
    production: dict[str, Any],
    audit: dict[str, Any],
    civilization: dict[str, Any],
    battle: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    checks = _audit_checks(audit)
    map_contract = civilization.get("map_contract") or {}
    agents = civilization.get("agents") or []
    causality_edges = ((civilization.get("causality") or {}).get("edges") or [])
    battle = battle or {}
    civilizations = battle.get("civilizations") or []
    interactions = battle.get("interactions") or []
    return {
        "memory_influences_decision": {
            "ok": _check_status(checks.get("prompt_control")),
            "source": "behavior_production_audit.status.checks.prompt_control",
            "value": checks.get("prompt_control"),
        },
        "pattern_influences_behavior": {
            "ok": _check_status(checks.get("pattern_participates")) and _check_status(checks.get("pattern_removal_changes_behavior")),
            "source": "behavior_production_audit.status.checks.pattern_participates + pattern_removal_changes_behavior",
            "value": {
                "pattern_participates": checks.get("pattern_participates"),
                "pattern_removal_changes_behavior": checks.get("pattern_removal_changes_behavior"),
            },
        },
        "audit_validates_causality": {
            "ok": _check_status(checks.get("causal_trace_complete")) and bool((audit.get("causality_graph") or {}).get("edge_count")),
            "source": "behavior_production_audit.status.checks.causal_trace_complete + causality_graph.edge_count",
            "value": {
                "causal_trace_complete": checks.get("causal_trace_complete"),
                "edge_count": (audit.get("causality_graph") or {}).get("edge_count"),
            },
        },
        "replay_ensures_determinism": {
            "ok": _check_status(checks.get("deterministic_replay")) and bool(production.get("deterministic_replay")),
            "source": "behavior_production_audit.status.checks.deterministic_replay + production_contract.deterministic_replay",
            "value": {
                "audit": checks.get("deterministic_replay"),
                "contract": production.get("deterministic_replay"),
            },
        },
        "ui_visualizes_civilization_structure": {
            "ok": map_contract.get("primary_ui") == "civilization_map" and len(agents) >= REQUIRED_SEAT_COUNT and bool(causality_edges),
            "source": "civilization_state.map_contract + agents + causality",
            "value": {
                "primary_ui": map_contract.get("primary_ui"),
                "agent_count": len(agents),
                "causality_edges": len(causality_edges),
            },
        },
        "event_store_append_only": {
            "ok": bool(production.get("append_only_event_sourcing")) and _check_status((production.get("readiness") or {}).get("event_sourcing")),
            "source": "production_contract.append_only_event_sourcing + readiness.event_sourcing",
            "value": {
                "append_only_event_sourcing": production.get("append_only_event_sourcing"),
                "readiness": (production.get("readiness") or {}).get("event_sourcing"),
            },
        },
        "memory_isolation": {
            "ok": bool(production.get("memory_isolation")) and _check_status((production.get("readiness") or {}).get("memory_isolation")),
            "source": "production_contract.memory_isolation + readiness.memory_isolation",
            "value": {
                "memory_isolation": production.get("memory_isolation"),
                "readiness": (production.get("readiness") or {}).get("memory_isolation"),
            },
        },
        "multi_civilization_layer": {
            "ok": len(civilizations) >= 2 and len(interactions) >= 1 and (battle.get("map_contract") or {}).get("primary_ui_extension") == "civilization_vs_civilization",
            "source": "civilization_battle.civilizations + interactions + map_contract",
            "value": {
                "civilization_count": len(civilizations),
                "interaction_count": len(interactions),
                "primary_ui_extension": (battle.get("map_contract") or {}).get("primary_ui_extension"),
            },
        },
    }


def _ready(evidence: dict[str, dict[str, Any]], audit: dict[str, Any], production: dict[str, Any]) -> bool:
    required = [
        "memory_influences_decision",
        "pattern_influences_behavior",
        "audit_validates_causality",
        "replay_ensures_determinism",
        "ui_visualizes_civilization_structure",
        "event_store_append_only",
        "memory_isolation",
        "multi_civilization_layer",
    ]
    return (
        all(bool(evidence.get(item, {}).get("ok")) for item in required)
        and (audit.get("status") or {}).get("verdict") == "PRODUCTION_READY"
        and bool((production.get("readiness") or {}).get("ok"))
    )


def build_civilization_freeze_manifest(
    run_id: str | None = None,
    *,
    behavior_summary: dict[str, Any] | None = None,
    production_contract: dict[str, Any] | None = None,
    production_audit: dict[str, Any] | None = None,
    civilization_state: dict[str, Any] | None = None,
    civilization_battle: dict[str, Any] | None = None,
    write: bool = True,
) -> dict[str, Any]:
    loaded_summary, loaded_production, loaded_audit, loaded_civilization, loaded_battle = _load_latest(run_id)
    summary = behavior_summary if behavior_summary is not None else loaded_summary
    production = production_contract if production_contract is not None else loaded_production
    audit = production_audit if production_audit is not None else loaded_audit
    civilization = civilization_state if civilization_state is not None else loaded_civilization
    battle = civilization_battle if civilization_battle is not None else loaded_battle
    resolved_run = run_id or summary.get("run_id") or production.get("run_id") or audit.get("run_id") or civilization.get("run_id")
    evidence = _evidence(production=production, audit=audit, civilization=civilization, battle=battle)
    ready = _ready(evidence, audit, production)
    manifest = {
        "version": FREEZE_VERSION,
        "generated_at": now_iso(),
        "run_id": resolved_run,
        "engine_version": ENGINE_VERSION,
        "kernel_version": production.get("kernel_version") or KERNEL_VERSION,
        "system_definition": "Behavior Civilization Simulation System",
        "system_formula": "multi-agent + economic pressure + memory + behavioral evolution",
        "final_status": READY_STATUS if ready else NOT_READY_STATUS,
        "ready": ready,
        "architecture_layers": ARCHITECTURE_LAYERS,
        "final_loop": FINAL_LOOP,
        "freeze_assertions": FREEZE_ASSERTIONS,
        "evidence": evidence,
        "public_surface_policy": {
            "primary_surface": "civilization_map",
            "home_rule": "show behavior structure and behavior change only",
            "data_center_rule": "show product health and drill-down surfaces only",
            "hide_by_default": ["odds", "bets", "ledger", "raw_logs", "local_paths", "provider_transcripts", "bridge_debug"],
            "api_contract": "product_objects_only_no_local_paths",
        },
        "validation": {
            "production_audit_verdict": (audit.get("status") or {}).get("verdict"),
            "production_audit_passed": (audit.get("status") or {}).get("passed"),
            "production_audit_partial": (audit.get("status") or {}).get("partial"),
            "kernel_ready": bool((production.get("readiness") or {}).get("ok")),
            "civilization_agent_count": len(civilization.get("agents") or []),
            "civilization_causality_edge_count": len(((civilization.get("causality") or {}).get("edges") or [])),
            "civilization_count": len(battle.get("civilizations") or []),
            "civilization_interaction_count": len(battle.get("interactions") or []),
        },
    }
    if write:
        write_json(DATA_ROOT / "civilization_freeze" / "latest.json", manifest)
        if resolved_run:
            write_json(DATA_ROOT / "civilization_freeze" / f"{resolved_run}.json", manifest)
    return manifest
