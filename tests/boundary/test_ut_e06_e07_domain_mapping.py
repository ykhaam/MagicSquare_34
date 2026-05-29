"""Boundary domain exception mapping — UT-E06, UT-E07 (Report 02 §2.3)."""

from __future__ import annotations

from unittest.mock import Mock

from boundary.schemas import ErrorResponse
from boundary.ui_boundary import UIBoundary
from entity.domain_codes import (
    DOMAIN_INVALID_GRID_CODE,
    DOMAIN_INVALID_GRID_MESSAGE,
)
from entity.exceptions import (
    DOMAIN_NO_SOLUTION_CODE,
    DOMAIN_NO_SOLUTION_MESSAGE,
    DomainInvalidGridError,
    UnsolvableDomainError,
)
from tests.entity.conftest import G1_RD01, G3


class TestUtE06E07DomainExceptionMapping:
    """UT-E06/UT-E07 — Domain failures map to flat ErrorResponse at Boundary."""

    def test_ut_e07_domain_invalid_grid_maps_to_error_response(self) -> None:
        """UT-E07 — DomainInvalidGridError maps to DOMAIN_INVALID_GRID."""
        # Given
        mock_execute = Mock(
            side_effect=DomainInvalidGridError(
                code=DOMAIN_INVALID_GRID_CODE,
                message=DOMAIN_INVALID_GRID_MESSAGE,
            )
        )
        boundary = UIBoundary(execute=mock_execute)

        # When
        result = boundary.solve(G1_RD01)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == DOMAIN_INVALID_GRID_CODE
        assert result.message == DOMAIN_INVALID_GRID_MESSAGE
        mock_execute.assert_called_once()

    def test_ut_e06_unsolvable_domain_maps_to_error_response(self) -> None:
        """UT-E06 — UnsolvableDomainError maps to DOMAIN_NO_SOLUTION."""
        # Given
        mock_execute = Mock(
            side_effect=UnsolvableDomainError(
                code=DOMAIN_NO_SOLUTION_CODE,
                message=DOMAIN_NO_SOLUTION_MESSAGE,
            )
        )
        boundary = UIBoundary(execute=mock_execute)

        # When
        result = boundary.solve(G3)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == DOMAIN_NO_SOLUTION_CODE
        assert result.message == DOMAIN_NO_SOLUTION_MESSAGE
        mock_execute.assert_called_once()
