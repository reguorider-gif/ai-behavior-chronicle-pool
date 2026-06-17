"""Behavior Kernel compatibility package.

The production implementation lives in focused modules under ``ops.pool``.
This package exposes the manifest-level names used by the Behavior Chronicle
patch contract without forking a second behavior system.
"""

from .compiler import compile_patterns, compile_state
from .event_logger import log_event
from .graph import build_graph
from .injector import inject_behavior
from .tracer import write_trace

__all__ = [
    "build_graph",
    "compile_patterns",
    "compile_state",
    "inject_behavior",
    "log_event",
    "write_trace",
]
