import unittest

from ops.pool.credit_engine import calculate_credit_delta
from ops.pool.io_utils import write_json
from ops.pool.paths import DATA_ROOT
from ops.pool.rules_engine import RULE_VERSION


class CreditEngineTest(unittest.TestCase):
    def test_credit_delta_can_increase_and_decrease(self):
        run_id = "unit-credit-v2"
        write_json(DATA_ROOT / "forecast_receipts" / f"{run_id}.json", {
            "run_id": run_id,
            "rule_version": RULE_VERSION,
            "seats": {
                "right": {"forecasts": [{"match_id": "CREDIT-M1", "home_win_prob": 0.7, "draw_prob": 0.2, "away_win_prob": 0.1, "edge_assessment": "bettable"}]},
                "wrong": {"forecasts": [{"match_id": "CREDIT-M1", "home_win_prob": 0.1, "draw_prob": 0.2, "away_win_prob": 0.7, "edge_assessment": "bettable"}]},
            },
        })
        write_json(DATA_ROOT / "match_results" / f"{run_id}.json", {"matches": [{"match_id": "CREDIT-M1", "score": "2-0"}]})
        self.assertGreater(calculate_credit_delta("right", run_id)["credit_delta"], 0)
        self.assertLess(calculate_credit_delta("wrong", run_id)["credit_delta"], 0)


if __name__ == "__main__":
    unittest.main()
