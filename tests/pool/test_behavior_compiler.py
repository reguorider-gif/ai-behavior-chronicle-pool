import unittest
import shutil

from ops.pool.behavior_compiler import compile_all_behavior_memory, compile_behavior_memory
from ops.pool.io_utils import append_jsonl
from ops.pool.paths import DATA_ROOT


class BehaviorCompilerTest(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(DATA_ROOT / "seat_journals" / "unit_behavior_compiler", ignore_errors=True)

    def test_compile_seat_memory_from_journal_events(self):
        seat_id = "unit_behavior_compiler"
        run_id = "unit-behavior-run"
        journal_path = DATA_ROOT / "seat_journals" / seat_id / "journal.jsonl"
        append_jsonl(journal_path, {
            "ts": "2026-06-16T00:00:00+00:00",
            "seat_id": seat_id,
            "run_id": run_id,
            "event_type": "investment_recorded",
            "investments": [
                {"match_id": "M1", "action": "bet", "stake_gp": 320, "loan_used_gp": 120},
                {"match_id": "M2", "action": "no_bet", "stake_gp": 0, "loan_used_gp": 0},
            ],
        })
        append_jsonl(journal_path, {
            "ts": "2026-06-16T01:00:00+00:00",
            "seat_id": seat_id,
            "run_id": run_id,
            "event_type": "settlement_recorded",
            "settlement": {"profit_gp": -80},
        })

        memory = compile_behavior_memory(seat_id, write=False)

        self.assertEqual(memory["seat_id"], seat_id)
        self.assertIn(memory["profile"]["risk_level"], {"medium", "high"})
        self.assertIn(memory["profile"]["loan_dependency"], {"medium", "high"})
        self.assertGreaterEqual(len(memory["top_patterns"]), 1)
        self.assertTrue(memory["memory_contract"]["must_reference_in_next_decision"])

    def test_compile_all_generates_product_objects(self):
        bundle = compile_all_behavior_memory(["chatgpt", "deepseek"], run_id="unit-kernel", write=False)

        self.assertEqual(bundle["seat_count"], 2)
        self.assertIn("top_patterns", bundle["pattern_graph"])
        self.assertEqual(len(bundle["agent_profiles"]["seats"]), 2)
        self.assertEqual(len(bundle["evolution_trace"]["traces"]), 2)


if __name__ == "__main__":
    unittest.main()
