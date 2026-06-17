import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "ops"
if str(OPS) in sys.path:
    sys.path.remove(str(OPS))
sys.path.insert(0, str(OPS))

import run_pred_invest_single_seat_reruns as reruns
import audit_pred_invest_bridge_outputs as bridge_audit
import dispatch_seats
import submit_pred_invest_bridge_run as bridge_submit


def _args(**overrides):
    base = {
        "date": "2026-06-17",
        "round_id": "unit-run",
        "runs": "base-run",
        "seats": "chatgpt,deepseek",
        "attempt": 4,
        "max_attempts": 5,
        "judge_mode": "quick_judge",
        "base_url": "https://pool-app-one.vercel.app",
        "bridge_base_url": "http://127.0.0.1:8501",
        "verdict_timeout_seconds": 720.0,
        "poll_seconds": 8.0,
        "bridge_wait_seconds": 300.0,
        "recover_after_seconds": 180.0,
        "recover_stuck_bridge": False,
        "force_valid_seats": False,
        "force_provider_blocked": False,
        "skip_page_salvage": True,
        "progress_reports": False,
        "cdp_endpoint": "http://127.0.0.1:9333",
        "dry_run": False,
    }
    base.update(overrides)
    return SimpleNamespace(**base)


def _gate(needs):
    required = len(reruns.DEFAULT_TARGET_SEATS)
    return {
        "status": "needs_rerun" if needs else "ready",
        "valid_count": required - len(needs),
        "required_seat_count": required,
        "valid_seats": [seat for seat in reruns.DEFAULT_TARGET_SEATS if seat not in set(needs)],
        "needs_rerun": needs,
        "provider_blocked_seats": [],
        "required_match_ids": ["M1", "M2"],
        "required_match_source": "unit",
    }


def _artifacts():
    required = len(reruns.DEFAULT_TARGET_SEATS)
    return {
        "audit_paths": {},
        "quality_gate_paths": {},
        "sop_guard_paths": {},
        "observer_paths": {},
        "observer_error": None,
        "daily_sop_return_code": 0,
        "current_game_return_code": 0,
        "quality_gate": {
            "status": "ready",
            "publish_allowed": True,
            "valid_count": required,
            "required_seat_count": required,
            "valid_seats": list(reruns.DEFAULT_TARGET_SEATS),
            "needs_rerun": [],
        },
    }


class SingleSeatRerunPerformanceTest(unittest.TestCase):
    def test_missing_prompt_pack_returns_structured_missing_contract(self):
        ids, source = bridge_audit._required_match_ids("2099-01-01", "missing-pack-unit")

        self.assertEqual(ids, [])
        self.assertEqual(source, "prompt_pack_missing:2099-01-01_missing-pack-unit_prompt_pack.json")

    def test_rerun_waits_bridge_once_and_writes_final_report_once(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with (
                patch.object(reruns, "OUT_DIR", Path(tmpdir)),
                patch.object(reruns.pred_invest_quality_gate, "build_gate", return_value=_gate(["chatgpt", "deepseek"])),
                patch.object(reruns, "_wait_for_bridge_idle", return_value={"ok": True, "status": {}}) as wait_bridge,
                patch.object(reruns, "submit", side_effect=[
                    {"ok": True, "response": {"run_id": "seat-run-1"}},
                    {"ok": True, "response": {"run_id": "seat-run-2"}},
                ]) as submit,
                patch.object(reruns, "_wait_for_verdict", return_value={"ok": True, "verdict": {"verdict_status": "ok"}}) as wait_verdict,
                patch.object(reruns, "_regenerate_artifacts", return_value=_artifacts()) as regenerate,
                patch.object(reruns, "_write_attempt_report", return_value={"json": "unit.json"}) as write_report,
            ):
                report = reruns.run(_args())
            self.assertEqual([row["seat"] for row in report["runs"]], ["chatgpt", "deepseek"])
            self.assertEqual(report["final_run_ids"], ["base-run", "seat-run-1", "seat-run-2"])
            for row in report["runs"]:
                receipt_path = Path(row["receipt_path"])
                self.assertTrue(receipt_path.exists())
                saved = json.loads(receipt_path.read_text(encoding="utf-8"))
                self.assertEqual(saved["response"]["run_id"], row["run_id"])
        wait_bridge.assert_called_once()
        self.assertEqual(submit.call_count, 2)
        for call in submit.call_args_list:
            self.assertTrue(call.kwargs["compact"])
            self.assertFalse(call.kwargs["ultra_compact"])
            self.assertTrue(call.kwargs["assume_requested_ready"])
        self.assertEqual(wait_verdict.call_count, 2)
        regenerate.assert_called_once()
        write_report.assert_called_once()

    def test_bridge_wait_does_not_treat_curl_failure_as_ready(self):
        statuses = [
            {
                "ok": False,
                "error": "curl_non_json_response",
                "curl_returncode": 7,
                "raw": "curl: (7) Failed to connect to 127.0.0.1 port 8501",
            },
            {
                "ok": True,
                "busy": False,
                "bridge_run": {"busy": False},
            },
        ]
        with (
            patch.object(reruns, "http_json", side_effect=statuses) as http_json,
            patch.object(reruns.time, "sleep") as sleep,
        ):
            result = reruns._wait_for_bridge_idle("http://127.0.0.1:8501", recover_after=180, wait_seconds=300)

        self.assertTrue(result["ok"])
        self.assertEqual(http_json.call_count, 2)
        sleep.assert_called_once_with(10)

    def test_no_target_rerun_skips_bridge_wait_but_refreshes_artifacts_once(self):
        with (
            patch.object(reruns.pred_invest_quality_gate, "build_gate", return_value=_gate([])),
            patch.object(reruns, "_wait_for_bridge_idle") as wait_bridge,
            patch.object(reruns, "submit") as submit,
            patch.object(reruns, "_regenerate_artifacts", return_value=_artifacts()) as regenerate,
            patch.object(reruns, "_write_attempt_report", return_value={"json": "unit.json"}) as write_report,
        ):
            report = reruns.run(_args())

        self.assertEqual(report["targets"], [])
        self.assertEqual(report["initial_bridge_ready"]["source"], "no_targets")
        wait_bridge.assert_not_called()
        submit.assert_not_called()
        regenerate.assert_called_once()
        write_report.assert_called_once()

    def test_rerun_refuses_to_expand_without_required_match_contract(self):
        gate = _gate(["chatgpt"])
        gate["required_match_ids"] = []
        gate["required_match_source"] = "prompt_pack_missing:unit"
        with (
            patch.object(reruns.pred_invest_quality_gate, "build_gate", return_value=gate),
            patch.object(reruns, "_wait_for_bridge_idle") as wait_bridge,
            patch.object(reruns, "submit") as submit,
            patch.object(reruns, "_regenerate_artifacts") as regenerate,
            patch.object(reruns, "_write_attempt_report", return_value={"json": "unit.json"}) as write_report,
        ):
            report = reruns.run(_args(seats="chatgpt"))

        self.assertEqual(report["errors"], ["missing_required_match_contract"])
        self.assertIn("prompt_pack_or_required_match_snapshot_missing", report["warnings"])
        wait_bridge.assert_not_called()
        submit.assert_not_called()
        regenerate.assert_not_called()
        write_report.assert_called_once()

    def test_rerun_stops_when_attempt_exceeds_limit(self):
        with (
            patch.object(reruns.pred_invest_quality_gate, "build_gate", return_value=_gate(["chatgpt"])),
            patch.object(reruns, "_wait_for_bridge_idle") as wait_bridge,
            patch.object(reruns, "submit") as submit,
            patch.object(reruns, "_regenerate_artifacts") as regenerate,
            patch.object(reruns, "_write_attempt_report", return_value={"json": "unit.json"}) as write_report,
        ):
            report = reruns.run(_args(seats="chatgpt", attempt=6, max_attempts=5))

        self.assertEqual(report["early_termination"]["action"], "manual_intervention_required")
        self.assertIn("attempt_limit_reached", report["warnings"])
        wait_bridge.assert_not_called()
        submit.assert_not_called()
        regenerate.assert_not_called()
        write_report.assert_called_once()

    def test_dry_run_attempt_limit_keeps_dry_run_metadata(self):
        with (
            patch.object(reruns.pred_invest_quality_gate, "build_gate", return_value=_gate(["chatgpt"])),
            patch.object(reruns, "_wait_for_bridge_idle") as wait_bridge,
            patch.object(reruns, "submit") as submit,
            patch.object(reruns, "_regenerate_artifacts") as regenerate,
            patch.object(reruns, "_write_attempt_report", return_value={"json": "unit.json"}) as write_report,
        ):
            report = reruns.run(_args(seats="chatgpt", attempt=6, max_attempts=5, dry_run=True))

        self.assertTrue(report["dry_run"])
        self.assertEqual(report["early_termination"]["action"], "manual_intervention_required")
        wait_bridge.assert_not_called()
        submit.assert_not_called()
        regenerate.assert_not_called()
        write_report.assert_called_once()

    def test_rerun_stops_when_previous_attempt_did_not_improve(self):
        previous = {"final_quality_gate": {"valid_seats": ["deepseek", "gemini"]}}
        gate = _gate(["chatgpt"])
        gate["valid_seats"] = ["deepseek", "gemini"]
        with (
            patch.object(reruns.pred_invest_quality_gate, "build_gate", return_value=gate),
            patch.object(reruns, "_load_json_file", return_value=previous),
            patch.object(reruns, "_wait_for_bridge_idle") as wait_bridge,
            patch.object(reruns, "submit") as submit,
            patch.object(reruns, "_regenerate_artifacts") as regenerate,
            patch.object(reruns, "_write_attempt_report", return_value={"json": "unit.json"}) as write_report,
        ):
            report = reruns.run(_args(seats="chatgpt", attempt=5))

        self.assertEqual(report["early_termination"]["reason"], "no improvement since last attempt")
        self.assertIn("no_attempt_improvement", report["warnings"])
        wait_bridge.assert_not_called()
        submit.assert_not_called()
        regenerate.assert_not_called()
        write_report.assert_called_once()

    def test_daily_dispatch_uses_full_structured_contract_not_ultra_compact(self):
        with (
            patch.object(dispatch_seats, "submit", return_value={"ok": True, "response": {"run_id": "dispatch-run-1"}}) as submit,
            patch.object(dispatch_seats, "_wait_for_verdict", return_value={"ok": True, "verdict": {"verdict_status": "ok"}}),
        ):
            report = dispatch_seats.SeatDispatcher("http://127.0.0.1:8501").dispatch(
                date="2026-06-17",
                round_id="unit-run",
                seats=["chatgpt"],
                dry_run=False,
                write=False,
            )

        self.assertTrue(report["ok"])
        submit.assert_called_once()
        self.assertTrue(submit.call_args.kwargs["compact"])
        self.assertFalse(submit.call_args.kwargs["ultra_compact"])
        self.assertEqual(submit.call_args.kwargs["judge_mode"], "strategic")
        self.assertTrue(submit.call_args.kwargs["assume_requested_ready"])

    def test_compact_prompt_preserves_credit_score_risk_and_four_market_rows(self):
        market_rows = [
            {"market": "h2h", "selection": "A", "line": None, "odds": 1.8, "provider": "pinnacle"},
            {"market": "h2h", "selection": "draw", "line": None, "odds": 3.3, "provider": "pinnacle"},
            {"market": "h2h", "selection": "B", "line": None, "odds": 4.2, "provider": "1xbet"},
            {"market": "total", "selection": "over", "line": 2.5, "odds": 1.95, "provider": "betus"},
            {"market": "total", "selection": "under", "line": 2.5, "odds": 1.9, "provider": "other"},
        ]
        with (
            patch.object(bridge_submit, "_filter_summary_matches", return_value=(
                {
                    "date": "2026-06-17",
                    "round_id": "unit-run",
                    "matches": [
                        {
                            "match_id": "M1",
                            "home_team": "A",
                            "away_team": "B",
                            "market_snapshot": market_rows,
                        }
                    ],
                    "active_models": [
                        {
                            "model_account": "chatgpt",
                            "rank": 3,
                            "balance_gp": 1000,
                            "net_worth_gp": 1100,
                            "loan_gp": 0,
                            "credit_grade": "A",
                            "credit_score": 730,
                            "required_next_action": "submit split receipt",
                        }
                    ],
                    "submission_required_match_ids": ["M1"],
                },
                "unit",
            )),
            patch("pool_data.get_runtime_summary", return_value={}),
        ):
            receipt = bridge_submit.submit(
                "http://127.0.0.1:8501",
                "2026-06-17",
                "unit-run",
                dry_run=True,
                requested_seats=["chatgpt"],
                compact=True,
                ultra_compact=False,
                assume_requested_ready=True,
            )

        question = receipt["payload"]["question"]
        self.assertIn("score730", question)
        self.assertIn("risksubmit split receipt", question)
        self.assertIn("over@1.95", question)
        self.assertNotIn("under@1.9", question)

    def test_pred_invest_single_seat_payload_marks_grok_and_mimo_required_rescue(self):
        for seat in ("grok", "mimo"):
            with (
                patch.object(bridge_submit, "_filter_summary_matches", return_value=(
                    {
                        "date": "2026-06-17",
                        "round_id": "unit-run",
                        "matches": [{"match_id": "M1", "home_team": "A", "away_team": "B"}],
                        "active_models": [
                            {
                                "model_account": "xai" if seat == "grok" else "mimo",
                                "rank": 12,
                                "balance_gp": 1000,
                                "net_worth_gp": 1000,
                                "loan_gp": 0,
                                "credit_grade": "B",
                            }
                        ],
                        "submission_required_match_ids": ["M1"],
                    },
                    "unit",
                )),
                patch("pool_data.get_runtime_summary", return_value={}),
            ):
                receipt = bridge_submit.submit(
                    "http://127.0.0.1:8501",
                    "2026-06-17",
                    "unit-run",
                    dry_run=True,
                    requested_seats=[seat],
                    compact=True,
                    ultra_compact=False,
                    attempt_no=8,
                    judge_mode="strategic",
                    assume_requested_ready=True,
                )

            seat_config = receipt["payload"]["seat_config"]
            question = receipt["payload"]["question"]
            seat_policy = seat_config["seats"][seat]
            self.assertEqual(seat_config["execution_policy"], "all_selected_required_for_pred_invest")
            self.assertEqual(seat_config["required_seats"], [seat])
            self.assertTrue(seat_config["fresh_chat_marker_required"])
            self.assertFalse(seat_config["ultra_compact"])
            self.assertNotIn("JSON schema", question)
            if seat == "grok":
                self.assertTrue(seat_config["compact_line_receipt"])
                self.assertIn("answer_contract: compact_line_receipt", question)
                self.assertIn("model_account=xai", question)
                self.assertIn("seat_id=grok", question)
                self.assertIn("PRED_INVEST_RECEIPT", question)
                self.assertNotIn("[AIJUDGE_DEALER_PACKET_GROK_ULTRA]", question)
                self.assertGreaterEqual(seat_policy["timeout_seconds"], 900)
            else:
                self.assertTrue(seat_config["compact_line_receipt"])
                self.assertIn("answer_contract: compact_line_receipt", question)
                self.assertIn("model_account=mimo", question)
                self.assertIn("seat_id=mimo", question)
                self.assertNotIn('"forecasts"', question)
            self.assertTrue(seat_policy["execution_required"])
            self.assertFalse(seat_policy["best_effort"])
            self.assertFalse(seat_policy["exclude_from_publish_gate"])
            self.assertTrue(seat_policy["force_fresh_conversation"])
            self.assertTrue(seat_policy["disable_existing_answer_recovery"])
            self.assertTrue(seat_policy["force_keyboard_submit"])
            self.assertGreaterEqual(seat_policy["timeout_seconds"], 540)


if __name__ == "__main__":
    unittest.main()
