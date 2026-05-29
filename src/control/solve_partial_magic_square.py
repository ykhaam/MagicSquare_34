"""Control entrypoint — thin orchestration over entity two-cell solver."""

from __future__ import annotations

from entity.services.two_cell_solver import solve_two_cell_magic_square


def solution(grid: list[list[int]]) -> list[int]:
    """Run the partial magic-square solve pipeline for a validated grid.

    Args:
        grid: 4×4 partial grid with exactly two empty cells.

    Returns:
        Six-element success vector ``[r1, c1, n1, r2, c2, n2]``.

    Raises:
        DomainInvalidGridError: When entity structure validation fails.
        UnsolvableDomainError: When no valid completion exists.
    """
    return solve_two_cell_magic_square(grid)
