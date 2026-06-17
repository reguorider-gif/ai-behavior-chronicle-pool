import unittest

from ops.pool.civilization_state import build_civilization_state


class CivilizationStateTest(unittest.TestCase):
    def test_builds_pressure_space_flow_and_causality(self):
        agent_profiles = {
            "seats": {
                "alpha": {
                    "seat_id": "alpha",
                    "behavior_type": "aggressive_edge_hunter",
                    "risk_level": "high",
                    "loan_dependency": "medium",
                    "no_bet_rate": 0.2,
                    "strategy_drift": "aggressive_shift",
                    "total_stake_gp": 900,
                    "total_loan_used_gp": 300,
                    "settlement_profit_gp": -120,
                    "top_patterns": [{"name": "loan_pressure_shapes_risk"}],
                },
                "beta": {
                    "seat_id": "beta",
                    "behavior_type": "discipline_first_observer",
                    "risk_level": "low",
                    "loan_dependency": "low",
                    "no_bet_rate": 0.8,
                    "strategy_drift": "risk_reduction",
                    "total_stake_gp": 0,
                    "total_loan_used_gp": 0,
                    "settlement_profit_gp": 0,
                    "top_patterns": [{"name": "uncertainty_to_no_bet"}],
                },
            }
        }
        pattern_graph = {
            "top_patterns": [
                {
                    "name": "loan_pressure_shapes_risk",
                    "label": "loan → risk constraint",
                    "confidence": 0.8,
                    "supporting_events": 3,
                    "source_event_ids": ["run-x:credit_updated:1"],
                    "seats": ["alpha"],
                }
            ]
        }
        evolution_trace = {
            "traces": [
                {
                    "seat_id": "alpha",
                    "run_id": "run-x",
                    "behavior_type": "aggressive_edge_hunter",
                    "risk_level": "high",
                    "loan_dependency": "medium",
                    "strategy_drift": "aggressive_shift",
                    "dominant_pattern": "loan_pressure_shapes_risk",
                    "decision_pressure": {
                        "no_bet_rate": 0.2,
                        "total_stake_gp": 900,
                        "settlement_profit_gp": -120,
                        "recovery_mode": False,
                    },
                }
            ]
        }

        state = build_civilization_state(
            run_id="run-x",
            agent_profiles=agent_profiles,
            pattern_graph=pattern_graph,
            evolution_trace=evolution_trace,
            write=False,
        )

        self.assertEqual(state["version"], "civilization_state.v1")
        self.assertEqual(len(state["agents"]), 2)
        self.assertIn("alpha", state["positions"])
        self.assertIn("credit_pressure", state["pressure"])
        self.assertEqual(state["causality"]["edges"][0]["cause"], "loan")
        self.assertEqual(state["causality"]["edges"][0]["effect"], "risk constraint")
        self.assertTrue(state["map_contract"]["show_behavior_structure_not_raw_data"])


if __name__ == "__main__":
    unittest.main()
