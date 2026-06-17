import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ops.pool.io_utils import http_json, is_local_url, read_json, write_json


class IoUtilsContractTest(unittest.TestCase):
    def test_read_json_returns_default_on_missing_or_parse_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "broken.json"
            self.assertEqual(read_json(path, {"ok": False}), {"ok": False})
            path.write_text("{broken", encoding="utf-8")
            self.assertEqual(read_json(path, {"fallback": True}), {"fallback": True})

    def test_write_json_round_trips_utf8_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "nested" / "payload.json"
            write_json(path, {"seat": "wenxin", "note": "ok"})
            self.assertEqual(read_json(path), {"seat": "wenxin", "note": "ok"})

    def test_http_json_has_bounded_non_json_error_shape_for_local_url(self):
        class FakeResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return ("x" * 2500).encode("utf-8")

        class FakeOpener:
            def open(self, _request, timeout=0):
                return FakeResponse()

        url = "http://127.0.0.1:8501/payload"
        self.assertTrue(is_local_url(url))
        with patch("ops.pool.io_utils.urllib.request.build_opener", return_value=FakeOpener()):
            response = http_json(url, timeout=5)

        self.assertFalse(response["ok"])
        self.assertEqual(response["error"], "non_json_response")
        self.assertLessEqual(len(response["raw"]), 2000)


if __name__ == "__main__":
    unittest.main()
