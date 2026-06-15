from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "pool-app-live-repair" / "index.html"


class FrontendSettlementContractTests(unittest.TestCase):
    def test_frontend_loads_latest_settlement_artifact(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("latestSettlement", html)
        self.assertIn("settlement_trigger?.path", html)
        self.assertIn("data/pool/settlements/${dailySop.round_id}.json", html)

    def test_match_detail_uses_settlement_profit_for_pl(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("settlementBySeatForMatch(matchId)", html)
        self.assertIn("settlementProfit", html)
        self.assertIn("r.settlementProfit !== null", html)
        self.assertIn("const displayNet=hasSettlementProfit ? Number(r.settlementProfit) : net", html)
