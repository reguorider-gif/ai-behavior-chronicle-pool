from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
POOL_META = ROOT / "api/pool-meta.js"
POOL_CATCH_ALL = ROOT / "api/pool/[...path].js"


REQUIRED_MODULES = {
    "overview",
    "audit",
    "civilization",
    "journal",
    "replay",
    "patterns",
    "agents",
    "credit",
    "survival",
    "settlement",
    "split",
    "forecasts",
    "investments",
    "god",
    "observer",
}


class DataCenterContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.pool_meta = POOL_META.read_text(encoding="utf-8")
        cls.pool_catch_all = POOL_CATCH_ALL.read_text(encoding="utf-8")

    def _module_registry(self) -> str:
        match = re.search(
            r"const DATA_CENTER_MODULES = \{(.*?)\n\};\nconst TEAM_ALIASES",
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(match, "DATA_CENTER_MODULES registry is missing")
        return match.group(1)

    def _section_registry(self) -> str:
        match = re.search(
            r"const DATA_CENTER_SECTIONS = \[(.*?)\n\];\nconst DATA_CENTER_MODULES",
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(match, "DATA_CENTER_SECTIONS registry is missing")
        return match.group(1)

    def test_data_center_has_5_clear_sections_and_15_unique_modules(self):
        sections = self._section_registry()
        module_lists = re.findall(r"modules:\[(.*?)\]", sections)
        section_ids = re.findall(r'\{id:"([^"]+)"', sections)
        modules = [
            item
            for module_list in module_lists
            for item in re.findall(r'"([^"]+)"', module_list)
        ]
        self.assertEqual(section_ids, ["ops", "behavior", "capital", "decision", "report"])
        self.assertEqual(len(modules), 15)
        self.assertEqual(len(modules), len(set(modules)))
        self.assertEqual(set(modules), REQUIRED_MODULES)

    def test_every_module_has_renderer_status_and_source(self):
        registry = self._module_registry()
        for module in REQUIRED_MODULES:
            with self.subTest(module=module):
                self.assertIn(f"{module}:{{", registry)
                start = registry.index(f"{module}:{{")
                end = min(
                    [idx for idx in [registry.find(f"\n  {other}:{{", start + 1) for other in REQUIRED_MODULES] if idx != -1]
                    or [len(registry)]
                )
                chunk = registry[start:end]
                self.assertIn("status:", chunk)
                self.assertIn("render:", chunk)
                self.assertIn("sources:[", chunk)
                self.assertRegex(chunk, r'(data/pool|/api/pool)')
                renderer = re.search(r"render:([A-Za-z0-9_]+)", chunk)
                self.assertIsNotNone(renderer)
                self.assertIn(f"function {renderer.group(1)}(", self.html)

    def test_modules_are_clickable_and_jump_to_detail_panel(self):
        self.assertIn('class="product-entry-card data-center-module', self.html)
        self.assertIn("data-data-view", self.html)
        self.assertIn('onclick="setDataCenterView', self.html)
        self.assertIn('id="dataCenterContent"', self.html)
        self.assertIn("scrollIntoView", self.html)
        self.assertIn("renderDataCenterModuleContent", self.html)
        self.assertIn("dataCenterSourcePanel", self.html)
        self.assertIn("?panel=data-center&view=", self.html)

    def test_frontend_registry_is_aligned_with_pool_backend_surfaces(self):
        frontend_required_routes = [
            "/api/pool/rules/current",
            "/api/pool/seats/{seat}/journal",
            "/api/pool/seats/{seat}/credit",
            "/api/pool/runs/{run}/behavior-replay",
            "/api/pool/pattern-graph",
            "/api/pool/agent-profiles",
            "/api/pool/runs/{run}/god-report",
        ]
        for route in frontend_required_routes:
            with self.subTest(route=route):
                self.assertIn(route, self.html)

        backend_handlers = [
            "currentRules",
            "seatJournal",
            "creditHistory",
            "behaviorReplay",
            "patternGraph",
            "agentProfile",
            "godReport",
        ]
        backend = self.pool_meta + "\n" + self.pool_catch_all
        for handler in backend_handlers:
            with self.subTest(handler=handler):
                self.assertIn(handler, backend)

    def test_pool_backend_does_not_default_to_production_self_proxy(self):
        backend = self.pool_meta + "\n" + self.pool_catch_all
        self.assertNotIn('|| "https://pool-app-one.vercel.app"', backend)
        self.assertGreaterEqual(backend.count('process.env.POOL_FALLBACK_ORIGIN || ""'), 2)
        self.assertIn("fallback_not_configured", backend)

    def test_v4_backend_contracts_are_present(self):
        self.assertIn("initialized_required_seats", self.pool_meta)
        self.assertIn("frontendArchives", self.pool_meta)
        self.assertIn("seatArchive", self.pool_meta)
        self.assertIn("account_initialized", self.pool_meta)
        sop = (ROOT / "ops/run_pred_invest_daily_sop.py").read_text(encoding="utf-8")
        rules = (ROOT / "data/pool/rules/PRED_INVEST_CREDIT_SURVIVE_V2.json").read_text(encoding="utf-8")
        self.assertIn("missing_or_invalid_receipt", sop)
        self.assertIn("missing_or_invalid_receipt", rules)
        self.assertNotIn("credit_delta = 0 if valid else -8", sop)


if __name__ == "__main__":
    unittest.main()
