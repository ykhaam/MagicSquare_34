"""Boundary validation tests for invalid grid size (UT-E01 / AC-FR-01-01)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

import pytest

from boundary.magic_square_boundary import MagicSquareBoundary
from boundary.schemas import ErrorResponse

AC_ID = "AC-FR-01-01"
PRD_SECTION = "PRD §8.1"
EXPECTED_CODE = "INVALID_SIZE"
EXPECTED_MESSAGE = "Grid must be 4x4."

THREE_BY_FOUR_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

EXCLUDED_AC_MARKERS: tuple[str, ...] = (
    "AC-FR-01-02",
    "AC-FR-01-03",
    "AC-FR-01-04",
    "AC-FR-01-05",
    "UI_INVALID_EMPTY_COUNT",
    "UI_INVALID_VALUE_RANGE",
    "UI_DUPLICATE_VALUE",
    "DOMAIN_NO_SOLUTION",
    "FR-02",
    "FR-03",
    "FR-04",
    "FR-05",
)


class TestAcFr0101InvalidSize:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary invalid grid size RED slice."""

    @pytest.fixture
    def boundary_with_mock_resolve(self) -> tuple[MagicSquareBoundary, Mock]:
        """Boundary wired with a spy stand-in for the Domain resolve entrypoint."""
        mock_resolve = Mock(name="resolve")
        boundary = MagicSquareBoundary(resolve=mock_resolve)
        return boundary, mock_resolve

    def test_none_grid_returns_invalid_size_failure(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid returns failure response."""
        # AC-FR-01-01
        # Given
        boundary, _mock_resolve = boundary_with_mock_resolve
        grid = None

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    def test_empty_list_returns_invalid_size_failure(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list returns failure response."""
        # AC-FR-01-01
        # Given
        boundary, _mock_resolve = boundary_with_mock_resolve
        grid: list[list[int]] = []

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    def test_ragged_four_rows_returns_invalid_size_failure(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — ragged rows return failure response."""
        # AC-FR-01-01
        # Given
        boundary, _mock_resolve = boundary_with_mock_resolve
        grid: list[list[int]] = [[]] * 4

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    def test_three_by_four_grid_returns_invalid_size_failure(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3x4 grid returns failure response."""
        # AC-FR-01-01
        # Given
        boundary, _mock_resolve = boundary_with_mock_resolve
        grid = THREE_BY_FOUR_GRID

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == EXPECTED_CODE
        assert result.message == EXPECTED_MESSAGE

    def test_none_grid_resolve_called_zero_times(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() is never invoked for None."""
        # AC-FR-01-01
        # Given
        boundary, mock_resolve = boundary_with_mock_resolve
        grid = None

        # When
        boundary.solve(grid)

        # Then
        mock_resolve.assert_not_called()
        assert mock_resolve.call_count == 0

    def test_none_grid_message_exact_prd_match(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message matches PRD text byte-for-byte."""
        # AC-FR-01-01
        # Given
        boundary, _mock_resolve = boundary_with_mock_resolve
        grid = None
        prd_message = "Grid must be 4x4."

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.message == prd_message
        assert result.message == EXPECTED_MESSAGE
        assert len(result.message) == len(prd_message)

    def test_none_grid_failure_result_is_error_response_type(
        self, boundary_with_mock_resolve: tuple[MagicSquareBoundary, Mock]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure payload is ErrorResponse."""
        # AC-FR-01-01
        # Given
        boundary, _mock_resolve = boundary_with_mock_resolve
        grid = None

        # When
        result = boundary.solve(grid)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.model_dump() == {
            "code": EXPECTED_CODE,
            "message": EXPECTED_MESSAGE,
            "field": None,
        }

    def test_scope_excludes_ac_fr01_02_to_05_and_fr02_to_fr05(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — RED slice excludes out-of-scope AC cases."""
        # AC-FR-01-01
        # Given
        module_source = Path(__file__).read_text(encoding="utf-8")

        # When / Then
        for marker in EXCLUDED_AC_MARKERS:
            assert marker not in module_source, (
                f"Out-of-scope marker {marker!r} must not appear in this RED module."
            )
