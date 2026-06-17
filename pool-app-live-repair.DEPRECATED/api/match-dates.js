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

function normalizeTeam(value) {
  return String(value || "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

function isStaleSeedRow(row, seedIds) {
  const matchId = String((row && row.match_id) || (row && row.id) || "");
  return matchId.startsWith("WC-SEED-") && seedIds && seedIds.size > 0 && !seedIds.has(matchId);
}

function fixtureKey(row, iso) {
  const matchId = String((row && (row.match_id || row.id)) || "");
  if (matchId) return `id:${matchId}`;
  const home = normalizeTeam(row && (row.home_team || row.home));
  const away = normalizeTeam(row && (row.away_team || row.away));
  if (home && away && iso) return `fixture:${iso}:${[home, away].sort().join("|")}`;
  return "";
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
  const query = (req && req.query) || {};
  const headers = (req && req.headers) || {};
  const dateBasis = typeof query.date_basis === "string" ? query.date_basis : "";
  const host = headers["x-forwarded-host"] || headers.host;
  const proto = headers["x-forwarded-proto"] || "https";
  const origin = host ? `${proto}://${host}` : "";
  const [current, promptPack, knownScores, scoreSync, apiMatches, scheduleSeed, alignment] = await Promise.all([
    readJson("data/pool/pred_invest/latest_current_game.json", origin),
    readJson("data/pool/pred_invest/latest_prompt_pack.json", origin),
    readJson("data/pool/match_results/latest_known_scores.json", origin),
    readJson("data/pool/pred_invest/latest_score_sync.json", origin),
    readMatchesFromApi(origin),
    readJson("data/pool/pred_invest/schedule_seed.json", origin),
    readJson("data/pool/pred_invest/latest_match_data_alignment_audit.json", origin),
  ]);
  const seedIds = new Set(
    rowsFrom(scheduleSeed)
      .map((row) => String((row && row.match_id) || ""))
      .filter((id) => id.startsWith("WC-SEED-"))
  );
  const authoritativeRows = apiMatches.length
    ? [...apiMatches, ...rowsFrom(scheduleSeed), ...rowsFrom(current), ...rowsFrom(promptPack), ...rowsFrom(knownScores), ...rowsFrom(scoreSync), ...(Array.isArray(alignment && alignment.rows) ? alignment.rows : [])]
    : [...rowsFrom(scheduleSeed), ...rowsFrom(current), ...rowsFrom(promptPack), ...rowsFrom(knownScores), ...rowsFrom(scoreSync), ...(Array.isArray(alignment && alignment.rows) ? alignment.rows : [])];
  const fixturesByDate = new Map();
  for (const row of authoritativeRows) {
    if (isStaleSeedRow(row, seedIds)) continue;
    for (const iso of dateValues(row, dateBasis)) {
      if (!fixturesByDate.has(iso)) fixturesByDate.set(iso, new Set());
      fixturesByDate.get(iso).add(fixtureKey(row, iso) || `row:${fixturesByDate.get(iso).size}`);
    }
  }
  const dates = [...fixturesByDate.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([date, fixtures]) => ({ date, iso: date, key: date, count: fixtures.size, wday: weekdayIndex(date) }));
  const todayIso = hkDateFromKickoff(new Date().toISOString());
  const today =
    dates.find((row) => row.iso === todayIso)?.key ||
    dates.find((row) => todayIso && row.iso > todayIso)?.key ||
    dates[dates.length - 1]?.key ||
    null;
  const payload = {
    ok: true,
    version: "local_match_dates_v1",
    date_basis: dateBasis || null,
    count: dates.length,
    today,
    dates,
  };
  if (!res) return payload;
  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.status(200).json(payload);
};
