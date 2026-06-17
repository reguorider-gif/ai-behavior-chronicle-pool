from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import ensure_parent

LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
LOCAL_NO_PROXY = "127.0.0.1,localhost,::1"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return {} if default is None else default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {} if default is None else default


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def append_jsonl(path: Path, payload: dict[str, Any]) -> Path:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def is_local_url(url: str) -> bool:
    return (urllib.parse.urlparse(url).hostname or "").lower() in LOCAL_HOSTS


def local_subprocess_env() -> dict[str, str]:
    """Return an env that keeps local control-plane requests off user proxies."""
    env = dict(os.environ)
    env["NO_PROXY"] = ",".join(filter(None, [env.get("NO_PROXY"), LOCAL_NO_PROXY]))
    env["no_proxy"] = ",".join(filter(None, [env.get("no_proxy"), LOCAL_NO_PROXY]))
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
        env.pop(key, None)
    return env


def http_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    """Fetch JSON with consistent local bridge/proxy behavior and error shape."""
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if is_local_url(url) else urllib.request
        with opener.open(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                return json.loads(raw)
            except Exception:
                return {"ok": False, "error": "non_json_response", "status": response.status, "raw": raw[:2000]}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw[:2000]}
        body.setdefault("ok", False)
        body.setdefault("status", exc.code)
        return body
    except Exception as exc:
        if is_local_url(url):
            cmd = [
                "curl",
                "-sS",
                "--noproxy",
                "*",
                "--http1.1",
                "--connect-timeout",
                "5",
                "--retry",
                "2",
                "--retry-delay",
                "1",
                "--retry-connrefused",
                "-m",
                str(timeout),
                "-H",
                "Accept: application/json",
            ]
            if payload is not None:
                cmd.extend([
                    "-H",
                    "Content-Type: application/json",
                    "-X",
                    "POST",
                    "--data-binary",
                    json.dumps(payload, ensure_ascii=False),
                ])
            cmd.append(url)
            try:
                completed = subprocess.run(
                    cmd,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=timeout + 5,
                    env=local_subprocess_env(),
                )
                raw = completed.stdout or completed.stderr or ""
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = {"ok": False, "error": "curl_non_json_response", "raw": raw[:2000]}
                parsed.setdefault("curl_fallback_used", True)
                parsed.setdefault("curl_returncode", completed.returncode)
                if completed.returncode != 0:
                    parsed.setdefault("ok", False)
                return parsed
            except Exception as curl_exc:
                return {
                    "ok": False,
                    "error": type(exc).__name__,
                    "message": str(exc),
                    "curl_fallback_error": str(curl_exc),
                }
        return {"ok": False, "error": type(exc).__name__, "message": str(exc)}
