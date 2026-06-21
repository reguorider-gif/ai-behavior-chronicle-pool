#!/usr/bin/env python3
"""Manual shortcut for one-day PRED-INVEST automation runs.

This wrapper keeps the operator-facing command stable while delegating all
real orchestration to ``ops/auto_sop.py``. By default it runs the full
pre/post cycle; when bridge dispatch is requested and no explicit seats are
provided, it targets the four recovery seats required by the production
pipeline contract.
"""

from __future__ import annotations

import sys

from auto_sop import main as auto_sop_main


DEFAULT_TARGETED_RERUN_SEATS = "grok,xunfei,stepfun,zhipu"
PHASE_TOKENS = {"pre", "post", "dry-run", "auto", "full"}


def _has_phase(argv: list[str]) -> bool:
    return any(arg in PHASE_TOKENS or arg == "--phase" or arg.startswith("--phase=") for arg in argv)


def _has_option(argv: list[str], name: str) -> bool:
    return any(arg == name or arg.startswith(f"{name}=") for arg in argv)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not _has_phase(args):
        args = ["--phase", "full", *args]
    if _has_option(args, "--dispatch") and not _has_option(args, "--seats"):
        args.extend(["--seats", DEFAULT_TARGETED_RERUN_SEATS])
    return auto_sop_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
