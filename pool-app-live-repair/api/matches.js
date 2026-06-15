const fs = require("node:fs/promises");
const path = require("node:path");

const ROOT = process.cwd();

async function readJson(relPath, origin) {
  try {
    const raw = await fs.readFile(path.join(ROOT, relPath), "utf8");
    return JSON.parse(raw);
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

function normalizeTeam(value) {
  return String(value || "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

function hkDateFromKickoff(value) {
  if (!value) return null;
  const time = Date.parse(value);
  if (Number.isNaN(time)) return null;
  return new Date(time + 8 * 60 * 60 * 1000).toISOString().slice(0, 10);
}

function dateValues(row) {
  const values = new Set();
  for (const key of ["date", "matchday_hk", "source_date_query"]) {
    if (row && row[key]) values.add(String(row[key]));
  }
  const hkDate = hkDateFromKickoff(row && row.kickoff_at);
  if (hkDate) values.add(hkDate);
  return values;
}

function scoreKey(row) {
  return [normalizeTeam(row && row.home_team), normalizeTeam(row && row.away_team)].join("|");
}

function rowsFrom(data) {
  if (Array.isArray(data && data.matches)) return data.matches;
  if (Array.isArray(data && data.known_scores)) return data.known_scores;
  return [];
}

function scoreOnlyMatch(score, requestedDate) {
  const values = dateValues(score);
  const publicDate =
    (requestedDate && values.has(requestedDate) && requestedDate) ||
    score.source_date_query ||
    score.matchday_hk ||
    hkDateFromKickoff(score.kickoff_at);
  return {
    match_id: score.match_id,
    date: publicDate,
    kickoff_at: score.kickoff_at,
    home_team: score.home_team,
    away_team: score.away_team,
    status: score.status || "settled",
    result_state: score.result_state || "finished",
    score: score.score,
    home_score: score.home_score,
    away_score: score.away_score,
    outcome: score.outcome,
    market_snapshot: [],
    available_markets: [],
    matchday_hk: score.matchday_hk,
    source_date_query: score.source_date_query,
    provider_event_id: score.provider_event_id,
    provider_last_update: score.provider_last_update,
    score_source: score.source || "match_result_registry",
    score_registry_applied: true,
    registry_only: true,
  };
}

function applyScore(match, score) {
  const merged = { ...match };
  for (const key of [
    "score",
    "home_score",
    "away_score",
    "outcome",
    "status",
    "result_state",
    "provider_event_id",
    "provider_last_update",
    "matchday_hk",
    "source_date_query",
  ]) {
    if (score[key] !== undefined && score[key] !== null) merged[key] = score[key];
  }
  merged.score_source = score.source || "match_result_registry";
  merged.score_registry_applied = true;
  return merged;
}

function mergeScores(baseRows, scoreRows, requestedDate) {
  const scoreById = new Map();
  const scoreByTeams = new Map();
  for (const row of scoreRows) {
    if (!row || typeof row !== "object") continue;
    if (row.match_id) scoreById.set(String(row.match_id), row);
    const key = scoreKey(row);
    if (key !== "|") scoreByTeams.set(key, row);
  }

  const merged = [];
  const seenIds = new Set();
  let applied = 0;
  for (const row of baseRows) {
    if (!row || typeof row !== "object") continue;
    const score = scoreById.get(String(row.match_id || "")) || scoreByTeams.get(scoreKey(row));
    const next = score ? applyScore(row, score) : { ...row };
    if (score) {
      applied += 1;
      if (score.match_id) seenIds.add(String(score.match_id));
    }
    if (next.match_id) seenIds.add(String(next.match_id));
    merged.push(next);
  }

  let appended = 0;
  for (const score of scoreRows) {
    const matchId = String(score.match_id || "");
    if (matchId && seenIds.has(matchId)) continue;
    if (requestedDate && !dateValues(score).has(requestedDate)) continue;
    merged.push(scoreOnlyMatch(score, requestedDate));
    appended += 1;
    if (matchId) seenIds.add(matchId);
  }

  merged.sort((a, b) => {
    const left = String(a.kickoff_at || "");
    const right = String(b.kickoff_at || "");
    if (left !== right) return left.localeCompare(right);
    return String(a.match_id || "").localeCompare(String(b.match_id || ""));
  });
  return { matches: merged, applied, appended };
}

function filterByDate(rows, requestedDate, dateBasis) {
  if (!requestedDate) return rows;
  return rows.filter((row) => {
    const values = dateValues(row);
    if (values.has(requestedDate)) return true;
    if (dateBasis === "public_or_automation") {
      const automationDates = Array.isArray(row.automation_dates) ? row.automation_dates.map(String) : [];
      return automationDates.includes(requestedDate);
    }
    return false;
  });
}

module.exports = async function handler(req, res) {
  const requestedDate = typeof req.query.date === "string" ? req.query.date : "";
  const dateBasis = typeof req.query.date_basis === "string" ? req.query.date_basis : "";
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  const proto = req.headers["x-forwarded-proto"] || "https";
  const origin = host ? `${proto}://${host}` : "";

  const [current, promptPack, latestScores, scoreSync] = await Promise.all([
    readJson("data/pool/pred_invest/latest_current_game.json", origin),
    readJson("data/pool/pred_invest/latest_prompt_pack.json", origin),
    readJson("data/pool/match_results/latest_known_scores.json", origin),
    readJson("data/pool/pred_invest/latest_score_sync.json", origin),
  ]);

  const baseRows = [...rowsFrom(current), ...rowsFrom(promptPack)];
  const dedupedBase = [];
  const seenBase = new Set();
  for (const row of baseRows) {
    const key = String((row && row.match_id) || "") || `${scoreKey(row)}|${row && row.kickoff_at}`;
    if (!key || seenBase.has(key)) continue;
    seenBase.add(key);
    dedupedBase.push(row);
  }

  const scoreRows = [...rowsFrom(latestScores), ...rowsFrom(scoreSync)];
  const uniqueScores = [];
  const seenScores = new Set();
  for (const row of scoreRows) {
    const key = String((row && row.match_id) || "") || `${scoreKey(row)}|${row && row.kickoff_at}`;
    if (!key || seenScores.has(key)) continue;
    seenScores.add(key);
    uniqueScores.push(row);
  }

  const filteredBase = filterByDate(dedupedBase, requestedDate, dateBasis);
  const merged = mergeScores(filteredBase, uniqueScores, requestedDate);
  const dates = [...new Set(merged.matches.map((row) => row.date).filter(Boolean))].sort();

  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.status(200).json({
    ok: true,
    version: "matches_score_registry_v1",
    source: "local_match_registry_with_score_sync",
    requested_date: requestedDate || null,
    date_basis: dateBasis || null,
    score_registry_applied: true,
    score_registry_rows: uniqueScores.length,
    score_registry_merged: merged.applied,
    score_registry_appended: merged.appended,
    count: merged.matches.length,
    dates,
    matches: merged.matches,
  });
};
