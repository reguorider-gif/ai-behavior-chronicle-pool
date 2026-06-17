import unittest
import shutil

from ops.pool.behavior_journal import append_seat_event, load_recent_seat_events, update_seat_summary
from ops.pool.paths import DATA_ROOT


class BehaviorJournalTest(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(DATA_ROOT / "seat_journals" / "tmp_unit_journal_alpha", ignore_errors=True)

    def test_append_and_summary(self):
        seat_id = "tmp_unit_journal_alpha"
        append_seat_event(seat_id, {"event_type": "self_review_recorded", "run_id": "unit-run", "self_review": {"what_i_learned": "keep memory"}})
        append_seat_event(seat_id, {"event_type": "account_snapshot", "run_id": "unit-run", "balance_gp": 1100, "outstanding_loan_gp": 50, "net_worth_gp": 1050})
        recent = load_recent_seat_events(seat_id, limit=2)
        self.assertEqual(len(recent), 2)
        summary = update_seat_summary(seat_id, "unit-run")
        self.assertIn("unit-run", summary["runs_seen"])
        self.assertEqual(summary["balance_gp"], 1100)
        self.assertEqual(summary["net_worth_gp"], 1050)


if __name__ == "__main__":
    unittest.main()
