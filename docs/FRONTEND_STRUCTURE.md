# Frontend Structure

The frontend is a pure static single-file SPA served by Vercel.

## Entry Points

- `index.html`: production SPA entry.
- `commentary-log.html`: observer / god-view commentary detail page.
- `ops-v2.html`: operations acceptance surface.

`pool-app-live-repair.DEPRECATED/` is retained only as historical reference.

## Styling

CSS lives inside `index.html`.

Important `:root` token groups:

- color tokens: dark page background, panel surfaces, semantic green/red/yellow/blue.
- spacing tokens: card padding, grid gaps, sidebar widths.
- radius/shadow tokens: compact cards, overlays, buttons, and data-center panels.
- typography tokens: dashboard labels, section headings, compact metadata.

## Main DOM Structure

- `topbar`: product name, run status, contact entry, language toggle.
- `sidebar`: product identity, KPI tiles, model ranking, data-center entry.
- `main-content`: behavior pages and secondary schedule page.
- `behaviorNav`: switches between behavior/civilization views.
- `behaviorHome`: behavior summary / civilization map home.
- `behaviorReplay`: replay surface.
- `behaviorTimeline`: per-agent behavior timeline.
- `patternGraph`: top behavior pattern graph.
- `agentPanel`: selected agent behavior profile.
- `scheduleSection`: secondary schedule / market / match grid surface.
- `dataCenterOverlay`: productized data-center drawer.
- `detailOverlay`: detail modal.

## Data Loading

The SPA reads JSON from:

- `/api/pool/*`
- `/api/behavior/*`
- `/api/civilization/*`
- `/api/matches`
- `/api/match-dates`
- static `data/pool/**` JSON artifacts as fallback/product bundles.

The code also has a `fetchStaticJson()` fallback resolver for local review.

## Internationalization

The UI uses `data-i18n` attributes and an internal translation table. Language state is held in the browser and toggled from the topbar.

## Known Technical Debt

- `index.html` is a large single-file SPA.
- CSS and JavaScript are embedded in one file.
- There is no build tool or module boundary.
- Behavior, schedule, settlement, and data-center rendering functions share global state.

## Future Split Direction

1. Extract CSS tokens and component styles into `src/styles/`.
2. Split data loading into a `data-client` module.
3. Split behavior/civilization views from schedule views.
4. Introduce a build step only after the static contract is stable.
5. Keep `data/pool/**` artifact compatibility during the migration.
