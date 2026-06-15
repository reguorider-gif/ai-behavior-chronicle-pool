import unittest

from ops.pool.io_utils import read_json
from ops.pool.paths import FIXTURE_ROOT
from ops.pool.rules_engine import RULE_VERSION, validate_forecast_receipt, validate_investment_receipt


class RulesEngineV2Test(unittest.TestCase):
    def test_fixture_receipts_validate_and_no_bet_is_legal(self):
        outputs = read_json(FIXTURE_ROOT / "smoke_behavior_v2" / "model_outputs_run_a.json")
        required = ["SMOKE-M1", "SMOKE-M2"]
        alpha = outputs["seats"]["alpha"]
        forecast = validate_forecast_receipt(alpha, required, RULE_VERSION)
        investment = validate_investment_receipt(alpha, required, loan_limit_gp=500, recovery_mode=False, net_worth_gp=1000, rule_version=RULE_VERSION)
        self.assertTrue(forecast["ok"], forecast)
        self.assertTrue(investment["ok"], investment)
        self.assertEqual(investment["total_loan_used_gp"], 0)

    def test_recovery_mode_rejects_new_loan(self):
        outputs = read_json(FIXTURE_ROOT / "smoke_behavior_v2" / "model_outputs_run_a.json")
        gamma = dict(outputs["seats"]["gamma"])
        gamma["loan_decision"] = {"request_loan_gp": 10}
        gamma["investments"] = [dict(item) for item in gamma["investments"]]
        gamma["investments"][0].update({"action": "bet", "market": "h2h", "selection": "home", "odds": 1.8, "stake_gp": 10, "loan_used_gp": 10})
        result = validate_investment_receipt(gamma, ["SMOKE-M1", "SMOKE-M2"], loan_limit_gp=0, recovery_mode=True, net_worth_gp=-60, rule_version=RULE_VERSION)
        self.assertFalse(result["ok"])
        self.assertIn("recovery_mode_new_loan_forbidden:SMOKE-M1", result["errors"])


if __name__ == "__main__":
    unittest.main()
