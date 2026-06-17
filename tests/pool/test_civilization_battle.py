import unittest

from ops.pool.civilization_battle import build_civilization_battle


class CivilizationBattleTest(unittest.TestCase):
    def test_builds_civilizations_interactions_and_headline_battle(self):
        agents = []
        for index in range(4):
            agents.append({
                "seat_id": f"safe-{index}",
                "behavior_type": "discipline_first_observer",
                "archetype": "Survival Optimizer",
                "risk_level": "low",
                "loan_dependency": "low",
                "no_bet_rate": 0.8,
                "total_stake_gp": 100,
                "settlement_profit_gp": 0,
                "top_patterns": [{"name": "uncertainty_to_no_bet", "label": "uncertainty → no-bet", "confidence": 0.8, "supporting_events": 1}],
            })
        for index in range(4):
            agents.append({
                "seat_id": f"risk-{index}",
                "behavior_type": "aggressive_edge_hunter",
                "archetype": "Risk Explorer",
                "risk_level": "high",
                "loan_dependency": "medium",
                "no_bet_rate": 0.1,
                "total_stake_gp": 900,
                "settlement_profit_gp": -100,
                "top_patterns": [{"name": "loan_pressure_shapes_risk", "label": "loan → risk constraint", "confidence": 0.75, "supporting_events": 2}],
            })
        for index in range(4):
            agents.append({
                "seat_id": f"adapt-{index}",
                "behavior_type": "selective_allocator",
                "archetype": "Balanced Adapter",
                "risk_level": "medium",
                "loan_dependency": "low",
                "no_bet_rate": 0.35,
                "total_stake_gp": 400,
                "settlement_profit_gp": 40,
                "top_patterns": [{"name": "capital_to_selective_allocation", "label": "capital → selective allocation", "confidence": 0.7, "supporting_events": 1}],
            })

        battle = build_civilization_battle(
            run_id="run-battle",
            civilization_state={"run_id": "run-battle", "agents": agents, "behavior_flow": []},
            write=False,
        )

        self.assertEqual(battle["version"], "civilization_battle.v9")
        self.assertEqual(len(battle["civilizations"]), 3)
        self.assertEqual(len(battle["interactions"]), 3)
        self.assertTrue(battle["headline_battle"])
        self.assertEqual(battle["engine"]["version"], "multiverse_civilization_physics_engine.v1")
        self.assertEqual(len(battle["civilization_models"]), 3)
        self.assertEqual(len(battle["interaction_graph"]["nodes"]), 3)
        self.assertEqual(len(battle["interaction_graph"]["edges"]), 3)
        self.assertEqual(len(battle["clash_view"]), 3)
        self.assertEqual(len(battle["civilization_timeline"]), 3)
        self.assertEqual(len(battle["collapse_signals"]), 3)
        self.assertEqual(battle["dynamics"]["version"], "civilization_dynamics.v7")
        self.assertEqual(len(battle["dynamics"]["state_vectors"]), 3)
        self.assertEqual(len(battle["dynamics"]["collapse_predictor"]["predictions"]), 3)
        self.assertEqual(len(battle["dynamics"]["evolution_engine"]["predictions"]), 3)
        self.assertEqual(len(battle["dynamics"]["competition_model"]["comparisons"]), 3)
        self.assertEqual(len(battle["dynamics"]["phase_transition_engine"]["phases"]), 3)
        self.assertEqual(len(battle["dynamics"]["civilization_field"]["nodes"]), 3)
        self.assertEqual(len(battle["dynamics"]["war_engine"]["battles"]), 3)
        self.assertEqual(len(battle["dynamics"]["war_phase_engine"]["triggers"]), 3)
        self.assertEqual(len(battle["dynamics"]["meta_layer"]["laws"]), 3)
        self.assertEqual(len(battle["dynamics"]["memory_dynamics_engine"]["civilizations"]), 3)
        self.assertEqual(battle["dynamics"]["meta_civilization_layer"]["version"], "meta_civilization_engine.v1")
        self.assertEqual(battle["dynamics"]["genome_engine"]["version"], "civilization_genome_engine.v1")
        self.assertEqual(battle["dynamics"]["universe_engine"]["version"], "universe_engine.v1")
        self.assertEqual(battle["dynamics"]["multiverse_engine"]["version"], "multiverse_engine.v1")
        self.assertEqual(battle["dynamics"]["physics_core"]["system_status"], "PRODUCTION_READY_MULTIVERSE_CIVILIZATION_PHYSICS_ENGINE")
        self.assertEqual(battle["phase_transitions"]["version"], "phase_transition_engine.v1")
        self.assertEqual(battle["civilization_field"]["version"], "civilization_field_engine.v1")
        self.assertEqual(battle["war_engine"]["version"], "civilization_war_engine.v1")
        self.assertEqual(battle["war_phase_engine"]["version"], "war_phase_engine.v1")
        self.assertEqual(battle["meta_layer"]["version"], "civilization_meta_layer.v1")
        self.assertEqual(battle["memory_dynamics"]["version"], "memory_dynamics_engine.v1")
        self.assertEqual(battle["meta_civilization"]["version"], "meta_civilization_engine.v1")
        self.assertTrue(battle["meta_civilization"]["clusters"])
        self.assertTrue(battle["meta_civilization"]["systemic_collapse_wave"])
        self.assertEqual(battle["genome_engine"]["version"], "civilization_genome_engine.v1")
        self.assertTrue(battle["genome_engine"]["civilizations"])
        self.assertEqual(battle["universe"]["version"], "universe_engine.v1")
        self.assertTrue(battle["universe"]["nodes"])
        self.assertTrue(battle["universe"]["evolution_tree"])
        self.assertEqual(battle["multiverse"]["version"], "multiverse_engine.v1")
        self.assertTrue(battle["multiverse"]["nodes"])
        self.assertTrue(battle["multiverse"]["couplings"])
        self.assertTrue(battle["multiverse"]["dominance_cluster"])
        self.assertEqual(battle["physics_core"]["version"], "civilization_physics_core.v4")
        self.assertEqual(len(battle["fate_curve"]), 3)
        self.assertTrue(battle["meta_strategy"]["reading"])
        self.assertEqual(battle["map_contract"]["primary_ui_extension"], "civilization_vs_civilization")
        self.assertEqual(battle["map_contract"]["primary_ui"], "multiverse_civilization_map_v9")
        self.assertTrue(battle["map_contract"]["show_fate_curve"])
        self.assertTrue(battle["map_contract"]["show_phase_transition"])
        self.assertTrue(battle["map_contract"]["show_war_map"])
        self.assertTrue(battle["map_contract"]["show_meta_layer"])
        self.assertTrue(battle["map_contract"]["show_phase_law"])
        self.assertTrue(battle["map_contract"]["show_memory_dynamics"])
        self.assertTrue(battle["map_contract"]["show_physics_core"])
        self.assertTrue(battle["map_contract"]["show_meta_civilization_layer"])
        self.assertTrue(battle["map_contract"]["show_genome_layer"])
        self.assertTrue(battle["map_contract"]["show_universe_layer"])
        self.assertTrue(battle["map_contract"]["show_multiverse_layer"])
        self.assertTrue(all(row["shared_memory"] for row in battle["civilizations"]))


if __name__ == "__main__":
    unittest.main()
