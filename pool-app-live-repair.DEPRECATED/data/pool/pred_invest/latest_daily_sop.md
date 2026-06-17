# PRED-INVEST-CREDIT-SURVIVE V2 Daily SOP · 2026-06-16 · run-16

- verdict: **PARTIAL_NOT_READY**
- rule: PRED_INVEST_CREDIT_SURVIVE_V2
- prompt models: 12/12
- forecast matches: 5
- required coverage: 5/5
- matches with odds: 5
- current structured decisions audited: 50
- decision source: strict_god_report
- receipt state: strict-report
- allowed / warned / rejected: 0 / 0 / 0
- surface: public frontend only shows results/logs/health; SOP internals stay in artifacts

## Errors

- none

## Warnings

- sop_guard:publish_blocked_by_quality_gate:10/12
- quality_gate_partial:10/12

## Settlement Trigger

- status: partially_settled
- source: strict_god_report+score_sync+/api/matches
- settled / positive / pending: 7 / 25 / 18
- stake / payout / profit: 1,170 GP / 1,708.2 GP / 538.2 GP
- debt-service account updates: 10
- pending matches: WC-SEED-20260617-ENGLAND-CROATIA, WC-SEED-20260617-GHANA-PANAMA, WC-SEED-20260617-PORTUGAL-CONGO-DR, WC-SEED-20260617-UZBEKISTAN-COLOMBIA

## Automation Guard

- guard status: PARTIAL_NOT_READY
- bridge: idle
- publish frontend: False
- valid seats: 10/12
- needs rerun: grok, qwen

## Guard Actions

- 供应商阻塞席位 grok 暂停普通补跑；额度/慢响应恢复后使用 --force-provider-blocked 做单席重试。
- 只补跑 rerunnable_seats 中的缺席席位，不重跑已合格席位。
- 前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。

## Production Artifacts

- seat journals: 12/12
- prompt contexts: 12/12
- forecast receipts: 12/12
- investment receipts: 12/12
- valid / blocked seats: 10 / 2
- god report seats/events: 13 / 78
- blocked: grok, qwen

## Latest Betting Method

- chatgpt：保守主胜分散布局；下注 5 单 / 决策 5 条，投入 92 GP，借款 0 GP。
- deepseek：以预测覆盖全部赛事，但仅在实时信息充分且存在明确正期望时才会投注，当前阶段观望为主。；下注 0 单 / 决策 5 条，投入 0 GP，借款 0 GP。
- mimo：结构化行协议回执；下注 3 单 / 决策 5 条，投入 500 GP，借款 0 GP。
- minimax：低风险种子赛保守下注；下注 3 单 / 决策 5 条，投入 450 GP，借款 0 GP。
- doubao：稳势低赔择优布局；下注 0 单 / 决策 5 条，投入 0 GP，借款 0 GP。
- gemini：分散防守反击策略；下注 4 单 / 决策 5 条，投入 1,000 GP，借款 0 GP。
- kimi：稳健跟盘，小额分散；下注 5 单 / 决策 5 条，投入 700 GP，借款 0 GP。
- meta：Low
risk
preservation:
forecast
all
matches,
no
bets
due
to
C-grade
credit
+
800gp
debt
+
lack
of
real-time
squad
data,
avoid
penalties
and
wait
for
clear
edge.；下注 0 单 / 决策 5 条，投入 0 GP，借款 0 GP。
- wenxin：择优投注控制风险；下注 3 单 / 决策 5 条，投入 450 GP，借款 0 GP。
- yuanbao：稳强队，博冷门；下注 2 单 / 决策 5 条，投入 700 GP，借款 300 GP。
- 待补席位：grok, qwen
