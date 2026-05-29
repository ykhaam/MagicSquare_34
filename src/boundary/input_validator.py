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
from entity.grid_validator import (
    STRUCTURE_DUPLICATE_VALUE,
    STRUCTURE_INVALID_EMPTY_COUNT,
    STRUCTURE_INVALID_SIZE,
    STRUCTURE_INVALID_VALUE_RANGE,
    structure_failure_kind,
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
        content_error = self._check_structure_content(grid)
        if content_error is not None:
            return content_error

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
        if structure_failure_kind(grid) == STRUCTURE_INVALID_SIZE:
            return self._failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
        return None

    def _check_structure_content(self, grid: list[list[Any]]) -> FailureResponse | None:
        """Map entity structure failures to Boundary error codes."""
        kind = structure_failure_kind(grid)
        if kind is None:
            return None
        if kind == STRUCTURE_INVALID_EMPTY_COUNT:
            return self._failure(INVALID_EMPTY_COUNT_CODE, INVALID_EMPTY_COUNT_MESSAGE)
        if kind == STRUCTURE_INVALID_VALUE_RANGE:
            return self._failure(INVALID_VALUE_RANGE_CODE, INVALID_VALUE_RANGE_MESSAGE)
        if kind == STRUCTURE_DUPLICATE_VALUE:
            return self._failure(DUPLICATE_VALUE_CODE, DUPLICATE_VALUE_MESSAGE)
        return self._failure(INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE)
