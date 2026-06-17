# PRED-INVEST SOP Guard · run-14

- date: 2026-06-14
- status: **PARTIAL_NOT_READY**
- bridge: idle
- recovered bridge: False
- quality gate: PARTIAL_NOT_READY (11/12)
- quality gate source: artifact
- publish frontend: False

## Errors

- none

## Warnings

- publish_blocked_by_quality_gate:11/12

## Needs Rerun

- grok

## Recommended Actions

- 只补跑 rerun_queue 中的缺席席位，不重跑已合格席位。
- 前端和日报必须标记 PARTIAL_NOT_READY，不得显示完整结论。
