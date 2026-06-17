from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _js_string_pairs(object_name: str, html: str) -> dict[str, str]:
    match = re.search(rf"const {object_name} = \{{(.*?)\n\}};", html, flags=re.S)
    if not match:
        raise AssertionError(f"Missing {object_name} object in index.html")
    body = match.group(1)
    return {
        key: value
        for key, value in re.findall(r'"([^"]+)":\s*"((?:\\.|[^"\\])*)"', body)
    }


def _active_team_names() -> set[str]:
    roots = [
        ROOT / "data/pool/pred_invest",
        ROOT / "data/pool/market_snapshots",
        ROOT / "data/pool/match_results",
    ]
    team_keys = {"home", "away", "home_team", "away_team", "home_name", "away_name"}
    names: set[str] = set()

    def walk(value):
        if isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for key, item in value.items():
                if key in team_keys and isinstance(item, str) and item.strip():
                    names.add(item.strip())
                walk(item)

    for root in roots:
        for path in root.rglob("*.json"):
            if "/_archive/" in str(path):
                continue
            try:
                walk(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                continue
    non_team_fixture_tokens = {"One", "Two", "home", "away", "draw"}
    return {
        name
        for name in names
        if not name.endswith(" FC")
        and name not in non_team_fixture_tokens
        and not re.match(r"^TBD(?:\b|$)", name, flags=re.I)
    }


class FrontendTeamFlagContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.aliases = _js_string_pairs("TEAM_ALIASES", cls.html)
        cls.zh = _js_string_pairs("TEAM_ZH", cls.html)
        cls.flags = _js_string_pairs("TEAM_FLAGS", cls.html)

    def canonical(self, name: str) -> str:
        return self.aliases.get(name, name)

    def test_known_aliases_from_current_slate_resolve_to_flags_and_chinese_names(self):
        expected = {
            "Congo DR": "DR Congo",
            "Cabo Verde": "Cape Verde",
            "Côte d’Ivoire": "Ivory Coast",
            "IR Iran": "Iran",
            "Korea Republic": "South Korea",
            "Türkiye": "Turkey",
        }
        for raw, canonical in expected.items():
            with self.subTest(raw=raw):
                self.assertEqual(self.canonical(raw), canonical)
                self.assertIn(canonical, self.flags)
                self.assertNotEqual(self.flags[canonical], "🏳️")
                self.assertIn(canonical, self.zh)

    def test_all_active_match_teams_have_non_placeholder_flags(self):
        missing = []
        for raw in sorted(_active_team_names()):
            canonical = self.canonical(raw)
            flag = self.flags.get(canonical)
            zh = self.zh.get(canonical)
            if not flag or flag == "🏳️" or not zh:
                missing.append(f"{raw} -> {canonical}")
        self.assertEqual(missing, [])

    def test_flag_renderer_prefers_canonical_mapping_over_upstream_raw_flag(self):
        self.assertIn("function isPlaceholderTeamName(teamName)", self.html)
        self.assertIn('if(isPlaceholderTeamName(teamName))return "—";', self.html)
        self.assertIn("const mapped = TEAM_FLAGS[canonical];", self.html)
        self.assertIn("if(mapped)return mapped;", self.html)
        self.assertIn("return teamFlag", self.html)


if __name__ == "__main__":
    unittest.main()
