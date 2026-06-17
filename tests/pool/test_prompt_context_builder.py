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
        behavior_kernel = context["private_context"]["behavior_kernel"]
        self.assertTrue(behavior_kernel["decision_contract"]["must_consider_memory"])
        self.assertIn("behavior_type", behavior_kernel["profile"])
        self.assertIn("behavior_memory_required_fields", context["public_context"]["output_contract"])
        self.assertIn("behavior_chronicle", context["private_context"])
        self.assertIn("prompt_injection", context["private_context"]["behavior_chronicle"])
        self.assertIn("behavior_chronicle_required_fields", context["public_context"]["output_contract"])
        self.assertNotIn("beta", json.dumps(context["private_context"], ensure_ascii=False).lower())
        leakage = validate_no_cross_seat_leakage(context, "alpha", ["alpha", "beta"])
        self.assertTrue(leakage["ok"], leakage)

    def test_leakage_detector_scans_public_context_without_team_name_false_positive(self):
        clean = {
            "seat_id": "alpha",
            "public_context": {
                "match": {"home_team": "Alpha FC", "away_team": "Beta FC"},
                "commentary": "public neutral market note",
            },
        }
        self.assertTrue(validate_no_cross_seat_leakage(clean, "alpha", ["alpha", "beta"])["ok"])

        leaked = {
            "seat_id": "alpha",
            "public_context": {
                "visible_owner": "beta",
            },
        }
        result = validate_no_cross_seat_leakage(leaked, "alpha", ["alpha", "beta"])
        self.assertFalse(result["ok"])
        self.assertEqual(result["leaked_seats"], ["beta"])


if __name__ == "__main__":
    unittest.main()
