"""Boundary input validation for magic-square grids."""

from __future__ import annotations

from typing import Any

from boundary.error_codes import (
    DUPLICATE_VALUE_CODE,
    DUPLICATE_VALUE_MESSAGE,
    INVALID_EMPTY_COUNT_CODE,
    INVALID_EMPTY_COUNT_MESSAGE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    INVALID_VALUE_RANGE_CODE,
    INVALID_VALUE_RANGE_MESSAGE,
)
from boundary.schemas import ErrorDetail, FailureResponse
from entity.constants import (
    EMPTY_CELL_VALUE,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    REQUIRED_EMPTY_COUNT,
)


class InputValidator:
    """Validates incoming grids before Domain execution."""

    def validate(self, grid: Any) -> FailureResponse | None:
        """Validate grid structure and content.

        Args:
            grid: 4×4 grid with 0 for empty cells, or None when absent.

        Returns:
            FailureResponse when validation fails; None when the grid is valid.
        """
        size_error = self._check_size(grid)
        if size_error is not None:
            return size_error

        assert isinstance(grid, list)
        empty_error = self._check_empty_count(grid)
        if empty_error is not None:
            return empty_error

        range_error = self._check_value_range(grid)
        if range_error is not None:
            return range_error

        duplicate_error = self._check_duplicates(grid)
        if duplicate_error is not None:
            return duplicate_error

        return None

    @staticmethod
    def _failure(code: str, message: str) -> FailureResponse:
        """Build a standard failure envelope."""
        return FailureResponse(
            type="ERROR",
            error=ErrorDetail(code=code, message=message),
        )

    def _check_size(self, grid: Any) -> FailureResponse | None:
        """Return failure when grid is None or not 4×4."""
        if grid is None:
            return self._failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        if not isinstance(grid, list):
            return self._failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        if len(grid) != GRID_SIZE:
            return self._failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        for row in grid:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                return self._failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        return None

    def _check_empty_count(self, grid: list[list[Any]]) -> FailureResponse | None:
        """Return failure when empty cell count is not exactly two."""
        empty_count = sum(
            1 for row in grid for value in row if value == EMPTY_CELL_VALUE
        )
        if empty_count != REQUIRED_EMPTY_COUNT:
            return self._failure(INVALID_EMPTY_COUNT_CODE, INVALID_EMPTY_COUNT_MESSAGE)
        return None

    def _check_value_range(self, grid: list[list[Any]]) -> FailureResponse | None:
        """Return failure when any cell is outside 0 or 1..16."""
        for row in grid:
            for value in row:
                if not isinstance(value, int):
                    return self._failure(
                        INVALID_VALUE_RANGE_CODE, INVALID_VALUE_RANGE_MESSAGE
                    )
                if value == EMPTY_CELL_VALUE:
                    continue
                if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
                    return self._failure(
                        INVALID_VALUE_RANGE_CODE, INVALID_VALUE_RANGE_MESSAGE
                    )
        return None

    def _check_duplicates(self, grid: list[list[Any]]) -> FailureResponse | None:
        """Return failure when non-zero values repeat."""
        seen: set[int] = set()
        for row in grid:
            for value in row:
                if value == EMPTY_CELL_VALUE:
                    continue
                if value in seen:
                    return self._failure(DUPLICATE_VALUE_CODE, DUPLICATE_VALUE_MESSAGE)
                seen.add(value)
        return None
