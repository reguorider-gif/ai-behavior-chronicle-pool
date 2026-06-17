#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${AI_JUDGE_PYTHON:-python3}"
DATE_EXPR="${AI_JUDGE_SOP_DATE:-$(date +%F)}"
ROUND_ID="${AI_JUDGE_SOP_ROUND:-run-auto}"

PRE_CMD="cd \"$ROOT\" && \"$PYTHON_BIN\" ops/auto_sop.py --phase pre --date \"$DATE_EXPR\" --round \"$ROUND_ID\" --write >> logs/pre.log 2>&1"
POST_CMD="cd \"$ROOT\" && \"$PYTHON_BIN\" ops/auto_sop.py --phase post --date \"$DATE_EXPR\" --round \"$ROUND_ID\" --write >> logs/post.log 2>&1"
SCORES_CMD="cd \"$ROOT\" && \"$PYTHON_BIN\" ops/fetch_odds.py --date \"$DATE_EXPR\" --round \"$ROUND_ID\" --sync scores --write >> logs/scores.log 2>&1"

if [[ "${1:-print}" == "install" ]]; then
  TMP_FILE="$(mktemp)"
  crontab -l 2>/dev/null > "$TMP_FILE" || true
  {
    grep -v "ops/auto_sop.py .*pre" "$TMP_FILE" | grep -v "ops/auto_sop.py .*post" | grep -v "ops/fetch_odds.py" || true
    printf '0 6 * * * %s\n' "$PRE_CMD"
    printf '30 23 * * * %s\n' "$POST_CMD"
    printf '0 */6 * * * %s\n' "$SCORES_CMD"
  } | crontab -
  rm -f "$TMP_FILE"
  echo "Installed AI Judge SOP cron entries."
else
  cat <<EOF
# AI Judge PRED-INVEST cron preview
# Install with: bash ops/cron_setup.sh install
0 6 * * * $PRE_CMD
30 23 * * * $POST_CMD
0 */6 * * * $SCORES_CMD
EOF
fi
