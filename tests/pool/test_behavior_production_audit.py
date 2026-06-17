import unittest

from ops.pool.audit.behavior_audit_engine import run_behavior_production_audit as run_engine_audit
from ops.pool.audit.causality_graph_builder import build_causality_graph
from ops.pool.audit.decision_tracer import audit_causal_trace_chains, audit_decision, audit_prompt_memory
from ops.pool.audit.pattern_influence_checker import audit_pattern_removal_sensitivity, trace_pattern_influence, verify_pattern_influence
from ops.pool.audit.replay_validator import validate_replay
from ops.pool.behavior_audit import run_behavior_production_audit
from ops.pool.paths import DATA_ROOT


class BehaviorProductionAuditTest(unittest.TestCase):
    def tearDown(self):
        (DATA_ROOT / "behavior_audits" / "unit-audit-modules.causality_graph.json").unlink(missing_ok=True)

    def test_run15_production_audit_contract(self):
        audit = run_behavior_production_audit("run-15")

        self.assertEqual(audit["version"], "behavior_production_audit.v1")
        self.assertEqual(audit["run_id"], "run-15")
        self.assertIn(audit["status"]["verdict"], {"PRODUCTION_READY", "PARTIAL_PRODUCTION_READY"})
        self.assertIn("prompt_memory", audit["sections"])
        self.assertIn("replay", audit["sections"])
        self.assertIn("influence", audit["sections"])
        self.assertIn("pattern_removal", audit["sections"])
        self.assertIn("causal_trace", audit["sections"])
        self.assertIn("credit_loan", audit["sections"])
        self.assertEqual(audit["sections"]["prompt_memory"]["status"], "pass")
        self.assertEqual(audit["sections"]["replay"]["status"], "pass")
        self.assertIn(audit["sections"]["influence"]["status"], {"pass", "partial"})
        self.assertIn(audit["sections"]["pattern_removal"]["status"], {"pass", "partial"})
        self.assertEqual(audit["sections"]["causal_trace"]["status"], "pass")
        self.assertIn(audit["sections"]["credit_loan"]["status"], {"pass", "partial"})
        self.assertGreater(audit["causality_graph"]["node_count"], 0)
        self.assertGreater(audit["causality_graph"]["edge_count"], 0)

    def test_run15_prompt_context_requires_memory_receipt_fields(self):
        audit = run_behavior_production_audit("run-15")
        prompt_rows = audit["sections"]["prompt_memory"]["rows"]

        self.assertGreaterEqual(len(prompt_rows), 12)
        self.assertTrue(all(row["has_behavior_memory"] for row in prompt_rows))
        self.assertTrue(all(row["must_consider_memory"] for row in prompt_rows))
        self.assertTrue(all(row["required_fields_present"] for row in prompt_rows))

    def test_final_audit_modules_are_directly_callable(self):
        seat_ids = ["deepseek", "gemini"]
        prompt = audit_prompt_memory("run-15", seat_ids)
        replay = validate_replay("run-15")
        influence = trace_pattern_influence("run-15", seat_ids)
        removal = audit_pattern_removal_sensitivity("run-15", seat_ids)
        causal_trace = audit_causal_trace_chains("run-15", seat_ids)
        credit = run_engine_audit("run-15", seat_ids)["sections"]["credit_loan"]
        graph = build_causality_graph("unit-audit-modules", influence, credit)

        self.assertEqual(prompt["status"], "pass")
        self.assertEqual(replay["status"], "pass")
        self.assertIn(influence["status"], {"pass", "partial"})
        self.assertIn(removal["status"], {"pass", "partial"})
        self.assertEqual(causal_trace["status"], "pass")
        self.assertGreater(graph["node_count"], 0)
        self.assertGreater(graph["edge_count"], 0)

    def test_decision_trace_and_pattern_influence_contract(self):
        event = {
            "event_id": "E1",
            "event_type": "investment_recorded",
            "action": "investment_recorded",
            "risk_shift": "higher_risk",
            "state_before": {"risk_level": "medium"},
            "state_after": {"risk_level": "high"},
            "decision_reconstruction": {
                "memory_summary": {
                    "memory_used": True,
                    "dominant_pattern": "loan_pressure_shapes_risk",
                    "active_patterns": ["loan_pressure_shapes_risk"],
                }
            },
        }

        decision = audit_decision("deepseek", event)
        influence = verify_pattern_influence("loan_pressure_shapes_risk", event)

        self.assertTrue(decision["memory_influence"])
        self.assertIn("loan_pressure_shapes_risk", decision["used_patterns"])
        self.assertTrue(decision["risk_alignment"]["changed"])
        self.assertTrue(influence["influenced"])
        self.assertGreater(influence["strength"], 0)


if __name__ == "__main__":
    unittest.main()
