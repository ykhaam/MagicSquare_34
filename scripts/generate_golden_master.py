#!/usr/bin/env python
"""Generate tests/golden_master_expected.txt from live Magic Square Solver output."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
for path in (str(SRC), str(ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from boundary.ui_boundary import UIBoundary  # noqa: E402
from control.puzzle_solver import solution  # noqa: E402
from tests.golden_master.approve import build_golden_master_content  # noqa: E402

DEFAULT_OUTPUT = ROOT / "tests" / "golden_master_expected.txt"


def main() -> int:
    """Write the GM-1 baseline file from current solver behavior."""
    boundary = UIBoundary(execute=solution)
    content = build_golden_master_content(boundary.solve)
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(content, encoding="utf-8")
    print(f"Wrote {DEFAULT_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
