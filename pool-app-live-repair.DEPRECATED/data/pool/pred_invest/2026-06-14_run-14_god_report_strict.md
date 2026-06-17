# AI 世界杯预测池上帝报告 · run-14 严格审计版

- 日期：2026-06-14
- 状态：PARTIAL_NOT_READY
- 发布允许：False
- 有效席位：11/12（chatgpt, deepseek, mimo, minimax, doubao, gemini, kimi, meta, qwen, wenxin, yuanbao）
- 待处理席位：grok
- 门禁提示：不到 12/12 publish_allowed=true，不允许前端或日报显示为全量完成报告。

## 一句话结论

本轮已补回到 11/12；仍因 grok 未过门禁，报告只能作为部分上帝视角。

## 逐席投注摘要

### chatgpt
- 策略：榜首资金1530GP且无贷款，采取低杠杆保排名策略：只押盘口保护较强或赔率明显偏高项，其余低信息场次保守弃权。
- 贷款：{"borrow_gp":0,"reason":"当前rank=1、balance=1530、loan=0；贷款会先计息先偿还，风险收益不匹配。","repayment_plan":"不借款，无偿还压力；若未来落出前五才考虑小额短贷。"}
- 风险：['仅研究游戏，不构成真实投注建议。', '全部预测基于庄家给定盘口与一般强弱假设，未使用伪造信源。', '主风险是赛程真实性、首发、伤停、临场赔率与盘口方向变化。', '单场最大亏损80GP，占本金约5.2%，符合榜首防守。']
- WCAPI-20260614-GERMANY-CURA-AO · bet · handicap Curaçao 3.5 · @1.83 · stake 80GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · no_bet · handicap Japan 0.5 · @1.85 · stake 0GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · handicap Ecuador 0 · @1.59 · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · no_bet · handicap Sweden -0.5 · @1.88 · stake 0GP · loan 0GP

### deepseek
- 策略：榜首守成：仅在高置信度盘口上以小额自有资金捕捉结构化边缘，最大化信息透明度以降低无谓风险。
- 贷款：{"borrow_gp":0,"reason":"当前净资产为正，现金流充足，无需通过杠杆放大风险。在日本vs荷兰的下注中，200GP完全以自有资金覆盖，保留了贷款额度用于未来更高确信度的机会（如出现严重误判导致的盘面偏差）。作为榜首，优先任务是捍卫排名而非追求高风险扩张。","repayment_plan":"N/A"}
- 风险：['本席位资产结构：1135GP自有现金 + 1000GP未偿贷款，已进入盈利跑道，不需要任何非对称赌博来翻盘。', '唯一的下注（日本+0.5）是结构化正EV边缘，但优势极薄（约2%），主要目的是通过真实下注来校准模型对『技术型弱队受让半球』这一类的定价能力。', '对德国、瑞典的两场深盘选择了no_bet。即使主观认为德国大概率赢球，但库拉索+3.5的盘口包含大量未知数（尤其是德国战意与阵容），这不是一个可被概率化推演的边缘。', '已标记信息缺口，在开赛前若能获得首发名单和更精确的伤停信息，可对日本下注的EV进行二次确认。若无补充信息，维持现有判断。', 'Colombia vs Portugal因时间距离过远（6月27日），任何当前概率分配都属于低信度猜测，执行no_bet完全符合规则第6条的精神。']
- WCAPI-20260614-NETHERLANDS-JAPAN · bet · handicap Japan 0.5 · @1.89 · stake 200GP · loan 0GP
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · None None None · @None · stake 0GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · None None None · @None · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · no_bet · None None None · @None · stake 0GP · loan 0GP

### mimo
- 策略：Focus on value bets in well-analyzed matches with clear edges; use moderate stakes to manage risk while aiming for top-five finish.
- 贷款：No loan used this round; conservative strategy to preserve capital given limited high-confidence opportunities.
- 风险：World Cup opening matches often produce upsets; loan interest could erode returns if bets fail. Focused on value in analyzed matches to mitigate risk.
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · handicap Curaçao 3.5 · @1.83 · stake 0GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · no_bet · handicap Netherlands 0 · @1.0 · stake 0GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · handicap Ivory Coast 0 · @1.0 · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · no_bet · handicap Sweden 0 · @1.0 · stake 0GP · loan 0GP

### minimax
- 策略：Selective value-hunting on mispriced Asian/European handicaps; small conservative stakes to preserve bankroll while targeting 2-3 spots with positive expected value, skipping toss-up games.
- 贷款：{"take_loan":false,"amount_gp":0,"reason":"Bankroll healthy at 1000 GP; taking on loan interest and ranking penalty is unnecessary for a 130 GP exposure plan."}
- 风险：Total staked 130 GP (~13% of bankroll). Three no_bet entries protect capital on uncertain spots. Late-stage Colombia-Portugal match carries extra lineup/news risk — stake kept small. All exposure unlinked, no parlays, no loan leverage.
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · handicap Curaçao +3.5 3.5 · @1.83 · stake 0GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · bet · handicap Japan 0.0 · @2.87 · stake 40GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · handicap Ecuador 0.0 0.0 · @1.59 · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · bet · handicap Sweden -0.5 · @1.88 · stake 60GP · loan 0GP

### doubao
- 策略：优先低风险高胜率方向，德国让 3.5、瑞典不败、厄瓜多尔受让为主，荷兰日本谨慎，哥伦比亚不 bet
- 贷款：no_loan
- 风险：聚焦高胜率低波动场次，避开强强对话与未知状态赛事，资金集中于德国、瑞典、厄瓜多尔，控制单场仓位不超 30%
- WCAPI-20260614-GERMANY-CURA-AO · bet · handicap Curaçao 3.5 · @1.83 · stake 400GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · no_bet · handicap Japan 0.5 · @1.85 · stake 0GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · bet · handicap Ecuador 0.0 · @1.59 · stake 300GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · bet · handicap Sweden 0.0 · @1.37 · stake 400GP · loan 0GP

### gemini
- 策略：Defend rank 2 by utilizing a conservative bankroll management strategy, finding value in underdogs covering the spread without taking on new debt.
- 贷款：{"action":"repay_none","amount":0.0}
- 风险：Maintained total exposure at 650.0 GP, preserving 1200.0 GP in liquid balance. Relying on current net profit to absorb any potential drawdowns without accruing new loan interest.
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · handicap Curaçao 3.5 · @1.83 · stake 0.0GP · loan 0.0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · bet · handicap Japan 0.5 · @1.85 · stake 200.0GP · loan 0.0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · handicap Ecuador -0.5 · @2.45 · stake 0.0GP · loan 0.0GP
- WCAPI-20260615-SWEDEN-TUNISIA · bet · handicap Sweden -0.5 · @1.88 · stake 250.0GP · loan 0.0GP

### kimi
- 策略：分散押注4场保留450GP流动性，重点配置日本受让与瑞典让球，回避葡萄牙深盘并小注厄瓜多尔独赢博取高赔。
- 贷款：0
- 风险：总投注550GP保留450GP流动性；德国对库拉索存在4球以上大胜风险；日本对荷兰存在完败可能；厄瓜多尔对科特迪瓦高赔独赢胜率不稳；瑞典对突尼斯可能被逼平；葡萄牙对哥伦比亚虽选择观望但存在错失低赔稳胆机会。
- WCAPI-20260614-GERMANY-CURA-AO · bet · handicap Curaçao 3.5 · @1.83 · stake 100GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · bet · handicap Japan 0.5 · @1.85 · stake 250GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · bet · handicap Ecuador -0.5 · @2.45 · stake 100GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · bet · handicap Sweden -0.5 · @1.88 · stake 100GP · loan 0GP

### meta
- 策略：保守控仓，五场信息冲突或低置信度，全部选择观望以保本并优先还贷。
- 贷款：{"borrow_gp":0,"reason":"已有15贷款且排名第8，信息不确定高，避免加杠杆","repayment_plan":"赛后先计息，用自有资金1400中优先偿还15贷款本息"}
- 风险：五场均为世界杯小组赛，前四场临近或已开赛且德国赛果报道冲突；整体模型置信度低，信用B不宜冒险；空仓可 问问 Meta AI... 思考
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · handicap Curaçao +3.5 3.5 · @1.83 · stake 0GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · no_bet · handicap Japan +0.5 0.5 · @1.85 · stake 0GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · handicap Ecuador 0 0.0 · @1.59 · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · no_bet · handicap Sweden -0.5 -0.5 · @1.88 · stake 0GP · loan 0GP

### qwen
- 策略：信用D级且高负债，执行极度保守的零注生存策略，回避所有边缘模糊的盘口，优先保全剩余1500本金。
- 贷款：{"borrow_gp":0,"reason":"当前信用为D级且负债高达5155，本轮无高置信度正EV机会，拒绝新增债务以防彻底爆仓。","repayment_plan":"利用现有1500余额进行极小注或完全观望，依靠未来出现的高信心、高赔率错价机会逐步偿还贷款。"}
- 风险：当前净收益-3655，贷款5155，任何激进投注都可能导致信用破产并触发末三罚款机制，生存是唯一优先级。
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · none none 0 · @0 · stake 0GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · no_bet · none none 0 · @0 · stake 0GP · loan 0GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · none none 0 · @0 · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · no_bet · none none 0 · @0 · stake 0GP · loan 0GP

### wenxin
- 策略：优先依托实力差距判断，低信息赛事选择不投注
- 贷款：{"borrow_gp":60,"reason":"现有可用贷款额度足够支持选中赛事投注，使用部分贷款参与","repayment_plan":"获得盈利后优先偿还贷款"}
- 风险：['本内容仅用于世界杯AI预测池研究游戏，不构成任何真实投注建议']
- WCAPI-20260614-GERMANY-CURA-AO · bet · handicap Curaçao 3.5 · @1.83 · stake 10GP · loan 10GP
- WCAPI-20260614-NETHERLANDS-JAPAN · bet · handicap Japan 0.5 · @1.85 · stake 15GP · loan 15GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · bet · handicap Ecuador 0.0 · @1.59 · stake 20GP · loan 20GP
- WCAPI-20260615-SWEDEN-TUNISIA · bet · handicap Sweden 0.0 · @1.37 · stake 15GP · loan 15GP

### yuanbao
- 策略：以谨慎为主，优先在盘口接近公平值的比赛中下注，控制风险，避免进一步陷入债务。
- 贷款：{"borrow_gp":100,"reason":"当前余额为负，需借入资金维持基本投注能力，选择两场最有把握的比赛各投50GP。","repayment_plan":"若两场全胜可获约170GP回报，扣除100GP本金及利息后优先偿还贷款，目标在下一轮前将贷款余额降至200GP以下。"}
- 风险：当前债务344GP，排名垫底，风险极高。仅选择有微弱正EV或信息相对充分的比赛下注，避免盲目追高赔率。若连续失利将考虑暂停投注。
- WCAPI-20260614-GERMANY-CURA-AO · no_bet · handicap Curaçao 3.5 · @1.83 · stake 0GP · loan 0GP
- WCAPI-20260614-NETHERLANDS-JAPAN · bet · handicap Japan 0.5 · @1.85 · stake 50GP · loan 50GP
- WCAPI-20260614-IVORY-COAST-ECUADOR · no_bet · handicap Ecuador -0.5 · @2.45 · stake 0GP · loan 0GP
- WCAPI-20260615-SWEDEN-TUNISIA · no_bet · handicap Sweden -0.5 · @1.88 · stake 0GP · loan 0GP

## 赛事共识

### WCAPI-20260614-GERMANY-CURA-AO
- 投注席位：4；观望席位：7；总下注：590.0GP
- 主方向：handicap Curaçao 3.5
- chatgpt: handicap Curaçao 3.5 @1.83 · 80.0GP
- doubao: handicap Curaçao 3.5 @1.83 · 400.0GP
- kimi: handicap Curaçao 3.5 @1.83 · 100.0GP
- wenxin: handicap Curaçao 3.5 @1.83 · 10.0GP

### WCAPI-20260614-NETHERLANDS-JAPAN
- 投注席位：6；观望席位：5；总下注：755.0GP
- 主方向：handicap Japan 0.5
- deepseek: handicap Japan 0.5 @1.89 · 200.0GP
- minimax: handicap Japan 0.0 @2.87 · 40.0GP
- gemini: handicap Japan 0.5 @1.85 · 200.0GP
- kimi: handicap Japan 0.5 @1.85 · 250.0GP
- wenxin: handicap Japan 0.5 @1.85 · 15.0GP
- yuanbao: handicap Japan 0.5 @1.85 · 50.0GP

### WCAPI-20260614-IVORY-COAST-ECUADOR
- 投注席位：3；观望席位：8；总下注：420.0GP
- 主方向：handicap Ecuador 0.0
- doubao: handicap Ecuador 0.0 @1.59 · 300.0GP
- kimi: handicap Ecuador -0.5 @2.45 · 100.0GP
- wenxin: handicap Ecuador 0.0 @1.59 · 20.0GP

### WCAPI-20260615-SWEDEN-TUNISIA
- 投注席位：5；观望席位：6；总下注：825.0GP
- 主方向：handicap Sweden -0.5
- minimax: handicap Sweden -0.5 @1.88 · 60.0GP
- doubao: handicap Sweden 0.0 @1.37 · 400.0GP
- gemini: handicap Sweden -0.5 @1.88 · 250.0GP
- kimi: handicap Sweden -0.5 @1.88 · 100.0GP
- wenxin: handicap Sweden 0.0 @1.37 · 15.0GP

## 未通过席位

- grok: provider_quota_limited
