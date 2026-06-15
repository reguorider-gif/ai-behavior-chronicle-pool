# Browser QA Runtime - Do Not Delete

The daily product-health and frontend smoke checks use:

- `/opt/homebrew/bin/chromium`
- `/opt/homebrew/Caskroom/chromium/latest/chromium.wrapper.sh`
- `/Applications/Chromium.app` when available
- `/Applications/Google Chrome.app` as the stable fallback

Do not delete `/Applications/Chromium.app` or `/Applications/Google Chrome.app`
without replacing the browser QA launcher and rerunning:

```bash
/opt/homebrew/bin/chromium --version
/opt/homebrew/bin/chromium --headless=new --disable-gpu --dump-dom https://pool-app-one.vercel.app/
python3 ops/audit_pred_invest_product_health.py --write
```

If the Homebrew Chromium cask app link is removed, the wrapper intentionally
falls back to Google Chrome so frontend QA can continue.
