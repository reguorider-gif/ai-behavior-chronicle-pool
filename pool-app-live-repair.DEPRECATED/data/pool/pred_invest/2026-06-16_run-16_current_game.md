# 当前游戏内容 · PRED-INVEST-CREDIT-SURVIVE V2 · 2026-06-16 · run-16

- verdict: **PARTIAL_NOT_READY**
- 模型：12/12
- 必须预测赛事：5 场
- 有盘口赛事：5 场
- 已收回结构化投资/观望决策：50 条
- 桥接席位门禁：10/12 部分回收；publish_allowed=False
- strict 门禁：10/12 席有效，待补 2 席。
- 原始投注额：3,892 GP
- 按新规则仓位上限转换后：3,892 GP

## 规则口径

- 每场比赛必须给 forecast；可以选择 no-bet。
- 投资不是强制 all-in；只有模型概率高于盘口隐含概率时才下注。
- 贷款由信用分、净资产、未还贷款决定；结算先还息还本，再排名。
- 旧规则下注会被保留为证据，但进入新账本前必须过仓位上限和贷款门禁。

## 数据缺口

- SOP warnings：sop_guard:publish_blocked_by_quality_gate:10/12; quality_gate_partial:10/12
- 桥接待补跑席位：grok, qwen

## 当前赛事

- WC-I1 · France vs Senegal · 7 条盘口样本 · France h2h  @ 1.46
- WC-SEED-20260617-ENGLAND-CROATIA · England vs Croatia · 7 条盘口样本 · England h2h  @ 1.85
- WC-SEED-20260617-GHANA-PANAMA · Ghana vs Panama · 7 条盘口样本 · Ghana h2h  @ 2.03
- WC-SEED-20260617-PORTUGAL-CONGO-DR · Portugal vs Congo DR · 7 条盘口样本 · Portugal h2h  @ 1.27
- WC-SEED-20260617-UZBEKISTAN-COLOMBIA · Uzbekistan vs Colombia · 7 条盘口样本 · Uzbekistan h2h  @ 5.9

## 逐模型新规则投注方式

### chatgpt

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 92 GP，新规转换 92 GP。
- 处理：strict_report_validated_decision
- WC-I1 · France moneyline none @ 1.46：原始 20 GP，新规 20 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · England moneyline none @ 1.85：原始 20 GP，新规 20 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · Ghana moneyline none @ 2.03：原始 12 GP，新规 12 GP，bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · Portugal moneyline none @ 1.27：原始 25 GP，新规 25 GP，bet；无

### deepseek

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WC-I1 ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-ENGLAND-CROATIA ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-GHANA-PANAMA ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR ·  @ None：原始 0 GP，新规 0 GP，no_bet；无

### mimo

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 500 GP，新规转换 500 GP。
- 处理：strict_report_validated_decision
- WC-I1 · France moneyline 1.46 @ 1.46：原始 150 GP，新规 150 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · England moneyline 1.85 @ 1.85：原始 200 GP，新规 200 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · Ghana moneyline 2.03 @ 2.03：原始 150 GP，新规 150 GP，bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无

### minimax

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 450 GP，新规转换 450 GP。
- 处理：strict_report_validated_decision
- WC-I1 · France moneyline 0 @ 1.46：原始 150 GP，新规 150 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · England moneyline 0 @ 1.85：原始 120 GP，新规 120 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · Portugal moneyline 0 @ 1.27：原始 180 GP，新规 180 GP，bet；无

### doubao

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WC-I1 · France moneyline 1.46 @ 220：原始 0 GP，新规 0 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · England moneyline 1.85 @ 180：原始 0 GP，新规 0 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · Ghana moneyline 2.03 @ 150：原始 0 GP，新规 0 GP，bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · Portugal moneyline 1.27 @ 250：原始 0 GP，新规 0 GP，bet；无

### gemini

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 1,000 GP，新规转换 1,000 GP。
- 处理：strict_report_validated_decision
- WC-I1 · France moneyline - @ 1.46：原始 300 GP，新规 300 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · England moneyline - @ 1.85：原始 200 GP，新规 200 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · Ghana moneyline - @ 2.03：原始 100 GP，新规 100 GP，bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · Portugal moneyline - @ 1.27：原始 400 GP，新规 400 GP，bet；无

### kimi

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 700 GP，新规转换 700 GP。
- 处理：strict_report_validated_decision
- WC-I1 · home moneyline none @ 1.46：原始 150 GP，新规 150 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · home moneyline none @ 1.85：原始 120 GP，新规 120 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · home moneyline none @ 2.03：原始 100 GP，新规 100 GP，bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · home moneyline none @ 1.27：原始 200 GP，新规 200 GP，bet；无

### meta

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 0 GP，新规转换 0 GP。
- 处理：strict_report_validated_decision
- WC-I1 ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-ENGLAND-CROATIA ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-GHANA-PANAMA ·  @ None：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR ·  @ None：原始 0 GP，新规 0 GP，no_bet；无

### wenxin

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 450 GP，新规转换 450 GP。
- 处理：strict_report_validated_decision
- WC-I1 · home moneyline h2h @ 1.46：原始 100 GP，新规 100 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · home moneyline h2h @ 1.85：原始 150 GP，新规 150 GP，bet；无
- WC-SEED-20260617-GHANA-PANAMA · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · home moneyline h2h @ 1.27：原始 200 GP，新规 200 GP，bet；无

### yuanbao

- 排名/信用：#None · None/None
- 净资产/可新增贷款：0 GP / 0 GP
- 投注：5 笔；原始 700 GP，新规转换 700 GP。
- 处理：strict_report_validated_decision
- WC-I1 · home moneyline none @ 1.46：原始 300 GP，新规 300 GP，bet；无
- WC-SEED-20260617-ENGLAND-CROATIA · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-GHANA-PANAMA · none none none @ 0：原始 0 GP，新规 0 GP，no_bet；无
- WC-SEED-20260617-PORTUGAL-CONGO-DR · home moneyline none @ 1.27：原始 400 GP，新规 400 GP，bet；无

> 说明：This bundle uses strict AI Judge output as the current decision source; it remains partial until the hard gate reaches 12/12.
