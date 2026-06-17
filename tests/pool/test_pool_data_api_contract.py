import json
import unittest

import pool_data


class PoolDataApiContractTest(unittest.TestCase):
    def test_public_accessors_do_not_expose_local_paths_or_commands(self):
        rules = pool_data.get_current_rules()
        serialized = json.dumps(rules, ensure_ascii=False)
        self.assertNotIn("/Users/", serialized)
        self.assertNotIn("Codex", serialized)
        self.assertTrue(rules["artifact_ref"].startswith("data/pool/"))

    def test_runtime_summary_merges_score_registry_into_matches(self):
        summary = pool_data.get_runtime_summary(round_id="run-15", date="2026-06-15")
        matches = {row.get("match_id"): row for row in summary["matches"]}

        germany = matches.get("WCAPI-20260614-GERMANY-CURA-AO")
        self.assertIsNotNone(germany)
        self.assertEqual(germany["home_score"], 7)
        self.assertEqual(germany["away_score"], 1)
        self.assertEqual(germany["status"], "settled")
        self.assertTrue(germany["score_registry_applied"])

        self.assertGreaterEqual(summary["audit"]["score_registry_applied"], 1)
        self.assertGreaterEqual(summary["audit"]["score_registry_rows"], 1)


if __name__ == "__main__":
    unittest.main()
