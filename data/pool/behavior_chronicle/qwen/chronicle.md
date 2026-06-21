# qwen 行为通鉴

- generated_at: 2026-06-21T21:42:55+00:00
- lesson_count: 3

## Prompt Injection

行为通鉴经验（只来自你自己的历史）：
必须规避：
- 避免复现：下一轮信息缺口未补齐时，置信度必须降档，下注动作默认 no-bet。
继续观察：
- 继续观察：保留 no-bet 合法性，但必须说明信息缺口和机会成本。
- 继续观察：下一轮必须显式评估平局基准概率，避免把平局系统性低估。
本轮输出必须说明：哪些历史经验被采用，哪些被拒绝，以及原因。

## Lessons

- [observe] 继续观察：保留 no-bet 合法性，但必须说明信息缺口和机会成本。（pattern=uncertainty_to_no_bet, confidence=0.81）
- [observe] 继续观察：下一轮必须显式评估平局基准概率，避免把平局系统性低估。（pattern=draw_avoidance, confidence=0.72）
- [avoid] 避免复现：下一轮信息缺口未补齐时，置信度必须降档，下注动作默认 no-bet。（pattern=high_confidence_low_information, confidence=0.68）
