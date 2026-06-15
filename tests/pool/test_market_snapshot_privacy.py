import json
import unittest

from ops.pool.prompt_context_builder import build_market_snapshot


class MarketSnapshotPrivacyTest(unittest.TestCase):
    def test_market_snapshot_has_no_seat_choices(self):
        snapshot = build_market_snapshot("2026-06-15", "unit-market", [{
            "match_id": "MKT-M1",
            "date": "2026-06-15",
            "home_team": "One",
            "away_team": "Two",
            "markets": [{"market": "h2h", "selection": "home", "odds": 1.9}],
        }])
        serialized = json.dumps(snapshot, ensure_ascii=False)
        self.assertNotIn("stake_gp", serialized)
        self.assertNotIn("loan_used_gp", serialized)
        self.assertNotIn("seat_id", serialized)
        self.assertEqual(snapshot["privacy"], "anonymous_market_only_no_seat_choices")


if __name__ == "__main__":
    unittest.main()
