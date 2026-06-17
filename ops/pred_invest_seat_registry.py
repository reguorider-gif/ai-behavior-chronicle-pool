from __future__ import annotations

import importlib.util
from pathlib import Path


_LOCAL_REGISTRY = Path(__file__).resolve().parent / "pool" / "seat_registry.py"
_SPEC = importlib.util.spec_from_file_location("_pred_invest_local_seat_registry", _LOCAL_REGISTRY)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Cannot load local seat registry: {_LOCAL_REGISTRY}")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

MODEL_ACCOUNT_BY_SEAT = _MODULE.MODEL_ACCOUNT_BY_SEAT
PRODUCTION_SEATS = _MODULE.PRODUCTION_SEATS
REQUIRED_SEAT_COUNT = _MODULE.REQUIRED_SEAT_COUNT
SEAT_ALIASES = _MODULE.SEAT_ALIASES
SEAT_DISPLAY_NAMES = _MODULE.SEAT_DISPLAY_NAMES
canonical_seat_id = _MODULE.canonical_seat_id
display_name_for_seat = _MODULE.display_name_for_seat
model_account_for_seat = _MODULE.model_account_for_seat
