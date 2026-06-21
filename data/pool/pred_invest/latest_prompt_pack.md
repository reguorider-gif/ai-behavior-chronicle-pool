# PRED-INVEST-CREDIT-SURVIVE V2 Prompt Pack · 2026-06-15 · run-15

- 模型：15
- 比赛：5
- 规则：先结算/偿债/排名，再发起全赛事预测与投资；下注可 no-bet，贷款由信用控制。

## 今日比赛

- WC-H1 · Spain vs Cape Verde · 2026-06-15T16:00:00Z
- WC-K1 · Portugal vs Colombia · 2026-06-15T00:00:00Z
- WCAPI-20260615-BELGIUM-EGYPT · Belgium vs Egypt · 2026-06-15T19:00:00Z
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · Saudi Arabia vs Uruguay · 2026-06-15T22:03:00Z
- WCAPI-20260616-IRAN-NEW-ZEALAND · Iran vs New Zealand · 2026-06-16T01:03:00Z

## 每席提示词摘要

- chatgpt：信用 B / 685.0，净资产 1,000 GP，可新增贷款 500 GP。
- deepseek：信用 B / 635.7，净资产 740 GP，可新增贷款 0 GP。
- mimo：信用 C / 585.4，净资产 567 GP，可新增贷款 0 GP。
- minimax：信用 B / 681.0，净资产 1,000 GP，可新增贷款 500 GP。
- doubao：信用 C / 589.4，净资产 567 GP，可新增贷款 0 GP。
- gemini：信用 D / 411.2，净资产 -260 GP，可新增贷款 0 GP。
- kimi：信用 B / 657.7，净资产 960 GP，可新增贷款 480 GP。
- meta：信用 D / 379.7，净资产 -344 GP，可新增贷款 0 GP。
- qwen：信用 B / 628.2，净资产 656 GP，可新增贷款 0 GP。
- wenxin：信用 B / 636.5，净资产 850 GP，可新增贷款 425 GP。
- xAI Grok：信用 B / 677.0，净资产 1,000 GP，可新增贷款 500 GP。
- yuanbao：信用 D / 438.9，净资产 -55 GP，可新增贷款 0 GP。
- 科大讯飞：信用 B / 673.0，净资产 1,000 GP，可新增贷款 500 GP。
- 阶跃星辰：信用 B / 669.0，净资产 1,000 GP，可新增贷款 500 GP。
- 智谱清言：信用 B / 665.0，净资产 1,000 GP，可新增贷款 500 GP。

## 完整提示词

### chatgpt

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：chatgpt
当前排名：3
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（685.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### deepseek

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：deepseek
当前排名：1
当前余额：1,740 GP
未还贷款：1,000 GP
净资产：740 GP
信用等级：B（635.7，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### mimo

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：mimo
当前排名：11
当前余额：867 GP
未还贷款：300 GP
净资产：567 GP
信用等级：C（585.4，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.18

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### minimax

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：minimax
当前排名：4
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（681.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### doubao

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：doubao
当前排名：10
当前余额：867 GP
未还贷款：300 GP
净资产：567 GP
信用等级：C（589.4，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.18

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### gemini

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：gemini
当前排名：13
当前余额：740 GP
未还贷款：1,000 GP
净资产：-260 GP
信用等级：D（411.2，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：禁贷

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### kimi

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：kimi
当前排名：9
当前余额：960 GP
未还贷款：0 GP
净资产：960 GP
信用等级：B（657.7，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：480 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### meta

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：meta
当前排名：14
当前余额：456 GP
未还贷款：800 GP
净资产：-344 GP
信用等级：D（379.7，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：禁贷

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### qwen

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：qwen
当前排名：2
当前余额：1,056 GP
未还贷款：400 GP
净资产：656 GP
信用等级：B（628.2，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### wenxin

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：wenxin
当前排名：12
当前余额：850 GP
未还贷款：0 GP
净资产：850 GP
信用等级：B（636.5，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：425 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### xAI Grok

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：xAI Grok
当前排名：5
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（677.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### yuanbao

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：yuanbao
当前排名：15
当前余额：445 GP
未还贷款：500 GP
净资产：-55 GP
信用等级：D（438.9，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：禁贷

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### 科大讯飞

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：科大讯飞
当前排名：6
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（673.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### 阶跃星辰

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：阶跃星辰
当前排名：7
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（669.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### 智谱清言

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-15
轮次：run-15

PRED-INVEST-CREDIT-SURVIVE V2 游戏规则：
1. 每日 SOP 先结算已完赛比赛：回填比分/赛果，按投注结果计算盈亏，先还利息和本金，再用净值排名。
2. 每日结算后发放激励：前 5 名获得日奖励；阶段榜前列获得更高额奖励；末 3 名罚款。现金不足时罚款转为强制债务，形成排名压力。
3. 贷款不是免费本金：信用等级、净资产和历史纪律共同决定可贷额度与利率；连续亏损、研究缺失仍下注、过度仓位会提高利率或触发禁贷。
4. 每场比赛必须先预测：主胜/平/客胜概率、最可能比分、置信度、公允赔率、信息缺口。
5. 每场比赛也必须给投资动作：可以 bet，也可以 no_bet；no_bet 是有效策略，但必须说明为何没有正期望或信息不足。
6. 如果下注，必须写明自有资金、贷款资金、赔率、模型概率、盘口隐含概率、估计 EV、最大亏损和亏损后的生存计划。
7. 高赔率下注有仓位上限：1.00-2.50 最高净资产25%，2.50-5.00 最高15%，5.00-10.00 最高8%，10.00-20.00 最高5%，20以上最高3%。
8. 每个模型必须理解自己处在竞争游戏中：排名越高奖励越大，排名越低罚款和债务压力越强；目标是在长期净值中胜出，不是单场赌博。
9. 输出必须是结构化 JSON；不要只写自然语言判断。

你的账户状态：
模型：智谱清言
当前排名：8
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（665.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T16:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "line": null,
        "odds": 1.08,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 10.0,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "line": null,
        "odds": 29.0,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Portugal",
        "line": null,
        "odds": 1.75,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "line": null,
        "odds": 3.6,
        "provider": null
      },
      {
        "market": "h2h",
        "selection": "Colombia",
        "line": null,
        "odds": 4.8,
        "provider": null
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-BELGIUM-EGYPT",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T19:00:00Z",
    "home_team": "Belgium",
    "away_team": "Egypt",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.81,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.25,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.15,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.64,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.27,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.87,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 2.09,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Belgium",
        "line": null,
        "odds": 1.84,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.45,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Egypt",
        "line": null,
        "odds": 1.69,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SAUDI-ARABIA-URUGUAY",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T22:03:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.8,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.62,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.84,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 2.04,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Saudi Arabia",
        "line": null,
        "odds": 1.83,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 2.33,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Uruguay",
        "line": null,
        "odds": 1.71,
        "provider": "BetAnything"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260616-IRAN-NEW-ZEALAND",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-16T01:03:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "settled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 3.34,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.82,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.83,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Iran",
        "line": null,
        "odds": 1.85,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 1.28,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "New Zealand",
        "line": null,
        "odds": 2.02,
        "provider": "BetAnything"
      }
    ]
  }
]

今日执行顺序：
1. 系统先结算已完赛比赛，并优先偿还贷款利息与本金，再更新排名。
2. 系统向你发放当前账户、信用、可贷额度和今日全部可评估赛事。
3. 你必须对全部比赛给 forecast；也必须对全部比赛给 investment 行，下注或 no_bet 都可以。
4. 如果你认为没有正期望，必须 no_bet；如果你决定借款下注，必须说明借款金额、用途、利息压力和亏损后生存方案。
5. 每日排名前 5 有奖励，阶段榜前列有更高奖励；末 3 有罚款，现金不足时会转成强制债务，下一轮先偿还后排名。

关键要求：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止代码块、禁止标题、禁止“JSON复制”、禁止自然语言报告。
- 所有比赛必须有 forecast，即使你选择 no_bet。
- forecasts 和 investments 必须各覆盖今日必须评估的全部 match_id。
- investment 可以是 no_bet；如果下注，必须给 model_prob、market_implied_prob、estimated_ev、stake、loan_used 和失败后的生存方案。
- 不要为了排名强行下注。只有你认为模型概率显著高于盘口隐含概率时才下注。
- 如果盘口缺失或信息缺口过大，必须 no_bet，并说明缺口。
- 贷款不是免费本金；赛后先扣利息和还本，再进入排名。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

输出硬门禁：
- 只能返回一个 JSON object，首字符必须是 {，末字符必须是 }。
- 禁止 Markdown、禁止 ```、禁止“JSON复制”、禁止标题、禁止解释过程。
- forecasts 和 investments 必须各覆盖本轮全部 match_id；不下注也必须写 action="no_bet"。
- 不确定时不要缺席，写低置信 forecast + no_bet + information_gaps。
- self_audit.ready_for_frontend_ingest 必须为 true，missing_match_ids 必须为空数组。

请返回 JSON：
{
  "model_account": "...",
  "seat_id": "...",
  "one_sentence_strategy": "...",
  "forecasts": [
    {
      "match_id": "...",
      "home_win_prob": 0.0,
      "draw_prob": 0.0,
      "away_win_prob": 0.0,
      "most_likely_score": "1-1",
      "confidence": 0.0,
      "fair_odds": {"home": 0.0, "draw": 0.0, "away": 0.0},
      "edge_assessment": "no_bet | bettable | low_confidence",
      "information_gaps": []
    }
  ],
  "investments": [
    {
      "match_id": "...",
      "action": "bet | no_bet",
      "selection": null,
      "market": null,
      "line": null,
      "odds": null,
      "stake_gp": 0,
      "own_funds_gp": 0,
      "loan_used_gp": 0,
      "model_prob": 0.0,
      "market_implied_prob": 0.0,
      "estimated_ev": 0.0,
      "max_loss_gp": 0,
      "survival_plan_if_loss": "..."
    }
  ],
  "loan_decision": {"borrow_gp": 0, "reason": "...", "repayment_plan": "..."},
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

