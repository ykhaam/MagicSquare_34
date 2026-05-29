"""Boundary entrypoint for magic-square solve requests."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from boundary.input_validator import InputValidator
from boundary.schemas import ErrorResponse


class MagicSquareBoundary:
    """Validates input and delegates valid grids to the injected resolve callable."""

    def __init__(self, resolve: Callable[..., Any]) -> None:
        """Wire Domain resolve; validation failures never invoke resolve.

        Args:
            resolve: Stand-in or real Domain entrypoint for valid grids.
        """
        self._resolve = resolve
        self._validator = InputValidator()

    def solve(self, grid: list[list[int]] | None) -> ErrorResponse:
        """Validate grid size; return ErrorResponse without calling resolve on failure.

        Args:
            grid: 4x4 puzzle grid, or None when absent.

        Returns:
            ErrorResponse when grid is None or not 4x4.
        """
        failure = self._validator.validate(grid)
        return ErrorResponse(
            code=failure.error.code,
            message=failure.error.message,
        )
