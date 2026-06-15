import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import audit_pred_invest_product_health
import pred_invest_quality_gate


class PredInvestResidualRiskTest(unittest.TestCase):
    def test_proxy_health_uses_nc_when_python_socket_is_sandboxed(self):
        completed = SimpleNamespace(returncode=0, stdout="", stderr="Connection to 127.0.0.1 port 7897 succeeded!")
        with patch.dict(os.environ, {"HTTP_PROXY": "http://127.0.0.1:7897"}, clear=True):
            with patch("socket.create_connection", side_effect=PermissionError(1, "Operation not permitted")):
                with patch("shutil.which", return_value="/usr/bin/nc"):
                    with patch("subprocess.run", return_value=completed) as run:
                        health = audit_pred_invest_product_health.proxy_health()
        self.assertTrue(health["configured"])
        self.assertTrue(health["ok"])
        self.assertTrue(health["diagnostic_only"])
        self.assertEqual(health["checks"][0]["reachable_via"], "nc_probe_after_python_socket_sandbox_block")
        run.assert_called_once()

    def test_quality_gate_splits_provider_blocked_from_rerunnable_seats(self):
        fake_audit = {
            "required_match_ids": ["M1"],
            "required_match_source": "test",
            "valid_seats": [seat for seat in pred_invest_quality_gate.REQUIRED_SEATS if seat != "grok"],
            "needs_rerun": ["grok"],
            "seat_results": [
                {
                    "seat": "grok",
                    "valid": False,
                    "issues": ["provider_quota_limited"],
                    "run_id": "42a97c4d0fa9",
                    "response_chars": 123,
                    "last_errors": [
                        {
                            "run_id": "42a97c4d0fa9",
                            "action": "seat_timeout",
                            "reason": "slow_response_pending",
                            "response_chars": 123,
                        }
                    ],
                }
            ],
        }
        with patch("pred_invest_quality_gate.bridge_audit.audit", return_value=fake_audit):
            with patch("pred_invest_quality_gate._load_json", return_value={"models": 12, "match_count": 1}):
                gate = pred_invest_quality_gate.build_gate("2026-06-15", "run-15", ["42a97c4d0fa9"])
        self.assertFalse(gate["publish_allowed"])
        self.assertEqual(gate["provider_blocked_seats"], ["grok"])
        self.assertEqual(gate["rerunnable_seats"], [])
        self.assertEqual(gate["rerun_queue"][0]["mode"], "provider_quota_blocked")


if __name__ == "__main__":
    unittest.main()
