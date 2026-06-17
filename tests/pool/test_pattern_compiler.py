import shutil
import unittest

from ops.pool.io_utils import append_jsonl
from ops.pool.paths import DATA_ROOT
from ops.pool.pattern_compiler import DETECTORS, PATTERN_CATALOG, REQUIRED_PATTERN_FIELDS, compile_all_patterns, compile_patterns


class PatternCompilerTest(unittest.TestCase):
    def setUp(self):
        self.seat_id = "unit_pattern_compiler"
        self.journal = DATA_ROOT / "seat_journals" / self.seat_id / "journal.jsonl"

    def tearDown(self):
        shutil.rmtree(DATA_ROOT / "seat_journals" / self.seat_id, ignore_errors=True)
        (DATA_ROOT / "behavior_patterns" / f"{self.seat_id}.json").unlink(missing_ok=True)

    def _write_fixture(self):
        append_jsonl(self.journal, {
            "ts": "2026-06-17T00:00:00+00:00",
            "seat_id": self.seat_id,
            "run_id": "unit-pattern-a",
            "event_type": "forecast_recorded",
            "forecasts": [
                {"match_id": "M1", "home_win_prob": 0.7, "draw_prob": 0.12, "away_win_prob": 0.18, "confidence": 0.78, "information_gaps": ["lineup"]},
                {"match_id": "M2", "home_win_prob": 0.64, "draw_prob": 0.16, "away_win_prob": 0.2, "confidence": 0.72, "information_gaps": ["odds"]},
                {"match_id": "M3", "home_win_prob": 0.61, "draw_prob": 0.19, "away_win_prob": 0.2, "confidence": 0.68},
                {"match_id": "M4", "home_win_prob": 0.59, "draw_prob": 0.18, "away_win_prob": 0.23, "confidence": 0.66},
            ],
        })
        append_jsonl(self.journal, {
            "ts": "2026-06-17T01:00:00+00:00",
            "seat_id": self.seat_id,
            "run_id": "unit-pattern-a",
            "event_type": "investment_recorded",
            "investments": [
                {"match_id": "M1", "action": "bet", "stake_gp": 700, "loan_used_gp": 650, "odds": 4.2, "model_prob": 0.42, "market_implied_prob": 0.31, "estimated_ev": 0.12},
                {"match_id": "M2", "action": "bet", "stake_gp": 80, "loan_used_gp": 0, "odds": 1.8, "model_prob": 0.58, "market_implied_prob": 0.52, "estimated_ev": 0.04},
                {"match_id": "M3", "action": "no_bet", "stake_gp": 0, "loan_used_gp": 0},
                {"match_id": "M4", "action": "no_bet", "stake_gp": 0, "loan_used_gp": 0},
            ],
        })
        append_jsonl(self.journal, {
            "ts": "2026-06-17T02:00:00+00:00",
            "seat_id": self.seat_id,
            "run_id": "unit-pattern-a",
            "event_type": "survival_updated",
            "recovery_mode": True,
        })
        append_jsonl(self.journal, {
            "ts": "2026-06-17T03:00:00+00:00",
            "seat_id": self.seat_id,
            "run_id": "unit-pattern-a",
            "event_type": "settlement_recorded",
            "settlement": {"profit_gp": -120},
        })

    def test_detector_catalog_has_twelve_behavior_patterns(self):
        self.assertEqual(len(DETECTORS), 12)
        self.assertEqual(set(PATTERN_CATALOG), {
            "home_bias",
            "upset_aversion",
            "confidence_calibration",
            "high_odds_exposure",
            "loss_chasing",
            "stake_volatility",
            "no_bet_quality",
            "recovery_compliance",
            "loan_discipline",
            "bankrupt_approach",
            "strategy_adaptation",
            "error_correction",
        })

    def test_compile_patterns_extracts_evidence_and_sources(self):
        self._write_fixture()
        payload = compile_patterns(self.seat_id, write=True)
        pattern_ids = {row["pattern_id"] for row in payload["patterns"]}

        self.assertEqual(payload["seat_id"], self.seat_id)
        self.assertEqual(set(payload["pattern_catalog"]), set(PATTERN_CATALOG))
        self.assertIn("favorite_bias", pattern_ids)
        self.assertIn("loan_dependency", pattern_ids)
        self.assertTrue(all(row["source_event_ids"] for row in payload["patterns"]))
        self.assertTrue(all(set(REQUIRED_PATTERN_FIELDS).issubset(row) for row in payload["patterns"]))
        self.assertTrue(all(row["canonical_pattern_id"] in PATTERN_CATALOG for row in payload["patterns"]))
        self.assertTrue((DATA_ROOT / "behavior_patterns" / f"{self.seat_id}.json").exists())

    def test_compile_all_patterns_returns_index_without_writing(self):
        self._write_fixture()
        index = compile_all_patterns([self.seat_id], write=False)
        self.assertEqual(index["seat_count"], 1)
        self.assertGreaterEqual(index["pattern_count"], 1)
        self.assertTrue(index["top_patterns"])


if __name__ == "__main__":
    unittest.main()
