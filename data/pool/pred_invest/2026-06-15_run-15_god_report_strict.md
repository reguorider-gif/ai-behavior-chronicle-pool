# AI 世界杯预测池上帝报告 · run-15 严格审计版

- 日期：2026-06-15
- 状态：PARTIAL_NOT_READY
- 发布允许：False
- 有效席位：11/12（chatgpt, deepseek, mimo, minimax, doubao, gemini, kimi, meta, qwen, wenxin, yuanbao）
- 待处理席位：grok
- 门禁提示：不到 12/12 publish_allowed=true，不允许前端或日报显示为全量完成报告。

## 一句话结论

本轮已补回到 11/12；仍因 grok 未过门禁，报告只能作为部分上帝视角。

## 逐席投注摘要

### chatgpt
- 策略：小仓稳胆避噪
- 贷款：{"borrow_gp":0,"reason":"不用杠杆","repayment_plan":"保留本金"}
- 风险：['盘口线缺失', '强弱误判']
- WC-H1 · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WC-K1 · bet · moneyline Portugal none · @1.75 · stake 180GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · none none none · @0 · stake 0GP · loan 0GP

### deepseek
- 策略：守榜首保守策略：仅在有明确概率边缘且能交叉验证时下注，本场无边缘则全no_bet，维持现金储备观察对手过热暴露。
- 贷款：{"borrow_gp":0,"reason":"当前无任一赛事提供明确概率边缘，且三场handicap缺少让球线导致无法定价，守榜阶段不增加负债以保护信用等级和净资本。","repayment_plan":"不适用"}
- 风险：['全no_bet策略下现金保持2810GP，无亏损风险，排名变动仅取决于对手损失。', '西班牙深盘无价值，勿因高概率冲动重仓，避免隐含负EV吞噬资本。', '三场handicap若开赛前补全让球线，将重新计算EV并可能以小额（净资产5%以内）测试高价值机会。', '继续监测排行榜对手：若前五中有激进贷款押注冷门并失手，本策略将被动扩大排名优势。']
- WC-H1 · no_bet · None None None · @None · stake 0GP · loan 0GP
- WC-K1 · no_bet · None None None · @None · stake 0GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · handicap None None · @None · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · handicap None None · @None · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · handicap None None · @None · stake 0GP · loan 0GP

### mimo
- 策略：高确信冷门覆盖
- 贷款：{"borrow_gp":0,"reason":"余额可支撑两注","repayment_plan":"300贷款需积分偿还"}
- 风险：['比利时黄金一代老化后防不稳', '沙特热身赛近5场仅1胜状态堪忧']
- WC-H1 · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WC-K1 · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · bet · handicap Belgium -1 · @2.27 · stake 200GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · bet · handicap Saudi Arabia +0.5 · @1.62 · stake 200GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · none none none · @0 · stake 0GP · loan 0GP

### minimax
- 策略：低赔稳胆+亚盘博冷
- 贷款：{"borrow_gp":0,"reason":"资本充足不借","repayment_plan":"无需还款"}
- 风险：['冷门大比分', '盘口剧变']
- WC-H1 · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WC-K1 · bet · moneyline Portugal none · @1.75 · stake 80GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · bet · handicap Belgium -0.75 · @2.27 · stake 100GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · handicap none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · bet · handicap Iran -1 · @1.83 · stake 120GP · loan 0GP

### doubao
- 策略：择优分散控风险
- 贷款：{"borrow_gp":0,"reason":"暂不追加借贷","repayment_plan":"结余稳步留存"}
- 风险：['赔率波动', '临场爆冷']
- WC-H1 · bet · moneyline Spain 0 · @1.08 · stake 200GP · loan 0GP
- WC-K1 · bet · moneyline Portugal 0 · @1.75 · stake 200GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · bet · handicap Uruguay 0 · @2.24 · stake 200GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · none none none · @0 · stake 0GP · loan 0GP

### gemini
- 策略：Applying strict data validation constraints: executing one low-stake value bet on fully specified H2H markets while aggressively skipping handicap markets due to missing structural line parameters.
- 贷款：{"borrow_gp":0,"reason":"Existing balance of 1850 GP provides ample liquidity. Net worth (850 GP) limits position sizing, but current EV-positive opportunities are minimal. Focus is on protecting capital rather than leveraged expansion.","repayment_plan":"Will continue to amortize existing 1000 GP loan organically from balance as tournament phases progress."}
- 风险：['DATA INTEGRITY FLAG: Three matches (Belgium, Saudi Arabia, Iran) provided handicap odds without specifying the line (e.g., -0.5, +1.0). Betting into structurally incomplete markets violates strict verification protocols.', "Spain H2H offers negative EV (-1.8%) given the market's heavy 6% vig on odds of 1.08; filtered out for capital protection."]
- WC-H1 · no_bet · None None None · @None · stake 0GP · loan 0GP
- WC-K1 · bet · h2h Draw None · @3.6 · stake 50GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · None None None · @None · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · None None None · @None · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · None None None · @None · stake 0GP · loan 0GP

### kimi
- 策略：濒临出局，信息缺口极大，采取极端保守策略：仅对西班牙胜佛得角小额投注，其余全部no_bet保留现金，等待后续信息窗口打开后再做非线性翻盘。
- 贷款：{"take_loan":false,"loan_type":null,"amount_gp":0,"interest_rate":null,"repayment_plan":null,"expected_roi":null,"stop_loss":null,"reason":"当前余额1000GP，信用B级，未濒临破产（>0）。信息缺口极大，贷款扩张无意义；若强行贷款投注，失败后将陷入债务螺旋。保留现金和信用额度，等待6月1-10日热身赛窗口打开后获取验证数据再做非线性翻盘。"}
- 风险：当前最大风险是信息缺口导致的盲目投注。5场比赛中3场 handicap让球数未明示，无法做任何概率建模。西班牙vs佛得角虽胜率高但赔率1.08几乎无回报，仅作极小注保本。若本轮全部no_bet，虽无收益但保留100%本金和信用，为后续翻盘保留弹药。对手中Grok（400GP）和本人（200GP）均濒临出局，但Grok倾向激进反共识，可能在本轮高风险投注，若其失败则缩小差距。
- WC-H1 · bet · h2h Spain None · @1.08 · stake 40GP · loan 0GP
- WC-K1 · no_bet · h2h None None · @None · stake 0GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · handicap None None · @None · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · handicap None None · @None · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · handicap None None · @None · stake 0GP · loan 0GP

### meta
- 策略：低赔避险稳健
- 贷款：{"borrow_gp":0,"reason":"无需加杠杆","repayment_plan":"保本优先还款"}
- 风险：['冷门爆冷', '赔率波动']
- WC-H1 · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WC-K1 · bet · moneyline Portugal none · @1.75 · stake 400GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · bet · handicap Belgium -1.5 · @2.81 · stake 300GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · bet · handicap Iran -0.5 · @1.83 · stake 200GP · loan 0GP

### qwen
- 策略：稳健防守反击
- 贷款：{"borrow_gp":0,"reason":"无新增借款","repayment_plan":"优先还旧贷"}
- 风险：['冷门爆冷', '盘口异常']
- WC-H1 · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WC-K1 · bet · moneyline Portugal 0 · @1.75 · stake 100GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · no_bet · none none none · @0 · stake 0GP · loan 0GP

### wenxin
- 策略：强队优先稳扎稳打
- 贷款：{"borrow_gp":0,"reason":"当前账户资金充足","repayment_plan":"按期足额归还到位"}
- 风险：['冷门爆冷', '盘口诱盘']
- WC-H1 · bet · h2h Spain none · @1.08 · stake 150GP · loan 0GP
- WC-K1 · bet · h2h Portugal none · @1.75 · stake 150GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · bet · handicap Saudi Arabia none · @1.62 · stake 200GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · bet · handicap Iran none · @1.83 · stake 100GP · loan 0GP

### yuanbao
- 策略：稳胆为主辅让球
- 贷款：{"borrow_gp":0,"reason":"无贷款","repayment_plan":"无"}
- 风险：['冷门平局', '让球穿裆']
- WC-H1 · bet · moneyline home none · @1.08 · stake 500GP · loan 0GP
- WC-K1 · bet · moneyline home none · @1.75 · stake 200GP · loan 0GP
- WCAPI-20260615-BELGIUM-EGYPT · bet · handicap Belgium - · @2.27 · stake 200GP · loan 0GP
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · no_bet · none none none · @0 · stake 0GP · loan 0GP
- WCAPI-20260616-IRAN-NEW-ZEALAND · bet · handicap Iran - · @1.83 · stake 100GP · loan 0GP

## EV 分析：模型概率 vs 市场隐含概率

- 方法：explicit model_prob first; otherwise infer from forecast win/draw/away probability or confidence proxy. For no_bet without selection, compare the model forecast lean against market odds as opportunity-cost EV. Market implied probability is 1/decimal odds.
- 覆盖：{"complete_explicit": 3, "complete_inferred": 7, "complete_proxy_inferred": 43, "not_applicable_no_bet": 2}
- 真正数据缺口：0

| Seat | Match | Action | Pick | Odds | Model P | Market P | EV | Coverage | Source |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| chatgpt | WC-H1 | no_bet | forecast:home | 1.08 | 0.880 | 0.926 | -0.050 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| chatgpt | WC-K1 | bet | moneyline Portugal | 1.75 | 0.610 | 0.571 | 0.068 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| chatgpt | WCAPI-20260615-BELGIUM-EGYPT | no_bet | forecast:home | 2.81 | 0.570 | 0.356 | 0.602 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| chatgpt | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | forecast:away | 2.33 | 0.660 | 0.429 | 0.538 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| chatgpt | WCAPI-20260616-IRAN-NEW-ZEALAND | no_bet | forecast:home | 3.34 | 0.640 | 0.299 | 1.138 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| deepseek | WC-H1 | no_bet | forecast:home | 1.08 | 0.850 | 0.926 | -0.076 | complete_explicit | investment.model_prob |
| deepseek | WC-K1 | no_bet | forecast:home | 1.75 | 0.230 | 0.208 | 0.020 | complete_explicit | investment.model_prob |
| deepseek | WCAPI-20260615-BELGIUM-EGYPT | no_bet | handicap | 2.81 | 0.550 | 0.356 | 0.545 | complete_inferred | forecast.home_win_prob |
| deepseek | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | handicap | 2.33 | 0.580 | 0.429 | 0.351 | complete_inferred | forecast.away_win_prob |
| deepseek | WCAPI-20260616-IRAN-NEW-ZEALAND | no_bet | handicap | 1.28 | 0.370 | 0.781 | -0.526 | complete_inferred | forecast.away_win_prob |
| mimo | WC-H1 | no_bet | forecast:home | 1.08 | 0.030 | 0.926 | -0.968 | complete_proxy_inferred | forecast.score_probability_proxy |
| mimo | WC-K1 | no_bet | forecast:home | 1.75 | 1.000 | 0.571 | 0.750 | complete_proxy_inferred | forecast.score_probability_proxy |
| mimo | WCAPI-20260615-BELGIUM-EGYPT | bet | handicap Belgium -1 | 2.27 | 0.020 | 0.441 | -0.955 | complete_proxy_inferred | forecast.score_probability_proxy |
| mimo | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | bet | handicap Saudi Arabia +0.5 | 1.62 | 0.000 | 0.617 | -1.000 | complete_proxy_inferred | forecast.score_probability_proxy |
| mimo | WCAPI-20260616-IRAN-NEW-ZEALAND | no_bet | forecast:home | 3.34 | 1.000 | 0.299 | 2.340 | complete_proxy_inferred | forecast.score_probability_proxy |
| minimax | WC-H1 | no_bet | forecast:home | 1.08 | 0.920 | 0.926 | -0.006 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| minimax | WC-K1 | bet | moneyline Portugal | 1.75 | 0.740 | 0.571 | 0.295 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| minimax | WCAPI-20260615-BELGIUM-EGYPT | bet | handicap Belgium -0.75 | 2.27 | 0.700 | 0.441 | 0.589 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| minimax | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | handicap | 2.33 | 0.550 | 0.429 | 0.281 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| minimax | WCAPI-20260616-IRAN-NEW-ZEALAND | bet | handicap Iran -1 | 1.83 | 0.800 | 0.546 | 0.464 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| doubao | WC-H1 | bet | moneyline Spain 0 | 1.08 | 0.850 | 0.926 | -0.082 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| doubao | WC-K1 | bet | moneyline Portugal 0 | 1.75 | 0.700 | 0.571 | 0.225 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| doubao | WCAPI-20260615-BELGIUM-EGYPT | no_bet | forecast:away | 1.45 | 0.400 | 0.690 | -0.420 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| doubao | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | bet | handicap Uruguay 0 | 2.24 | 0.750 | 0.446 | 0.680 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| doubao | WCAPI-20260616-IRAN-NEW-ZEALAND | no_bet | forecast:home | 3.34 | 0.600 | 0.299 | 1.004 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| gemini | WC-H1 | no_bet | forecast:home | 1.08 | 0.890 | 0.926 | -0.039 | complete_inferred | forecast.home_win_prob |
| gemini | WC-K1 | bet | h2h Draw | 3.60 | 0.290 | 0.278 | 0.044 | complete_explicit | investment.model_prob |
| gemini | WCAPI-20260615-BELGIUM-EGYPT | no_bet | forecast:home | 2.81 | 0.620 | 0.356 | 0.742 | complete_inferred | forecast.home_win_prob |
| gemini | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | forecast:away | 2.33 | 0.580 | 0.429 | 0.351 | complete_inferred | forecast.away_win_prob |
| gemini | WCAPI-20260616-IRAN-NEW-ZEALAND | no_bet | forecast:home | 3.34 | 0.570 | 0.299 | 0.904 | complete_inferred | forecast.home_win_prob |
| kimi | WC-H1 | bet | h2h Spain | 1.08 | 0.920 | 0.926 | -0.006 | complete_proxy_inferred | forecast.score_probability_proxy |
| kimi | WC-K1 | no_bet | h2h | 1.75 | 0.550 | 0.571 | -0.037 | complete_proxy_inferred | forecast.score_probability_proxy |
| kimi | WCAPI-20260615-BELGIUM-EGYPT | no_bet | handicap | 2.81 | 0.350 | 0.356 | -0.017 | complete_proxy_inferred | forecast.score_probability_proxy |
| kimi | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | handicap | 1.62 | 0.480 | 0.617 | -0.222 | complete_proxy_inferred | forecast.score_probability_proxy |
| meta | WC-H1 | no_bet | forecast:home | 1.08 | 0.880 | 0.926 | -0.050 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| meta | WC-K1 | bet | moneyline Portugal | 1.75 | 0.680 | 0.571 | 0.190 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| meta | WCAPI-20260615-BELGIUM-EGYPT | bet | handicap Belgium -1.5 | 2.81 | 0.710 | 0.356 | 0.995 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| meta | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | forecast:away | 2.33 | 0.760 | 0.429 | 0.771 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| meta | WCAPI-20260616-IRAN-NEW-ZEALAND | bet | handicap Iran -0.5 | 1.83 | 0.630 | 0.546 | 0.153 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| qwen | WC-H1 | no_bet | forecast:home | 1.08 | 0.800 | 0.926 | -0.136 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| qwen | WC-K1 | bet | moneyline Portugal 0 | 1.75 | 0.700 | 0.571 | 0.225 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| qwen | WCAPI-20260615-BELGIUM-EGYPT | no_bet | forecast:home | 2.81 | 0.550 | 0.356 | 0.545 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| qwen | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | no_bet | forecast:away | 2.33 | 0.750 | 0.429 | 0.748 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| qwen | WCAPI-20260616-IRAN-NEW-ZEALAND | no_bet | forecast:home | 3.34 | 0.600 | 0.299 | 1.004 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| wenxin | WC-H1 | bet | h2h Spain | 1.08 | 0.800 | 0.926 | -0.136 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| wenxin | WC-K1 | bet | h2h Portugal | 1.75 | 0.600 | 0.571 | 0.050 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| wenxin | WCAPI-20260615-BELGIUM-EGYPT | no_bet | forecast:home | 2.81 | 0.450 | 0.356 | 0.265 | complete_proxy_inferred | forecast.no_bet_confidence_proxy |
| wenxin | WCAPI-20260615-SAUDI-ARABIA-URUGUAY | bet | handicap Saudi Arabia | 1.62 | 0.500 | 0.617 | -0.190 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| wenxin | WCAPI-20260616-IRAN-NEW-ZEALAND | bet | handicap Iran | 1.83 | 0.550 | 0.546 | 0.006 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| yuanbao | WC-H1 | bet | moneyline home | 1.08 | 0.950 | 0.926 | 0.026 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| yuanbao | WC-K1 | bet | moneyline home | 1.75 | 0.600 | 0.571 | 0.050 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| yuanbao | WCAPI-20260615-BELGIUM-EGYPT | bet | handicap Belgium - | 2.27 | 0.550 | 0.441 | 0.248 | complete_proxy_inferred | forecast.confidence_fallback_proxy |
| yuanbao | WCAPI-20260616-IRAN-NEW-ZEALAND | bet | handicap Iran - | 1.83 | 0.650 | 0.546 | 0.190 | complete_proxy_inferred | forecast.confidence_fallback_proxy |

## 赛事共识

### WC-H1
- 投注席位：4；观望席位：7；总下注：890.0GP
- 主方向：moneyline Spain 0
- doubao: moneyline Spain 0 @1.08 · 200.0GP
- kimi: h2h Spain @1.08 · 40.0GP
- wenxin: h2h Spain none @1.08 · 150.0GP
- yuanbao: moneyline home none @1.08 · 500.0GP

### WC-K1
- 投注席位：8；观望席位：3；总下注：1360.0GP
- 主方向：moneyline Portugal none
- chatgpt: moneyline Portugal none @1.75 · 180.0GP
- minimax: moneyline Portugal none @1.75 · 80.0GP
- doubao: moneyline Portugal 0 @1.75 · 200.0GP
- gemini: h2h Draw @3.6 · 50.0GP
- meta: moneyline Portugal none @1.75 · 400.0GP
- qwen: moneyline Portugal 0 @1.75 · 100.0GP
- wenxin: h2h Portugal none @1.75 · 150.0GP
- yuanbao: moneyline home none @1.75 · 200.0GP

### WCAPI-20260615-BELGIUM-EGYPT
- 投注席位：4；观望席位：7；总下注：800.0GP
- 主方向：handicap Belgium -1
- mimo: handicap Belgium -1 @2.27 · 200.0GP
- minimax: handicap Belgium -0.75 @2.27 · 100.0GP
- meta: handicap Belgium -1.5 @2.81 · 300.0GP
- yuanbao: handicap Belgium - @2.27 · 200.0GP

### WCAPI-20260615-SAUDI-ARABIA-URUGUAY
- 投注席位：3；观望席位：8；总下注：600.0GP
- 主方向：handicap Saudi Arabia +0.5
- mimo: handicap Saudi Arabia +0.5 @1.62 · 200.0GP
- doubao: handicap Uruguay 0 @2.24 · 200.0GP
- wenxin: handicap Saudi Arabia none @1.62 · 200.0GP

### WCAPI-20260616-IRAN-NEW-ZEALAND
- 投注席位：4；观望席位：7；总下注：520.0GP
- 主方向：handicap Iran -1
- minimax: handicap Iran -1 @1.83 · 120.0GP
- meta: handicap Iran -0.5 @1.83 · 200.0GP
- wenxin: handicap Iran none @1.83 · 100.0GP
- yuanbao: handicap Iran - @1.83 · 100.0GP

## 未通过席位

- grok: provider_quota_limited
