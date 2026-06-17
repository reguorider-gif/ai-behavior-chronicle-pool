import json
import subprocess
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PoolMetaV4ContractTest(unittest.TestCase):
    def _call_pool_meta(self) -> dict:
        script = textwrap.dedent(
            """
            const handler = require('./api/pool-meta.js');
            async function call(query) {
              const res = {
                statusCode: 0,
                headers: {},
                body: '',
                setHeader(k, v) { this.headers[k] = v; },
                status(code) { this.statusCode = code; return this; },
                send(body) { this.body = body; return this; },
              };
              await handler({ query }, res);
              return { status: res.statusCode, data: JSON.parse(res.body) };
            }
            (async () => {
              const runtime = await call({ type: 'runtime-summary', round_id: 'run-15', date: '2026-06-15' });
              const journal = await call({ type: 'seat-journal', seatId: 'xunfei' });
              const credit = await call({ type: 'credit', seatId: 'xunfei' });
              const archive = await call({ type: 'seat-archives', runId: 'run-15', seatId: 'xunfei' });
              const frontend = await call({ type: 'frontend-archives' });
              console.log(JSON.stringify({ runtime, journal, credit, archive, frontend }));
            })().catch((error) => {
              console.error(error && error.stack || error);
              process.exit(1);
            });
            """
        )
        result = subprocess.run(
            ["node", "-e", script],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_runtime_summary_uses_ledgers_and_initializes_required_seats(self):
        payload = self._call_pool_meta()
        runtime = payload["runtime"]
        self.assertEqual(runtime["status"], 200)
        summary = runtime["data"]["summary"]
        self.assertEqual(summary["model_count"], 15)
        self.assertGreater(summary["total_pool"], 0)
        self.assertGreater(summary["net_worth_total"], 0)
        self.assertEqual(sorted(summary["initialized_required_seats"]), ["stepfun", "xunfei", "zhipu"])
        ranking = runtime["data"]["current_ranking"]
        self.assertEqual(len(ranking), 15)
        for seat_id in ["xunfei", "stepfun", "zhipu"]:
            row = next(item for item in ranking if item["seat_id"] == seat_id)
            self.assertEqual(row["balance_gp"], 1000)
            self.assertEqual(row["net_worth_gp"], 1000)
            self.assertEqual(row["credit_score"], 600)
            self.assertEqual(row["credit_grade"], "B")

    def test_new_seat_journal_credit_and_archives_are_clickable(self):
        payload = self._call_pool_meta()
        self.assertEqual(payload["journal"]["status"], 200)
        self.assertEqual(payload["journal"]["data"]["events"][0]["event_type"], "account_initialized")
        self.assertEqual(payload["credit"]["status"], 200)
        self.assertEqual(payload["credit"]["data"]["history"][0]["credit_grade"], "B")
        self.assertEqual(payload["archive"]["status"], 200)
        self.assertEqual(payload["archive"]["data"]["state"], "initialized")
        self.assertEqual(payload["frontend"]["status"], 200)
        self.assertGreater(len(payload["frontend"]["data"]["artifacts"]), 0)

    def test_pool_api_never_defaults_to_production_self_proxy(self):
        for rel in ["api/pool-meta.js", "api/pool/[...path].js"]:
            source = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn('|| "https://pool-app-one.vercel.app"', source)
            self.assertIn('process.env.POOL_FALLBACK_ORIGIN || ""', source)

    def test_missing_receipt_credit_delta_is_rule_driven(self):
        rules = json.loads((ROOT / "data/pool/rules/PRED_INVEST_CREDIT_SURVIVE_V2.json").read_text(encoding="utf-8"))
        self.assertEqual(rules["credit_delta"]["missing_or_invalid_receipt"], -8)
        sop = (ROOT / "ops/run_pred_invest_daily_sop.py").read_text(encoding="utf-8")
        self.assertNotIn("credit_delta = 0 if valid else -8", sop)
        self.assertIn("missing_or_invalid_receipt", sop)


if __name__ == "__main__":
    unittest.main()
