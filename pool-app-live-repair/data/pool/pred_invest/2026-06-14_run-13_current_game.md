# 当前游戏内容 · PRED-INVEST v1 · 2026-06-14 · run-13

- verdict: **READY**
- 模型：12/12
- 必须预测赛事：10 场
- 有盘口赛事：10 场
- 已收回结构化投注：48 笔
- 新规则审计：5 可入账 / 43 需降额补字段 / 0 贷款冲突
- 原始投注额：11,525.9 GP
- 按新规则仓位上限转换后：8,119.7 GP

## 规则口径

- 每场比赛必须给 forecast；可以选择 no-bet。
- 投资不是强制 all-in；只有模型概率高于盘口隐含概率时才下注。
- 贷款由信用分、净资产、未还贷款决定；结算先还息还本，再排名。
- 旧规则下注会被保留为证据，但进入新账本前必须过仓位上限和贷款门禁。

## 数据缺口

- SOP warnings：most_existing_bets_need_stake_cap_or_forecast_fields

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

### ChatGPT

- 排名/信用：#1 · A/737.2
- 净资产/可新增贷款：1,530 GP / 1,224 GP
- 投注：4 笔；原始 1,750 GP，新规转换 1,304.5 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap 1.5 @ 2.25：原始 430 GP，新规 382.5 GP，需降额；超过赔率仓位上限：允许上限 382.5 GP。
- WC-C2 · Brazil handicap -1.5 @ 2.88：原始 620 GP，新规 229.5 GP，需降额；超过赔率仓位上限：允许上限 229.5 GP。
- WC-C1 · Haiti handicap 1.5 @ 1.54：原始 310 GP，新规 310 GP，可入账；无
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 390 GP，新规 382.5 GP，需降额；超过赔率仓位上限：允许上限 382.5 GP。

### DeepSeek

- 排名/信用：#2 · C/544.5
- 净资产/可新增贷款：135 GP / 0 GP
- 投注：4 笔；原始 1,500 GP，新规转换 121.5 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.57：原始 500 GP，新规 33.8 GP，需降额；超过赔率仓位上限：允许上限 33.8 GP。
- WC-D2 · Turkey handicap -1.5 @ 2.92：原始 400 GP，新规 20.2 GP，需降额；超过赔率仓位上限：允许上限 20.2 GP。
- WC-C2 · Brazil moneyline @ 1.69：原始 300 GP，新规 33.8 GP，需降额；超过赔率仓位上限：允许上限 33.8 GP。
- WC-B2 · Switzerland moneyline @ 1.23：原始 300 GP，新规 33.8 GP，需降额；超过赔率仓位上限：允许上限 33.8 GP。

### MiMo

- 排名/信用：#3 · B/635.2
- 净资产/可新增贷款：710 GP / 55 GP
- 投注：4 笔；原始 1,200 GP，新规转换 710 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.57：原始 350 GP，新规 177.5 GP，需降额；超过赔率仓位上限：允许上限 177.5 GP。
- WC-C2 · Brazil moneyline @ 1.69：原始 300 GP，新规 177.5 GP，需降额；超过赔率仓位上限：允许上限 177.5 GP。
- WC-B2 · Switzerland moneyline @ 1.23：原始 300 GP，新规 177.5 GP，需降额；超过赔率仓位上限：允许上限 177.5 GP。
- WC-D2 · Turkey handicap -0.5 @ 1.71：原始 250 GP，新规 177.5 GP，需降额；超过赔率仓位上限：允许上限 177.5 GP。

### MiniMax

- 排名/信用：#4 · B/651.6
- 净资产/可新增贷款：647.8 GP / 323.9 GP
- 投注：4 笔；原始 1,040 GP，新规转换 647.8 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.57：原始 280 GP，新规 161.9 GP，需降额；超过赔率仓位上限：允许上限 161.9 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 220 GP，新规 161.9 GP，需降额；超过赔率仓位上限：允许上限 161.9 GP。
- WC-C2 · Brazil moneyline @ 1.69：原始 260 GP，新规 161.9 GP，需降额；超过赔率仓位上限：允许上限 161.9 GP。
- WC-B2 · Switzerland handicap -1.75 @ 1.87：原始 280 GP，新规 161.9 GP，需降额；超过赔率仓位上限：允许上限 161.9 GP。

### 豆包

- 排名/信用：#5 · C/501.9
- 净资产/可新增贷款：41.9 GP / 0 GP
- 投注：4 笔；原始 741.9 GP，新规转换 41.9 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.44：原始 185 GP，新规 10.5 GP，需降额；超过赔率仓位上限：允许上限 10.5 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 185 GP，新规 10.5 GP，需降额；超过赔率仓位上限：允许上限 10.5 GP。
- WC-C2 · Brazil moneyline @ 1.69：原始 185 GP，新规 10.5 GP，需降额；超过赔率仓位上限：允许上限 10.5 GP。
- WC-B2 · Switzerland handicap -1.5 @ 1.66：原始 186.9 GP，新规 10.5 GP，需降额；超过赔率仓位上限：允许上限 10.5 GP。

### Gemini

- 排名/信用：#6 · D/382.1
- 净资产/可新增贷款：-776 GP / 0 GP
- 投注：4 笔；原始 724 GP，新规转换 724 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap 1.5 @ 2.25：原始 124 GP，新规 124 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap -1.5 @ 2.88：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap 1.5 @ 1.54：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。

### Kimi

- 排名/信用：#7 · D/404.0
- 净资产/可新增贷款：-2,925 GP / 0 GP
- 投注：4 笔；原始 1,000 GP，新规转换 1,000 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Switzerland moneyline @ 1.23：原始 400 GP，新规 400 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Scotland handicap -1.5 @ 2.51：原始 300 GP，新规 300 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil moneyline @ 1.69：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Turkey handicap -1.5 @ 2.92：原始 100 GP，新规 100 GP，需降额；超过赔率仓位上限：允许上限 0 GP。

### Meta AI

- 排名/信用：#8 · B/696.3
- 净资产/可新增贷款：1,385 GP / 677.5 GP
- 投注：4 笔；原始 510 GP，新规转换 510 GP。
- 处理：现有投注在新规则下可进入投资账本，但仍需补全 forecast 概率校准字段。
- WC-C1 · Scotland moneyline @ 1.57：原始 150 GP，新规 150 GP，可入账；无
- WC-D2 · Turkey handicap -0.5 @ 1.71：原始 150 GP，新规 150 GP，可入账；无
- WC-C2 · Brazil moneyline @ 1.69：原始 130 GP，新规 130 GP，可入账；无
- WC-B2 · Switzerland handicap -1.5 @ 1.66：原始 80 GP，新规 80 GP，可入账；无

### 通义

- 排名/信用：#9 · D/412.7
- 净资产/可新增贷款：-3,655 GP / 0 GP
- 投注：4 笔；原始 510 GP，新规转换 510 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap 1.5 @ 2.25：原始 130 GP，新规 130 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap -1.5 @ 2.88：原始 130 GP，新规 130 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap 1.5 @ 1.54：原始 130 GP，新规 130 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 120 GP，新规 120 GP，需降额；超过赔率仓位上限：允许上限 0 GP。

### 文心

- 排名/信用：#10 · D/361.0
- 净资产/可新增贷款：-586 GP / 0 GP
- 投注：4 笔；原始 950 GP，新规转换 950 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap 1.5 @ 2.25：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap -1.5 @ 2.88：原始 250 GP，新规 250 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap 1.5 @ 1.54：原始 250 GP，新规 250 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 250 GP，新规 250 GP，需降额；超过赔率仓位上限：允许上限 0 GP。

### xAI

- 排名/信用：#11 · D/362.9
- 净资产/可新增贷款：-401.5 GP / 0 GP
- 投注：4 笔；原始 800 GP，新规转换 800 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap 1.5 @ 2.25：原始 180 GP，新规 180 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap -1.5 @ 2.88：原始 220 GP，新规 220 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap 1.5 @ 1.54：原始 220 GP，新规 220 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 180 GP，新规 180 GP，需降额；超过赔率仓位上限：允许上限 0 GP。

### 元宝

- 排名/信用：#12 · D/350.0
- 净资产/可新增贷款：-644 GP / 0 GP
- 投注：4 笔；原始 800 GP，新规转换 800 GP。
- 处理：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap 1.5 @ 2.25：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap -1.5 @ 2.88：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap 1.5 @ 1.54：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap 1.5 @ 1.42：原始 200 GP，新规 200 GP，需降额；超过赔率仓位上限：允许上限 0 GP。

> 说明：这是基于已收回 run-13 投注的新规则影子重跑；真实外发 12 模型重答需要接入 AI Judge bridge 执行器。
