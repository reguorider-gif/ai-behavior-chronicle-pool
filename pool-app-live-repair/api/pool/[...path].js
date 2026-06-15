const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();
const POOL_ROOT = path.join(ROOT, "data", "pool");
const FALLBACK_ORIGIN = process.env.POOL_FALLBACK_ORIGIN || "https://pool-efqknizkv-reguorider-9181s-projects.vercel.app";

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

function pathParts(req) {
  const value = req.query.path;
  if (Array.isArray(value)) return value.map(String);
  if (typeof value === "string" && value) return value.split("/");
  return [];
}

async function proxyFallback(req, res, parts) {
  const qs = new URLSearchParams();
  for (const [key, value] of Object.entries(req.query || {})) {
    if (key === "path") continue;
    if (Array.isArray(value)) value.forEach((item) => qs.append(key, String(item)));
    else if (value !== undefined) qs.set(key, String(value));
  }
  const suffix = qs.toString() ? `?${qs}` : "";
  const url = `${FALLBACK_ORIGIN}/api/pool/${parts.map(encodeURIComponent).join("/")}${suffix}`;
  try {
    const response = await fetch(url, { headers: { accept: "application/json" } });
    const body = await response.text();
    res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
    res.status(response.status).send(body);
  } catch (error) {
    send(res, 502, { ok: false, detail: "fallback_unreachable", path: `/api/pool/${parts.join("/")}`, error: String(error && error.message || error) });
  }
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
  const date = String(req.query.date || "2026-06-15");
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
  const limit = Math.max(1, Math.min(200, Number(req.query.limit || 20)));
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

async function marketSnapshot(req, res, runId) {
  const date = String(req.query.date || "2026-06-15");
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
  const parts = pathParts(req);
  if (parts[0] === "rules" && parts[1] === "current") return currentRules(res);
  if (parts[0] === "runs" && parts[2] === "behavior-summary") return behaviorSummary(res, parts[1]);
  if (parts[0] === "runs" && parts[2] === "god-report") return godReport(req, res, parts[1]);
  if (parts[0] === "runs" && parts[2] === "market-snapshot") return marketSnapshot(req, res, parts[1]);
  if (parts[0] === "seats" && parts[2] === "journal") return seatJournal(req, res, parts[1]);
  if (parts[0] === "seats" && parts[2] === "credit") return creditHistory(res, parts[1]);
  return proxyFallback(req, res, parts);
};
