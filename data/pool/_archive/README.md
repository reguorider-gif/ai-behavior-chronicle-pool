# Archived Pool Debug Artifacts

These files are historical debug and rerun artifacts. They do not affect the current production run.

Active data stays under `data/pool/` outside `_archive/`.

Do not truncate append-only streams such as:

- `data/pool/god_ledger/events.jsonl`
- `data/pool/seat_journals/*/journal.jsonl`

Archive groups:

- `model_outputs_reruns/`: historical model output rerun captures.
- `pred_invest_reruns/`: single-seat rerun attempt artifacts.
- `pred_invest_attempts/`: bridge attempt payloads, responses, and verdict snapshots.
- `shadow_reruns/`: shadow rerun artifacts.
- `dry_runs/`: dry-run artifacts.
