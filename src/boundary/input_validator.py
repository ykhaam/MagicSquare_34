"""Boundary input validation for magic-square grids."""

from __future__ import annotations

from boundary.schemas import (
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    ErrorDetail,
    FailureResponse,
)


class InputValidator:
    """Validates incoming grids before Domain execution."""

    def validate(self, grid: list[list[int]] | None) -> FailureResponse:
        """Validate grid structure and content.

        Args:
            grid: 4x4 grid with 0 for empty cells, or None when absent.

        Returns:
            FailureResponse when validation fails for null or invalid size.
        """
        if self._is_invalid_size(grid):
            return FailureResponse(
                type="ERROR",
                error=ErrorDetail(
                    code=INVALID_SIZE_CODE,
                    message=INVALID_SIZE_MESSAGE,
                ),
            )
        raise NotImplementedError(
            "InputValidator.validate: only null/invalid-size grids are implemented"
        )

    @staticmethod
    def _is_invalid_size(grid: list[list[int]] | None) -> bool:
        """Return True when grid is None or not 4×4."""
        if grid is None:
            return True
        if len(grid) != 4:
            return True
        for row in grid:
            if not isinstance(row, list) or len(row) != 4:
                return True
        return False
