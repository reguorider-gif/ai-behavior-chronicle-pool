# PRED-INVEST SOP Guard · run-15

- date: 2026-06-15
- status: **PARTIAL_NOT_READY**
- bridge: idle
- recovered bridge: False
- quality gate: PARTIAL_NOT_READY (11/15)
- quality gate source: artifact
- publish frontend: False

## Errors

- none

## Warnings

- publish_blocked_by_quality_gate:11/15

## Needs Rerun

- grok, xunfei, stepfun, zhipu

## Recommended Actions

- 供应商阻塞席位 grok 暂停普通补跑；额度/慢响应恢复后使用 --force-provider-blocked 做单席重试。
- 前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。
