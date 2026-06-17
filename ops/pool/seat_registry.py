from __future__ import annotations

from typing import Any


PRODUCTION_SEATS = [
    "chatgpt",
    "deepseek",
    "mimo",
    "minimax",
    "doubao",
    "gemini",
    "kimi",
    "meta",
    "qwen",
    "wenxin",
    "grok",
    "yuanbao",
    "xunfei",
    "stepfun",
    "zhipu",
]

REQUIRED_SEAT_COUNT = len(PRODUCTION_SEATS)

SEAT_DISPLAY_NAMES = {
    "chatgpt": "ChatGPT",
    "deepseek": "DeepSeek",
    "mimo": "MiMo",
    "minimax": "MiniMax",
    "doubao": "Doubao",
    "gemini": "Gemini",
    "kimi": "Kimi",
    "meta": "Meta AI",
    "qwen": "Qwen",
    "wenxin": "Wenxin",
    "grok": "xAI Grok",
    "yuanbao": "Yuanbao",
    "xunfei": "科大讯飞",
    "stepfun": "阶跃星辰",
    "zhipu": "智谱清言",
}

MODEL_ACCOUNT_BY_SEAT = {
    "grok": "xai",
}

SEAT_ALIASES = {
    "xai": "grok",
    "xai grok": "grok",
    "iflytek": "xunfei",
    "iflytek spark": "xunfei",
    "spark": "xunfei",
    "xinghuo": "xunfei",
    "讯飞": "xunfei",
    "科大讯飞": "xunfei",
    "stepfun": "stepfun",
    "step fun": "stepfun",
    "step": "stepfun",
    "stepchat": "stepfun",
    "stepchat ai": "stepfun",
    "阶跃": "stepfun",
    "阶跃星辰": "stepfun",
    "zhipu": "zhipu",
    "zhipuai": "zhipu",
    "zhipu ai": "zhipu",
    "glm": "zhipu",
    "智谱": "zhipu",
    "智谱清言": "zhipu",
}


def canonical_seat_id(value: Any) -> str:
    raw = str(value or "").strip().lower()
    if not raw:
        return ""
    return SEAT_ALIASES.get(raw, raw.replace(" ", ""))


def display_name_for_seat(seat_id: Any) -> str:
    canonical = canonical_seat_id(seat_id)
    return SEAT_DISPLAY_NAMES.get(canonical, str(seat_id or canonical))


def model_account_for_seat(seat_id: Any) -> str:
    canonical = canonical_seat_id(seat_id)
    return MODEL_ACCOUNT_BY_SEAT.get(canonical, canonical)
