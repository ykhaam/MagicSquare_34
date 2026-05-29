"""Magic-square domain constants (SSOT)."""

from __future__ import annotations

from typing import Final

MAGIC_SUM: Final[int] = 34
GRID_SIZE: Final[int] = 4
REQUIRED_EMPTY_COUNT: Final[int] = 2
MIN_CELL_VALUE: Final[int] = 1
MAX_CELL_VALUE: Final[int] = 16
EMPTY_CELL_VALUE: Final[int] = 0

ALL_VALUES: Final[frozenset[int]] = frozenset(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1))
