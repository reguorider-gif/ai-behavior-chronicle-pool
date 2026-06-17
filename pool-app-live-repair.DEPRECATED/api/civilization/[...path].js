const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();
const POOL_ROOT = path.join(ROOT, "data", "pool");

async function readJson(relPath, fallback = {}) {
  try {
    const raw = await fs.readFile(path.join(POOL_ROOT, relPath), "utf8");
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

function publicState(state, resolvedRun) {
  return {
    ok: Boolean(state.version),
    version: "civilization_state_api.v1",
    run_id: state.run_id || resolvedRun,
    generated_at: state.generated_at || null,
    title: state.title || "Behavior Civilization Map",
    question: state.question || null,
    pressure: state.pressure || {},
    agents: state.agents || [],
    positions: state.positions || {},
    drift: state.drift || {},
    archetypes: state.archetypes || {},
    behavior_flow: state.behavior_flow || [],
    causality: state.causality || {},
    map_contract: state.map_contract || {},
  };
}

function publicFreeze(freeze, resolvedRun) {
  return {
    ok: Boolean(freeze.version),
    version: "civilization_freeze_api.v1",
    run_id: freeze.run_id || resolvedRun,
    generated_at: freeze.generated_at || null,
    engine_version: freeze.engine_version || null,
    kernel_version: freeze.kernel_version || null,
    system_definition: freeze.system_definition || null,
    system_formula: freeze.system_formula || null,
    final_status: freeze.final_status || "UNKNOWN",
    ready: Boolean(freeze.ready),
    architecture_layers: freeze.architecture_layers || [],
    final_loop: freeze.final_loop || [],
    freeze_assertions: freeze.freeze_assertions || {},
    evidence: freeze.evidence || {},
    public_surface_policy: freeze.public_surface_policy || {},
    validation: freeze.validation || {},
  };
}

function publicBattle(battle, resolvedRun) {
  return {
    ok: Boolean(battle.version),
    version: "civilization_battle_api.v9",
    run_id: battle.run_id || resolvedRun,
    generated_at: battle.generated_at || null,
    title: battle.title || "Civilization vs Civilization",
    question: battle.question || null,
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
  };
}

async function state(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let payload = await readJson(path.join("civilization_state", `${resolvedRun}.json`));
  if (!payload.version) payload = await readJson(path.join("civilization_state", "latest.json"));
  send(res, payload.version ? 200 : 404, publicState(payload, resolvedRun));
}

async function freeze(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let payload = await readJson(path.join("civilization_freeze", `${resolvedRun}.json`));
  if (!payload.version) payload = await readJson(path.join("civilization_freeze", "latest.json"));
  send(res, payload.version ? 200 : 404, publicFreeze(payload, resolvedRun));
}

async function battle(res, runId) {
  const resolvedRun = await latestRunId(runId);
  let payload = await readJson(path.join("civilization_battle", `${resolvedRun}.json`));
  if (!payload.version) payload = await readJson(path.join("civilization_battle", "latest.json"));
  send(res, payload.version ? 200 : 404, publicBattle(payload, resolvedRun));
}

module.exports = async function handler(req, res) {
  const p = parts(req);
  if (p[0] === "state" || p.length === 0) return state(res, p[1]);
  if (p[0] === "freeze" || p[0] === "design-freeze") return freeze(res, p[1]);
  if (p[0] === "battle" || p[0] === "vs") return battle(res, p[1]);
  return send(res, 404, { ok: false, detail: "unknown_civilization_endpoint", path: p.join("/") });
};
