import unittest
import shutil

from ops.pool.behavior_journal import append_seat_event
from ops.pool.behavior_replay import build_replay_for_run
from ops.pool.paths import DATA_ROOT


class BehaviorReplayTest(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(DATA_ROOT / "seat_journals" / "unit_replay", ignore_errors=True)

    def test_build_replay_for_run_reconstructs_event_state_and_counterfactual(self):
        seat_id = "unit_replay"
        run_id = "unit-replay-run"
        append_seat_event(seat_id, {
            "run_id": run_id,
            "event_type": "forecast_recorded",
            "forecasts": [{"match_id": "M1", "pick": "home"}],
            "status": "accepted",
        })
        append_seat_event(seat_id, {
            "run_id": run_id,
            "event_type": "investment_recorded",
            "investments": [
                {"match_id": "M1", "action": "bet", "market": "moneyline", "stake_gp": 300, "loan_used_gp": 100},
                {"match_id": "M2", "action": "no_bet", "market": "moneyline", "stake_gp": 0, "loan_used_gp": 0},
            ],
            "status": "accepted",
        })
        append_seat_event(seat_id, {
            "run_id": run_id,
            "event_type": "settlement_recorded",
            "settlement": {"profit_gp": -75},
        })

        replay = build_replay_for_run(run_id, [seat_id], write=False)

        self.assertEqual(replay["run_id"], run_id)
        self.assertEqual(replay["seat_count"], 1)
        self.assertGreaterEqual(replay["event_count"], 3)
        investment_event = next(row for row in replay["timeline"] if row["event_type"] == "investment_recorded")
        self.assertEqual(investment_event["action"], "investment")
        self.assertEqual(investment_event["risk_shift"], "loan_used")
        self.assertIn("state_before", investment_event)
        self.assertIn("state_after", investment_event)
        self.assertIn("decision_reconstruction", investment_event)
        self.assertIn("counterfactual", investment_event)
        self.assertTrue(investment_event["snapshot_ref"].endswith(".json"))


if __name__ == "__main__":
    unittest.main()
