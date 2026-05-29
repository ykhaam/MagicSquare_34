"""Boundary output contract RED skeletons — U-OUT-01~03."""

from __future__ import annotations

import pytest

class TestUOut01Through03OutputContract:
    """U-OUT-01~03: success payload shape (Control execute mock/spy in comments)."""

    def test_u_out_01_success_payload_length_six(self) -> None:
        """U-OUT-01 — success int[6] length contract (G1-RD01 + Mock)."""
        # Given
        # mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
        # boundary = UIBoundary(execute=mock_execute)
        # matrix = G1_RD01

        # When
        # result = boundary.solve(matrix)

        pytest.fail("RED: U-OUT-01 — 성공 반환 길이 6 (AC-FR05-04)")

    def test_u_out_02_success_coordinates_one_indexed(self) -> None:
        """U-OUT-02 — r,c coordinates in [1,4] (1-index, TS-B04)."""
        # Given
        # mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
        # boundary = UIBoundary(execute=mock_execute)
        # matrix = G1_RD01

        # When
        # result = boundary.solve(matrix)

        pytest.fail("RED: U-OUT-02 — 좌표 1-index [1,4] 범위")

    def test_u_out_03_success_fill_values_in_range(self) -> None:
        """U-OUT-03 — n1,n2 fill values in 1..16 (TS-B01/B02)."""
        # Given
        # mock_execute = Mock(return_value=[2, 2, 7, 3, 3, 10])
        # boundary = UIBoundary(execute=mock_execute)
        # matrix = G1_RD01

        # When
        # result = boundary.solve(matrix)

        pytest.fail("RED: U-OUT-03 — 채움 값 n1,n2 ∈ [1,16]")
