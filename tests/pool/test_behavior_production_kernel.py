import shutil
import tempfile
import unittest
from pathlib import Path

from ops.pool.behavior_production_kernel import (
    KERNEL_VERSION,
    _append_immutable_event,
    behavior_kernel_definition,
    memory_isolation_audit,
)
from ops.pool.io_utils import write_json
from ops.pool.paths import DATA_ROOT


class BehaviorProductionKernelTest(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(DATA_ROOT / "prompt_contexts" / "unit-production-run", ignore_errors=True)
        for path in [
            DATA_ROOT / "data_lake" / "runs" / "unit-production-run.memory_isolation.json",
        ]:
            path.unlink(missing_ok=True)

    def test_kernel_definition_is_versioned_and_stably_hashed(self):
        first = behavior_kernel_definition()
        second = behavior_kernel_definition()

        self.assertEqual(first["version"], KERNEL_VERSION)
        self.assertEqual(first["kernel_hash"], second["kernel_hash"])
        self.assertEqual(first["event_sourcing"]["mode"], "append_only")
        self.assertEqual(first["memory_policy"]["agent_private_memory"], "own_history_only")

    def test_append_only_event_rejects_conflicting_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            event = {"event_id": "E1", "event_hash": "H1", "payload": {"x": 1}}
            duplicate = {"event_id": "E1", "event_hash": "H1", "payload": {"x": 1}}
            conflict = {"event_id": "E1", "event_hash": "H2", "payload": {"x": 2}}

            self.assertTrue(_append_immutable_event(path, event))
            self.assertFalse(_append_immutable_event(path, duplicate))
            with self.assertRaises(ValueError):
                _append_immutable_event(path, conflict)

    def test_memory_isolation_audit_accepts_own_history_only(self):
        run_id = "unit-production-run"
        write_json(DATA_ROOT / "prompt_contexts" / run_id / "alpha.json", {
            "private_context": {
                "own_account": {"seat_id": "alpha", "balance_gp": 1000},
                "behavior_kernel": {"profile": {"behavior_type": "balanced"}},
            },
            "public_context": {"anonymous_market_snapshot": {"matches": []}},
        })
        write_json(DATA_ROOT / "prompt_contexts" / run_id / "beta.json", {
            "private_context": {
                "own_account": {"seat_id": "beta", "balance_gp": 1000},
                "behavior_kernel": {"profile": {"behavior_type": "guarded"}},
            },
            "public_context": {"anonymous_market_snapshot": {"matches": []}},
        })

        audit = memory_isolation_audit(run_id, ["alpha", "beta"])

        self.assertTrue(audit["ok"], audit)
        self.assertEqual(audit["checked_prompt_contexts"], 2)


if __name__ == "__main__":
    unittest.main()
