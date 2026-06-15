const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();

async function readJson(relPath, origin) {
  try {
    return JSON.parse(await fs.readFile(path.join(ROOT, relPath), "utf8"));
  } catch (_error) {
    if (!origin) return {};
    try {
      const response = await fetch(`${origin}/${relPath}`);
      if (!response.ok) return {};
      return await response.json();
    } catch (_fetchError) {
      return {};
    }
  }
}

async function readMatchesFromApi(origin) {
  if (!origin) return [];
  try {
    const response = await fetch(`${origin}/api/matches`);
    if (!response.ok) return [];
    const data = await response.json();
    return rowsFrom(data);
  } catch (_error) {
    return [];
  }
}

function hkDateFromKickoff(value) {
  if (!value) return "";
  const time = Date.parse(value);
  if (Number.isNaN(time)) return "";
  return new Date(time + 8 * 60 * 60 * 1000).toISOString().slice(0, 10);
}

function weekdayIndex(iso) {
  const d = new Date(`${iso}T00:00:00Z`);
  return Number.isNaN(d.getTime()) ? 0 : d.getUTCDay();
}

function rowsFrom(data) {
  if (Array.isArray(data && data.matches)) return data.matches;
  if (Array.isArray(data && data.known_scores)) return data.known_scores;
  return [];
}

function dateValues(row, dateBasis) {
  const values = new Set();
  for (const key of ["date", "matchday_hk", "source_date_query"]) {
    if (row && row[key]) values.add(String(row[key]));
  }
  const hkDate = hkDateFromKickoff(row && row.kickoff_at);
  if (hkDate) values.add(hkDate);
  if (dateBasis === "automation_hk" || dateBasis === "public_or_automation") {
    for (const item of Array.isArray(row && row.automation_dates) ? row.automation_dates : []) {
      if (item) values.add(String(item));
    }
  }
  return [...values].filter(Boolean);
}

module.exports = async function handler(req, res) {
  const dateBasis = typeof req.query.date_basis === "string" ? req.query.date_basis : "";
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  const proto = req.headers["x-forwarded-proto"] || "https";
  const origin = host ? `${proto}://${host}` : "";
  const [current, promptPack, knownScores, scoreSync, apiMatches] = await Promise.all([
    readJson("data/pool/pred_invest/latest_current_game.json", origin),
    readJson("data/pool/pred_invest/latest_prompt_pack.json", origin),
    readJson("data/pool/match_results/latest_known_scores.json", origin),
    readJson("data/pool/pred_invest/latest_score_sync.json", origin),
    readMatchesFromApi(origin),
  ]);
  const counts = new Map();
  for (const row of [...rowsFrom(current), ...rowsFrom(promptPack), ...rowsFrom(knownScores), ...rowsFrom(scoreSync), ...apiMatches]) {
    for (const iso of dateValues(row, dateBasis)) {
      counts.set(iso, (counts.get(iso) || 0) + 1);
    }
  }
  const dates = [...counts.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([date, count]) => ({ date, iso: date, key: date, count, wday: weekdayIndex(date) }));
  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.status(200).json({
    ok: true,
    version: "local_match_dates_v1",
    date_basis: dateBasis || null,
    count: dates.length,
    dates,
  });
};
