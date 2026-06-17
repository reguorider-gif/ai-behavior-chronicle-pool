# PRED-INVEST Attempt 46 Single-Seat Reruns · run-16

- date: 2026-06-16
- requested seats: chatgpt, doubao, gemini, grok, kimi, mimo, minimax, qwen, wenxin, yuanbao
- executed seats: chatgpt, doubao, gemini, kimi, mimo, minimax, qwen, wenxin, yuanbao
- provider blocked skipped: grok
- final gate: PARTIAL_NOT_READY (2/12)
- publish allowed: False

## Seat Runs

| Seat | Run ID | Submit | Wait | Notes |
| --- | --- | --- | --- | --- |
| chatgpt | - | fail | fail | no_ready_seats |
| doubao | - | fail | fail | no_ready_seats |
| gemini | - | fail | fail | no_ready_seats |
| kimi | - | fail | fail | no_ready_seats |
| mimo | - | fail | fail | no_ready_seats |
| minimax | - | fail | fail | no_ready_seats |
| qwen | - | fail | fail | no_ready_seats |
| wenxin | - | fail | fail | no_ready_seats |
| yuanbao | - | fail | fail | no_ready_seats |

## Page Salvage

- ok: False
- error: RuntimeError · runtime_python_page_salvage_failed: {"direct_error": {"type": "ModuleNotFoundError", "message": "No module named 'playwright'"}, "returncode": 1, "stdout": "", "stderr": "runtime/.venv/lib/python3.12/site-packages/playwright/async_api/_generated.py\", line 16720, in connect_over_cdp\n    await self._impl_obj.connect_over_cdp(\n  File \"/Users/audimacmini/Library/Application Support/AI Judge/user-app-support/runtime/.venv/lib/python3.12/site-packages/playwright/_impl/_browser_type.py\", line 209, in connect_over_cdp\n    response = await self._channel.send_return_as_dict(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/audimacmini/Library/Application Support/AI Judge/user-app-support/runtime/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py\", line 83, in send_return_as_dict\n    return await self._connection.wrap_api_call(\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/audimacmini/Library/Application Support/AI Judge/user-app-support/runtime/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py\", line 559, in wrap_api_call\n    raise rewrite_error(error, f\"{parsed_st['apiName']}: {error}\") from None\nplaywright._impl._errors.Error: BrowserType.connect_over_cdp: connect EPERM 127.0.0.1:9333 - Local (0.0.0.0:0)\nCall log:\n  - <ws preparing> retrieving websocket url from http://127.0.0.1:9333\n\n"}

## Final Needs Rerun

- chatgpt, doubao, gemini, grok, kimi, mimo, minimax, qwen, wenxin, yuanbao
