import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ops"))
loaded_pool = sys.modules.get("pool")
if loaded_pool and "/tests/pool" in str(getattr(loaded_pool, "__file__", "")):
    del sys.modules["pool"]

from run_daily_pool_pipeline import _apply_settlement_to_accounts, _settle


class SettlementFromMatchesTest(unittest.TestCase):
    def test_settlement_derives_results_from_scored_matches(self):
        payload = _settle(
            "unit-settle-from-matches",
            [
                {
                    "match_id": "M1",
                    "home_team": "Haiti",
                    "away_team": "Scotland",
                    "status": "settled",
                    "home_score": 0,
                    "away_score": 1,
                    "score_registry_applied": True,
                }
            ],
            {"matches": []},
            {
                "seats": {
                    "alpha": {
                        "investments": [
                            {
                                "match_id": "M1",
                                "action": "bet",
                                "market": "h2h",
                                "selection": "Scotland",
                                "odds": 1.57,
                                "stake_gp": 100,
                            }
                        ]
                    }
                }
            },
        )
        self.assertEqual(payload["settlement_status"], "settled")
        self.assertEqual(payload["summary"]["settled_bets"], 1)
        self.assertEqual(payload["summary"]["winning_bets"], 1)
        self.assertAlmostEqual(payload["seats"]["alpha"]["profit_gp"], 57)
        self.assertEqual(payload["matches"][0]["source"], "matches_api_score_registry")

    def test_handicap_and_total_settlement_use_score_registry_rows(self):
        payload = _settle(
            "unit-settle-handicap-total",
            [
                {
                    "match_id": "M2",
                    "home_team": "Germany",
                    "away_team": "Curacao",
                    "status": "settled",
                    "score": "7-1",
                    "score_registry_applied": True,
                }
            ],
            {},
            {
                "seats": {
                    "beta": {
                        "investments": [
                            {
                                "match_id": "M2",
                                "action": "bet",
                                "market": "handicap",
                                "selection": "Curacao",
                                "line": 3.5,
                                "odds": 1.83,
                                "stake_gp": 100,
                            },
                            {
                                "match_id": "M2",
                                "action": "bet",
                                "market": "total",
                                "selection": "over",
                                "line": 5.5,
                                "odds": 2.1,
                                "stake_gp": 50,
                            },
                        ]
                    }
                }
            },
        )
        self.assertEqual(payload["summary"]["settled_bets"], 2)
        self.assertEqual(payload["summary"]["winning_bets"], 1)
        self.assertEqual(payload["summary"]["losing_bets"], 1)
        self.assertAlmostEqual(payload["seats"]["beta"]["profit_gp"], -45)

    def test_debt_service_runs_before_ranking_basis(self):
        accounts = {
            "alpha": {
                "balance_gp": 1000,
                "outstanding_loan_gp": 100,
                "accrued_interest_gp": 0,
            }
        }
        settlement = {
            "run_id": "unit-debt-service",
            "seats": {"alpha": {"profit_gp": 200}},
        }
        updates = _apply_settlement_to_accounts(
            accounts,
            settlement,
            {
                "seats": {
                    "alpha": {
                        "investments": [
                            {"action": "bet", "loan_used_gp": 50}
                        ]
                    }
                }
            },
        )
        self.assertEqual(updates["alpha"]["ranking_basis"], "net_worth_after_settlement_interest_and_principal_repayment")
        self.assertGreater(updates["alpha"]["interest_paid_gp"], 0)
        self.assertEqual(updates["alpha"]["outstanding_loan_gp"], 0)
        self.assertEqual(accounts["alpha"]["outstanding_loan_gp"], 0)
        self.assertGreater(accounts["alpha"]["net_worth_gp"], 1000)


if __name__ == "__main__":
    unittest.main()
