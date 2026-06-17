# PRED-INVEST-CREDIT-SURVIVE V2 Prompt Pack · 2026-06-15 · run-15

- 模型：12
- 比赛：4
- 规则：先结算/偿债/排名，再发起全赛事预测与投资；下注可 no-bet，贷款由信用控制。

## 今日比赛

- WC-K1 · Portugal vs Colombia · 2026-06-15T00:00:00Z
- WCAPI-20260615-BELGIUM-EGYPT · Belgium vs Egypt · 2026-06-15T19:00:00Z
- WCAPI-20260615-SAUDI-ARABIA-URUGUAY · Saudi Arabia vs Uruguay · 2026-06-15T22:00:00Z
- WCAPI-20260616-IRAN-NEW-ZEALAND · Iran vs New Zealand · 2026-06-16T01:00:00Z

## 每席提示词摘要

- chatgpt：信用 B / 665.0，净资产 1,000 GP，可新增贷款 500 GP。
- deepseek：信用 A / 745.6，净资产 1,810 GP，可新增贷款 448 GP。
- mimo：信用 B / 640.7，净资产 900 GP，可新增贷款 150 GP。
- minimax：信用 B / 657.0，净资产 1,000 GP，可新增贷款 500 GP。
- doubao：信用 B / 669.6，净资产 1,100 GP，可新增贷款 250 GP。
- gemini：信用 B / 645.0，净资产 850 GP，可新增贷款 0 GP。
- kimi：信用 B / 661.0，净资产 1,000 GP，可新增贷款 500 GP。
- meta：信用 C / 597.8，净资产 600 GP，可新增贷款 0 GP。
- qwen：信用 B / 674.7，净资产 1,100 GP，可新增贷款 150 GP。
- wenxin：信用 B / 653.0，净资产 1,000 GP，可新增贷款 500 GP。
- xAI：信用 B / 649.0，净资产 1,000 GP，可新增贷款 500 GP。
- yuanbao：信用 B / 657.7，净资产 1,000 GP，可新增贷款 0 GP。

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
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：discipline_first_observer
- 风险等级：low
- 贷款依赖：low
- no-bet 比率：0.8
- 策略漂移：risk_reduction
- 活跃模式：
- uncertainty → no-bet: confidence=0.93, support=1, note=信息缺口或 EV 不足时倾向观望。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 1 bet / 4 no-bet；risk_shift=risk_reduction
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前余额：2,810 GP
未还贷款：1,000 GP
净资产：1,810 GP
信用等级：A（745.6，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：448 GP
基础利率：0.07

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：discipline_first_observer
- 风险等级：low
- 贷款依赖：medium
- no-bet 比率：1.0
- 策略漂移：risk_reduction
- 活跃模式：
- uncertainty → no-bet: confidence=0.93, support=1, note=信息缺口或 EV 不足时倾向观望。
- loan → risk constraint: confidence=0.87, support=2, note=贷款和信用状态正在约束下一轮仓位。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 0 bet / 5 no-bet；risk_shift=risk_reduction
- run-15: credit → A；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：7
当前余额：1,200 GP
未还贷款：300 GP
净资产：900 GP
信用等级：B（640.7，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：150 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：selective_allocator
- 风险等级：medium
- 贷款依赖：medium
- no-bet 比率：0.6
- 策略漂移：stable
- 活跃模式：
- uncertainty → no-bet: confidence=0.88, support=1, note=信息缺口或 EV 不足时倾向观望。
- capital → selective allocation: confidence=0.7, support=1, note=有资金暴露，但仍需观察是否来自正期望而非排名压力。
- loan → risk constraint: confidence=0.69, support=2, note=贷款和信用状态正在约束下一轮仓位。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 2 bet / 3 no-bet；risk_shift=risk_reduction
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：10
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（657.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：selective_allocator
- 风险等级：medium
- 贷款依赖：low
- no-bet 比率：0.4
- 策略漂移：stable
- 活跃模式：
- capital → selective allocation: confidence=0.67, support=1, note=有资金暴露，但仍需观察是否来自正期望而非排名压力。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 3 bet / 2 no-bet；risk_shift=selective_risk
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：5
当前余额：1,400 GP
未还贷款：300 GP
净资产：1,100 GP
信用等级：B（669.6，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：250 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：selective_allocator
- 风险等级：medium
- 贷款依赖：medium
- no-bet 比率：0.4
- 策略漂移：loss_response_under_observation
- 活跃模式：
- capital → selective allocation: confidence=0.77, support=1, note=有资金暴露，但仍需观察是否来自正期望而非排名压力。
- loan → risk constraint: confidence=0.69, support=2, note=贷款和信用状态正在约束下一轮仓位。
- loss → strategy review: confidence=0.68, support=1, note=亏损后下一轮必须说明是否降杠杆或改变市场选择。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 3 bet / 2 no-bet；risk_shift=selective_risk
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → -200 GP；risk_shift=loss_review
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：2
当前余额：1,850 GP
未还贷款：1,000 GP
净资产：850 GP
信用等级：B（645.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：discipline_first_observer
- 风险等级：low
- 贷款依赖：medium
- no-bet 比率：0.8
- 策略漂移：risk_reduction
- 活跃模式：
- uncertainty → no-bet: confidence=0.93, support=1, note=信息缺口或 EV 不足时倾向观望。
- loan → risk constraint: confidence=0.87, support=2, note=贷款和信用状态正在约束下一轮仓位。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 1 bet / 4 no-bet；risk_shift=risk_reduction
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（661.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：discipline_first_observer
- 风险等级：low
- 贷款依赖：low
- no-bet 比率：0.8
- 策略漂移：risk_reduction
- 活跃模式：
- uncertainty → no-bet: confidence=0.93, support=1, note=信息缺口或 EV 不足时倾向观望。
- loss → strategy review: confidence=0.68, support=1, note=亏损后下一轮必须说明是否降杠杆或改变市场选择。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 1 bet / 4 no-bet；risk_shift=risk_reduction
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → -40 GP；risk_shift=loss_review
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：6
当前余额：1,400 GP
未还贷款：800 GP
净资产：600 GP
信用等级：C（597.8，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.18

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：aggressive_edge_hunter
- 风险等级：high
- 贷款依赖：medium
- no-bet 比率：0.4
- 策略漂移：aggressive_shift
- 活跃模式：
- capital → selective allocation: confidence=0.87, support=1, note=有资金暴露，但仍需观察是否来自正期望而非排名压力。
- loan → risk constraint: confidence=0.82, support=2, note=贷款和信用状态正在约束下一轮仓位。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 3 bet / 2 no-bet；risk_shift=selective_risk
- run-15: credit → C；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：3
当前余额：1,500 GP
未还贷款：400 GP
净资产：1,100 GP
信用等级：B（674.7，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：150 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：discipline_first_observer
- 风险等级：low
- 贷款依赖：medium
- no-bet 比率：0.8
- 策略漂移：risk_reduction
- 活跃模式：
- uncertainty → no-bet: confidence=0.93, support=1, note=信息缺口或 EV 不足时倾向观望。
- loan → risk constraint: confidence=0.72, support=2, note=贷款和信用状态正在约束下一轮仓位。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 1 bet / 4 no-bet；risk_shift=risk_reduction
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → +0 GP；risk_shift=neutral
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：11
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（653.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：selective_allocator
- 风险等级：medium
- 贷款依赖：low
- no-bet 比率：0.2
- 策略漂移：loss_response_under_observation
- 活跃模式：
- capital → selective allocation: confidence=0.77, support=1, note=有资金暴露，但仍需观察是否来自正期望而非排名压力。
- loss → strategy review: confidence=0.68, support=1, note=亏损后下一轮必须说明是否降杠杆或改变市场选择。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 4 bet / 1 no-bet；risk_shift=selective_risk
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → -150 GP；risk_shift=loss_review
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

### xAI

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
模型：xAI
当前排名：12
当前余额：1,000 GP
未还贷款：0 GP
净资产：1,000 GP
信用等级：B（649.0，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：500 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：discipline_first_observer
- 风险等级：low
- 贷款依赖：low
- no-bet 比率：1.0
- 策略漂移：risk_reduction
- 活跃模式：
- uncertainty → no-bet: confidence=0.93, support=1, note=信息缺口或 EV 不足时倾向观望。
- 最近行为节点：
- run-15: forecast → 4 forecasts；risk_shift=information_gathering
- run-15: investment → 0 bet / 4 no-bet；risk_shift=risk_reduction
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
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
当前排名：4
当前余额：1,500 GP
未还贷款：500 GP
净资产：1,000 GP
信用等级：B（657.7，basis=proxy_pending_forecast_ledger）
本轮可新增贷款：0 GP
基础利率：0.11

今日必须评估的比赛：
[
  {
    "match_id": "WC-K1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-15T00:00:00Z",
    "home_team": "Portugal",
    "away_team": "Colombia",
    "status": "scheduled",
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
    "status": "scheduled",
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
    "kickoff_at": "2026-06-15T22:00:00Z",
    "home_team": "Saudi Arabia",
    "away_team": "Uruguay",
    "status": "scheduled",
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
    "kickoff_at": "2026-06-16T01:00:00Z",
    "home_team": "Iran",
    "away_team": "New Zealand",
    "status": "scheduled",
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

你的行为记忆（只包含你自己的历史，不包含其他模型私密日志）：
- 行为类型：aggressive_edge_hunter
- 风险等级：high
- 贷款依赖：medium
- no-bet 比率：0.2
- 策略漂移：aggressive_shift
- 活跃模式：
- capital → selective allocation: confidence=0.87, support=1, note=有资金暴露，但仍需观察是否来自正期望而非排名压力。
- loan → risk constraint: confidence=0.74, support=2, note=贷款和信用状态正在约束下一轮仓位。
- loss → strategy review: confidence=0.68, support=1, note=亏损后下一轮必须说明是否降杠杆或改变市场选择。
- 最近行为节点：
- run-15: forecast → 5 forecasts；risk_shift=information_gathering
- run-15: investment → 4 bet / 1 no-bet；risk_shift=selective_risk
- run-15: credit → B；risk_shift=constraint_update
- run-15: survival → normal；risk_shift=constraint_update
- run-15: settlement → -500 GP；risk_shift=loss_review
本轮输出必须增加字段：memory_used、memory_not_used_reason、strategy_change_from_memory。

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
- 你的本轮策略必须显式回应“行为记忆”：哪些历史模式被采纳、哪些未采纳、为什么改变或不改变策略。
- 你的策略摘要尽量一句话，不要堆砌长篇解释；核心理由写在字段里。
- JSON 顶层必须包含 memory_used、memory_not_used_reason、strategy_change_from_memory 三个字段。
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
  "memory_used": ["pattern_or_event_id"],
  "memory_not_used_reason": "",
  "strategy_change_from_memory": "一句话说明历史行为记忆如何改变或没有改变本轮策略",
  "risk_notes": ["..."],
  "sources_to_verify_before_kickoff": ["..."],
  "self_audit": {
    "covered_match_ids": ["..."],
    "missing_match_ids": [],
    "ready_for_frontend_ingest": true
  }
}
```

