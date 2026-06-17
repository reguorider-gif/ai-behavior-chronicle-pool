import unittest

from ops.pool.civilization_competitor import compete_civilizations
from ops.pool.civilization_field_engine import compute_field
from ops.pool.civilization_state_engine import compute_states
from ops.pool.civilization_war_engine import simulate_civilization_wars
from ops.pool.collapse_predictor import predict_collapses
from ops.pool.evolution_engine import predict_evolutions
from ops.pool.phase_transition_engine import detect_phase_transitions
from ops.pool.war_phase_engine import build_war_phase_triggers
from ops.pool.civilization_meta_layer import build_civilization_meta_layer
from ops.pool.memory_dynamics_engine import build_memory_dynamics
from ops.pool.civilization_physics_core import build_civilization_physics_core
from ops.pool.meta_civilization_engine import build_meta_civilization_physics
from ops.pool.civilization_genome_engine import build_civilization_genomes
from ops.pool.universe_engine import build_universe_engine
from ops.pool.multiverse_engine import build_multiverse_engine


class CivilizationDynamicsTest(unittest.TestCase):
    def sample_civilizations(self):
        return [
            {
                "id": "stable",
                "zh_name": "稳定文明",
                "agents": ["a", "b"],
                "shared_memory": [{"confidence": 0.8}],
                "shared_risk_profile": {"risk_score": 0.2, "loan_score": 0.1, "no_bet_rate": 0.7},
                "performance": {"survival_score": 0.9, "stability_score": 0.84, "volatility_score": 0.2, "roi": 0.03},
            },
            {
                "id": "volatile",
                "zh_name": "波动文明",
                "agents": ["c", "d"],
                "shared_memory": [{"confidence": 0.45}, {"confidence": 0.4}],
                "shared_risk_profile": {"risk_score": 0.86, "loan_score": 0.78, "no_bet_rate": 0.08},
                "performance": {"survival_score": 0.34, "stability_score": 0.22, "volatility_score": 0.88, "roi": -0.2},
            },
        ]

    def test_state_collapse_evolution_and_competition_are_linked(self):
        states = compute_states(
            self.sample_civilizations(),
            {"civilizations": [
                {"civilization_id": "stable", "drift_rate": 0.0},
                {"civilization_id": "volatile", "drift_rate": 0.8},
            ]},
        )
        collapses = predict_collapses(states)
        evolutions = predict_evolutions(states, collapses["predictions"])
        competition = compete_civilizations(states, collapses["predictions"], evolutions["predictions"])
        phases = detect_phase_transitions(states, collapses["predictions"], evolutions["predictions"])
        field = compute_field(phases["phases"])
        war = simulate_civilization_wars(phases["phases"])
        war_phase = build_war_phase_triggers(phases["phases"], war["battles"])
        meta = build_civilization_meta_layer(phases["phases"], war_phase)
        memory = build_memory_dynamics(self.sample_civilizations(), phases["phases"], meta)
        genome = build_civilization_genomes(self.sample_civilizations(), phases["phases"], memory)
        meta_civilization = build_meta_civilization_physics(
            phase_rows=phases["phases"],
            war_engine=war,
            collapse_predictor=collapses,
            memory_dynamics=memory,
        )
        universe = build_universe_engine(
            phase_rows=phases["phases"],
            genome_engine=genome,
            meta_civilization=meta_civilization,
        )
        multiverse = build_multiverse_engine(
            universe=universe,
            meta_civilization=meta_civilization,
            memory_dynamics=memory,
        )
        physics = build_civilization_physics_core({
            "state_vectors": states,
            "phase_transition_engine": phases,
            "war_engine": war,
            "collapse_predictor": collapses,
            "memory_dynamics_engine": memory,
            "meta_layer": meta,
            "meta_civilization_layer": meta_civilization,
            "genome_engine": genome,
            "universe_engine": universe,
            "multiverse_engine": multiverse,
        })

        self.assertEqual(len(states), 2)
        self.assertEqual(collapses["version"], "collapse_predictor.v1")
        self.assertEqual(len(collapses["fate_curve"]), 2)
        self.assertEqual(evolutions["version"], "evolution_engine.v1")
        self.assertTrue(evolutions["phase_transition_watch"])
        self.assertEqual(competition["version"], "civilization_competitor.v1")
        self.assertEqual(len(competition["comparisons"]), 1)
        self.assertEqual(competition["long_term_winner"], "stable")
        self.assertEqual(phases["version"], "phase_transition_engine.v1")
        self.assertEqual(len(phases["phases"]), 2)
        self.assertGreaterEqual(phases["critical_count"], 1)
        self.assertEqual(field["version"], "civilization_field_engine.v1")
        self.assertEqual(len(field["nodes"]), 2)
        self.assertEqual(war["version"], "civilization_war_engine.v1")
        self.assertEqual(len(war["battles"]), 1)
        self.assertIn(war["headline_war"]["war_type"], {"resource_war", "stability_war", "strategy_war", "collapse_war"})
        self.assertEqual(war_phase["version"], "war_phase_engine.v1")
        self.assertEqual(len(war_phase["triggers"]), 1)
        self.assertEqual(meta["version"], "civilization_meta_layer.v1")
        self.assertEqual(len(meta["laws"]), 2)
        self.assertTrue(meta["why_phase_changes"])
        self.assertEqual(memory["version"], "memory_dynamics_engine.v1")
        self.assertEqual(len(memory["civilizations"]), 2)
        self.assertTrue(memory["injection_contract"]["private_memory_only"])
        self.assertEqual(meta_civilization["version"], "meta_civilization_engine.v1")
        self.assertTrue(meta_civilization["clusters"])
        self.assertTrue(meta_civilization["migration_paths"])
        self.assertEqual(genome["version"], "civilization_genome_engine.v1")
        self.assertEqual(len(genome["civilizations"]), 2)
        self.assertEqual(universe["version"], "universe_engine.v1")
        self.assertTrue(universe["nodes"])
        self.assertTrue(universe["evolution_tree"])
        self.assertEqual(multiverse["version"], "multiverse_engine.v1")
        self.assertTrue(multiverse["couplings"])
        self.assertTrue(multiverse["memory_field"])
        self.assertEqual(physics["version"], "civilization_physics_core.v4")
        self.assertTrue(physics["ready"])
        self.assertEqual(physics["system_status"], "PRODUCTION_READY_MULTIVERSE_CIVILIZATION_PHYSICS_ENGINE")
        self.assertTrue(physics["production_lock"]["meta_civilization_integrated"])
        self.assertTrue(physics["production_lock"]["genome_integrated"])
        self.assertTrue(physics["production_lock"]["universe_field_integrated"])
        self.assertTrue(physics["production_lock"]["multiverse_integrated"])


if __name__ == "__main__":
    unittest.main()
