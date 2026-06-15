# 当前游戏内容 · PRED-INVEST-CREDIT-SURVIVE V2 · 2026-06-15 · run-15

- verdict: **PARTIAL_NOT_READY**
- 模型：12/12
- 必须预测赛事：5 场
- 有盘口赛事：5 场
- 已收回结构化投资/观望决策：55 条
- 桥接席位门禁：11/12 部分回收；publish_allowed=False
- strict 门禁：11/12 席有效，待补 1 席。
- 原始投注额：4,170 GP
- 按新规则仓位上限转换后：4,170 GP

## 规则口径

- 每场比赛必须给 forecast；可以选择 no-bet。
- 投资不是强制 all-in；只有模型概率高于盘口隐含概率时才下注。
- 贷款由信用分、净资产、未还贷款决定；结算先还息还本，再排名。
- 旧规则下注会被保留为证据，但进入新账本前必须过仓位上限和贷款门禁。

## 数据缺口

- SOP warnings：sop_guard:publish_blocked_by_quality_gate:11/12; quality_gate_partial:11/12
- 桥接待补跑席位：grok

## 当前赛事

- WC-H1 · Spain vs Cape Verde · 3 条盘口样本 · Spain h2h  @ 1.08
- WC-K1 · Portugal vs Colombia · 3 条盘口样本 · Portugal h2h  @ 1.75
- WCAPI-20260615-BELGIUM-EGYPT · Belgium vs Egypt · 12 条盘口样本 · Belgium handicap  @ 2.81
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · Saudi Arabia vs Uruguay · 12 条盘口样本 · Saudi Arabia handicap  @ 1.62
- WCAPI-20260616-IRAN-NEW-ZEALAND · Iran vs New Zealand · 12 条盘口样本 · Iran handicap  @ 3.34

## 逐模型新规则投注方式

### chatgpt

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 180 GP，新规转换 180 GP。
- 处理：strict_report_validated_decision
- WC-H1 · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 · Portugal moneyline none @ 1.75：原始 180 GP，新规 180 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无

### deepseek

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WC-H1 ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-BELGIUM-EGYPT · handicap @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · handicap @ None：原始 0 GP，新规 0 GP，no_bet；无

### mimo

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 400 GP，新规转换 400 GP。
- 处理：strict_report_validated_decision
- WC-H1 · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-BELGIUM-EGYPT · Belgium handicap -1 @ 2.27：原始 200 GP，新规 200 GP，bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · Saudi Arabia handicap +0.5 @ 1.62：原始 200 GP，新规 200 GP，bet；无

### minimax

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 300 GP，新规转换 300 GP。
- 处理：strict_report_validated_decision
- WC-H1 · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 · Portugal moneyline none @ 1.75：原始 80 GP，新规 80 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · Belgium handicap -0.75 @ 2.27：原始 100 GP，新规 100 GP，bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · none handicap none @ 0：原始 0 GP，新规 0 GP，no_bet；无

### doubao

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 600 GP，新规转换 600 GP。
- 处理：strict_report_validated_decision
- WC-H1 · Spain moneyline 0 @ 1.08：原始 200 GP，新规 200 GP，bet；无
- WC-K1 · Portugal moneyline 0 @ 1.75：原始 200 GP，新规 200 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · Uruguay handicap 0 @ 2.24：原始 200 GP，新规 200 GP，bet；无

### gemini

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 50 GP，新规转换 50 GP。
- 处理：strict_report_validated_decision
- WC-H1 ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 · Draw h2h @ 3.6：原始 50 GP，新规 50 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY ·  @ None：原始 0 GP，新规 0 GP，no_bet；无

### kimi

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 40 GP，新规转换 40 GP。
- 处理：strict_report_validated_decision
- WC-H1 · Spain h2h @ 1.08：原始 40 GP，新规 40 GP，bet；无
- WC-K1 · h2h @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-BELGIUM-EGYPT · handicap @ None：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · handicap @ None：原始 0 GP，新规 0 GP，no_bet；无

### meta

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 900 GP，新规转换 900 GP。
- 处理：strict_report_validated_decision
- WC-H1 · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 · Portugal moneyline none @ 1.75：原始 400 GP，新规 400 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · Belgium handicap -1.5 @ 2.81：原始 300 GP，新规 300 GP，bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无

### qwen

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 100 GP，新规转换 100 GP。
- 处理：strict_report_validated_decision
- WC-H1 · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-K1 · Portugal moneyline 0 @ 1.75：原始 100 GP，新规 100 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无

### wenxin

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 600 GP，新规转换 600 GP。
- 处理：strict_report_validated_decision
- WC-H1 · Spain h2h none @ 1.08：原始 150 GP，新规 150 GP，bet；无
- WC-K1 · Portugal h2h none @ 1.75：原始 150 GP，新规 150 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · Saudi Arabia handicap none @ 1.62：原始 200 GP，新规 200 GP，bet；无

### yuanbao

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 1,000 GP，新规转换 1,000 GP。
- 处理：strict_report_validated_decision
- WC-H1 · home moneyline none @ 1.08：原始 500 GP，新规 500 GP，bet；无
- WC-K1 · home moneyline none @ 1.75：原始 200 GP，新规 200 GP，bet；无
- WCAPI-20260615-BELGIUM-EGYPT · Belgium handicap - @ 2.27：原始 200 GP，新规 200 GP，bet；无
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无

> 说明：This bundle uses strict AI Judge output as the current decision source; it remains partial until the hard gate reaches 12/12.
