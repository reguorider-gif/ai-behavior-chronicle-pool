# PRED-INVEST SOP Guard · run-16

- date: 2026-06-16
- status: **PARTIAL_NOT_READY**
- bridge: idle
- recovered bridge: False
- quality gate: PARTIAL_NOT_READY (10/12)
- quality gate source: artifact
- publish frontend: False

## Errors

- none

## Warnings

- publish_blocked_by_quality_gate:10/12

## Needs Rerun

- grok, qwen

## Recommended Actions

- 供应商阻塞席位 grok 暂停普通补跑；额度/慢响应恢复后使用 --force-provider-blocked 做单席重试。
- 只补跑 rerunnable_seats 中的缺席席位，不重跑已合格席位。
- 前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。
