const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();
const POOL_ROOT = path.join(ROOT, "data", "pool");

async function readText(relPath) {
  try {
    return await fs.readFile(path.join(POOL_ROOT, relPath), "utf8");
  } catch (_error) {
    return "";
  }
}

async function readJson(relPath, fallback = {}) {
  const raw = await readText(relPath);
  if (!raw) return fallback;
  try {
    return JSON.parse(raw);
  } catch (_error) {
    return fallback;
  }
}

function send(res, status, payload) {
  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.status(status).send(JSON.stringify(payload, null, 2));
}

function parts(req) {
  const value = req.query.path;
  if (Array.isArray(value)) return value.map(String);
  if (typeof value === "string" && value) return value.split("/");
  return [];
}

async function latestRunId(fallback) {
  const summary = await readJson(path.join("behavior_summary", "latest.json"));
  return summary.run_id || fallback || "run-15";
}

async function behaviorHome(res) {
  const summary = await readJson(path.join("behavior_summary", "latest.json"));
  const profiles = await readJson(path.join("agent_profiles", "latest.json"), { seats: {} });
  const seats = Object.values(profiles.seats || {});
  const shifts = {
    aggressive: seats.filter((seat) => seat.strategy_drift === "aggressive_shift").length,
    risk_reduction: seats.filter((seat) => seat.strategy_drift === "risk_reduction").length,
    loan_pressure: seats.filter((seat) => ["high", "medium"].includes(seat.loan_dependency)).length,
  };
  send(res, summary.run_id ? 200 : 404, {
    ok: Boolean(summary.run_id),
    version: "behavior_home.v1",
    run_id: summary.run_id || null,
    rule_version: summary.rule_version || null,
    generated_at: summary.generated_at || null,
    counts: summary.counts || {},
    readiness: summary.readiness || {},
    shifts,
    key_agents: seats.slice(0, 5).map((seat) => ({
      seat_id: seat.seat_id,
      behavior_type: seat.behavior_type,
      risk_level: seat.risk_level,
      loan_dependency: seat.loan_dependency,
      strategy_drift: seat.strategy_drift,
    })),
  });
}

async function behaviorTimeline(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let replay = await readJson(path.join("replay", "runs", `${resolvedRun}.json`));
  if (!replay.version) replay = await readJson(path.join("replay", "runs", "latest.json"));
  const lanes = Object.entries(replay.seat_index || {}).map(([seat_id, event_ids]) => ({
    seat_id,
    event_ids,
    events: (replay.timeline || [])
      .filter((event) => event.seat_id === seat_id)
      .map((event) => ({
        event_id: event.event_id,
        run_id: event.run_id,
        action: event.action,
        outcome: event.outcome,
        risk_shift: event.risk_shift,
        state_before: event.state_before,
        state_after: event.state_after,
        decision_reconstruction: event.decision_reconstruction,
        counterfactual: event.counterfactual,
      })),
  }));
  send(res, replay.version ? 200 : 404, {
    ok: Boolean(replay.version),
    version: "behavior_timeline.v1",
    run_id: replay.run_id || resolvedRun,
    event_count: replay.event_count || 0,
    seat_count: replay.seat_count || lanes.length,
    lanes,
  });
}

async function behaviorGraph(res) {
  const graph = await readJson(path.join("pattern_graph", "latest.json"));
  send(res, graph.version ? 200 : 404, {
    ok: Boolean(graph.version),
    version: "behavior_graph.v1",
    run_id: graph.run_id || null,
    generated_at: graph.generated_at || null,
    patterns: (graph.top_patterns || []).slice(0, 5).map((pattern) => ({
      id: pattern.pattern_id || pattern.name || pattern.label,
      name: pattern.label || pattern.name,
      confidence: pattern.confidence,
      supporting_events: pattern.supporting_events,
      seats: pattern.seats || [],
      note: pattern.note || "",
    })),
  });
}

async function behaviorCivilization(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let state = await readJson(path.join("civilization_state", `${resolvedRun}.json`));
  if (!state.version) state = await readJson(path.join("civilization_state", "latest.json"));
  send(res, state.version ? 200 : 404, {
    ok: Boolean(state.version),
    version: "behavior_civilization_api.v1",
    run_id: state.run_id || resolvedRun,
    generated_at: state.generated_at || null,
    pressure: state.pressure || {},
    agents: state.agents || [],
    positions: state.positions || {},
    drift: state.drift || {},
    archetypes: state.archetypes || {},
    behavior_flow: state.behavior_flow || [],
    causality: state.causality || {},
    map_contract: state.map_contract || {},
  });
}

async function behaviorCivilizationBattle(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let battle = await readJson(path.join("civilization_battle", `${resolvedRun}.json`));
  if (!battle.version) battle = await readJson(path.join("civilization_battle", "latest.json"));
  send(res, battle.version ? 200 : 404, {
    ok: Boolean(battle.version),
    version: "behavior_civilization_battle_api.v9",
    run_id: battle.run_id || resolvedRun,
    generated_at: battle.generated_at || null,
    engine: battle.engine || {},
    civilization_models: battle.civilization_models || [],
    civilizations: battle.civilizations || [],
    interactions: battle.interactions || [],
    headline_battle: battle.headline_battle || {},
    interaction_graph: battle.interaction_graph || {},
    evolution_timeline: battle.evolution_timeline || [],
    civilization_timeline: battle.civilization_timeline || [],
    clash_view: battle.clash_view || [],
    drift_engine: battle.drift_engine || {},
    collapse_signals: battle.collapse_signals || [],
    dynamics: battle.dynamics || {},
    phase_transitions: battle.phase_transitions || {},
    civilization_field: battle.civilization_field || {},
    war_engine: battle.war_engine || {},
    war_phase_engine: battle.war_phase_engine || {},
    meta_layer: battle.meta_layer || {},
    memory_dynamics: battle.memory_dynamics || {},
    genome_engine: battle.genome_engine || {},
    meta_civilization: battle.meta_civilization || {},
    universe: battle.universe || {},
    multiverse: battle.multiverse || {},
    physics_core: battle.physics_core || {},
    fate_curve: battle.fate_curve || [],
    meta_strategy: battle.meta_strategy || {},
    map_contract: battle.map_contract || {},
  });
}

async function behaviorAgents(res) {
  const profiles = await readJson(path.join("agent_profiles", "latest.json"), { seats: {} });
  send(res, Object.keys(profiles.seats || {}).length ? 200 : 404, {
    ok: Object.keys(profiles.seats || {}).length > 0,
    version: "behavior_agents.v1",
    run_id: profiles.run_id || null,
    generated_at: profiles.generated_at || null,
    agents: Object.values(profiles.seats || {}).map((seat) => ({
      seat_id: seat.seat_id,
      behavior_type: seat.behavior_type,
      risk_level: seat.risk_level,
      loan_dependency: seat.loan_dependency,
      no_bet_rate: seat.no_bet_rate,
      strategy_drift: seat.strategy_drift,
      timeline_events: seat.timeline_events || [],
      top_patterns: seat.top_patterns || [],
    })),
  });
}

async function behaviorAgent(res, seatId) {
  const id = String(seatId || "").toLowerCase();
  const profiles = await readJson(path.join("agent_profiles", "latest.json"), { seats: {} });
  const profile = (profiles.seats || {})[id] || null;
  const memory = await readJson(path.join("behavior_memory", "compiled", `${id}.json`));
  const replay = await readJson(path.join("replay", "runs", "latest.json"));
  const events = (replay.timeline || []).filter((event) => event.seat_id === id);
  send(res, profile || memory.version ? 200 : 404, {
    ok: Boolean(profile || memory.version),
    version: "behavior_agent.v1",
    run_id: profiles.run_id || replay.run_id || null,
    seat_id: id || null,
    profile,
    memory: memory.version ? {
      version: memory.version,
      profile: memory.profile || {},
      top_patterns: memory.top_patterns || [],
      recent_timeline_events: memory.recent_timeline_events || [],
      memory_contract: memory.memory_contract || {},
    } : null,
    replay_events: events,
  });
}

async function behaviorReplay(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let replay = await readJson(path.join("replay", "runs", `${resolvedRun}.json`));
  if (!replay.version) replay = await readJson(path.join("replay", "runs", "latest.json"));
  send(res, replay.version ? 200 : 404, {
    ok: Boolean(replay.version),
    version: "behavior_replay_api.v1",
    run_id: replay.run_id || resolvedRun,
    event_count: replay.event_count || 0,
    seat_count: replay.seat_count || 0,
    timeline: replay.timeline || [],
    seat_index: replay.seat_index || {},
  });
}

async function behaviorTrace(res, eventId) {
  const id = String(eventId || "");
  const replay = await readJson(path.join("replay", "runs", "latest.json"));
  const event = (replay.timeline || []).find((row) => row.event_id === id);
  send(res, event ? 200 : 404, {
    ok: Boolean(event),
    version: "behavior_trace.v1",
    run_id: replay.run_id || null,
    event_id: id || null,
    trace: event || null,
  });
}

async function behaviorPatterns(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let graph = await readJson(path.join("pattern_graph", `${resolvedRun}.json`));
  if (!graph.version) graph = await readJson(path.join("pattern_graph", "latest.json"));
  send(res, graph.version ? 200 : 404, {
    ok: Boolean(graph.version),
    version: "behavior_patterns_api.v1",
    run_id: graph.run_id || resolvedRun,
    generated_at: graph.generated_at || null,
    patterns: graph.top_patterns || [],
  });
}

async function behaviorDataCenter(res) {
  const summary = await readJson(path.join("behavior_summary", "latest.json"));
  const production = await readJson(path.join("data_lake", "runs", "latest.json"));
  const audit = await readJson(path.join("behavior_audits", "latest.json"));
  const contract = production.contract || {};
  const counts = summary.counts || {};
  send(res, summary.run_id ? 200 : 404, {
    ok: Boolean(summary.run_id),
    version: "behavior_datacenter.v1",
    run_id: summary.run_id || null,
    rule_version: summary.rule_version || null,
    entries: [
      { id: "journal", label: "Seat Journal", count: counts.seat_journal_count || 0 },
      { id: "credit", label: "Credit Ledger", ready: Boolean(counts.prompt_context_count) },
      { id: "split", label: "Forecast / Investment Split", forecast_count: counts.forecast_receipt_count || 0, investment_count: counts.investment_receipt_count || 0 },
      { id: "god", label: "God Report", count: counts.god_report_seat_count || 0 },
      { id: "audit", label: "Raw Audit", behavior_memory_count: counts.behavior_memory_count || 0, replay_event_count: counts.replay_event_count || 0, production_ready: Boolean(contract.readiness && contract.readiness.ok), production_audit: (audit.status || {}).verdict || null },
    ],
  });
}

async function behaviorProduction(res, runId) {
  const resolvedRun = await latestRunId(runId);
  const run = await readJson(path.join("data_lake", "runs", `${resolvedRun}.json`));
  const latest = run.version ? run : await readJson(path.join("data_lake", "runs", "latest.json"));
  const contract = latest.contract || {};
  send(res, contract.version ? 200 : 404, {
    ok: Boolean(contract.version),
    version: "behavior_production_api.v1",
    run_id: contract.run_id || latest.run_id || resolvedRun,
    kernel_version: contract.kernel_version || null,
    kernel_hash: contract.kernel_hash || null,
    append_only_event_sourcing: Boolean(contract.append_only_event_sourcing),
    deterministic_replay: Boolean(contract.deterministic_replay),
    memory_isolation: Boolean(contract.memory_isolation),
    audit_layer: Boolean(contract.audit_layer),
    event_count: contract.event_count || 0,
    input_hash: contract.input_hash || null,
    readiness: contract.readiness || {},
    product_contract: contract.product_contract || {},
  });
}

async function behaviorAudit(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let audit = await readJson(path.join("behavior_audits", `${resolvedRun}.json`));
  if (!audit.version) audit = await readJson(path.join("behavior_audits", "latest.json"));
  send(res, audit.version ? 200 : 404, {
    ok: Boolean(audit.version),
    version: "behavior_audit_api.v1",
    run_id: audit.run_id || resolvedRun,
    kernel_version: audit.kernel_version || null,
    status: audit.status || {},
    sections: audit.sections || {},
    causality_graph: audit.causality_graph || {},
  });
}

async function behaviorFreeze(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let freeze = await readJson(path.join("civilization_freeze", `${resolvedRun}.json`));
  if (!freeze.version) freeze = await readJson(path.join("civilization_freeze", "latest.json"));
  send(res, freeze.version ? 200 : 404, {
    ok: Boolean(freeze.version),
    version: "behavior_freeze_api.v1",
    run_id: freeze.run_id || resolvedRun,
    generated_at: freeze.generated_at || null,
    engine_version: freeze.engine_version || null,
    kernel_version: freeze.kernel_version || null,
    system_definition: freeze.system_definition || null,
    final_status: freeze.final_status || "UNKNOWN",
    ready: Boolean(freeze.ready),
    architecture_layers: freeze.architecture_layers || [],
    final_loop: freeze.final_loop || [],
    freeze_assertions: freeze.freeze_assertions || {},
    evidence: freeze.evidence || {},
    validation: freeze.validation || {},
  });
}

module.exports = async function handler(req, res) {
  const p = parts(req);
  if (p[0] === "home") return behaviorHome(res);
  if (p[0] === "civilization") return behaviorCivilization(res, p[1]);
  if (p[0] === "civilizations" || p[0] === "battle") return behaviorCivilizationBattle(res, p[1]);
  if (p[0] === "timeline") return behaviorTimeline(res, p[1]);
  if (p[0] === "graph") return behaviorGraph(res);
  if (p[0] === "agents") return behaviorAgents(res);
  if (p[0] === "agent") return behaviorAgent(res, p[1]);
  if (p[0] === "replay") return behaviorReplay(res, p[1]);
  if (p[0] === "trace") return behaviorTrace(res, p.slice(1).join("/"));
  if (p[0] === "patterns") return behaviorPatterns(res, p[1]);
  if (p[0] === "datacenter") return behaviorDataCenter(res);
  if (p[0] === "production") return behaviorProduction(res, p[1]);
  if (p[0] === "audit") return behaviorAudit(res, p[1]);
  if (p[0] === "freeze" || p[0] === "design-freeze") return behaviorFreeze(res, p[1]);
  return send(res, 404, { ok: false, detail: "unknown_behavior_endpoint", path: p.join("/") });
};
