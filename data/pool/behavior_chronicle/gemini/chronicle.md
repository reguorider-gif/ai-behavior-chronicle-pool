# gemini 行为通鉴

- generated_at: 2026-06-21T21:42:55+00:00
- lesson_count: 5

## Prompt Injection

行为通鉴经验（只来自你自己的历史）：
必须规避：
- 避免复现：下一轮信息缺口未补齐时，置信度必须降档，下注动作默认 no-bet。
继续观察：
- 继续观察：下一轮高赔率下注必须给出模型概率、盘口隐含概率和止损边界。
- 继续观察：下一轮必须说明主队优势来自盘口边际还是惯性偏好。
- 继续观察：保留 no-bet 合法性，但必须说明信息缺口和机会成本。
本轮输出必须说明：哪些历史经验被采用，哪些被拒绝，以及原因。

## Lessons

- [observe] 继续观察：下一轮高赔率下注必须给出模型概率、盘口隐含概率和止损边界。（pattern=longshot_seeking, confidence=0.82）
- [observe] 继续观察：下一轮必须说明主队优势来自盘口边际还是惯性偏好。（pattern=home_bias, confidence=0.81）
- [observe] 继续观察：保留 no-bet 合法性，但必须说明信息缺口和机会成本。（pattern=uncertainty_to_no_bet, confidence=0.81）
- [avoid] 避免复现：下一轮信息缺口未补齐时，置信度必须降档，下注动作默认 no-bet。（pattern=high_confidence_low_information, confidence=0.8）
- [observe] 继续观察：下一轮需要说明热门判断是否来自真实信号，而不是默认追随强队。（pattern=favorite_bias, confidence=0.684）
