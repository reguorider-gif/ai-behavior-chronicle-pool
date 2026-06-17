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

function scheduleOverridesMap(data) {
  const matches = data && data.matches && typeof data.matches === "object" ? data.matches : {};
  return new Map(Object.entries(matches).filter(([, value]) => value && typeof value === "object"));
}

function applyScheduleOverride(row, overrides) {
  if (!row || typeof row !== "object") return row;
  const override = overrides && overrides.get(String(row.match_id || ""));
  if (!override) return row;
  const next = { ...row };
  for (const key of ["date", "kickoff_at", "matchday_hk", "home_team", "away_team"]) {
    if (override[key]) next[key] = override[key];
  }
  if (override.source_note) next.schedule_override_note = override.source_note;
  next.schedule_override_applied = true;
  return next;
}

function isStaleSeedRow(row, seedIds) {
  const matchId = String((row && row.match_id) || (row && row.id) || "");
  return matchId.startsWith("WC-SEED-") && seedIds && seedIds.size > 0 && !seedIds.has(matchId);
}

function parseScoreText(value) {
  const text = String(value || "").trim();
  if (!text || !text.includes("-")) return [null, null];
  const [left, right] = text.split("-", 2);
  const home = Number.parseInt(left.trim(), 10);
  const away = Number.parseInt(right.trim(), 10);
  return [Number.isFinite(home) ? home : null, Number.isFinite(away) ? away : null];
}

function publicDate(row) {
  return (
    row.date ||
    row.date_query ||
    row.source_date_query ||
    row.matchday_hk ||
    hkDateFromKickoff(row.kickoff_at)
  );
}

function normalizeRegistryMatch(raw, registrySource) {
  if (!raw || typeof raw !== "object") return null;
  const matchId = String(raw.match_id || raw.id || "").trim();
  if (!matchId || !matchId.startsWith("WC")) return null;
  const home = raw.home_team || raw.home;
  const away = raw.away_team || raw.away;
  if (!home || !away) return null;

  let homeScore = raw.home_score;
  let awayScore = raw.away_score;
  const [parsedHome, parsedAway] = parseScoreText(raw.score);
  if (homeScore === undefined || homeScore === null) homeScore = parsedHome;
  if (awayScore === undefined || awayScore === null) awayScore = parsedAway;
  const hasScore = homeScore !== undefined && homeScore !== null && awayScore !== undefined && awayScore !== null;

  const row = {
    match_id: matchId,
    date: publicDate(raw),
    kickoff_at: raw.kickoff_at,
    home_team: home,
    away_team: away,
    status: raw.status || (hasScore ? "settled" : "scheduled"),
    result_state: raw.result_state || (hasScore ? "finished" : "missing_or_not_finished"),
    market_snapshot: Array.isArray(raw.market_snapshot) ? raw.market_snapshot : [],
    available_markets: Array.isArray(raw.available_markets) ? raw.available_markets : [],
    matchday_hk: raw.matchday_hk,
    source_date_query: raw.source_date_query || raw.date_query,
    provider_event_id: raw.provider_event_id,
    provider_last_update: raw.provider_last_update,
    registry_source: registrySource,
  };
  if (hasScore) {
    row.home_score = homeScore;
    row.away_score = awayScore;
    row.score = raw.score || `${homeScore}-${awayScore}`;
    row.outcome = homeScore > awayScore ? "home" : homeScore < awayScore ? "away" : "draw";
  }
  return row;
}

async function readJsonMatchesFromDir(relDir, overrides) {
  const out = [];
  try {
    const dir = path.join(ROOT, relDir);
    const names = await fs.readdir(dir);
    for (const name of names.sort()) {
      if (!name.endsWith(".json") || name.includes("smoke") || name.includes("unit")) continue;
      try {
        const data = JSON.parse(await fs.readFile(path.join(dir, name), "utf8"));
        for (const row of rowsFrom(data)) {
          const normalized = normalizeRegistryMatch(row, name);
          if (normalized) out.push(applyScheduleOverride(normalized, overrides));
        }
      } catch (_error) {
        // Keep the public route resilient; bad artifacts are surfaced by SOP health checks.
      }
    }
  } catch (_error) {
    // Vercel filesystem may not contain every optional artifact directory.
  }
  return out;
}

async function registryRows(origin, overrides) {
  const rows = [];
  const scheduleSeed = await readJson("data/pool/pred_invest/schedule_seed.json", origin);
  const seedIds = new Set(
    rowsFrom(scheduleSeed)
      .map((row) => String((row && row.match_id) || ""))
      .filter((id) => id.startsWith("WC-SEED-"))
  );
  const required = await readJson("data/pool/pred_invest/required_matches.json", origin);
  for (const row of rowsFrom(required)) {
    const normalized = normalizeRegistryMatch(row, "required_matches");
    if (normalized) rows.push(applyScheduleOverride(normalized, overrides));
  }
  for (const row of rowsFrom(scheduleSeed)) {
    const normalized = normalizeRegistryMatch(row, "schedule_seed");
    if (normalized) rows.push(applyScheduleOverride(normalized, overrides));
  }
  const alignment = await readJson("data/pool/pred_invest/latest_match_data_alignment_audit.json", origin);
  for (const row of Array.isArray(alignment && alignment.rows) ? alignment.rows : []) {
    if (isStaleSeedRow(row, seedIds)) continue;
    const normalized = normalizeRegistryMatch(row, "match_data_alignment_audit");
    if (normalized) rows.push(applyScheduleOverride(normalized, overrides));
  }
  rows.push(...(await readJsonMatchesFromDir("data/pool/pred_invest", overrides)).filter((row) => !isStaleSeedRow(row, seedIds)));
  rows.push(...(await readJsonMatchesFromDir("data/pool/market_snapshots", overrides)).filter((row) => !isStaleSeedRow(row, seedIds)));
  return rows;
}

function fixtureKey(row) {
  const home = normalizeTeam(row && row.home_team);
  const away = normalizeTeam(row && row.away_team);
  const date = String((row && (row.date || row.matchday_hk || hkDateFromKickoff(row.kickoff_at))) || "");
  if (!home || !away || !date) return "";
  return `${date}|${[home, away].sort().join("|")}`;
}

function rowQuality(row) {
  const hasScore = row && row.home_score !== undefined && row.home_score !== null && row.away_score !== undefined && row.away_score !== null ? 1 : 0;
  const marketCount = Array.isArray(row && row.market_snapshot) ? row.market_snapshot.length : 0;
  const hasKickoff = row && row.kickoff_at ? 1 : 0;
  const isSeed = String((row && row.match_id) || "").startsWith("WC-SEED-") ? 1 : 0;
  return [hasScore, marketCount, hasKickoff, -isSeed];
}

function betterRow(a, b) {
  const qa = rowQuality(a);
  const qb = rowQuality(b);
  for (let index = 0; index < qa.length; index += 1) {
    if (qa[index] !== qb[index]) return qa[index] > qb[index] ? a : b;
  }
  return a;
}

function dedupeRows(rows) {
  const byFixture = new Map();
  const passthrough = [];
  for (const row of rows) {
    const key = fixtureKey(row);
    if (!key) {
      passthrough.push(row);
      continue;
    }
    const current = byFixture.get(key);
    byFixture.set(key, current ? betterRow(row, current) : row);
  }
  return [...passthrough, ...byFixture.values()];
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
    const left = String(a.kickoff_at || a.date || "");
    const right = String(b.kickoff_at || b.date || "");
    if (left !== right) return left.localeCompare(right);
    return String(a.match_id || "").localeCompare(String(b.match_id || ""));
  });
  return { matches: merged, applied, appended };
}

function annotateResultSyncState(rows) {
  const now = Date.now();
  const overdue = [];
  const matches = rows.map((row) => {
    const next = { ...row };
    const status = String(next.status || "").toLowerCase();
    const hasScore = next.home_score !== undefined && next.home_score !== null && next.away_score !== undefined && next.away_score !== null;
    const kickoff = Date.parse(next.kickoff_at || "");
    if (!hasScore && !["settled", "finished", "final"].includes(status) && Number.isFinite(kickoff) && kickoff + 3 * 60 * 60 * 1000 < now) {
      next.status = "result_missing";
      next.result_state = "overdue_result_missing";
      next.result_sync_required = true;
      overdue.push({
        match_id: next.match_id,
        home_team: next.home_team,
        away_team: next.away_team,
        kickoff_at: next.kickoff_at,
        date: next.date,
      });
    }
    return next;
  });
  return { matches, overdue };
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
  const query = (req && req.query) || {};
  const headers = (req && req.headers) || {};
  const requestedDate = typeof query.date === "string" ? query.date : "";
  const dateBasis = typeof query.date_basis === "string" ? query.date_basis : "";
  const host = headers["x-forwarded-host"] || headers.host;
  const proto = headers["x-forwarded-proto"] || "https";
  const origin = host ? `${proto}://${host}` : "";

  const [current, promptPack, latestScores, scoreSync, scheduleSeed, scheduleOverrides] = await Promise.all([
    readJson("data/pool/pred_invest/latest_current_game.json", origin),
    readJson("data/pool/pred_invest/latest_prompt_pack.json", origin),
    readJson("data/pool/match_results/latest_known_scores.json", origin),
    readJson("data/pool/pred_invest/latest_score_sync.json", origin),
    readJson("data/pool/pred_invest/schedule_seed.json", origin),
    readJson("data/pool/pred_invest/schedule_overrides.json", origin),
  ]);
  const overrides = scheduleOverridesMap(scheduleOverrides);
  const registry = await registryRows(origin, overrides);
  const seedIds = new Set(
    rowsFrom(scheduleSeed)
      .map((row) => String((row && row.match_id) || ""))
      .filter((id) => id.startsWith("WC-SEED-"))
  );

  const baseRows = [...rowsFrom(current), ...rowsFrom(promptPack), ...registry]
    .filter((row) => !isStaleSeedRow(row, seedIds))
    .map((row) => applyScheduleOverride(row, overrides));
  const dedupedBase = [];
  const seenBase = new Set();
  for (const row of baseRows) {
    const key = String((row && row.match_id) || "") || `${scoreKey(row)}|${row && row.kickoff_at}`;
    if (!key || seenBase.has(key)) continue;
    seenBase.add(key);
    dedupedBase.push(row);
  }

  const scoreRows = [...rowsFrom(latestScores), ...rowsFrom(scoreSync)].map((row) => applyScheduleOverride(row, overrides));
  const uniqueScores = [];
  const seenScores = new Set();
  for (const row of scoreRows) {
    const key = String((row && row.match_id) || "") || `${scoreKey(row)}|${row && row.kickoff_at}`;
    if (!key || seenScores.has(key)) continue;
    seenScores.add(key);
    uniqueScores.push(row);
  }

  const filteredBase = filterByDate(dedupeRows(dedupedBase), requestedDate, dateBasis);
  const merged = mergeScores(filteredBase, uniqueScores, requestedDate);
  const annotated = annotateResultSyncState(merged.matches);
  const dates = [...new Set(annotated.matches.flatMap((row) => [...dateValues(row)]).filter(Boolean))].sort();

  const payload = {
    ok: true,
    version: "matches_score_registry_v2",
    source: "local_match_registry_with_score_sync",
    requested_date: requestedDate || null,
    date_basis: dateBasis || null,
    score_registry_applied: true,
    score_registry_rows: uniqueScores.length,
    score_registry_merged: merged.applied,
    score_registry_appended: merged.appended,
    match_registry_rows: registry.length,
    overdue_result_matches: annotated.overdue,
    count: annotated.matches.length,
    dates,
    matches: annotated.matches,
  };
  if (!res) return payload;
  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.status(200).json(payload);
};
