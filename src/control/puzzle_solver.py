"""Puzzle solver entrypoint for partial magic-square grids."""

from __future__ import annotations

import copy

from entity.exceptions import DomainInvalidGridError, UnsolvableDomainError
from entity.magic_grid import MagicGrid
from entity.services.blank_locator import find_blank_coords
from entity.services.magic_validator import is_magic_square
from entity.services.missing_number_finder import find_not_exist_nums


def solution(grid: list[list[int]]) -> list[int]:
    """Solve a partial 4×4 magic square using Step A then Step B placement.

    Step A places the smaller missing value in the first blank and the larger
    in the second blank. Step B reverses the assignment. Coordinates are 1-indexed.

    Args:
        grid: Valid partial 4×4 grid with exactly two empty cells.

    Returns:
        Six-element result ``[r1, c1, n1, r2, c2, n2]``.

    Raises:
        DomainInvalidGridError: When the grid fails domain structure checks.
        UnsolvableDomainError: When neither placement yields a magic square.
    """
    MagicGrid.from_raw(grid)
    first, second = find_blank_coords(grid)
    missing = find_not_exist_nums(grid)
    small, large = missing[0], missing[1]

    step_a = _try_placement(grid, first, second, small, large)
    if step_a is not None:
        return step_a

    step_b = _try_placement(grid, first, second, large, small)
    if step_b is not None:
        return step_b

    raise UnsolvableDomainError()


def _try_placement(
    grid: list[list[int]],
    first: tuple[int, int],
    second: tuple[int, int],
    first_value: int,
    second_value: int,
) -> list[int] | None:
    """Attempt a placement and return the output vector when magic."""
    candidate = copy.deepcopy(grid)
    candidate[first[0] - 1][first[1] - 1] = first_value
    candidate[second[0] - 1][second[1] - 1] = second_value
    if is_magic_square(candidate):
        return [
            first[0],
            first[1],
            first_value,
            second[0],
            second[1],
            second_value,
        ]
    return None
