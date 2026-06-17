const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();
const POOL_ROOT = path.join(ROOT, "data", "pool");
const FALLBACK_ORIGIN = process.env.POOL_FALLBACK_ORIGIN || "";
const PRODUCTION_SEATS = ["chatgpt","deepseek","mimo","minimax","doubao","gemini","kimi","meta","qwen","wenxin","grok","yuanbao","xunfei","stepfun","zhipu"];
const REQUIRED_SEAT_COUNT = PRODUCTION_SEATS.length;
const DEFAULT_CREDIT_SCORE = 600;
const DEFAULT_CREDIT_GRADE = "B";
const DEFAULT_BALANCE_GP = 1000;

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

function n(value, fallback = 0) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function initializedSeatState(seatId) {
  return {
    seat_id: seatId,
    display_name: compactSeatName(seatId),
    balance_gp: DEFAULT_BALANCE_GP,
    outstanding_loan_gp: 0,
    accrued_interest_gp: 0,
    net_worth_gp: DEFAULT_BALANCE_GP,
    credit_score: DEFAULT_CREDIT_SCORE,
    credit_grade: DEFAULT_CREDIT_GRADE,
    credit_delta: 0,
    loan_limit_gp: 500,
    available_loan_gp: 500,
    recovery_mode: false,
    source: "initialized_required_seat",
  };
}

async function ledgerForRun(kind, runId) {
  if (runId) {
    const exact = await readJson(path.join(kind, `${runId}.json`), null);
    if (exact && exact.version) return exact;
  }
  try {
    const dir = path.join(POOL_ROOT, kind);
    const files = (await fs.readdir(dir)).filter((file) => file.endsWith(".json")).sort();
    for (const file of files.reverse()) {
      const data = await readJson(path.join(kind, file), null);
      if (data && data.version) return data;
    }
  } catch (_error) {
    // Fall through to an empty ledger.
  }
  return {};
}

async function loadSeatSummaries() {
  const summaries = {};
  await Promise.all(PRODUCTION_SEATS.map(async (seat) => {
    summaries[seat] = await readJson(path.join("seat_journals", seat, "summary.json"), null);
  }));
  return summaries;
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

function seatStateFromSources(seat, currentRow = {}, survival = {}, credit = {}, summary = {}) {
  const base = initializedSeatState(seat);
  const loanTerms = currentRow.loan_terms && typeof currentRow.loan_terms === "object" ? currentRow.loan_terms : {};
  const merged = {
    ...base,
    ...summary,
    ...survival,
    ...credit,
  };
  return {
    ...merged,
    display_name: currentRow.display_name || summary.display_name || compactSeatName(seat),
    balance_gp: n(merged.balance_gp ?? merged.cash_gp ?? loanTerms.balance_gp, base.balance_gp),
    outstanding_loan_gp: n(merged.outstanding_loan_gp ?? merged.loan_gp ?? loanTerms.outstanding_loan_gp, base.outstanding_loan_gp),
    accrued_interest_gp: n(merged.accrued_interest_gp ?? loanTerms.accrued_interest_gp, base.accrued_interest_gp),
    net_worth_gp: n(merged.net_worth_gp ?? loanTerms.net_worth_gp, base.net_worth_gp),
    credit_score: n(merged.credit_score ?? loanTerms.credit_score, base.credit_score),
    credit_grade: String(merged.credit_grade || loanTerms.credit_grade || base.credit_grade),
    credit_delta: n(merged.credit_delta, base.credit_delta),
    loan_limit_gp: n(merged.loan_limit_gp ?? loanTerms.max_loan_gp, base.loan_limit_gp),
    available_loan_gp: n(merged.available_loan_gp ?? loanTerms.available_loan_gp, base.available_loan_gp),
    recovery_mode: Boolean(merged.recovery_mode),
    source: survival.seat_id || credit.seat_id || summary.seat_id ? "ledger" : base.source,
  };
}

function runtimeRanking(current = {}, quality = {}, ledgers = {}) {
  const summaries = Array.isArray(current.model_summaries) ? current.model_summaries : [];
  const bySeat = new Map();
  for (const row of summaries) {
    const seat = String(row.model_account || row.seat_id || row.display_name || "").toLowerCase();
    if (!seat) continue;
    bySeat.set(seat, row);
  }
  const rows = PRODUCTION_SEATS.map((seat) => {
    const currentRow = bySeat.get(seat) || {};
    const state = seatStateFromSources(
      seat,
      currentRow,
      (ledgers.survival?.seats || {})[seat] || {},
      (ledgers.credit?.seats || {})[seat] || {},
      (ledgers.summaries || {})[seat] || {},
    );
    const missing = !quality.valid_seats?.includes(seat);
    return {
      rank: 0,
      seat_id: seat,
      model_account: seat === "grok" ? "xai" : seat,
      display_name: state.display_name,
      balance_gp: state.balance_gp,
      loan_gp: state.outstanding_loan_gp,
      outstanding_loan_gp: state.outstanding_loan_gp,
      accrued_interest_gp: state.accrued_interest_gp,
      net_worth_gp: state.net_worth_gp,
      credit_score: state.credit_score,
      credit_grade: state.credit_grade,
      credit_delta: state.credit_delta,
      loan_limit_gp: state.loan_limit_gp,
      available_loan_gp: state.available_loan_gp,
      recovery_mode: state.recovery_mode,
      account_source: state.source,
      receipt_state: missing ? "missing_or_pending_receipt" : "validated_receipt",
      required_next_action: currentRow.required_next_action || (missing ? "targeted_rerun_required" : "ready"),
    };
  });
  return rows
    .sort((a, b) => b.net_worth_gp - a.net_worth_gp || b.credit_score - a.credit_score || PRODUCTION_SEATS.indexOf(a.seat_id) - PRODUCTION_SEATS.indexOf(b.seat_id))
    .map((row, index) => ({ ...row, rank: index + 1 }));
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

function archiveBuckets(matches = []) {
  const rows = Array.isArray(matches) ? matches : [];
  const settled = rows.filter((match) => ["done", "settled", "final"].includes(String(match.status || match.state || "").toLowerCase()));
  const future = rows.filter((match) => !settled.includes(match));
  return {
    matches: rows,
    future_matches: future,
    settled_matches: settled,
  };
}

async function runtimeSummary(req, res) {
  const current = await readJson(path.join("pred_invest", "latest_current_game.json"));
  const quality = normalizeQualityGate(await readJson(path.join("pred_invest", "latest_quality_gate.json")));
  const daily = await readJson(path.join("pred_invest", "latest_daily_sop.json"));
  const scoreSync = await readJson(path.join("pred_invest", "latest_score_sync.json"));
  const roundId = queryValue(req, "round_id", current.round_id || daily.round_id || "run-15");
  const date = queryValue(req, "date", current.date || daily.date || "");
  const [credit, survival, summaries] = await Promise.all([
    ledgerForRun("credit_ledger", roundId),
    ledgerForRun("survival_ledger", roundId),
    loadSeatSummaries(),
  ]);
  const matches = Array.isArray(current.matches) ? current.matches : [];
  const ranking = runtimeRanking(current, quality, { credit, survival, summaries });
  const marketRows = matches.reduce((sum, match) => sum + (Array.isArray(match.market_snapshot) ? match.market_snapshot.length : 0), 0);
  const totalPool = ranking.reduce((sum, row) => sum + Number(row.balance_gp || 0), 0);
  const loanSeats = ranking.filter((row) => Number(row.loan_gp || 0) > 0).length;
  return send(res, current.version ? 200 : 404, {
    ok: Boolean(current.version),
    version: "pool_runtime_summary.local.v1",
    date,
    round_id: roundId,
    current_round: current.round_id || daily.round_id || roundId,
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
    archives: archiveBuckets(matches),
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
      net_worth_total: ranking.reduce((sum, row) => sum + Number(row.net_worth_gp || 0), 0),
      net_pl: current.scoreboard?.net_pl || "—",
      loan_seats: loanSeats,
      verified_ratio: `${quality.valid_count}/${REQUIRED_SEAT_COUNT}`,
      model_count: REQUIRED_SEAT_COUNT,
      initialized_required_seats: ranking.filter((row) => row.account_source === "initialized_required_seat").map((row) => row.seat_id),
    },
    reports: {
      current_game_html: publicRef("pred_invest", "latest_current_game.html"),
      daily_sop_md: publicRef("pred_invest", "latest_daily_sop.md"),
      quality_gate_json: publicRef("pred_invest", "latest_quality_gate.json"),
    },
  });
}

async function frontendArchives(res) {
  const current = await readJson(path.join("pred_invest", "latest_current_game.json"));
  const matches = Array.isArray(current.matches) ? current.matches : [];
  let artifacts = [];
  try {
    const files = (await fs.readdir(path.join(POOL_ROOT, "pred_invest")))
      .filter((file) => predInvestFileAllowed(file))
      .sort()
      .reverse()
      .slice(0, 80);
    artifacts = files.map((file) => ({
      file,
      artifact_ref: publicRef("pred_invest", file),
      kind: file.endsWith(".json") ? "json" : (file.endsWith(".html") ? "html" : "markdown"),
    }));
  } catch (_error) {
    artifacts = [];
  }
  send(res, current.version ? 200 : 404, {
    ok: Boolean(current.version),
    version: "frontend_archives.local.v1",
    date: current.date || null,
    round_id: current.round_id || null,
    ...archiveBuckets(matches),
    artifacts,
  });
}

async function seatArchive(req, res, runId, seatId) {
  const [seatRun, summary, creditLedger, survivalLedger] = await Promise.all([
    readJson(path.join("seat_journals", seatId, "runs", `${runId}.json`), null),
    readJson(path.join("seat_journals", seatId, "summary.json"), null),
    ledgerForRun("credit_ledger", runId),
    ledgerForRun("survival_ledger", runId),
  ]);
  const credit = (creditLedger.seats || {})[seatId] || {};
  const survival = (survivalLedger.seats || {})[seatId] || {};
  const state = seatStateFromSources(seatId, {}, survival, credit, summary || {});
  const investments = Array.isArray(seatRun?.investments) ? seatRun.investments : [];
  const loan = seatRun?.loan_decision && typeof seatRun.loan_decision === "object" ? seatRun.loan_decision : {};
  const status = seatRun?.status || (state.source === "initialized_required_seat" ? "initialized" : "available");
  if (!PRODUCTION_SEATS.includes(seatId)) {
    return send(res, 404, { ok: false, missing: true, seat_id: seatId, round_id: runId, detail: "unknown_seat" });
  }
  return send(res, 200, {
    ok: true,
    version: "seat_archive.local.v1",
    seat_id: seatId,
    display_name: state.display_name,
    round_id: runId,
    state: status,
    status_label: status === "initialized" ? "账户已初始化，等待首轮回执" : status,
    account: {
      rank: null,
      balance_gp: state.balance_gp,
      loan_gp: state.outstanding_loan_gp,
      net_worth_gp: state.net_worth_gp,
      credit_score: state.credit_score,
      credit_grade: state.credit_grade,
      recovery_mode: state.recovery_mode,
    },
    loan_decision: {
      amount: loan.request_loan_gp || loan.borrow_gp || state.outstanding_loan_gp || 0,
      repayment_plan: loan.repayment_plan || "按 SOP 在排名前优先偿还利息和本金。",
      stop_loss: loan.stop_loss || (state.recovery_mode ? "Recovery Mode 下冻结新增高杠杆。" : ""),
      reason: loan.reason || "",
    },
    game_response: {
      rank_strategy: "Use account state, credit score, and market edge before allocating stake.",
      reward_strategy: "Prefer durable edge over isolated high-odds exposure.",
      loan_strategy: "Use borrowed GP only when expected value covers interest and drawdown risk.",
      audience_pressure_response: "Expose reasoning through structured journal and archive records.",
    },
    game_response_zh: {
      rank_strategy: "根据净值、信用分和盘口边际决定仓位，不把缺席回执伪装成完成。",
      reward_strategy: "优先选择稳定优势，避免只追逐高赔率。",
      loan_strategy: "只有当预期收益覆盖利息和回撤时才使用借用积分。",
      audience_pressure_response: "通过结构化行为日志和席位档案公开可审计依据。",
    },
    bets: investments.map((row) => ({
      match_id: row.match_id,
      market: row.market || row.action,
      market_zh: row.action === "no_bet" ? "观望 / no-bet" : row.market,
      selection: row.selection,
      line: row.line,
      odds: row.odds,
      stake_gp: row.stake_gp || 0,
      rationale: row.reason || row.why_bet_or_no_bet || row.rationale || "",
      rationale_zh: row.reason || row.why_bet_or_no_bet || row.rationale || "",
    })),
    analysis_summary: seatRun?.status
      ? "Structured forecast and investment receipt was archived for this seat."
      : "This required seat has been initialized and is waiting for a valid structured receipt.",
    analysis_summary_zh: seatRun?.status
      ? "该席位的结构化预测与投资分账已归档，可从行为日志追溯。"
      : "该固定席位已完成账户初始化，等待下一轮有效结构化回执。",
    risk_summary: "Missing or stale receipts remain visible as targeted rerun work, not hidden completion.",
    risk_summary_zh: "缺失或过期回执会保留为定向补跑任务，不再被隐藏成已完成状态。",
    artifact_ref: seatRun ? publicRef("seat_journals", seatId, "runs", `${runId}.json`) : null,
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
  if (!summary.seat_id && events.length === 0 && PRODUCTION_SEATS.includes(seatId)) {
    const initial = initializedSeatState(seatId);
    return send(res, 200, {
      ok: true,
      seat_id: seatId,
      summary: {
        ...initial,
        runs_seen: [],
        event_counts: { account_initialized: 1 },
      },
      events: [{
        ts: null,
        seat_id: seatId,
        event_type: "account_initialized",
        balance_gp: DEFAULT_BALANCE_GP,
        net_worth_gp: DEFAULT_BALANCE_GP,
        credit_score: DEFAULT_CREDIT_SCORE,
        credit_grade: DEFAULT_CREDIT_GRADE,
        source: "api_initialized_required_seat",
      }],
      artifact_ref: publicRef("seat_journals", seatId, "journal.jsonl"),
    });
  }
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
  if (rows.length === 0 && PRODUCTION_SEATS.includes(seatId)) {
    rows.push({
      run_id: "initial",
      seat_id: seatId,
      credit_score: DEFAULT_CREDIT_SCORE,
      credit_grade: DEFAULT_CREDIT_GRADE,
      credit_delta: 0,
      loan_limit_gp: 500,
      available_loan_gp: 500,
      outstanding_loan_gp: 0,
      source: "initialized_required_seat",
    });
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
  if (type === "frontend-archives") return frontendArchives(res);
  if (type === "seat-archives") {
    const archiveRunId = queryValue(req, "runId", "run-15");
    return seatArchive(req, res, archiveRunId, seatId);
  }

  return send(res, 404, { ok: false, detail: "unknown_pool_meta_route", type });
};
