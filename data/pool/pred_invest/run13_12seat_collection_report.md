# Run-13 12 Seat Collection Verification

Generated: 2026-06-14

## Result

- Main web answers collected: 12/12
- Missing seats: none
- Bridge status after fixes: available=true, ready_count=13, configured_count=13, busy=false

## Official Run Sources

| Seat | Source run | Claim |
| --- | --- | --- |
| ChatGPT | 5ba30a02fd23 | chatgpt-web-main |
| DeepSeek | 36b6cd3db20c | deepseek-web-main |
| Gemini | 5ba30a02fd23 | gemini-web-main |
| MiMo | 36b6cd3db20c | mimo-web-main |
| MiniMax | 36b6cd3db20c | minimax-web-main |
| Meta AI | 36b6cd3db20c | meta-web-main |
| Qwen | 36b6cd3db20c | qwen-web-main |
| Wenxin | 36b6cd3db20c | wenxin-web-main |
| Yuanbao | 36b6cd3db20c | yuanbao-web-main |
| Doubao | 36b6cd3db20c | doubao-web-main |
| Kimi | 1690401c4ac1 | kimi-web-main |
| Grok | b62a28006438 | grok-web-main |

## Fixes Applied

- Doubao: fixed false login detection caused by `?from_login=1`.
- Kimi: verified and switched to K2.6 thinking mode before accepted rerun.
- Grok: removed false quota detection from persistent SuperGrok upsell text.
- Grok: added ultra-compact prompt path for fragile recovery.
- Grok: fixed marker capture to reject placeholder `JSON` / `(你的JSON)` and prefer real JSON payloads.
- Grok: added mandatory after-write pacing in Chrome fixed-tab bridge for ProseMirror state sync.
- Submit script: added exact `--seats` targeting and `--compact` recovery prompt mode.

## Verification Commands

- `python3 -m py_compile` on patched submit and bridge files: pass.
- `/api/bridge/status`: available=true, ready_count=13, configured_count=13, busy=false.
- Verdict aggregation by `*-web-main` and `web_ok=true`: total_main_web_ok=12, missing=[].

