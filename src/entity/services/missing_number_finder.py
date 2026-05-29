"""Find missing numbers from the 1..16 set for a partial grid."""

from __future__ import annotations

from entity.constants import ALL_VALUES, EMPTY_CELL_VALUE, GRID_SIZE


def find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    """Return missing values from ``{1..16}`` not present as non-zero cells.

    Args:
        grid: 4×4 partial magic-square grid.

    Returns:
        Missing numbers in ascending order.
    """
    present: set[int] = set()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            if value != EMPTY_CELL_VALUE:
                present.add(value)
    return sorted(ALL_VALUES - present)
