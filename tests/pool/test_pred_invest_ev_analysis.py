import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import generate_pred_invest_strict_god_report as report


class PredInvestEvAnalysisTest(unittest.TestCase):
    def test_infers_ev_from_compact_forecast_confidence(self):
        valid = [
            {
                "seat": "chatgpt",
                "forecasts": [
                    {
                        "match_id": "M1",
                        "p": "home",
                        "confidence": 61,
                        "score": "2-1",
                    }
                ],
                "investments": [
                    {
                        "match_id": "M1",
                        "action": "bet",
                        "market": "moneyline",
                        "selection": "Portugal",
                        "odds": 1.75,
                        "stake_gp": 100,
                    }
                ],
            }
        ]
        matches = {"M1": {"match_id": "M1", "home_team": "Portugal", "away_team": "Colombia"}}
        ev = report._ev_analysis(valid, matches)
        row = ev["rows"][0]
        self.assertEqual(row["coverage"], "complete_proxy_inferred")
        self.assertEqual(row["model_prob"], 0.61)
        self.assertAlmostEqual(row["market_implied_prob"], 0.5714, places=4)
        self.assertAlmostEqual(row["estimated_ev"], 0.0675, places=4)
        self.assertEqual(ev["data_gap_rows"], [])

    def test_preserves_explicit_model_probability(self):
        valid = [
            {
                "seat": "deepseek",
                "forecasts": [{"match_id": "M1", "home_win_prob": 0.48, "draw_prob": 0.29, "away_win_prob": 0.23}],
                "investments": [
                    {
                        "match_id": "M1",
                        "action": "bet",
                        "market": "h2h",
                        "selection": "Draw",
                        "odds": 3.6,
                        "model_prob": 0.29,
                        "market_implied_prob": 0.278,
                        "estimated_ev": 0.044,
                    }
                ],
            }
        ]
        matches = {"M1": {"match_id": "M1", "home_team": "Portugal", "away_team": "Colombia"}}
        ev = report._ev_analysis(valid, matches)
        row = ev["rows"][0]
        self.assertEqual(row["coverage"], "complete_explicit")
        self.assertEqual(row["model_prob_source"], "investment.model_prob")
        self.assertEqual(row["estimated_ev"], 0.044)

    def test_no_bet_uses_forecast_lean_as_opportunity_cost_ev(self):
        valid = [
            {
                "seat": "mimo",
                "forecasts": [
                    {
                        "match_id": "M1",
                        "p": "away",
                        "confidence": 66,
                    }
                ],
                "investments": [
                    {
                        "match_id": "M1",
                        "action": "no_bet",
                        "market": "none",
                        "selection": "none",
                        "line": "none",
                        "odds": 0,
                        "stake_gp": 0,
                    }
                ],
            }
        ]
        matches = {
            "M1": {
                "match_id": "M1",
                "home_team": "Saudi Arabia",
                "away_team": "Uruguay",
                "market_snapshot": [
                    {"market": "h2h", "selection": "Saudi Arabia", "odds": 6.5},
                    {"market": "h2h", "selection": "Uruguay", "odds": 1.62},
                ],
            }
        }
        ev = report._ev_analysis(valid, matches)
        row = ev["rows"][0]
        self.assertEqual(row["probability_target"], "away")
        self.assertEqual(row["coverage"], "complete_proxy_inferred")
        self.assertEqual(row["model_prob"], 0.66)
        self.assertAlmostEqual(row["market_implied_prob"], 0.6173, places=4)
        self.assertAlmostEqual(row["estimated_ev"], 0.0692, places=4)
        self.assertEqual(ev["data_gap_rows"], [])


if __name__ == "__main__":
    unittest.main()
