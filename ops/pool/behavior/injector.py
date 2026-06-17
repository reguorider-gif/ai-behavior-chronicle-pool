from __future__ import annotations

from typing import Any

from ..memory_injector import inject_behavior_memory


def inject_behavior(prompt_context: dict[str, Any], seat_id: str) -> dict[str, Any]:
    """Inject private behavior memory into one agent prompt context."""

    return inject_behavior_memory(prompt_context, seat_id)
