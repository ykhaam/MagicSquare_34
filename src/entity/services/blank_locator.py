"""Locate empty cells in row-major order."""

from __future__ import annotations

from entity.constants import EMPTY_CELL_VALUE, GRID_SIZE


def find_blank_coords(grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return the two empty cell positions in 1-indexed row-major order.

    Args:
        grid: 4×4 grid with exactly two ``0`` cells.

    Returns:
        First and second blank positions as ``(row, col)`` tuples (1-indexed).
    """
    blanks: list[tuple[int, int]] = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == EMPTY_CELL_VALUE:
                blanks.append((row + 1, col + 1))
    first, second = blanks[0], blanks[1]
    return first, second
