# 当前游戏内容 · PRED-INVEST-CREDIT-SURVIVE V2 · 2026-06-14 · run-14

- verdict: **NOT_READY**
- 模型：12/12
- 必须预测赛事：10 场
- 有盘口赛事：10 场
- 已收回结构化投资/观望决策：44 条
- 桥接席位门禁：11/12 部分回收；publish_allowed=False
- 新规则审计：0 可入账 / 0 需降额补字段 / 0 贷款冲突
- 原始投注额：2,590 GP
- 按新规则仓位上限转换后：2,590 GP

## 规则口径

- 每场比赛必须给 forecast；可以选择 no-bet。
- 投资不是强制 all-in；只有模型概率高于盘口隐含概率时才下注。
- 贷款由信用分、净资产、未还贷款决定；结算先还息还本，再排名。
- 旧规则下注会被保留为证据，但进入新账本前必须过仓位上限和贷款门禁。

## 数据缺口

- SOP errors：score_sync_overdue:WC-C1,WC-D2,WC-C2,WC-B2,WC-H1,WC-I1
- SOP warnings：no_existing_bets_to_shadow_audit_bridge_run_required; bet_receipts_missing:unknown; sop_guard:publish_blocked_by_quality_gate:11/12; quality_gate_partial:11/12
- 桥接待补跑席位：grok

## 当前赛事

- WC-C1 · Haiti vs Scotland · 12 条盘口样本 · Haiti handicap 1.5 @ 1.54
- WC-D2 · Australia vs Turkey · 12 条盘口样本 · Australia handicap 1.5 @ 1.42
- WC-C2 · Brazil vs Morocco · 12 条盘口样本 · Brazil handicap -1.5 @ 2.88
- WC-B2 · Qatar vs Switzerland · 12 条盘口样本 · Qatar handicap 1.5 @ 2.25
- WCAPI-20260614-GERMANY-CURA-AO · Germany vs Curaçao · 12 条盘口样本 · Curaçao handicap 3.5 @ 1.83
- WCAPI-20260614-NETHERLANDS-JAPAN · Netherlands vs Japan · 12 条盘口样本 · Japan handicap  @ 2.87
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ivory Coast vs Ecuador · 12 条盘口样本 · Ecuador handicap  @ 1.59
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden vs Tunisia · 12 条盘口样本 · Sweden handicap  @ 1.37
- WC-H1 · Spain vs Cape Verde · 3 条盘口样本 · Spain h2h  @ 1.08
- WC-I1 · France vs Senegal · 3 条盘口样本 · France h2h  @ 1.35

## 逐模型新规则投注方式

### chatgpt

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 80 GP，新规转换 80 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 80 GP，新规 80 GP，bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.85：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador handicap 0 @ 1.59：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap -0.5 @ 1.88：原始 0 GP，新规 0 GP，no_bet；无

### deepseek

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 200 GP，新规转换 200 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.89：原始 200 GP，新规 200 GP，bet；无
- WCAPI-20260614-GERMANY-CURA-AO ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA ·  @ None：原始 0 GP，新规 0 GP，no_bet；无

### mimo

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Netherlands handicap 0 @ 1.0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ivory Coast handicap 0 @ 1.0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap 0 @ 1.0：原始 0 GP，新规 0 GP，no_bet；无

### minimax

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 100 GP，新规转换 100 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao +3.5 handicap 3.5 @ 1.83：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.0 @ 2.87：原始 40 GP，新规 40 GP，bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador 0.0 handicap 0.0 @ 1.59：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap -0.5 @ 1.88：原始 60 GP，新规 60 GP，bet；无

### doubao

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 1,100 GP，新规转换 1,100 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 400 GP，新规 400 GP，bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.85：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador handicap 0.0 @ 1.59：原始 300 GP，新规 300 GP，bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap 0.0 @ 1.37：原始 400 GP，新规 400 GP，bet；无

### gemini

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 450 GP，新规转换 450 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.85：原始 200 GP，新规 200 GP，bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador handicap -0.5 @ 2.45：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap -0.5 @ 1.88：原始 250 GP，新规 250 GP，bet；无

### kimi

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 550 GP，新规转换 550 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 100 GP，新规 100 GP，bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.85：原始 250 GP，新规 250 GP，bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador handicap -0.5 @ 2.45：原始 100 GP，新规 100 GP，bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap -0.5 @ 1.88：原始 100 GP，新规 100 GP，bet；无

### meta

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao +3.5 handicap 3.5 @ 1.83：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan +0.5 handicap 0.5 @ 1.85：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador 0 handicap 0.0 @ 1.59：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden -0.5 handicap -0.5 @ 1.88：原始 0 GP，新规 0 GP，no_bet；无

### qwen

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · none none 0 @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · none none 0 @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · none none 0 @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · none none 0 @ 0：原始 0 GP，新规 0 GP，no_bet；无

### wenxin

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 60 GP，新规转换 60 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 10 GP，新规 10 GP，bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.85：原始 15 GP，新规 15 GP，bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador handicap 0.0 @ 1.59：原始 20 GP，新规 20 GP，bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap 0.0 @ 1.37：原始 15 GP，新规 15 GP，bet；无

### yuanbao

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：4 笔；原始 50 GP，新规转换 50 GP。
- 处理：strict_report_validated_decision
- WCAPI-20260614-GERMANY-CURA-AO · Curaçao handicap 3.5 @ 1.83：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260614-NETHERLANDS-JAPAN · Japan handicap 0.5 @ 1.85：原始 50 GP，新规 50 GP，bet；无
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ecuador handicap -0.5 @ 2.45：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden handicap -0.5 @ 1.88：原始 0 GP，新规 0 GP，no_bet；无

> 说明：这是基于当前 run-14 投注资料的新规则影子重跑；真实外发 12 模型重答需要接入 AI Judge bridge 执行器。
