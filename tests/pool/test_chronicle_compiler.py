import shutil
import unittest

from ops.pool.chronicle_compiler import compile_all_lessons, compile_lessons, generate_run_chronicle
from ops.pool.io_utils import append_jsonl
from ops.pool.paths import DATA_ROOT


class ChronicleCompilerTest(unittest.TestCase):
    def setUp(self):
        self.seat_id = "unit_chronicle"
        self.run_id = "unit-chronicle-run"
        self.journal = DATA_ROOT / "seat_journals" / self.seat_id / "journal.jsonl"
        append_jsonl(self.journal, {
            "ts": "2026-06-17T00:00:00+00:00",
            "seat_id": self.seat_id,
            "run_id": self.run_id,
            "event_type": "investment_recorded",
            "investments": [
                {"match_id": "M1", "action": "bet", "stake_gp": 500, "loan_used_gp": 200, "odds": 4.5},
                {"match_id": "M2", "action": "no_bet", "stake_gp": 0, "loan_used_gp": 0},
                {"match_id": "M3", "action": "no_bet", "stake_gp": 0, "loan_used_gp": 0},
            ],
        })
        append_jsonl(self.journal, {
            "ts": "2026-06-17T01:00:00+00:00",
            "seat_id": self.seat_id,
            "run_id": self.run_id,
            "event_type": "settlement_recorded",
            "settlement": {"profit_gp": -90},
        })

    def tearDown(self):
        shutil.rmtree(DATA_ROOT / "seat_journals" / self.seat_id, ignore_errors=True)
        shutil.rmtree(DATA_ROOT / "behavior_chronicle" / self.seat_id, ignore_errors=True)
        (DATA_ROOT / "behavior_patterns" / f"{self.seat_id}.json").unlink(missing_ok=True)
        (DATA_ROOT / "behavior_chronicle" / "runs" / f"{self.run_id}.json").unlink(missing_ok=True)
        (DATA_ROOT / "behavior_chronicle" / "runs" / f"{self.run_id}.md").unlink(missing_ok=True)

    def test_compile_lessons_writes_prompt_injection(self):
        payload = compile_lessons(self.seat_id, write=True)

        self.assertEqual(payload["seat_id"], self.seat_id)
        self.assertGreaterEqual(payload["lesson_count"], 1)
        self.assertIn("行为通鉴经验", payload["prompt_injection"])
        self.assertTrue((DATA_ROOT / "behavior_chronicle" / self.seat_id / "lessons.json").exists())
        self.assertTrue((DATA_ROOT / "behavior_chronicle" / self.seat_id / "chronicle.md").exists())

    def test_generate_run_chronicle_summarizes_seat_lessons(self):
        index = compile_all_lessons([self.seat_id], write=False)
        run = generate_run_chronicle("2026-06-17", self.run_id, [self.seat_id], write=True)

        self.assertEqual(index["seat_count"], 1)
        self.assertEqual(run["run_id"], self.run_id)
        self.assertTrue(run["highlights"])
        self.assertIn(self.seat_id, run["markdown"])


if __name__ == "__main__":
    unittest.main()
