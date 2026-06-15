import unittest

from ops.pool.survival_engine import apply_recovery_constraints, calculate_net_worth, detect_recovery_mode


class SurvivalEngineTest(unittest.TestCase):
    def test_net_worth_and_recovery_constraints(self):
        self.assertEqual(calculate_net_worth(50, 100, 10), -60)
        account = {"balance_gp": 50, "outstanding_loan_gp": 100, "accrued_interest_gp": 10}
        self.assertTrue(detect_recovery_mode("gamma", account))
        constraints = apply_recovery_constraints("gamma", account)
        self.assertTrue(constraints["freeze_new_loan"])
        self.assertIn("no_bet", constraints["allowed_actions"])


if __name__ == "__main__":
    unittest.main()
