from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class FrontendQualityContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")

    def test_first_screen_round_verdict_is_rendered_from_data(self):
        self.assertIn('id="roundVerdict"', self.html)
        self.assertIn("function renderRoundVerdict()", self.html)
        self.assertIn("staticArtifacts.qualityGate", self.html)
        self.assertIn("verdict-card", self.html)

    def test_match_cards_use_structured_visual_layers(self):
        self.assertIn("function teamBadgeText", self.html)
        self.assertIn("function aiTendencyMeta", self.html)
        self.assertIn("team-badge", self.html)
        self.assertIn("ai-tendency-fill", self.html)

    def test_detail_panel_uses_ai_decision_table(self):
        self.assertIn("function renderAiDecisionTable", self.html)
        self.assertIn('class="ai-decisions"', self.html)
        self.assertIn("confidenceCell", self.html)
        self.assertIn("席位档案", self.html)

    def test_god_report_is_folded_into_data_center_not_homepage(self):
        self.assertNotIn('id="godReportSection"', self.html)
        self.assertIn('god:{section:"report"', self.html)
        self.assertIn("function renderGodReportProductView()", self.html)
        self.assertIn("上帝行为日报", self.html)


if __name__ == "__main__":
    unittest.main()
