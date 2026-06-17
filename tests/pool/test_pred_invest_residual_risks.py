import os
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops"))

import audit_pred_invest_product_health
import pred_invest_quality_gate
import verify_vercel_live_endpoint


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
            with patch("pred_invest_quality_gate._load_json", return_value={"models": len(pred_invest_quality_gate.REQUIRED_SEATS), "match_count": 1}):
                gate = pred_invest_quality_gate.build_gate("2026-06-15", "run-15", ["42a97c4d0fa9"])
        self.assertFalse(gate["publish_allowed"])
        self.assertEqual(gate["provider_blocked_seats"], ["grok"])
        self.assertEqual(gate["rerunnable_seats"], [])
        self.assertEqual(gate["rerun_queue"][0]["mode"], "provider_quota_blocked")

    def test_vercel_live_verifier_classifies_proxy_success_as_local_network_issue(self):
        direct = {
            "ok": False,
            "returncode": 28,
            "http_status": None,
            "resolved_ips": ["108.160.169.54"],
        }
        proxied = {
            "ok": True,
            "returncode": 0,
            "http_status": 200,
            "server": "Vercel",
            "x_vercel_id": "iad1::unit",
            "json_summary": {"date": "2026-06-16", "round_id": "run-16"},
        }
        with patch("verify_vercel_live_endpoint.run_curl", side_effect=[direct, proxied]):
            report = verify_vercel_live_endpoint.verify("https://pool-app-live-repair.vercel.app/test.json")
        self.assertEqual(report["verdict"], "READY_VIA_PROXY_LOCAL_DNS_OR_ROUTE_ISSUE")
        self.assertIn("direct_curl_failed_but_proxy_curl_succeeded", report["warnings"])
        self.assertEqual(report["proxy_result"]["server"], "Vercel")

    def test_vercel_live_verifier_does_not_mark_codex_sandbox_as_deploy_failure(self):
        direct = {"ok": False, "returncode": 6, "stderr_tail": "Could not resolve host"}
        proxied = {"ok": False, "returncode": 7, "stderr_tail": "Operation not permitted"}
        with patch.dict(os.environ, {"CODEX_SANDBOX_NETWORK_DISABLED": "1"}, clear=True):
            with patch("verify_vercel_live_endpoint.run_curl", side_effect=[direct, proxied]):
                report = verify_vercel_live_endpoint.verify("https://pool-app-live-repair.vercel.app/test.json")
        self.assertEqual(report["verdict"], "UNVERIFIED_CODEX_SANDBOX_NETWORK_BLOCKED")
        self.assertIn("python_subprocess_network_blocked_by_codex_sandbox", report["warnings"])

    def test_fresh_score_cache_fallback_is_not_product_health_warning(self):
        meta = {
            "transport": "cache_fallback",
            "ok": True,
            "row_count": 64,
            "cache_mtime": "2026-06-17T14:57:13+00:00",
            "primary_transport_error": "URLError: sandbox DNS blocked",
        }
        warning = audit_pred_invest_product_health.score_cache_warning(
            meta,
            blocking_score_count=0,
            now=datetime(2026, 6, 17, 18, 0, tzinfo=timezone.utc),
        )
        self.assertIsNone(warning)

    def test_stale_score_cache_fallback_remains_product_health_warning(self):
        meta = {
            "transport": "cache_fallback",
            "ok": True,
            "row_count": 64,
            "cache_mtime": "2026-06-17T00:00:00+00:00",
            "primary_transport_error": "URLError: sandbox DNS blocked",
        }
        warning = audit_pred_invest_product_health.score_cache_warning(
            meta,
            blocking_score_count=0,
            now=datetime(2026, 6, 17, 18, 0, tzinfo=timezone.utc),
        )
        self.assertIn("the_odds_api_scores_cache_stale", warning)


if __name__ == "__main__":
    unittest.main()
