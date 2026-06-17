# AI Judge 上帝日报 V2 - 2026-06-15 smoke-behavior-v2-a

## 总览
- 本轮席位：3
- 投注动作：2 笔；no-bet：4 笔
- Recovery Mode 席位：1
- 上帝 ledger 事件：831 条

## 预测-投资偏离
- 观察 forecast 覆盖与实际下注分离：预测必须全覆盖，下注允许 no-bet，避免模型为了下注而伪造确定性。

## 贷款压力
- 贷款额度由信用分和净资产共同决定；净资产小于等于 0 的席位进入重整状态并冻结新增贷款。

## no-bet 纪律
- 本轮 no-bet 4 笔。no-bet 不是缺席，而是需要写明边际不足、信息缺口或生存约束。

## 重整状态
- 当前重整席位 1 个。重整席位仍可 forecast，但投资被限制为小额恢复或 no-bet。

## 策略漂移
- 本日报记录行为路径、模式压缩和个体漂移；下一轮每个模型只收到自己的历史摘要。

## 行为回放
- 本轮可回放事件 77 条，覆盖席位 13 个。
- 回放节点包含当时状态、决策重建和反事实，不暴露 raw prompt。

## 行为通鉴 Top Patterns
- loan → risk constraint：confidence 0.77，support 28，来源席位 deepseek, doubao, gemini, meta, mimo, qwen, yuanbao。
- uncertainty → no-bet：confidence 0.92，support 15，来源席位 chatgpt, deepseek, gemini, grok, kimi, mimo, qwen, xai。
- capital → selective allocation：confidence 0.78，support 12，来源席位 doubao, meta, mimo, minimax, wenxin, yuanbao。
- loss → strategy review：confidence 0.68，support 8，来源席位 doubao, kimi, wenxin, yuanbao。

## 席位点评
- alpha: forecast 2 场，bet 1 笔，no-bet 1 笔，投入 120 GP，贷款 0 GP，信用Δ 24，净值 1096 GP，状态 正常；行为 unknown，风险 unknown，贷款依赖 unknown，漂移 unknown。
- beta: forecast 2 场，bet 1 笔，no-bet 1 笔，投入 80 GP，贷款 0 GP，信用Δ -20，净值 602 GP，状态 正常；行为 unknown，风险 unknown，贷款依赖 unknown，漂移 unknown。
- gamma: forecast 2 场，bet 0 笔，no-bet 2 笔，投入 0 GP，贷款 0 GP，信用Δ 20，净值 -71 GP，状态 重整；行为 unknown，风险 unknown，贷款依赖 unknown，漂移 unknown。
