"""UI constants for the MagicSquare screen layer."""

from __future__ import annotations

from typing import Final

from entity.constants import GRID_SIZE

WINDOW_TITLE: Final[str] = "MagicSquare - 4x4 Puzzle"
GRID_DIMENSION: Final[int] = GRID_SIZE

SAMPLE_PUZZLE: Final[list[list[int]]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 0, 1],
]

STATUS_READY: Final[str] = (
    "Enter a 4×4 grid (0 = empty). Exactly two empty cells required."
)
STATUS_SOLVED: Final[str] = "Solved - filled cells highlighted in green."
STATUS_CLEARED: Final[str] = "Grid cleared."
STATUS_VALIDATION_FAILED: Final[str] = "Validation failed"

STYLE_DEFAULT: Final[str] = ""
STYLE_ERROR: Final[str] = "color: #c0392b; font-weight: 600;"
STYLE_SUCCESS: Final[str] = "color: #1e8449; font-weight: 600;"
STYLE_CELL_FILLED: Final[str] = (
    "QSpinBox { background-color: #d5f5e3; font-weight: 600; }"
)
STYLE_CELL_DEFAULT: Final[str] = ""
