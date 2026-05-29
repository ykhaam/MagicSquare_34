"""Boundary output contract — U-OUT-01~03."""

from __future__ import annotations

from unittest.mock import Mock

from boundary.ui_boundary import UIBoundary
from tests.entity.conftest import G1_RD01


class TestUOut01Through03OutputContract:
    """U-OUT-01~03: success payload shape (Control execute mock/spy)."""

    def test_u_out_01_success_payload_length_six(self) -> None:
        """U-OUT-01 — success int[6] length contract (G1-RD01 + Mock)."""
        # Given
        mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
        boundary = UIBoundary(execute=mock_execute)
        matrix = G1_RD01

        # When
        result = boundary.solve(matrix)

        # Then
        assert result == [2, 2, 7, 3, 3, 10]
        assert len(result) == 6

    def test_u_out_02_success_coordinates_one_indexed(self) -> None:
        """U-OUT-02 — r,c coordinates in [1,4] (1-index, TS-B04)."""
        # Given
        mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
        boundary = UIBoundary(execute=mock_execute)
        matrix = G1_RD01

        # When
        result = boundary.solve(matrix)

        # Then
        assert isinstance(result, list)
        r1, c1, _n1, r2, c2, _n2 = result
        for coord in (r1, c1, r2, c2):
            assert 1 <= coord <= 4

    def test_u_out_03_success_fill_values_in_range(self) -> None:
        """U-OUT-03 — n1,n2 fill values in 1..16 (TS-B01/B02)."""
        # Given
        mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
        boundary = UIBoundary(execute=mock_execute)
        matrix = G1_RD01

        # When
        result = boundary.solve(matrix)

        # Then
        assert isinstance(result, list)
        _r1, _c1, n1, _r2, _c2, n2 = result
        assert 1 <= n1 <= 16
        assert 1 <= n2 <= 16
