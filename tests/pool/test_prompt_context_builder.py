import json
import unittest

from ops.pool.prompt_context_builder import build_prompt_context
from ops.pool.rules_engine import RULE_VERSION, validate_no_cross_seat_leakage


class PromptContextBuilderTest(unittest.TestCase):
    def test_context_contains_own_state_and_no_private_opponent_logs(self):
        matches = [{"match_id": "CTX-M1", "date": "2026-06-15", "home_team": "Alpha FC", "away_team": "Beta FC", "markets": []}]
        accounts = {
            "alpha": {"balance_gp": 1000, "outstanding_loan_gp": 0, "accrued_interest_gp": 0},
            "beta": {"balance_gp": 900, "outstanding_loan_gp": 100, "accrued_interest_gp": 0},
        }
        context = build_prompt_context("2026-06-15", "unit-context", "alpha", RULE_VERSION, accounts=accounts, matches=matches)
        self.assertEqual(context["private_context"]["own_account"]["balance_gp"], 1000)
        self.assertIn("anonymous_market_snapshot", context["public_context"])
        self.assertNotIn("beta", json.dumps(context["private_context"], ensure_ascii=False).lower())
        leakage = validate_no_cross_seat_leakage(context, "alpha", ["alpha", "beta"])
        self.assertTrue(leakage["ok"], leakage)


if __name__ == "__main__":
    unittest.main()
