"""Validate whether a grid is a complete magic square."""

from __future__ import annotations

from entity.constants import (
    ALL_VALUES,
    EMPTY_CELL_VALUE,
    GRID_SIZE,
    MAGIC_SUM,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when the grid is a complete 4×4 magic square.

    Args:
        grid: 4×4 integer grid.

    Returns:
        True if all rows, columns, diagonals sum to ``MAGIC_SUM`` with values 1..16.
    """
    if len(grid) != GRID_SIZE:
        return False
    for row in grid:
        if len(row) != GRID_SIZE:
            return False

    values: list[int] = []
    for row in grid:
        for value in row:
            if value == EMPTY_CELL_VALUE:
                return False
            if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
                return False
            values.append(value)

    if len(set(values)) != len(values):
        return False
    if set(values) != set(ALL_VALUES):
        return False

    for row in grid:
        if sum(row) != MAGIC_SUM:
            return False

    for col in range(GRID_SIZE):
        if sum(grid[row][col] for row in range(GRID_SIZE)) != MAGIC_SUM:
            return False

    main_diag = sum(grid[i][i] for i in range(GRID_SIZE))
    anti_diag = sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE))
    return main_diag == MAGIC_SUM and anti_diag == MAGIC_SUM
