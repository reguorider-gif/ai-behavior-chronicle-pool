import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class PipelineSmokeBehaviorMemoryTest(unittest.TestCase):
    def setUp(self):
        self._latest_paths = [
            ROOT / "data" / "pool" / "behavior_summary" / "latest.json",
            ROOT / "data" / "pool" / "behavior_summary" / "latest.md",
        ]
        self._backups = []
        for path in self._latest_paths:
            backup = path.with_suffix(path.suffix + ".test-backup")
            if path.exists():
                shutil.copy2(path, backup)
                self._backups.append((path, backup))

    def tearDown(self):
        for path, backup in self._backups:
            if backup.exists():
                shutil.copy2(backup, path)
                backup.unlink()

    def _run(self, run_id: str):
        cmd = [
            sys.executable,
            "ops/run_daily_pool_pipeline.py",
            "--date", "2026-06-15",
            "--round", run_id,
            "--odds-provider", "fixture",
            "--rule-version", "PRED_INVEST_CREDIT_SURVIVE_V2",
            "--with-behavior-memory",
            "--require-forecast",
            "--allow-no-bet",
            "--build-market-snapshot",
            "--write-god-ledger",
            "--write-seat-journals",
            "--smoke",
        ]
        proc = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
        return json.loads(proc.stdout)

    def test_a_then_b_preserves_behavior_memory(self):
        a = self._run("smoke-behavior-v2-a")
        self.assertTrue(a["ok"], a)
        self.assertEqual(a["forecast_receipt_count"], 3)
        self.assertEqual(a["investment_receipt_count"], 3)
        b = self._run("smoke-behavior-v2-b")
        self.assertTrue(b["ok"], b)
        context_path = ROOT / "data" / "pool" / "prompt_contexts" / "smoke-behavior-v2-b" / "alpha.json"
        context = json.loads(context_path.read_text(encoding="utf-8"))
        runs_seen = context["private_context"]["own_behavior_summary"]["runs_seen"]
        self.assertIn("smoke-behavior-v2-a", runs_seen)
        self.assertIn("behavior_kernel", context["private_context"])
        self.assertTrue(context["private_context"]["behavior_kernel"]["decision_contract"]["must_consider_memory"])
        report_path = ROOT / "data" / "pool" / "god_reports" / "2026-06-15_smoke-behavior-v2-b.md"
        report = report_path.read_text(encoding="utf-8")
        self.assertIn("预测-投资偏离", report)
        self.assertIn("贷款压力", report)
        behavior_path = ROOT / "data" / "pool" / "behavior_summary" / "2026-06-15_smoke-behavior-v2-b.json"
        behavior = json.loads(behavior_path.read_text(encoding="utf-8"))
        self.assertEqual(behavior["rule_version"], "PRED_INVEST_CREDIT_SURVIVE_V2")
        self.assertEqual(behavior["run_id"], "smoke-behavior-v2-b")
        self.assertTrue(behavior["separation"]["forecast_and_investment_are_separate"])
        self.assertTrue(behavior["readiness"]["god_report_v2_generated"])
        self.assertIn("行为日志：可查看", behavior["public_frontend_contract"]["seat_journal_label"])
        self.assertIn("预测/投资分账：可查看", behavior["public_frontend_contract"]["forecast_investment_label"])


if __name__ == "__main__":
    unittest.main()
