"""Boundary output guard — UT-F01, UT-F02 (Report 02 §2.3)."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from boundary.error_codes import (
    UI_INTERNAL_CONTRACT_CODE,
    UI_INTERNAL_CONTRACT_MESSAGE,
)
from boundary.schemas import ErrorResponse
from boundary.ui_boundary import UIBoundary
from tests.entity.conftest import G1_RD01


class TestUtF01F02OutputGuard:
    """UT-F01/F02 — int[6] length and 1-index coordinate guard."""

    def test_ut_f01_wrong_length_returns_internal_contract(self) -> None:
        """UT-F01 — Mock int[5] returns UI_INTERNAL_CONTRACT."""
        # Given
        mock_execute = Mock(return_value=[1, 2, 3, 4, 5])
        boundary = UIBoundary(execute=mock_execute)

        # When
        result = boundary.solve(G1_RD01)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == UI_INTERNAL_CONTRACT_CODE
        assert result.message == UI_INTERNAL_CONTRACT_MESSAGE

    def test_ut_f02_zero_index_coordinate_returns_internal_contract(self) -> None:
        """UT-F02 — Mock r1=0 returns UI_INTERNAL_CONTRACT."""
        # Given
        mock_execute = Mock(return_value=[0, 2, 7, 3, 3, 10])
        boundary = UIBoundary(execute=mock_execute)

        # When
        result = boundary.solve(G1_RD01)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == UI_INTERNAL_CONTRACT_CODE
        assert result.message == UI_INTERNAL_CONTRACT_MESSAGE

    @pytest.mark.parametrize(
        "invalid_vector",
        [
            [2, 2, 7, 3, 3],
            [5, 2, 7, 3, 3, 10],
            [2, 5, 7, 3, 3, 10],
            [2, 2, 0, 3, 3, 10],
            [2, 2, 7, 3, 3, 7],
        ],
        ids=[
            "length_five",
            "coord_row_out_of_range",
            "coord_col_out_of_range",
            "fill_out_of_range",
            "duplicate_fill_values",
        ],
    )
    def test_ut_f01_f02_invalid_vectors_rejected(
        self, invalid_vector: list[int]
    ) -> None:
        """UT-F01/F02 — contract violations return UI_INTERNAL_CONTRACT."""
        # Given
        mock_execute = Mock(return_value=invalid_vector)
        boundary = UIBoundary(execute=mock_execute)

        # When
        result = boundary.solve(G1_RD01)

        # Then
        assert isinstance(result, ErrorResponse)
        assert result.code == UI_INTERNAL_CONTRACT_CODE
