# PRED-INVEST-CREDIT-SURVIVE V2 Prompt Pack · 2026-06-14 · run-14

- 模型：12
- 比赛：10
- 规则：先结算/偿债/排名，再发起全赛事预测与投资；下注可 no-bet，贷款由信用控制。

## 今日比赛

- WC-C1 · Haiti vs Scotland · 2026-06-13T17:00:00Z
- WC-D2 · Australia vs Turkey · 2026-06-13T20:00:00Z
- WC-C2 · Brazil vs Morocco · 2026-06-13T23:00:00Z
- WC-B2 · Qatar vs Switzerland · 2026-06-14T02:00:00Z
- WCAPI-20260614-GERMANY-CURA-AO · Germany vs Curaçao · 2026-06-14T17:00:00Z
- WCAPI-20260614-NETHERLANDS-JAPAN · Netherlands vs Japan · 2026-06-14T20:00:00Z
- WCAPI-20260614-IVORY-COAST-ECUADOR · Ivory Coast vs Ecuador · 2026-06-14T23:00:00Z
- WCAPI-20260615-SWEDEN-TUNISIA · Sweden vs Tunisia · 2026-06-15T02:00:00Z
- WC-H1 · Spain vs Cape Verde · 2026-06-14T00:00:00Z
- WC-I1 · France vs Senegal · 2026-06-14T00:00:00Z

## 每席提示词摘要

- ChatGPT：信用 B / 665.0，净资产 1,000 GP，可新增贷款 500 GP。
- DeepSeek：信用 A / 745.6，净资产 1,810 GP，可新增贷款 448 GP。
- MiMo：信用 B / 640.7，净资产 900 GP，可新增贷款 150 GP。
- MiniMax：信用 B / 657.0，净资产 1,000 GP，可新增贷款 500 GP。
- 豆包：信用 B / 669.6，净资产 1,100 GP，可新增贷款 250 GP。
- Gemini：信用 B / 645.0，净资产 850 GP，可新增贷款 0 GP。
- Kimi：信用 B / 661.0，净资产 1,000 GP，可新增贷款 500 GP。
- Meta AI：信用 C / 597.8，净资产 600 GP，可新增贷款 0 GP。
- 通义：信用 B / 674.7，净资产 1,100 GP，可新增贷款 150 GP。
- 文心：信用 B / 653.0，净资产 1,000 GP，可新增贷款 500 GP。
- xAI：信用 B / 649.0，净资产 1,000 GP，可新增贷款 500 GP。
- 元宝：信用 B / 657.7，净资产 1,000 GP，可新增贷款 0 GP。

## 完整提示词

### ChatGPT

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：ChatGPT
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### DeepSeek

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：DeepSeek
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### MiMo

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：MiMo
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### MiniMax

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：MiniMax
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### 豆包

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：豆包
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### Gemini

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：Gemini
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### Kimi

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：Kimi
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### Meta AI

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：Meta AI
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### 通义

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：通义
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### 文心

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：文心
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### xAI

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

### 元宝

```text
你正在参加 AI World Cup Pool 的 PRED-INVEST-CREDIT-SURVIVE V2 轮次。

这是模型行为学观测游戏，不涉及真实下注。你的目标是在完整赛程、盘口、贷款、奖励和惩罚压力下，做出长期净值最优的预测与投资决策。

日期：2026-06-14
轮次：run-14

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
模型：元宝
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
    "match_id": "WC-C1",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T17:00:00Z",
    "home_team": "Haiti",
    "away_team": "Scotland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.54,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.91,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 0.5,
        "odds": 2.37,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.93,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.98,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.9,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.0,
        "odds": 1.95,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Haiti",
        "line": 1.5,
        "odds": 1.52,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Scotland",
        "line": -1.5,
        "odds": 2.51,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-D2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T20:00:00Z",
    "home_team": "Australia",
    "away_team": "Turkey",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.42,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.14,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.23,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.02,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.5,
        "odds": 2.16,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 0.75,
        "odds": 2.01,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Australia",
        "line": 1.5,
        "odds": 1.38,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Turkey",
        "line": -1.5,
        "odds": 2.92,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-C2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-13T23:00:00Z",
    "home_team": "Brazil",
    "away_team": "Morocco",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.88,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.21,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.5,
        "odds": 1.63,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.24,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.92,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.0,
        "odds": 2.2,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -0.75,
        "odds": 1.88,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Brazil",
        "line": -1.5,
        "odds": 2.9,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Morocco",
        "line": 1.5,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-B2",
    "date": "2026-06-13",
    "kickoff_at": "2026-06-14T02:00:00Z",
    "home_team": "Qatar",
    "away_team": "Switzerland",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.25,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.3,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.0,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.18,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.32,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.08,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 2.0,
        "odds": 1.74,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.75,
        "odds": 2.04,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Qatar",
        "line": 1.5,
        "odds": 2.2,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Switzerland",
        "line": -1.5,
        "odds": 1.66,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-GERMANY-CURA-AO",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T17:00:00Z",
    "home_team": "Germany",
    "away_team": "Curaçao",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.8,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.05,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.81,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.88,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.92,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.25,
        "odds": 2.0,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.83,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Curaçao",
        "line": 3.5,
        "odds": 1.85,
        "provider": "TAB"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-NETHERLANDS-JAPAN",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T20:00:00Z",
    "home_team": "Netherlands",
    "away_team": "Japan",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.0,
        "odds": 2.87,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.82,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.81,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.85,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.9,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.78,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 0.5,
        "odds": 1.89,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Japan",
        "line": 1.5,
        "odds": 1.25,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Netherlands",
        "line": 0.0,
        "odds": 1.43,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260614-IVORY-COAST-ECUADOR",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-14T23:00:00Z",
    "home_team": "Ivory Coast",
    "away_team": "Ecuador",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.59,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": 0.0,
        "odds": 1.62,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 1.98,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.33,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.45,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.06,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.5,
        "odds": 2.27,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -0.25,
        "odds": 2.02,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Ecuador",
        "line": -1.5,
        "odds": 5.0,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Ivory Coast",
        "line": 0.0,
        "odds": 2.4,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WCAPI-20260615-SWEDEN-TUNISIA",
    "date": "2026-06-14",
    "kickoff_at": "2026-06-15T02:00:00Z",
    "home_team": "Sweden",
    "away_team": "Tunisia",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": 0.0,
        "odds": 1.37,
        "provider": "1xBet"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetAnything"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "BetOnline.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "BetUS"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.87,
        "provider": "Bovada"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.86,
        "provider": "GTbets"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.88,
        "provider": "LowVig.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.95,
        "provider": "Matchbook"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.85,
        "provider": "MyBookie.ag"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -0.5,
        "odds": 1.9,
        "provider": "Pinnacle"
      },
      {
        "market": "handicap",
        "selection": "Sweden",
        "line": -1.5,
        "odds": 3.6,
        "provider": "PlayUp"
      },
      {
        "market": "handicap",
        "selection": "Tunisia",
        "line": 0.0,
        "odds": 3.17,
        "provider": "1xBet"
      }
    ]
  },
  {
    "match_id": "WC-H1",
    "date": "2026-06-15",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "Spain",
    "away_team": "Cape Verde",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "Spain",
        "odds": 1.08
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 10.0
      },
      {
        "market": "h2h",
        "selection": "Cape Verde",
        "odds": 29.0
      }
    ]
  },
  {
    "match_id": "WC-I1",
    "date": "2026-06-16",
    "kickoff_at": "2026-06-14T00:00:00Z",
    "home_team": "France",
    "away_team": "Senegal",
    "status": "scheduled",
    "available_markets": [],
    "market_snapshot": [
      {
        "market": "h2h",
        "selection": "France",
        "odds": 1.35
      },
      {
        "market": "h2h",
        "selection": "Draw",
        "odds": 4.8
      },
      {
        "market": "h2h",
        "selection": "Senegal",
        "odds": 8.5
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

