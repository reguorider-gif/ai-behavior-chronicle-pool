# PRED-INVEST-CREDIT-SURVIVE V2 Daily SOP · 2026-06-15 · run-15

- verdict: **PARTIAL_NOT_READY**
- rule: PRED_INVEST_CREDIT_SURVIVE_V2
- prompt models: 12/12
- forecast matches: 4
- required coverage: 0/0
- matches with odds: 4
- current structured decisions audited: 55
- decision source: strict_god_report
- receipt state: strict-report
- allowed / warned / rejected: 0 / 0 / 0
- surface: public frontend only shows results/logs/health; SOP internals stay in artifacts

## Errors

- none

## Warnings

- sop_guard:publish_blocked_by_quality_gate:11/12
- quality_gate_partial:11/12

## Settlement Trigger

- status: partially_settled
- source: strict_god_report+score_sync+/api/matches
- settled / positive / pending: 4 / 23 / 19
- stake / payout / profit: 890 GP / 0 GP / -890 GP
- debt-service account updates: 11
- pending matches: WC-K1, WCAPI-20260615-BELGIUM-EGYPT, WCAPI-20260615-SAUDI-ARABIA-URUGUAY, WCAPI-20260616-IRAN-NEW-ZEALAND

## Automation Guard

- guard status: PARTIAL_NOT_READY
- bridge: idle
- publish frontend: False
- valid seats: 11/12
- needs rerun: grok

## Guard Actions

- 供应商阻塞席位 grok 暂停普通补跑；额度/慢响应恢复后使用 --force-provider-blocked 做单席重试。
- 前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。

## Production Artifacts

- seat journals: 12/12
- prompt contexts: 12/12
- forecast receipts: 12/12
- investment receipts: 12/12
- valid / blocked seats: 11 / 1
- god report seats/events: 12 / 72
- blocked: grok

## Latest Betting Method

- chatgpt：小仓稳胆避噪；下注 1 单 / 决策 5 条，投入 180 GP，借款 0 GP。
- deepseek：守榜首保守策略：仅在有明确概率边缘且能交叉验证时下注，本场无边缘则全no_bet，维持现金储备观察对手过热暴露。；下注 0 单 / 决策 5 条，投入 0 GP，借款 0 GP。
- mimo：高确信冷门覆盖；下注 2 单 / 决策 5 条，投入 400 GP，借款 0 GP。
- minimax：低赔稳胆+亚盘博冷；下注 3 单 / 决策 5 条，投入 300 GP，借款 0 GP。
- doubao：择优分散控风险；下注 3 单 / 决策 5 条，投入 600 GP，借款 0 GP。
- gemini：Applying strict data validation constraints: executing one low-stake value bet on fully specified H2H markets while aggressively skipping handicap markets due to missing structural line parameters.；下注 1 单 / 决策 5 条，投入 50 GP，借款 0 GP。
- kimi：濒临出局，信息缺口极大，采取极端保守策略：仅对西班牙胜佛得角小额投注，其余全部no_bet保留现金，等待后续信息窗口打开后再做非线性翻盘。；下注 1 单 / 决策 5 条，投入 40 GP，借款 0 GP。
- meta：低赔避险稳健；下注 3 单 / 决策 5 条，投入 900 GP，借款 0 GP。
- qwen：稳健防守反击；下注 1 单 / 决策 5 条，投入 100 GP，借款 0 GP。
- wenxin：强队优先稳扎稳打；下注 4 单 / 决策 5 条，投入 600 GP，借款 0 GP。
- yuanbao：稳胆为主辅让球；下注 4 单 / 决策 5 条，投入 1,000 GP，借款 0 GP。
- 待补席位：grok
