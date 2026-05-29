"""Pytest configuration — ensure src layout is importable."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# --- G0~G3 grid fixtures (placeholder; see tests/entity/conftest.py) ---
# G1-RD01 (Boundary U-OUT Mock): PRD §16.4 RD-01
# G1_RD01 = [
#     [16, 0, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 0, 1],
# ]
