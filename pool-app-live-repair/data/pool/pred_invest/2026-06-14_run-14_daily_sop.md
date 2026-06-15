# PRED-INVEST-CREDIT-SURVIVE V2 Daily SOP · 2026-06-14 · run-14

- verdict: **NOT_READY**
- rule: PRED_INVEST_CREDIT_SURVIVE_V2
- prompt models: 12/12
- forecast matches: 10
- required coverage: 0/0
- matches with odds: 10
- existing structured bets audited: 0
- receipt state: missing
- allowed / warned / rejected: 0 / 0 / 0
- surface: public frontend only shows results/logs/health; SOP internals stay in artifacts

## Errors

- score_sync_overdue:WC-C1,WC-D2,WC-C2,WC-B2,WC-H1,WC-I1

## Warnings

- no_existing_bets_to_shadow_audit_bridge_run_required
- bet_receipts_missing:unknown
- sop_guard:publish_blocked_by_quality_gate:11/12
- quality_gate_partial:11/12

## Automation Guard

- guard status: PARTIAL_NOT_READY
- bridge: idle
- publish frontend: False
- valid seats: 11/12
- needs rerun: grok

## Guard Actions

- 只补跑 rerun_queue 中的缺席席位，不重跑已合格席位。
- 前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。

## Latest Betting Method

- DeepSeek：信用 A/745.6，净资产 1,810 GP，可贷 448 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- Gemini：信用 B/645.0，净资产 850 GP，可贷 0 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- 通义：信用 B/674.7，净资产 1,100 GP，可贷 150 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- 元宝：信用 B/657.7，净资产 1,000 GP，可贷 0 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- 豆包：信用 B/669.6，净资产 1,100 GP，可贷 250 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- Meta AI：信用 C/597.8，净资产 600 GP，可贷 0 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- MiMo：信用 B/640.7，净资产 900 GP，可贷 150 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- ChatGPT：信用 B/665.0，净资产 1,000 GP，可贷 500 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- Kimi：信用 B/661.0，净资产 1,000 GP，可贷 500 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- MiniMax：信用 B/657.0，净资产 1,000 GP，可贷 500 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- 文心：信用 B/653.0，净资产 1,000 GP，可贷 500 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
- xAI：信用 B/649.0，净资产 1,000 GP，可贷 500 GP；必须补 forecast；投资可 no-bet，但不能缺席判断。
