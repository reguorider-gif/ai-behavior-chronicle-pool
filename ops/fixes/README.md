# Ops Fixes

`proxy_diagnostic_and_fix.sh` is the single proxy diagnostic and repair entry point.

## Commands

```bash
bash ops/fixes/proxy_diagnostic_and_fix.sh diagnose
bash ops/fixes/proxy_diagnostic_and_fix.sh fix-local
bash ops/fixes/proxy_diagnostic_and_fix.sh fix-gateway
bash ops/fixes/proxy_diagnostic_and_fix.sh full
```

## Behavior

- `diagnose` checks whether `127.0.0.1:7897` is reachable and verifies the Vercel data endpoint through the proxy.
- `fix-local` installs a shared shell hook at `~/.config/shell/local-proxy-env.zsh` and sources it from both `~/.zprofile` and `~/.zshrc`.
- `fix-gateway` requires `GATEWAY_HOST=user@host`; it runs `GATEWAY_FIX_COMMAND` remotely, or a conservative clash/mihomo restart fallback.
- `full` runs diagnose, local fix, then diagnose again.

The repository did not contain the older root scripts (`fix_codex.sh`, `fix_codex_local.sh`, `fix_proxy.sh`, `proxy_diagnostic.sh`) at cleanup time, so there were no legacy files to delete.
