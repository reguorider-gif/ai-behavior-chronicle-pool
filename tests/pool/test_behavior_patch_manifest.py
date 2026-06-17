import shutil
import unittest

from ops.pool.behavior import build_graph, compile_patterns, compile_state, inject_behavior, log_event, write_trace
from ops.pool.behavior_production_kernel import KERNEL_VERSION
from ops.pool.paths import DATA_ROOT


class BehaviorPatchManifestTest(unittest.TestCase):
    def tearDown(self):
        for path in [
            DATA_ROOT / "seat_journals" / "unit_manifest",
            DATA_ROOT / "behavior" / "events" / "unit_manifest.jsonl",
            DATA_ROOT / "behavior" / "compiled" / "unit_manifest.json",
            DATA_ROOT / "behavior" / "patterns" / "unit_manifest.json",
            DATA_ROOT / "behavior_memory" / "compiled" / "unit_manifest.json",
            DATA_ROOT / "behavior_patterns" / "unit_manifest.json",
            DATA_ROOT / "replay" / "runs" / "unit-manifest-run.json",
            DATA_ROOT / "behavior" / "traces" / "unit-manifest-run.json",
        ]:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)

    def test_manifest_modules_form_behavior_loop(self):
        seat_id = "unit_manifest"
        run_id = "unit-manifest-run"
        log_event(seat_id, run_id, {
            "event_type": "investment_recorded",
            "investments": [
                {"match_id": "M1", "action": "bet", "stake_gp": 420, "loan_used_gp": 120},
                {"match_id": "M2", "action": "no_bet", "stake_gp": 0, "loan_used_gp": 0},
            ],
        })
        log_event(seat_id, run_id, {
            "event_type": "settlement_recorded",
            "settlement": {"profit_gp": -90},
        })

        state = compile_state(seat_id, write=True)
        patterns = compile_patterns(seat_id, write=True)
        context = inject_behavior({"private_context": {}, "public_context": {"output_contract": {}}}, seat_id)
        graph = build_graph([seat_id], run_id=run_id, write=False)
        trace = write_trace(run_id, [seat_id], write=False)

        self.assertEqual(context["behavior_kernel_version"], KERNEL_VERSION)
        self.assertGreaterEqual(state["event_count"], 2)
        self.assertTrue(patterns)
        self.assertTrue(context["private_context"]["behavior_kernel"]["active_patterns"])
        self.assertTrue(graph["top_patterns"])
        self.assertGreaterEqual(trace["event_count"], 2)

    def test_history_change_changes_injected_memory(self):
        seat_id = "unit_manifest"
        before = inject_behavior({"private_context": {}, "public_context": {"output_contract": {}}}, seat_id)
        before_patterns = [row["name"] for row in before["private_context"]["behavior_kernel"]["active_patterns"]]

        log_event(seat_id, "unit-manifest-run", {
            "event_type": "investment_recorded",
            "investments": [{"match_id": "M1", "action": "bet", "stake_gp": 500, "loan_used_gp": 250}],
        })
        after = inject_behavior({"private_context": {}, "public_context": {"output_contract": {}}}, seat_id)
        after_patterns = [row["name"] for row in after["private_context"]["behavior_kernel"]["active_patterns"]]

        self.assertNotEqual(before_patterns, after_patterns)
        self.assertIn("loan_pressure_shapes_risk", after_patterns)


if __name__ == "__main__":
    unittest.main()
