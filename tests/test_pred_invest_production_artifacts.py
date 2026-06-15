from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "ops"
if str(OPS) in sys.path:
    sys.path.remove(str(OPS))
sys.path.insert(0, str(OPS))
for name in list(sys.modules):
    if name == "pool" or name.startswith("pool."):
        del sys.modules[name]

from run_pred_invest_daily_sop import PRODUCTION_SEATS, build_production_artifacts


class PredInvestProductionArtifactTests(unittest.TestCase):
    def _pack(self):
        prompts = [
            {
                "model_account": seat_id,
                "display_name": seat_id,
                "loan_terms": {"credit_score": 600, "credit_grade": "B", "net_worth_gp": 1000},
                "prompt": f"prompt for {seat_id}",
            }
            for seat_id in PRODUCTION_SEATS
        ]
        return {
            "matches": [{"match_id": "M1"}, {"match_id": "M2"}],
            "prompts": prompts,
        }

    def _shadow(self):
        return {
            "models_detail": [
                {
                    "model_account": seat_id,
                    "display_name": seat_id,
                    "loan_terms": {
                        "credit_score": 600,
                        "credit_grade": "B",
                        "net_worth_gp": 1000,
                        "outstanding_loan_gp": 0,
                        "max_loan_gp": 500,
                        "available_loan_gp": 500,
                        "base_interest_rate": 0.1,
                    },
                    "required_next_action": "submit split receipt",
                }
                for seat_id in PRODUCTION_SEATS
            ]
        }

    def _decision_state(self):
        seats = []
        for seat_id in PRODUCTION_SEATS:
            if seat_id == "grok":
                continue
            seats.append(
                {
                    "seat": seat_id,
                    "one_sentence_strategy": "test strategy",
                    "forecasts": [{"match_id": "M1", "p": 0.55}, {"match_id": "M2", "p": 0.45}],
                    "investments": [
                        {"match_id": "M1", "action": "bet", "stake_gp": 10, "odds": 1.8},
                        {"match_id": "M2", "action": "no_bet", "stake_gp": 0},
                    ],
                }
            )
        return {
            "seat_summaries": seats,
            "needs_rerun": ["grok"],
        }

    def test_production_artifacts_keep_all_12_seats_and_mark_missing(self):
        result = build_production_artifacts(
            "2026-06-15",
            "unit-production-run",
            self._pack(),
            self._shadow(),
            self._decision_state(),
            {"status": "unit"},
            write=False,
        )
        counts = result["counts"]
        self.assertEqual(counts["seat_count"], 12)
        self.assertEqual(counts["forecast_receipt_count"], 12)
        self.assertEqual(counts["investment_receipt_count"], 12)
        self.assertEqual(counts["valid_seat_count"], 11)
        self.assertEqual(counts["missing_seat_count"], 1)
        self.assertEqual(result["seat_statuses"]["grok"], "missing_provider_blocked")
        self.assertIn("run-15", build_production_artifacts(
            "2026-06-15",
            "run-15",
            self._pack(),
            self._shadow(),
            self._decision_state(),
            {"status": "unit"},
            write=False,
        )["artifact_refs"]["forecast_receipts"])


if __name__ == "__main__":
    unittest.main()
