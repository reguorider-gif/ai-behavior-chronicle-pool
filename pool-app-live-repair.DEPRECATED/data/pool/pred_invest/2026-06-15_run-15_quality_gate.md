# PRED-INVEST Quality Gate · run-15

- date: 2026-06-15
- status: **PARTIAL_NOT_READY**
- publish allowed: False
- frontend badge: 11/12 部分回收
- valid seats: 11/12 (chatgpt, deepseek, doubao, gemini, kimi, meta, mimo, minimax, qwen, wenxin, yuanbao)
- needs rerun: grok

## Rerun Queue

| Seat | Mode | Prompt | Reason |
| --- | --- | --- | --- |
| grok | provider_quota_blocked | wait_for_quota_reset | 供应商额度限制，页面未生成当前轮答案；不能继续普通补跑，需额度恢复后单席重试。 |

## Product Findings

- 发布状态必须来自 quality_gate.publish_allowed，不得只看有无任意模型答案。
- 前端必须展示 frontend_badge 和 needs_rerun，避免用户误以为本轮已全量。
- 日报可以引用部分上帝报告，但标题必须标注 PARTIAL_NOT_READY。
- 自动化下一步只能补跑 rerun_queue，不应重跑已合格席位。
- provider_blocked_seats 不进入普通自动补跑；供应商额度/慢响应恢复后才能单席强制重试。
- 同一轮发布门禁使用 required_match_snapshot 或上次质量门禁冻结口径，避免 prompt_pack 刷新后误伤已合格席位。
- 供应商额度限制必须作为阻塞态呈现，不得被误判为普通 coverage failure 反复补跑。
