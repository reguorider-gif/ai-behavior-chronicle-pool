#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-diagnose}"
PROXY_HOST="${PROXY_HOST:-127.0.0.1}"
PROXY_PORT="${PROXY_PORT:-7897}"
PROXY_URL="http://${PROXY_HOST}:${PROXY_PORT}"
SHELL_PROXY_FILE="${HOME}/.config/shell/local-proxy-env.zsh"

usage() {
  cat <<'EOF'
Usage:
  bash ops/fixes/proxy_diagnostic_and_fix.sh diagnose
  bash ops/fixes/proxy_diagnostic_and_fix.sh fix-local
  bash ops/fixes/proxy_diagnostic_and_fix.sh fix-gateway
  bash ops/fixes/proxy_diagnostic_and_fix.sh full

Environment:
  PROXY_HOST=127.0.0.1
  PROXY_PORT=7897
  GATEWAY_HOST=user@host        # required by fix-gateway
  GATEWAY_FIX_COMMAND='...'     # optional remote command
EOF
}

proxy_reachable() {
  nc -z "${PROXY_HOST}" "${PROXY_PORT}" >/dev/null 2>&1
}

diagnose() {
  echo "== Proxy endpoint =="
  echo "${PROXY_URL}"
  if proxy_reachable; then
    echo "proxy: reachable"
  else
    echo "proxy: unreachable"
  fi

  echo
  echo "== Shell proxy env =="
  env | grep -E '^(HTTP_PROXY|HTTPS_PROXY|http_proxy|https_proxy|NO_PROXY|no_proxy)=' || true

  echo
  echo "== Vercel endpoint via proxy =="
  if proxy_reachable; then
    curl -sS -I --connect-timeout 12 --max-time 25 --proxy "${PROXY_URL}" \
      https://pool-app-live-repair.vercel.app/data/pool/pred_invest/latest_current_game.json || true
  else
    echo "skip: proxy not reachable"
  fi
}

fix_local() {
  mkdir -p "$(dirname "${SHELL_PROXY_FILE}")"
  cat > "${SHELL_PROXY_FILE}" <<EOF
# Enable shell proxy variables only when the local mixed proxy is reachable.
if command -v nc >/dev/null 2>&1 && nc -z ${PROXY_HOST} ${PROXY_PORT} >/dev/null 2>&1; then
  export HTTPS_PROXY=${PROXY_URL}
  export HTTP_PROXY=${PROXY_URL}
  export https_proxy=${PROXY_URL}
  export http_proxy=${PROXY_URL}
  export NO_PROXY=localhost,127.0.0.1,::1
  export no_proxy=localhost,127.0.0.1,::1
else
  unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy
  unset NO_PROXY no_proxy
fi
EOF
  for rc in "${HOME}/.zprofile" "${HOME}/.zshrc"; do
    touch "${rc}"
    if ! grep -Fq "${SHELL_PROXY_FILE}" "${rc}"; then
      {
        echo
        echo "# Local proxy env shared by interactive and non-interactive shells."
        echo "[ -s \"${SHELL_PROXY_FILE}\" ] && source \"${SHELL_PROXY_FILE}\""
      } >> "${rc}"
    fi
  done
  echo "local proxy shell hook installed: ${SHELL_PROXY_FILE}"
}

fix_gateway() {
  if [[ -z "${GATEWAY_HOST:-}" ]]; then
    echo "GATEWAY_HOST is not set; skip gateway fix." >&2
    return 2
  fi
  remote_cmd="${GATEWAY_FIX_COMMAND:-systemctl restart clash || systemctl restart mihomo || true}"
  ssh "${GATEWAY_HOST}" "${remote_cmd}"
}

case "${MODE}" in
  diagnose)
    diagnose
    ;;
  fix-local)
    fix_local
    ;;
  fix-gateway)
    fix_gateway
    ;;
  full)
    diagnose
    fix_local
    diagnose
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage
    exit 2
    ;;
esac
