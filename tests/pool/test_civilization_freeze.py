import unittest

from ops.pool.civilization_freeze import (
    ENGINE_VERSION,
    READY_STATUS,
    build_civilization_freeze_manifest,
)
from ops.pool.seat_registry import REQUIRED_SEAT_COUNT


class CivilizationFreezeTest(unittest.TestCase):
    def test_freeze_manifest_requires_kernel_audit_replay_and_map_evidence(self):
        production = {
            "kernel_version": "behavior_kernel_v1",
            "append_only_event_sourcing": True,
            "deterministic_replay": True,
            "memory_isolation": True,
            "readiness": {
                "ok": True,
                "event_sourcing": "pass",
                "replay": "pass",
                "memory_isolation": "pass",
            },
        }
        audit = {
            "status": {
                "verdict": "PRODUCTION_READY",
                "passed": 8,
                "partial": 0,
                "checks": {
                    "prompt_control": "pass",
                    "pattern_participates": "pass",
                    "pattern_removal_changes_behavior": "pass",
                    "deterministic_replay": "pass",
                    "causal_trace_complete": "pass",
                },
            },
            "causality_graph": {"edge_count": 3},
        }
        civilization = {
            "run_id": "run-freeze",
            "agents": [{"seat_id": f"seat-{index}"} for index in range(REQUIRED_SEAT_COUNT)],
            "causality": {"edges": [{"cause": "loss", "effect": "risk_review"}]},
            "map_contract": {"primary_ui": "civilization_map"},
        }
        battle = {
            "civilizations": [{"id": "stable"}, {"id": "risk"}],
            "interactions": [{"id": "stable__vs__risk"}],
            "map_contract": {"primary_ui_extension": "civilization_vs_civilization"},
        }

        manifest = build_civilization_freeze_manifest(
            "run-freeze",
            production_contract=production,
            production_audit=audit,
            civilization_state=civilization,
            civilization_battle=battle,
            write=False,
        )

        self.assertTrue(manifest["ready"])
        self.assertEqual(manifest["engine_version"], ENGINE_VERSION)
        self.assertEqual(manifest["final_status"], READY_STATUS)
        self.assertEqual(manifest["system_definition"], "Behavior Civilization Simulation System")
        self.assertEqual(manifest["final_loop"][0], "event")
        self.assertEqual(manifest["final_loop"][-1], "next_run")
        self.assertEqual(len(manifest["architecture_layers"]), 6)
        self.assertTrue(manifest["evidence"]["memory_influences_decision"]["ok"])
        self.assertTrue(manifest["evidence"]["pattern_influences_behavior"]["ok"])
        self.assertTrue(manifest["evidence"]["multi_civilization_layer"]["ok"])
        self.assertEqual(manifest["public_surface_policy"]["primary_surface"], "civilization_map")


if __name__ == "__main__":
    unittest.main()
