# 2026-06-14 run-14 游戏 SOP 与桥接验收报告

生成时间：2026-06-14 24:24 HKT

## 结论

本轮已把 Grok 的「强制 fresh chat + 系统键盘注入」固化到底层 bridge，并完成 release reseal。新一轮游戏 SOP 已跑，葡萄牙 vs 哥伦比亚已被强制纳入 prompt pack 和审计口径。

但本轮不能发布为 12 席完整投注结果：严格审计后，只有 DeepSeek 产出了可直接入库的结构化 JSON 投注单；其余 11 席仍需补跑或增加结构化修复层。

## 已落地修复

1. CDP bridge 固化 Grok fresh chat 策略：
   - Grok 每次自动走 fresh navigation，不再依赖旧页面状态救援。
   - trace 标记：`cdp_fresh_navigation` / `seat_forced_fresh_chat`。

2. CDP bridge 固化 Grok 系统键盘提交：
   - Grok 使用 macOS System Events Enter 注入完成提交。
   - trace 标记：`cdp_system_keyboard_submit`。

3. JSON 投注单 contract 强化：
   - 世界杯预测池任务新增 `response_format=json`、`structured_json_required=true`。
   - bridge 的 final nudge 改为 JSON-only，不再用长文本补全提示污染投注单。

4. 葡萄牙 vs 哥伦比亚强制覆盖：
   - match_id：`WCAPI-20260627-COLOMBIA-PORTUGAL`
   - 盘口：
     - 胜平负：哥伦比亚 3.48 / 平 3.29 / 葡萄牙 2.10
     - 让球：哥伦比亚 +0.25 @2.00 / 葡萄牙 -0.25 @1.81
     - 总进球：大 2.25 @1.83 / 小 2.25 @1.96
   - 已写入 `required_matches.json`，并进入 prompt pack 与严格审计。

5. 新增严格审计脚本：
   - 只接受 JSON。
   - 要求 forecasts 覆盖全部 required matches。
   - 要求 investments 对每场给出 bet 或 no_bet。
   - 要求 self_audit ready。

## 本轮运行记录

主运行：
- `d2c66e23d985`

补跑：
- `6eeeabc3310b`
- `d03ac664f7e9`
- `e1f4c5392ee4`
- `67967f5e63c4`

SOP 输出：
- `2026-06-14_run-14_daily_sop.json`
- `2026-06-14_run-14_prompt_pack.json`
- `2026-06-14_run-14_bridge_output_audit.json`
- `2026-06-14_run-14_bridge_output_audit.md`

## 严格审计结果

必覆盖比赛：
- `WCAPI-20260614-GERMANY-CURA-AO`
- `WCAPI-20260614-NETHERLANDS-JAPAN`
- `WCAPI-20260614-IVORY-COAST-ECUADOR`
- `WCAPI-20260615-SWEDEN-TUNISIA`
- `WCAPI-20260627-COLOMBIA-PORTUGAL`

审计结果：
- 有效席位：1/12
- 有效席位：DeepSeek
- 需补跑/修复席位：ChatGPT、Doubao、Gemini、Grok、Kimi、Meta、MiMo、MiniMax、Qwen、Wenxin、Yuanbao

DeepSeek 可入库投注单：
- 荷兰 vs 日本：日本 +0.5 @1.89，投注 200 GP，不贷款。
- 德国 vs 库拉索：no_bet。
- 科特迪瓦 vs 厄瓜多尔：no_bet。
- 瑞典 vs 突尼斯：no_bet。
- 哥伦比亚 vs 葡萄牙：no_bet。

## 主要失败类型

1. 自然语言替代 JSON：
   - Gemini、Grok、Meta、MiMo、MiniMax、Qwen、Wenxin、Yuanbao 等仍返回可读文本，不符合可入库投注单 contract。

2. 无可采集回包：
   - ChatGPT 本轮未采到相关答案。
   - Doubao、Qwen、Wenxin 多次 slow_response_pending。

3. 覆盖范围错误：
   - Kimi 返回 JSON，但缺少强制比赛 `WCAPI-20260627-COLOMBIA-PORTUGAL`，同时扩展出多个非本轮 Portugal 伪 match id，不能入库。

## 验证状态

通过：
- Python 编译检查通过。
- 关键 JSON 文件解析通过。
- release status：`integrity=pass`，`drift_count=0`，`missing_count=0`。
- bridge status：空闲，可启动新 run，ready_count=13。
- Grok bridge 路径已进入 release seed。

未通过：
- 12 席完整投注单未通过。
- 本轮不能把自然语言输出当作前端投注结果发布。

## 下一步最小修复

1. 增加结构化修复层：
   - 对自然语言答案自动二次压缩为 JSON 投注单。
   - 修复层必须保留原文 archive，并标记 `derived_from_raw_answer=true`。
   - 若缺 required match，自动生成同席位补问，只问缺失比赛。

2. 对慢响应席位使用缺席补跑队列：
   - 不重跑已合格席位。
   - 每个缺席席位最多 2 次普通补跑 + 1 次极简 JSON-only 补跑。

3. 前端发布门禁保持严格：
   - 只有 valid JSON 才进入投注工作台。
   - 未合格席位展示“待补结构化投注单”，不能显示半截自然语言为下注结果。

