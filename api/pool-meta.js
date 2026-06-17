const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();
const POOL_ROOT = path.join(ROOT, "data", "pool");
const FALLBACK_ORIGIN = process.env.POOL_FALLBACK_ORIGIN || "";
const PRODUCTION_SEATS = ["chatgpt","deepseek","mimo","minimax","doubao","gemini","kimi","meta","qwen","wenxin","grok","yuanbao","xunfei","stepfun","zhipu"];
const REQUIRED_SEAT_COUNT = PRODUCTION_SEATS.length;

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

async function readJsonl(relPath, limit = 20) {
  const raw = await readText(relPath);
  if (!raw) return [];
  const rows = [];
  for (const line of raw.split(/\r?\n/)) {
    if (!line.trim()) continue;
    try {
      rows.push(JSON.parse(line));
    } catch (_error) {
      rows.push({ parse_error: true, raw: line });
    }
  }
  return rows.slice(-limit);
}

function publicRef(...parts) {
  return ["data", "pool", ...parts].map(encodeURIComponent).join("/");
}

function send(res, status, payload) {
  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.status(status).send(JSON.stringify(payload, null, 2));
}

async function latestGodReportDate(runId) {
  const dir = path.join(POOL_ROOT, "god_reports");
  let files = [];
  try {
    files = await fs.readdir(dir);
  } catch (_error) {
    return null;
  }
  const suffix = `_${runId}.json`;
  const dates = files
    .filter((file) => file.endsWith(suffix))
    .map((file) => file.slice(0, -suffix.length))
    .filter((date) => /^\d{4}-\d{2}-\d{2}$/.test(date))
    .sort();
  return dates.length ? dates[dates.length - 1] : null;
}

async function godReportDate(req, runId) {
  const explicit = queryValue(req, "date", "");
  if (explicit) return explicit;
  return (await latestGodReportDate(runId)) || "2026-06-15";
}

const PRED_INVEST_PUBLIC_FILES = new Set([
  "latest_current_game.json",
  "latest_current_game.md",
  "latest_current_game.html",
  "latest_daily_sop.json",
  "latest_daily_sop.md",
  "latest_god_report_strict.json",
  "latest_god_report_strict.md",
  "latest_product_health.json",
  "latest_product_health.md",
  "latest_quality_gate.json",
  "latest_quality_gate.md",
  "latest_score_sync.json",
  "latest_score_sync.md",
  "latest_sop_guard.json",
  "latest_sop_guard.md",
]);

function predInvestFileAllowed(fileName) {
  if (PRED_INVEST_PUBLIC_FILES.has(fileName)) return true;
  return /^\d{4}-\d{2}-\d{2}_[A-Za-z0-9._-]+_(current_game|daily_sop|god_report_strict|product_health|quality_gate|score_sync|sop_guard)\.(json|md|html)$/.test(fileName);
}

async function predInvestArtifact(res, fileName) {
  if (!fileName || fileName.includes("/") || fileName.includes("\\") || !predInvestFileAllowed(fileName)) {
    return send(res, 404, { ok: false, detail: "pred_invest_artifact_not_public", file: fileName || null });
  }
  const relPath = path.join("pred_invest", fileName);
  if (fileName.endsWith(".json")) {
    const data = await readJson(relPath, null);
    return send(res, data ? 200 : 404, data || { ok: false, detail: "pred_invest_artifact_not_found", file: fileName });
  }
  const text = await readText(relPath);
  return send(res, text ? 200 : 404, {
    ok: Boolean(text),
    file: fileName,
    content_type: fileName.endsWith(".html") ? "text/html" : "text/markdown",
    content: text,
    artifact_ref: text ? publicRef("pred_invest", fileName) : null,
  });
}

function queryValue(req, key, fallback = "") {
  const value = req.query && req.query[key];
  if (Array.isArray(value)) return String(value[0] || fallback);
  if (value == null) return fallback;
  return String(value);
}

function appendForwardedQuery(req, url, omit = []) {
  const parsed = new URL(url);
  const blocked = new Set(["type", "path", ...omit]);
  for (const [key, value] of Object.entries(req.query || {})) {
    if (blocked.has(key)) continue;
    if (Array.isArray(value)) {
      value.forEach((item) => parsed.searchParams.append(key, String(item)));
    } else if (value !== undefined) {
      parsed.searchParams.set(key, String(value));
    }
  }
  return parsed.toString();
}

async function proxyFallback(req, res, endpointPath, omit = []) {
  if (!FALLBACK_ORIGIN) {
    return send(res, 404, {
      ok: false,
      detail: "fallback_not_configured",
      path: `/api/pool/${endpointPath}`,
    });
  }
  const url = appendForwardedQuery(req, `${FALLBACK_ORIGIN}/api/pool/${endpointPath}`, omit);
  try {
    const response = await fetch(url, { headers: { accept: "application/json" } });
    const body = await response.text();
    res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
    res.status(response.status).send(body);
  } catch (error) {
    send(res, 502, {
      ok: false,
      detail: "fallback_unreachable",
      path: `/api/pool/${endpointPath}`,
      error: String((error && error.message) || error),
    });
  }
}

function compactSeatName(seatId) {
  const names = {
    chatgpt: "ChatGPT",
    deepseek: "DeepSeek",
    mimo: "MiMo",
    minimax: "MiniMax",
    doubao: "Doubao",
    gemini: "Gemini",
    kimi: "Kimi",
    meta: "Meta AI",
    qwen: "Qwen",
    wenxin: "Wenxin",
    grok: "xAI Grok",
    yuanbao: "Yuanbao",
    xunfei: "科大讯飞",
    stepfun: "阶跃星辰",
    zhipu: "智谱清言",
  };
  return names[seatId] || seatId;
}

function normalizeQualityGate(raw = {}) {
  const valid = Array.isArray(raw.valid_seats)
    ? raw.valid_seats.filter((seat) => PRODUCTION_SEATS.includes(String(seat)))
    : [];
  const needs = Array.from(new Set([
    ...PRODUCTION_SEATS.filter((seat) => !valid.includes(seat)),
    ...(Array.isArray(raw.needs_rerun) ? raw.needs_rerun.filter((seat) => PRODUCTION_SEATS.includes(String(seat))) : []),
  ]));
  const publishAllowed = valid.length === REQUIRED_SEAT_COUNT && needs.length === 0 && raw.publish_allowed !== false;
  return {
    ...raw,
    required_seat_count: REQUIRED_SEAT_COUNT,
    valid_count: valid.length,
    valid_seats: valid,
    needs_rerun: needs,
    publish_allowed: publishAllowed,
    frontend_badge: publishAllowed ? `${REQUIRED_SEAT_COUNT}/${REQUIRED_SEAT_COUNT} 已验证` : `${valid.length}/${REQUIRED_SEAT_COUNT} 部分回收`,
  };
}

function runtimeRanking(current = {}, quality = {}) {
  const summaries = Array.isArray(current.model_summaries) ? current.model_summaries : [];
  const bySeat = new Map();
  for (const row of summaries) {
    const seat = String(row.model_account || row.seat_id || row.display_name || "").toLowerCase();
    if (!seat) continue;
    bySeat.set(seat, row);
  }
  return PRODUCTION_SEATS.map((seat, index) => {
    const row = bySeat.get(seat) || {};
    const missing = !quality.valid_seats?.includes(seat);
    return {
      rank: Number(row.rank || index + 1),
      seat_id: seat,
      model_account: seat === "grok" ? "xai" : seat,
      display_name: row.display_name || compactSeatName(seat),
      balance_gp: Number(row.balance_gp || row.cash_gp || 0),
      loan_gp: Number(row.loan_gp || row.loan_terms?.outstanding_loan_gp || 0),
      net_worth_gp: Number(row.loan_terms?.net_worth_gp || row.net_worth_gp || 0),
      required_next_action: row.required_next_action || (missing ? "missing_required_seat" : "ready"),
    };
  });
}

function matchDatesFrom(matches = []) {
  const counts = new Map();
  for (const match of matches) {
    const date = String(match.date || "").slice(0, 10);
    if (!date) continue;
    counts.set(date, (counts.get(date) || 0) + 1);
  }
  return Array.from(counts.entries()).sort().map(([date, count]) => ({ date, count }));
}

async function runtimeSummary(req, res) {
  const current = await readJson(path.join("pred_invest", "latest_current_game.json"));
  const quality = normalizeQualityGate(await readJson(path.join("pred_invest", "latest_quality_gate.json")));
  const daily = await readJson(path.join("pred_invest", "latest_daily_sop.json"));
  const scoreSync = await readJson(path.join("pred_invest", "latest_score_sync.json"));
  const matches = Array.isArray(current.matches) ? current.matches : [];
  const ranking = runtimeRanking(current, quality);
  const marketRows = matches.reduce((sum, match) => sum + (Array.isArray(match.market_snapshot) ? match.market_snapshot.length : 0), 0);
  const totalPool = ranking.reduce((sum, row) => sum + Number(row.balance_gp || 0), 0);
  const loanSeats = ranking.filter((row) => Number(row.loan_gp || 0) > 0).length;
  return send(res, current.version ? 200 : 404, {
    ok: Boolean(current.version),
    version: "pool_runtime_summary.local.v1",
    date: queryValue(req, "date", current.date || daily.date || ""),
    round_id: queryValue(req, "round_id", current.round_id || daily.round_id || "run-15"),
    current_round: current.round_id || daily.round_id || "run-15",
    provider: {
      provider: "local_pred_invest_artifacts",
      valid_odds_rows: marketRows,
      matches_with_odds: current.scoreboard?.matches_with_odds || matches.filter((match) => (match.market_snapshot || []).length).length,
      forecast_matches: current.scoreboard?.forecast_matches || matches.length,
      overall: current.verdict || daily.verdict || "UNKNOWN",
    },
    betting: {
      accepted_bets: Number(current.scoreboard?.existing_decisions || current.scoreboard?.existing_bets || 0),
      compact_decisions: [],
      summary: {
        accepted_bets: Number(current.scoreboard?.existing_decisions || current.scoreboard?.existing_bets || 0),
        candidate_bets: Number(current.scoreboard?.existing_bets || 0),
        models_without_bets: quality.needs_rerun || [],
      },
    },
    automation: {
      verdict: current.verdict || daily.verdict || "UNKNOWN",
      pipeline_status: quality.publish_allowed ? "ready" : "attention_required",
      warnings: current.missing_data?.sop_warnings || daily.warnings || [],
      errors: current.missing_data?.sop_errors || daily.errors || [],
    },
    matches,
    match_dates: matchDatesFrom(matches),
    current_ranking: ranking,
    historical_ranking: ranking,
    active_models: ranking,
    active_models_count: REQUIRED_SEAT_COUNT,
    quality_gate: quality,
    score_sync: {
      ok: Boolean(scoreSync.ok || scoreSync.version),
      updated_at: scoreSync.generated_at || scoreSync.updated_at || null,
    },
    summary: {
      total_pool: totalPool,
      net_pl: current.scoreboard?.net_pl || "—",
      loan_seats: loanSeats,
      verified_ratio: `${quality.valid_count}/${REQUIRED_SEAT_COUNT}`,
      model_count: REQUIRED_SEAT_COUNT,
    },
    reports: {
      current_game_html: publicRef("pred_invest", "latest_current_game.html"),
      daily_sop_md: publicRef("pred_invest", "latest_daily_sop.md"),
      quality_gate_json: publicRef("pred_invest", "latest_quality_gate.json"),
    },
  });
}

async function currentRules(res) {
  const data = await readJson("rules/PRED_INVEST_CREDIT_SURVIVE_V2.json");
  send(res, data.rule_version ? 200 : 404, {
    ok: Boolean(data.rule_version),
    rule_version: data.rule_version || null,
    forecast_required: data.forecast_required,
    allow_no_bet: data.allow_no_bet,
    repay_before_ranking: data.repay_before_ranking,
    credit: data.credit,
    recovery_mode: data.recovery_mode,
    privacy: data.privacy,
    artifact_ref: publicRef("rules", "PRED_INVEST_CREDIT_SURVIVE_V2.json"),
  });
}

async function behaviorSummary(res, runId) {
  const run = await readJson(path.join("god_ledger", "runs", `${runId}.json`));
  const behavior = await readJson(path.join("behavior_summary", "latest.json"));
  const events = Array.isArray(run.events) ? run.events : [];
  const seats = Array.from(new Set(events.map((event) => event && event.seat_id).filter(Boolean))).sort();
  send(res, run.run_id ? 200 : 404, {
    ok: Boolean(run.run_id),
    run_id: runId,
    event_count: events.length,
    seats,
    event_counts: run.event_counts || {},
    counts: behavior.run_id === runId ? behavior.counts : undefined,
    readiness: behavior.run_id === runId ? behavior.readiness : undefined,
    artifact_ref: publicRef("god_ledger", "runs", `${runId}.json`),
    behavior_summary_ref: publicRef("behavior_summary", "latest.json"),
  });
}

async function godReport(req, res, runId) {
  const date = await godReportDate(req, runId);
  const report = await readJson(path.join("god_reports", `${date}_${runId}.json`));
  const markdown = await readText(path.join("god_reports", `${date}_${runId}.md`));
  send(res, report.run_id || markdown ? 200 : 404, {
    ok: Boolean(report.run_id || markdown),
    date,
    run_id: runId,
    summary: {
      seat_count: report.seat_count,
      event_count: report.event_count,
      action_counts: report.action_counts,
    },
    seat_cards: report.seat_cards || [],
    markdown: markdown || report.markdown || "",
    artifact_ref: publicRef("god_reports", `${date}_${runId}.md`),
  });
}

async function seatJournal(req, res, seatId) {
  const limit = Math.max(1, Math.min(200, Number(queryValue(req, "limit", "20"))));
  const summary = await readJson(path.join("seat_journals", seatId, "summary.json"));
  const events = await readJsonl(path.join("seat_journals", seatId, "journal.jsonl"), limit);
  send(res, summary.seat_id || events.length ? 200 : 404, {
    ok: Boolean(summary.seat_id || events.length),
    seat_id: seatId,
    summary,
    events,
    artifact_ref: publicRef("seat_journals", seatId, "journal.jsonl"),
  });
}

async function creditHistory(res, seatId) {
  const dir = path.join(POOL_ROOT, "credit_ledger");
  const rows = [];
  try {
    const files = (await fs.readdir(dir)).filter((file) => file.endsWith(".json")).sort();
    for (const file of files) {
      const data = await readJson(path.join("credit_ledger", file));
      const seat = data.seats && data.seats[seatId];
      if (seat) rows.push({ run_id: data.run_id || file.replace(/\.json$/, ""), ...seat });
    }
  } catch (_error) {
    // Keep rows empty.
  }
  send(res, 200, { ok: true, seat_id: seatId, history: rows });
}

async function behaviorMemory(res, seatId) {
  if (seatId) {
    const memory = await readJson(path.join("behavior_memory", "compiled", `${seatId}.json`));
    return send(res, memory.seat_id ? 200 : 404, {
      ok: Boolean(memory.seat_id),
      seat_id: seatId,
      profile: memory.profile || {},
      top_patterns: memory.top_patterns || [],
      timeline_events: memory.recent_timeline_events || [],
      memory_contract: memory.memory_contract || {},
    });
  }
  const compiled = {};
  try {
    const dir = path.join(POOL_ROOT, "behavior_memory", "compiled");
    const files = (await fs.readdir(dir)).filter((file) => file.endsWith(".json")).sort();
    for (const file of files) {
      const row = await readJson(path.join("behavior_memory", "compiled", file));
      if (row.seat_id) compiled[row.seat_id] = {
        profile: row.profile || {},
        top_patterns: row.top_patterns || [],
        timeline_events: row.recent_timeline_events || [],
      };
    }
  } catch (_error) {
    // Keep compiled empty.
  }
  return send(res, Object.keys(compiled).length ? 200 : 404, {
    ok: Object.keys(compiled).length > 0,
    seat_count: Object.keys(compiled).length,
    seats: compiled,
  });
}

async function patternGraph(res) {
  const graph = await readJson(path.join("pattern_graph", "latest.json"));
  send(res, graph.version ? 200 : 404, {
    ok: Boolean(graph.version),
    version: graph.version || null,
    run_id: graph.run_id || null,
    generated_at: graph.generated_at || null,
    top_patterns: graph.top_patterns || [],
  });
}

async function evolutionTrace(res, runId) {
  let trace = await readJson(path.join("evolution_traces", `${runId}.json`));
  if (!trace.version) trace = await readJson(path.join("evolution_traces", "latest.json"));
  send(res, trace.version ? 200 : 404, {
    ok: Boolean(trace.version),
    version: trace.version || null,
    run_id: trace.run_id || runId,
    generated_at: trace.generated_at || null,
    traces: trace.traces || [],
  });
}

async function agentProfile(res, seatId) {
  const profiles = await readJson(path.join("agent_profiles", "latest.json"));
  const seats = profiles.seats || {};
  if (seatId) {
    const profile = seats[seatId] || {};
    return send(res, profile.seat_id ? 200 : 404, { ok: Boolean(profile.seat_id), profile });
  }
  return send(res, Object.keys(seats).length ? 200 : 404, {
    ok: Object.keys(seats).length > 0,
    version: profiles.version || null,
    run_id: profiles.run_id || null,
    seats,
  });
}

async function behaviorReplay(res, runId) {
  let replay = await readJson(path.join("replay", "runs", `${runId}.json`));
  if (!replay.version) replay = await readJson(path.join("replay", "runs", "latest.json"));
  send(res, replay.version ? 200 : 404, {
    ok: Boolean(replay.version),
    version: replay.version || null,
    run_id: replay.run_id || runId,
    generated_at: replay.generated_at || null,
    event_count: replay.event_count || 0,
    seat_count: replay.seat_count || 0,
    timeline: replay.timeline || [],
    seat_index: replay.seat_index || {},
    artifact_ref: replay.version ? publicRef("replay", "runs", `${replay.run_id || runId}.json`) : null,
  });
}

async function marketSnapshot(req, res, runId) {
  const date = queryValue(req, "date", "2026-06-15");
  let snapshot = await readJson(path.join("market_snapshots", `${date}_${runId}.json`));
  if (!snapshot.ok && !snapshot.matches) {
    const pack = await readJson(path.join("pred_invest", "latest_prompt_pack.json"));
    if (pack.round_id === runId || pack.date === date) {
      snapshot = {
        ok: true,
        date: pack.date,
        run_id: pack.round_id,
        privacy: {
          anonymous_only: true,
          source: "prompt_pack_market_snapshot_fallback",
          no_cross_seat_private_logs: true,
        },
        matches: pack.matches || [],
      };
    }
  }
  send(res, snapshot.matches ? 200 : 404, {
    ok: Boolean(snapshot.matches),
    date,
    run_id: runId,
    privacy: snapshot.privacy,
    matches: snapshot.matches || [],
    artifact_ref: snapshot.matches ? publicRef("market_snapshots", `${date}_${runId}.json`) : null,
  });
}

module.exports = async function handler(req, res) {
  const type = queryValue(req, "type");
  const runId = queryValue(req, "runId", queryValue(req, "run_id", "run-15"));
  const seatId = queryValue(req, "seatId");

  if (type === "rules") return currentRules(res);
  if (type === "behavior-summary") return behaviorSummary(res, runId);
  if (type === "god-report") return godReport(req, res, runId);
  if (type === "market-snapshot") return marketSnapshot(req, res, runId);
  if (type === "seat-journal") return seatJournal(req, res, seatId);
  if (type === "credit") return creditHistory(res, seatId);
  if (type === "behavior-memory") return behaviorMemory(res, seatId);
  if (type === "pattern-graph") return patternGraph(res);
  if (type === "evolution-trace") return evolutionTrace(res, runId);
  if (type === "agent-profile") return agentProfile(res, seatId);
  if (type === "behavior-replay") return behaviorReplay(res, runId);
  if (type === "pred-invest-artifact") return predInvestArtifact(res, queryValue(req, "file"));
  if (type === "runtime-summary") return runtimeSummary(req, res);
  if (type === "frontend-archives") return proxyFallback(req, res, "frontend-archives");
  if (type === "seat-archives") {
    const archiveRunId = queryValue(req, "runId", "run-15");
    return proxyFallback(req, res, `seat-archives/${encodeURIComponent(archiveRunId)}/${encodeURIComponent(seatId)}`, ["runId", "seatId"]);
  }

  return send(res, 404, { ok: false, detail: "unknown_pool_meta_route", type });
};
